"""Escape check under its exit rule (RD6; note 5; D2): how much of the energy released at ED's saturated core reaches far away?

Geometry (as strong_field_check.py): isotropic exponential metric ds^2 = -e^(-2U) dt^2 + e^(2U)(dr^2 + r^2 dOmega^2), U = m / r
for r > m (m = GM/c^2), and U = 1 inside the core r <= m (flat, rescaled). Light: refractive index n(r) = e^(2U); impact
parameter b = n(r) r sin(alpha) for local angle alpha from the radial direction, conserved along the ray.

Energy: matter falling from rest far away has conserved energy 1 (per unit rest-mass energy). If it is brought to rest and
thermalized at the core edge (U = 1), the heat released, measured far away, is 1 - e^(-1).

Escape of light emitted isotropically by a static emitter at the core edge r0 = m:
  outward rays escape if b <= min over r >= r0 of n(r) r (no turning point on the way out);
  inward rays enter the core; since the core is flat and has no horizon, a transparent core returns them to the edge on the far
  side heading outward with the same b, so they escape by the same condition.
The minimum is found on a grid (not from the formula), and the escaping solid-angle fraction by Monte Carlo over 2,000,000
isotropic directions, and compared with the closed form 1 - cos(alpha_c), sin(alpha_c) = 2e m / (m e^2) = 2/e.

Readings of f = (energy reaching far away) / (accreted rest-mass energy):
  (1) single emission, outward directions only: f1 = (1 - e^-1) x (escaping share of all directions that are outward);
  (2) single emission, all directions, transparent core: f2 = (1 - e^-1) x (escaping share of all directions);
  (3) steady state, unescaped light reabsorbed and re-emitted, no energy sink (no horizon): f3 = 1 - e^-1.
f_min = min(f1, f2, f3).

Exit rule (RD6, confirmed before running): if f_min > 0.004, record that a full locus with ED's current rate law conflicts
with the horizon evidence and close ED's strong-field line.

Expected results, written down before the first run (2026-09-15):
  X1 released heat 1 - e^-1 = 0.63212 (to 1e-5).
  X2 grid minimum of n(r) r beyond the core edge at r = 2m with value 2e m = 5.43656 m (to 1e-4); critical sin(alpha) = 2/e = 0.73576.
  X3 escaping share: outward-only 0.16138, all directions 0.32276 (Monte Carlo within 0.001 of these).
  X4 f1 = 0.102, f2 = 0.204, f3 = 0.632 (to 0.002); f_min = f1 = 0.102, above 0.004.
  Exit: the rule fires; ED's strong-field line closes as in conflict with the horizon evidence.
Exit code: 0 if it completes.
"""
import math
import sys

import numpy as np


def main():
    m = 1.0
    r0 = m
    r = np.linspace(r0, 200.0, 4_000_001)
    nr = np.exp(2 * m / r) * r
    i = int(np.argmin(nr))
    bmin = float(nr[i])
    n0r0 = math.exp(2.0) * r0
    sin_c = bmin / n0r0
    released = 1 - math.exp(-1)

    rng = np.random.default_rng(271828)
    N = 2_000_000
    cos_a = rng.uniform(-1, 1, N)
    sin_a = np.sqrt(1 - cos_a ** 2)
    b = n0r0 * sin_a
    escapes = b <= bmin
    share_all = float(np.mean(escapes))
    share_out = float(np.mean(escapes & (cos_a > 0)))
    closed_all = 1 - math.sqrt(1 - (2 / math.e) ** 2)
    closed_out = closed_all / 2

    f1, f2, f3 = released * share_out, released * share_all, released
    fmin = min(f1, f2, f3)
    fires = fmin > 0.004

    print("X1 released heat at the core edge (far-away units): %.6f" % released)
    print("X2 grid minimum of n(r) r at r = %.5f m, value %.6f m; critical sin(alpha) = %.6f (2/e = %.6f)" % (r[i], bmin, sin_c, 2 / math.e))
    print("X3 escaping share of directions: outward-only %.5f (closed form %.5f); all directions %.5f (closed form %.5f)" % (share_out, closed_out, share_all, closed_all))
    print("X4 f1 (single, outward) = %.4f; f2 (single, all, transparent core) = %.4f; f3 (steady state) = %.4f; f_min = %.4f" % (f1, f2, f3, fmin))
    print("\nExit rule (RD6): f_min = %.4f %s 0.004" % (fmin, ">" if fires else "<="))
    print("VERDICT: %s" % ("the rule fires: a full locus with ED's current rate law conflicts with the horizon evidence; ED's strong-field line closes"
                            if fires else "the rule does not fire; ED's strong-field line stays open"))
    x1 = abs(released - 0.63212) < 1e-5
    x2 = abs(r[i] - 2 * m) < 1e-3 and abs(bmin - 2 * math.e * m) < 1e-4 and abs(sin_c - 0.73576) < 1e-4
    x3 = abs(share_out - 0.16138) < 0.001 and abs(share_all - 0.32276) < 0.001
    x4 = abs(f1 - 0.102) < 0.002 and abs(f2 - 0.204) < 0.002 and abs(f3 - 0.632) < 0.002 and fmin == f1 and fmin > 0.004
    print("\nExpected results:")
    for label, ok in (("X1 released heat 1 - 1/e", x1), ("X2 barrier at 2m, critical sin 2/e", x2), ("X3 escaping shares", x3),
                      ("X4 fractions and f_min", x4), ("Exit: the rule fires", fires)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
