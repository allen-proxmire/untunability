"""Numerical check of the result in the paper and Result.md.

For H(k) = sum over m from -R to R of e^{imk} C_m, with N channels:
  symmetric case    C_{-m} = S C_m S^-1  -> det H(k) even in k, winding 0
  one-way control   only C_R nonzero     -> winding R*N about 0
  Hermitian control C_{-m} = C_m^dagger  -> det H(k) real, winding 0

Part 1 checks nearest-neighbour hops (R = 1) with S the reversal of the channel order.
Part 2 checks the general case: S any reflection (any matrix with S^2 = 1), and hops
reaching R = 1, 2 or 3 loci.

    python Handedness/check_result.py

Requires numpy.
"""
import math
import sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
rng = np.random.default_rng(0)
k = np.linspace(-math.pi, math.pi, 4001)[:-1]
MIRROR = (-np.arange(len(k))) % len(k)  # index of -k on the grid
TRIALS = 20


def cplx(N):
    return rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))


def transport(C, q):
    """H(q) for C = {m: C_m}; q may be an array."""
    q = np.atleast_1d(q)
    N = next(iter(C.values())).shape[0]
    H = np.zeros((len(q), N, N), dtype=complex)
    for m, Cm in C.items():
        H += np.exp(1j * m * q)[:, None, None] * Cm
    return H


def det_curve(C):
    return np.linalg.det(transport(C, k))


def winding(f, z0):
    ph = np.angle(f - z0)
    steps = np.angle(np.exp(1j * np.diff(np.append(ph, ph[0]))))
    return int(round(steps.sum() / (2 * math.pi)))


def reference(f):
    """A point well clear of the curve f."""
    scale = np.max(np.abs(f))
    z0 = 0.0
    while np.min(np.abs(f - z0)) < 1e-3 * scale:
        z0 = complex(*rng.normal(size=2)) * 0.1 * scale
    return z0


def even_error(f):
    return np.max(np.abs(f - f[MIRROR])) / np.max(np.abs(f))


def random_reflection(N):
    """A random, generally non-unitary matrix S with S^2 = 1."""
    D = np.diag(rng.choice([-1.0, 1.0], size=N))
    while True:
        P = cplx(N)
        if np.linalg.cond(P) < 50:
            return P @ D @ np.linalg.inv(P)


def check(S, R, N):
    """Run the symmetric case and both controls for one S and range R.

    Returns (even error, symmetric windings, one-way winding, Hermitian windings, symmetry ok).
    """
    Si = np.linalg.inv(S)
    even_err, sym_w, herm_w, sym_ok = 0.0, set(), set(), True
    for _ in range(TRIALS):
        C0 = cplx(N)
        C = {0: (C0 + S @ C0 @ Si) / 2}
        for m in range(1, R + 1):
            C[m] = cplx(N)
            C[-m] = S @ C[m] @ Si
        q = rng.uniform(-math.pi, math.pi)
        sym_ok &= np.allclose(S @ transport(C, q)[0] @ Si, transport(C, -q)[0])
        f = det_curve(C)
        even_err = max(even_err, even_error(f))
        sym_w.add(winding(f, reference(f)))

        Ch = {0: (C0 + C0.conj().T) / 2}
        for m in range(1, R + 1):
            Ch[m] = cplx(N)
            Ch[-m] = Ch[m].conj().T
        g = det_curve(Ch)
        herm_w.add(winding(g, reference(g) + 1j * 1e-3 * np.max(np.abs(g))))
    oneway = winding(det_curve({R: cplx(N)}), 0)
    return even_err, sym_w, oneway, herm_w, sym_ok


ok = True
header = "N  max|f(k)-f(-k)|/max|f|  symmetric windings | one-way winding | Hermitian windings"

print("Part 1: nearest-neighbour hops (R = 1), S reverses the channel order")
print(header)
for N in range(1, 7):
    S = np.fliplr(np.eye(N))
    e, sw, ow, hw, sok = check(S, 1, N)
    ok &= sok and e < 1e-9 and sw == {0} and ow == N and hw == {0}
    print("%d  %.1e  %s | %d | %s" % (N, e, sorted(sw), ow, sorted(hw)))

for R in (1, 2, 3):
    print("\nPart 2: any reflection S (S^2 = 1), hops of range R = %d; one-way winding should be %d*N" % (R, R))
    print(header)
    for N in range(1, 7):
        e, sw, ow, hw, sok = 0.0, set(), None, set(), True
        for _ in range(5):
            e1, sw1, ow1, hw1, sok1 = check(random_reflection(N), R, N)
            e, sw, hw, sok = max(e, e1), sw | sw1, hw | hw1, sok and sok1
            ok &= ow1 == R * N
            ow = ow1
        ok &= sok and e < 1e-9 and sw == {0} and hw == {0}
        print("%d  %.1e  %s | %d | %s" % (N, e, sorted(sw), ow, sorted(hw)))

print("\nresult holds for N = 1..6, any reflection S, hop range R = 1..3" if ok else "\nCHECK FAILED")
sys.exit(0 if ok else 1)
