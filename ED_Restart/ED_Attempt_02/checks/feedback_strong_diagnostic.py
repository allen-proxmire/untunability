"""Diagnostic (not pre-registered; follows C70): the strengthened lane-imbalance feedback (kappa 4 and 8) locks the draw rates fully one
way (s = +-1 at the end) but the walker never settles. Does it carry a net flow on average, in the direction of the rate asymmetry,
and does the lossy step have the winding?

Same rule as feedback_candidates_check.py (K2). For kappa 4 and 8 and all 7 starts: 4,000 steps, then 2,000 watched. Reports the
mean and standard deviation of v over the watched steps, the fraction of watched steps on which every committed locus has the same
sign of s, the mean s, and the winding of the lossy step at the final rates.
"""
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
import robustness_check as rc  # noqa: E402
from feedback_candidates_check import D, GAM, L  # noqa: E402
from rule_v4 import kraus, lane_channels  # noqa: E402

STEPS, WATCH = 4000, 2000


def run(job):
    kappa, k = job
    W, Cf = fp.walk_matrix(L, rc.C), fp.coin_full(L, rc.C)
    lane, dest = lane_channels(L, D)
    x = np.arange(0, L, D)
    rho = rc.start(L, k)
    vs, same, smeans = [], 0, []
    for t in range(STEPS + WATCH):
        w = W @ rho @ W.conj().T
        d = np.real(np.diag(w))
        nR, nL = d[3 * x + fp.RI], d[3 * x + fp.LE]
        s = np.clip(kappa * (nR - nL) / np.maximum(nR + nL, 1e-300), -1.0, 1.0)
        rho = kraus(w, lane, dest, np.concatenate([GAM * (1 - s), GAM * (1 + s)]))
        if t >= STEPS:
            vs.append(fp.displacement(rho, Cf, L))
            same += int(np.all(s > 0) or np.all(s < 0))
            smeans.append(float(np.mean(s)))
    vs = np.array(vs)
    wind = rc.winding(W, dict(rc.BASE, g=1.0), s)
    return job, (vs.mean(), vs.std(), same / WATCH, float(np.mean(smeans)), wind)


def main():
    jobs = [(kap, k) for kap in (4.0, 8.0) for k in range(rc.NSTART)]
    with Pool(7) as pool:
        res = dict(pool.map(run, jobs))
    for kap, k in jobs:
        m, sd, frac, sm, wind = res[(kap, k)]
        print("kappa %.0f %-13s: mean v %+.4e, sd %.3e; all loci same rate sign on %.0f%% of watched steps; mean s %+.3f; winding at final rates %d"
              % (kap, rc.START_NAMES[k], m, sd, 100 * frac, sm, wind), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
