"""C3b static check (note 16, C61; D22, D23; IMPLEMENTATION_NOTES.md, C3b section).

Stand-in 3D slices and the three signals: sync (largest single-link tick difference in the exact
linear steady state of C2b's update), commitment (mean degree), curvature proxy (readings v2's
exponential-growth / small-world flag).
"""
import math
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import spsolve, cg
from scipy.spatial import cKDTree
from readings import bfs_distances, N_CENTRES
from readings_v2 import mass_and_cut

KINDS = ("F", "FR", "B", "H", "Cr")
SIZES = {"F": (1000, 8000, 27000), "FR": (1000, 8000, 27000), "B": (1024, 8192, 27648),
         "H": (1000, 8000, 27000), "Cr": (1000, 8000, 27000)}


def from_edges(N, ei, ej):
    ei, ej = np.asarray(ei), np.asarray(ej)
    A = sp.csr_matrix((np.ones(2 * len(ei)), (np.concatenate([ei, ej]), np.concatenate([ej, ei]))), shape=(N, N))
    A.data[:] = 1.0
    A.setdiag(0)
    A.eliminate_zeros()
    return A


def connected(A):
    return connected_components(A, directed=False)[0] == 1


def grid3(n, periodic=True):
    idx = np.arange(n ** 3).reshape(n, n, n)
    ei, ej = [], []
    for ax in range(3):
        if periodic:
            ei.append(idx.ravel()); ej.append(np.roll(idx, -1, axis=ax).ravel())
        else:
            sl_a = [slice(None)] * 3; sl_b = [slice(None)] * 3
            sl_a[ax] = slice(0, n - 1); sl_b[ax] = slice(1, n)
            ei.append(idx[tuple(sl_a)].ravel()); ej.append(idx[tuple(sl_b)].ravel())
    return np.concatenate(ei), np.concatenate(ej)


def make_F(N, seed):
    n = round(N ** (1 / 3))
    ei, ej = grid3(n)
    return from_edges(n ** 3, ei, ej), dict(redraws=0)


def make_FR(N, seed):
    r = (14.0 / ((N - 1) * 4.0 / 3.0 * math.pi)) ** (1 / 3)
    for redraw in range(1000):
        rng = np.random.default_rng(1000 * (seed + 1) + redraw)
        pts = rng.random((N, 3))
        pairs = cKDTree(pts, boxsize=1.0).query_pairs(r, output_type="ndarray")
        A = from_edges(N, pairs[:, 0], pairs[:, 1])
        if connected(A):
            return A, dict(redraws=redraw)
    raise RuntimeError("FR: no connected draw")


def prufer_tree(B, rng):
    if B == 2:
        return [(0, 1)]
    seq = rng.integers(0, B, size=B - 2)
    degree = np.ones(B, dtype=int)
    for x in seq:
        degree[x] += 1
    import heapq
    leaves = [i for i in range(B) if degree[i] == 1]
    heapq.heapify(leaves)
    edges = []
    for x in seq:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, int(x)))
        degree[x] -= 1
        if degree[x] == 1:
            heapq.heappush(leaves, int(x))
    u, v = heapq.heappop(leaves), heapq.heappop(leaves)
    edges.append((u, v))
    return edges


def make_B(N, seed, b=4):
    nb = b ** 3
    Bn = N // nb
    rng = np.random.default_rng(1000 * (seed + 1))
    bi, bj = grid3(b, periodic=False)
    ei = [bi + k * nb for k in range(Bn)]
    ej = [bj + k * nb for k in range(Bn)]
    tree = prufer_tree(Bn, rng)
    necks = []
    for (p, q) in tree:
        x = p * nb + int(rng.integers(nb))
        y = q * nb + int(rng.integers(nb))
        necks.append((x, y))
    necks = np.array(necks)
    A = from_edges(Bn * nb, np.concatenate(ei + [necks[:, 0]]), np.concatenate(ej + [necks[:, 1]]))
    return A, dict(redraws=0, necks=necks, tree_edges=len(tree), blocks=Bn)


def make_H(N, seed, d=6):
    """Configuration model with double-edge-swap repair of self-loops and repeated links."""
    for redraw in range(100):
        rng = np.random.default_rng(1000 * (seed + 1) + redraw)
        stubs = np.repeat(np.arange(N), d)
        rng.shuffle(stubs)
        E = stubs.reshape(-1, 2).copy()
        for _ in range(200):
            key = np.minimum(E[:, 0], E[:, 1]) * N + np.maximum(E[:, 0], E[:, 1])
            _, first = np.unique(key, return_index=True)
            bad = np.ones(len(E), bool)
            bad[first] = False
            bad |= E[:, 0] == E[:, 1]
            bad_idx = np.where(bad)[0]
            if len(bad_idx) == 0:
                break
            for i in bad_idx:
                j = int(rng.integers(len(E)))
                a, b = E[i]
                c, e = E[j]
                E[i] = (a, c)
                E[j] = (b, e)
        key = np.minimum(E[:, 0], E[:, 1]) * N + np.maximum(E[:, 0], E[:, 1])
        if len(np.unique(key)) != len(E) or np.any(E[:, 0] == E[:, 1]):
            continue
        A = from_edges(N, E[:, 0], E[:, 1])
        if connected(A):
            return A, dict(redraws=redraw)
    raise RuntimeError("H: no simple connected draw")


def make_Cr(N, seed):
    m = round(N * math.sqrt(N) / 2)
    for redraw in range(100):
        rng = np.random.default_rng(1000 * (seed + 1) + redraw)
        keys = set()
        while len(keys) < m:
            k = m - len(keys)
            a = rng.integers(0, N, size=int(1.2 * k) + 10)
            b = rng.integers(0, N, size=int(1.2 * k) + 10)
            ok = a != b
            kk = np.minimum(a[ok], b[ok]).astype(np.int64) * N + np.maximum(a[ok], b[ok])
            for x in kk.tolist():
                if len(keys) >= m:
                    break
                keys.add(x)
        kk = np.fromiter(keys, dtype=np.int64)
        A = from_edges(N, kk // N, kk % N)
        if connected(A):
            return A, dict(redraws=redraw)
    raise RuntimeError("Cr: no connected draw")


MAKERS = {"F": make_F, "FR": make_FR, "B": make_B, "H": make_H, "Cr": make_Cr}


def sync_steady_state(A, seed, K=1.0):
    """Exact linear steady state of C2b's update: K (D - A) phi = deg * (omega - Omega)."""
    N = A.shape[0]
    deg = np.asarray(A.sum(axis=1)).ravel()
    omega = np.random.default_rng(100 + seed).standard_normal(N)
    Omega = float(np.sum(deg * omega) / np.sum(deg))
    rhs = deg * (omega - Omega)
    L = (sp.diags(deg) - A).tocsr() * K
    Lr = L[1:, 1:].tocsc()
    if deg.mean() > 7 or np.allclose(deg, 6):  # well-conditioned expanders and dense graphs
        x, info = cg(Lr, rhs[1:], rtol=1e-12, maxiter=20000)
        method = f"cg(info={info})"
    else:
        x = spsolve(Lr, rhs[1:])
        method = "spsolve"
    phi = np.concatenate([[0.0], x])
    resid = float(np.linalg.norm(L @ phi - rhs) / np.linalg.norm(rhs))
    phi -= phi.mean()
    rows, cols = A.nonzero()
    up = rows < cols
    diffs = np.abs(phi[rows[up]] - phi[cols[up]])
    k = int(np.argmax(diffs))
    return dict(W=float(np.sqrt(np.mean(phi ** 2))), max_link_diff=float(diffs[k]),
                argmax_edge=(int(rows[up][k]), int(cols[up][k])), residual=resid, method=method)


def readings(A, seed):
    """Ball-growth part of readings v2 only (mass dimension and the exponential-growth flag).
    The walk part (spectral dimension) is not used by E1-E4 and is very slow on tree-like graphs (D23 timing)."""
    rng = np.random.default_rng(3000 + seed)
    N = A.shape[0]
    centres = rng.choice(N, size=min(N_CENTRES, N), replace=False)
    r = mass_and_cut(A, bfs_distances(A, centres))
    out = {k: (float(r[k]) if r.get(k) is not None else None) for k in ("d_H", "r2_power", "r2_exp", "r_max", "r_lo")}
    out["small_world"] = bool(r["small_world"])
    return out


def degree_stats(A):
    deg = np.asarray(A.sum(axis=1)).ravel()
    return dict(mean_degree=float(deg.mean()), max_degree=int(deg.max()), min_degree=int(deg.min()))
