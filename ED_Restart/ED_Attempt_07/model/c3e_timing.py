"""C3e timing trial (note 23 running order; D35). Timing and harness only: no reading values printed.

Per size n = 20, 24: build; flat-start readings with the walk; 10 ticks for S0 (0,0,0) and S4 (1,1,1)
with the structure check, both budgets, the ceiling and the link-neutrality of paired flips.
Projection for T = 150 and 100: 20 growth runs, 2 no-ceiling contrast runs and 4 calibrations, 3 workers.
"""
import time
import numpy as np
from c3c import Slice3, SIGMA
from c3e import tick, slice_readings, FLAT_LINKS_PER_EVENT, CEILING

lines, per = [], {}
for n in (20, 24):
    t0 = time.perf_counter(); M = Slice3(n); t_build = time.perf_counter() - t0
    V0 = len(M.vt)
    t0 = time.perf_counter(); r = slice_readings(M, 0, with_walk=True); t_read = time.perf_counter() - t0
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
            res, pool = tick(M, b, omega, phi, rng, *setting, pool, cap=CEILING)
            assert not M.check(), "structure"
            assert len(M.val) + pool == BL, "link budget"
            assert max(len(x) for x in M.nbrs.values()) <= CEILING, "ceiling"
            assert res["flips_link_neutral"], "flips changed the link count"
        tt[name] = (time.perf_counter() - t0) / 10
    per[n] = dict(tick_S0=tt["S0"], tick_S4=tt["S4"], read=t_read, build=t_build)
    lines.append(f"n={n} (V={V0}): build {t_build:.1f} s; flat readings with walk {t_read:.1f} s "
                 f"(d_H defined {r['d_H'] is not None}, d_s defined {r['d_s'] is not None}, diameter {r['diameter']:.0f}); "
                 f"tick+checks S0 {tt['S0']:.1f} s, S4 {tt['S4']:.1f} s")
    print(lines[-1], flush=True)
for T in (150, 100):
    tot = 0.0
    for n, p in per.items():
        tot += 2 * (T * p["tick_S0"] + 3 * p["read"]) + 8 * (T * p["tick_S4"] + 3 * p["read"]) + 2 * p["read"] + 2 * p["build"]
    tot += 2 * (T * per[24]["tick_S4"] + 3 * per[24]["read"])  # the two no-ceiling contrast runs
    lines.append(f"T={T}: {tot/3600:.1f} h single process, {tot/3600/3:.1f} h on 3 workers")
print("\n".join(lines[-2:]))
open("c3e_timing.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
