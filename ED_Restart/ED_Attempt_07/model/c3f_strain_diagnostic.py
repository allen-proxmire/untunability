"""C3f strain diagnostic (NOT pre-registered; D41). Measures what the sync condition would bind on.

C3f's sync condition refuses a move that would leave a link carrying more than s_max. The timing trial
showed no refusals at s_max = 3x the flat calibration's largest link strain. This records, per tick, the
spread of link strains the model actually produces, and how many links would exceed 1x, 1.5x, 2x and 3x
the flat value, for settings A (1,1) and D (0,0) at V = 8,000 over 40 ticks. No verdict is read here.
"""
import time
import numpy as np
from c3c import Slice3, SIGMA, K
from c3d import slice_readings
from c3e import CEILING
from c3f import tick, FLAT_LINKS_PER_EVENT

n, T = 20, 40
M0 = Slice3(n)
flat = slice_readings(M0, 0, with_walk=False)["neck_strain"]
lines = [f"flat calibration largest link strain at V={n**3}: {flat:.3f}"]
print(lines[-1], flush=True)
for label, (alpha, lam) in (("A (1,1)", (1, 1)), ("D (0,0)", (0, 0))):
    M = Slice3(n); rng = np.random.default_rng(0)
    V0 = len(M.vt)
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - len(M.val)
    b = {v: 1.0 for v in M.vt}
    omega = {v: 1 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
    phi = {v: 0.0 for v in M.vt}
    t0 = time.perf_counter()
    for t in range(1, T + 1):
        r, pool = tick(M, b, omega, phi, rng, alpha, lam, pool, s_max=None, cap=CEILING)
        if t in (5, 10, 20, 30, 40):
            s = np.array([abs(phi[a] - phi[bb]) for a, bb in M.val]) / (SIGMA / K)
            over = [int((s > f * flat).sum()) for f in (1.0, 1.5, 2.0, 3.0)]
            lines.append(f"{label} tick {t:>3}: links {len(s)}, strain mean {s.mean():.2f}, 95th {np.percentile(s, 95):.2f}, "
                         f"max {s.max():.2f} ({s.max()/flat:.2f}x flat); links over 1x/1.5x/2x/3x flat: {over}")
            print(lines[-1], flush=True)
    lines.append(f"{label}: {time.perf_counter()-t0:.0f} s for {T} ticks")
open("c3f_strain_diagnostic.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
