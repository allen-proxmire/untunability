"""H3 S0: can the whole-history weight find anything to choose between? (note 7; D10)

Two checks, both cheap, run before any rewind-and-regrow sampler is built.

S0-a, THE FLOOR'S TEETH. The floor is 'rates can match across the pattern' with ED's bounded pull
(A6 D7). A link can transmit at most the pull's limit, so a slice whose steady tick field needs a
larger difference across some link cannot lock its rates. With the rate spread raised (H3-Q4) so
that the flat slice uses half the pull's range, the floor passes a slice iff its largest steady link
strain is at most TWICE the flat slice's (flat: median over 8 reading seeds, 7.323 at n = 24).

S0-b, RESPONSIVENESS. From a conditions-only state at n = 24 after 100 ticks, run 30 more ticks
two ways: plainly, and 'best of 8' - at each tick grow eight candidate next slices and keep the one
the weight prefers (fewest directions = the largest mean distance, among those passing the floor).
If even that greedy selection cannot move the mean distance toward flat, a proper sampler at any
workable strength will not either.

Expected results, written down before this run:
  S0-a1 the flat slice passes the floor (by construction, at half the limit).
  S0-a2 a stringy slice - attempt 8's commitment-and-curvature run at n = 24, seed 0 - FAILS it.
        If it passes, the floor is still toothless and the rate spread must be revisited before S1.
  S0-a3 the conditions-only (small-world) slices PASS it: sync alone favours small worlds (A6 C22).
  S0-b  HONEST EXPECTATION: little movement - the small world is what the counting favours, and
        eight candidates a tick is a weak push. It passes if the best-of-8 run's final mean distance
        exceeds the plain run's by more than three times the plain run's tick-to-tick spread.
Exit: S0-a2 failing -> revisit the rate spread; S0-b failing -> recorded as 'weighting at workable
strength cannot move the shape at this size', and S1 is not built without Allen.
"""
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from p3 import Slice3P                                        # noqa: E402
from p3_ops import State                                      # noqa: E402
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING      # noqa: E402
from readings import bfs_distances                            # noqa: E402
from c3b import sync_steady_state                             # noqa: E402

N = 24
FLAT_STRAIN = 7.3232          # median over 8 reading seeds, A8 e3_pilot_runs/cal_n24.json
FLOOR = 2.0 * FLAT_STRAIN
WARM = 100
EXTRA = 30
K_CAND = 8


def copy_state(M):
    C = Slice3P.__new__(Slice3P)
    C.S = State(*[a.copy() for a in M.S])
    C.n = M.n
    return C


def mean_distance(M, seed):
    A = M.adjacency()[0]
    rng = np.random.default_rng(900 + seed)
    src = rng.choice(A.shape[0], size=200, replace=False)
    d = bfs_distances(A, src)
    return float(d[np.isfinite(d)].mean()), A


def floor_strain(A):
    return float(sync_steady_state(A, 0)["max_link_diff"])


def grow(M, pool, ticks, alpha=0.0, lam=0.0):
    for _ in range(ticks):
        r, pool, kids, absd = M.tick(alpha, lam, pool, s_max=None, cap=CEILING)
    return pool


def fresh(n, seed):
    M = Slice3P(n)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    return M, round(FLAT_LINKS_PER_EVENT * V0) - M.E


def main():
    out = {}
    t0 = time.perf_counter()
    # ---- S0-a: the floor on three kinds of slice
    F = Slice3P(N)
    md_flat, Af = mean_distance(F, 0)
    fa = {"flat": dict(strain=floor_strain(Af), mean_distance=md_flat)}
    S, pool = fresh(N, 0)
    grow(S, pool, 150, alpha=1.0, lam=1.0)                       # attempt 8's commitment + curvature, no veto
    md_s, As = mean_distance(S, 0)
    fa["stringy (A8 costs on)"] = dict(strain=floor_strain(As), mean_distance=md_s)
    M, pool = fresh(N, 0)
    pool = grow(M, pool, WARM)                                   # conditions only
    md_m, Am = mean_distance(M, 0)
    fa["small world (conditions only)"] = dict(strain=floor_strain(Am), mean_distance=md_m)
    for k, v in fa.items():
        v["passes_floor"] = v["strain"] <= FLOOR
    out["S0a"] = fa
    print("S0-a floor (pass iff strain <= %.2f):" % FLOOR, flush=True)
    for k, v in fa.items():
        print("  %-32s strain %7.3f  mean distance %.3f  -> %s" % (k, v["strain"], v["mean_distance"],
                                                                    "PASS" if v["passes_floor"] else "FAIL"), flush=True)
    # ---- S0-b: plain against best-of-8, from the same warmed state
    base, base_pool = M, pool
    plain = copy_state(base)
    ppool = base_pool
    traj_plain = []
    for t in range(EXTRA):
        ppool = grow(plain, ppool, 1)
        traj_plain.append(mean_distance(plain, t)[0])
    best = copy_state(base)
    bpool = base_pool
    traj_best, passes = [], []
    for t in range(EXTRA):
        cands = []
        for c in range(K_CAND):
            C = copy_state(best)
            C.seed(10_000 * (t + 1) + c)
            cp = grow(C, bpool, 1)
            md, A = mean_distance(C, t)
            st = floor_strain(A)
            cands.append((st <= FLOOR, md, st, C, cp))
        ok = [x for x in cands if x[0]]
        pick = max(ok, key=lambda x: x[1]) if ok else max(cands, key=lambda x: x[1])
        best, bpool = pick[3], pick[4]
        traj_best.append(pick[1])
        passes.append(len(ok))
        print("  tick %2d: plain %.3f | best-of-8 %.3f (%d/8 pass floor) | %.0f s"
              % (t + 1, traj_plain[t], pick[1], len(ok), time.perf_counter() - t0), flush=True)
    spread = float(np.std(np.diff(traj_plain))) if len(traj_plain) > 2 else float("nan")
    gain = traj_best[-1] - traj_plain[-1]
    moved = gain > 3 * spread
    out["S0b"] = dict(plain=traj_plain, best=traj_best, floor_passes=passes, spread=spread, gain=gain,
                      moved=bool(moved), flat_mean_distance=md_flat)
    text = ["H3 S0 at n = %d" % N, "",
            "S0-a floor (pass iff largest steady link strain <= %.2f = 2 x flat):" % FLOOR]
    for k, v in fa.items():
        text.append("  %-32s strain %7.3f  mean distance %.3f  -> %s" % (k, v["strain"], v["mean_distance"],
                                                                         "PASS" if v["passes_floor"] else "FAIL"))
    text += ["", "S0-b responsiveness over %d ticks from the same state:" % EXTRA,
             "  plain run mean distance %.3f -> %.3f (tick-to-tick spread %.4f)" % (traj_plain[0], traj_plain[-1], spread),
             "  best-of-%d  mean distance %.3f -> %.3f" % (K_CAND, traj_best[0], traj_best[-1]),
             "  gain %.3f against 3 x spread = %.4f -> %s" % (gain, 3 * spread, "MOVED" if moved else "did not move"),
             "  flat slice mean distance at this size: %.3f" % md_flat,
             "  total %.0f s" % (time.perf_counter() - t0)]
    txt = "\n".join(text)
    print(txt)
    with open("h3_s0.txt", "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    with open("h3_s0.json", "w", encoding="utf-8") as f:
        json.dump(out, f, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
