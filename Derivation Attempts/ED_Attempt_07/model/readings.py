"""Readings R1-R8 for the constrained growth model (note 11, C58).

Procedures follow M1_Model_Spec.md; implementation choices not fixed there are
recorded in IMPLEMENTATION_NOTES.md before any run.

A pattern is given as a scipy.sparse CSR adjacency matrix A (symmetric, 0/1,
no self-loops), connected.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import breadth_first_order, shortest_path

N_CENTRES = 200
T_START = 10
T_CAP = 20000
N_FIT_POINTS = 30


def _fit_slope(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    A = np.vstack([x, np.ones_like(x)]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ coef
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2)) or 1e-300
    return float(coef[0]), 1.0 - ss_res / ss_tot


def bfs_distances(A, centres):
    """Hop distances from each centre to every locus (rows = centres)."""
    return shortest_path(A, method="D", unweighted=True, indices=centres).astype(np.int64)


def mass_and_cut(A, dist):
    """R1 mass dimension with small-world flag, R2 ball-cut exponent, R6 CV.

    dist: (n_centres, N) hop distances.
    """
    N = A.shape[0]
    rows, cols = A.nonzero()
    upper = rows < cols
    ei, ej = rows[upper], cols[upper]
    rmax_all = int(dist.max())
    radii = np.arange(0, rmax_all + 1)
    V = np.zeros((dist.shape[0], len(radii)))
    Cc = np.zeros((dist.shape[0], len(radii)))
    for c in range(dist.shape[0]):
        d = dist[c]
        counts = np.bincount(d, minlength=len(radii))
        V[c] = np.cumsum(counts)
        # a relation crosses the edge of the ball of radius r when one end is at
        # distance <= r and the other at distance > r; for a graph, that is
        # exactly |d_i - d_j| = 1 with min(d_i, d_j) = r
        di, dj = d[ei], d[ej]
        lo = np.minimum(di, dj)
        crossing = np.abs(di - dj) == 1
        Cc[c] = np.bincount(lo[crossing], minlength=len(radii))[: len(radii)]
    Vm = V.mean(axis=0)
    Cm = Cc.mean(axis=0)
    ok_r = np.where(Vm <= N / 10)[0]
    r_max = int(ok_r.max()) if len(ok_r) else 0
    out = {"r_max": r_max}
    if r_max >= 3:
        rr = radii[2 : r_max + 1]
        logV = np.log(Vm[2 : r_max + 1])
        dH, r2_pow = _fit_slope(np.log(rr), logV)
        _, r2_exp = _fit_slope(rr, logV)
        beta, _ = _fit_slope(logV, np.log(np.maximum(Cm[2 : r_max + 1], 1e-300)))
        out.update(d_H=dH, r2_power=r2_pow, r2_exp=r2_exp, beta=beta)
        out["small_world"] = bool(r_max < 5 or r2_exp > r2_pow)
        mid = int(round((2 + r_max) / 2))
        out["cv_mid"] = float(V[:, mid].std() / V[:, mid].mean())
    else:
        out.update(d_H=np.nan, r2_power=np.nan, r2_exp=np.nan, beta=np.nan, small_world=True, cv_mid=np.nan)
    return out


def walk_readings(A, centres, dist):
    """R3 spectral dimension, R4 walk dimension, R5 consistency input.

    Lazy random walk: half the mass stays, half spreads evenly over neighbours.
    Exact distributions by sparse matrix powers from all centres at once.
    """
    N = A.shape[0]
    deg = np.asarray(A.sum(axis=1)).ravel()
    Dinv = sp.diags(1.0 / deg)
    P = 0.5 * sp.identity(N, format="csr") + 0.5 * (A @ Dinv)  # column-stochastic
    P = P.tocsr()
    nC = len(centres)
    X = np.zeros((N, nC))
    X[centres, np.arange(nC)] = 1.0
    d2 = (dist.astype(float) ** 2).T  # (N, nC)
    ret, msd = [], []
    t_end = None
    for t in range(1, T_CAP + 1):
        X = P @ X
        p = float(np.mean(X[centres, np.arange(nC)]))
        ret.append(p)
        msd.append(float(np.mean(np.sum(X * d2, axis=0))))
        if t >= T_START and p <= 10.0 / N:
            t_end = t
            break
    capped = t_end is None
    if capped:
        t_end = T_CAP
    out = {"t_end": t_end, "t_capped": capped}
    if t_end >= T_START + 5:
        ts = np.unique(np.round(np.geomspace(T_START, t_end, N_FIT_POINTS)).astype(int))
        ret = np.array(ret)
        msd = np.array(msd)
        s_ret, _ = _fit_slope(np.log(ts), np.log(ret[ts - 1]))
        s_msd, _ = _fit_slope(np.log(ts), np.log(msd[ts - 1]))
        out["d_s"] = -2.0 * s_ret
        out["d_w"] = 2.0 / s_msd if s_msd > 0 else np.inf
    else:
        out["d_s"] = np.nan
        out["d_w"] = np.nan
    return out


def all_readings(A, rng):
    N = A.shape[0]
    centres = rng.choice(N, size=min(N_CENTRES, N), replace=False)
    dist = bfs_distances(A, centres)
    r = mass_and_cut(A, dist)
    r.update(walk_readings(A, centres, dist))
    if np.isfinite(r.get("d_H", np.nan)) and np.isfinite(r.get("d_w", np.nan)) and r["d_w"] > 0:
        r["R5"] = abs(r["d_s"] - 2 * r["d_H"] / r["d_w"])
    else:
        r["R5"] = np.nan
    E = A.nnz // 2
    dbar = 2 * E / N
    r["N"], r["E"], r["mean_degree"] = N, E, dbar
    r["stuck_share"] = 1 - 2 / dbar + 1 / (2 * E)
    return r
