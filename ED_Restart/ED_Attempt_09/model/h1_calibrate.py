"""Calibrate the curvature reading (H1; D3). Runs BEFORE any grown slice is measured.

Expected results, written down before this run:
  H1-0  the reading orders objects whose curvature is known: a regular tree (walks spread apart,
        negative) below a cube torus (flat, zero) below a hypercube (walks draw together, positive),
        on every one of three seeds.
  H1-1  the cube torus reads within 0.02 of zero.
Exit rule: either failing means the reading cannot see curvature, and the curvature part of H1 is
dropped before any grown slice is touched (the other readings still run).

AND, fixed here from the calibration alone, before any grown slice is measured:
  H1-2  a grown slice MEETS 'curvature bounded below' if its median edge curvature is at or above
        the midpoint between the tree's median and ED's flat slice's median; it FAILS if it sits
        below that midpoint, toward the tree.
"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from h1_curvature import curvature_sample, regular_tree, hypercube   # noqa: E402

SEEDS = (0, 1, 2)


def cube_torus(n):
    from f1_tilt import cube_torus as ct
    return ct(n)


def objects():
    from p3 import Slice3P
    return [("tree (negative)", regular_tree(3, 9), 4),
            ("cube torus (zero)", cube_torus(16), 1),
            ("hypercube (positive)", hypercube(8), 1),
            ("ED flat slice", Slice3P(24).adjacency()[0], 1)]


def main():
    res, lines = {}, []
    for name, A, mindeg in objects():
        meds = []
        for s in SEEDS:
            r = curvature_sample(A, s, min_degree=mindeg)
            meds.append(r["median"])
        res[name] = dict(medians=meds, last=r)
        lines.append("  %-22s median %.3f to %.3f | mean %.3f  p05 %.3f  negative %.0f%%"
                     % (name, min(meds), max(meds), r["mean"], r["p05"], 100 * r["frac_negative"]))
    t, c, h = (res[k]["medians"] for k in ("tree (negative)", "cube torus (zero)", "hypercube (positive)"))
    ordered = all(t[i] < c[i] < h[i] for i in range(len(SEEDS)))
    zero = all(abs(x) <= 0.02 for x in c)
    ok = ordered and zero
    flat = float(np.mean(res["ED flat slice"]["medians"]))
    tree = float(np.mean(t))
    thr = 0.5 * (flat + tree)
    lines += ["", "  H1-0 ordered tree < torus < hypercube on every seed: %s" % ("ok" if ordered else "FAIL"),
              "  H1-1 cube torus within 0.02 of zero: %s" % ("ok" if zero else "FAIL"),
              "", "  H1-2, fixed before any grown slice: tree %.3f, ED flat %.3f -> threshold %.3f" % (tree, flat, thr)]
    text = ("H1 curvature calibration: %s\n" % ("PASS" if ok else "FAIL")) + "\n".join(lines)
    print(text)
    res["_threshold"] = thr
    res["_flat"] = flat
    res["_tree"] = tree
    with open("h1_calibrate.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    with open("h1_calibrate.json", "w", encoding="utf-8") as f:
        json.dump(res, f, default=str)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
