"""Ollivier curvature of a slice's edges (H1, note 2; D3): the direct reading of 'curvature bounded below'.

For an edge x~y, put the lazy walk's one-step measure on each end, m_x = 1/2 at x and 1/(2 deg x) on
each neighbour, and ask how far apart those two small clouds are in the earth-mover sense (W1, with
graph distance as the ground cost). The curvature is kappa = 1 - W1. Neighbours whose walks draw
together have positive curvature; neighbours whose walks spread apart, as on a tree, have negative.

Every support point is within three hops of every other (u - x - y - v), so the ground distance is
0 if equal, 1 if adjacent, 2 if they share a neighbour, and 3 otherwise - exact, with no search.
Each W1 is a small linear programme, solved exactly.
"""
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

N_EDGES = 400


def _nbrs(A):
    A = A.tocsr()
    return [set(A.indices[A.indptr[i]:A.indptr[i + 1]].tolist()) for i in range(A.shape[0])]


def edge_curvature(nb, x, y):
    sx = [x] + sorted(nb[x])
    sy = [y] + sorted(nb[y])
    mx = np.array([0.5] + [0.5 / len(nb[x])] * len(nb[x]))
    my = np.array([0.5] + [0.5 / len(nb[y])] * len(nb[y]))
    D = np.empty((len(sx), len(sy)))
    for i, u in enumerate(sx):
        for j, v in enumerate(sy):
            if u == v:
                D[i, j] = 0
            elif v in nb[u]:
                D[i, j] = 1
            elif nb[u] & nb[v]:
                D[i, j] = 2
            else:
                D[i, j] = 3
    a, b = len(sx), len(sy)
    Aeq = np.zeros((a + b, a * b))
    for i in range(a):
        Aeq[i, i * b:(i + 1) * b] = 1
    for j in range(b):
        Aeq[a + j, j::b] = 1
    res = linprog(D.ravel(), A_eq=Aeq, b_eq=np.concatenate([mx, my]), bounds=(0, None), method="highs")
    return 1.0 - float(res.fun)


def curvature_sample(A, seed, n_edges=N_EDGES, min_degree=1):
    """Curvature on a random sample of edges. Returns the distribution's summary."""
    nb = _nbrs(A)
    rows, cols = sp.triu(A, 1).nonzero()
    keep = [(int(u), int(v)) for u, v in zip(rows, cols) if len(nb[u]) >= min_degree and len(nb[v]) >= min_degree]
    rng = np.random.default_rng(7000 + seed)
    pick = rng.choice(len(keep), size=min(n_edges, len(keep)), replace=False)
    k = np.array([edge_curvature(nb, *keep[i]) for i in pick])
    return dict(n=int(len(k)), mean=float(k.mean()), median=float(np.median(k)),
                p05=float(np.percentile(k, 5)), p25=float(np.percentile(k, 25)),
                min=float(k.min()), max=float(k.max()), frac_negative=float((k < -1e-9).mean()))


# ---------------------------------------------------------------- calibration objects
def regular_tree(branch=3, depth=9):
    """A tree whose interior nodes all have degree branch+1 (the root has branch)."""
    edges, frontier, nxt = [], [0], 1
    for _ in range(depth):
        new = []
        for p in frontier:
            for _ in range(branch):
                edges.append((p, nxt))
                new.append(nxt)
                nxt += 1
        frontier = new
    e = np.array(edges)
    N = nxt
    A = sp.csr_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(N, N))
    return (A + A.T).tocsr()


def hypercube(d=8):
    N = 2 ** d
    a, b = [], []
    for i in range(N):
        for k in range(d):
            j = i ^ (1 << k)
            if j > i:
                a.append(i)
                b.append(j)
    A = sp.csr_matrix((np.ones(len(a)), (a, b)), shape=(N, N))
    return (A + A.T).tocsr()
