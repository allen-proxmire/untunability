"""The bar for road R1: what general relativity's post-Newtonian weights demand of ED's sources (RD2). Bookkeeping check only.

Bookkeeping as attempt 1 (A1-ledger C206, C207) and attempt 3 (A3-ledger C42): ED's clock rate e^(-U), so -g00 = e^(-2U) and U enters
g00 as 2U. If ED's field U is sourced by rho (1 + a1 v^2 + a2 U + a3 Pi + a4 p/rho) (motion, gravity's own energy, internal energy,
pressure), then U gains a1 Phi1 + a2 Phi2 + a3 Phi3 + a4 Phi4, and the PPN g00 coefficients are c_k = 2 a_k.
PPN (gamma = beta = 1, alpha = xi = 0): c1 = 4 + zeta1, c2 = 2(2 + zeta2), c3 = 2(1 + zeta3), c4 = 6 + 6 zeta4;
eta_N = 4 beta - gamma - 3 - (2/3) zeta1 - (1/3) zeta2.
General relativity: c = (4, 4, 2, 6).
Energy counting (A1-ledger C207 case B, 'all commitment counts linearly'): kinetic energy 1/2 v^2, gravitational energy -1/2 U,
internal energy Pi, no pressure: a = (1/2, -1/2, 1, 0).
Rest mass only (case A): a = (0, 0, 0, 0).
Bounds (A1-ledger C206): |eta_N| about 4.5e-4; zeta1 2e-2; zeta2 4e-5; zeta3 1e-8.

Expected results, written down before the first run (2026-09-15):
  B1 general relativity's bar in ED's source weights: a = (2, 2, 1, 3).
  B2 energy counting gives c = (1, -1, 2, 0), zeta1 = -3, zeta2 = -2.5, zeta3 = 0, zeta4 = -1, eta_N = 17/6, reproducing A1-ledger C207 case B.
  B3 rest mass only gives zeta1 = -4, zeta2 = -2, zeta3 = -1, zeta4 = -1, eta_N = 10/3, reproducing case A.
  B4 the gap from energy counting to the bar: motion +3/2, gravity's own energy +5/2, internal energy 0, pressure +3.
Exit code: 0 if it completes.
"""
import sys
from fractions import Fraction as Fr


def cs_from_a(a):
    return tuple(2 * x for x in a)


def zetas(c):
    c1, c2, c3, c4 = c
    z1 = c1 - 4
    z2 = Fr(c2, 2) - 2 if isinstance(c2, int) else c2 / 2 - 2
    z3 = Fr(c3, 2) - 1 if isinstance(c3, int) else c3 / 2 - 1
    z4 = (Fr(c4) - 6) / 6
    eta = 4 - 1 - 3 - Fr(2, 3) * z1 - Fr(1, 3) * z2
    return z1, z2, z3, z4, eta


def main():
    GR_c = (4, 4, 2, 6)
    bar = tuple(Fr(x, 2) for x in GR_c)
    B = (Fr(1, 2), Fr(-1, 2), Fr(1), Fr(0))
    A = (Fr(0), Fr(0), Fr(0), Fr(0))
    cB = cs_from_a(B)
    cA = cs_from_a(A)
    zB = zetas(tuple(Fr(x) for x in cB))
    zA = zetas(tuple(Fr(x) for x in cA))
    zGR = zetas(tuple(Fr(x) for x in GR_c))
    gap = tuple(b - e for b, e in zip(bar, B))
    fmt = lambda t: "(" + ", ".join(str(x) for x in t) + ")"
    print("B1 GR bar in ED source weights (motion, gravity's energy, internal energy, pressure): a = %s; GR zetas and eta_N %s" % (fmt(bar), fmt(zGR)))
    print("B2 energy counting: c = %s; zeta1, zeta2, zeta3, zeta4, eta_N = %s" % (fmt(cB), fmt(zB)))
    print("B3 rest mass only: c = %s; zeta1, zeta2, zeta3, zeta4, eta_N = %s" % (fmt(cA), fmt(zA)))
    print("B4 gap from energy counting to the bar: %s" % fmt(gap))
    b1 = bar == (2, 2, 1, 3) and zGR == (0, 0, 0, 0, 0)
    b2 = cB == (1, -1, 2, 0) and zB == (-3, Fr(-5, 2), 0, -1, Fr(17, 6))
    b3 = zA == (-4, -2, -1, -1, Fr(10, 3))
    b4 = gap == (Fr(3, 2), Fr(5, 2), 0, 3)
    print("\nExpected results:")
    for label, ok in (("B1 bar a = (2, 2, 1, 3)", b1), ("B2 energy counting reproduces A1 case B", b2),
                      ("B3 rest mass reproduces A1 case A", b3), ("B4 gap (3/2, 5/2, 0, 3)", b4)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
