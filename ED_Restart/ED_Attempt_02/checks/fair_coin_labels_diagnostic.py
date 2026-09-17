"""Diagnostic (not pre-registered; follows C58): is 'the plain Fourier coin' (phi = 0) independent of how the three channels are labelled?

Every fair coin C reduces to e^{i theta} Q diag(1, e^{ia}, e^{ib}) B Q^dagger with B = F or F* (C55 Q1). With M = C / B elementwise
(rank 1), the phases are a = arg(M_LL / M_II), b = arg(M_RR / M_II). For all 36 row and column permutations of F this reports B,
phi = a + b, and a - b; a - b a multiple of 15 degrees (2 pi / L, L 24) is removable by the momentum gauge, and then the coin is
the family member at phi (up to that gauge). The only relabelling that keeps Internal as Internal and is a symmetry of ED is the
Left-Right swap; the others are listed to see whether phi = 0 depends on which channel is called Internal.
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402

F = fp.FOURIER
I, LE, RI = fp.I, fp.LE, fp.RI


def reduce(C):
    best = None
    for name, B in (("F", F), ("F*", F.conj())):
        M = C / B
        sv = np.linalg.svd(M, compute_uv=False)
        if sv[1] / sv[0] < 1e-10:
            a = np.degrees(np.angle(M[LE, LE] / M[I, I]))
            b = np.degrees(np.angle(M[RI, RI] / M[I, I]))
            best = (name, (a + b) % 360, (a - b) % 360)
            break
    return best


rows = {}
for p1 in itertools.permutations(range(3)):
    for p2 in itertools.permutations(range(3)):
        C = F[np.ix_(p1, p2)]
        name, phi, diff = reduce(C)
        gauge = min(diff % 15, 15 - diff % 15) < 1e-9
        rows.setdefault((name, round(phi, 6) % 360, gauge), []).append((p1, p2))
for (name, phi, gauge), perms in sorted(rows.items()):
    print("B %-2s phi %7.2f  a-b removable by gauge: %-5s  from %2d of 36 relabellings, e.g. rows %s columns %s"
          % (name, phi, gauge, len(perms), perms[0][0], perms[0][1]))
