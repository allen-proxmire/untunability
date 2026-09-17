"""C1 timing (note 3, running order step 1). Timing only: readings values are not results.

Times the build and all readings on the flat strip and on tree seed 0, and the
1,000-seed slice-length generation on 20 seeds, then estimates c1_run.py's total.
"""
import time
import numpy as np
from c1 import grow, slice_lengths, build
from readings_v2 import all_readings

T = 200
t0 = time.perf_counter()
lengths, offspring = grow(T, seed=0, flat_L=200)
A, _, _ = build(lengths, offspring)
tb = time.perf_counter() - t0
all_readings(A, np.random.default_rng(999))
tf = time.perf_counter() - t0
t1 = time.perf_counter()
lengths, offspring = grow(T, seed=0)
A, _, _ = build(lengths, offspring)
all_readings(A, np.random.default_rng(1000))
tt = time.perf_counter() - t1
t2 = time.perf_counter()
for s in range(20):
    slice_lengths(T, s)
ts = (time.perf_counter() - t2) / 20 * 1000
print(f"flat strip build {tb:.1f} s, build+readings {tf:.1f} s ({A.shape[0]} events in tree seed 0)")
print(f"tree seed 0 build+readings {tt:.1f} s")
print(f"slice lengths, 1,000 seeds: about {ts:.0f} s")
print(f"estimated c1_run.py total: about {(tf + 10 * tt + ts)/60:.1f} min (tree sizes vary by seed)")
