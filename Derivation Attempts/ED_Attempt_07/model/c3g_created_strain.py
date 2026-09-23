"""Created-link strain diagnostic (NOT pre-registered; D43).

C3f's sync condition screens links a move would CREATE, and it never fired. This measures the strain
carried by created links, against the flat calibration's link-strain distribution, so the threshold can
be set where it refuses a small but real fraction. Setting A (1,1) at V = 8,000, 25 ticks, seed 0.
"""
import numpy as np
from c3c import Slice3, SIGMA, K
from c3d import slice_readings
from c3e import CEILING
import c3f
from c3f import FLAT_LINKS_PER_EVENT

n, T = 20, 25
M0 = Slice3(n)
A0, ids0, pos0, ei0, ej0 = M0.adjacency()
from c3b import sync_steady_state
ss = sync_steady_state(A0, 0)
flat_max = ss["max_link_diff"]
lines = [f"flat calibration at V={n**3}: largest link strain {flat_max:.3f}"]
print(lines[-1], flush=True)

created = []
real_allowed = c3f.allowed


def spy_allowed(M, plan, pool, phi, s_max, gone=(), cap=CEILING):
    ok, born, dies, why = real_allowed(M, plan, pool, phi, None, gone=gone, cap=cap)
    if ok:
        dv = {}
        from c3c import edges_of
        for tid in plan[0]:
            for e in edges_of(M.tets[tid]):
                dv[e] = dv.get(e, 0) - 1
        for t in plan[1]:
            for e in edges_of(tuple(sorted(t))):
                dv[e] = dv.get(e, 0) + 1
        for e, d in dv.items():
            if d > 0 and M.val.get(e, 0) == 0 and e[0] in phi and e[1] in phi:
                created.append(abs(phi[e[0]] - phi[e[1]]) / (SIGMA / K))
    return ok, born, dies, why


c3f.allowed = spy_allowed
M = Slice3(n); rng = np.random.default_rng(0)
V0 = len(M.vt)
BL = round(FLAT_LINKS_PER_EVENT * V0)
pool = BL - len(M.val)
b = {v: 1.0 for v in M.vt}
omega = {v: 1 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
phi = {v: 0.0 for v in M.vt}
for t in range(1, T + 1):
    created.clear() if t == T - 4 else None      # keep the last five ticks' worth
    r, pool = c3f.tick(M, b, omega, phi, rng, 1.0, 1.0, pool, s_max=None, cap=CEILING)
    if t in (5, 15, T):
        s = np.array([abs(phi[a] - phi[bb]) for a, bb in M.val]) / (SIGMA / K)
        c = np.array(created) if created else np.zeros(1)
        lines.append(f"tick {t:>3}: all links mean {s.mean():.2f}, 95th {np.percentile(s, 95):.2f}, max {s.max():.2f} "
                     f"({s.max()/flat_max:.2f}x flat) | created links this window: {len(c)}, mean {c.mean():.2f}, "
                     f"95th {np.percentile(c, 95):.2f}, 99th {np.percentile(c, 99):.2f}, max {c.max():.2f}")
        print(lines[-1], flush=True)
open("c3g_created_strain.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
