"""Stage B 3D slice operations (note 14, C24) for sb_core.History, on Slice10P states (narrow moves, D14).

Bundles (type chosen 1/4 each), all V- and E-neutral:
  0  split (valence k) + narrow merge (valence k)
  1  2-3 + 3-2
  2  split (k) + narrow merge (k+1) + 2-3
  3  split (k+1) + narrow merge (k) + 3-2
Site proposals (label-invariant; REVISION after G2's first run, which accepted about 1 per cent): split = random event x
+ random neighbour -> 1/(V deg x); merge = random event v + random target among its narrow-merge targets A(v) ->
1/(V |A(v)|); 2-3 = random tetrahedron + face -> 1/(2T) per triangle (T = E - V fixed); 3-2 = uniform from the list of
valence-3 links -> 1/N3. Acceptance min(1, q_rev/q_fwd) with the reverse bundle's probability computed in the new slice.
"""
import os
import sys
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_09", "model"))

from p10 import Slice10P, narrow_ok                                        # noqa: E402
from p3 import (split_plan, merge_plan, flip23_plan, flip32_plan, link_condition, B_A)  # noqa: E402
from p3_ops import (apply_plan, allowed, valence, edge_slot, vert_free, _lst_alloc, C_V, C_T, C_VTOP, C_VFREE,  # noqa
                    C_ATTOP, C_ANTOP, C_OVER)
from p3_core import CEILING                                                 # noqa: E402
from sb_core import inverse                                                 # noqa: E402

CAP = CEILING
BIG = 10 ** 9


@njit(cache=True)
def vert_new_at(S, y):
    """Allocate the specific vertex index y (free), as vert_new does for the next free one."""
    top = S.ctr[C_VTOP]
    if y < top:
        n = S.ctr[C_VFREE]
        i = 0
        while i < n and S.v_free[i] != y:
            i += 1
        if i == n:
            return -1
        S.v_free[i] = S.v_free[n - 1]
        S.ctr[C_VFREE] = n - 1
    else:
        if y >= S.v_alive.shape[0]:
            S.ctr[C_OVER] = 5
            return -1
        for z in range(top, y):
            S.v_free[S.ctr[C_VFREE]] = z
            S.ctr[C_VFREE] += 1
        S.ctr[C_VTOP] = y + 1
    S.v_alive[y] = 1
    S.v_tl[y] = 0
    S.v_nl[y] = 0
    st, cls = _lst_alloc(S.at_data, S.at_head, S.ctr, C_ATTOP, 1)
    S.v_ts[y], S.v_tc[y] = st, cls
    st, cls = _lst_alloc(S.an_data, S.an_head, S.ctr, C_ANTOP, 1)
    S.v_ns[y], S.v_nc[y] = st, cls
    S.ctr[C_V] += 1
    return y


def _nbr(M, v):
    s = M.S.v_ns[v]
    return M.S.an_data[s:s + M.S.v_nl[v]]


def _edge_ring(M, a, b):
    """Vertices of Lk(ab): the other two vertices of every tetrahedron holding both a and b."""
    out = set()
    S = M.S
    s = S.v_ts[a]
    for i in range(S.v_tl[a]):
        t = S.at_data[s + i]
        tv = S.tv[t]
        if b in tv:
            for w in tv:
                if w != a and w != b:
                    out.add(int(w))
    return out


def _ok(M, nr, na, gone=-1):
    ok, born, dies, why = allowed(M.S, B_A, nr, na, BIG, -1.0, gone, CAP)
    return ok


class Ops3D:
    def __init__(self):
        self.stats = {}

    # ---- labels -------------------------------------------------------------------------------
    def labels(self, M):
        return set(int(v) for v in M.vertices())

    def has(self, M, y):
        return y < M.S.v_alive.shape[0] and M.S.v_alive[y] == 1

    def fresh(self, slices):
        n = min(M.S.v_alive.shape[0] for M in slices)
        occ = np.zeros(n, dtype=bool)
        for M in slices:
            occ |= M.S.v_alive[:n].astype(bool)
        free = np.flatnonzero(~occ)
        if len(free) == 0:
            raise RuntimeError("no free label")
        return int(free[0])

    def copy(self, M):
        from p3_ops import State
        C = Slice10P.__new__(Slice10P)
        C.S = State(*[a.copy() for a in M.S])
        C.n = M.n
        return C

    def same(self, A, B):
        ta = sorted(tuple(sorted(int(x) for x in A.S.tv[t])) for t in A.S.t_items[:A.S.ctr[C_T]])
        tb = sorted(tuple(sorted(int(x) for x in B.S.tv[t])) for t in B.S.t_items[:B.S.ctr[C_T]])
        return ta == tb

    # ---- sites (revision after G2's first run: targeted proposals, Hastings-corrected) -------------
    def _rand_vertex(self, M, rng):
        vs = M.vertices()
        return int(vs[int(rng.integers(len(vs)))]), len(vs)

    def targets(self, M, v):
        """Neighbours a that v may narrow-merge into (link condition, narrow shape, ceiling)."""
        out = []
        for a in _nbr(M, v):
            a = int(a)
            if link_condition(M.S, v, a) and narrow_ok(M.S, v, a):
                nr, na = merge_plan(M.S, v, a, B_A)
                if nr >= 0 and _ok(M, nr, na, gone=v):
                    out.append(a)
        return out

    def _split_site(self, M, rng):
        x, V = self._rand_vertex(M, rng)
        nb = _nbr(M, x)
        u = int(nb[int(rng.integers(len(nb)))])
        nr, na = split_plan(M.S, x, u, M.next_free_vertex(), B_A)
        if nr < 0 or not _ok(M, nr, na):
            return None
        return ("S", x, u), int(valence(M.S, x, u)), 1.0 / len(nb)

    def _merge_site(self, M, rng):
        v, V = self._rand_vertex(M, rng)
        A = self.targets(M, v)
        if not A:
            return None
        a = A[int(rng.integers(len(A)))]
        nb = _nbr(M, v)
        Na = set(int(w) for w in _nbr(M, a))
        u = [int(w) for w in nb if int(w) != a and int(w) not in Na][0]
        return ("M", v, a, u), int(valence(M.S, v, a)), 1.0 / len(A)

    def _f23_site(self, M, rng):
        S = M.S
        tid = int(S.t_items[int(rng.integers(S.ctr[C_T]))])
        f = int(rng.integers(4))
        nr, na = flip23_plan(S, tid, f, B_A)
        if nr < 0 or not _ok(M, nr, na):
            return None
        d = int(S.tv[tid, f])
        ring = frozenset(int(S.tv[tid, j]) for j in range(4) if j != f)
        e = [int(w) for w in S.buf_add[B_A, :2] if int(w) != d][0]
        return ("F23", ring, frozenset((d, e))), 1.0 / (2.0 * S.ctr[C_T])

    def _f32_site(self, M, rng):
        from p3_ops import C_V3
        S = M.S
        n3 = int(S.ctr[C_V3])
        if n3 == 0:
            return None
        slot = int(S.e3_items[int(rng.integers(n3))])
        nr, na = flip32_plan(S, slot, B_A)
        if nr < 0 or not _ok(M, nr, na):
            return None
        d, e = int(S.e_a[slot]), int(S.e_b[slot])
        return ("F32", frozenset((d, e)), frozenset(_edge_ring(M, d, e))), 1.0 / n3

    def propose(self, M, rng):
        """Returns (parts, q_fwd) with q_fwd the site-proposal probability up to factors shared with the reverse
        (1/4 for the type, 1/V per chosen event)."""
        typ = int(rng.integers(4))
        if typ == 1:
            a = self._f23_site(M, rng)
            b = self._f32_site(M, rng)
            if a is None or b is None:
                return self._n("sites")
            return [a[0], b[0]], a[1] * b[1]
        s = self._split_site(M, rng)
        m = self._merge_site(M, rng)
        if s is None or m is None:
            return self._n("sites")
        (sk, k1, qs), (mk, k2, qm) = s, m
        if typ == 0:
            if k1 != k2:
                return self._n("sizes")
            return [sk, mk], qs * qm
        if typ == 2:
            if k2 != k1 + 1:
                return self._n("sizes")
            f = self._f23_site(M, rng)
            if f is None:
                return self._n("sites")
            return [sk, mk, f[0]], qs * qm * f[1]
        if k1 != k2 + 1:
            return self._n("sizes")
        f = self._f32_site(M, rng)
        if f is None:
            return self._n("sites")
        return [sk, mk, f[0]], qs * qm * f[1]

    def reverse_q(self, M, keys):
        """Proposal probability of the reverse bundle in the new slice M (same shared factors)."""
        from p3_ops import C_V3
        S = M.S
        q = 1.0
        for k in keys:
            if k[0] == "S":                        # reverse: merge the child y into x
                q *= 1.0 / max(len(self.targets(M, k[3])), 1)
            elif k[0] == "M":                      # reverse: split a along u, recreating v
                q *= 1.0 / int(S.v_nl[k[2]])
            elif k[0] == "F23":                    # reverse: 3-2 on the new edge, from the valence-3 list
                q *= 1.0 / max(int(S.ctr[C_V3]), 1)
            else:                                  # reverse: 2-3 on the new triangle
                q *= 1.0 / (2.0 * S.ctr[C_T])
        return q

    def _n(self, why):
        self.stats[why] = self.stats.get(why, 0) + 1
        return None

    # ---- supports, validity, application -----------------------------------------------------
    def support(self, M, key):
        k = key[0]
        if k == "S":
            _, x, u, y = key
            return frozenset({x, u, y} | _edge_ring(M, x, u))
        if k == "M":
            _, v, a, u = key
            return frozenset({v, a, u} | _edge_ring(M, v, a))
        if k == "F23":
            return frozenset(key[1] | key[2])
        return frozenset(key[1] | key[2])

    def _tet_with(self, M, verts):
        S = M.S
        v0 = next(iter(verts))
        s = S.v_ts[v0]
        for i in range(S.v_tl[v0]):
            t = S.at_data[s + i]
            if verts <= set(int(w) for w in S.tv[t]):
                return int(t)
        return -1

    def valid(self, M, key):
        S = M.S
        k = key[0]
        if k == "S":
            _, x, u, y = key
            if not (self.has(M, x) and self.has(M, u)) or self.has(M, y) or valence(S, x, u) == 0:
                return False
            nr, na = split_plan(S, x, u, y, B_A)
            return nr >= 0 and _ok(M, nr, na)
        if k == "M":
            _, v, a, u = key
            if not (self.has(M, v) and self.has(M, a) and self.has(M, u)) or valence(S, v, a) == 0:
                return False
            if not link_condition(S, v, a) or not narrow_ok(S, v, a):
                return False
            nb = set(int(w) for w in _nbr(M, v))
            Na = set(int(w) for w in _nbr(M, a))
            if [w for w in nb if w != a and w not in Na] != [u]:
                return False
            nr, na = merge_plan(S, v, a, B_A)
            return nr >= 0 and _ok(M, nr, na, gone=v)
        if k == "F23":
            ring, apex = key[1], key[2]
            d, e = tuple(apex)
            if valence(S, d, e) != 0:
                return False
            t1 = self._tet_with(M, set(ring) | {d})
            t2 = self._tet_with(M, set(ring) | {e})
            if t1 < 0 or t2 < 0:
                return False
            f = [j for j in range(4) if int(S.tv[t1, j]) == d][0]
            nr, na = flip23_plan(S, t1, f, B_A)
            return nr >= 0 and _ok(M, nr, na)
        d, e = tuple(key[1])
        if valence(S, d, e) != 3 or _edge_ring(M, d, e) != set(key[2]):
            return False
        nr, na = flip32_plan(S, edge_slot(S, d, e), B_A)
        return nr >= 0 and _ok(M, nr, na)

    def swap_valid(self, M, key):
        if key[0] == "S":
            return True
        _, v, a, u = key
        if not link_condition(M.S, v, a) or not narrow_ok(M.S, v, a):
            return False
        nr, na = merge_plan(M.S, v, a, B_A)
        return nr >= 0 and _ok(M, nr, na, gone=v)

    def apply(self, M, key):
        S = M.S
        k = key[0]
        if k == "S":
            _, x, u, y = key
            if vert_new_at(S, y) != y:
                raise RuntimeError("label %d not free" % y)
            nr, na = split_plan(S, x, u, y, B_A)
            apply_plan(S, B_A, nr, na)
            S.b[y] = S.b[x]
            S.phi[y] = S.phi[x]
            S.omega[y] = S.omega[x]
        elif k == "M":
            _, v, a, u = key
            nr, na = merge_plan(S, v, a, B_A)
            apply_plan(S, B_A, nr, na)
            vert_free(S, v)
        elif k == "F23":
            ring, apex = key[1], key[2]
            d = next(iter(apex))
            t1 = self._tet_with(M, set(ring) | {d})
            f = [j for j in range(4) if int(S.tv[t1, j]) == d][0]
            nr, na = flip23_plan(S, t1, f, B_A)
            apply_plan(S, B_A, nr, na)
        else:
            d, e = tuple(key[1])
            nr, na = flip32_plan(S, edge_slot(S, d, e), B_A)
            apply_plan(S, B_A, nr, na)
        if S.ctr[C_OVER]:
            raise RuntimeError("capacity overflow %d" % S.ctr[C_OVER])
