"""Making both halves solid: more seeds, two size ranges.

C10 rests on three seeds at one size range. Its two halves are:
    the POSITIVE  in the thick regime ED's rules preserve a dimension exactly (ring 1, cubic torus 3);
    the NEGATIVE  a pattern with no dimension never acquires one (the random web).
This repeats both with eight seeds and at two sizes, so each rests on numbers rather than on a handful of runs.

Nothing about the model or the instrument changes. Thickness is held at 25 relations per event (road T showed 25
and 50 give the same), and the robustness rule for a definite reading is exactly C10's: the same group size at all
three clustering tolerances, an even group, and a gap ratio of at least 1.5.

EXPECTATIONS, fixed before this file was run:
  S1  the ring reads exactly 1 at both sizes, in at least 7 of 8 seeds                      high
  S2  the cubic torus reads exactly 3 at both sizes, in at least 5 of 8 seeds               moderate - C10 got 5 of
                                                                                            9, and a thick grown
                                                                                            lattice is a messy object
  S3  the web reads nothing definite at both sizes, in 8 of 8 seeds                         high
  S4  reported: gap ratios everywhere, and whether the readings hold up when the pattern is twice as big
If S3 fails - if a web start does acquire a definite reading at some seed or size - C10's answer is withdrawn.
"""
import io
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for rel in (("..", "..", "ED_Attempt_12", "model"), ("..", "..", "ED_Attempt_11", "model"),
            ("..", "..", "ED_Attempt_08", "model")):
    sys.path.insert(0, os.path.join(HERE, *rel))
import w_web as W                                           # noqa: E402

OUT = os.path.join(HERE, "e_runs")
STARTS = ("ring", "grid3D", "web")
RHO = 25
SEEDS = tuple(range(1, 9))
GROWS = (4.0, 8.0)


def main():
    os.makedirs(OUT, exist_ok=True)
    res, lines = [], []
    for name in STARTS:
        for grow in GROWS:
            for seed in SEEDS:
                t0 = time.time()
                A, frac = W.giant(W.grow_thick(name, RHO, seed, grow=grow))
                d, detail = W.directions_robust(A)
                r = dict(start=name, grow=grow, seed=seed, n=A.shape[0], whole=round(frac, 3), directions=d,
                         secs=round(time.time() - t0, 1), **detail)
                res.append(r)
                print("%-6s grow %.0fx seed %d | n %6d | ED DIRECTIONS %s | groups %s | gap %s | %.0fs"
                      % (name, grow, seed, A.shape[0], d, detail.get("groups"), detail.get("gap_ratio"),
                         r["secs"]), flush=True)
                json.dump(res, open(os.path.join(OUT, "solid.json"), "w"), indent=1, default=str)
    for name in STARTS:
        for grow in GROWS:
            rs = [r for r in res if r["start"] == name and r["grow"] == grow]
            vals = [r["directions"] for r in rs]
            definite = [v for v in vals if v is not None]
            gaps = [r["gap_ratio"] for r in rs]
            lines.append("%-6s at %.0fx (n about %d) | definite in %d of %d | values %s | gap ratios %.2f to %.2f"
                         % (name, grow, rs[0]["n"], len(definite), len(rs), sorted(set(definite)),
                            min(gaps), max(gaps)))
    def hits(name, want, grow):
        rs = [r for r in res if r["start"] == name and r["grow"] == grow]
        return sum(1 for r in rs if r["directions"] == want)
    s1 = all(hits("ring", 1.0, g) >= 7 for g in GROWS)
    s2 = all(hits("grid3D", 3.0, g) >= 5 for g in GROWS)
    s3 = all(sum(1 for r in res if r["start"] == "web" and r["grow"] == g and r["directions"] is None) == len(SEEDS)
             for g in GROWS)
    lines.append("")
    lines.append("S1 (ring reads 1 in at least 7 of 8, at both sizes) %s   %s"
                 % (s1, {g: hits("ring", 1.0, g) for g in GROWS}))
    lines.append("S2 (cubic torus reads 3 in at least 5 of 8, at both sizes) %s   %s"
                 % (s2, {g: hits("grid3D", 3.0, g) for g in GROWS}))
    lines.append("S3 (web reads nothing definite, 8 of 8, at both sizes) %s" % s3)
    if not s3:
        lines.append("   ** S3 FAILED: a web start DID acquire a definite reading. C10's answer is withdrawn. **")
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "s_solid.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
