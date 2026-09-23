"""Check C14 and C15: facts the simulation spec relies on.

C14: all-equal start F = G = J gives det H(k) = 0 for N >= 2.
C15: start F = G = I + J gives winding 0; reversible transport G = F^T gives real
     det H(k) and winding 0; forward-only transport gives W = +N, all using the
     spec's reference point z0 = mean(f) + i 1e-3 max|f|.
"""
import math
import sys
import numpy as np

k = np.linspace(-math.pi, math.pi, 4001)[:-1]
rng = np.random.default_rng(0)


def det_curve(A, B):
    H = np.exp(1j * k)[:, None, None] * A + np.exp(-1j * k)[:, None, None] * B
    return np.linalg.det(H)


def winding(f, z0):
    ph = np.angle(f - z0)
    steps = np.angle(np.exp(1j * np.diff(np.append(ph, ph[0]))))
    return int(round(steps.sum() / (2 * math.pi)))


def spec_reference(f):
    return f.mean() + 1j * 1e-3 * np.max(np.abs(f))


ok = True
for N in range(1, 7):
    I, J = np.eye(N), np.ones((N, N))
    if N >= 2:
        ok &= np.max(np.abs(det_curve(J, J))) < 1e-9
    f = det_curve(I + J, I + J)
    ok &= np.max(np.abs(f)) > 1e-9 and winding(f, spec_reference(f)) == 0
    for _ in range(20):
        F = rng.random((N, N)) * 3
        g = det_curve(F, F.T)
        ok &= np.max(np.abs(g.imag)) < 1e-9 * np.max(np.abs(g))
        ok &= winding(g, spec_reference(g)) == 0
        h = det_curve(F + I, np.zeros((N, N)))
        ok &= winding(h, spec_reference(h)) == N

print("C14 and C15 hold" if ok else "C14/C15 FAILED")
sys.exit(0 if ok else 1)
