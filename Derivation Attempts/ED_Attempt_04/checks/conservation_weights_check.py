"""Arithmetic check for note 14 (road R4 part 2): how the PPN conservation parameters set a source's weights and the Moon-test number.
Not a model of ED; bookkeeping only, in the same conventions as A3 checks/feedback_weights_check.py.

PPN (Will): g00 = -1 + 2U - 2 beta U^2 + (2 gamma + 2 + alpha3 + zeta1) Phi1 + 2 (3 gamma - 2 beta + 1 + zeta2) Phi2
                 + 2 (1 + zeta3) Phi3 + 2 (3 gamma + 3 zeta4) Phi4 + (preferred-frame and xi terms, set to zero here),
with Phi1 ~ rho v^2, Phi2 ~ rho U, Phi3 ~ rho Pi, Phi4 ~ p. Reading the source as 2 x (active density) gives the weights
  motion w_v = (2 gamma + 2 + alpha3 + zeta1)/2, gravity's own energy w_U = 3 gamma - 2 beta + 1 + zeta2,
  internal energy w_Pi = 1 + zeta3, pressure w_p = 3 gamma + 3 zeta4   (A4 C3's bar: 2, 2, 1, 3; plain counting 1/2, -1/2, 1, 0).
Nordtvedt: eta = 4 beta - gamma - 3 - (10/3) xi - alpha1 + (2/3) alpha2 - (2/3) zeta1 - (1/3) zeta2.
Fully conservative theories (total four-momentum and angular momentum conserved) have alpha3 = zeta1 = zeta2 = zeta3 = zeta4 = 0.

Expected results, written down before the first run (2026-09-15):
  K1 with gamma = beta = 1, no preferred frame (alpha1 = alpha2 = xi = 0) and full conservation, the weights are exactly (2, 2, 1, 3)
     and eta = 0.
  K2 plain counting (1/2, -1/2, 1, 0) corresponds to zeta1 = -3, zeta2 = -5/2 and eta = 17/6, reproducing A3 C42 case B;
     rest mass only (weights 0, 0) gives zeta1 = -4, zeta2 = -2, eta = 10/3 (case A).
  K3 with gamma = beta = 1 and no preferred frame, eta depends only on 2 zeta1 + zeta2: zeta1 = 1, zeta2 = -2 gives eta = 0 while the
     weights are (2.5, 0, 1, 3), so the Moon test alone does not fix each weight; conservation fixes each one.
  K4 with full conservation but beta = 1 + 1e-4 (gamma = 1), eta = 4e-4, and the gravity's-own-energy weight moves to 2 - 2e-4.
Exit code: 0 if it completes.
"""
import sys
from fractions import Fraction as F


def weights(gamma, beta, alpha3=F(0), z1=F(0), z2=F(0), z3=F(0), z4=F(0)):
    return ((2 * gamma + 2 + alpha3 + z1) / 2, 3 * gamma - 2 * beta + 1 + z2, 1 + z3, 3 * gamma + 3 * z4)


def eta(gamma, beta, xi=F(0), a1=F(0), a2=F(0), z1=F(0), z2=F(0)):
    return 4 * beta - gamma - 3 - F(10, 3) * xi - a1 + F(2, 3) * a2 - F(2, 3) * z1 - F(1, 3) * z2


def zetas_from_weights(wv, wU, gamma=F(1), beta=F(1)):
    return 2 * wv - (2 * gamma + 2), wU - (3 * gamma - 2 * beta + 1)


def main():
    one = F(1)
    w1 = weights(one, one)
    e1 = eta(one, one)
    print("K1 full conservation, gamma = beta = 1: weights", tuple(str(x) for x in w1), "eta", e1)

    zB = zetas_from_weights(F(1, 2), F(-1, 2))
    eB = eta(one, one, z1=zB[0], z2=zB[1])
    zA = zetas_from_weights(F(0), F(0))
    eA = eta(one, one, z1=zA[0], z2=zA[1])
    print("K2 plain counting: zeta1 %s, zeta2 %s, eta %s ; rest mass only: zeta1 %s, zeta2 %s, eta %s" % (zB[0], zB[1], eB, zA[0], zA[1], eA))

    e3 = eta(one, one, z1=F(1), z2=F(-2))
    w3 = weights(one, one, z1=F(1), z2=F(-2))
    print("K3 zeta1 = 1, zeta2 = -2: eta %s, weights %s" % (e3, tuple(str(x) for x in w3)))

    b4 = one + F(1, 10000)
    e4 = eta(one, b4)
    w4 = weights(one, b4)
    print("K4 beta = 1 + 1e-4: eta %s (= %.1e), own-energy weight %s (= %.4f)" % (e4, float(e4), w4[1], float(w4[1])))

    checks = (
        ("K1 weights (2, 2, 1, 3), eta 0", w1 == (2, 2, 1, 3) and e1 == 0),
        ("K2 reproduces A3 cases A and B", zB == (-3, F(-5, 2)) and eB == F(17, 6) and zA == (-4, -2) and eA == F(10, 3)),
        ("K3 Moon test fixes only 2 zeta1 + zeta2", e3 == 0 and w3 == (F(5, 2), 0, 1, 3)),
        ("K4 beta off by 1e-4 gives eta 4e-4", e4 == F(4, 10000) and w4[1] == 2 - F(2, 10000)),
    )
    print("\nExpected results:")
    for label, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
