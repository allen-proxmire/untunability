"""C1 model (note 3): ED's causal growth with slices as circles and no splitting.

Kesten's tree (critical offspring (1/2)^(c+1), size-biased spine) with cyclic order,
in-slice circle links and forward runs of c+1 consecutive next-slice events.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components


def grow(T, seed, flat_L=None):
    """Return slices as offspring arrays. flat_L: every event exactly one child, slices of flat_L."""
    rng = np.random.default_rng(seed)
    lengths = [1 if flat_L is None else flat_L]
    offspring = []
    spine = 0
    for t in range(T - 1):
        L = lengths[-1]
        if flat_L is not None:
            c = np.ones(L, dtype=np.int64)
        else:
            c = rng.geometric(0.5, size=L) - 1          # P(c) = (1/2)^(c+1), c >= 0
            c[spine] = 1 + rng.negative_binomial(2, 0.5)  # P(c) = c (1/2)^(c+1), c >= 1
        offspring.append(c)
        if flat_L is None:
            start = int(np.sum(c[:spine]))
            spine = start + int(rng.integers(c[spine]))
        lengths.append(int(c.sum()))
    return lengths, offspring


def slice_lengths(T, seed):
    return grow(T, seed)[0]


def build(lengths, offspring):
    """Edges of the spacetime pattern plus structure checks (S2)."""
    T = len(lengths)
    offs = np.concatenate([[0], np.cumsum(lengths)])
    N = int(offs[-1])
    slice_of = np.repeat(np.arange(T), lengths)
    edges = []
    parent_edges = []
    ok = True
    notes = []
    for t in range(T):
        L = lengths[t]
        base = offs[t]
        idx = np.arange(L) + base
        if L >= 3:
            e = np.stack([idx, np.roll(idx, -1)], axis=1)
            edges.append(e)
            deg = np.bincount(np.concatenate([e[:, 0], e[:, 1]]) - base, minlength=L)
            A = sp.csr_matrix((np.ones(L), (e[:, 0] - base, e[:, 1] - base)), shape=(L, L))
            ncomp, _ = connected_components(A, directed=False)
            if not (np.all(deg == 2) and ncomp == 1):
                ok = False
                notes.append(f"slice {t} not a single cycle")
        elif L == 2:
            edges.append(np.array([[base, base + 1]]))
    for t in range(T - 1):
        c = offspring[t]
        L, Ln = lengths[t], lengths[t + 1]
        base, nbase = offs[t], offs[t + 1]
        starts = np.concatenate([[0], np.cumsum(c)[:-1]])
        f = []
        for i in range(L):
            for j in range(c[i] + 1):
                f.append((base + i, nbase + (starts[i] + j) % Ln))
            for j in range(c[i]):
                parent_edges.append((base + i, nbase + starts[i] + j))
        f = np.array(f, dtype=np.int64)
        if len(f) != Ln + L:
            ok = False
            notes.append(f"slice {t}: forward links {len(f)} != L_(t+1) + L_t = {Ln + L}")
        if not np.all((slice_of[f[:, 0]] == t) & (slice_of[f[:, 1]] == t + 1)):
            ok = False
            notes.append(f"slice {t}: a forward link does not join t to t+1")
        edges.append(f)
    pe = np.array(parent_edges, dtype=np.int64).reshape(-1, 2)
    if len(pe) != N - 1:
        ok = False
        notes.append(f"parent links {len(pe)} != events - 1 = {N - 1}")
    else:
        P = sp.csr_matrix((np.ones(len(pe)), (pe[:, 0], pe[:, 1])), shape=(N, N))
        nc, _ = connected_components(P, directed=False)
        if nc != 1:
            ok = False
            notes.append(f"parent links form {nc} components, not one tree")
    E = np.concatenate(edges)
    E = np.sort(E, axis=1)
    E = E[E[:, 0] != E[:, 1]]
    E = np.unique(E, axis=0)
    A = sp.csr_matrix((np.ones(2 * len(E)), (np.concatenate([E[:, 0], E[:, 1]]), np.concatenate([E[:, 1], E[:, 0]]))), shape=(N, N))
    A.data[:] = 1.0
    return A, ok, notes


def flat_structure_ok_note():
    return "flat strip: no parent-tree check (every event one child starting from a full slice, so parent links are N - L, a forest of L lines)"
