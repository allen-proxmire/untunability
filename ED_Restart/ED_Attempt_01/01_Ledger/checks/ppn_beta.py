"""Check C203: the PPN parameter beta implied by ED's clock-rate function (C201, RD36).

If a clock at used budget U runs at rate r(U), then -g00 = r(U)^2 = 1 - 2U + 2 beta U^2 + ...,
so beta = (r^2)''(0) / 4 (and the first-order term needs (r^2)'(0) = -2). Mercury's perihelion
advance is 42.98" per century x (2 + 2 gamma - beta) / 3 (Will 2014, Eq. 65, ignoring J2), with
gamma = 1 (RD35). Measured: beta - 1 = (-4.1 +- 7.8) x 10^-5 (C200).

Predictions frozen before the first run (2026-09-14):
  P1  linear rate r = 1 - U: first-order coefficient -2; beta = 0.5 to 1e-6; perihelion 50.14" per century
      (to 0.01"); excluded (|beta - 1| more than 1000 times the measured uncertainty).
  P2  exponential rate r = e^(-U): first-order coefficient -2; beta = 1 to 1e-6; perihelion 42.98";
      consistent with the measurement at this order.

Change after freezing (2026-09-14): the first run failed P2 only on the first-order coefficient,
-2.0000013 against the 1e-6 tolerance. That is the finite-difference error of the method with step
1e-3 (about h^2 x 4/3 = 1.3e-6), not the rate function; beta, the perihelion and the comparison
with measurement came out as predicted. The step was changed to 1e-4 (error about 1e-8);
predictions and tolerances unchanged.
"""
import math
import sys

H_STEP = 1e-4
MEASURED, SIGMA = -4.1e-5, 7.8e-5


def coefficients(rate):
    f = lambda U: rate(U) ** 2
    d1 = (f(H_STEP) - f(-H_STEP)) / (2 * H_STEP)
    d2 = (f(H_STEP) - 2 * f(0.0) + f(-H_STEP)) / H_STEP ** 2
    return d1, d2 / 4


rates = {"linear 1 - U": lambda U: 1 - U, "exponential e^(-U)": lambda U: math.exp(-U)}
ok = True
out = {}
for name, rate in rates.items():
    d1, beta = coefficients(rate)
    perihelion = 42.98 * (2 + 2 * 1.0 - beta) / 3
    sigmas = abs(beta - 1 - MEASURED) / SIGMA
    out[name] = (d1, beta, perihelion, sigmas)
    print("%-20s first-order %.6f  beta %.6f  perihelion %.2f\" per century  %.0f sigma from measurement"
          % (name, d1, beta, perihelion, sigmas))

d1, b, p, s = out["linear 1 - U"]
p1 = abs(d1 + 2) < 1e-6 and abs(b - 0.5) < 1e-6 and abs(p - 50.14) < 0.01 and s > 1000
d1e, be, pe, se = out["exponential e^(-U)"]
p2 = abs(d1e + 2) < 1e-6 and abs(be - 1) < 1e-6 and abs(pe - 42.98) < 0.01 and se < 2
for name, passed in (("P1 linear rate gives beta 1/2, excluded", p1), ("P2 exponential rate gives beta 1, consistent", p2)):
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
