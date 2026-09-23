"""The port (E2; note 2 C6; D3): attempt 7's C3c-C3f slice, moves, tick and wrapper.

Same model, same knobs, same moves, same gates, same acceptance rule as
`../../ED_Attempt_07/model/c3f.py`. Only the representation differs (IMPLEMENTATION_NOTES.md),
and with it the set-iteration order, so the random path is not attempt 7's - see note 2's C5
and the tier 1-3 ladder. Containers and gates are in `p3_ops.py`.
"""
import time
import numpy as np
import scipy.sparse as sp
from numba import njit, int64, objmode
from p3_core import (FLAT_VALENCE, SIGMA, K, K_RESPONSE, FLAT_LINKS_PER_EVENT, CEILING,
                     NCLASS, MINCLASS, rng_seed, rng_float, rng_below, rng_geometric, rng_shuffle,
                     ekey)
from p3_ops import (State, FIELDS, NCTR, C_T, C_V, C_E, C_V3, C_ATTOP, C_ANTOP, C_VFREE, C_TFREE,
                    C_EFREE, C_SV, C_SE, C_SF, C_SD, C_STM, C_OVER, C_TTOP, C_VTOP, C_ETOP, C_ERR, REGION,
                    REASON, _kor, _kget, _kfind_pub, tri_key, _lst_alloc, edge_slot, valence, tet_add,
                    tet_remove, vert_new, vert_free, edge_delta, n3_after, delta_S, allowed,
                    gate_and_cost, apply_plan)

B_A, B_B, B_C = 0, REGION, 2 * REGION          # scratch plan regions


# ------------------------------------------------------------------ the link condition
@njit(cache=True)
def link_condition(S, v, a):
    """Lk(v) & Lk(a) == Lk(va), for vertices, edges and triangles (Dey-Edelsbrunner)."""
    st_t = S.ctr[C_STM] + 1
    S.ctr[C_STM] = st_t
    st_e = S.ctr[C_SE] + 1
    S.ctr[C_SE] = st_e
    st_v = S.ctr[C_SV] + 1
    S.ctr[C_SV] = st_v
    st_f = S.ctr[C_SF] + 1
    S.ctr[C_SF] = st_f
    me = S.ke_key.shape[0] - 1
    mv = S.kv_key.shape[0] - 1
    mf = S.kf_key.shape[0] - 1
    sa = S.v_ts[a]
    for i in range(S.v_tl[a]):
        S.tmark[S.at_data[sa + i]] = st_t
    sv = S.v_ts[v]
    n_both = 0
    n_lke = 0
    n_lkv = 0
    for i in range(S.v_tl[v]):
        t = S.at_data[sv + i]
        if S.tmark[t] != st_t:
            continue
        n_both += 1
        p = -1
        q = -1
        for j in range(4):
            w = S.tv[t, j]
            if w != v and w != a:
                if p < 0:
                    p = w
                else:
                    q = w
        if _kor(S.ke_key, S.ke_val, S.ke_st, me, ekey(p, q), 1, st_e):
            n_lke += 1
        if _kor(S.kv_key, S.kv_val, S.kv_st, mv, int64(p), 1, st_v):
            n_lkv += 1
        if _kor(S.kv_key, S.kv_val, S.kv_st, mv, int64(q), 1, st_v):
            n_lkv += 1
    if n_both == 0:
        return False
    n_common = 0
    sn = S.v_ns[v]
    for i in range(S.v_nl[v]):
        w = S.an_data[sn + i]
        if w == a:
            continue
        if edge_slot(S, w, a) < 0:
            continue
        n_common += 1
        if (_kget(S.kv_key, S.kv_val, S.kv_st, mv, int64(w), st_v) & 1) == 0:
            return False
    if n_common != n_lkv:
        return False
    for i in range(S.v_tl[v]):
        t = S.at_data[sv + i]
        if S.tmark[t] == st_t:
            continue
        p0 = -1
        p1 = -1
        p2 = -1
        for j in range(4):
            w = S.tv[t, j]
            if w == v:
                continue
            if p0 < 0:
                p0 = w
            elif p1 < 0:
                p1 = w
            else:
                p2 = w
        _kor(S.ke_key, S.ke_val, S.ke_st, me, ekey(p0, p1), 2, st_e)
        _kor(S.ke_key, S.ke_val, S.ke_st, me, ekey(p0, p2), 2, st_e)
        _kor(S.ke_key, S.ke_val, S.ke_st, me, ekey(p1, p2), 2, st_e)
        _kor(S.kf_key, S.kf_val, S.kf_st, mf, tri_key(p0, p1, p2), 1, st_f)
    n_inter = 0
    for i in range(S.v_tl[a]):
        t = S.at_data[sa + i]
        has_v = False
        p0 = -1
        p1 = -1
        p2 = -1
        for j in range(4):
            w = S.tv[t, j]
            if w == v:
                has_v = True
            if w == a:
                continue
            if p0 < 0:
                p0 = w
            elif p1 < 0:
                p1 = w
            else:
                p2 = w
        if has_v:
            continue
        if (_kget(S.kf_key, S.kf_val, S.kf_st, mf, tri_key(p0, p1, p2), st_f) & 1) != 0:
            return False
        for c in range(3):
            if c == 0:
                key = ekey(p0, p1)
            elif c == 1:
                key = ekey(p0, p2)
            else:
                key = ekey(p1, p2)
            val = _kget(S.ke_key, S.ke_val, S.ke_st, me, key, st_e)
            if (val & 2) != 0 and (val & 4) == 0:
                _kor(S.ke_key, S.ke_val, S.ke_st, me, key, 4, st_e)
                n_inter += 1
                if (val & 1) == 0:
                    return False
    return n_inter == n_lke


# ------------------------------------------------------------------ plans
@njit(cache=True)
def merge_plan(S, v, a, base):
    st_t = S.ctr[C_STM] + 1
    S.ctr[C_STM] = st_t
    sa = S.v_ts[a]
    for i in range(S.v_tl[a]):
        S.tmark[S.at_data[sa + i]] = st_t
    sv = S.v_ts[v]
    nrem = 0
    nadd = 0
    if S.v_tl[v] >= REGION:
        S.ctr[C_OVER] = 6
        return -1, -1
    for i in range(S.v_tl[v]):
        t = S.at_data[sv + i]
        S.buf_rem[base + nrem] = t
        nrem += 1
        if S.tmark[t] == st_t:
            continue
        for j in range(4):
            w = S.tv[t, j]
            S.buf_add[base + nadd, j] = a if w == v else w
        nadd += 1
    return nrem, nadd


@njit(cache=True)
def split_plan(S, x, u, y, base):
    st_t = S.ctr[C_STM] + 1
    S.ctr[C_STM] = st_t
    su = S.v_ts[u]
    for i in range(S.v_tl[u]):
        S.tmark[S.at_data[su + i]] = st_t
    sx = S.v_ts[x]
    nrem = 0
    nadd = 0
    for i in range(S.v_tl[x]):
        t = S.at_data[sx + i]
        if S.tmark[t] != st_t:
            continue
        p = -1
        q = -1
        for j in range(4):
            w = S.tv[t, j]
            if w != x and w != u:
                if p < 0:
                    p = w
                else:
                    q = w
        if nrem >= REGION or nadd + 2 > REGION:
            S.ctr[C_OVER] = 6
            return -1, -1
        S.buf_rem[base + nrem] = t
        nrem += 1
        S.buf_add[base + nadd, 0] = y
        S.buf_add[base + nadd, 1] = u
        S.buf_add[base + nadd, 2] = p
        S.buf_add[base + nadd, 3] = q
        nadd += 1
        S.buf_add[base + nadd, 0] = x
        S.buf_add[base + nadd, 1] = y
        S.buf_add[base + nadd, 2] = p
        S.buf_add[base + nadd, 3] = q
        nadd += 1
    return nrem, nadd


@njit(cache=True)
def flip23_plan(S, tid, face_index, base):
    d = S.tv[tid, face_index]
    t0 = -1
    t1 = -1
    t2 = -1
    for j in range(4):
        if j == face_index:
            continue
        w = S.tv[tid, j]
        if t0 < 0:
            t0 = w
        elif t1 < 0:
            t1 = w
        else:
            t2 = w
    other = -1
    s0 = S.v_ts[t0]
    for i in range(S.v_tl[t0]):
        t = S.at_data[s0 + i]
        if t == tid:
            continue
        c = 0
        for j in range(4):
            w = S.tv[t, j]
            if w == t0 or w == t1 or w == t2:
                c += 1
        if c == 3:
            if other >= 0:
                return -1, -1
            other = t
    if other < 0:
        return -1, -1
    e = -1
    for j in range(4):
        w = S.tv[other, j]
        if w != t0 and w != t1 and w != t2:
            e = w
    if e == d or edge_slot(S, d, e) >= 0:
        return -1, -1
    S.buf_rem[base] = tid
    S.buf_rem[base + 1] = other
    S.buf_add[base, 0] = d
    S.buf_add[base, 1] = e
    S.buf_add[base, 2] = t0
    S.buf_add[base, 3] = t1
    S.buf_add[base + 1, 0] = d
    S.buf_add[base + 1, 1] = e
    S.buf_add[base + 1, 2] = t1
    S.buf_add[base + 1, 3] = t2
    S.buf_add[base + 2, 0] = d
    S.buf_add[base + 2, 1] = e
    S.buf_add[base + 2, 2] = t0
    S.buf_add[base + 2, 3] = t2
    return 2, 3


@njit(cache=True)
def flip32_plan(S, slot, base):
    d = S.e_a[slot]
    e = S.e_b[slot]
    st_t = S.ctr[C_STM] + 1
    S.ctr[C_STM] = st_t
    se = S.v_ts[e]
    for i in range(S.v_tl[e]):
        S.tmark[S.at_data[se + i]] = st_t
    sd = S.v_ts[d]
    n = 0
    r0 = -1
    r1 = -1
    r2 = -1
    for i in range(S.v_tl[d]):
        t = S.at_data[sd + i]
        if S.tmark[t] != st_t:
            continue
        if n >= 3:
            return -1, -1
        S.buf_rem[base + n] = t
        n += 1
        for j in range(4):
            w = S.tv[t, j]
            if w == d or w == e:
                continue
            if w == r0 or w == r1 or w == r2:
                continue
            if r0 < 0:
                r0 = w
            elif r1 < 0:
                r1 = w
            elif r2 < 0:
                r2 = w
            else:
                return -1, -1
    if n != 3 or r2 < 0:
        return -1, -1
    a = r0
    b = r1
    c = r2
    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a
    s0 = S.v_ts[a]
    for i in range(S.v_tl[a]):
        t = S.at_data[s0 + i]
        k = 0
        for j in range(4):
            w = S.tv[t, j]
            if w == a or w == b or w == c:
                k += 1
        if k == 3:
            return -1, -1
    S.buf_add[base, 0] = a
    S.buf_add[base, 1] = b
    S.buf_add[base, 2] = c
    S.buf_add[base, 3] = d
    S.buf_add[base + 1, 0] = a
    S.buf_add[base + 1, 1] = b
    S.buf_add[base + 1, 2] = c
    S.buf_add[base + 1, 3] = e
    return 3, 2


@njit(cache=True)
def paired_flip_plan(S, rs):
    """One 2-3 and one 3-2 at disjoint places, concatenated into region B_C. (nrem, nadd) or (-1,-1)."""
    if S.ctr[C_T] == 0 or S.ctr[C_V3] == 0:
        return -1, -1
    tid = S.t_items[rng_below(rs, S.ctr[C_T])]
    fa = rng_below(rs, 4)
    ra, aa = flip23_plan(S, tid, fa, B_A)
    if ra < 0:
        return -1, -1
    if S.ctr[C_V3] == 0:
        return -1, -1
    slot = S.e3_items[rng_below(rs, S.ctr[C_V3])]
    rb, ab = flip32_plan(S, slot, B_B)
    if rb < 0:
        return -1, -1
    for i in range(ra):
        for j in range(rb):
            if S.buf_rem[B_A + i] == S.buf_rem[B_B + j]:
                return -1, -1
    # the 2-3 must not create the triangle the 3-2 needs absent
    g0 = S.buf_add[B_B, 0]
    g1 = S.buf_add[B_B, 1]
    g2 = S.buf_add[B_B, 2]
    for i in range(aa):
        k = 0
        for j in range(4):
            w = S.buf_add[B_A + i, j]
            if w == g0 or w == g1 or w == g2:
                k += 1
        if k == 3:
            return -1, -1
    for i in range(ra):
        S.buf_rem[B_C + i] = S.buf_rem[B_A + i]
    for i in range(rb):
        S.buf_rem[B_C + ra + i] = S.buf_rem[B_B + i]
    for i in range(aa):
        for j in range(4):
            S.buf_add[B_C + i, j] = S.buf_add[B_A + i, j]
    for i in range(ab):
        for j in range(4):
            S.buf_add[B_C + aa + i, j] = S.buf_add[B_B + i, j]
    return ra + rb, aa + ab


# ------------------------------------------------------------------ structure checks
@njit(cache=True)
def check_codes(S, out):
    """Structure checks, same content as c3c.Slice3.check(). Codes into `out`; returns how many."""
    n = 0
    V = S.ctr[C_V]
    E = S.ctr[C_E]
    T = S.ctr[C_T]
    # every triangle in exactly two tetrahedra
    bad_face = 0
    for ii in range(T):
        t = S.t_items[ii]
        for f in range(4):
            p0 = -1
            p1 = -1
            p2 = -1
            for j in range(4):
                if j == f:
                    continue
                w = S.tv[t, j]
                if p0 < 0:
                    p0 = w
                elif p1 < 0:
                    p1 = w
                else:
                    p2 = w
            best, bl = p0, S.v_tl[p0]
            if S.v_tl[p1] < bl:
                best, bl = p1, S.v_tl[p1]
            if S.v_tl[p2] < bl:
                best, bl = p2, S.v_tl[p2]
            s = S.v_ts[best]
            c = 0
            for i in range(bl):
                tt = S.at_data[s + i]
                k = 0
                for j in range(4):
                    w = S.tv[tt, j]
                    if w == p0 or w == p1 or w == p2:
                        k += 1
                if k == 3:
                    c += 1
            if c != 2:
                bad_face = 1
                break
        if bad_face == 1:
            break
    if bad_face == 1:
        out[n] = 1
        n += 1
    # V - E + F - T = 0 with F = 2T
    if V - E + 2 * T - T != 0:
        out[n] = 2
        n += 1
    cap = 4096
    CK = 65536
    ck_key = np.zeros(CK, dtype=np.int64)
    ck_val = np.zeros(CK, dtype=np.int32)
    ck_st = np.zeros(CK, dtype=np.int64)
    cv_key = np.zeros(CK, dtype=np.int64)
    cv_val = np.zeros(CK, dtype=np.int32)
    cv_st = np.zeros(CK, dtype=np.int64)
    stamp_e = 0
    stamp_v = 0
    ecount = np.empty(3 * cap, dtype=np.int32)
    etri = np.empty((3 * cap, 2), dtype=np.int32)
    par = np.empty(cap, dtype=np.int32)
    tri = np.empty((cap, 3), dtype=np.int32)
    for v in range(S.v_alive.shape[0]):
        if S.v_alive[v] == 0:
            continue
        ntris = S.v_tl[v]
        if ntris == 0:
            out[n] = 3
            n += 1
            out[n] = v
            n += 1
            return n
        if ntris > cap:
            out[n] = 7
            n += 1
            return n
        s = S.v_ts[v]
        for i in range(ntris):
            t = S.at_data[s + i]
            p0 = -1
            p1 = -1
            p2 = -1
            for j in range(4):
                w = S.tv[t, j]
                if w == v:
                    continue
                if p0 < 0:
                    p0 = w
                elif p1 < 0:
                    p1 = w
                else:
                    p2 = w
            tri[i, 0] = p0
            tri[i, 1] = p1
            tri[i, 2] = p2
            par[i] = i
        stamp_e += 1
        stamp_v += 1
        st_e = stamp_e
        st_v = stamp_v
        me = CK - 1
        mv = CK - 1
        le = 0
        lv = 0
        for i in range(ntris):
            for c in range(3):
                if c == 0:
                    key = ekey(tri[i, 0], tri[i, 1])
                elif c == 1:
                    key = ekey(tri[i, 0], tri[i, 2])
                else:
                    key = ekey(tri[i, 1], tri[i, 2])
                idx, found = _kfind_pub(ck_key, ck_st, me, key, st_e)
                if not found:
                    ck_st[idx] = st_e
                    ck_key[idx] = key
                    ck_val[idx] = le
                    ecount[le] = 0
                    etri[le, 0] = -1
                    etri[le, 1] = -1
                    le += 1
                e = ck_val[idx]
                if ecount[e] >= 2:
                    out[n] = 4
                    n += 1
                    out[n] = v
                    n += 1
                    return n
                etri[e, ecount[e]] = i
                ecount[e] += 1
            for c in range(3):
                if _kor(cv_key, cv_val, cv_st, mv, int64(tri[i, c]), 1, st_v):
                    lv += 1
        for e in range(le):
            if ecount[e] != 2:
                out[n] = 4
                n += 1
                out[n] = v
                n += 1
                return n
            ra = etri[e, 0]
            while par[ra] != ra:
                par[ra] = par[par[ra]]
                ra = par[ra]
            rb = etri[e, 1]
            while par[rb] != rb:
                par[rb] = par[par[rb]]
                rb = par[rb]
            if ra != rb:
                par[ra] = rb
        roots = 0
        for i in range(ntris):
            if par[i] == i:
                roots += 1
        if lv - le + ntris != 2 or roots != 1:
            out[n] = 5
            n += 1
            out[n] = v
            n += 1
            return n
        if S.v_nl[v] != lv:
            out[n] = 6
            n += 1
            out[n] = v
            n += 1
            return n
        sn = S.v_ns[v]
        for i in range(S.v_nl[v]):
            if (_kget(cv_key, cv_val, cv_st, mv, int64(S.an_data[sn + i]), st_v) & 1) == 0:
                out[n] = 6
                n += 1
                out[n] = v
                n += 1
                return n
    return n


# ------------------------------------------------------------------ the torus start
@njit(cache=True)
def build_torus(S, n):
    perms = np.array([[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]], dtype=np.int32)
    for v in range(n ** 3):
        vert_new(S)
    cur = np.empty(3, dtype=np.int32)
    verts = np.empty(4, dtype=np.int32)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for pi in range(6):
                    cur[0], cur[1], cur[2] = i, j, k
                    verts[0] = (cur[0] % n) * n * n + (cur[1] % n) * n + (cur[2] % n)
                    for a in range(3):
                        ax = perms[pi, a]
                        cur[ax] += 1
                        verts[a + 1] = (cur[0] % n) * n * n + (cur[1] % n) * n + (cur[2] % n)
                    tet_add(S, verts[0], verts[1], verts[2], verts[3])


# ------------------------------------------------------------------ one growth tick
@njit(cache=True, inline="always")
def _wchoice(rs, dS, m):
    if m == 1:
        return 0
    lo = dS[0]
    for i in range(1, m):
        if dS[i] < lo:
            lo = dS[i]
    tot = 0.0
    for i in range(m):
        x = -(dS[i] - lo)
        if x < -700.0:
            x = -700.0
        elif x > 0.0:
            x = 0.0
        tot += np.exp(x)
    u = rng_float(rs) * tot
    acc = 0.0
    for i in range(m):
        x = -(dS[i] - lo)
        if x < -700.0:
            x = -700.0
        elif x > 0.0:
            x = 0.0
        acc += np.exp(x)
        if u <= acc:
            return i
    return m - 1



@njit(cache=True)
def sync_step(S):
    """C2b's tick-field update: phi += omega + (K/deg) * sum_j tanh(phi_j - phi_i).

    Pulled out of `tick` so it can be compared directly with attempt 7's numpy form; the port's
    tier 1 and tier 2 cover the moves and the gates, and left this untested.
    """
    pull = np.zeros(S.v_alive.shape[0], dtype=np.float64)
    for slot in range(S.ctr[C_ETOP]):
        if S.e_val[slot] <= 0:
            continue
        a = S.e_a[slot]
        b = S.e_b[slot]
        t = np.tanh(S.phi[b] - S.phi[a])
        pull[a] += t
        pull[b] -= t
    for v in range(S.v_alive.shape[0]):
        if S.v_alive[v] == 1:
            if S.v_nl[v] == 0:
                S.ctr[C_ERR] = v + 1
                continue
            S.phi[v] = S.phi[v] + S.omega[v] + (K / S.v_nl[v]) * pull[v]


@njit(cache=True)
def tick(S, rs, alpha, lam, pool, s_max, cap, out, kids_out, abs_out, tm):
    """One growth tick, following c3f.tick. Returns the new pool; counts land in `out`.

    `tm` collects phase timestamps (offspring, merges, splits, flips, sync), so the cost of a tick
    can always be split without editing the model - the carry-forward's "instrument every gate".
    """
    with objmode(t0="f8"):
        t0 = time.perf_counter()
    none = alpha == 0.0 and lam == 0.0
    NV = S.v_alive.shape[0]
    ids = np.empty(S.ctr[C_V], dtype=np.int32)
    m = 0
    for v in range(NV):
        if S.v_alive[v] == 1:
            ids[m] = v
            m += 1
    cntv = np.zeros(NV, dtype=np.int32)
    for i in range(m):
        v = ids[i]
        mu = 1.0 + K_RESPONSE * (S.b[v] - 1.0)
        if mu < 0.0:
            mu = 0.0
        cntv[v] = rng_geometric(rs, 1.0 / (1.0 + mu)) - 1
    with objmode(t1="f8"):
        t1 = time.perf_counter()
    forced = 0
    merges = 0
    splits = 0
    f_acc = 0
    ref_b = 0
    ref_c = 0
    ref_s = 0
    split_refused = 0
    n_kids = 0
    n_abs = 0

    order = np.empty(m, dtype=np.int32)
    k = 0
    for i in range(m):
        if cntv[ids[i]] == 0:
            order[k] = ids[i]
            k += 1
    rng_shuffle(rs, order, k)
    cand = np.empty(256, dtype=np.int32)
    cb = np.empty(256, dtype=np.int32)
    cd = np.empty(256, dtype=np.int32)
    dS = np.empty(256, dtype=np.float64)
    for oi in range(k):
        v = order[oi]
        nc = 0
        sn = S.v_ns[v]
        for i in range(S.v_nl[v]):
            a = S.an_data[sn + i]
            if not link_condition(S, v, a):
                continue
            nr, na = merge_plan(S, v, a, B_A)
            if nr < 0:
                continue
            ok, born, dies, why, d = gate_and_cost(S, B_A, nr, na, pool, s_max, v, cap, alpha, lam)
            if not ok:
                if why == 1:
                    ref_b += 1
                elif why == 2:
                    ref_c += 1
                else:
                    ref_s += 1
                continue
            if nc < 256:
                cand[nc] = a
                cb[nc] = born
                cd[nc] = dies
                dS[nc] = d
                nc += 1
        if nc == 0:
            cntv[v] = 1
            forced += 1
            continue
        ch = rng_below(rs, nc) if none else _wchoice(rs, dS, nc)
        a = cand[ch]
        born = cb[ch]
        dies = cd[ch]
        nr, na = merge_plan(S, v, a, B_A)
        apply_plan(S, B_A, nr, na)
        vert_free(S, v)
        pool += dies - born
        S.b[a] += S.b[v]
        abs_out[n_abs, 0] = v
        abs_out[n_abs, 1] = a
        n_abs += 1
        merges += 1

    with objmode(t2="f8"):
        t2 = time.perf_counter()
    k = 0
    for i in range(m):
        v = ids[i]
        if S.v_alive[v] == 1 and cntv[v] >= 1:
            order[k] = v
            k += 1
    rng_shuffle(rs, order, k)
    nbrbuf = np.empty(256, dtype=np.int32)
    for oi in range(k):
        v = order[oi]
        nkid = 1
        x = v
        kids_out[n_kids, 0] = v
        kids_out[n_kids, 1] = v
        n_kids += 1
        first_kid = n_kids - 1
        for _ in range(cntv[v] - 1):
            y = S.v_free[S.ctr[C_VFREE] - 1] if S.ctr[C_VFREE] > 0 else S.ctr[C_VTOP]
            nopt = 0
            nn = S.v_nl[x]
            sn = S.v_ns[x]
            for i in range(nn):
                nbrbuf[i] = S.an_data[sn + i]
            for i in range(1, nn):                       # sorted(M.nbrs[x])
                tmp = nbrbuf[i]
                j = i - 1
                while j >= 0 and nbrbuf[j] > tmp:
                    nbrbuf[j + 1] = nbrbuf[j]
                    j -= 1
                nbrbuf[j + 1] = tmp
            for i in range(nn):
                u = nbrbuf[i]
                nr, na = split_plan(S, x, u, y, B_A)
                if nr < 0:
                    continue
                ok, born, dies, why, d = gate_and_cost(S, B_A, nr, na, pool, s_max, -1, cap, alpha, lam)
                if not ok:
                    if why == 1:
                        ref_b += 1
                    elif why == 2:
                        ref_c += 1
                    else:
                        ref_s += 1
                    continue
                if nopt < 256:
                    cand[nopt] = u
                    cb[nopt] = born
                    cd[nopt] = dies
                    dS[nopt] = d
                    nopt += 1
            if nopt == 0:
                split_refused += 1
                break
            ch = rng_below(rs, nopt) if none else _wchoice(rs, dS, nopt)
            u = cand[ch]
            born = cb[ch]
            dies = cd[ch]
            y2 = vert_new(S)
            nr, na = split_plan(S, x, u, y2, B_A)
            apply_plan(S, B_A, nr, na)
            pool += dies - born
            S.phi[y2] = S.phi[x]
            S.omega[y2] = S.omega[x]
            kids_out[n_kids, 0] = v
            kids_out[n_kids, 1] = y2
            n_kids += 1
            nkid += 1
            x = y2
            splits += 1
        share = S.b[v] / nkid
        for i in range(nkid):
            S.b[kids_out[first_kid + i, 1]] = share

    with objmode(t3="f8"):
        t3 = time.perf_counter()
    links_before = S.ctr[C_E]
    sweeps = S.ctr[C_V] // 2
    for _ in range(sweeps):
        nr, na = paired_flip_plan(S, rs)
        if nr < 0:
            continue
        ok, born, dies, why, d = gate_and_cost(S, B_C, nr, na, pool, s_max, -1, cap, alpha, lam)
        if not ok:
            if why == 1:
                ref_b += 1
            elif why == 2:
                ref_c += 1
            else:
                ref_s += 1
            continue
        n3n = S.ctr[C_V3]
        n3a = n3_after(S, B_C, nr, na)
        if n3a < 1:
            n3a = 1
        corr = n3n / n3a
        if d > -700.0:
            acc = corr * np.exp(-d)
        else:
            acc = 1e308
        if acc >= 1.0 or rng_float(rs) < acc:
            apply_plan(S, B_C, nr, na)
            pool += dies - born
            f_acc += 1

    with objmode(t4="f8"):
        t4 = time.perf_counter()
    sync_step(S)

    with objmode(t5="f8"):
        t5 = time.perf_counter()
    tm[0] = t1 - t0
    tm[1] = t2 - t1
    tm[2] = t3 - t2
    tm[3] = t4 - t3
    tm[4] = t5 - t4
    out[0] = forced
    out[1] = merges
    out[2] = splits
    out[3] = f_acc
    out[4] = S.ctr[C_V]
    out[5] = ref_b
    out[6] = ref_c
    out[7] = ref_s
    out[8] = split_refused
    out[9] = S.ctr[C_E]
    out[10] = pool
    out[11] = 1 if S.ctr[C_E] == links_before else 0
    out[12] = n_kids
    out[13] = n_abs
    return pool



@njit(cache=True)
def flip_randomize(S, rs, sweeps):
    """Calibration RC: uniform-measure 2-3/3-2 flips at a fixed vertex set, no cost, no budget gate.

    Ports c3c.flip_randomize. Deliberately ignores the link budget, which is why RC reaches the
    crumpled phase that budgeted growth cannot (C22).
    """
    acc = 0
    total = sweeps * S.ctr[C_V]
    for _ in range(total):
        if rng_float(rs) < 0.5:
            if S.ctr[C_T] == 0:
                continue
            tid = S.t_items[rng_below(rs, S.ctr[C_T])]
            nr, na = flip23_plan(S, tid, rng_below(rs, 4), B_A)
            if nr < 0:
                continue
            n3a = n3_after(S, B_A, nr, na)
            if n3a < 1:
                n3a = 1
            corr = 2.0 * S.ctr[C_T] / n3a
        else:
            if S.ctr[C_V3] == 0:
                continue
            slot = S.e3_items[rng_below(rs, S.ctr[C_V3])]
            nr, na = flip32_plan(S, slot, B_A)
            if nr < 0:
                continue
            corr = S.ctr[C_V3] / (2.0 * (S.ctr[C_T] - 1))
        if corr >= 1.0 or rng_float(rs) < corr:
            apply_plan(S, B_A, nr, na)
            acc += 1
    return acc


CHECK_MSG = {1: "a triangle not in exactly two tetrahedra", 2: "V-E+F-T nonzero", 3: "vertex in no tetrahedron",
             4: "link not a closed surface", 5: "link not a sphere", 6: "neighbour set inconsistent",
             7: "link too large for the check buffer"}


def _pow2(x):
    n = 1
    while n < x:
        n *= 2
    return n


class Slice3P:
    """Array-backed Slice3. Same start, same moves, same gates as c3c/c3f."""

    def __init__(self, n, v_cap=None, t_cap=None, e_cap=None):
        V0 = n ** 3
        NV = v_cap or max(4096, 3 * V0)
        NT = t_cap or max(8192, 12 * V0)
        NE = e_cap or max(8192, 10 * V0)
        SC = 2048          # scratch tables: small enough to stay in cache
        arena_t = 128 * V0 + 65536
        arena_n = 96 * V0 + 65536
        S = State(
            ctr=np.zeros(NCTR, dtype=np.int64),
            v_alive=np.zeros(NV, dtype=np.uint8),
            v_ts=np.zeros(NV, dtype=np.int32), v_tl=np.zeros(NV, dtype=np.int32),
            v_tc=np.zeros(NV, dtype=np.int8),
            v_ns=np.zeros(NV, dtype=np.int32), v_nl=np.zeros(NV, dtype=np.int32),
            v_nc=np.zeros(NV, dtype=np.int8),
            b=np.zeros(NV), omega=np.zeros(NV), phi=np.zeros(NV),
            v_free=np.zeros(NV, dtype=np.int32),
            tv=np.zeros((NT, 4), dtype=np.int32), te=np.full((NT, 6), -1, dtype=np.int32),
            t_alive=np.zeros(NT, dtype=np.uint8),
            t_items=np.zeros(NT, dtype=np.int32), t_pos=np.zeros(NT, dtype=np.int32),
            t_free=np.zeros(NT, dtype=np.int32), tmark=np.zeros(NT, dtype=np.int64),
            e_a=np.zeros(NE, dtype=np.int32), e_b=np.zeros(NE, dtype=np.int32),
            e_val=np.zeros(NE, dtype=np.int32), e_free=np.zeros(NE, dtype=np.int32),
            e3_items=np.zeros(NE, dtype=np.int32), e3_pos=np.full(NE, -1, dtype=np.int32),
            ek_key=np.zeros(_pow2(4 * NE), dtype=np.int64),
            ek_slot=np.full(_pow2(4 * NE), -1, dtype=np.int64),
            at_data=np.zeros(arena_t, dtype=np.int32), at_head=np.full(NCLASS, -1, dtype=np.int32),
            an_data=np.zeros(arena_n, dtype=np.int32), an_head=np.full(NCLASS, -1, dtype=np.int32),
            kv_key=np.zeros(SC, dtype=np.int64), kv_val=np.zeros(SC, dtype=np.int32),
            kv_st=np.zeros(SC, dtype=np.int64), kv_list=np.zeros(SC, dtype=np.int32),
            ke_key=np.zeros(SC, dtype=np.int64), ke_val=np.zeros(SC, dtype=np.int32),
            ke_st=np.zeros(SC, dtype=np.int64),
            kf_key=np.zeros(SC, dtype=np.int64), kf_val=np.zeros(SC, dtype=np.int32),
            kf_st=np.zeros(SC, dtype=np.int64),
            kd_key=np.zeros(SC, dtype=np.int64), kd_val=np.zeros(SC, dtype=np.int32),
            kd_st=np.zeros(SC, dtype=np.int64), kd_list=np.zeros(SC, dtype=np.int32),
            kd_slot=np.full(SC, -1, dtype=np.int32),
            buf_rem=np.zeros(3 * REGION, dtype=np.int32),
            buf_add=np.zeros((3 * REGION, 4), dtype=np.int32),
            cnt=np.zeros(64, dtype=np.int64), rs=rng_seed(0),
        )
        S.ctr[C_SV] = S.ctr[C_SE] = S.ctr[C_SF] = S.ctr[C_SD] = S.ctr[C_STM] = 1
        self.S = S
        self.n = n
        build_torus(S, n)
        if S.ctr[C_OVER]:
            raise RuntimeError("capacity overflow while building the torus")
        self.b[:] = 0.0

    # ---- counts ----------------------------------------------------------
    @property
    def V(self):
        return int(self.S.ctr[C_V])

    @property
    def E(self):
        return int(self.S.ctr[C_E])

    @property
    def T(self):
        return int(self.S.ctr[C_T])

    @property
    def b(self):
        return self.S.b

    def n3(self):
        return int(self.S.ctr[C_V3])

    def overflowed(self):
        return bool(self.S.ctr[C_OVER])

    # ---- reads -----------------------------------------------------------
    def vertices(self):
        return np.flatnonzero(self.S.v_alive[:self.S.ctr[C_VTOP]]).astype(np.int32)

    def neighbours(self, v):
        s = self.S.v_ns[v]
        return np.sort(self.S.an_data[s:s + self.S.v_nl[v]].copy())

    def tets_of(self, v):
        s = self.S.v_ts[v]
        return self.S.at_data[s:s + self.S.v_tl[v]].copy()

    def tet(self, tid):
        return tuple(int(x) for x in self.S.tv[tid])

    def tets(self):
        return self.S.tv[self.S.t_items[:self.T]]

    def valence(self, a, b):
        return int(valence(self.S, a, b))

    def degree(self, v):
        return int(self.S.v_nl[v])

    def edges(self):
        m = self.S.e_val[:self.S.ctr[C_ETOP]] > 0
        return np.stack([self.S.e_a[:self.S.ctr[C_ETOP]][m], self.S.e_b[:self.S.ctr[C_ETOP]][m]], axis=1)

    def valences(self):
        return self.S.e_val[:self.S.ctr[C_ETOP]][self.S.e_val[:self.S.ctr[C_ETOP]] > 0].astype(float)

    def get_phi(self, v):
        return float(self.S.phi[v])

    def set_phi(self, v, x):
        self.S.phi[v] = x

    def get_b(self, v):
        return float(self.S.b[v])

    def set_b(self, v, x):
        self.S.b[v] = x

    def set_omega(self, v, x):
        self.S.omega[v] = x

    def next_free_vertex(self):
        S = self.S
        return int(S.v_free[S.ctr[C_VFREE] - 1] if S.ctr[C_VFREE] > 0 else S.ctr[C_VTOP])

    # ---- structure -------------------------------------------------------
    def check(self):
        out = np.zeros(32, dtype=np.int64)
        n = check_codes(self.S, out)
        notes = []
        i = 0
        while i < n:
            code = int(out[i])
            msg = CHECK_MSG.get(code, "code %d" % code)
            if code in (3, 4, 5, 6, 7):
                i += 1
                msg = "%s (vertex %d)" % (msg, out[i])
            notes.append(msg)
            i += 1
        return notes

    def adjacency(self):
        ids = self.vertices()
        pos = {int(v): i for i, v in enumerate(ids)}
        ed = self.edges()
        lut = np.full(int(self.S.ctr[C_VTOP]) + 1, -1, dtype=np.int64)
        lut[ids] = np.arange(len(ids))
        ei = lut[ed[:, 0]]
        ej = lut[ed[:, 1]]
        N = len(ids)
        A = sp.csr_matrix((np.ones(2 * len(ei)),
                           (np.concatenate([ei, ej]), np.concatenate([ej, ei]))), shape=(N, N))
        return A, [int(v) for v in ids], pos, ei, ej

    # ---- plans (tier 1 and 2 use these) ----------------------------------
    def _plan(self, nr, na, base=B_A):
        if nr < 0:
            return None
        return (self.S.buf_rem[base:base + nr].copy(),
                self.S.buf_add[base:base + na].copy())

    def link_condition(self, v, a):
        return bool(link_condition(self.S, v, a))

    def merge_plan(self, v, a):
        return self._plan(*merge_plan(self.S, v, a, B_A))

    def split_plan(self, x, u, y):
        return self._plan(*split_plan(self.S, x, u, y, B_A))

    def flip23_plan(self, tid, face_index):
        return self._plan(*flip23_plan(self.S, tid, face_index, B_A))

    def flip32_plan(self, a, b):
        slot = edge_slot(self.S, a, b)
        if slot < 0:
            return None
        return self._plan(*flip32_plan(self.S, slot, B_A))

    def _load(self, plan):
        rem, add = plan
        self.S.buf_rem[B_A:B_A + len(rem)] = rem
        self.S.buf_add[B_A:B_A + len(add)] = add
        return len(rem), len(add)

    def n3_after_exact(self, plan):
        nr, na = self._load(plan)
        return int(n3_after(self.S, B_A, nr, na))

    def delta_S(self, plan, alpha, lam, phi_extra_vertex=-1, phi_extra_value=0.0):
        nr, na = self._load(plan)
        return float(delta_S(self.S, B_A, nr, na, alpha, lam))

    def allowed(self, plan, pool, s_max, gone=-1, cap=CEILING):
        nr, na = self._load(plan)
        sm = -1.0 if s_max is None else float(s_max)
        ok, born, dies, why = allowed(self.S, B_A, nr, na, int(pool), sm, int(gone), int(cap))
        return bool(ok), int(born), int(dies), REASON[why]

    def apply(self, plan):
        nr, na = self._load(plan)
        apply_plan(self.S, B_A, nr, na)

    def merge(self, v, a):
        self.apply(self.merge_plan(v, a))
        vert_free(self.S, v)

    def split(self, x, u):
        y = vert_new(self.S)
        nr, na = split_plan(self.S, x, u, y, B_A)
        apply_plan(self.S, B_A, nr, na)
        return int(y)

    # ---- the growth tick --------------------------------------------------
    def flip_randomize(self, sweeps):
        n = int(flip_randomize(self.S, self.S.rs, int(sweeps)))
        if self.S.ctr[C_OVER]:
            raise RuntimeError('capacity overflow in flip_randomize: code %d' % int(self.S.ctr[C_OVER]))
        return n

    def sync_step(self):
        sync_step(self.S)

    def seed(self, s):
        self.S.rs[:] = rng_seed(int(s))

    def tick(self, alpha, lam, pool, s_max=None, cap=CEILING):
        S = self.S
        out = np.zeros(16, dtype=np.int64)
        room = 4 * S.ctr[C_V] + 1024
        kids = np.zeros((room, 2), dtype=np.int32)
        absd = np.zeros((room, 2), dtype=np.int32)
        sm = -1.0 if s_max is None else float(s_max)
        self.phases = np.zeros(8)
        pool = tick(S, S.rs, float(alpha), float(lam), int(pool), sm, int(cap), out, kids, absd, self.phases)
        if S.ctr[C_OVER]:
            which = {1: "tetrahedron-list arena", 2: "neighbour-list arena", 3: "tetrahedra",
                     4: "edges", 5: "vertices", 6: "plan buffer"}.get(int(S.ctr[C_OVER]), "unknown")
            raise RuntimeError("capacity overflow in tick: %s" % which)
        if S.ctr[C_ERR]:
            raise RuntimeError("live vertex %d has no neighbours" % (S.ctr[C_ERR] - 1))
        r = dict(forced=int(out[0]), merges=int(out[1]), splits=int(out[2]), flips_accepted=int(out[3]),
                 size=int(out[4]), refused_budget=int(out[5]), refused_cap=int(out[6]),
                 refused_sync=int(out[7]), split_refused=int(out[8]), links=int(out[9]),
                 pool=int(out[10]), flips_link_neutral=bool(out[11]))
        return r, int(pool), kids[:out[12]], absd[:out[13]]
