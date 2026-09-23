"""Stage A, flat reference at ED's link density (Allen D5: option (b) with (c) folded in, reference first).

The flat cube grid has 7 links per event; ED's link budget sets 6.699 (A7 C66). No regular triangulation has 6.699
(it is the flat mean edge valence 5.104, not an integer), so the reference is the flat grid moved to ED's density with
as little disturbance as possible: single 2-3 / 3-2 flips at the fixed vertex set, uniform-measure proposal
corrections as in attempt 8's flip_randomize, plus a bias exp(-beta * dE) toward fewer links, stopped the first time
the link count equals BL = round(6.699 V). The ceiling (60) applies. beta = 2 (labelled; a construction setting).
Then the slice is counted exactly as in sa_count.py.

Expected results, written down before this run:
  R0  the reference reaches exactly BL links with a clean structure check, and stays extended: mean distance within
      5 per cent of the grid's 11.491. If it falls further, it is not a flat reference: recorded, stop and report.
  R1  Claude's expectation (moderate confidence): its s is somewhat below the grid's 0.69348 (fewer links, fewer
      options) but above every grown slice (F1, W1 at 0.621-0.641).
Exit, by revision (b) (D5: compare only slices ED allows; recorded after stage A's results):
  reference above every grown slice (F1, W1, both seeds) by more than the stage A margin 0.00583
      -> "counting leans toward flat at one tick" -> spec stage B in 3D on paper.
  a grown slice above the reference by more than the margin -> "counting leans toward small worlds".
  otherwise -> "too close": take stock with Allen.
"""
import json
import math
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sa_count as sc                                           # noqa: E402

BETA = 2.0
OUT = os.path.join(HERE, "sa_runs", "3D_FREF_s0.json")


def to_budget(M, BL, seed, beta=BETA, max_attempts=50_000_000):
    from p3 import flip23_plan, flip32_plan, B_A
    from p3_ops import n3_after, apply_plan, C_T, C_V3, C_E
    from p3_core import rng_float, rng_below
    S = M.S
    M.seed(1000 + seed)
    acc = 0
    att = 0
    while S.ctr[C_E] != BL and att < max_attempts:
        att += 1
        if rng_float(S.rs) < 0.5:
            tid = S.t_items[rng_below(S.rs, S.ctr[C_T])]
            nr, na = flip23_plan(S, tid, rng_below(S.rs, 4), B_A)
            if nr < 0:
                continue
            n3a = max(int(n3_after(S, B_A, nr, na)), 1)
            corr = 2.0 * S.ctr[C_T] / n3a
            dE = 1
        else:
            if S.ctr[C_V3] == 0:
                continue
            slot = S.e3_items[rng_below(S.rs, S.ctr[C_V3])]
            nr, na = flip32_plan(S, slot, B_A)
            if nr < 0:
                continue
            corr = S.ctr[C_V3] / (2.0 * (S.ctr[C_T] - 1))
            dE = -1
        pl = (S.buf_rem[B_A:B_A + nr].copy(), S.buf_add[B_A:B_A + na].copy())
        if not M.allowed(pl, sc.BIG, None, cap=sc.CAP)[0]:
            continue
        nr, na = M._load(pl)
        p = corr * math.exp(-beta * dE)
        if p >= 1.0 or rng_float(S.rs) < p:
            apply_plan(S, B_A, nr, na)
            acc += 1
    return acc, att


def main():
    t0 = time.perf_counter()
    M, pool, BL, V0 = sc.fresh3(24, 0)
    acc, att = to_budget(M, BL, 0)
    notes = M.check()
    arr, deg, tot = sc.options3(M)
    A = M.adjacency()[0]
    out = sc.summarise(arr, deg, sc.mean_distance(A, 0), M.V)
    out.update(dim=3, kind="FREF", seed=0, ok=dict(structure=not notes, at_budget=bool(M.E == BL)),
               links=int(M.E), BL=int(BL), flips_accepted=acc, attempts=att, totals=tot, beta=BETA,
               seconds=time.perf_counter() - t0)
    json.dump(out, open(OUT, "w", encoding="utf-8"))
    print(json.dumps(out, indent=1))
    ref = out["s"]
    grown = {}
    for k in ("F1", "W1"):
        for s in (0, 1):
            grown["%s_s%d" % (k, s)] = json.load(open(os.path.join(HERE, "sa_runs", "3D_%s_s%d.json" % (k, s))))["s"]
    margin = 0.00583
    md_ok = abs(out["mean_distance"] - 11.491) <= 0.05 * 11.491
    L = ["reference s %.5f (grid 0.69348), links %d / BL %d, flips %d of %d attempts, mean distance %.3f (grid 11.491), "
         "degree sd %.3f max %d" % (ref, out["links"], BL, acc, att, out["mean_distance"], out["deg_sd"], out["deg_max"]),
         "delta s grown - reference: " + ", ".join("%s %+.5f" % (k, v - ref) for k, v in grown.items())]
    if not (out["ok"]["structure"] and out["ok"]["at_budget"]) or not md_ok:
        L.append("VERDICT: R0 failed - not a flat reference at ED's density (recorded; stop and report).")
    elif all(ref - v > margin for v in grown.values()):
        L.append("VERDICT: counting leans toward flat at one tick -> spec stage B in 3D on paper.")
    elif any(v - ref > margin for v in grown.values()):
        L.append("VERDICT: counting leans toward small worlds.")
    else:
        L.append("VERDICT: too close -> take stock with Allen.")
    text = "\n".join(L)
    open(os.path.join(HERE, "sa_flatref.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
