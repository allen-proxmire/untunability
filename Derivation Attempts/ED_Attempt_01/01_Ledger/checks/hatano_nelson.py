"""Check C5: the N = 1 cases of the handedness result.

H(k) = A e^{ik} + B e^{-ik} with scalars A, B.
  B = A (mirror-symmetric):  winding 0
  |A| > |B| (Hatano-Nelson): winding +1 about 0
  |A| < |B|:                 winding -1 about 0
"""
import math
import sys
import numpy as np

k = np.linspace(-math.pi, math.pi, 4001)[:-1]


def winding(f, z0):
    ph = np.angle(f - z0)
    steps = np.angle(np.exp(1j * np.diff(np.append(ph, ph[0]))))
    return int(round(steps.sum() / (2 * math.pi)))


def curve(A, B):
    return A * np.exp(1j * k) + B * np.exp(-1j * k)


rng = np.random.default_rng(0)
ok = True
for _ in range(50):
    A = complex(*rng.normal(size=2))
    ok &= winding(curve(A, A), 1e-3 * abs(A) * (1 + 1j)) == 0
    B = A * rng.uniform(0.1, 0.9) * np.exp(1j * rng.uniform(0, 2 * math.pi))
    ok &= winding(curve(A, B), 0) == 1
    ok &= winding(curve(B, A), 0) == -1

print("C5 holds" if ok else "C5 FAILED")
sys.exit(0 if ok else 1)
