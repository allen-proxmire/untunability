"""Complex conjugation and the mirror (D6; Allen's association: the draw pairs psi with psi*, 'its mirror image').

Two different 'mirrors' are in play:
  the space mirror used so far (x -> -x with Left and Right swapped; fixed_point_check.mirror_perm), and
  complex conjugation psi -> psi*, which in quantum mechanics is the core of time reversal (Wigner 1932).
This check asks how they meet in ED's discrete rule.

  K1 Fourier coin: is its complex conjugate the same coin with Left and Right swapped (F* = P F = F P)?
  K2 Grover coin: is it real (G* = G)?
  K3 The two hands of the Fourier g +0.9 setting (C45; loop gain 3; start 0 went one way, start 2 the other): is one the space
     mirror of the other, up to a shift by an even number of loci?
  K4 Is one the complex conjugate of the other, up to an even shift?
  K5 Is one the complex conjugate of the other with Left and Right swapped but space not reflected, up to an even shift?

Expected results, written down before the first run (2026-09-14):
  K1 yes (to 1e-12); K2 yes (to 1e-15); K3 yes (to 1e-8); K4 no (distance above 1e-3); K5 no (distance above 1e-3).
Exit code: 0 if it completes.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
from discrete_hand_test import D, step  # noqa: E402
from lasting_states_check import CHI, L, starts  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402

STEPS = 4000


def perm_shift(t):
    idx = np.zeros(3 * L, dtype=int)
    for u in range(L):
        for c in range(3):
            idx[3 * ((u + t) % L) + c] = 3 * u + c
    return idx


def perm_channel_swap():
    idx = np.zeros(3 * L, dtype=int)
    for u in range(L):
        for c, cm in ((fp.I, fp.I), (fp.LE, fp.RI), (fp.RI, fp.LE)):
            idx[3 * u + cm] = 3 * u + c
    return idx


def moved(rho, idx):
    return rho[np.ix_(idx, idx)]


def best_distance(target, candidate):
    return min(float(np.max(np.abs(target - moved(candidate, perm_shift(t))))) for t in range(0, L, D))


def main():
    F, G = fp.FOURIER, fp.GROVER
    P = np.eye(3)[[fp.I, fp.RI, fp.LE]] if (fp.I, fp.LE, fp.RI) == (0, 1, 2) else None
    k1a = float(np.max(np.abs(F.conj() - P @ F)))
    k1b = float(np.max(np.abs(F.conj() - F @ P)))
    k2 = float(np.max(np.abs(G.conj() - G)))
    print("K1 Fourier: |F* - P F| %.1e, |F* - F P| %.1e" % (k1a, k1b), flush=True)
    print("K2 Grover: |G* - G| %.1e" % k2, flush=True)

    W, Cf = fp.walk_matrix(L, F), fp.coin_full(L, F)
    lane, dest = lane_channels(L, D)
    V0 = abs(0.9 * CHI["Fourier"]) / 3
    st = starts()
    finals = []
    for i in (0, 2):
        rho = st[i].copy()
        for _ in range(STEPS):
            rho, _ = step(rho, W, Cf, lane, dest, L, 0.9, V0)
        finals.append(rho)
        print("start %d: v %+.5e" % (i, fp.displacement(rho, Cf, L)), flush=True)
    a, b = finals
    k3 = best_distance(b, moved(a, fp.mirror_perm(L)))
    k4 = best_distance(b, a.conj())
    k5 = best_distance(b, moved(a.conj(), perm_channel_swap()))
    print("K3 other hand vs space mirror: %.1e" % k3, flush=True)
    print("K4 other hand vs complex conjugate: %.1e" % k4, flush=True)
    print("K5 other hand vs conjugate with Left and Right swapped: %.1e" % k5, flush=True)
    print("\nExpected results:")
    for label, ok in (("K1 F* = P F = F P", k1a < 1e-12 and k1b < 1e-12), ("K2 G real", k2 < 1e-15),
                      ("K3 hands are space mirrors", k3 < 1e-8), ("K4 hands are not conjugates", k4 > 1e-3),
                      ("K5 hands are not swapped conjugates", k5 > 1e-3)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
