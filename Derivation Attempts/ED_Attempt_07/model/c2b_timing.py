"""C2b timing trial (note 9 running order; D11). Timing only: no readings kept.

For every (d, n, slice kind, noise type): time building the slice (seed 0),
the tilt pairs, and 500 update steps; project one run as
build + pairs + T * step + (300 tilt samples for the control). A harness smoke
test runs the smallest 3D random slice with fresh noise end to end, only to
check the code path; its numbers are not results.
"""
import time
import numpy as np
from c2b import SIZES, run_length, grid_slice, random_slice, tilt_pairs, simulate

STEPS = 500
total = 0.0
lines = []
for d in (1, 2, 3):
    for n in SIZES[d]:
        for kind in ("G", "R"):
            t0 = time.perf_counter()
            sl = grid_slice(d, n) if kind == "G" else random_slice(d, n, 0)
            t_build = time.perf_counter() - t0
            t0 = time.perf_counter()
            pairs = tilt_pairs(sl, 0)
            t_pairs = time.perf_counter() - t0
            t0 = time.perf_counter()
            psi = np.random.default_rng(0).standard_normal(sl["N"])
            for _ in range(20):
                for a, b in pairs.values():
                    np.mean((psi[a] - psi[b]) ** 2)
            t_sample = (time.perf_counter() - t0) / 20
            for fresh in (False, True):
                t0 = time.perf_counter()
                simulate(sl, 0, fresh, steps=STEPS)
                t_step = (time.perf_counter() - t0) / STEPS
                T = run_length(d, n)
                per_run = t_build + t_pairs + T * t_step + (300 * t_sample if fresh else 0)
                total += 3 * per_run
                lines.append(f"d={d} n={n:4d} {kind} {'fresh' if fresh else 'persistent':10s} N={sl['N']:6d} "
                             f"edges={len(sl['src']):7d} T={T:7d} step {t_step*1e6:8.1f} us  one run {per_run:7.1f} s  "
                             f"(build {t_build:.2f} s, pairs {t_pairs:.2f} s, redraws {sl['redraws']})")
                print(lines[-1], flush=True)
lines.append(f"projected total for 144 runs (3 seeds each): {total/60:.1f} min")
print(lines[-1])

t0 = time.perf_counter()
r = simulate(random_slice(3, 8, 0), 0, True)
lines.append(f"smoke test (harness only, not results): d=3 n=8 R fresh, T={r['T']}, finished in "
             f"{time.perf_counter()-t0:.1f} s, keys {sorted(r.keys())}")
t0 = time.perf_counter()
r = simulate(grid_slice(1, 64), 0, False)
lines.append(f"smoke test (harness only, not results): d=1 n=64 G persistent, T={r['T']}, finished in "
             f"{time.perf_counter()-t0:.1f} s, keys {sorted(r.keys())}")
print("\n".join(lines[-2:]))
with open("c2b_timing.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
