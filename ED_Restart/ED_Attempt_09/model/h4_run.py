"""H4: mostly exactly one child (D11; note 9). Does a slice keep - or regain - its shape?

Allen decided (D11): an event has mostly exactly one child. The model draws from the old spread
(geometric, which A7 C1 took from CDT) with probability q = 0.1, and otherwise gives exactly one
child - so about 5 per cent of events merge away each tick instead of about 50. q = 0.1 is a new
setting, labelled. Growth otherwise has the conditions only: budget, link budget, ceiling; no
costs, no veto (as H1).

Two sources of churn are separated. Merges and splits are now rare; the paired cut-and-rejoin
sweep (V/2 attempts a tick, accepted freely with no cost) still runs, and is switched off in one
run to see what it does alone.

Runs at n = 24, T = 150, mean distance tracked every 10 ticks (flat: 11.491):
  F1, F2  flat start, flips on, seeds 0 and 1
  F0      flat start, flips OFF, seed 0
  W1      SMALL-WORLD start (H1's n = 24 seed 0, re-grown 150 ticks at q = 1), then 150 ticks here
End readings: mean distance, slice d_H and d_s, curvature median, and the SPACETIME of the last 20
ticks against the calibrated flat spacetime 3.608 (C20) - judged per A7 D40.

Expected results, written down before this run:
  H4-a  structure and both budgets exact; merges about 5 per cent of events per tick.
  H4-b  F0 stays near flat (mean distance within 10 per cent of 11.491) - but a flat START that
        stays flat is weak evidence: nothing happened to it.
  H4-c  HONEST EXPECTATION: F1 and F2 still drift from flat toward a small world, only more slowly,
        because the free paired flips alone randomise the wiring.
  H4-d  HONEST EXPECTATION: W1 does NOT return toward flat - nothing in the rule prefers flat.
Pass: a spacetime within 0.5 of flat's 3.608 READS 3+1. W1 passing would be the decisive result -
the rule selecting flat, not merely preserving it.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from p9 import Slice9P                                        # noqa: E402
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING      # noqa: E402

N = 24
T = 150
KEEP = 20
Q = 0.1
FLAT_MD = 11.491
FLAT_ST = 3.608
JOBS = [("F1", 0, 1.0, "flat"), ("F2", 1, 1.0, "flat"), ("F0", 0, 0.0, "flat"), ("W1", 0, 1.0, "small")]
OUT = "h4_runs"


def mean_distance(M, seed):
    from readings import bfs_distances
    A = M.adjacency()[0]
    rng = np.random.default_rng(900 + seed)
    src = rng.choice(A.shape[0], size=200, replace=False)
    d = bfs_distances(A, src)
    return float(d[np.isfinite(d)].mean())


def fresh(seed):
    M = Slice9P(N)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    return M, round(FLAT_LINKS_PER_EVENT * V0) - M.E, round(FLAT_LINKS_PER_EVENT * V0), V0


def do_job(job):
    tag, seed, ff, start = job
    path = os.path.join(OUT, tag + ".json")
    if os.path.exists(path):
        return path, 0.0
    from p3_readings import slice_readings, spacetime_readings
    from h1_curvature import curvature_sample
    t0 = time.perf_counter()
    M, pool, BL, V0 = fresh(seed)
    if start == "small":
        for _ in range(T):                                   # H1's growth: the old spread, flips on
            r, pool, k, a = M.tick9(0.0, 0.0, pool, q=1.0, flip_frac=1.0)
    ok = dict(structure=True, budget=True, link=True)
    traj = [(0, mean_distance(M, 0))]
    turnover = []
    snaps = []
    for t in range(1, T + 1):
        e = M.edges() if t > T - KEEP else None
        r, pool, kids, absd = M.tick9(0.0, 0.0, pool, q=Q, flip_frac=ff)
        if e is not None:
            snaps.append((e, kids.copy(), absd.copy()))
        turnover.append(r["merges"] / max(r["size"], 1))
        if M.check():
            ok["structure"] = False
            break
        if abs(float(M.S.b[M.vertices()].sum()) - V0) > 1e-9 * V0:
            ok["budget"] = False
        if M.E + pool != BL:
            ok["link"] = False
        if t % 10 == 0:
            traj.append((t, mean_distance(M, t)))
    snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
    sl = slice_readings(M, seed)
    st = spacetime_readings(snaps, 4000 + seed)
    cu = curvature_sample(M.adjacency()[0], seed)
    res = dict(tag=tag, seed=seed, flip_frac=ff, start=start, q=Q, ok=ok, events=M.V, events_vs_start=M.V / V0,
               mean_degree=2 * M.E / max(M.V, 1), trajectory=traj, turnover_mean=float(np.mean(turnover)),
               slice={k: sl[k] for k in ("d_H", "d_s", "diameter", "mean_distance", "small_world", "r_lo", "r_max")},
               spacetime={k: st.get(k) for k in ("d_H", "r_lo", "r_max", "small_world", "events")},
               curvature_median=cu["median"], seconds=time.perf_counter() - t0)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, default=str)
    os.replace(tmp, path)
    return path, res["seconds"]


def report():
    L = ["H4: mostly exactly one child (q = %.1f), n = %d, T = %d. Flat: mean distance %.3f, spacetime %.3f."
         % (Q, N, T, FLAT_MD, FLAT_ST), ""]
    for tag, seed, ff, start in JOBS:
        p = os.path.join(OUT, tag + ".json")
        if not os.path.exists(p):
            continue
        r = json.load(open(p, encoding="utf-8"))
        st = r["spacetime"].get("d_H")
        L.append("%s (%s start, flips %s): ok %s | turnover %.1f%%/tick | V %d meandeg %.2f | slice d_H %s d_s %s diam %s | "
                 "curv %.3f | spacetime %s -> %s" % (
                     tag, start, "on" if ff else "OFF", all(r["ok"].values()), 100 * r["turnover_mean"], r["events"],
                     r["mean_degree"], r["slice"]["d_H"] and round(r["slice"]["d_H"], 3),
                     r["slice"]["d_s"] and round(r["slice"]["d_s"], 3), r["slice"]["diameter"], r["curvature_median"],
                     st and round(st, 3), ("READS 3+1" if st and abs(st - FLAT_ST) <= 0.5 else "does not" if st else "-")))
        L.append("    mean distance by tick: " + "  ".join("%d:%.2f" % (t, m) for t, m in r["trajectory"]))
    text = "\n".join(L)
    with open("h4_run.txt", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.perf_counter()
    with Pool(2) as pool:
        for path, sec in pool.imap_unordered(do_job, JOBS):
            print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec, (time.perf_counter() - t0) / 3600), flush=True)
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
