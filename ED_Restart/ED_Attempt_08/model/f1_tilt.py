"""The tilt reading (road F, note 10; D13, D14): does a slice support a common "now"?

Synced Now (A7 C2b) measured the structure function G(r) = mean of (phi_a - phi_b)^2 over pairs at
hop distance exactly r, on a doubling ladder r = 1, 2, 4, 8..., from about 20 sources with at least
100 pairs a rung. The wobble at scale r is sqrt(G(r)) and the TILT is sqrt(G(r))/r.

    tilt shrinks with r  ->  a common now survives at large scales
    tilt holds or grows  ->  it does not

Synced Now's prediction, from the same scaling: the tilt exponent is (2 - d)/2, so +0.5 in one
dimension, 0 in two and -0.5 in three.

The tick field is the steady state of C2b's update, K (D - A) phi = deg * (omega - Omega), which is
what `c3b.sync_steady_state` already solves - but that function returns only summaries, not the
field, so `steady_phi` below repeats the solve and is **verified against it** (W and the largest
link difference must agree to machine precision) rather than trusted.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from scipy.sparse.linalg import cg, spsolve

# A7 C2b used 20 sources for RANDOM slices and a different branch for grids, which took every
# vertex and axis-rolled it. Porting only the random-slice branch left too few pairs in low
# dimensions: a ring gives 2 vertices at each distance from a source, so 20 sources give 40 pairs
# and the ladder is empty at r = 1. The calibration caught this before any grown slice was touched.
N_SOURCES = 200
MIN_PAIRS = 100
DROP_TOP = 2            # rungs nearest the system's own size saturate and are not fitted


def steady_phi(A, seed, K=1.0):
    """The steady tick field. Same solve as c3b.sync_steady_state; verified against it by `check`."""
    N = A.shape[0]
    deg = np.asarray(A.sum(axis=1)).ravel()
    omega = np.random.default_rng(100 + seed).standard_normal(N)
    Omega = float(np.sum(deg * omega) / np.sum(deg))
    rhs = deg * (omega - Omega)
    L = (sp.diags(deg) - A).tocsr() * K
    Lr = L[1:, 1:].tocsc()
    if deg.mean() > 7 or np.allclose(deg, 6):
        x, info = cg(Lr, rhs[1:], rtol=1e-12, maxiter=20000)
    else:
        x = spsolve(Lr, rhs[1:])
    phi = np.concatenate([[0.0], x])
    phi -= phi.mean()
    return phi


def check_against_c3b(A, seed):
    """The solve here must reproduce c3b's summaries exactly."""
    from c3b import sync_steady_state
    ref = sync_steady_state(A, seed)
    phi = steady_phi(A, seed)
    rows, cols = A.nonzero()
    up = rows < cols
    diffs = np.abs(phi[rows[up]] - phi[cols[up]])
    return dict(dW=abs(float(np.sqrt(np.mean(phi ** 2))) - ref["W"]),
                dmax=abs(float(diffs.max()) - ref["max_link_diff"]))


def tilt_curve(A, seed, n_sources=N_SOURCES, min_pairs=MIN_PAIRS):
    """A7 C2b's pair construction, applied to a slice's steady tick field."""
    N = A.shape[0]
    phi = steady_phi(A, seed)
    rng = np.random.default_rng(5000 + seed)
    sources = rng.choice(N, size=min(n_sources, N), replace=False)
    dist = shortest_path(A, directed=False, unweighted=True, indices=sources)
    rs, Ws, tilts, npair = [], [], [], []
    r = 1
    while True:
        rows, cols = np.nonzero(dist == r)
        if len(rows) < min_pairs:
            break
        a, b = sources[rows], cols
        G = float(np.mean((phi[a] - phi[b]) ** 2))
        W = float(np.sqrt(G))
        rs.append(r)
        Ws.append(W)
        tilts.append(W / r)
        npair.append(int(len(rows)))
        r *= 2
    out = dict(r=rs, W=Ws, tilt=tilts, pairs=npair, N=int(N),
               mean_degree=float(np.asarray(A.sum(axis=1)).ravel().mean()))
    # The top rungs saturate: on a ring the tilt is flat out to r = 128 and then falls off a cliff
    # as r approaches half the ring. Fitting through that turns a flat curve into a sloping one.
    # Dropping the top two rungs is the same cut as r <= max/4 on every calibration object.
    k = len(rs) - DROP_TOP
    if k >= 3:
        lr, lt, lw = np.log(rs[:k]), np.log(tilts[:k]), np.log(Ws[:k])
        out["fit_rungs"] = rs[:k]
        out["tilt_exponent"] = float(np.polyfit(lr, lt, 1)[0])
        out["W_exponent"] = float(np.polyfit(lr, lw, 1)[0])
    else:
        out["fit_rungs"] = []
        out["tilt_exponent"] = None
        out["W_exponent"] = None
    return out


# ---------------------------------------------------------------- calibration objects
def ring(N):
    i = np.arange(N)
    return _sym(i, (i + 1) % N, N)


def square_torus(n):
    N = n * n
    i = np.arange(N)
    x, y = i // n, i % n
    a = np.concatenate([i, i])
    b = np.concatenate([((x + 1) % n) * n + y, x * n + (y + 1) % n])
    return _sym(a, b, N)


def cube_torus(n):
    N = n ** 3
    i = np.arange(N)
    x, y, z = i // (n * n), (i // n) % n, i % n
    a = np.concatenate([i, i, i])
    b = np.concatenate([((x + 1) % n) * n * n + y * n + z,
                        x * n * n + ((y + 1) % n) * n + z,
                        x * n * n + y * n + (z + 1) % n])
    return _sym(a, b, N)


def _sym(a, b, N):
    A = sp.csr_matrix((np.ones(len(a)), (a, b)), shape=(N, N))
    A = A + A.T
    A.data[:] = 1.0
    A.setdiag(0)
    A.eliminate_zeros()
    return A
