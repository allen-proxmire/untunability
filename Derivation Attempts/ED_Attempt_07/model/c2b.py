"""C2b model (note 9, C27; D10, D11; IMPLEMENTATION_NOTES.md, C2b section).

Slices given as d-dimensional periodic grids (G) or random slices (R: uniform
points in the unit d-torus, linked within the radius for mean degree 10,
connected). Event x in slice t+1 has past links to x and its slice neighbours
in slice t. Tick counts carried forward:
  phi(x,t+1) = phi(x,t) + omega(x) + (K/deg x) * sum_y tanh(phi(y,t) - phi(x,t)),
stored as psi = phi - t. omega = 1 + sigma*g, persistent or fresh each tick.
"""
import math
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, shortest_path

SIGMA = 0.002
K = 0.5
SIZES = {1: (64, 128, 256, 512), 2: (16, 32, 64, 128), 3: (8, 16, 24, 32)}
MEAN_DEGREE = 10.0


def run_length(d, n):
    return math.ceil(3 * math.log(1000) * 2 * d * n * n / (4 * math.pi ** 2 * K))


def grid_slice(d, n):
    N = n ** d
    idx = np.arange(N).reshape((n,) * d)
    src, dst = [], []
    for ax in range(d):
        for sh in (1, -1):
            src.append(idx.ravel())
            dst.append(np.roll(idx, sh, axis=ax).ravel())
    src, dst = np.concatenate(src), np.concatenate(dst)
    return dict(kind="G", d=d, n=n, N=N, src=src, dst=dst, idx=idx, redraws=0)


def random_slice(d, n, seed, max_redraws=100, scheme="v1"):
    """scheme v1 (runs 1, 2): slice seed 1000 + 10*seed + redraw.
    scheme v2 (run 3, D14): slice seed 1000*(seed + 1) + redraw, redraw < 1000, never overlapping."""
    N = n ** d
    vol = {1: 2.0, 2: math.pi, 3: 4.0 * math.pi / 3.0}[d]
    radius = (MEAN_DEGREE / (vol * (N - 1))) ** (1.0 / d)
    if scheme == "v2":
        max_redraws = min(max_redraws, 1000)
    for redraw in range(max_redraws):
        base = 1000 * (seed + 1) if scheme == "v2" else 1000 + 10 * seed
        rng = np.random.default_rng(base + redraw)
        pts = rng.random((N, d))
        pairs = cKDTree(pts, boxsize=1.0).query_pairs(radius, output_type="ndarray")
        src = np.concatenate([pairs[:, 0], pairs[:, 1]])
        dst = np.concatenate([pairs[:, 1], pairs[:, 0]])
        A = csr_matrix((np.ones(len(src)), (src, dst)), shape=(N, N))
        ncomp, _ = connected_components(A, directed=False)
        if ncomp == 1:
            return dict(kind="R", d=d, n=n, N=N, src=src, dst=dst, A=A, redraws=redraw)
    raise RuntimeError(f"no connected random slice after {max_redraws} draws (d={d}, n={n}, seed={seed})")


def tilt_pairs(sl, seed):
    """Pair lists by hop distance r = 1, 2, 4, ... for the tilt reading (D11)."""
    d, n, N = sl["d"], sl["n"], sl["N"]
    out = {}
    if sl["kind"] == "G":
        idx = sl["idx"]
        r = 1
        while r <= n // 2:
            a = np.concatenate([idx.ravel()] * d)
            b = np.concatenate([np.roll(idx, r, axis=ax).ravel() for ax in range(d)])
            out[r] = (a, b)
            r *= 2
    else:
        rng = np.random.default_rng(5000 + seed)
        sources = rng.choice(N, size=min(20, N), replace=False)
        dist = shortest_path(sl["A"], directed=False, unweighted=True, indices=sources)
        r = 1
        while True:
            rows, cols = np.nonzero(dist == r)
            if len(rows) < 100:
                break
            out[r] = (sources[rows], cols)
            r *= 2
    return out


def simulate(sl, seed, fresh, T=None, steps=None, sigma=SIGMA):
    """Run the tick-count update. steps (timing only) overrides T's step count."""
    d, n, N = sl["d"], sl["n"], sl["N"]
    T = T or run_length(d, n)
    nsteps = steps or T
    src, dst = sl["src"], sl["dst"]
    deg = np.bincount(src, minlength=N).astype(float)
    coef = K / deg
    rng = np.random.default_rng(seed)
    omega = None if fresh else sigma * rng.standard_normal(N)
    psi = np.zeros(N)
    t23, t09 = (2 * T) // 3, (9 * T) // 10
    sample_times = set(np.linspace(T - T // 3, T - 1, 300).astype(int).tolist()) if fresh else set()
    pairs = tilt_pairs(sl, seed) if steps is None else {}
    w2_sum, n_samp = 0.0, 0
    g2_sum = {r: 0.0 for r in pairs}
    psi_23 = psi_09 = None
    for t in range(nsteps):
        if t == t23:
            psi_23 = psi.copy()
        if t == t09:
            psi_09 = psi.copy()
        if t in sample_times:
            c = psi - psi.mean()
            w2_sum += float(np.mean(c * c))
            for r, (a, b) in pairs.items():
                g2_sum[r] += float(np.mean((psi[a] - psi[b]) ** 2))
            n_samp += 1
        pull = np.bincount(src, weights=np.tanh(psi[dst] - psi[src]), minlength=N)
        noise = sigma * rng.standard_normal(N) if fresh else omega
        psi = psi + noise + coef * pull
    if steps is not None:
        return None
    res = dict(kind=sl["kind"], d=d, n=n, N=N, seed=seed, fresh=fresh, T=T, redraws=sl["redraws"], sigma=sigma,
               mean_degree=float(deg.mean()))
    if fresh:
        res["W"] = math.sqrt(w2_sum / n_samp)
        g2 = {r: g2_sum[r] / n_samp for r in pairs}
    else:
        c = psi - psi.mean()
        res["W"] = float(np.sqrt(np.mean(c * c)))
        c23 = psi_23 - psi_23.mean()
        W23 = float(np.sqrt(np.mean(c23 * c23)))
        res["W_change"] = abs(res["W"] - W23) / res["W"]
        res["rate_spread"] = float(np.std((psi - psi_09) / (T - t09)))
        res["max_neighbour_diff"] = float(np.max(np.abs(psi[dst] - psi[src])))
        g2 = {r: float(np.mean((psi[a] - psi[b]) ** 2)) for r, (a, b) in pairs.items()}
    res["tilt_r"] = {int(r): math.sqrt(g2[r]) / r for r in g2}
    return res
