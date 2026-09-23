"""Calibrate the tilt reading (road F; D15, C48). Runs BEFORE any grown slice is measured.

Allen's decision (D15): **the calibration objects are the scale.** The reading is not tested against
a theoretical exponent - note 10's predicted +0.5, 0, -0.5 were system-size exponents where this
reading measures a separation exponent, and Claude conflated them (C47). Instead a ring, a square
torus and a cube torus define empirically what one, two and three dimensions look like, and a grown
slice is placed on that ladder.

Expected results, written down before this run:
  F1-0  the solve reproduces c3b.sync_steady_state's summaries to machine precision.
  F1-1  the three calibration objects come out ORDERED - ring above square above cube - and
        SEPARATED by at least 0.15 between neighbours, on every one of five seeds.
Exit rule: either failing means the reading cannot tell the dimensions apart, and road F stops
before any grown slice is touched.

AND, fixed here before any grown slice is measured, the test that matters:
  F1-2  a grown slice SUPPORTS a common now if its tilt exponent is at or below the two-dimensional
        reference, two being the literature's lower critical dimension for frequency synchronisation;
        it FAILS if the exponent sits above that reference, toward the one-dimensional end.
"""
import json
import sys
import numpy as np
from f1_tilt import tilt_curve, check_against_c3b, ring, square_torus, cube_torus

SEEDS = (0, 1, 2, 3, 4)
ORDER = ["ring (d=1)", "square torus (d=2)", "cube torus (d=3)"]
MIN_GAP = 0.15


def objects():
    out = [("ring (d=1)", ring(16384)),
           ("square torus (d=2)", square_torus(128)),
           ("cube torus (d=3)", cube_torus(24))]
    from p3 import Slice3P
    out.append(("ED flat slice (d=3)", Slice3P(24).adjacency()[0]))
    R = Slice3P(24, t_cap=24 * 24 ** 3, e_cap=24 * 24 ** 3)
    R.seed(7)
    R.flip_randomize(50)
    out.append(("randomised slice", R.adjacency()[0]))
    return out


def main():
    lines, res = [], {}
    solve_ok = True
    for name, A in objects():
        chk = check_against_c3b(A, 0)
        if not (chk["dW"] < 1e-9 and chk["dmax"] < 1e-9):
            solve_ok = False
            lines.append("  %-22s SOLVE MISMATCH dW %.3g dmax %.3g" % (name, chk["dW"], chk["dmax"]))
        exps = []
        for s in SEEDS:
            c = tilt_curve(A, s)
            if c["tilt_exponent"] is not None:
                exps.append(c["tilt_exponent"])
        res[name] = dict(exponents=exps, scales=c["r"], fit_rungs=c["fit_rungs"],
                         pairs=c["pairs"], N=c["N"], mean_degree=c["mean_degree"])
        if exps:
            lines.append("  %-22s tilt exponent %7.3f to %7.3f (mean %7.3f) | rungs %s fitted %s"
                         % (name, min(exps), max(exps), float(np.mean(exps)), c["r"], c["fit_rungs"]))
        else:
            lines.append("  %-22s too few scales: rungs %s, and the top two are dropped for saturation"
                         % (name, c["r"]))
    means = [float(np.mean(res[n]["exponents"])) for n in ORDER]
    ordered = means[0] > means[1] > means[2]
    gaps = [means[0] - means[1], means[1] - means[2]]
    separated = min(gaps) >= MIN_GAP
    perseed = all(res[ORDER[0]]["exponents"][i] > res[ORDER[1]]["exponents"][i] >
                  res[ORDER[2]]["exponents"][i] for i in range(len(SEEDS)))
    ok = solve_ok and ordered and separated and perseed
    lines.append("")
    lines.append("  F1-0 solve matches c3b: %s" % ("ok" if solve_ok else "FAIL"))
    lines.append("  F1-1 ordered %s, separated by %.3f and %.3f (need %.2f) %s, on every seed %s"
                 % ("ok" if ordered else "FAIL", gaps[0], gaps[1], MIN_GAP,
                    "ok" if separated else "FAIL", "ok" if perseed else "FAIL"))
    lines.append("")
    lines.append("  THE SCALE:  d=1 %.3f   d=2 %.3f   d=3 %.3f" % tuple(means))
    lines.append("  F1-2, fixed before any grown slice is measured: a grown slice supports a common")
    lines.append("        now if its tilt exponent is at or below %.3f (the d=2 reference)." % means[1])
    text = ("F1 calibration: %s\n" % ("PASS" if ok else "FAIL")) + "\n".join(lines)
    print(text)
    with open("f1_calibrate.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    res["_scale"] = dict(zip(ORDER, means))
    res["_threshold"] = means[1]
    with open("f1_calibrate.json", "w", encoding="utf-8") as f:
        json.dump(res, f, default=str)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
