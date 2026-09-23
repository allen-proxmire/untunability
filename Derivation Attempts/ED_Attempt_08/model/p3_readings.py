"""Readings for the port: the same reading code as attempt 7, fed from the port's arrays.

`readings.py`, `readings_v2.py`, `c3a.py` and `c3b.py` are byte-identical copies of attempt 7's
(hashes in IMPLEMENTATION_NOTES.md). Nothing here changes a reading; this only builds the
adjacency matrices they take, so that a port result and an attempt 7 result are measured the same way.
"""
import numpy as np
import scipy.sparse as sp
from c3b import sync_steady_state
from readings import bfs_distances, N_CENTRES
from readings_v2 import all_readings, mass_and_cut
from p3_core import FLAT_VALENCE


def slice_readings(M, seed, with_walk=True):
    """c3d.slice_readings, taking a port slice instead of a c3c one."""
    A, ids, pos, ei, ej = M.adjacency()
    rng = np.random.default_rng(3000 + seed)
    N = A.shape[0]
    centres = rng.choice(N, size=min(N_CENTRES, N), replace=False)
    dist = bfs_distances(A, centres)
    if with_walk:
        r = all_readings(A, np.random.default_rng(3000 + seed))
        d_H, d_s, sw, r_lo, r_max = r["d_H"], r["d_s"], bool(r["small_world"]), r["r_lo"], r["r_max"]
    else:
        r = mass_and_cut(A, dist)
        d_H, d_s, sw, r_lo, r_max = r["d_H"], np.nan, bool(r["small_world"]), r["r_lo"], r["r_max"]
    deg = np.asarray(A.sum(axis=1)).ravel()
    vals = M.valences()
    s = sync_steady_state(A, seed)
    f = lambda x: (float(x) if x is not None and np.isfinite(x) else None)
    return dict(d_H=f(d_H), d_s=f(d_s), small_world=sw, r_lo=f(r_lo), r_max=f(r_max),
                diameter=float(dist.max()), mean_distance=float(dist.mean()),
                mean_degree=float(deg.mean()), max_degree=int(deg.max()),
                links_per_event=M.E / max(M.V, 1), tets_per_event=M.T / max(M.V, 1),
                valence_mean=float(vals.mean()), valence_sd=float(vals.std()),
                curv2=float(np.mean((vals - FLAT_VALENCE) ** 2)),
                neck_strain=float(s["max_link_diff"]), solve_residual=float(s["residual"]),
                V=M.V, T=M.T, E=M.E)


def build_spacetime(snapshots):
    """c3a.build_spacetime, taking the port's (edges, kids, absorbed) arrays.

    `kids` is (parent, child) pairs including the parent itself; `absorbed` is (v, a) pairs. Both
    are what c3a's `children` and `absorbed` dicts held, in array form.
    """
    key = {}

    def node(t, v):
        k = (t, int(v))
        if k not in key:
            key[k] = len(key)
        return key[k]

    rows, cols = [], []
    for t, (edges, kids, absorbed) in enumerate(snapshots):
        for a, b in edges:
            rows.append(node(t, a))
            cols.append(node(t, b))
        if t + 1 >= len(snapshots):
            continue
        for v, x in kids:
            rows.append(node(t, v))
            cols.append(node(t + 1, x))
        chain = {int(v): int(a) for v, a in absorbed}
        for v, a in chain.items():
            while a in chain:
                a = chain[a]
            rows.append(node(t, v))
            cols.append(node(t + 1, a))
    N = len(key)
    r = np.array(rows + cols)
    c = np.array(cols + rows)
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(N, N))
    A.data[:] = 1.0
    A.setdiag(0)
    A.eliminate_zeros()
    return A


def spacetime_readings(snapshots, seed):
    """c3f.spacetime_readings: ball growth on the grown spacetime pattern."""
    from c3b import readings as ball_readings
    A = build_spacetime(snapshots)
    r = ball_readings(A, seed)
    r["events"] = int(A.shape[0])
    r["links"] = int(A.nnz // 2)
    return {k: (float(v) if isinstance(v, (int, float, np.floating)) and v is not None else v)
            for k, v in r.items()}
