"""Flat reference by adding events (note 5, C12; Allen D6: 'a, build it by adding events and count it').

Start from the n = 24 flat grid (13,824 events, 96,768 links, 7 per event). Split valence-4 links (ED's own edge split:
+1 event, +5 links) in a random order, skipping any link that is no longer valence 4 or whose ends were already
the ends of a split, until the link count equals round(FLAT_LINKS_PER_EVENT * V) exactly. Seed 0.

Checks and verdict, written down before this run (C12, revised rule):
  B0  structure check clean; links exactly round(6.699 V).
  B1  extended by construction: for 200 grid events as sources, no distance to another grid event is shorter than on
      the grid (every one >= the grid's).
  Claude's expectation (moderate): s below the grid's 0.69348 but above every grown slice (0.621-0.641).
Verdict (revision (b), D5; margin 0.00583 from stage A):
  B0 or B1 fails -> recorded, stop and report.
  reference above every grown slice (F1, W1, both seeds) by more than the margin -> "counting leans toward flat at
      one tick" -> spec stage B in 3D on paper.
  a grown slice above the reference by more than the margin -> "counting leans toward small worlds".
  otherwise -> "too close": take stock with Allen.
"""
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sa_count as sc                                           # noqa: E402

OUT = os.path.join(HERE, "sa_runs", "3D_FREF2_s0.json")
MARGIN = 0.00583


def build(seed=0):
    from p3_core import FLAT_LINKS_PER_EVENT
    M, pool, BL, V0 = sc.fresh3(24, seed)
    grid_A = M.adjacency()[0]
    edges = M.edges()
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(edges))
    used = set()
    k = 0
    # FIX (recorded after the first build missed by one link, 109,028 vs 109,027): +5-link splits alone cannot land
    # exactly on round(6.699 V); three valence-6 splits (+7 each) first make it exact (a = 2453, b = 3 solves it).
    six = 0
    for i in order:
        x, u = int(edges[i, 0]), int(edges[i, 1])
        if six == 3:
            break
        if x in used or u in used or M.valence(x, u) != 6:
            continue
        M.split(x, u)
        used.update((x, u))
        six += 1
        k += 1
    for i in order:
        x, u = int(edges[i, 0]), int(edges[i, 1])
        if round(FLAT_LINKS_PER_EVENT * M.V) == M.E:
            break
        if x in used or u in used or M.valence(x, u) != 4:
            continue
        if M.E + 5 < round(FLAT_LINKS_PER_EVENT * (M.V + 1)):
            break                                                # would overshoot: stop and report
        M.split(x, u)
        used.update((x, u))
        k += 1
    return M, grid_A, V0, k


def main():
    from p3_core import FLAT_LINKS_PER_EVENT
    from readings import bfs_distances
    t0 = time.perf_counter()
    M, grid_A, V0, k = build(0)
    target = round(FLAT_LINKS_PER_EVENT * M.V)
    notes = M.check()
    A, ids, pos = M.adjacency()[:3]
    rng = np.random.default_rng(900)
    src = rng.choice(V0, size=200, replace=False)                # grid events keep their ids 0..V0-1
    d_grid = bfs_distances(grid_A, src)
    d_new = bfs_distances(A, np.array([pos[int(s)] for s in src]))
    cols = np.array([pos[v] for v in range(V0)])
    shorter = int((d_new[:, cols] < d_grid).sum())
    arr, deg, tot = sc.options3(M)
    out = sc.summarise(arr, deg, sc.mean_distance(A, 0), M.V)
    out.update(dim=3, kind="FREF2", seed=0, splits=k, links=int(M.E), target=int(target),
               ok=dict(structure=not notes, at_budget=bool(M.E == target), no_shorter=bool(shorter == 0)),
               grid_pairs_shorter=shorter, grid_mean_distance_on_grid_pairs=float(d_new[:, cols].mean()),
               totals=tot, seconds=time.perf_counter() - t0)
    json.dump(out, open(OUT, "w", encoding="utf-8"))
    ref = out["s"]
    grown = {"%s_s%d" % (kk, s): json.load(open(os.path.join(HERE, "sa_runs", "3D_%s_s%d.json" % (kk, s))))["s"]
             for kk in ("F1", "W1") for s in (0, 1)}
    L = ["reference: V %d (splits %d), links %d / target %d, structure %s, grid pairs shorter %d, mean distance %.3f "
         "(grid pairs %.3f; grid 11.491), a_mean %.3f a_sd %.3f, degree mean %.3f sd %.3f max %d" % (
             M.V, k, M.E, target, not notes, shorter, out["mean_distance"], out["grid_mean_distance_on_grid_pairs"],
             out["a_mean"], out["a_sd"], out["deg_mean"], out["deg_sd"], out["deg_max"]),
         "s reference %.5f (grid 0.69348); totals %s" % (ref, tot),
         "delta s grown - reference: " + ", ".join("%s %+.5f (V*ds %+.0f)" % (g, v - ref, 0) for g, v in grown.items())]
    if not all(out["ok"].values()):
        L.append("VERDICT: B0 or B1 failed - recorded, stop and report.")
    elif all(ref - v > MARGIN for v in grown.values()):
        L.append("VERDICT: counting leans toward flat at one tick -> spec stage B in 3D on paper.")
    elif any(v - ref > MARGIN for v in grown.values()):
        L.append("VERDICT: counting leans toward small worlds.")
    else:
        L.append("VERDICT: too close -> take stock with Allen.")
    text = "\n".join(L)
    open(os.path.join(HERE, "sa_flatref2.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
