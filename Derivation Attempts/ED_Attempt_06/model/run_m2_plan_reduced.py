"""Reduced M2 plan (Allen D17), after the full plan was stopped for cost (C75).

Kept:
  * constrained scan at floor -0.2 only: 36 settings (K/sigma, c, k_max) x seeds 0-2 at 4,000;
  * control scan: the same 36 settings x seeds 0-2 at 4,000;
  * central setting (K/sigma 10, c 1, k_max 12) at 1,000 and 4,000, seeds 0-4,
    constrained (floor -0.1) and control.
Dropped:
  * every 16,000-locus job;
  * the constrained scan at floors -0.1 and 0 (216 jobs), recorded as rings on
    C73's arithmetic and the three measured runs in C75.
Jobs already saved in m2_runs/ are skipped, so the three finished runs count.

Usage: python run_m2_plan_reduced.py
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import time
import itertools
from multiprocessing import Pool
from run_m2 import run_job, job_name

INF = float("-inf")


def jobs():
    out, seen = [], set()

    def add(j):
        name = job_name(j)
        if name not in seen:
            seen.add(name)
            out.append(j)

    for kind, kap in (("constrained", -0.1), ("control", INF)):
        for N in (4000, 1000):
            for s in range(5):
                add(dict(kind=kind, K=10, c=1.0, k_max=12, kappa_min=kap, N=N, seed=s, leak=(N == 1000)))
    for K, c, k in itertools.product((1, 3, 10, 30), (0.5, 1.0, 2.0), (8, 12, 16)):
        for s in range(3):
            add(dict(kind="constrained", K=K, c=c, k_max=k, kappa_min=-0.2, N=4000, seed=s, leak=False))
            add(dict(kind="control", K=K, c=c, k_max=k, kappa_min=INF, N=4000, seed=s, leak=False))
    return out


def main():
    J = jobs()
    os.makedirs("m2_runs", exist_ok=True)
    todo = [j for j in J if not os.path.exists(os.path.join("m2_runs", job_name(j) + ".json"))]
    with open("m2_plan_progress.log", "a", encoding="utf-8") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} reduced plan start: {len(J)} jobs, {len(todo)} to run\n")
        log.flush()
        t0 = time.time()
        with Pool(8) as pool:
            for i, path in enumerate(pool.imap_unordered(run_job, todo, chunksize=1), 1):
                log.write(f"{time.strftime('%H:%M:%S')} reduced done {i}/{len(todo)} ({(time.time()-t0)/3600:.2f} h): {os.path.basename(path)}\n")
                log.flush()
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} reduced plan: all {len(J)} jobs present\n")


if __name__ == "__main__":
    main()
