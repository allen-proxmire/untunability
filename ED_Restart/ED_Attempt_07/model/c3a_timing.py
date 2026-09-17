"""C3a timing trial (note 13 running order; D19). Timing only: no readings values kept or printed.

For each size n in (20, 40, 80): 20 growth ticks for rule U and Q2 from the flat start (structure
check every tick, as in the runs), one slice readings call and one eccentricity call on the grown
slice (only whether the readings are defined is printed), and for n = 20 a spacetime pattern of
100 ticks with one readings call. Calibration R: 2 flip sweeps on n = 80, scaled to 200.
Projection: 36 growth runs (12 settings x 3 seeds) of T = 1,000 ticks with readings at 4
checkpoints, eccentricity at T, spacetime readings for n = 20; plus calibrations; on 6 workers.
"""
import time
import numpy as np
from c3a import Torus, grow_tick, flip_randomize, slice_readings, mean_eccentricity, slice_edges, build_spacetime
from readings_v2 import all_readings

T = 1000
lines = []
tick = {}
read = {}
for n in (20, 40, 80):
    for lam in (None, 2.0):
        M = Torus(n); b = {v: 1.0 for v in M.ring}; rng = np.random.default_rng(0)
        t0 = time.perf_counter()
        for _ in range(20):
            grow_tick(M, b, rng, lam)
            assert not M.check()
        tick[(n, lam)] = (time.perf_counter() - t0) / 20
    t0 = time.perf_counter(); r = slice_readings(M, 1); t_read = time.perf_counter() - t0
    t0 = time.perf_counter(); mean_eccentricity(M, 1); t_ecc = time.perf_counter() - t0
    read[n] = t_read + t_ecc
    defined = r["d_H"] is not None and np.isfinite(r["d_H"])
    lines.append(f"n={n} (L*={n*n}): tick U {tick[(n, None)]*1e3:.1f} ms, Q2 {tick[(n, 2.0)]*1e3:.1f} ms (with structure check); "
                 f"slice readings {t_read:.1f} s, eccentricity {t_ecc:.2f} s; readings defined on this slice: {defined} "
                 f"(r_lo {r['r_lo']}, r_max {r['r_max']})")
    print(lines[-1], flush=True)

M = Torus(20); b = {v: 1.0 for v in M.ring}; rng = np.random.default_rng(0)
snaps = []
for _ in range(100):
    e = slice_edges(M); rec = {}
    grow_tick(M, b, rng, None, record=rec)
    snaps.append((e, rec))
A = build_spacetime(snaps)
t0 = time.perf_counter(); rr = all_readings(A, np.random.default_rng(2)); t_st = time.perf_counter() - t0
lines.append(f"spacetime n=20, 100 ticks: {A.shape[0]} events, readings {t_st:.1f} s, defined {bool(np.isfinite(rr['d_H']))}")
print(lines[-1], flush=True)

M = Torus(80); rng = np.random.default_rng(7)
t0 = time.perf_counter(); flip_randomize(M, 2, rng); t_flip = (time.perf_counter() - t0) / 2
assert not M.check()
lines.append(f"calibration R: {t_flip:.1f} s per sweep at n=80; 200 sweeps {200*t_flip/60:.1f} min")

total = 0.0
for n in (20, 40, 80):
    for lam in (None, 0.5, 1.0, 2.0):
        per = T * tick[(n, None if lam is None else 2.0)] + 4 * read[n] + (t_st if n == 20 else 0)
        total += 3 * per
lines.append(f"projected growth runs: {total/3600:.2f} h single process, {total/3600/6:.2f} h on 6 workers "
             f"(largest single run {T*tick[(80, 2.0)]/60 + 4*read[80]/60:.1f} min); calibrations {(200*t_flip + 2*read[80])/60:.1f} min")
print("\n".join(lines[-2:]))
open("c3a_timing.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
