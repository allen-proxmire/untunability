"""Strong-sync M2 plan (Allen D20), after the reduced plan was stopped for cost (C81).

Runs only K/sigma = 30: constrained at floor -0.2 and the control, for the 9
(c, k_max) settings x seeds 0-2 at 4,000 loci (54 jobs). Readings, checkpoints,
rules and per-run criteria are unchanged (run_m2.run_job). Saved jobs are skipped.

Usage: python run_m2_plan_k30.py
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import time
import itertools
from multiprocessing import Pool
from run_m2 import run_job, job_name

INF = float("-inf")


def jobs():
    out = []
    # most expensive first, so long jobs start early
    for k, c in itertools.product((16, 12, 8), (0.5, 1.0, 2.0)):
        for s in range(3):
            out.append(dict(kind="constrained", K=30, c=c, k_max=k, kappa_min=-0.2, N=4000, seed=s, leak=False))
            out.append(dict(kind="control", K=30, c=c, k_max=k, kappa_min=INF, N=4000, seed=s, leak=False))
    return out


def main():
    J = jobs()
    os.makedirs("m2_runs", exist_ok=True)
    todo = [j for j in J if not os.path.exists(os.path.join("m2_runs", job_name(j) + ".json"))]
    with open("m2_plan_progress.log", "a", encoding="utf-8") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} strong-sync plan start: {len(J)} jobs, {len(todo)} to run\n")
        log.flush()
        t0 = time.time()
        with Pool(8) as pool:
            for i, path in enumerate(pool.imap_unordered(run_job, todo, chunksize=1), 1):
                log.write(f"{time.strftime('%H:%M:%S')} strong-sync done {i}/{len(todo)} ({(time.time()-t0)/3600:.2f} h): {os.path.basename(path)}\n")
                log.flush()
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} strong-sync plan: all {len(J)} jobs present\n")


if __name__ == "__main__":
    main()
