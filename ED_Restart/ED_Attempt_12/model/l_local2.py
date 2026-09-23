"""Local sync, with D6: a relation persists while it is part of a commitment.

C11's run let a relation go the moment it carried nothing in one generation's flow. With rates redrawn each
generation that churned the pattern - about 13,000 relations added and 15,000 let go in a run ending with 25,000 -
and the churn is a plausible cause of the randomising. That rule was Claude's reading of D13, not ED's.

D6 (Allen): a relation persists while it is part of a commitment. Taken here, with no new number:
    a relation that has EVER carried something is part of a commitment and PERSISTS;
    a relation that has NEVER carried anything was never part of one and LAPSES.
A relation made by repair starts uncommitted. A relation inherited by descent carries its parent relation's
standing forward - which is also the plainest reading of Allen's "to persist is to update".

Everything else is C11's model unchanged: A6's condition as an exact max-flow feasibility (every patch sheds its
surplus through its own edge, no shared now, no patch-size dial), relations added across the minimum cut that names
the starved patch, growth by passing on once and being spent with neighbourhoods inherited.

EXPECTATIONS, fixed before this file was run:
  M1  patterns still hold together without fragmenting                                              high
  M2  MAIN: shapes are kept - the ring and the 3D grid still read as themselves                     about 35%
  M3  the churn falls sharply - far fewer relations let go than in C11. If it does not, the rule has not bitten
      and the rerun says nothing                                                                    high
  M4  reported: relations per event each start settles on, and whether the starts still converge on one end state
"""
import json
import os
import sys
import time
import numpy as np
from scipy.sparse.csgraph import connected_components

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_11", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402
import l_local as L                                         # noqa: E402

OUT = os.path.join(HERE, "p_runs")
SEEDS = (1, 2, 3)
GROW = 4.0


def key(a, b):
    return (a, b) if a < b else (b, a)


def inherit_marked(adj, committed, rng, q=P.Q, ceil=P.CEIL):
    """Road P's inheritance, carrying each relation's standing forward to the relation that descends from it."""
    n_old = len(adj)
    r_old = sum(len(s) for s in adj)
    kids, m = [], 0
    for _ in range(n_old):
        c = 2 if rng.random() < q else 1
        kids.append(list(range(m, m + c)))
        m += c
    new = [set() for _ in range(m)]
    mark = set()

    def link(a, b, from_parent=None):
        if a != b and b not in new[a] and len(new[a]) < ceil and len(new[b]) < ceil:
            new[a].add(b)
            new[b].add(a)
            if from_parent is not None and from_parent in committed:
                mark.add(key(a, b))
            return 1
        return 0

    count, extras, base = 0, [], []
    for p in range(n_old):
        ks = kids[p]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                base.append((ks[i], ks[j], None))            # siblings are new relations, uncommitted
        for qn in adj[p]:
            if qn <= p:
                continue
            kq = kids[qn]
            mm = max(len(ks), len(kq))
            base.append((ks[int(rng.integers(len(ks)))], kq[int(rng.integers(len(kq)))], key(p, qn)))
            for i in range(mm):
                extras.append((ks[i % len(ks)], kq[i % len(kq)], key(p, qn)))
    target = int(round(r_old / 2.0 * m / n_old))
    for a, b, src in base:
        if count >= target:
            break
        count += link(a, b, src)
    if extras and count < target:
        for k in rng.permutation(len(extras)):
            if count >= target:
                break
            a, b, src = extras[int(k)]
            count += link(a, b, src)
    return new, mark


def loads(adj, omega, K):
    """Which relations carried something, from the flow the condition is checked with."""
    ok, res, G, b = L.holds_local(adj, omega, K)
    carried = set()
    if res is not None:
        F = res.flow.tocoo()
        n = len(adj)
        for u, v, f in zip(F.row, F.col, F.data):
            if 1 <= u <= n and 1 <= v <= n and f > 0:
                carried.add(key(int(u) - 1, int(v) - 1))
    return ok, carried


def dissolve_uncommitted(adj, committed, omega, rng, K):
    """D6: only a relation that has NEVER carried anything may lapse."""
    ok, carried = loads(adj, omega, K)
    committed |= carried                                     # what carried now is part of a commitment from now on
    if not ok:
        return adj, committed, 0
    idle = [(i, j) for i in range(len(adj)) for j in adj[i] if i < j and key(i, j) not in committed]
    if not idle:
        return adj, committed, 0
    rng.shuffle(idle)
    gone, step, k = 0, max(1, len(idle) // 8), 0
    while k < len(idle):
        batch = idle[k:k + step]
        for i, j in batch:
            adj[i].discard(j)
            adj[j].discard(i)
        ok2, _, _, _ = L.holds_local(adj, omega, K)
        if ok2:
            gone += len(batch)
        else:
            for i, j in batch:
                adj[i].add(j)
                adj[j].add(i)
        k += step
    return adj, committed, gone


def run(name, seed, K=L.K0, grow=GROW):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng),
          "web": lambda: N1.rand_regular(2000, rng)}[name]()
    adj = P.to_adj(A0)
    committed = set()                                        # the start's relations have carried nothing yet
    start = P.read(A0)
    target, t0, gen = grow * len(adj), time.time(), 0
    adds, goes, failed = [], [], False
    while len(adj) < target:
        adj, committed = inherit_marked(adj, committed, rng)
        omega = rng.normal(0, 1, len(adj))
        omega -= omega.mean()
        adj, a, ok = L.repair(adj, omega, rng, K)
        if not ok:
            failed = True
            adds.append(a)
            break
        adj, committed, g = dissolve_uncommitted(adj, committed, omega, rng, K)
        adds.append(a)
        goes.append(g)
        gen += 1
    A = P.to_A(adj)
    k, lab = connected_components(A, directed=False)
    big = np.flatnonzero(lab == np.bincount(lab).argmax()) if k > 1 else None
    whole = 1.0 if k == 1 else float(len(big)) / A.shape[0]
    final = P.read(A if k == 1 else A[big][:, big])
    ref = P.reference(name, A.shape[0], np.random.default_rng(99))
    kept = (ref is not None and final["d_H"] is not None and abs(final["d_H"] - ref) <= P.TOL)
    if ref is None and final["d_H"] is None:
        kept = True
    return dict(start_name=name, seed=seed, K=K, n0=A0.shape[0], n=len(adj), start=start, final=final, ref_d_H=ref,
                kept=bool(kept), whole=round(whole, 3), failed=failed, added=int(sum(adds)),
                dissolved=int(sum(goes)), secs=round(time.time() - t0, 1))


def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    for name in ("ring", "grid3D", "web"):
        for seed in SEEDS:
            r = run(name, seed)
            res.append(r)
            print("%-6s seed %d | n %5d -> %5d | reading %s -> %s (a real one reads %s) | kept %s | in one piece %s"
                  " | relations/event %.2f -> %.2f | added %d dissolved %d | %.0fs"
                  % (name, seed, r["n0"], r["n"], r["start"]["d_H"], r["final"]["d_H"], r["ref_d_H"], r["kept"],
                     r["whole"], r["start"]["per_event"], r["final"]["per_event"], r["added"], r["dissolved"],
                     r["secs"]), flush=True)
            json.dump(res, open(os.path.join(OUT, "local2.json"), "w"), indent=1, default=str)
    for K in (0.5, 2.0):
        r = run("grid3D", 1, K=K)
        res.append(r)
        print("grid3D pull %.1f | reading %s (a real one reads %s) | relations/event %.2f | added %d dissolved %d"
              % (K, r["final"]["d_H"], r["ref_d_H"], r["final"]["per_event"], r["added"], r["dissolved"]), flush=True)
        json.dump(res, open(os.path.join(OUT, "local2.json"), "w"), indent=1, default=str)
    lines = []
    for r in res:
        lines.append("%-6s seed %d pull %.1f | %s -> %s (a real one reads %s) | md %.1f -> %.1f | small world %s ->"
                     " %s | kept %s | in one piece %s | relations/event %.2f -> %.2f | added %d dissolved %d"
                     % (r["start_name"], r["seed"], r["K"], r["start"]["d_H"], r["final"]["d_H"], r["ref_d_H"],
                        r["start"]["md"], r["final"]["md"], r["start"]["small_world"], r["final"]["small_world"],
                        r["kept"], r["whole"], r["start"]["per_event"], r["final"]["per_event"], r["added"],
                        r["dissolved"]))
    main_runs = [r for r in res if r["K"] == L.K0]
    m1 = all((not r["failed"]) and r["whole"] > 0.9 for r in main_runs)
    m2 = all(r["kept"] for r in main_runs if r["start_name"] in ("ring", "grid3D"))
    lines.append("M1 (patterns hold together without fragmenting) %s" % m1)
    lines.append("M2 (the ring and the 3D grid still read as themselves) %s" % m2)
    lines.append("M3 dissolved per run: %s   (C11 let go 12,600-17,300)"
                 % {r["start_name"]: int(np.mean([x["dissolved"] for x in main_runs
                                                  if x["start_name"] == r["start_name"]])) for r in main_runs})
    lines.append("M4 relations per event: %s   (C11 settled at 3.0 everywhere)"
                 % {r["start_name"]: round(float(np.mean([x["final"]["per_event"] for x in main_runs
                                                          if x["start_name"] == r["start_name"]])), 2)
                    for r in main_runs})
    text = "\n".join(lines)
    open(os.path.join(HERE, "l_local2.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
