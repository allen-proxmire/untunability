"""Follow-up diagnostic for calibration run 1 (NOT pre-registered).

Run 1 (calibration_run1.txt): E0 NOT AS EXPECTED for the 3D cubic grid
(d_H = 2.589 < 2.6) and the 2D random geometric graph (d_w = 2.214 > 2.2).
Those verdicts stand; exit rule X0 applies. This script only asks why, by
local slopes, on the same four patterns with the same seeds. It changes no
reading and records no process result.

Reported per pattern:
  * local mass-dimension slopes d ln V / d ln r at each radius up to r_max;
  * local return slopes -2 d ln p / d ln t and local walk slopes
    2 / (d ln <r^2> / d ln t) at log-spaced times across run 1's window;
  * where sqrt(<r^2>) stands relative to r_max, and <r^2> relative to its
    finite-pattern ceiling (the mean squared distance between loci), at the
    window's end.
"""
import numpy as np
import scipy.sparse as sp
from calibrate import rgg, cubic_grid, random_regular
from readings import bfs_distances, T_START, T_CAP


def local_slopes(x, y):
    lx, ly = np.log(x), np.log(y)
    return (ly[1:] - ly[:-1]) / (lx[1:] - lx[:-1])


def diagnose(name, A, rng_read):
    N = A.shape[0]
    centres = rng_read.choice(N, size=200, replace=False)
    dist = bfs_distances(A, centres)
    radii = np.arange(dist.max() + 1)
    V = np.array([np.cumsum(np.bincount(d, minlength=len(radii))) for d in dist]).mean(axis=0)
    r_max = int(np.where(V <= N / 10)[0].max())
    rr = np.arange(2, r_max + 1)
    sl = local_slopes(rr, V[2:r_max + 1])
    print(f"\n== {name}: N={N}, r_max={r_max}")
    print("   local mass slopes r->r+1 (r=2..):", " ".join(f"{s:.2f}" for s in sl))
    ceiling = float(np.mean(dist.astype(float) ** 2))
    deg = np.asarray(A.sum(axis=1)).ravel()
    P = (0.5 * sp.identity(N, format="csr") + 0.5 * (A @ sp.diags(1.0 / deg))).tocsr()
    X = np.zeros((N, 200))
    X[centres, np.arange(200)] = 1.0
    d2 = (dist.astype(float) ** 2).T
    ret, msd = [], []
    t_end = None
    for t in range(1, T_CAP + 1):
        X = P @ X
        p = float(np.mean(X[centres, np.arange(200)]))
        ret.append(p)
        msd.append(float(np.mean(np.sum(X * d2, axis=0))))
        if t >= T_START and p <= 10.0 / N:
            t_end = t
            break
    ret, msd = np.array(ret), np.array(msd)
    ts = np.unique(np.round(np.geomspace(2, t_end, 16)).astype(int))
    ls_ret = -2 * local_slopes(ts, ret[ts - 1])
    ls_msd = 2 / local_slopes(ts, msd[ts - 1])
    print(f"   window end t_end={t_end}; sqrt<r^2> at t_end = {np.sqrt(msd[t_end-1]):.2f} (r_max {r_max}); "
          f"<r^2>/ceiling at t_end = {msd[t_end-1]/ceiling:.3f}")
    print("   times:", " ".join(str(t) for t in ts))
    print("   local d_s:", " ".join(f"{s:.2f}" for s in ls_ret))
    print("   local d_w:", " ".join(f"{s:.2f}" for s in ls_msd))
    print("   sqrt<r^2>:", " ".join(f"{np.sqrt(msd[t-1]):.1f}" for t in ts))


def main():
    rng_build = np.random.default_rng(1)
    rng_read = np.random.default_rng(2)
    A, _ = rgg(16000, 3, 12, rng_build)
    diagnose("3D random geometric (mean 12)", A, rng_read)
    A, _ = cubic_grid(25)
    diagnose("3D cubic grid 25^3", A, rng_read)
    A, _ = rgg(16000, 2, 8, rng_build)
    diagnose("2D random geometric (mean 8)", A, rng_read)
    A, _ = random_regular(16000, 12, rng_build)
    diagnose("random 12-regular", A, rng_read)


if __name__ == "__main__":
    main()
