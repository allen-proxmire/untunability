"""Check C230: what (3 / 8 pi) H0^2 M_P^2 is (Allen's 'flow meets boundary' thought).

In units with hbar = c = 1 and M_P the Planck mass (G = 1 / M_P^2):
  rho_crit = 3 H^2 / (8 pi G) = (3 / 8 pi) H^2 M_P^2       (critical density: the density a flat universe needs)
  rho_L    = Omega_L rho_crit                               (the dark energy density)
  Lambda   = 8 pi G rho_L = 3 Omega_L H^2                  (the cosmological constant, a curvature: 1 / length^2)
So (3 / 8 pi) H0^2 M_P^2 is the critical density, not Lambda itself; the dark energy density is 0.685 times it.
Inputs: H0 = 67.4 km/s/Mpc, Omega_L = 0.685 (C140); G = 6.674e-11, c = 2.998e8, t_P = 5.391e-44 s.

Predictions frozen before the first run (2026-09-14):
  P1  rho_crit in SI is 8.5e-27 kg/m^3 within 2%.
  P2  In Planck units rho_crit = (3 / 8 pi) (H0 t_P)^2 = 1.66e-123 within 2%, and rho_L = 1.13e-123 within 2%.
  P3  Lambda l_P^2 = 8 pi rho_L (Planck units) agrees with birth_rate_lambda.py's 2.8495e-122 to 1e-3 relative.
  P4  rho_L / rho_crit = 0.685 exactly (by definition), and Lambda / (3 H0^2) = 0.685.
"""
import math
import sys

H0 = 67.4e3 / 3.0857e22
OMEGA_L = 0.685
G, C, T_P = 6.674e-11, 2.998e8, 5.391e-44

rho_crit_si = 3 * H0 ** 2 / (8 * math.pi * G)
h = H0 * T_P
rho_crit_pl = (3 / (8 * math.pi)) * h ** 2
rho_L_pl = OMEGA_L * rho_crit_pl
lam_pl = 8 * math.pi * rho_L_pl
lam_over = lam_pl / (3 * h ** 2)

print("rho_crit (SI)            %.4e kg/m^3" % rho_crit_si)
print("rho_crit (Planck units)  %.4e" % rho_crit_pl)
print("rho_L (Planck units)     %.4e" % rho_L_pl)
print("Lambda l_P^2             %.4e" % lam_pl)
print("Lambda / (3 H0^2)        %.4f" % lam_over)

checks = [
    ("P1 rho_crit = 8.5e-27 kg/m^3 within 2%", abs(rho_crit_si / 8.5e-27 - 1) < 0.02),
    ("P2 rho_crit 1.66e-123 and rho_L 1.13e-123 within 2%", abs(rho_crit_pl / 1.66e-123 - 1) < 0.02 and abs(rho_L_pl / 1.13e-123 - 1) < 0.02),
    ("P3 Lambda l_P^2 matches 2.8495e-122 to 1e-3", abs(lam_pl / 2.8495e-122 - 1) < 1e-3),
    ("P4 ratios equal 0.685", abs(rho_L_pl / rho_crit_pl - 0.685) < 1e-12 and abs(lam_over - 0.685) < 1e-12),
]
ok = True
for name, passed in checks:
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
