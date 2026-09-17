"""Does on/off exclusion supply gravity's self-feedback? Algebra check (RD9; note 7; follows C38-C41).

Bookkeeping as attempt 1 (A1-ledger C200, C203, C206, C207): ED's clock rate e^(-U) with -g00 = e^(-2U) (A1-ledger RD36; C38);
PPN g00 = -1 + 2U - 2 beta U^2 + c1 Phi1 + c2 Phi2 + ..., with c1 = 2 gamma + 2 + alpha3 + zeta1 and c2 = 2(3 gamma - 2 beta + 1 + zeta2);
gamma = 1, alpha = xi = 0 assumed; Nordtvedt eta_N = 4 beta - gamma - 3 - (2/3) zeta1 - (1/3) zeta2.
beta is read from the exterior field of a point mass: beta = -(d^2 g00 / dU_N^2)(0) / 4, U_N the Newtonian potential.

Feedback channels from on/off exclusion (O1-O4 of note 6):
  F1 influence hops slowed like motion, weight e^(-2U): static flux law div(e^(-2U) grad U) = -S, so (1 - e^(-2U))/2 = U_N.
  F1b influence hops slowed once, weight e^(-U): 1 - e^(-U) = U_N.
  F0 influence not slowed: U = U_N.
  F2 a source's on-ticks slowed by its own clock rate: active density rho e^(-U) (1 - v^2/2), so c2 = 2 x (-1) = -2 and
     c1 = 2 x (-1/2) = -1 (relative to rest-mass-only counting, c1 = c2 = 0).
Reference cases: A1-ledger C207 case A (rest mass only: c1 = 0, c2 = 0) and case B (all commitment linearly: c1 = 1, c2 = -1);
general relativity (c1 = 4, c2 = 4).

Expected results, written down before the first run (2026-09-15):
  W1 F1: g00 = -1 + 2 U_N exactly, beta = 0.
  W2 F1b: beta = 1/2.
  W3 F0: beta = 1.
  W4 reference: case A zeta1 = -4, zeta2 = -2, eta_N = 10/3; case B zeta1 = -3, zeta2 = -2.5, eta_N = 17/6 (reproducing A1-ledger C207);
     GR zeta1 = zeta2 = eta_N = 0.
  W5 F2 (with F0): beta = 1, zeta1 = -5, zeta2 = -3, eta_N = 13/3, further from GR than case A.
  W6 Mercury's perihelion factor (2 + 2 gamma - beta)/3: F1 4/3, F1b 7/6, F0 1.
Exit code: 0 if it completes.
"""
import math
import sys


def g00_from_U(U):
    return -math.exp(-2 * U)


def beta_of(U_of_UN, h=1e-4):
    f = lambda x: g00_from_U(U_of_UN(x))
    second = (f(h) - 2 * f(0.0) + f(-h)) / h ** 2
    first = (f(h) - f(-h)) / (2 * h)
    return -second / 4, first


def zetas(c1, c2, beta=1.0, gamma=1.0):
    zeta1 = c1 - (2 * gamma + 2)
    zeta2 = c2 / 2 - (3 * gamma - 2 * beta + 1)
    eta = 4 * beta - gamma - 3 - (2 / 3) * zeta1 - (1 / 3) * zeta2
    return zeta1, zeta2, eta


def main():
    F1 = lambda un: -0.5 * math.log(1 - 2 * un)
    F1b = lambda un: -math.log(1 - un)
    F0 = lambda un: un
    exact_F1 = max(abs(g00_from_U(F1(x)) - (-1 + 2 * x)) for x in (0.001, 0.01, 0.1, 0.3))
    b1, d1 = beta_of(F1)
    b1b, d1b = beta_of(F1b)
    b0, d0 = beta_of(F0)
    print("W1 F1 (hops weighted e^-2U): largest |g00 - (-1 + 2 U_N)| over U_N in {0.001, 0.01, 0.1, 0.3} = %.1e; first-order coefficient %.6f; beta = %.6f" % (exact_F1, d1, b1))
    print("W2 F1b (hops weighted e^-U): first-order coefficient %.6f; beta = %.6f" % (d1b, b1b))
    print("W3 F0 (influence not slowed): first-order coefficient %.6f; beta = %.6f" % (d0, b0))
    A = zetas(0, 0)
    B = zetas(1, -1)
    GR = zetas(4, 4)
    F2 = zetas(-1, -2)
    for name, z in (("case A (rest mass only)", A), ("case B (all commitment linearly)", B), ("general relativity", GR), ("F2 (on-ticks slowed by own clock)", F2)):
        print("W4/W5 %-36s zeta1 = %+.4f, zeta2 = %+.4f, eta_N = %+.4f" % (name, z[0], z[1], z[2]))
    merc = {n: (2 + 2 * 1.0 - b) / 3 for n, b in (("F1", b1), ("F1b", b1b), ("F0", b0))}
    print("W6 Mercury perihelion factor relative to GR: F1 %.6f, F1b %.6f, F0 %.6f" % (merc["F1"], merc["F1b"], merc["F0"]))

    w1 = exact_F1 < 1e-12 and abs(b1) < 1e-5
    w2 = abs(b1b - 0.5) < 1e-5
    w3 = abs(b0 - 1) < 1e-5
    w4 = (abs(A[0] + 4) < 1e-12 and abs(A[1] + 2) < 1e-12 and abs(A[2] - 10 / 3) < 1e-12 and abs(B[0] + 3) < 1e-12 and abs(B[1] + 2.5) < 1e-12
          and abs(B[2] - 17 / 6) < 1e-12 and max(abs(v) for v in GR) < 1e-12)
    w5 = abs(F2[0] + 5) < 1e-12 and abs(F2[1] + 3) < 1e-12 and abs(F2[2] - 13 / 3) < 1e-12
    w6 = abs(merc["F1"] - 4 / 3) < 1e-5 and abs(merc["F1b"] - 7 / 6) < 1e-5 and abs(merc["F0"] - 1) < 1e-5
    print("\nExpected results:")
    for label, ok in (("W1 F1 gives beta 0", w1), ("W2 F1b gives beta 1/2", w2), ("W3 F0 gives beta 1", w3),
                      ("W4 reference cases reproduce A1 C207 and GR", w4), ("W5 F2 moves further from GR", w5), ("W6 Mercury factors", w6)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
