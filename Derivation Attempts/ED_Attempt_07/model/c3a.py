"""C3a model (note 13, C49; D18, D19; IMPLEMENTATION_NOTES.md, C3a section).

A triangulated torus slice stored as a rotation system: ring[v] is the
counter-clockwise cyclic list of v's neighbours; consecutive neighbours (a, b)
in ring[v] form the triangle (v, a, b). Moves: vertex split and edge collapse
under the link condition (C43). Budget reading B on a surface (C48). Choice
rules U (uniform) and Q (weights exp(-lambda * dE), E = sum (deg - 6)^2).
"""
import math
import numpy as np
import scipy.sparse as sp
from readings import bfs_distances
from readings_v2 import all_readings

K_RESPONSE = 1.0
SIZES = (20, 40, 80)  # n; L* = n^2


class Torus:
    def __init__(self, n):
        self.ring = {}
        idx = lambda i, j: (i % n) * n + (j % n)
        for i in range(n):
            for j in range(n):
                # triangular lattice: neighbours in counter-clockwise order
                self.ring[idx(i, j)] = [idx(i + 1, j), idx(i, j + 1), idx(i - 1, j + 1),
                                        idx(i - 1, j), idx(i, j - 1), idx(i + 1, j - 1)]
        self.next_id = n * n

    def deg(self, v):
        return len(self.ring[v])

    # ---- moves -------------------------------------------------------
    def split_options(self, v):
        """All (i, j), i < j, ring positions of u, w; degrees of the two children."""
        k = len(self.ring[v])
        return [(i, j, j - i + 2, k - (j - i) + 2) for i in range(k) for j in range(i + 1, k)]

    def split(self, v, i, j):
        """Split v at ring positions i < j. v keeps arc ring[i..j]; new y takes the rest."""
        R = self.ring[v]
        k = len(R)
        u, w = R[i], R[j]
        arc1 = R[i:j + 1]
        arc2 = R[j:] + R[:i + 1]
        y = self.next_id
        self.next_id += 1
        self.ring[v] = arc1 + [y]
        self.ring[y] = arc2 + [v]
        for x in arc2[1:-1]:
            rx = self.ring[x]
            rx[rx.index(v)] = y
        ru = self.ring[u]
        p = ru.index(v)
        ru[p:p + 1] = [v, y]
        rw = self.ring[w]
        p = rw.index(v)
        rw[p:p + 1] = [y, v]
        return y

    def collapse_ok(self, v, a):
        R = self.ring[v]
        p = R.index(a)
        c1, c2 = R[(p + 1) % len(R)], R[p - 1]
        if c1 == c2:
            return False
        if len(R) + len(self.ring[a]) - 4 < 3:
            return False
        common = set(R) & set(self.ring[a])
        return common == {c1, c2} and len(self.ring[c1]) >= 4 and len(self.ring[c2]) >= 4

    def collapse(self, v, a):
        """Merge v into a (link condition assumed checked)."""
        R = self.ring[v]
        p = R.index(a)
        R = R[p:] + R[:p]  # a, n1, ..., n_{k-1}
        n1, nk1 = R[1], R[-1]
        inner = R[2:-1]
        ra = self.ring[a]
        q = ra.index(v)
        ra[q:q + 1] = inner
        self.ring[n1].remove(v)
        self.ring[nk1].remove(v)
        for x in inner:
            rx = self.ring[x]
            rx[rx.index(v)] = a
        del self.ring[v]

    def flip_ok_and_do(self, v, a, rng):
        """Metropolis flip of edge (v, a) proposed by picking v uniformly, then a neighbour uniformly.
        Proposal weight of an edge is 1/deg(v) + 1/deg(a); acceptance corrects to the uniform measure."""
        R = self.ring[v]
        dv, da = len(R), len(self.ring[a])
        if dv < 4 or da < 4:
            return False
        p = R.index(a)
        c1, c2 = R[(p + 1) % len(R)], R[p - 1]
        if c1 == c2 or c2 in self.ring[c1]:
            return False
        d1, d2 = len(self.ring[c1]), len(self.ring[c2])
        q_fwd = 1.0 / dv + 1.0 / da
        q_rev = 1.0 / (d1 + 1) + 1.0 / (d2 + 1)
        if q_rev < q_fwd and rng.random() >= q_rev / q_fwd:
            return False
        R.remove(a)
        self.ring[a].remove(v)
        r1 = self.ring[c1]
        q = r1.index(v)
        r1.insert(q + 1, c2)  # c1 ring: v, c2, a
        r2 = self.ring[c2]
        q = r2.index(a)
        r2.insert(q + 1, c1)  # c2 ring: a, c1, v
        return True

    # ---- checks and graph --------------------------------------------
    def check(self):
        notes = []
        V = len(self.ring)
        S = sum(len(r) for r in self.ring.values())  # S = 2E = 3F
        if S != 6 * V:
            notes.append(f"Euler: V - E + F = {V - S / 6:.3f} (degree sum {S}, V {V})")
        for v, R in self.ring.items():
            if len(set(R)) != len(R) or v in R or len(R) < 3:
                notes.append(f"ring of {v} invalid")
                break
            k = len(R)
            for t in range(k):
                a, b = R[t], R[(t + 1) % k]
                ra, rb = self.ring[a], self.ring[b]
                ia, ib = ra.index(v), rb.index(v)
                if ra[ia - 1] != b or rb[(ib + 1) % len(rb)] != a:
                    notes.append(f"orientation at triangle ({v},{a},{b})")
                    return notes
        return notes

    def adjacency(self):
        ids = sorted(self.ring)
        pos = {v: i for i, v in enumerate(ids)}
        rows, cols = [], []
        for v, R in self.ring.items():
            pv = pos[v]
            rows.extend([pv] * len(R))
            cols.extend(pos[x] for x in R)
        N = len(ids)
        return sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N)), ids


def choose(rng, dE, lam):
    """Index chosen uniformly (lam None) or with weights exp(-lam * dE)."""
    if lam is None:
        return int(rng.integers(len(dE)))
    x = -lam * (np.asarray(dE, float) - min(dE))
    w = np.exp(x)
    return int(rng.choice(len(dE), p=w / w.sum()))


def grow_tick(M, b, rng, lam, record=None):
    """One tick. b: dict budget. Returns dict of counts. record: optional dict for forward links."""
    ids = list(M.ring)
    bb = np.array([b[v] for v in ids])
    mu = np.maximum(0.0, 1.0 + K_RESPONSE * (bb - 1.0))
    c = rng.geometric(1.0 / (1.0 + mu)) - 1
    cnt = dict(zip(ids, c.tolist()))
    forced = collapses = splits = 0
    absorbed = {}
    order = [v for v in ids if cnt[v] == 0]
    rng.shuffle(order)
    for v in order:
        R = M.ring[v]
        cands = [a for a in R if M.collapse_ok(v, a)]
        if not cands:
            cnt[v] = 1
            forced += 1
            continue
        if lam is None:
            a = cands[int(rng.integers(len(cands)))]
        else:
            dv = len(R)
            dE = []
            for a in cands:
                p = R.index(a)
                c1, c2 = R[(p + 1) % dv], R[p - 1]
                da, d1, d2 = len(M.ring[a]), len(M.ring[c1]), len(M.ring[c2])
                before = (dv - 6) ** 2 + (da - 6) ** 2 + (d1 - 6) ** 2 + (d2 - 6) ** 2
                after = (da + dv - 4 - 6) ** 2 + (d1 - 7) ** 2 + (d2 - 7) ** 2
                dE.append(after - before)
            a = cands[choose(rng, dE, lam)]
        M.collapse(v, a)
        b[a] += b.pop(v)
        absorbed[v] = a
        collapses += 1
    children = {}
    order = [v for v in ids if v in M.ring and cnt[v] >= 1]
    rng.shuffle(order)
    for v in order:
        kids = [v]
        for _ in range(cnt[v] - 1):
            x = kids[-1]
            opts = M.split_options(x)
            if lam is None:
                i, j, _, _ = opts[int(rng.integers(len(opts)))]
            else:
                dx = len(M.ring[x])
                R = M.ring[x]
                dE = []
                for (i, j, d1, d2) in opts:
                    du, dw = len(M.ring[R[i]]), len(M.ring[R[j]])
                    before = (dx - 6) ** 2 + (du - 6) ** 2 + (dw - 6) ** 2
                    after = (d1 - 6) ** 2 + (d2 - 6) ** 2 + (du - 5) ** 2 + (dw - 5) ** 2
                    dE.append(after - before)
                i, j, _, _ = opts[choose(rng, dE, lam)]
            kids.append(M.split(x, i, j))
            splits += 1
        share = b[v] / len(kids)
        for x in kids:
            b[x] = share
        children[v] = kids
    if record is not None:
        record["children"] = children
        record["absorbed"] = absorbed
    return dict(forced=forced, collapses=collapses, splits=splits, size=len(M.ring))


def flip_randomize(M, sweeps, rng):
    """Uniform edge-flip Monte Carlo on a fixed vertex set (calibration R)."""
    ids = list(M.ring)
    E = sum(len(r) for r in M.ring.values()) // 2
    acc = 0
    for _ in range(sweeps * E):
        v = ids[int(rng.integers(len(ids)))]
        R = M.ring[v]
        a = R[int(rng.integers(len(R)))]
        acc += M.flip_ok_and_do(v, a, rng)
    return acc


def slice_readings(M, seed):
    A, _ = M.adjacency()
    r = all_readings(A, np.random.default_rng(seed))
    out = {}
    for k in ("d_H", "d_s", "d_w", "r_lo", "r_max", "N", "mean_degree"):
        out[k] = float(r[k]) if r.get(k) is not None else None
    out["small_world"] = bool(r["small_world"])
    return out


def mean_eccentricity(M, seed, n_centres=20):
    A, _ = M.adjacency()
    rng = np.random.default_rng(seed)
    centres = rng.choice(A.shape[0], size=min(n_centres, A.shape[0]), replace=False)
    d = bfs_distances(A, centres)
    return float(d.max(axis=1).mean())


def degree_stats(M):
    d = np.array([len(r) for r in M.ring.values()])
    return dict(deg_sd=float(d.std()), curv2=float(np.mean((d - 6) ** 2)), deg_max=int(d.max()))


def slice_edges(M):
    return [(v, x) for v, R in M.ring.items() for x in R if v < x]


def build_spacetime(snapshots):
    """snapshots: list of (edges_t, record_t) for consecutive ticks, where edges_t is slice t
    before tick t's moves and record_t holds that tick's children and absorbed maps.
    Nodes are (t, id); in-slice links from edges_t; forward links to children, and from a
    collapsed event to the event that finally absorbed it in slice t+1."""
    key = {}
    def node(t, v):
        if (t, v) not in key:
            key[(t, v)] = len(key)
        return key[(t, v)]
    rows, cols = [], []
    for t, (edges, rec) in enumerate(snapshots):
        for (a, b) in edges:
            rows.append(node(t, a)); cols.append(node(t, b))
        if t + 1 >= len(snapshots):
            continue
        for v, kids in rec["children"].items():
            for x in kids:
                rows.append(node(t, v)); cols.append(node(t + 1, x))
        for v, a in rec["absorbed"].items():
            while a in rec["absorbed"]:
                a = rec["absorbed"][a]
            rows.append(node(t, v)); cols.append(node(t + 1, a))
    N = len(key)
    r = np.array(rows + cols); c = np.array(cols + rows)
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(N, N))
    A.data[:] = 1.0
    A.setdiag(0)
    A.eliminate_zeros()
    return A
