"""ED's strong-field object under D2 (a full locus is part of ED's meaning): photon sphere, shadow and core redshift (RD5).

From ED's rules (A1-ledger RD35, RD36): ticking slows by s = e^(-U), moving between loci by s^2, so light-like and clock-like
behaviour follow the isotropic exponential metric ds^2 = -e^(-2U) dt^2 + e^(2U) (dr^2 + r^2 dOmega^2). Weak field: U = m / r with
m = GM/c^2 (A1-ledger C104). Cap (A1-ledger RD14; D2): U <= 1, so for r <= m the metric is constant: a saturated core with clock
slowing e^(-1) relative to far away. Assumption carried into the strong field: U = m / r outside the core (A1-ledger RD37 matched
weights only at the orders tested).

Photon circular orbit where d/dr [ r^2 e^(2U) / e^(-2U) ] = 0; shadow (critical impact parameter) b = r e^(2U) at that radius.
Schwarzschild comparison: b = 3 sqrt(3) m. EHT Sgr A* fractional shadow deviations (Vagnozzi et al. 2022, arXiv:2205.07787):
delta = -0.08 +- 0.09 (VLTI prior), -0.04 +0.09 -0.10 (Keck prior).

Expected results, written down before the first run (2026-09-15):
  S1 photon circular orbit at r = 2m (to 1e-9), outside the core (r > m).
  S2 critical impact parameter b = 2e m = 5.43656 m (to 1e-6); ratio to 3 sqrt(3) m = 1.04627 (to 1e-5), i.e. a shadow 4.6% larger.
  S3 at the core edge (U = 1) clocks run at e^(-1) = 0.36788 of far-away clocks: redshift 1 + z = e, z = 1.71828.
  S4 the ratio's distance from the EHT Sgr A* deviations: above the VLTI-prior value by about 1.4 standard deviations and above the
     Keck-prior value by about 1.0 (using the upper errors); not excluded by shadow size alone at 2 standard deviations.
Exit code: 0 if it completes.
"""
import math
import sys

import numpy as np


def main():
    m = 1.0
    r = np.linspace(1.0001, 10.0, 2_000_001)
    f = r ** 2 * np.exp(4 * m / r)
    i = int(np.argmin(f))
    lo, hi = r[max(i - 2, 0)], r[min(i + 2, len(r) - 1)]
    g = lambda x: 2 * x - 4 * m
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(lo) * g(mid) <= 0:
            hi = mid
        else:
            lo = mid
    r_ph = 0.5 * (lo + hi)
    b = r_ph * math.exp(2 * m / r_ph)
    b_s = 3 * math.sqrt(3) * m
    ratio = b / b_s
    clock = math.exp(-1.0)
    z = math.e - 1
    delta = ratio - 1
    sig_vlti = (delta - (-0.08)) / 0.09
    sig_keck = (delta - (-0.04)) / 0.09
    print("S1 photon circular orbit r = %.10f m (grid minimum at %.6f m); core edge at r = %.1f m" % (r_ph, r[i], m))
    print("S2 critical impact parameter b = %.8f m; Schwarzschild 3 sqrt(3) m = %.8f m; ratio %.6f (delta = %+.4f)" % (b, b_s, ratio, delta))
    print("S3 core-edge clock rate e^-1 = %.6f; redshift 1 + z = %.6f, z = %.6f" % (clock, math.e, z))
    print("S4 distance above EHT Sgr A* deviations: VLTI prior %.2f standard deviations; Keck prior %.2f (upper errors)" % (sig_vlti, sig_keck))
    s1 = abs(r_ph - 2 * m) < 1e-9 and r_ph > m
    s2 = abs(b - 2 * math.e * m) < 1e-6 and abs(ratio - 1.04627) < 1e-5
    s3 = abs(clock - 0.36788) < 1e-5 and abs(z - 1.71828) < 1e-5
    s4 = 1.2 <= sig_vlti <= 1.6 and 0.8 <= sig_keck <= 1.2 and max(sig_vlti, sig_keck) < 2
    print("\nExpected results:")
    for label, ok in (("S1 photon orbit at 2m, outside the core", s1), ("S2 shadow 4.6% larger", s2),
                      ("S3 core redshift factor e", s3), ("S4 within 2 standard deviations of EHT Sgr A*", s4)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
