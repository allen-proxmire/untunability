"""C3c timing trial (note 18 running order; D26). Timing and harness only: no reading values printed.

Per size n = 16, 24: build; structure check; 10 growth ticks for S0 (0,0,0) and S4 (1,1,1) from the
flat start with the check after every tick; one readings call; one flip sweep for calibration RC.
Projection for T in (500, 300, 200): 12 runs per size (S0 at S0's tick time, S1-S5 at S4's), readings
at 3 checkpoints, plus calibrations (FC readings; RC 50 sweeps and readings), on 6 workers.
"""
import time
import numpy as np
from c3c import Slice3, tick, flip_randomize, slice_readings

lines, per = [], {}
for n in (16, 24):
    t0 = time.perf_counter(); M = Slice3(n); t_build = time.perf_counter() - t0
    t0 = time.perf_counter(); notes = M.check(); t_check = time.perf_counter() - t0
    t0 = time.perf_counter(); r = slice_readings(M, 0); t_read = time.perf_counter() - t0
    Mr = Slice3(n); rng = np.random.default_rng(7)
    t0 = time.perf_counter(); flip_randomize(Mr, 1, rng); t_sweep = time.perf_counter() - t0
    tt = {}
    for name, setting in (("S0", (0, 0, 0)), ("S4", (1, 1, 1))):
        M = Slice3(n); rng = np.random.default_rng(0)
        b = {v: 1.0 for v in M.vt}
        omega = {v: 1 + 0.0005 * rng.standard_normal() for v in M.vt}
        phi = {v: 0.0 for v in M.vt}
        t0 = time.perf_counter()
        for _ in range(10):
            tick(M, b, omega, phi, rng, *setting)
            assert not M.check()
        tt[name] = (time.perf_counter() - t0) / 10
    per[n] = dict(tick_S0=tt["S0"], tick_S4=tt["S4"], read=t_read, sweep=t_sweep, build=t_build)
    lines.append(f"n={n} (V={n**3}): build {t_build:.1f} s; start check {t_check:.1f} s (clean: {not notes}); "
                 f"tick+check S0 {tt['S0']:.1f} s, S4 {tt['S4']:.1f} s; readings {t_read:.1f} s "
                 f"(d_H defined: {r['d_H'] is not None and np.isfinite(r['d_H'])}, r_lo {r['r_lo']}, r_max {r['r_max']}); flip sweep {t_sweep:.1f} s")
    print(lines[-1], flush=True)
for T in (500, 300, 200):
    tot = 0.0
    for n, p in per.items():
        tot += 2 * (T * p["tick_S0"] + 3 * p["read"]) + 10 * (T * p["tick_S4"] + 3 * p["read"])
        tot += 2 * p["read"] + 50 * p["sweep"] + 2 * p["build"]
    lines.append(f"T={T}: {tot/3600:.1f} h single process, {tot/3600/6:.1f} h on 6 workers")
print("\n".join(lines[-3:]))
open("c3c_timing.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
