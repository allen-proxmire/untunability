"""C3c model (note 18, C67; D25, D26; IMPLEMENTATION_NOTES.md, C3c section).

A triangulated 3-torus slice stored as tetrahedra (4-vertex tuples) with, per vertex, the set of
tetrahedra containing it, per edge its valence (number of tetrahedra containing it), and per vertex
its neighbour set. Every move is "remove these tetrahedra, add these": link-condition contraction
(merge), star split, 2-3 and 3-2 flips. Cost S = alpha*E + lam*sum_edges (valence - 5.104)^2
- gamma*sum_links ((phi_x - phi_y)/(sigma/K))^2.
"""
import math
import random
import numpy as np
import scipy.sparse as sp

FLAT_VALENCE = 2 * math.pi / math.acos(1 / 3)  # 5.1043
SIGMA = 0.0005
K = 0.5
K_RESPONSE = 1.0


class RandomSet:
    def __init__(self):
        self.items, self.pos = [], {}

    def add(self, x):
        if x not in self.pos:
            self.pos[x] = len(self.items)
            self.items.append(x)

    def discard(self, x):
        i = self.pos.pop(x, None)
        if i is None:
            return
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last
            self.pos[last] = i

    def choice(self, rng):
        return self.items[int(rng.integers(len(self.items)))]

    def __len__(self):
        return len(self.items)


def ekey(a, b):
    return (a, b) if a < b else (b, a)


def edges_of(t):
    a, b, c, d = t
    return (ekey(a, b), ekey(a, c), ekey(a, d), ekey(b, c), ekey(b, d), ekey(c, d))


class Slice3:
    def __init__(self, n):
        self.tets = {}           # tid -> sorted 4-tuple
        self.tetkey = {}         # sorted 4-tuple -> tid
        self.vt = {}             # vertex -> set of tids
        self.val = {}            # edge -> valence
        self.nbrs = {}           # vertex -> set of neighbours
        self.tid_set = RandomSet()
        self.val3 = RandomSet()  # edges of valence 3
        self.next_tid = 0
        idx = lambda i, j, k: (i % n) * n * n + (j % n) * n + (k % n)
        for v in range(n ** 3):
            self.vt[v] = set()
            self.nbrs[v] = set()
        self.next_id = n ** 3
        perms = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for p in perms:
                        cur = [i, j, k]
                        verts = [idx(*cur)]
                        for ax in p:
                            cur[ax] += 1
                            verts.append(idx(*cur))
                        self.add_tet(verts)
        if len(self.tetkey) != len(self.tets):
            raise RuntimeError("repeated tetrahedra in the start")

    # ---- primitives ---------------------------------------------------------
    def add_tet(self, verts):
        t = tuple(sorted(verts))
        if len(set(t)) != 4 or t in self.tetkey:
            raise RuntimeError(f"invalid or repeated tetrahedron {t}")
        tid = self.next_tid
        self.next_tid += 1
        self.tets[tid] = t
        self.tetkey[t] = tid
        self.tid_set.add(tid)
        for v in t:
            self.vt[v].add(tid)
        for e in edges_of(t):
            old = self.val.get(e, 0)
            self.val[e] = old + 1
            if old == 0:
                self.nbrs[e[0]].add(e[1]); self.nbrs[e[1]].add(e[0])
            if old + 1 == 3:
                self.val3.add(e)
            elif old == 3:
                self.val3.discard(e)
        return tid

    def remove_tet(self, tid):
        t = self.tets.pop(tid)
        del self.tetkey[t]
        self.tid_set.discard(tid)
        for v in t:
            self.vt[v].discard(tid)
        for e in edges_of(t):
            old = self.val[e]
            if old == 1:
                del self.val[e]
                self.nbrs[e[0]].discard(e[1]); self.nbrs[e[1]].discard(e[0])
            else:
                self.val[e] = old - 1
            if old == 3:
                self.val3.discard(e)
            elif old - 1 == 3:
                self.val3.add(e)

    def degree(self, v):
        return len(self.nbrs[v])

    # ---- cost change --------------------------------------------------------
    def delta_S(self, remove, add, alpha, lam, gamma, phi, phi_extra=None):
        """Change in S if tetrahedra `remove` (tids) are replaced by `add` (vertex tuples).
        phi_extra: tick counts for vertices not yet in phi (a new split child)."""
        if alpha == 0 and lam == 0 and gamma == 0:
            return 0.0
        dv = {}
        for tid in remove:
            for e in edges_of(self.tets[tid]):
                dv[e] = dv.get(e, 0) - 1
        for t in add:
            for e in edges_of(tuple(sorted(t))):
                dv[e] = dv.get(e, 0) + 1
        dS = 0.0
        scale = (SIGMA / K) ** 2
        for e, d in dv.items():
            if d == 0:
                continue
            old = self.val.get(e, 0)
            new = old + d
            if lam:
                dS += lam * (((new - FLAT_VALENCE) ** 2 if new > 0 else 0.0) - ((old - FLAT_VALENCE) ** 2 if old > 0 else 0.0))
            born, dies = old == 0 and new > 0, old > 0 and new == 0
            if born or dies:
                if alpha:
                    dS += alpha if born else -alpha
                if gamma:
                    pa = phi_extra[e[0]] if phi_extra and e[0] in phi_extra else phi[e[0]]
                    pb = phi_extra[e[1]] if phi_extra and e[1] in phi_extra else phi[e[1]]
                    s2 = (pa - pb) ** 2 / scale
                    dS += -gamma * s2 if born else gamma * s2
        return dS

    # ---- merge (contraction) ------------------------------------------------
    def link_condition(self, v, a):
        """Lk(v) ∩ Lk(a) == Lk(va) for the vertices, edges and triangles of the links."""
        tv, ta = self.vt[v], self.vt[a]
        both = tv & ta
        if not both:
            return False
        lk_va_edges = set()
        lk_va_verts = set()
        for tid in both:
            p, q = [x for x in self.tets[tid] if x != v and x != a]
            lk_va_edges.add(ekey(p, q)); lk_va_verts.update((p, q))
        common_verts = (self.nbrs[v] - {a}) & (self.nbrs[a] - {v})
        if common_verts != lk_va_verts:
            return False
        def link_edges_tris(x, tids, other):
            E, F = set(), set()
            for tid in tids:
                t = self.tets[tid]
                if other in t:
                    continue
                tri = tuple(y for y in t if y != x)
                F.add(tri)
                E.update((ekey(tri[0], tri[1]), ekey(tri[0], tri[2]), ekey(tri[1], tri[2])))
            return E, F
        Ev, Fv = link_edges_tris(v, tv, a)
        Ea, Fa = link_edges_tris(a, ta, v)
        if (Ev & Ea) != lk_va_edges:
            return False
        return not (Fv & Fa)

    def merge_plan(self, v, a):
        both = self.vt[v] & self.vt[a]
        only_v = self.vt[v] - both
        remove = list(both) + list(only_v)
        add = [tuple(a if x == v else x for x in self.tets[tid]) for tid in only_v]
        return remove, add

    def apply(self, remove, add):
        for tid in remove:
            self.remove_tet(tid)
        for t in add:
            self.add_tet(t)

    def merge(self, v, a, plan=None):
        remove, add = plan or self.merge_plan(v, a)
        self.apply(remove, add)
        del self.vt[v]
        del self.nbrs[v]

    # ---- split --------------------------------------------------------------
    def split_plan(self, x, u, y):
        """New vertex y takes the star of u in Lk(x); cone tetrahedra {x, y, p, q} over Lk(xu)."""
        star = self.vt[x] & self.vt[u]
        remove, add = [], []
        for tid in star:
            t = self.tets[tid]
            p, q = [z for z in t if z != x and z != u]
            remove.append(tid)
            add.append((y, u, p, q))
            add.append((x, y, p, q))
        return remove, add

    def split(self, x, u, plan=None):
        y = self.next_id
        self.next_id += 1
        self.vt[y] = set()
        self.nbrs[y] = set()
        remove, add = plan or self.split_plan(x, u, y)
        self.apply(remove, add)
        return y

    # ---- flips --------------------------------------------------------------
    def flip23_plan(self, tid, face_index):
        t = self.tets[tid]
        tri = tuple(z for i, z in enumerate(t) if i != face_index)
        d = t[face_index]
        others = (self.vt[tri[0]] & self.vt[tri[1]] & self.vt[tri[2]]) - {tid}
        if len(others) != 1:
            return None
        tid2 = next(iter(others))
        e = [z for z in self.tets[tid2] if z not in tri][0]
        if e == d or ekey(d, e) in self.val:
            return None
        a, b, c = tri
        return [tid, tid2], [(d, e, a, b), (d, e, b, c), (d, e, a, c)]

    def flip32_plan(self, edge):
        d, e = edge
        star = self.vt[d] & self.vt[e]
        if len(star) != 3:
            return None
        ring = set()
        for tid in star:
            ring.update(z for z in self.tets[tid] if z != d and z != e)
        if len(ring) != 3:
            return None
        a, b, c = sorted(ring)
        if self.vt[a] & self.vt[b] & self.vt[c]:
            return None  # triangle abc already exists
        return list(star), [(a, b, c, d), (a, b, c, e)]

    # ---- checks and graph ---------------------------------------------------
    def check(self):
        notes = []
        T = len(self.tets)
        V = len(self.vt)
        E = len(self.val)
        faces = {}
        for t in self.tets.values():
            for i in range(4):
                f = t[:i] + t[i + 1:]
                faces[f] = faces.get(f, 0) + 1
        if any(c != 2 for c in faces.values()):
            notes.append("a triangle not in exactly two tetrahedra")
        if V - E + len(faces) - T != 0:
            notes.append(f"V-E+F-T = {V - E + len(faces) - T}")
        if len(self.tetkey) != T:
            notes.append("repeated tetrahedra")
        for v, tids in self.vt.items():
            if not tids:
                notes.append(f"vertex {v} in no tetrahedron")
                break
            tris = [tuple(z for z in self.tets[tid] if z != v) for tid in tids]
            lv = set(z for tri in tris for z in tri)
            le = set()
            parent = {tri: tri for tri in tris}
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            by_edge = {}
            for tri in tris:
                for ed in (ekey(tri[0], tri[1]), ekey(tri[0], tri[2]), ekey(tri[1], tri[2])):
                    le.add(ed)
                    by_edge.setdefault(ed, []).append(tri)
            for ed, ts in by_edge.items():
                if len(ts) != 2:
                    notes.append(f"link of {v} not a closed surface")
                    return notes
                ra, rb = find(ts[0]), find(ts[1])
                if ra != rb:
                    parent[ra] = rb
            if len(lv) - len(le) + len(tris) != 2 or len({find(t) for t in tris}) != 1:
                notes.append(f"link of {v} not a sphere")
                return notes
            if lv != self.nbrs[v]:
                notes.append(f"neighbour set of {v} inconsistent")
                return notes
        return notes

    def adjacency(self):
        ids = list(self.vt)
        pos = {v: i for i, v in enumerate(ids)}
        ei = np.fromiter((pos[e[0]] for e in self.val), dtype=np.int64, count=len(self.val))
        ej = np.fromiter((pos[e[1]] for e in self.val), dtype=np.int64, count=len(self.val))
        N = len(ids)
        A = sp.csr_matrix((np.ones(2 * len(ei)), (np.concatenate([ei, ej]), np.concatenate([ej, ei]))), shape=(N, N))
        return A, ids, pos, ei, ej


def weighted_choice(rng, dS):
    if len(dS) == 1:
        return 0
    x = -(np.asarray(dS, float) - min(dS))
    w = np.exp(np.clip(x, -700, 0))
    return int(rng.choice(len(dS), p=w / w.sum()))


def tick(M, b, omega, phi, rng, alpha, lam, gamma):
    """One growth tick. Returns counts."""
    none = alpha == 0 and lam == 0 and gamma == 0
    ids = list(M.vt)
    bb = np.array([b[v] for v in ids])
    mu = np.maximum(0.0, 1.0 + K_RESPONSE * (bb - 1.0))
    c = rng.geometric(1.0 / (1.0 + mu)) - 1
    cnt = dict(zip(ids, c.tolist()))
    forced = merges = splits = f_acc = f_try = 0
    order = [v for v in ids if cnt[v] == 0]
    rng.shuffle(order)
    for v in order:
        cands, plans, dS = [], [], []
        for a in list(M.nbrs[v]):
            if M.link_condition(v, a):
                plan = M.merge_plan(v, a)
                cands.append(a); plans.append(plan)
                if not none:
                    dS.append(M.delta_S(plan[0], plan[1], alpha, lam, gamma, phi))
        if not cands:
            cnt[v] = 1
            forced += 1
            continue
        k = int(rng.integers(len(cands))) if none else weighted_choice(rng, dS)
        a = cands[k]
        M.merge(v, a, plans[k])
        b[a] += b.pop(v)
        del phi[v], omega[v]
        merges += 1
    order = [v for v in ids if v in M.vt and cnt[v] >= 1]
    rng.shuffle(order)
    for v in order:
        kids = [v]
        for _ in range(cnt[v] - 1):
            x = kids[-1]
            y = M.next_id
            opts = sorted(M.nbrs[x])
            plans = [M.split_plan(x, u, y) for u in opts]
            if none:
                k = int(rng.integers(len(opts)))
            else:
                extra = {y: phi[x]}
                k = weighted_choice(rng, [M.delta_S(p[0], p[1], alpha, lam, gamma, phi, extra) for p in plans])
            y = M.split(x, opts[k], plans[k])
            phi[y] = phi[x]
            omega[y] = omega[x]
            kids.append(y)
            splits += 1
        share = b[v] / len(kids)
        for x in kids:
            b[x] = share
    # one flip sweep: as many attempts as events
    for _ in range(len(M.vt)):
        f_try += 1
        if rng.random() < 0.5:
            tid = M.tid_set.choice(rng)
            plan = M.flip23_plan(tid, int(rng.integers(4)))
            if plan is None:
                continue
            # proposal correction: forward picks a triangle (1/F), reverse picks a valence-3 edge (1/n3 after)
            corr = 2 * len(M.tets) / max(n3_after_exact(M, plan), 1)
        else:
            if len(M.val3) == 0:
                continue
            edge = M.val3.choice(rng)
            plan = M.flip32_plan(edge)
            if plan is None:
                continue
            n3_before = len(M.val3)
            F_after = 2 * (len(M.tets) - 1)
            corr = n3_before / F_after
        dS = 0.0 if none else M.delta_S(plan[0], plan[1], alpha, lam, gamma, phi)
        acc = corr * math.exp(-dS) if dS > -700 else float("inf")
        if acc >= 1 or rng.random() < acc:
            M.apply(plan[0], plan[1])
            f_acc += 1
    # sync update (C2b)
    A, idsA, pos, ei, ej = M.adjacency()
    ph = np.array([phi[v] for v in idsA])
    om = np.array([omega[v] for v in idsA])
    deg = np.bincount(np.concatenate([ei, ej]), minlength=len(idsA)).astype(float)
    t_ = np.tanh(ph[ej] - ph[ei])
    pull = np.bincount(ei, weights=t_, minlength=len(idsA)) - np.bincount(ej, weights=t_, minlength=len(idsA))
    ph = ph + om + (K / deg) * pull
    for i, v in enumerate(idsA):
        phi[v] = ph[i]
    return dict(forced=forced, merges=merges, splits=splits, flips_accepted=f_acc, flips_tried=f_try, size=len(M.vt))


def n3_after_exact(M, plan):
    """Number of valence-3 edges after applying a flip plan (without applying it)."""
    remove, add = plan
    dv = {}
    for tid in remove:
        for e in edges_of(M.tets[tid]):
            dv[e] = dv.get(e, 0) - 1
    for t in add:
        for e in edges_of(tuple(sorted(t))):
            dv[e] = dv.get(e, 0) + 1
    n3 = len(M.val3)
    for e, d in dv.items():
        old = M.val.get(e, 0)
        new = old + d
        n3 += (new == 3) - (old == 3)
    return n3


def flip_randomize(M, sweeps, rng):
    """Calibration RC: uniform-measure 2-3/3-2 flips at fixed vertex set (no cost)."""
    acc = 0
    for _ in range(sweeps * len(M.vt)):
        if rng.random() < 0.5:
            plan = M.flip23_plan(M.tid_set.choice(rng), int(rng.integers(4)))
            if plan is None:
                continue
            corr = 2 * len(M.tets) / max(n3_after_exact(M, plan), 1)
        else:
            if len(M.val3) == 0:
                continue
            plan = M.flip32_plan(M.val3.choice(rng))
            if plan is None:
                continue
            corr = len(M.val3) / (2 * (len(M.tets) - 1))
        if corr >= 1 or rng.random() < corr:
            M.apply(plan[0], plan[1])
            acc += 1
    return acc


def slice_readings(M, seed):
    """Ball-growth readings (C3b form), degrees, valences and C3b's neck strain (fresh rates)."""
    from c3b import readings as ball_readings, sync_steady_state
    A, ids, pos, ei, ej = M.adjacency()
    r = ball_readings(A, seed)
    deg = np.asarray(A.sum(axis=1)).ravel()
    vals = np.fromiter(M.val.values(), dtype=float, count=len(M.val))
    s = sync_steady_state(A, seed)
    return dict(d_H=r["d_H"], small_world=r["small_world"], r_lo=r["r_lo"], r_max=r["r_max"],
                mean_degree=float(deg.mean()), max_degree=int(deg.max()),
                valence_mean=float(vals.mean()), valence_sd=float(vals.std()),
                curv2=float(np.mean((vals - FLAT_VALENCE) ** 2)),
                neck_strain=float(s["max_link_diff"]), solve_residual=float(s["residual"]), V=len(M.vt), T=len(M.tets))
