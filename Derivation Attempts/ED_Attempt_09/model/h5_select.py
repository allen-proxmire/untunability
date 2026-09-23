"""H5: does picking the best accumulate now that slices persist? (note 10; D12)

S0-b (C31) picked the best of eight next slices each tick and found a constant one-tick bump with
zero trend, because about 58 per cent of each slice was rewired every tick (C32). With mostly one
child (D11, q = 0.1) churn is about 6 per cent and slices persist (C37). This reruns the same
selection at q = 0.1, for longer, from two starts.

Each tick: grow K = 8 candidate next slices from the current one; keep the one with the largest mean
distance (the 'fewest directions' preference, C24) among those passing the floor (largest steady
link strain <= 2 x flat = 14.65; C30 found this floor toothless, and it is kept only so the rule
is the same as S0 - Allen has not chosen a sharper one).

Runs at n = 24, 100 ticks:
  B-W  from a small world (H1's n = 24 seed 0 re-grown 150 ticks at q = 1) - plain comparator: H4's W1
  B-F  from flat                                                          - plain comparator: H4's F1

Expected results, written down before this run (S0-b's end-point rule is replaced, since a one-tick
bump satisfied it - C31):
  H5-1  ACCUMULATION: over the last 50 ticks the selected run's mean distance has a positive slope,
        and its final value exceeds the plain comparator's final by more than 1.0.
  H5-2  record the share of the gap to flat closed: (selected - plain) / (11.491 - plain).
  H5-3  judged per A7 D40: the selected run's spacetime (last 20 ticks) within 0.5 of flat's 3.608
        reads 3+1.
  HONEST EXPECTATION: some accumulation now, well short of flat; and a risk, known from C30, that
  selecting on mean distance drifts toward stringy rather than flat, since stringy slices have the
  larger mean distance and the floor cannot stop them. Slice d_s is read at the end to see which.
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
from p3_ops import State                                      # noqa: E402
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT               # noqa: E402

N = 24
TICKS = 100
KEEP = 20
K_CAND = 8
Q = 0.1
FLOOR = 2.0 * 7.3232
FLAT_MD = 11.491
FLAT_ST = 3.608
OUT = "h5_runs"


def copy_state(M):
    C = Slice9P.__new__(Slice9P)
    C.S = State(*[a.copy() for a in M.S])
    C.n = M.n
    return C


def mdist(M, seed):
    from readings import bfs_distances
    A = M.adjacency()[0]
    rng = np.random.default_rng(900 + seed)
    d = bfs_distances(A, rng.choice(A.shape[0], size=200, replace=False))
    return float(d[np.isfinite(d)].mean()), A


def strain(A):
    from c3b import sync_steady_state
    return float(sync_steady_state(A, 0)["max_link_diff"])


def fresh(seed):
    M = Slice9P(N)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    return M, round(FLAT_LINKS_PER_EVENT * V0) - M.E


def do_job(tag):
    path = os.path.join(OUT, tag + ".json")
    if os.path.exists(path):
        return path, 0.0
    from p3_readings import slice_readings, spacetime_readings
    t0 = time.perf_counter()
    M, pool = fresh(0)
    if tag == "B-W":
        for _ in range(150):
            r, pool, k, a = M.tick9(0.0, 0.0, pool, q=1.0, flip_frac=1.0)
    traj = [(0, mdist(M, 0)[0])]
    passes, snaps = [], []
    for t in range(1, TICKS + 1):
        e = M.edges() if t > TICKS - KEEP else None
        cands = []
        for c in range(K_CAND):
            C = copy_state(M)
            C.seed(50_000 * t + c)
            r, cp, kids, absd = C.tick9(0.0, 0.0, pool, q=Q, flip_frac=1.0)
            md, A = mdist(C, t)
            st = strain(A)
            cands.append((st <= FLOOR, md, st, C, cp, kids, absd))
        ok = [x for x in cands if x[0]]
        pick = max(ok, key=lambda x: x[1]) if ok else max(cands, key=lambda x: x[1])
        M, pool = pick[3], pick[4]
        if e is not None:
            snaps.append((e, pick[5].copy(), pick[6].copy()))
        passes.append(len(ok))
        traj.append((t, pick[1]))
        if t % 10 == 0:
            print("  %s tick %3d: mean distance %.3f (%d/8 pass floor) %.0f s" % (tag, t, pick[1], len(ok), time.perf_counter() - t0), flush=True)
    snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
    sl = slice_readings(M, 0)
    st = spacetime_readings(snaps, 4000)
    res = dict(tag=tag, trajectory=traj, floor_passes=passes, events=M.V,
               mean_degree=2 * M.E / max(M.V, 1),
               slice={k: sl[k] for k in ("d_H", "d_s", "diameter", "mean_distance", "small_world", "neck_strain")},
               spacetime={k: st.get(k) for k in ("d_H", "r_lo", "r_max", "small_world", "events")},
               seconds=time.perf_counter() - t0)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, default=str)
    os.replace(tmp, path)
    return path, res["seconds"]


def report():
    plain = {}
    for tag, comp in (("B-W", "W1"), ("B-F", "F1")):
        c = json.load(open(os.path.join("h4_runs", comp + ".json"), encoding="utf-8"))
        plain[tag] = (comp, c["trajectory"])
    L = ["H5: best-of-%d selection at q = %.1f, n = %d, %d ticks. Flat: mean distance %.3f, spacetime %.3f." % (K_CAND, Q, N, TICKS, FLAT_MD, FLAT_ST), ""]
    for tag in ("B-W", "B-F"):
        p = os.path.join(OUT, tag + ".json")
        if not os.path.exists(p):
            continue
        r = json.load(open(p, encoding="utf-8"))
        tr = np.array(r["trajectory"], dtype=float)
        last = tr[tr[:, 0] >= TICKS - 50]
        slope = float(np.polyfit(last[:, 0], last[:, 1], 1)[0])
        comp, ptr = plain[tag]
        pt = dict((int(a), b) for a, b in ptr)
        p_at = pt.get(TICKS, pt[max(k for k in pt if k <= TICKS)])
        fin = float(tr[-1, 1])
        gain = fin - p_at
        share = gain / (FLAT_MD - p_at) if FLAT_MD != p_at else float("nan")
        acc = slope > 0 and gain > 1.0
        std = r["spacetime"].get("d_H")
        L.append("%s: start %.3f -> end %.3f | slope over last 50 ticks %+.4f/tick | plain %s at tick %d: %.3f | gain %+.3f | "
                 "gap to flat closed %.0f%% | H5-1 %s" % (tag, tr[0, 1], fin, slope, comp, TICKS, p_at, gain, 100 * share,
                                                          "ACCUMULATES" if acc else "does not accumulate"))
        L.append("    end slice: d_H %s d_s %s diameter %s mean degree %.2f strain %.2f | spacetime %s -> %s" % (
            r["slice"]["d_H"] and round(r["slice"]["d_H"], 3), r["slice"]["d_s"] and round(r["slice"]["d_s"], 3),
            r["slice"]["diameter"], r["mean_degree"], r["slice"]["neck_strain"], std and round(std, 3),
            "READS 3+1" if std and abs(std - FLAT_ST) <= 0.5 else "does not"))
        L.append("    selected mean distance every 10 ticks: " + "  ".join("%d:%.2f" % (int(a), b) for a, b in tr if int(a) % 10 == 0))
    text = "\n".join(L)
    with open("h5_select.txt", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    with Pool(2) as pool:
        for path, sec in pool.imap_unordered(do_job, ["B-W", "B-F"]):
            print("  %s done %.0f s" % (os.path.basename(path), sec), flush=True)
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
