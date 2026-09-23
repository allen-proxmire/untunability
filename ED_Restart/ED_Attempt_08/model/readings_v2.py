"""Readings v2 (Allen D14, fix proposed in note 12 / C65), written before calibration run 2.

Change from readings.py (v1), and nothing else:
  * R1 mass dimension, R2 ball-cut exponent and the small-world flag's
    comparison use radii from r_lo = max(2, ceil(r_max/2)) to r_max, needing
    at least 3 radii (otherwise undefined, flag raised). R6 uses the middle of
    that range.
  * R3 spectral and R4 walk dimension use times from the first t with
    sqrt(<r^2>) >= r_lo to the first t with sqrt(<r^2>) >= r_max (same scales as
    the balls), 30 log-spaced points, at least 5 ticks long (otherwise
    undefined); cap t = 20,000 unchanged.
Centres, distances, the lazy walk, R5 and R9 are as in v1.
"""
import math
import numpy as np
import scipy.sparse as sp
from readings import _fit_slope, bfs_distances, N_CENTRES, T_CAP, N_FIT_POINTS


def mass_and_cut(A, dist):
    N = A.shape[0]
    rows, cols = A.nonzero()
    upper = rows < cols
    ei, ej = rows[upper], cols[upper]
    radii = np.arange(0, int(dist.max()) + 1)
    V = np.zeros((dist.shape[0], len(radii)))
    Cc = np.zeros((dist.shape[0], len(radii)))
    for c in range(dist.shape[0]):
        d = dist[c]
        V[c] = np.cumsum(np.bincount(d, minlength=len(radii)))
        di, dj = d[ei], d[ej]
        lo = np.minimum(di, dj)
        crossing = np.abs(di - dj) == 1
        Cc[c] = np.bincount(lo[crossing], minlength=len(radii))[: len(radii)]
    Vm, Cm = V.mean(axis=0), Cc.mean(axis=0)
    ok_r = np.where(Vm <= N / 10)[0]
    r_max = int(ok_r.max()) if len(ok_r) else 0
    r_lo = max(2, math.ceil(r_max / 2))
    out = {"r_max": r_max, "r_lo": r_lo}
    if r_max - r_lo + 1 >= 3:
        rr = radii[r_lo : r_max + 1]
        logV = np.log(Vm[r_lo : r_max + 1])
        dH, r2_pow = _fit_slope(np.log(rr), logV)
        _, r2_exp = _fit_slope(rr, logV)
        beta, _ = _fit_slope(logV, np.log(np.maximum(Cm[r_lo : r_max + 1], 1e-300)))
        mid = int(round((r_lo + r_max) / 2))
        out.update(d_H=dH, r2_power=r2_pow, r2_exp=r2_exp, beta=beta,
                   small_world=bool(r_max < 5 or r2_exp > r2_pow),
                   cv_mid=float(V[:, mid].std() / V[:, mid].mean()))
    else:
        out.update(d_H=np.nan, r2_power=np.nan, r2_exp=np.nan, beta=np.nan, small_world=True, cv_mid=np.nan)
    return out


def walk_readings(A, centres, dist, r_lo, r_max, defined):
    out = {"t_start": None, "t_end": None, "t_capped": False, "d_s": np.nan, "d_w": np.nan}
    if not defined:
        return out
    N = A.shape[0]
    deg = np.asarray(A.sum(axis=1)).ravel()
    P = (0.5 * sp.identity(N, format="csr") + 0.5 * (A @ sp.diags(1.0 / deg))).tocsr()
    nC = len(centres)
    X = np.zeros((N, nC))
    X[centres, np.arange(nC)] = 1.0
    d2 = (dist.astype(float) ** 2).T
    ret, msd = [], []
    t_start = t_end = None
    for t in range(1, T_CAP + 1):
        X = P @ X
        ret.append(float(np.mean(X[centres, np.arange(nC)])))
        m = float(np.mean(np.sum(X * d2, axis=0)))
        msd.append(m)
        if t_start is None and math.sqrt(m) >= r_lo:
            t_start = t
        if math.sqrt(m) >= r_max:
            t_end = t
            break
    if t_end is None:
        t_end = T_CAP
        out["t_capped"] = True
    out["t_start"], out["t_end"] = t_start, t_end
    if t_start is None or t_end - t_start + 1 < 5:
        return out
    ts = np.unique(np.round(np.geomspace(t_start, t_end, N_FIT_POINTS)).astype(int))
    ret, msd = np.array(ret), np.array(msd)
    s_ret, _ = _fit_slope(np.log(ts), np.log(ret[ts - 1]))
    s_msd, _ = _fit_slope(np.log(ts), np.log(msd[ts - 1]))
    out["d_s"] = -2.0 * s_ret
    out["d_w"] = 2.0 / s_msd if s_msd > 0 else np.inf
    return out


def all_readings(A, rng):
    N = A.shape[0]
    centres = rng.choice(N, size=min(N_CENTRES, N), replace=False)
    dist = bfs_distances(A, centres)
    r = mass_and_cut(A, dist)
    r.update(walk_readings(A, centres, dist, r["r_lo"], r["r_max"], np.isfinite(r["d_H"])))
    if np.isfinite(r["d_H"]) and np.isfinite(r["d_w"]) and r["d_w"] > 0 and np.isfinite(r["d_s"]):
        r["R5"] = abs(r["d_s"] - 2 * r["d_H"] / r["d_w"])
    else:
        r["R5"] = np.nan
    E = A.nnz // 2
    dbar = 2 * E / N
    r["N"], r["E"], r["mean_degree"] = N, E, dbar
    r["stuck_share"] = 1 - 2 / dbar + 1 / (2 * E)
    return r
