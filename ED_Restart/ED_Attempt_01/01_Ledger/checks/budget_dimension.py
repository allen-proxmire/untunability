"""Check C84 and C85: with spreading factor q = 1, the budget rule U = M + (average of the
neighbours' U) settles to a finite profile only in three or more dimensions, and in 3D it
falls off like 1/r with the expected constant.

Rule (RD14) with q = 1, no cap reached:  U = M + avg_neighbours(U),  i.e. (I - A) U = M.
A unit mass sits at the centre of a box of side N with U = 0 outside (Dirichlet).

Frozen criteria (set before the first run):
  P1  1D: U(centre) keeps growing with the box: U0(N=801) / U0(N=401) > 1.8
  P2  2D: U(centre) grows like a logarithm: each doubling of N (21, 41, 81, 161) adds between
      0.35 and 0.55 (continuum expectation (2/pi) ln 2 = 0.441)
  P3  3D: U(centre) settles: increasing with N (21, 41, 61), |U0(61) - 1.516386| < 0.05
      (Watson's lattice Green's function value), and U0(61) - U0(41) < 0.03
  P4  3D far field (N = 61): along an axis at r = 3, 4, 5, U(r) is within 15% of
      (3 / 2pi) (1/r - 1/30), the continuum 1/r profile with the box's boundary correction
"""
import math
import sys
import numpy as np


def neighbour_average(U):
    P = np.pad(U, 1)
    total = np.zeros_like(U)
    for ax in range(U.ndim):
        plus = [slice(1, -1)] * U.ndim
        minus = [slice(1, -1)] * U.ndim
        plus[ax] = slice(2, None)
        minus[ax] = slice(0, -2)
        total += P[tuple(plus)] + P[tuple(minus)]
    return total / (2 * U.ndim)


def solve(N, d, tol=1e-11, max_iter=100000):
    """Conjugate gradient for (I - A) U = M, unit mass at the centre."""
    M = np.zeros((N,) * d)
    M[(N // 2,) * d] = 1.0
    op = lambda X: X - neighbour_average(X)
    U = np.zeros_like(M)
    r = M - op(U)
    p = r.copy()
    rs = (r * r).sum()
    for _ in range(max_iter):
        Ap = op(p)
        alpha = rs / (p * Ap).sum()
        U += alpha * p
        r -= alpha * Ap
        rs_new = (r * r).sum()
        if math.sqrt(rs_new) < tol:
            return U
        p = r + (rs_new / rs) * p
        rs = rs_new
    raise RuntimeError("CG did not converge")


ok = True

u1 = {N: solve(N, 1)[N // 2] for N in (401, 801)}
ratio = u1[801] / u1[401]
p1 = ratio > 1.8
ok &= p1
print("P1 1D  U0: N=401 %.2f, N=801 %.2f, ratio %.3f  %s" % (u1[401], u1[801], ratio, "PASS" if p1 else "FAIL"))

u2 = {N: solve(N, 2)[N // 2, N // 2] for N in (21, 41, 81, 161)}
steps = [u2[41] - u2[21], u2[81] - u2[41], u2[161] - u2[81]]
p2 = all(0.35 < s < 0.55 for s in steps)
ok &= p2
print("P2 2D  U0: %s; added per doubling %s  %s" % (
    ", ".join("N=%d %.3f" % (N, v) for N, v in u2.items()),
    ", ".join("%.3f" % s for s in steps), "PASS" if p2 else "FAIL"))

U3 = {N: solve(N, 3) for N in (21, 41, 61)}
u3 = {N: U3[N][(N // 2,) * 3] for N in U3}
p3 = u3[21] < u3[41] < u3[61] and abs(u3[61] - 1.516386) < 0.05 and (u3[61] - u3[41]) < 0.03
ok &= p3
print("P3 3D  U0: %s  %s" % (", ".join("N=%d %.4f" % (N, v) for N, v in u3.items()), "PASS" if p3 else "FAIL"))

c = N3 = 61
U = U3[N3]
p4 = True
for rr in (3, 4, 5):
    measured = U[c // 2 + rr, c // 2, c // 2]
    expected = (3 / (2 * math.pi)) * (1 / rr - 1 / 30)
    rel = abs(measured - expected) / expected
    p4 &= rel < 0.15
    print("P4 3D  r=%d: U %.4f, 1/r profile %.4f, relative difference %.3f" % (rr, measured, expected, rel))
ok &= p4
print("P4 %s" % ("PASS" if p4 else "FAIL"))

print("C84/C85 hold" if ok else "C84/C85 FAILED")
sys.exit(0 if ok else 1)
