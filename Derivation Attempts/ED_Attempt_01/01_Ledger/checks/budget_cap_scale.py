"""How close ordinary matter comes to the budget cap (U = 1).

Question (G35): could a locus at full budget be what forces a draw?

Link used: in the rule the local rate is 1 - U (rule_v0.rate, RD14, RD16).
Weak-field gravity slows clocks by a fraction GM/(r c^2) (T1, T3). So to pass
T3, U must be about GM/(r c^2) wherever gravity is weak. This is the weak-field
identification only; it says nothing exact near U = 1.

Predictions frozen before the first run (2026-09-13):
  P1  Earth's surface: U below 1e-8.
  P2  Sun's surface: U below 1e-5.
  P3  A neutron star's surface: U between 0.05 and 0.5 (the only everyday-physics
      object that comes near the cap is extreme).
  P4  One electron or one proton, one Planck length away: U below 1e-18
      (so a single particle does not fill its own locus if steps are Planck-sized).
"""

G = 6.67430e-11        # m^3 kg^-1 s^-2
c = 2.99792458e8       # m/s
hbar = 1.054571817e-34 # J s
M_sun = 1.98847e30     # kg
M_earth = 5.9722e24    # kg
R_earth = 6.371e6      # m
R_sun = 6.957e8        # m
m_e = 9.1093837e-31    # kg
m_p = 1.67262192e-27   # kg
l_P = (hbar * G / c**3) ** 0.5


def U(M, r):
    return G * M / (r * c**2)


cases = [
    ("P1 Earth surface", U(M_earth, R_earth), lambda u: u < 1e-8),
    ("P2 Sun surface", U(M_sun, R_sun), lambda u: u < 1e-5),
    ("P3 neutron star (1.4 Msun, 12 km)", U(1.4 * M_sun, 1.2e4), lambda u: 0.05 < u < 0.5),
    ("P4 electron at one Planck length", U(m_e, l_P), lambda u: u < 1e-18),
    ("P4 proton at one Planck length", U(m_p, l_P), lambda u: u < 1e-18),
]

ok = True
for name, u, test in cases:
    passed = test(u)
    ok &= passed
    print(f"{name:40s} U = {u:.3e}  {'PASS' if passed else 'FAIL'}")

print(f"Planck length used: {l_P:.4e} m")
print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
