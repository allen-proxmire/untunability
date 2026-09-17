"""Diagnostic (not pre-registered; follows C62): two things the robustness check turned up.

  G1 draw strength 0.6: all 14 runs were reported 'dead' with no change and a NaN shift error. With feedback amplitude 0.9 the draw
     probability Gamma (1 + g s) reaches 0.6 x 1.9 = 1.14 > 1, where the Kraus factor sqrt(1 - p) is not defined. Check: the largest
     draw probability, and whether the state holds NaN after 10 steps from the near-uniform start.
  G2 the largest valid draw strength at amplitude 0.9 is 1 / 1.9 = 0.526; rerun the robustness check's setting at Gamma 0.5 (largest
     probability 0.95), same starts, gains 3 and 10, same kinds and 'found' criterion.
  G3 at amplitude 0.3 the hands had winding 0; at 0.6 and 0.9, winding 1. Amplitudes 0.4 and 0.5, gain 3, near-uniform start:
     kind, v, winding, and the final rate difference Gamma g |s|.
"""
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
import robustness_check as rc  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402


def g1():
    c = dict(rc.BASE)
    c["Gamma"] = 0.6
    L, D = c["L"], c["D"]
    W, Cf = fp.walk_matrix(L, rc.C), fp.coin_full(L, rc.C)
    lane, dest = lane_channels(L, D)
    V0 = c["g"] * rc.chi_for(L, D, 0.6) / 3
    rho = rc.start(L, 0)
    pmax = 0.0
    with np.errstate(all="ignore"):
        for _ in range(10):
            rho, s = rc.step(rho, W, Cf, lane, dest, c, V0)
            pmax = max(pmax, float(np.max(rc.rates(L, D, 0.6, c["g"], s))))
    return pmax, bool(np.isnan(rho).any())


def main():
    pmax, has_nan = g1()
    print("G1 Gamma 0.6, g 0.9: largest draw probability in 10 steps %.3f; state holds NaN: %s" % (pmax, has_nan), flush=True)
    c5 = dict(rc.BASE)
    c5["Gamma"] = 0.5
    cg = [dict(rc.BASE, g=a) for a in (0.4, 0.5)]
    with Pool(7) as pool:
        chis = dict(pool.map(rc.work, [("chi", 24, 2, 0.5), ("chi", 24, 2, 0.3)]))
        chi5, chi3 = chis[("chi", 24, 2, 0.5)], chis[("chi", 24, 2, 0.3)]
        jobs = [("run", c5, chi5, gain, k) for gain in rc.GAINS for k in range(rc.NSTART)]
        jobs += [("run", c, chi3, 3.0, 0) for c in cg]
        res = dict(pool.map(rc.work, jobs))
    print("G2 chi at Gamma 0.5: %+.5e" % chi5, flush=True)
    letter = {"hand": "H", "dead": "D", "patterned": "P", "unsteady": "U"}
    found = False
    for gain in rc.GAINS:
        rs = [res[("run", rc.ckey(c5), gain, k)] for k in range(rc.NSTART)]
        hands = [a for a in rs if a["kind"] == "hand"]
        found = found or len(hands) >= 4
        print("G2 Gamma 0.5 gain %4.1f: %s hands %d; v %s; windings %s"
              % (gain, "".join(letter[a["kind"]] for a in rs), len(hands), " ".join("%+.5e" % a["v"] for a in hands),
                 [a["winding"] for a in hands]), flush=True)
    print("G2 found at Gamma 0.5: %s" % found, flush=True)
    for c in cg:
        a = res[("run", rc.ckey(c), 3.0, 0)]
        print("G3 amplitude %.1f gain 3 near-uniform: %s, v %+.5e, winding %s"
              % (c["g"], a["kind"], a["v"], a.get("winding")), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
