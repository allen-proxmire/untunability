"""Diagnostic after v2b run 1's mirror check (1.45e-4 at t = 20; not pre-registered): is the mismatch a code asymmetry
(present from the first steps) or round-off amplified by an instability (growing exponentially from about 1e-16)?
Reports the mirror error at t = 1, 2.5, 5, 10, 20 for three settings, plus the mirror error after one step."""
import math

import numpy as np

from rule_v2b import RuleB, mirror_perm, pure

L, D, GAMMA, V0, DT = 48, 3, 1.0, 0.05, 0.01
rng = np.random.default_rng(2468)
s0 = pure(1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2))
p = mirror_perm(L)
times = (1.0, 2.5, 5.0, 10.0, 20.0)
for g, theta0, mode in ((0.5, 0.4, "flow"), (0.5, 0.0, "flow"), (0.0, 0.4, "flow"), (0.5, 0.4, "const")):
    a, b = RuleB(L, D, GAMMA, g, theta0, V0, phase_mode=mode), RuleB(L, D, GAMMA, g, theta0, V0, phase_mode=mode)
    ra, rb = s0.copy(), s0[np.ix_(p, p)]
    out, t_done = [], 0.0
    ra, rb = a.step(ra, DT), b.step(rb, DT)
    one = float(np.max(np.abs(ra[np.ix_(p, p)] - rb)))
    t_done = DT
    for t in times:
        for _ in range(int(round((t - t_done) / DT))):
            ra, rb = a.step(ra, DT), b.step(rb, DT)
        t_done = t
        out.append(float(np.max(np.abs(ra[np.ix_(p, p)] - rb))))
    print("g %+.1f theta0 %.1f %s: one step %.1e; t = 1, 2.5, 5, 10, 20: %s"
          % (g, theta0, mode, one, " ".join("%.1e" % e for e in out)), flush=True)
