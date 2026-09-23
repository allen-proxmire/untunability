"""Arithmetic check for note 13 (road R4, the speed part). Not a model of ED; it checks the algebra of three ways to count a
zigzag body's own ticks, and one experimental comparison.

Picture (D25, D27, D28): every commitment is a hop to a neighbouring locus, one per substrate tick, so everything moves at c
(one locus per tick). In one space dimension a body makes n_R right hops and n_L left hops: total hops (the budget) t = n_R + n_L,
net motion x = n_R - n_L, speed beta = x / t. Light never turns (n_L = 0).

Three counting rules for a body's own ticks, all written from the picture before this script was run:
  S1 leftover budget: own = t - |x| = 2 min(n_R, n_L)          (ticks are the hops not spent on net motion)
  S2 pairing:         own = 2 sqrt(n_R n_L)                     (every right hop related to every left hop)
  S3 turns:           own = number of direction reversals of a periodic zigzag, with the moving zigzag's legs a, b
                      obtained from the resting legs k, k either by (S3a) a drift that keeps a + b = 2k, or
                      (S3b) a Doppler scaling a = k D, b = k / D with D = sqrt((1 + beta) / (1 - beta)), which keeps a b = k^2.

Expected results, written down before the first run (2026-09-15):
  Z1 identity: for all n_R, n_L >= 0, (2 sqrt(n_R n_L))^2 + (n_R - n_L)^2 = (n_R + n_L)^2 exactly (integers up to 200).
  Z2 S1 gives own/t = 1 - beta (linear); S2 gives own/t = sqrt(1 - beta^2) (special relativity's rate), to 1e-12 on a grid.
  Z3 light (n_L = 0): own ticks 0 under S1, S2 and S3.
  Z4 S3a: turns per unit coordinate time stay 1/k at every speed (no time dilation); S3b: turns per unit time are
     (1/k) sqrt(1 - beta^2) (special relativity's rate) to 1e-12.
  Z5 muons at gamma = 29.33 (Bailey et al. 1977, agreement with special relativity to 2e-3): S2/S3b give lifetime dilation 29.33;
     S1 gives about 1720, off by a factor of about 59.
Exit code: 0 if it completes.
"""
import math
import sys


def main():
    z1 = all((2 * math.isqrt(a * b)) ** 2 == 4 * a * b and 4 * a * b + (a - b) ** 2 == (a + b) ** 2
             for a in range(201) for b in range(201) if math.isqrt(a * b) ** 2 == a * b) and \
        all(abs(4 * a * b + (a - b) ** 2 - (a + b) ** 2) == 0 for a in range(201) for b in range(201))
    print("Z1 identity 4 nR nL + (nR - nL)^2 = (nR + nL)^2 holds for all integers to 200:", z1)

    worst1 = worst2 = 0.0
    for nR in range(1, 400):
        for nL in range(0, nR + 1):
            t, x = nR + nL, nR - nL
            beta = x / t
            s1 = (t - abs(x)) / t
            s2 = 2 * math.sqrt(nR * nL) / t
            worst1 = max(worst1, abs(s1 - (1 - beta)))
            worst2 = max(worst2, abs(s2 - math.sqrt(1 - beta * beta)))
    print("Z2 max |S1 - (1 - beta)| = %.2e ; max |S2 - sqrt(1 - beta^2)| = %.2e" % (worst1, worst2))

    light = (100 - 100, 2 * math.sqrt(100 * 0), 0)
    print("Z3 light (nR = 100, nL = 0): S1 = %s, S2 = %s, S3 turns = %s" % light)

    k = 10.0
    worst3a = worst3b = 0.0
    for i in range(1, 99):
        beta = i / 100
        a, b = k + beta * k, k - beta * k          # S3a: drift, a + b = 2k gives net speed (a - b)/(a + b) = beta
        rate_a = 2 / (a + b)
        worst3a = max(worst3a, abs(rate_a - 1 / k))
        D = math.sqrt((1 + beta) / (1 - beta))
        a, b = k * D, k / D                        # S3b: Doppler legs, net speed (a - b)/(a + b) = beta
        assert abs((a - b) / (a + b) - beta) < 1e-12
        rate_b = 2 / (a + b)
        worst3b = max(worst3b, abs(rate_b - math.sqrt(1 - beta * beta) / k))
    print("Z4 S3a max |turn rate - 1/k| = %.2e (no dilation) ; S3b max |turn rate - sqrt(1 - beta^2)/k| = %.2e" % (worst3a, worst3b))

    gamma = 29.33
    beta = math.sqrt(1 - 1 / gamma ** 2)
    dil_s2 = 1 / math.sqrt(1 - beta ** 2)
    dil_s1 = 1 / (1 - beta)
    print("Z5 muons gamma = 29.33: S2/S3b dilation %.2f ; S1 dilation %.0f (ratio %.1f)" % (dil_s2, dil_s1, dil_s1 / dil_s2))

    checks = (
        ("Z1 identity", z1),
        ("Z2 S1 linear, S2 square-root", worst1 < 1e-12 and worst2 < 1e-12),
        ("Z3 light has no own ticks", light == (0, 0.0, 0)),
        ("Z4 S3a no dilation, S3b special-relativity rate", worst3a < 1e-12 and worst3b < 1e-12),
        ("Z5 muons: S2/S3b 29.33, S1 about 1720", abs(dil_s2 - 29.33) < 0.01 and abs(dil_s1 - 1720) < 10),
    )
    print("\nExpected results:")
    for label, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
