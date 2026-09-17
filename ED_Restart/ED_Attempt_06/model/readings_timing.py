"""Readings timing (before any M2 process reading; D16; IMPLEMENTATION_NOTES.md, M2 runs section).

Times one checkpoint's readings (readings_v2.all_readings) on stand-in patterns
that bracket what M2 grows: a ring (the constrained central shape, C71) and a
3D random geometric graph with mean degree about 9 (the control's density,
C72), at 4,000 and 16,000 loci. Timing only: the readings' values here are not
results. Then combines with the M2 timing trial estimates (C71, C72) to give the
full plan's time including readings, and applies note 11's halving rule under
Allen's 24-hour budget on 8 cores.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import time
import numpy as np
import scipy.sparse as sp
from calibrate import rgg, to_csr
from readings_v2 import all_readings


def ring(n):
    i = np.arange(n)
    return to_csr(n, np.stack([i, (i + 1) % n], axis=1))


def timed(A):
    t0 = time.perf_counter()
    all_readings(A, np.random.default_rng(0))
    return time.perf_counter() - t0


def main():
    rng = np.random.default_rng(3)
    T = {}
    T[("ring", 4000)] = timed(ring(4000))
    T[("dense", 4000)] = timed(rgg(4000, 3, 9, rng)[0])
    T[("ring", 16000)] = timed(ring(16000))
    T[("dense", 16000)] = timed(rgg(16000, 3, 9, rng)[0])
    T[("ring", 1000)] = timed(ring(1000))
    T[("dense", 1000)] = timed(rgg(1000, 3, 9, rng)[0])
    for k, v in T.items():
        print(f"readings, one checkpoint, {k[0]} {k[1]}: {v:.1f} s")

    # process time per run from the M2 timing trial (C71 constrained ring, C72 control), same scaling as there
    proc = {"ring": (2.6656, 22.2807 - 0.0151, 0.0151, 25.0681 - 2.6656 - 22.2807),
            "dense": (15.4837, 19.1965 - 2.4595, 2.4595, 35.0426 - 15.4837 - 19.1965)}

    def proc_est(kind, N):
        clock, mv, conn, other = proc[kind]
        s = N / 1000.0
        return clock * s ** 2 + mv * s + conn * s ** 2 + other * s

    def run_est(kind, N):
        return proc_est(kind, N) + 5 * T[(kind, N)]

    def plan(largest):
        sizes = [1000, 4000, largest]
        total = 0.0
        for N in sizes:
            total += 5 * run_est("ring", N)    # central constrained (floor -0.1: ring, C73)
            total += 5 * run_est("dense", N)   # central control
        total += 72 * 3 * run_est("ring", 4000)   # scan, floors -0.1 and 0 (ring by C73 arithmetic)
        total += 36 * 3 * run_est("dense", 4000)  # scan, floor -0.2 (taken as dense, the costlier case)
        total += 36 * 3 * run_est("dense", 4000)  # scan control (36 distinct settings)
        return total

    for largest in (16000, 8000, 4000):
        tot = plan(largest)
        print(f"largest size {largest}: {tot/3600:.1f} core-hours = {tot/3600/8:.1f} wall-clock hours on 8 cores")
    chosen = None
    for largest in (16000, 8000, 4000):
        if plan(largest) / 3600 / 8 <= 24:
            chosen = largest
            break
    print(f"24-hour budget: halving rule gives largest size {chosen if chosen else 'none fits'}")


if __name__ == "__main__":
    main()
