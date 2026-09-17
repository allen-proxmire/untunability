"""Check C131: can locus birth balance the q = 1 budget on a closed graph? (C91, G29b)

Rule (RD14) with q = 1, cap not reached: U_{t+1} = M + average of the 6 neighbours' U_t,
on a 3D torus (closed: no edge, so nothing is lost at a boundary).

Birth here is a test input, not ED's rule: every 10 steps one layer of new loci with U = 0 is
inserted on every side, at the seam farthest from the mass, so the side grows from 15 to 135
in 600 steps.

Exact bookkeeping: the total used budget after t steps is t * M whether or not loci are born
(newborn loci start at 0, and averaging on a regular graph conserves the total). So birth can
only dilute the budget, never remove it.

Predictions frozen before the first run (2026-09-13), mass M = 0.1:
  P0  Total used budget = t * M to relative 1e-9 at every 100th step, in both cases.
  P1  Fixed torus (side 15): U at the mass rises between steps 500 and 600 by
      100 M / 15^3 = 0.002963, within 10%. It never settles.
  P2  Growing torus: the rise between steps 500 and 600 is below 0.25 x the fixed-case rise.
  P3  Growing torus: U at the mass at step 600 is within 5% of the infinite-lattice value
      1.516386 M (Watson, C83).
  P4  Growing torus: average U at step 600 is below 1/10 of the fixed torus's.
"""
import sys

import numpy as np

M0 = 0.1
WATSON = 1.516386


def avg6(U):
    return (np.roll(U, 1, 0) + np.roll(U, -1, 0) + np.roll(U, 1, 1) + np.roll(U, -1, 1)
            + np.roll(U, 1, 2) + np.roll(U, -1, 2)) / 6.0


def run(L0, grow_every, T):
    U = np.zeros((L0, L0, L0))
    M = np.zeros_like(U)
    c = L0 // 2
    M[c, c, c] = M0
    at_mass, total_err = {}, 0.0
    for t in range(1, T + 1):
        U = M + avg6(U)
        if t % 100 == 0:
            at_mass[t] = U[tuple(np.argwhere(M > 0)[0])]
            total_err = max(total_err, abs(U.sum() - t * M0) / (t * M0))
        if grow_every and t % grow_every == 0:
            # new loci at both array ends; on the torus the ends meet, so this is one seam opposite the mass
            U = np.pad(U, 1)
            M = np.pad(M, 1)
    assert U.max() < 1.0
    return at_mass, total_err, U.mean(), U.shape[0]


fixed, err_f, mean_f, side_f = run(15, 0, 600)
grow, err_g, mean_g, side_g = run(15, 10, 600)

rise_f = fixed[600] - fixed[500]
rise_g = grow[600] - grow[500]
expected_f = 100 * M0 / 15 ** 3

checks = [
    ("P0 total = t x M (fixed, growing)", max(err_f, err_g) < 1e-9, "max relative error %.1e" % max(err_f, err_g)),
    ("P1 fixed torus keeps rising", abs(rise_f - expected_f) < 0.1 * expected_f,
     "rise 500->600 %.6f, expected %.6f" % (rise_f, expected_f)),
    ("P2 growing torus rise is small", rise_g < 0.25 * rise_f, "rise 500->600 %.6f (%.3f of fixed)" % (rise_g, rise_g / rise_f)),
    ("P3 growing torus approaches the infinite-lattice value", abs(grow[600] - WATSON * M0) < 0.05 * WATSON * M0,
     "U at mass %.5f, infinite lattice %.5f" % (grow[600], WATSON * M0)),
    ("P4 growing torus is diluted", mean_g < 0.1 * mean_f, "average U %.2e vs fixed %.2e" % (mean_g, mean_f)),
]

print("U at the mass every 100 steps")
print("  fixed (side 15):      " + "  ".join("%.5f" % fixed[t] for t in sorted(fixed)))
print("  growing (side %d):  " % side_g + "  ".join("%.5f" % grow[t] for t in sorted(grow)))
ok = True
for name, passed, detail in checks:
    ok &= passed
    print("%-4s %s  %s" % ("PASS" if passed else "FAIL", name, detail))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
