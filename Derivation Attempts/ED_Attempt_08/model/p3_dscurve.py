"""The spectral dimension as a function of scale, rather than one fitted slope (diagnostic).

`readings_v2.walk_readings` fits a single slope of log(return probability) against log(walk time)
over one window and reports that as d_s. In causal dynamical triangulations the spectral dimension
RUNS with scale - about 2 at short distances and about 4 at long ones - so a single slope can
describe a curve that is nowhere near constant. ED's d_s has never been looked at this way.

This reuses the same lazy walk P = (I + A D^-1)/2 and the same centres, and reports the LOCAL slope
in a sliding window, together with the walk's radius sqrt(mean square displacement) at each point,
so d_s can be read against a distance rather than against an abstract time.

It does not change any existing reading. `d_s` from readings_v2 is untouched and still reported.
"""
import numpy as np
import scipy.sparse as sp
from readings import N_CENTRES
from readings import T_CAP

WINDOW = 5          # points per local slope, in log-spaced walk times


def d_s_curve(A, seed, t_cap=None, n_points=24):
    """Returns dict with walk times, radii and the local spectral dimension at each."""
    N = A.shape[0]
    rng = np.random.default_rng(3000 + seed)
    centres = rng.choice(N, size=min(N_CENTRES, N), replace=False)
    deg = np.asarray(A.sum(axis=1)).ravel()
    P = (0.5 * sp.identity(N, format="csr") + 0.5 * (A @ sp.diags(1.0 / deg))).tocsr()
    nC = len(centres)
    X = np.zeros((N, nC))
    X[centres, np.arange(nC)] = 1.0
    cap = int(t_cap or T_CAP)
    ret = np.empty(cap)
    msd = np.empty(cap)
    # squared distance from each centre, for the walk radius
    from readings import bfs_distances
    d2 = (bfs_distances(A, centres).astype(float) ** 2).T
    for t in range(cap):
        X = P @ X
        ret[t] = float(np.mean(X[centres, np.arange(nC)]))
        msd[t] = float(np.mean(np.sum(X * d2, axis=0)))
    ts = np.unique(np.round(np.geomspace(2, cap, n_points)).astype(int))
    lt, lr = np.log(ts), np.log(np.maximum(ret[ts - 1], 1e-300))
    out_t, out_r, out_ds = [], [], []
    h = WINDOW // 2
    for i in range(h, len(ts) - h):
        sl = slice(i - h, i + h + 1)
        s = np.polyfit(lt[sl], lr[sl], 1)[0]
        out_t.append(int(ts[i]))
        out_r.append(float(np.sqrt(msd[ts[i] - 1])))
        out_ds.append(float(-2.0 * s))
    return dict(t=out_t, radius=out_r, d_s=out_ds,
                d_s_min=float(min(out_ds)) if out_ds else None,
                d_s_max=float(max(out_ds)) if out_ds else None,
                d_s_last=float(out_ds[-1]) if out_ds else None,
                ret_final=float(ret[-1]), t_cap=cap, centres=int(nC))
