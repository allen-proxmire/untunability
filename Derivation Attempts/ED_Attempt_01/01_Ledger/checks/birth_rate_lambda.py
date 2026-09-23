"""Check C211: what ED's even birth chance (RD29) must be to make today's dark energy, and how big its fluctuations are.

Assumptions (stated before running):
  - One step is one Planck time, and a locus holds a fixed Planck-sized volume (RD15 leaves scale open; this picks one).
  - If every locus has birth chance p per step, the number of loci grows as e^(p t), volume grows the same way,
    so the scale factor grows as e^(p t / 3): the expansion rate from births is H = p / 3 per step.
  - Dark energy alone would drive expansion at H_L = H0 sqrt(Omega_L). So p = 3 H_L t_P.
  - Lambda in Planck units: Lambda l_P^2 = 3 (H_L t_P)^2.
  - Sorkin's everpresent estimate: Lambda ~ 1 / sqrt(V4), with V4 ~ (1 / (H0 t_P))^4 in Planck units.
  - Random (Poisson) births: over one Hubble time in one Hubble volume the number of births is about N (one e-fold
    order), so its relative fluctuation is about 1 / sqrt(N), with N = (4 pi / 3) (c / (H0 l_P))^3.
Inputs: H0 = 67.4 km/s/Mpc, Omega_L = 0.685 (Planck 2018, C140), t_P = 5.391e-44 s, l_P = 1.616e-35 m.

Predictions frozen before the first run (2026-09-14):
  P1  H0 t_P = 1.18e-61 within 1%.
  P2  p = 3 H_L t_P = 2.92e-61 per step within 2%.
  P3  Lambda l_P^2 = 2.85e-122 within 3%.
  P4  Sorkin's 1 / sqrt(V4) is within a factor of 10 of Lambda l_P^2.
  P5  The relative fluctuation of Poisson births in a Hubble volume over a Hubble time is below 1e-90.
"""
import math
import sys

H0 = 67.4e3 / 3.0857e22        # s^-1
OMEGA_L = 0.685
T_P, L_P, C = 5.391e-44, 1.616e-35, 2.998e8

h0tp = H0 * T_P
HL = H0 * math.sqrt(OMEGA_L)
p = 3 * HL * T_P
lam = 3 * (HL * T_P) ** 2
sorkin = 1 / math.sqrt((1 / h0tp) ** 4)
N = (4 * math.pi / 3) * (C / (H0 * L_P)) ** 3
fluct = 1 / math.sqrt(N)

print("H0 t_P                      %.4e" % h0tp)
print("birth chance p per step     %.4e" % p)
print("Lambda l_P^2                %.4e" % lam)
print("Sorkin 1/sqrt(V4)           %.4e  (ratio to Lambda l_P^2: %.2f)" % (sorkin, sorkin / lam))
print("loci in a Hubble volume     %.4e" % N)
print("Poisson relative fluctuation %.4e" % fluct)

checks = [
    ("P1 H0 t_P = 1.18e-61 within 1%", abs(h0tp / 1.18e-61 - 1) < 0.01),
    ("P2 p = 2.92e-61 within 2%", abs(p / 2.92e-61 - 1) < 0.02),
    ("P3 Lambda l_P^2 = 2.85e-122 within 3%", abs(lam / 2.85e-122 - 1) < 0.03),
    ("P4 Sorkin estimate within a factor of 10", 0.1 < sorkin / lam < 10),
    ("P5 Poisson fluctuation below 1e-90", fluct < 1e-90),
]
ok = True
for name, passed in checks:
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
