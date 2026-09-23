"""Settling G2: does where a pattern starts really change where it ends, or was that seed noise?

C5 found ring 3.99, cubic torus 4.60, web 4.57 on three seeds - a gap of 0.6 between starts against a seed spread
of 0.3-0.4, which passed G2's pre-registered rule but at only about twice the noise. A12 C11 and C12 (every start
converging on one end state) were therefore left UNREVISED. This settles it with ten seeds per start.

Nothing about the model changes. Same code, same settings, same two numbers (SIGMA_PASS 0.1, ALPHA 0.1), same
sizes. Only the number of seeds.

THE RULE, fixed before this file was run:
  G2a  the ring's mean reading is LOWER than the cubic torus's, with non-overlapping 95% intervals
       (mean +/- 1.96 standard errors). If the intervals overlap, G2 is NOT established, C5's claim is withdrawn,
       and A12 C11/C12's convergence finding stands as it is.
  G2b  reported: all three pairwise gaps with their intervals; how many runs give no reading at all; and whether
       the small-world flag still separates the starts (C5's side-finding: the cubic torus stopped being one).
A run whose reading is undefined is counted and excluded from the means, and that count is reported - excluding
them silently would bias whichever start fails to give a number.
"""
import io
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g_grad as G                                          # noqa: E402

OUT = os.path.join(HERE, "e_runs")
SEEDS = tuple(range(1, 11))
STARTS = ("ring", "grid3D", "web")


def ci(vals):
    v = np.asarray([x for x in vals if x is not None], dtype=float)
    if len(v) < 2:
        return None, None, None, len(v)
    m = float(v.mean())
    se = float(v.std(ddof=1) / np.sqrt(len(v)))
    return m, m - 1.96 * se, m + 1.96 * se, len(v)


def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    for name in STARTS:
        for seed in SEEDS:
            t0 = time.time()
            r = G.run(name, seed)
            res.append(r)
            print("%-6s seed %2d | reading %s | md %.1f | small world %s | relations/event %.2f | spread x%.2f |"
                  " void %s | %.0fs"
                  % (name, seed, r["final"]["d_H"], r["final"]["md"], r["final"]["small_world"],
                     r["final"]["per_event"], r["spread_ratio"], r["void"], time.time() - t0), flush=True)
            json.dump(res, open(os.path.join(OUT, "seeds.json"), "w"), indent=1, default=str)
    lines = []
    stats = {}
    for name in STARTS:
        runs = [r for r in res if r["start_name"] == name]
        m, lo, hi, k = ci([r["final"]["d_H"] for r in runs])
        undef = len(runs) - k
        sw = sum(1 for r in runs if r["final"]["small_world"])
        per = float(np.mean([r["final"]["per_event"] for r in runs]))
        stats[name] = (m, lo, hi, k)
        lines.append("%-6s | reading %s  95%% interval [%s, %s] from %d runs (%d gave no reading) | small world in"
                     " %d of %d | relations/event %.2f"
                     % (name, None if m is None else round(m, 3), None if lo is None else round(lo, 3),
                        None if hi is None else round(hi, 3), k, undef, sw, len(runs), per))
    r_m, r_lo, r_hi, _ = stats["ring"]
    g_m, g_lo, g_hi, _ = stats["grid3D"]
    ok = (r_m is not None and g_m is not None and r_hi < g_lo)
    lines.append("")
    lines.append("G2a (ring's reading lower than the 3D grid's, intervals not overlapping) %s" % ok)
    if not ok:
        lines.append("   ** NOT ESTABLISHED: C5's G2 is withdrawn and A12 C11/C12's convergence finding stands **")
    for a, b in (("ring", "grid3D"), ("ring", "web"), ("grid3D", "web")):
        am, alo, ahi, _ = stats[a]
        bm, blo, bhi, _ = stats[b]
        if am is not None and bm is not None:
            lines.append("G2b %s vs %s: gap %.3f, intervals [%.3f, %.3f] and [%.3f, %.3f], separated %s"
                         % (a, b, bm - am, alo, ahi, blo, bhi, (ahi < blo or bhi < alo)))
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "g_seeds.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
