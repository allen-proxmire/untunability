"""Check C207: what ED's budget counts, and the post-Newtonian tests it then passes or fails (Nordtvedt, G39).

PPN metric, g00 terms (Will 2014, Box 2, with xi = 0):
  -2 beta U^2 + (2 gamma + 2 + alpha3 + zeta1) Phi1 + 2 (3 gamma - 2 beta + 1 + zeta2) Phi2
  + 2 (1 + zeta3) Phi3 + 2 (3 gamma + 3 zeta4) Phi4
with Phi1 = source kinetic energy (rho v^2), Phi2 = source gravitational energy (rho U), Phi3 = source internal
energy (rho Pi), Phi4 = source pressure, each spread as 1/r.
Nordtvedt (Eq. 66): eta_N = 4 beta - gamma - 3 - (10/3) xi - alpha1 + (2/3) alpha2 - (2/3) zeta1 - (1/3) zeta2.
Bounds (Table 4): eta_N 2.3e-4, zeta1 2e-2, zeta2 4e-5, zeta3 1e-8, alpha3 4e-20.

ED so far: gamma = 1 (RD35), beta = 1 (RD36), clocks at e^(-U_total), with U_total a linear sum of 1/r
contributions from whatever the budget counts. If a density s sources the budget, it adds 2 x (its share) to g00:
  rest mass rho          -> U        (always)
  internal energy rho Pi -> c3 = 2   if counted, else 0
  kinetic energy rho v^2 / 2 -> c1 = 1 if counted, else 0
  gravitational energy -rho U / 2 -> c2 = -1 if counted, else 0
  pressure p             -> c4 = 2   if counted, else 0
Solving the coefficients gives zeta3 = c3/2 - 1, zeta2 = c2/2 - (3 gamma - 2 beta + 1), alpha3 + zeta1 = c1 - 2 gamma - 2,
zeta4 = c4/6 - gamma. For eta_N, alpha1 = alpha2 = alpha3 = xi = 0 are assumed (ED has no velocity-dependent or
preferred-frame terms worked out; this is an assumption).

Caveats: this treats ED's effective metric as if it were in the standard PPN gauge with ED's U as the PPN U, and the
c-values are Claude's reading of "what the budget counts". It shows the size of any mismatch, not a derivation.

Scenarios:
  A  budget counts rest mass only (RD14 as written): c1 = c2 = c3 = c4 = 0
  B  budget counts all commitment linearly (rest, internal, kinetic, gravitational energy), not pressure:
     c1 = 1, c2 = -1, c3 = 2, c4 = 0
  GR the coefficients GR needs: c1 = 4, c2 = 4, c3 = 2, c4 = 6

Predictions frozen before the first run (2026-09-14):
  P1  A: zeta3 = -1, zeta2 = -2, zeta1 = -4, eta_N = 10/3 (to 1e-12); fails zeta3, zeta2, zeta1 and eta_N bounds,
      eta_N by more than 10^4 times its bound.
  P2  B: zeta3 = 0 (passes), zeta2 = -2.5, zeta1 = -3, eta_N = 17/6 (to 1e-12); fails zeta2, zeta1 and eta_N.
  P3  GR: all zero, eta_N = 0; passes everything.
  P4  For A and B, the Earth-Moon Nordtvedt signal eta_N x (4.6e-10 - 0.2e-10) exceeds the level allowed by the
      eta_N bound (2.3e-4 x 4.4e-10) by more than 10^4.
"""
import sys

GAMMA, BETA = 1.0, 1.0
BOUNDS = {"eta_N": 2.3e-4, "zeta1": 2e-2, "zeta2": 4e-5, "zeta3": 1e-8}
EARTH_MOON = 4.6e-10 - 0.2e-10

scenarios = {"A rest mass only": (0, 0, 0, 0), "B all commitment, linear": (1, -1, 2, 0), "GR": (4, 4, 2, 6)}


def params(c1, c2, c3, c4):
    zeta3 = c3 / 2 - 1
    zeta2 = c2 / 2 - (3 * GAMMA - 2 * BETA + 1)
    zeta1 = c1 - 2 * GAMMA - 2  # alpha3 = 0 assumed
    zeta4 = c4 / 6 - GAMMA
    eta = 4 * BETA - GAMMA - 3 - (2 / 3) * zeta1 - (1 / 3) * zeta2
    return {"zeta1": zeta1, "zeta2": zeta2, "zeta3": zeta3, "zeta4": zeta4, "eta_N": eta}


res = {}
for name, c in scenarios.items():
    p = params(*c)
    res[name] = p
    fails = [k for k in BOUNDS if abs(p[k]) > BOUNDS[k]]
    signal = abs(p["eta_N"]) * EARTH_MOON
    allowed = BOUNDS["eta_N"] * EARTH_MOON
    print("%-26s zeta1 %+.4f  zeta2 %+.4f  zeta3 %+.4f  zeta4 %+.4f  eta_N %+.6f  fails: %s  Earth-Moon signal %.2e (allowed %.2e, x%.0f)"
          % (name, p["zeta1"], p["zeta2"], p["zeta3"], p["zeta4"], p["eta_N"], ", ".join(fails) or "none", signal, allowed, signal / allowed))

A, B, G = res["A rest mass only"], res["B all commitment, linear"], res["GR"]


def fails(p):
    return {k for k in BOUNDS if abs(p[k]) > BOUNDS[k]}


checks = [
    ("P1 A: zeta3 -1, zeta2 -2, zeta1 -4, eta_N 10/3, fails all four, eta_N > 1e4 x bound",
     abs(A["zeta3"] + 1) < 1e-12 and abs(A["zeta2"] + 2) < 1e-12 and abs(A["zeta1"] + 4) < 1e-12
     and abs(A["eta_N"] - 10 / 3) < 1e-12 and fails(A) == set(BOUNDS) and abs(A["eta_N"]) > 1e4 * BOUNDS["eta_N"]),
    ("P2 B: zeta3 0, zeta2 -2.5, zeta1 -3, eta_N 17/6, fails zeta1, zeta2, eta_N",
     abs(B["zeta3"]) < 1e-12 and abs(B["zeta2"] + 2.5) < 1e-12 and abs(B["zeta1"] + 3) < 1e-12
     and abs(B["eta_N"] - 17 / 6) < 1e-12 and fails(B) == {"zeta1", "zeta2", "eta_N"}),
    ("P3 GR: all zero, passes", all(abs(v) < 1e-12 for v in G.values()) and not fails(G)),
    ("P4 A and B Earth-Moon signal more than 1e4 x allowed",
     all(abs(p["eta_N"]) * EARTH_MOON > 1e4 * BOUNDS["eta_N"] * EARTH_MOON for p in (A, B))),
]
ok = True
for name, passed in checks:
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
