"""Run the full M2 plan on 8 worker processes (note 13; D16; IMPLEMENTATION_NOTES.md, M2 runs section).

Usage: python run_m2_plan.py LARGEST   (LARGEST from the halving rule, e.g. 16000)
Resumable: jobs with a saved JSON in m2_runs/ are skipped.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
import time
import itertools
from multiprocessing import Pool
import numpy as np
from run_m2 import run_job, job_name


def jobs(largest):
    out, seen = [], set()

    def add(j):
        name = job_name(j)
        if name not in seen:
            seen.add(name)
            out.append(j)

    inf = float("-inf")
    for kind, kap in (("constrained", -0.1), ("control", inf)):
        for N in (largest, 4000, 1000):
            for s in range(5):
                add(dict(kind=kind, K=10, c=1.0, k_max=12, kappa_min=kap, N=N, seed=s, leak=(N == 1000)))
    for K, c, k, kap in itertools.product((1, 3, 10, 30), (0.5, 1.0, 2.0), (8, 12, 16), (-0.2, -0.1, 0.0)):
        for s in range(3):
            add(dict(kind="constrained", K=K, c=c, k_max=k, kappa_min=kap, N=4000, seed=s, leak=False))
    for K, c, k in itertools.product((1, 3, 10, 30), (0.5, 1.0, 2.0), (8, 12, 16)):
        for s in range(3):
            add(dict(kind="control", K=K, c=c, k_max=k, kappa_min=inf, N=4000, seed=s, leak=False))
    return out


def main():
    largest = int(sys.argv[1])
    J = jobs(largest)
    os.makedirs("m2_runs", exist_ok=True)
    with open("m2_plan_progress.log", "a", encoding="utf-8") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} start: {len(J)} jobs, largest {largest}\n")
        log.flush()
        t0 = time.time()
        with Pool(8) as pool:
            for i, path in enumerate(pool.imap_unordered(run_job, J, chunksize=1), 1):
                log.write(f"{time.strftime('%H:%M:%S')} done {i}/{len(J)} ({(time.time()-t0)/3600:.2f} h): {os.path.basename(path)}\n")
                log.flush()
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} all {len(J)} jobs finished\n")


if __name__ == "__main__":
    main()
