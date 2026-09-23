"""Forward-growth check with narrow moves (D14: Allen adopted narrow both ways; note 12 option (a)).

Attempt 9's H4 run (q = 0.1, flips on, conditions only, n = 24, T = 150) with ONE change: merges are narrow (p10.tick10,
narrow = True). The small-world start is made exactly as H4's W1 (150 ticks of attempt 8's growth, q = 1, general merges),
then grown 150 ticks with narrow moves.

Runs: N1, N2 flat start, seeds 0 and 1; NW small-world start, seed 0.
Readings: mean distance every 10 ticks (flat 11.491); size; forced keeps and refused splits per tick; structure and both
budgets every tick; at the end, slice d_H and d_s, and the spacetime of the last 20 ticks against flat's 3.608 (C20 of A9).
Comparison (A9 H4, general merges): flat starts fell to 4.55 and 4.53; the small-world start stayed at 4.34.

Expected results, written down before this run:
  G0  narrow = False reproduces attempt 9's tick9 exactly (checked first, 5 ticks, n = 8); narrow_ok agrees with
      sa3_count.narrow_merges on every link-condition pair of a grown n = 8 slice.
  G1  structure and both budgets exact in every run.
  G2  moderate confidence: flat starts stay far flatter than H4's (mean distance at tick 150 >= 8), because flat events
      cannot merge and so the slice can only change by flips and short-lived children.
  G3  high confidence: the small-world start does NOT return toward flat (forward growth has no counting weight).
  Reported: size against the start (forced keeps may push it up), refused splits.
REVISION (recorded after the first run, before this one): the grid start (N1, N2) was frozen - its events cannot merge
under narrow moves, it sits above the link budget so every split is refused, and it has no paired-flip sites - so it
stayed flat because nothing happened (A9 C35's trap). Added NF1, NF2: the flat reference at ED's density (note 6,
16,280 events, exactly at the link budget, 15 per cent of events mergeable), every event's budget 1, seeds 0 and 1,
judged by the same G2 and the same 'what follows' rules against its own start (mean distance 11.594).
What follows (all branches go to stage B, the real test of counting; this check only informs it):
  flat starts within 10 per cent of 11.491 -> 'narrow moves keep flat under forward growth'.
  NW mean distance rises by >= 30 per cent of the gap to flat -> 'narrow forward growth moves toward flat'.
  flat starts fall as in H4 (below 6) -> 'forward growth with narrow moves still collapses; only counting can say more'.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_09", "model"))

N = 24
T = 150
KEEP = 20
Q = 0.1
FLAT_MD = 11.491
FLAT_ST = 3.608
JOBS = [("N1", 0, "flat"), ("N2", 1, "flat"), ("NW", 0, "small"), ("NF1", 0, "fref"), ("NF2", 1, "fref")]
OUT = os.path.join(HERE, "n1_runs")


def fresh(seed, n=N):
    from p10 import Slice10P
    from p3_core import SIGMA, FLAT_LINKS_PER_EVENT
    M = Slice10P(n)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    return M, round(FLAT_LINKS_PER_EVENT * V0) - M.E, round(FLAT_LINKS_PER_EVENT * V0), V0


def mean_distance(M, seed):
    from readings import bfs_distances
    A = M.adjacency()[0]
    rng = np.random.default_rng(900 + seed)
    src = rng.choice(A.shape[0], size=200, replace=False)
    d = bfs_distances(A, src)
    return float(d[np.isfinite(d)].mean())


def check_G0():
    from p9 import Slice9P
    from p3_core import SIGMA, FLAT_LINKS_PER_EVENT
    import sa3_count as s3
    A, pa, BL, V0 = fresh(3, 8)
    B = Slice9P(8)
    B.seed(3)
    rng = np.random.default_rng(3)
    B.S.b[:V0] = 1.0
    B.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    B.S.phi[:V0] = 0.0
    pb = pa
    same = True
    for _ in range(5):
        _, pa, _, _ = A.tick10(0.0, 0.0, pa, q=1.0, flip_frac=1.0, narrow=False)
        _, pb, _, _ = B.tick9(0.0, 0.0, pb, q=1.0, flip_frac=1.0)
        same &= (pa == pb) and np.array_equal(np.sort(A.edges(), axis=0), np.sort(B.edges(), axis=0))
    from p10 import narrow_ok
    verts = [int(v) for v in A.vertices()]
    nbr = {v: set(int(w) for w in A.neighbours(v)) for v in verts}
    agree = total = 0
    for v in verts:
        py = set(a for a, u in s3.narrow_merges(A, v, nbr))
        for a in nbr[v]:
            if not A.link_condition(v, a):
                continue
            pl = A.merge_plan(v, a)
            if pl is None or not A.allowed(pl, 10 ** 9, None, gone=v, cap=60)[0]:
                continue
            total += 1
            agree += bool(narrow_ok(A.S, v, a)) == (a in py)
    return dict(bit_for_bit=bool(same), narrow_pairs=total, narrow_agree=agree)


def do_job(job):
    tag, seed, start = job
    path = os.path.join(OUT, tag + ".json")
    if os.path.exists(path):
        return path, 0.0
    from p3_readings import slice_readings, spacetime_readings
    t0 = time.perf_counter()
    if start == "fref":
        import sa_flatref2 as fr
        from p10 import Slice10P
        from p3_core import SIGMA, FLAT_LINKS_PER_EVENT
        M, _, _, _ = fr.build(0)
        M.__class__ = Slice10P
        M.seed(seed)
        vs = M.vertices()
        rng = np.random.default_rng(seed)
        M.S.b[vs] = 1.0
        M.S.omega[vs] = 1.0 + SIGMA * rng.standard_normal(len(vs))
        M.S.phi[vs] = 0.0
        V0 = M.V
        BL = round(FLAT_LINKS_PER_EVENT * V0)
        pool = BL - M.E
    else:
        M, pool, BL, V0 = fresh(seed)
    if start == "small":
        for _ in range(T):
            r, pool, k, a = M.tick10(0.0, 0.0, pool, q=1.0, flip_frac=1.0, narrow=False)
    ok = dict(structure=True, budget=True, link=True)
    traj = [(0, mean_distance(M, 0), M.V)]
    forced, refused, merges = [], [], []
    snaps = []
    for t in range(1, T + 1):
        e = M.edges() if t > T - KEEP else None
        r, pool, kids, absd = M.tick10(0.0, 0.0, pool, q=Q, flip_frac=1.0, narrow=True)
        if e is not None:
            snaps.append((e, kids.copy(), absd.copy()))
        forced.append(r["forced"])
        refused.append(r["split_refused"] + r["refused_budget"])
        merges.append(r["merges"])
        if M.check():
            ok["structure"] = False
            break
        if abs(float(M.S.b[M.vertices()].sum()) - V0) > 1e-9 * V0:
            ok["budget"] = False
        if M.E + pool != BL:
            ok["link"] = False
        if t % 10 == 0:
            traj.append((t, mean_distance(M, t), M.V))
    snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
    sl = slice_readings(M, seed)
    st = spacetime_readings(snaps, 4000 + seed)
    res = dict(tag=tag, seed=seed, start=start, ok=ok, events=M.V, events_vs_start=M.V / V0,
               mean_degree=2 * M.E / max(M.V, 1), trajectory=traj, forced_mean=float(np.mean(forced)),
               refused_mean=float(np.mean(refused)), merges_mean=float(np.mean(merges)),
               slice={k: sl[k] for k in ("d_H", "d_s", "diameter", "mean_distance", "small_world")},
               spacetime=st.get("d_H"), seconds=time.perf_counter() - t0)
    json.dump(res, open(path, "w", encoding="utf-8"), default=str)
    return path, res["seconds"]


def report():
    L = ["Narrow-merge forward growth (q = %.1f, n = %d, T = %d). Flat mean distance %.3f, spacetime %.3f. "
         "A9 H4 (general merges): flat starts 4.55, 4.53 at tick 150; small-world start 4.34." % (Q, N, T, FLAT_MD, FLAT_ST)]
    g0 = json.load(open(os.path.join(OUT, "G0.json"), encoding="utf-8"))
    L.append("G0 %s" % g0)
    for tag, seed, start in JOBS:
        p = os.path.join(OUT, tag + ".json")
        if not os.path.exists(p):
            continue
        r = json.load(open(p, encoding="utf-8"))
        L.append("%s (%s start): ok %s | V %d (%.3f of start) meandeg %.2f | merges/tick %.1f forced/tick %.1f refused/tick %.1f | "
                 "slice d_H %s d_s %s | spacetime %s" % (tag, start, all(r["ok"].values()), r["events"], r["events_vs_start"],
                                                          r["mean_degree"], r["merges_mean"], r["forced_mean"],
                                                          r["refused_mean"], r["slice"]["d_H"], r["slice"]["d_s"],
                                                          r["spacetime"]))
        L.append("    mean distance (size) by tick: " + "  ".join("%d:%.2f(%d)" % (t, m, v) for t, m, v in r["trajectory"]))
    text = "\n".join(L)
    open(os.path.join(HERE, "n1_grow.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    g0p = os.path.join(OUT, "G0.json")
    if not os.path.exists(g0p):
        json.dump(check_G0(), open(g0p, "w", encoding="utf-8"))
    print(open(g0p).read(), flush=True)
    with Pool(3) as p:
        for path, sec in p.imap_unordered(do_job, JOBS):
            print("  %s %.0f s" % (os.path.basename(path), sec), flush=True)
    report()


if __name__ == "__main__":
    main()
