"""The balance point: is there a rate of relations-per-event at which a shape stops drifting as it grows?

From Allen's reading of ED's inflation language - "event-structure complexity outpacing event-production capacity"
(ED-Orientation, the ED-08 / 00.1 cosmology summary). Note 5 `B_Balance_Spec.md`, ledger C6.

Road P's generation growth, unchanged, with one knob: RHO, the relations per event the growth holds to as the
pattern grows (road P held it at whatever the start had; here it is set). The filter is OFF, so this is purely
about whether relations keep pace with events.

EXPECTATIONS, fixed in note 5 before this file was written:
  B1  a balance point exists - the drift in the reading changes sign as RHO varies          about 50%
  B2  if it exists, the reading there is between 2.5 and 3.5                                about 25%
  B3  reported, no expectation: the drift at each RHO, what each settles on, whether the two starts agree
Honest cost, recorded in note 5: RHO is a dial. A balance point at some RHO reading three dimensions is NOT a
derivation unless ED supplies that RHO - or unless stability itself picks it out, which is why this reads DRIFT
rather than dimension.
"""
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_11", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
from scipy.sparse.csgraph import connected_components       # noqa: E402
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402

OUT = os.path.join(HERE, "p_runs")
RHOS = (2, 3, 4, 5, 6, 8, 12, 16)
SEEDS = (1, 2, 3)
GROW = 4.0


def inherit_rho(adj, rng, rho, q=P.Q, ceil=P.CEIL):
    """Road P's inheritance, with relations per event held at rho instead of at whatever the start carried."""
    n_old = len(adj)
    kids, m = [], 0
    for _ in range(n_old):
        c = 2 if rng.random() < q else 1
        kids.append(list(range(m, m + c)))
        m += c
    new = [set() for _ in range(m)]

    def link(a, b):
        if a != b and b not in new[a] and len(new[a]) < ceil and len(new[b]) < ceil:
            new[a].add(b)
            new[b].add(a)
            return 1
        return 0

    target = int(round(rho / 2.0 * m))
    count, extras, base = 0, [], []
    for p in range(n_old):
        ks = kids[p]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                base.append((ks[i], ks[j]))
        for qn in adj[p]:
            if qn <= p:
                continue
            kq = kids[qn]
            mm = max(len(ks), len(kq))
            base.append((ks[int(rng.integers(len(ks)))], kq[int(rng.integers(len(kq)))]))
            for i in range(mm):
                extras.append((ks[i % len(ks)], kq[i % len(kq)]))
    for a, b in base:                                        # every parent relation is inherited first
        if count >= target:
            break
        count += link(a, b)
    if extras and count < target:                            # then top up to the rate being tested
        for k in rng.permutation(len(extras)):
            if count >= target:
                break
            a, b = extras[int(k)]
            count += link(a, b)
    return new


def giant(A):
    """The largest connected piece, and what share of the pattern it holds.

    Recorded: at low rates the pattern FALLS APART - relations cannot keep up with events - so the reading is taken
    on the largest piece and the share it holds is reported. A pattern in pieces has not kept its shape whatever
    the largest piece reads.
    """
    k, lab = connected_components(A, directed=False)
    if k == 1:
        return A, 1.0
    sizes = np.bincount(lab)
    big = int(np.argmax(sizes))
    idx = np.flatnonzero(lab == big)
    return A[idx][:, idx], float(sizes[big]) / A.shape[0]


def readat(name, adj, seed_ref=99):
    A = P.to_A(adj)
    Ag, frac = giant(A)
    rr = P.read(Ag)
    return (len(adj), rr["d_H"], P.reference(name, Ag.shape[0], np.random.default_rng(seed_ref)), round(frac, 3), rr)


def run(name, rho, seed):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng)}[name]()
    adj = P.to_adj(A0)
    n0 = len(adj)
    mid_target, end_target = 2.0 * n0, GROW * n0
    mid = None
    t0 = time.time()
    while len(adj) < end_target:
        adj = inherit_rho(adj, rng, rho)
        if mid is None and len(adj) >= mid_target:
            mid = readat(name, adj)
    end = readat(name, adj)
    rr = end[4]
    drift = None if (mid[1] is None or end[1] is None) else round(end[1] - mid[1], 3)
    # REVISION (recorded before the scan): a REAL shape's reading also drifts with size, so what counts is whether
    # the GAP to a real shape of the same kind grows. That is the quantity B1 is about.
    gaps = [None if (p[1] is None or p[2] is None) else round(p[1] - p[2], 3) for p in (mid, end)]
    gap_drift = None if None in gaps else round(gaps[1] - gaps[0], 3)
    return dict(start=name, rho=rho, seed=seed, mid=mid[:4], end=end[:4], drift=drift, gaps=gaps,
                gap_drift=gap_drift, md=rr["md"],
                small_world=rr["small_world"], per_event=rr["per_event"], whole=end[3],
                secs=round(time.time() - t0, 1))


def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    for name in ("ring", "grid3D"):
        for rho in RHOS:
            for seed in SEEDS:
                r = run(name, rho, seed)
                res.append(r)
                print("%-6s rho %d seed %d | reading %s at %d -> %s at %d (a real one reads %s) | drift %s | "
                      "gap %s -> %s (grows by %s) | in one piece %s | relations/event %.2f | %.0fs"
                      % (name, rho, seed, r["mid"][1], r["mid"][0], r["end"][1], r["end"][0], r["end"][2],
                         r["drift"], r["gaps"][0], r["gaps"][1], r["gap_drift"], r["whole"], r["per_event"],
                         r["secs"]), flush=True)
                json.dump(res, open(os.path.join(OUT, "balance.json"), "w"), indent=1, default=str)
    lines = []
    for r in res:
        lines.append("%-6s rho %d seed %d | %s -> %s (a real one reads %s) | drift %s | md %.1f | small world %s |"
                     " in one piece %s | relations/event %.2f"
                     % (r["start"], r["rho"], r["seed"], r["mid"][1], r["end"][1], r["end"][2], r["drift"], r["md"],
                        r["small_world"], r["whole"], r["per_event"]))
    for name in ("ring", "grid3D"):
        ds = []
        for rho in RHOS:
            got = [r["gap_drift"] for r in res if r["start"] == name and r["rho"] == rho
                   and r["gap_drift"] is not None and r["whole"] > 0.9]
            ds.append((rho, None if not got else round(float(np.mean(got)), 3)))
        lines.append("[%s] how fast the gap to a real shape grows, against rho (patterns in one piece only): %s"
                     % (name, ds))
        signs = [d for _, d in ds if d is not None]
        crossed = any(a < 0 < b or b < 0 < a for a, b in zip(signs, signs[1:]))
        lines.append("[%s] B1 (drift changes sign - a balance point) %s" % (name, crossed))
    text = "\n".join(lines)
    open(os.path.join(HERE, "b_balance.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
