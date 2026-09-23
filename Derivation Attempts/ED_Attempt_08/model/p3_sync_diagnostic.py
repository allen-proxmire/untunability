"""Why the port refuses fewer moves on sync than attempt 7 does (diagnostic, not pre-registered).

Tier 3 found every bulk quantity agreeing except the sync refusal count, which is about 19 per cent
lower in the port, with budget and ceiling refusals - so the number of candidates reaching the sync
gate - matching. The gate itself is exact (tier 1) and the tick-field update is exact to 2e-16, so
what is left is the tick field's spread. This runs both codes from the same start and compares,
per tick, the spread of phi across links: the max, the 99th percentile and the count above the
threshold. Attempt 7's modules are imported, never edited.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_07", "model"))

from p3 import Slice3P                                     # noqa: E402
from p3_core import SIGMA, K, FLAT_LINKS_PER_EVENT, CEILING  # noqa: E402
import c3c                                                 # noqa: E402
import c3f                                                 # noqa: E402

N = 12
T = 40
SYNC_FACTOR = 1.5


def strain_stats_ref(M, phi):
    d = np.array([abs(phi[a] - phi[b]) / (SIGMA / K) for (a, b) in M.val])
    return d


def strain_stats_port(M):
    ed = M.edges()
    ph = M.S.phi
    return np.abs(ph[ed[:, 0]] - ph[ed[:, 1]]) / (SIGMA / K)


def run_ref(s_max, seed):
    M = c3c.Slice3(N)
    rng = np.random.default_rng(seed)
    V0 = len(M.vt)
    b = {v: 1.0 for v in M.vt}
    omega = {v: 1.0 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
    phi = {v: 0.0 for v in M.vt}
    pool = round(FLAT_LINKS_PER_EVENT * V0) - len(M.val)
    rows = []
    for t in range(1, T + 1):
        r, pool = c3f.tick(M, b, omega, phi, rng, 1.0, 1.0, pool, s_max=s_max, cap=CEILING)
        d = strain_stats_ref(M, phi)
        rows.append((r["refused_sync"], d.max(), np.percentile(d, 99), int((d > s_max).sum()), len(M.vt)))
    return np.array(rows, dtype=float)


def run_port(s_max, seed):
    M = Slice3P(N)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    pool = round(FLAT_LINKS_PER_EVENT * V0) - M.E
    rows = []
    for t in range(1, T + 1):
        r, pool, kids, absd = M.tick(1.0, 1.0, pool, s_max=s_max, cap=CEILING)
        d = strain_stats_port(M)
        rows.append((r["refused_sync"], d.max(), np.percentile(d, 99), int((d > s_max).sum()), M.V))
    return np.array(rows, dtype=float)


def main():
    from c3b import sync_steady_state
    cal = c3c.Slice3(N)
    A, ids, pos, ei, ej = cal.adjacency()
    s_max = SYNC_FACTOR * float(sync_steady_state(A, 0)["max_link_diff"])
    print("threshold %.4f, n=%d, %d ticks" % (s_max, N, T), flush=True)
    out = []
    for seed in (0, 1, 2):
        a = run_ref(s_max, seed)
        p = run_port(s_max, seed)
        out.append((seed, a, p))
        print("seed %d  refusals/tick  ref %8.1f  port %8.1f | max strain ref %7.3f port %7.3f | "
              "p99 ref %7.4f port %7.4f | links over threshold ref %6.1f port %6.1f | V ref %d port %d"
              % (seed, a[:, 0].mean(), p[:, 0].mean(), a[:, 1].mean(), p[:, 1].mean(),
                 a[:, 2].mean(), p[:, 2].mean(), a[:, 3].mean(), p[:, 3].mean(),
                 int(a[-1, 4]), int(p[-1, 4])), flush=True)
    A_ = np.concatenate([a for _, a, _ in out])
    P_ = np.concatenate([p for _, _, p in out])
    txt = ("pooled over 3 seeds: refusals/tick ref %.1f port %.1f (ratio %.3f); "
           "max strain ref %.3f port %.3f; links over threshold ref %.1f port %.1f"
           % (A_[:, 0].mean(), P_[:, 0].mean(), P_[:, 0].mean() / max(A_[:, 0].mean(), 1e-9),
              A_[:, 1].mean(), P_[:, 1].mean(), A_[:, 3].mean(), P_[:, 3].mean()))
    print(txt)
    with open("p3_sync_diagnostic.txt", "w", encoding="utf-8") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
