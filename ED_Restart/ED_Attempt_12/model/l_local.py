"""Local sync: attempt 6's condition, at last, with no shared now and relations free to dissolve (D4, D5; C9).

A patch holds if the relations crossing its edge can carry the surplus of its clocks; the pattern holds if EVERY
patch does. Nothing happens at the same time anywhere - there is no shared now (D5). By max-flow/min-cut that whole
family of conditions is one exact question: does an assignment of carrying f exist with |f| <= K on every relation
and net outflow omega at every event? When it fails, the minimum cut NAMES the starved patch, so relations are
added exactly where attempt 6's argument says the shortfall is - not where a proxy guesses. And relations that
carry nothing DISSOLVE (D4), which is D13 applied in both directions for the first time.

Growth is road P's, unchanged: every event passes on once and is then spent, siblings and cousins linked,
relations per event carried forward.

EXPECTATIONS, fixed in note 7 before this file was written:
  L1  patterns satisfying the condition exist and growth reaches them without fragmenting          high
  L2  MAIN: shapes are kept - the ring and the 3D grid each still read as themselves after four-fold growth   ~50%
  L3  the one most worth seeing: a SMALL-WORLD start sheds relations and reads LOWER than it started          ~25%
  L4  reported: relations per event each start settles on, against ED's budget of 6.7 and C7's fragmentation
      threshold of about 5
Claude's, labelled: growth rate, start sizes, seeds, the bell-curve rate spread, and the pull K - the one number
ED does not supply - held at 1 in units of the rate spread and varied over 0.5, 1, 2 afterwards.
"""
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import maximum_flow, connected_components

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_11", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402

OUT = os.path.join(HERE, "p_runs")
K0 = 1.0
SCALE = 1000          # rates and capacities are integers for the max-flow; 1/1000 of a rate unit
CEIL = P.CEIL
SEEDS = (1, 2, 3)
GROW = 4.0


def _flow_problem(adj, omega, K):
    """Source -> events with surplus, events with deficit -> sink, each relation carrying at most K both ways."""
    n = len(adj)
    cap = int(round(K * SCALE))
    b = np.round(omega * SCALE).astype(np.int64)
    b -= int(round(b.sum() / n)) * np.ones(n, dtype=np.int64)     # keep it balanced after rounding
    b[0] -= int(b.sum())
    rows, cols, vals = [], [], []
    for i, s in enumerate(adj):
        for j in s:
            rows.append(i + 1)
            cols.append(j + 1)
            vals.append(cap)
    pos = np.flatnonzero(b > 0)
    neg = np.flatnonzero(b < 0)
    for i in pos:
        rows.append(0)
        cols.append(int(i) + 1)
        vals.append(int(b[i]))
    for i in neg:
        rows.append(int(i) + 1)
        cols.append(n + 1)
        vals.append(int(-b[i]))
    G = sp.csr_matrix((np.array(vals, dtype=np.int32), (rows, cols)), shape=(n + 2, n + 2))
    return G, int(b[pos].sum()), b


def holds_local(adj, omega, K=K0):
    """Can every patch shed its surplus through its own edge? Returns (ok, flow result, problem, supply)."""
    G, need, b = _flow_problem(adj, omega, K)
    if need == 0:
        return True, None, G, b
    res = maximum_flow(G, 0, len(adj) + 1)
    return int(res.flow_value) >= need, res, G, b


def starved_patch(G, res, n):
    """The minimum cut: the events on the source side are the patch whose edge cannot carry its surplus."""
    resid = (G - res.flow).tocsr()
    seen = np.zeros(n + 2, dtype=bool)
    seen[0] = True
    stack = [0]
    while stack:
        u = stack.pop()
        for k in range(resid.indptr[u], resid.indptr[u + 1]):
            v = int(resid.indices[k])
            if resid.data[k] > 0 and not seen[v]:
                seen[v] = True
                stack.append(v)
    return np.flatnonzero(seen[1:n + 1])


def repair(adj, omega, rng, K=K0, ceil=CEIL):
    """Add relations across the starved patch's edge until every patch can shed its surplus."""
    n = len(adj)
    added = 0
    for _ in range(400):
        ok, res, G, b = holds_local(adj, omega, K)
        if ok:
            return adj, added, True
        S = starved_patch(G, res, n)
        if len(S) == 0 or len(S) == n:
            return adj, added, False
        other = np.setdiff1d(np.arange(n), S, assume_unique=False)
        room_S = np.array([i for i in S if len(adj[i]) < ceil])
        room_o = np.array([i for i in other if len(adj[i]) < ceil])
        if len(room_S) == 0 or len(room_o) == 0:
            return adj, added, False
        want = np.abs(b[room_S])                                 # the most unmet surplus first
        order = room_S[np.argsort(-want)]
        for i in order[:max(8, n // 200)]:
            j = int(room_o[int(rng.integers(len(room_o)))])
            if j in adj[int(i)]:
                continue
            adj[int(i)].add(j)
            adj[j].add(int(i))
            added += 1
        if added > 20 * n:
            return adj, added, False
    return adj, added, False


def dissolve(adj, omega, rng, K=K0):
    """D4 + D13: a relation that carries nothing lets go, as long as every patch can still shed its surplus."""
    n = len(adj)
    ok, res, G, b = holds_local(adj, omega, K)
    if not ok or res is None:
        return adj, 0
    F = res.flow.tocoo()
    load = {}
    for u, v, f in zip(F.row, F.col, F.data):
        if 1 <= u <= n and 1 <= v <= n and f != 0:
            a, c = int(u) - 1, int(v) - 1
            key = (a, c) if a < c else (c, a)
            load[key] = load.get(key, 0) + abs(int(f))
    idle = [(i, j) for i in range(n) for j in adj[i] if i < j and load.get((i, j), 0) == 0]
    if not idle:
        return adj, 0
    rng.shuffle(idle)
    gone = 0
    step = max(1, len(idle) // 8)
    k = 0
    while k < len(idle):
        batch = idle[k:k + step]
        for i, j in batch:
            adj[i].discard(j)
            adj[j].discard(i)
        ok, _, _, _ = holds_local(adj, omega, K)
        if ok:
            gone += len(batch)
        else:
            for i, j in batch:                                   # that batch was needed after all: put it back
                adj[i].add(j)
                adj[j].add(i)
        k += step
    return adj, gone


def run(name, seed, K=K0, grow=GROW):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng),
          "web": lambda: N1.rand_regular(2000, rng)}[name]()
    adj = P.to_adj(A0)
    start = P.read(A0)
    target = grow * len(adj)
    t0, gen, trail, adds, goes, failed = time.time(), 0, [], [], [], False
    while len(adj) < target:
        adj, _ = P.inherit(adj, rng)
        omega = rng.normal(0, 1, len(adj))
        omega -= omega.mean()
        adj, a, ok = repair(adj, omega, rng, K)
        adj, g = dissolve(adj, omega, rng, K)
        adds.append(a)
        goes.append(g)
        if not ok:
            failed = True
            break
        gen += 1
        if gen % 4 == 0:
            trail.append((len(adj), round(sum(len(s) for s in adj) / len(adj), 2)))
    A = P.to_A(adj)
    k, lab = connected_components(A, directed=False)
    whole = float(np.bincount(lab).max()) / A.shape[0] if k > 1 else 1.0
    final = P.read(A if k == 1 else A[np.flatnonzero(lab == np.bincount(lab).argmax())][:,
                                       np.flatnonzero(lab == np.bincount(lab).argmax())])
    ref = P.reference(name, A.shape[0], np.random.default_rng(99))
    kept = (ref is not None and final["d_H"] is not None and abs(final["d_H"] - ref) <= P.TOL)
    if ref is None and final["d_H"] is None:
        kept = True
    return dict(start_name=name, seed=seed, K=K, n0=A0.shape[0], n=len(adj), start=start, final=final, ref_d_H=ref,
                kept=bool(kept), whole=round(whole, 3), failed=failed, added=int(sum(adds)), dissolved=int(sum(goes)),
                trail=trail[-4:], secs=round(time.time() - t0, 1))


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
            json.dump(res, open(os.path.join(OUT, "local.json"), "w"), indent=1, default=str)
    for K in (0.5, 2.0):                                         # does the answer depend on the one supplied number?
        r = run("grid3D", 1, K=K)
        res.append(r)
        print("grid3D pull %.1f | reading %s (a real one reads %s) | relations/event %.2f | added %d dissolved %d"
              % (K, r["final"]["d_H"], r["ref_d_H"], r["final"]["per_event"], r["added"], r["dissolved"]), flush=True)
        json.dump(res, open(os.path.join(OUT, "local.json"), "w"), indent=1, default=str)
    lines = []
    for r in res:
        lines.append("%-6s seed %d pull %.1f | %s -> %s (a real one reads %s) | md %.1f -> %.1f | small world %s ->"
                     " %s | kept %s | in one piece %s | relations/event %.2f -> %.2f | added %d dissolved %d"
                     % (r["start_name"], r["seed"], r["K"], r["start"]["d_H"], r["final"]["d_H"], r["ref_d_H"],
                        r["start"]["md"], r["final"]["md"], r["start"]["small_world"], r["final"]["small_world"],
                        r["kept"], r["whole"], r["start"]["per_event"], r["final"]["per_event"], r["added"],
                        r["dissolved"]))
    main_runs = [r for r in res if r["K"] == K0]
    l1 = all((not r["failed"]) and r["whole"] > 0.9 for r in main_runs)
    l2 = all(r["kept"] for r in main_runs if r["start_name"] in ("ring", "grid3D"))
    webs = [r for r in main_runs if r["start_name"] == "web"]
    l3 = all(w["final"]["d_H"] is not None and (w["start"]["d_H"] is None or w["final"]["d_H"] < w["start"]["d_H"])
             and w["final"]["md"] > w["start"]["md"] for w in webs)
    lines.append("L1 (patterns hold together without fragmenting) %s" % l1)
    lines.append("L2 (the ring and the 3D grid still read as themselves) %s" % l2)
    lines.append("L3 (a small-world start sheds relations and reads lower) %s" % l3)
    lines.append("L4 relations per event: %s"
                 % {r["start_name"]: round(float(np.mean([x["final"]["per_event"] for x in main_runs
                                                          if x["start_name"] == r["start_name"]])), 2)
                    for r in main_runs})
    text = "\n".join(lines)
    open(os.path.join(HERE, "l_local.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
