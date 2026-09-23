"""C3d timing trial (note 21 running order; D32). Timing and harness only: no reading values printed.

Per size n = 20, 24: build; flat-start readings with the walk (the calibration gate's cost); 10 ticks
for S0 (0,0,0) and S4 (1,1,1) with the structure check, the link budget and the ceiling; one flip sweep
(calibration RC's cost). Projection for T = 200 and 150: 20 growth runs plus 4 calibrations on 3 workers.
"""
import time
import numpy as np
from c3c import Slice3, flip_randomize, SIGMA
from c3d import tick, slice_readings, FLAT_LINKS_PER_EVENT, DEGREE_CAP

lines, per = [], {}
for n in (20, 24):
    t0 = time.perf_counter(); M = Slice3(n); t_build = time.perf_counter() - t0
    V0 = len(M.vt)
    t0 = time.perf_counter(); r = slice_readings(M, 0, with_walk=True); t_read = time.perf_counter() - t0
    Mr = Slice3(n); rng = np.random.default_rng(7)
    t0 = time.perf_counter(); flip_randomize(Mr, 1, rng); t_sweep = time.perf_counter() - t0
    tt = {}
    for name, setting in (("S0", (0, 0, 0)), ("S4", (1, 1, 1))):
        M = Slice3(n); rng = np.random.default_rng(0)
        BL = round(FLAT_LINKS_PER_EVENT * V0)
        pool = BL - len(M.val)
        b = {v: 1.0 for v in M.vt}
        omega = {v: 1 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
        phi = {v: 0.0 for v in M.vt}
        t0 = time.perf_counter()
        for _ in range(10):
            res, pool = tick(M, b, omega, phi, rng, *setting, pool)
            assert not M.check(), "structure"
            assert len(M.val) + pool == BL, "budget"
            assert max(len(x) for x in M.nbrs.values()) <= DEGREE_CAP, "ceiling"
        tt[name] = (time.perf_counter() - t0) / 10
    per[n] = dict(tick_S0=tt["S0"], tick_S4=tt["S4"], read=t_read, sweep=t_sweep, build=t_build)
    lines.append(f"n={n} (V={V0}): build {t_build:.1f} s; flat readings with walk {t_read:.1f} s "
                 f"(d_H defined {r['d_H'] is not None}, d_s defined {r['d_s'] is not None}, radii {r['r_lo']}-{r['r_max']}, "
                 f"diameter {r['diameter']:.0f}); tick+checks S0 {tt['S0']:.1f} s, S4 {tt['S4']:.1f} s; flip sweep {t_sweep:.1f} s")
    print(lines[-1], flush=True)
for T in (200, 150):
    tot = 0.0
    for n, p in per.items():
        tot += 2 * (T * p["tick_S0"] + 3 * p["read"]) + 8 * (T * p["tick_S4"] + 3 * p["read"])
        tot += 2 * p["read"] + 50 * p["sweep"] + 2 * p["build"]
    lines.append(f"T={T}: {tot/3600:.1f} h single process, {tot/3600/3:.1f} h on 3 workers")
print("\n".join(lines[-2:]))
open("c3d_timing.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
