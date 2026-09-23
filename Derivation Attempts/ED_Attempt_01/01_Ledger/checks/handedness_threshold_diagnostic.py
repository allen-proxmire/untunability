"""Diagnostic after C248 follow-up F (not pre-registered): where is the threshold between a seed current that dies
and one that sustains a hand, and are the delta 0.01 and 0.1 runs still decaying at t = 60?
Same rule as handedness_toy.py (g = 0.5, J0 = 0.05, RK4 dt 0.02); runs to t = 240 and reports t_b - t_f every t = 30."""
import math
import numpy as np
import handedness_toy as h

L = h.L
kx = 2 * math.pi * np.arange(L) / L
for delta in (0.01, 0.1, 0.15, 0.2, 0.25, 0.3):
    psi = np.ones(L, dtype=complex) + delta * np.exp(1j * kx)
    psi = psi / np.linalg.norm(psi)
    row = []
    for block in range(8):
        for _ in range(1500):
            tf, tb = h.hops(psi, 0.5)
            k1 = h.rhs(psi, tf, tb); k2 = h.rhs(psi + 0.5 * h.DT * k1, tf, tb)
            k3 = h.rhs(psi + 0.5 * h.DT * k2, tf, tb); k4 = h.rhs(psi + h.DT * k3, tf, tb)
            psi = psi + h.DT * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            psi = psi / np.linalg.norm(psi)
        tf, tb = h.hops(psi, 0.5)
        row.append(tb - tf)
    print("delta %.2f: t_b - t_f at t = 30..240: %s" % (delta, " ".join("%.2e" % v for v in row)))
