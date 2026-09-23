"""The 2+1 test (note 6, C9; Allen D6): ED's layered spacetime in one dimension down, on attempt 8's 3D engine.

A spacetime is a 3D triangulation of T^2 x S^1 foliated into T slices; every tetrahedron spans two consecutive slices, of
type (3,1), (2,2) or (1,3). Each slice is a triangulated torus (its spatial triangles are the tetrahedra's faces lying in
one slice). Every allowed spacetime counts once (A10 D3), with a soft hold on ED's totals: the number of events N0 (total
only, D6/L-Q7) and N22, which with N0 fixes the forward links (N1T = 2 N0 + N22) - L-Q5/L-Q6 at the flat value.

Moves are the published 3D CDT move set (Ambjorn-Jurkiewicz-Loll hep-th/0011276, moves 1-5), used as tools only:
  26  insert an event into a spatial triangle (its (3,1) tet above and (1,3) tet below become 6)      N0 +1, N3 +4
  62  its inverse: remove an event whose star is exactly those 6 tetrahedra                            N0 -1, N3 -4
  44  flip a spatial link inside a slice (4 tets round it, two above sharing an apex, two below)       counts unchanged
  23  two tetrahedra sharing a timelike triangle, apexes in different slices -> 3 round a new timelike link   N22 +1
  32  its inverse on a timelike link of valence 3 whose ring is not all in one slice                   N22 -1
Proposals (move chosen 1/5 each):
  26: uniform tetrahedron (1/N3), used if it is a (3,1) with its base below   -> each spatial triangle 1/N3
  62: uniform event (1/N0)
  44: uniform tetrahedron (1/N3), a (3,1)-up, and one of its 3 base links (1/3) -> each spatial link 2/(3 N3)
  23: uniform tetrahedron and face (1/(4 N3)); the face must be timelike      -> each timelike triangle 1/(2 N3)
  32: a random event, then a random neighbour -> each link (1/N0)(1/deg d + 1/deg e)   (docstring fixed after review)
Acceptance min(1, q_rev/q_fwd x w'/w), w = exp(-EPS [(N0 - N0*)^2 + (N22 - N22*)^2]); q_rev computed in the new state.
Ceiling: no event may exceed 60 links within its slice (ED's ceiling).
"""
import os
import sys
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from p3 import Slice3P, B_A                                              # noqa: E402
from p3_ops import (apply_plan, tet_remove, vert_free, vert_new, valence, edge_slot, C_T, C_V, C_V3, C_E,  # noqa
                    C_OVER)

CEIL = 60


class Spacetime:
    def __init__(self, L, T, eps=0.02, seed=0, cap_factor=4, slice_tris=None):
        self.L, self.T, self.eps = L, T, eps
        self.mu0 = self.mu22 = 0.0          # linear counterweights (constant on the exact-total slice; tuned in warm-up, then frozen)
        self.slice_tris = slice_tris
        assert T >= 3, "periodic time needs at least 3 slices"
        nmax = cap_factor * L * L * T
        n = int(math.ceil((nmax / 3) ** (1 / 3))) + 2          # sizes the engine's arenas
        # FIX (review): the engine first builds an n^3 torus, so the caps must cover it too
        M = Slice3P(n, v_cap=max(nmax, n ** 3) + 64, t_cap=max(12 * nmax, 7 * n ** 3), e_cap=max(12 * nmax, 8 * n ** 3))
        S = M.S
        for tid in list(S.t_items[:S.ctr[C_T]]):
            tet_remove(S, int(tid))
        for v in list(M.vertices()):
            vert_free(S, int(v))
        self.M, self.S = M, S
        self.time = np.full(S.v_alive.shape[0], -1, dtype=np.int64)
        self.rng = np.random.default_rng(seed)
        self._build_flat()
        self.N0s, self.N22s = self.N0(), self.N22()
        self.N22_cur = self.N22s
        self.tried = self.acc = 0
        self.why = {}
        self.acck = {}

    # ---- construction: triangular-lattice torus slices, staircase prism layers ------------------
    def _build_flat(self):
        L, T, S = self.L, self.T, self.S
        ids = np.zeros((T, L, L), dtype=np.int64)
        for t in range(T):
            for i in range(L):
                for j in range(L):
                    v = vert_new(S)
                    ids[t, i, j] = v
                    self.time[v] = t
        if self.slice_tris is None:
            tris = []
            for i in range(L):
                for j in range(L):
                    a, b, c, d = (i, j), ((i + 1) % L, j), (i, (j + 1) % L), ((i + 1) % L, (j + 1) % L)
                    tris.append((a, b, d))
                    tris.append((a, d, c))
        else:                                                   # a given torus triangulation on labels 0..L^2-1
            tris = [tuple((x // L, x % L) for x in tri) for tri in self.slice_tris]
        order = {}
        for i in range(L):
            for j in range(L):
                order[(i, j)] = i * L + j
        for t in range(T):
            t1 = (t + 1) % T
            for tri in tris:
                q = sorted(tri, key=lambda p: order[p])        # global order -> consistent staircases
                lo = [int(ids[t, p[0], p[1]]) for p in q]
                hi = [int(ids[t1, p[0], p[1]]) for p in q]
                for k in range(3):                             # simplices (lo_0..lo_k, hi_k..hi_2)
                    verts = lo[:k + 1] + hi[k:]
                    self._tet_add(verts)

    def _tet_add(self, verts):
        from p3_ops import tet_add
        tet_add(self.S, *[int(x) for x in verts])

    # ---- counts ---------------------------------------------------------------------------------
    def N0(self):
        return int(self.S.ctr[C_V])

    def N3(self):
        return int(self.S.ctr[C_T])

    def tet_times(self, verts):
        return [int(self.time[v]) for v in verts]

    def ttype(self, verts):
        """(k, 4-k) as the number of vertices in the lower of the two slices; None if not a valid layer piece."""
        ts = self.tet_times(verts)
        u = sorted(set(ts))
        if len(u) != 2:
            return None
        a, b = u
        if (b - a) == 1:
            lo = a
        elif a == 0 and b == self.T - 1:
            lo = b
        else:
            return None
        k = sum(1 for x in ts if x == lo)
        return k, lo

    def N22(self):
        S = self.S
        n = 0
        for tid in S.t_items[:S.ctr[C_T]]:
            r = self.ttype(S.tv[tid])
            if r and r[0] == 2:
                n += 1
        return n

    def weight(self, n0, n22):
        if getattr(self, "mode", "ed") == "cdt":               # plain 3D CDT: exp(k0 N0 - k3 N3), volume held softly
            n3 = 4 * n0 + n22
            return self.k0 * n0 - self.epsv * (n3 - self.N3s) ** 2
        d0, d22 = n0 - self.N0s, n22 - self.N22s
        return -self.mu0 * d0 - self.mu22 * d22 - self.eps * (d0 * d0 + d22 * d22)

    def as_cdt(self, k0, epsv=0.0005):
        """Switch to plain 3D CDT at coupling k0, with the total volume N3 held near its present value (validation)."""
        self.mode, self.k0, self.epsv = "cdt", float(k0), float(epsv)
        self.N3s = self.N3()
        return self

    def tune(self, steps, rounds=40, gain=0.02):
        """Warm-up only: adjust the linear counterweights so the totals sit at ED's values; then they stay frozen."""
        for _ in range(rounds):
            s0 = s22 = 0.0
            for _ in range(steps):
                self.step()
                s0 += self.N0() - self.N0s
                s22 += self.N22_cur - self.N22s
            self.mu0 += gain * s0 / steps
            self.mu22 += gain * s22 / steps

    def to_exact(self, max_steps=200000):
        """Step until both totals are exactly at ED's values (readings are taken only there)."""
        for _ in range(max_steps):
            if self.N0() == self.N0s and self.N22_cur == self.N22s:
                return True
            self.step()
        return False

    # ---- helpers --------------------------------------------------------------------------------
    def tets_of(self, v):
        S = self.S
        s = S.v_ts[v]
        return [int(S.at_data[s + i]) for i in range(S.v_tl[v])]

    def nbrs(self, v):
        S = self.S
        s = S.v_ns[v]
        return [int(S.an_data[s + i]) for i in range(S.v_nl[v])]

    def sdeg(self, v):
        t = self.time[v]
        return sum(1 for w in self.nbrs(v) if self.time[w] == t)

    def tv(self, tid):
        return [int(x) for x in self.S.tv[tid]]

    def _plan(self, rem, add):
        S = self.S
        for i, t in enumerate(rem):
            S.buf_rem[B_A + i] = t
        for i, q in enumerate(add):
            for j in range(4):
                S.buf_add[B_A + i, j] = q[j]
        return len(rem), len(add)

    def _apply(self, rem, add):
        nr, na = self._plan(rem, add)
        apply_plan(self.S, B_A, nr, na)
        if self.S.ctr[C_OVER]:
            raise RuntimeError("capacity overflow %d" % self.S.ctr[C_OVER])

    def _edge_exists(self, a, b):
        return edge_slot(self.S, a, b) >= 0 and valence(self.S, a, b) > 0

    def _tets_with(self, verts):
        v0 = verts[0]
        out = []
        for t in self.tets_of(v0):
            tv = self.tv(t)
            if all(x in tv for x in verts):
                out.append(t)
        return out

    # ---- moves: each returns (rem, add, dN0, dN22, extra) or a reason string ---------------------
    def _up_base(self, tid):
        """If tid is a (3,1) tetrahedron with its base in slice t and apex in t+1: (base triangle, apex)."""
        tv = self.tv(tid)
        r = self.ttype(tv)
        if not r or r[0] != 3:
            return None
        lo = r[1]
        base = [v for v in tv if self.time[v] == lo]
        apex = [v for v in tv if self.time[v] != lo][0]
        return base, apex

    def m26(self, tid):
        ub = self._up_base(tid)
        if ub is None:
            return "26 not a (3,1)"
        (a, b, c), p = ub
        below = [t for t in self._tets_with([a, b, c]) if t != tid]
        if len(below) != 1:
            return "26 no lower tet"
        q = [x for x in self.tv(below[0]) if x not in (a, b, c)][0]
        for w in (a, b, c):
            if self.sdeg(w) + 1 > CEIL:
                return "26 ceiling"
        return ([tid, below[0]],
                [(None, a, b, p), (None, b, c, p), (None, a, c, p), (None, a, b, q), (None, b, c, q), (None, a, c, q)],
                +1, 0, dict(tlabel=self.time[a]))

    def m62(self, v):
        st = self.tets_of(v)
        if len(st) != 6:
            return "62 not 6 tets"
        t0 = self.time[v]
        up, down = set(), set()
        spat = set()
        for tid in st:
            for w in self.tv(tid):
                if w == v:
                    continue
                if self.time[w] == t0:
                    spat.add(w)
                elif (self.time[w] - t0) % self.T == 1:
                    up.add(w)
                else:
                    down.add(w)
        if len(spat) != 3 or len(up) != 1 or len(down) != 1:
            return "62 wrong star"
        a, b, c = sorted(spat)
        p, q = next(iter(up)), next(iter(down))
        if self._tets_with([a, b, c]):
            return "62 triangle exists"
        return (st, [(a, b, c, p), (a, b, c, q)], -1, 0, dict(gone=v))

    def m44(self, tid, k):
        ub = self._up_base(tid)
        if ub is None:
            return "44 not a (3,1)"
        base, p = ub
        a, b = [x for i, x in enumerate(base) if i != k]
        around = self._tets_with([a, b])
        if len(around) != 4:
            return "44 valence not 4"
        ups, downs = [], []
        t0 = self.time[a]
        for t in around:
            tv = self.tv(t)
            others = [x for x in tv if x not in (a, b)]
            ts = [self.time[x] for x in others]
            if sum(1 for x in ts if x == t0) != 1:
                return "44 not (3,1)"
            sp = [x for x in others if self.time[x] == t0][0]
            ap = [x for x in others if self.time[x] != t0][0]
            (ups if (self.time[ap] - t0) % self.T == 1 else downs).append((sp, ap))
        if len(ups) != 2 or len(downs) != 2:
            return "44 shape"
        if ups[0][1] != ups[1][1] or downs[0][1] != downs[1][1]:
            return "44 apexes differ"
        c, d = ups[0][0], ups[1][0]
        if {downs[0][0], downs[1][0]} != {c, d} or c == d:
            return "44 shape"
        if self._edge_exists(c, d):
            return "44 edge exists"
        for w in (c, d):
            if self.sdeg(w) + 1 > CEIL:
                return "44 ceiling"
        P, Q = ups[0][1], downs[0][1]
        return (around, [(c, d, a, P), (c, d, b, P), (c, d, a, Q), (c, d, b, Q)], 0, 0, {})

    def m23(self, tid, f):
        tv = self.tv(tid)
        d = tv[f]
        tri = [x for i, x in enumerate(tv) if i != f]
        if len(set(self.time[x] for x in tri)) == 1:
            return "23 spatial triangle"
        other = [t for t in self._tets_with(tri) if t != tid]
        if len(other) != 1:
            return "23 no partner"
        e = [x for x in self.tv(other[0]) if x not in tri][0]
        if self.time[d] == self.time[e]:
            return "23 apexes same slice"
        if self._edge_exists(d, e):
            return "23 edge exists"
        add = [(d, e, tri[0], tri[1]), (d, e, tri[1], tri[2]), (d, e, tri[0], tri[2])]
        for q in add:
            if self.ttype(q) is None:
                return "23 bad piece"
        return ([tid, other[0]], add, 0, None, {})

    def m32(self, slot):
        S = self.S
        d, e = int(S.e_a[slot]), int(S.e_b[slot])
        if self.time[d] == self.time[e]:
            return "32 spatial link"
        around = self._tets_with([d, e])
        if len(around) != 3:
            return "32 valence"
        ring = sorted(set(x for t in around for x in self.tv(t) if x not in (d, e)))
        if len(ring) != 3:
            return "32 ring"
        if len(set(self.time[x] for x in ring)) == 1:
            return "32 ring in one slice"
        if self._tets_with(ring):
            return "32 triangle exists"
        add = [tuple(ring) + (d,), tuple(ring) + (e,)]
        for q in add:
            if self.ttype(q) is None:
                return "32 bad piece"
        return (around, add, 0, None, {})

    # ---- one Metropolis step (every q known before applying, so nothing is ever undone) ----------
    def _dN22(self, rem, add):
        dn = 0
        for t in rem:
            r = self.ttype(self.tv(t))
            if r and r[0] == 2:
                dn -= 1
        for q in add:
            r = self.ttype(list(q))
            if r and r[0] == 2:
                dn += 1
        return dn

    def _q32(self, d, e, dd=0, de=0):
        """Probability of proposing the link (d, e) for a 3-2 move: random event, random neighbour."""
        return (1.0 / self.N0()) * (1.0 / (self.S.v_nl[d] + dd) + 1.0 / (self.S.v_nl[e] + de))

    def step(self):
        S = self.S
        self.tried += 1
        kind = int(self.rng.integers(5))
        N0, N3 = self.N0(), self.N3()
        if kind == 0:
            tid = int(S.t_items[int(self.rng.integers(N3))])
            r = self.m26(tid)
            if isinstance(r, str):
                return self._no(r)
            q_fwd, q_rev = 1.0 / N3, 1.0 / (N0 + 1)
        elif kind == 1:
            vs = self.M.vertices()
            r = self.m62(int(vs[int(self.rng.integers(len(vs)))]))
            if isinstance(r, str):
                return self._no(r)
            q_fwd, q_rev = 1.0 / N0, 1.0 / (N3 - 4)
        elif kind == 2:
            tid = int(S.t_items[int(self.rng.integers(N3))])
            r = self.m44(tid, int(self.rng.integers(3)))
            if isinstance(r, str):
                return self._no(r)
            q_fwd = q_rev = 1.0
        elif kind == 3:
            tid = int(S.t_items[int(self.rng.integers(N3))])
            r = self.m23(tid, int(self.rng.integers(4)))
            if isinstance(r, str):
                return self._no(r)
            d, e = r[1][0][0], r[1][0][1]
            q_fwd, q_rev = 1.0 / (2 * N3), self._q32(d, e, 1, 1)
        else:
            vs = self.M.vertices()
            v = int(vs[int(self.rng.integers(len(vs)))])
            nb = self.nbrs(v)
            w = nb[int(self.rng.integers(len(nb)))]
            slot = edge_slot(S, v, w)
            r = self.m32(slot)
            if isinstance(r, str):
                return self._no(r)
            q_fwd, q_rev = self._q32(v, w), 1.0 / (2 * (N3 - 1))
        rem, add, dN0, _, extra = r
        y = None
        if kind == 0:
            y = self.M.next_free_vertex()
            add = [tuple(y if x is None else x for x in q) for q in add]
            self.time[y] = extra["tlabel"]
        dN22 = self._dN22(rem, add)
        lw = self.weight(N0 + dN0, self.N22_cur + dN22) - self.weight(N0, self.N22_cur)
        la = math.log(q_rev / q_fwd) + lw
        if la < 0 and self.rng.random() >= math.exp(la):
            if kind == 0:
                self.time[y] = -1
            return self._no("hastings")
        if kind == 0:
            if vert_new(S) != y:
                raise RuntimeError("vertex label mismatch")
        self._apply(rem, add)
        if kind == 1:
            vert_free(S, extra["gone"])
            self.time[extra["gone"]] = -1
        self.N22_cur += dN22
        self.acc += 1
        self.acck[kind] = self.acck.get(kind, 0) + 1        # accepted by move kind (diagnostic)
        return True

    # ---- checks ---------------------------------------------------------------------------------
    def check(self):
        """Structure check (engine), every tetrahedron a layer piece, every slice a closed surface (each spatial link in
        exactly two spatial triangles), tracked N22 equal to a full recount."""
        notes = list(self.M.check())
        S = self.S
        spat_tri = {}
        for tid in S.t_items[:S.ctr[C_T]]:
            tv = self.tv(tid)
            r = self.ttype(tv)
            if r is None:
                notes.append("bad piece %s" % tv)
                break
            if r[0] in (1, 3):
                lo = r[1]
                tri = tuple(sorted(x for x in tv if (self.time[x] == lo) == (r[0] == 3)))
                spat_tri[tri] = spat_tri.get(tri, 0) + 1
        if any(c != 2 for c in spat_tri.values()):
            notes.append("a spatial triangle not shared by exactly one up and one down piece")
        ecount = {}
        for tri in spat_tri:
            for i in range(3):
                for j in range(i + 1, 3):
                    ecount[(tri[i], tri[j])] = ecount.get((tri[i], tri[j]), 0) + 1
        if any(c != 2 for c in ecount.values()):
            notes.append("a spatial link not in exactly two spatial triangles")
        if self.N22() != self.N22_cur:
            notes.append("N22 tracking %d vs %d" % (self.N22_cur, self.N22()))
        return notes

    # ---- readings -------------------------------------------------------------------------------
    def slices(self):
        vs = [int(v) for v in self.M.vertices()]
        out = {t: [] for t in range(self.T)}
        for v in vs:
            out[int(self.time[v])].append(v)
        return out

    def _no(self, why):
        self.why[why] = self.why.get(why, 0) + 1
        return False


def random_torus_tris(L, sweeps=200, seed=7):
    """A randomly rewired triangulated torus on L*L vertices (attempt 7's flip randomizer), as triangles on labels
    0..L^2-1 - the crowded slices for the crowded start."""
    sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_07", "model"))
    import c3a
    Tt = c3a.Torus(L)
    c3a.flip_randomize(Tt, sweeps, np.random.default_rng(seed))
    tris = set()
    for v, R in Tt.ring.items():
        k = len(R)
        for i in range(k):
            tris.add(tuple(sorted((v, R[i], R[(i + 1) % k]))))
    return sorted(tris)
