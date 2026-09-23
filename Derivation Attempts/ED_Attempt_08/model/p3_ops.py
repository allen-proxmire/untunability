"""Port containers and gates (E2; note 2 C6; D3). Low-level half of attempt 7's C3c-C3f slice on flat arrays with a Numba inner loop.

Same model, same knobs, same moves, same gates, same acceptance rule as
`../../ED_Attempt_07/model/c3f.py`. Only the representation differs (IMPLEMENTATION_NOTES.md,
"The port"), and with it the set-iteration order, so the random path is not attempt 7's - see
note 2's C5 and the tier 1-3 ladder.

State is a NamedTuple of arrays; mutable scalars live in `S.ctr`, since numba cannot write a tuple
field. Capacity is checked as it is used, flagged in `ctr[C_OVER]`, and grown in Python by rebuilding.
"""
import numpy as np
import scipy.sparse as sp
from collections import namedtuple
from numba import njit, int64
from p3_core import (FLAT_VALENCE, SIGMA, K, K_RESPONSE, FLAT_LINKS_PER_EVENT, CEILING,
                     NCLASS, MINCLASS, rng_seed, rng_float, rng_below, rng_geometric,
                     rng_shuffle, mix64, ekey, etab_find, etab_delete, arena_class)

C_T, C_V, C_E, C_V3 = 0, 1, 2, 3
C_ATTOP, C_ANTOP = 4, 5
C_VFREE, C_TFREE, C_EFREE = 6, 7, 8
C_SV, C_SE, C_SF, C_SD, C_STM = 9, 10, 11, 12, 13
C_OVER, C_TTOP, C_VTOP, C_ETOP, C_ERR = 14, 15, 16, 17, 18
REGION = 8192          # room per plan region in buf_rem/buf_add
NCTR = 24

FIELDS = ("ctr v_alive v_ts v_tl v_tc v_ns v_nl v_nc b omega phi v_free "
          "tv te t_alive t_items t_pos t_free tmark "
          "e_a e_b e_val e_free e3_items e3_pos ek_key ek_slot "
          "at_data at_head an_data an_head "
          "kv_key kv_val kv_st kv_list ke_key ke_val ke_st kf_key kf_val kf_st "
          "kd_key kd_val kd_st kd_list kd_slot buf_rem buf_add cnt rs").split()
State = namedtuple("State", FIELDS)

R_MERGE, R_SPLIT, R_F23, R_F32 = 0, 1, 2, 3
REASON = ("", "budget", "cap", "sync")


# ------------------------------------------------------------------ scratch tables
@njit(cache=True, inline="always")
def _kfind(key_arr, st_arr, mask, key, stamp):
    i = int64(mix64(key) & np.uint64(mask))
    while True:
        if st_arr[i] != stamp:
            return i, False
        if key_arr[i] == key:
            return i, True
        i = (i + 1) & mask


_kfind_pub = _kfind


@njit(cache=True, inline="always")
def _kor(key_arr, val_arr, st_arr, mask, key, bit, stamp):
    i, found = _kfind(key_arr, st_arr, mask, key, stamp)
    if found:
        val_arr[i] |= bit
        return False
    st_arr[i] = stamp
    key_arr[i] = key
    val_arr[i] = bit
    return True


@njit(cache=True, inline="always")
def _kget(key_arr, val_arr, st_arr, mask, key, stamp):
    i, found = _kfind(key_arr, st_arr, mask, key, stamp)
    if found:
        return val_arr[i]
    return 0


@njit(cache=True, inline="always")
def tri_key(a, b, c):
    x, y, z = a, b, c
    if x > y:
        x, y = y, x
    if y > z:
        y, z = z, y
    if x > y:
        x, y = y, x
    return int64(x) | (int64(y) << int64(21)) | (int64(z) << int64(42))


# ------------------------------------------------------------------ arena lists
@njit(cache=True)
def _lst_alloc(data, head, ctr, ctr_i, need):
    cls = arena_class(need)
    h = head[cls]
    if h >= 0:
        head[cls] = data[h]
        return h, cls
    start = ctr[ctr_i]
    ctr[ctr_i] = start + (1 << (cls + MINCLASS))
    if ctr[ctr_i] > data.shape[0]:
        ctr[C_OVER] = 1 if ctr_i == C_ATTOP else 2
        return 0, cls
    return start, cls


@njit(cache=True, inline="always")
def _lst_release(data, head, start, cls):
    """Give a per-vertex block back to its size class. Without this every split leaks two blocks."""
    data[start] = head[cls]
    head[cls] = start


@njit(cache=True)
def _lst_push(data, head, ctr, ctr_i, starts, lens, clss, v, x):
    n = lens[v]
    cls = clss[v]
    if n + 1 > (1 << (cls + MINCLASS)):
        ns, ncls = _lst_alloc(data, head, ctr, ctr_i, n + 1)
        if ctr[C_OVER] == 1:
            return
        s = starts[v]
        for i in range(n):
            data[ns + i] = data[s + i]
        data[s] = head[cls]
        head[cls] = s
        starts[v] = ns
        clss[v] = ncls
    data[starts[v] + n] = x
    lens[v] = n + 1


@njit(cache=True)
def _lst_remove(data, starts, lens, v, x):
    s = starts[v]
    n = lens[v]
    for i in range(n):
        if data[s + i] == x:
            data[s + i] = data[s + n - 1]
            lens[v] = n - 1
            return True
    return False


# ------------------------------------------------------------------ edges
@njit(cache=True)
def edge_slot(S, a, b):
    mask = S.ek_key.shape[0] - 1
    _, slot = etab_find(S.ek_key, S.ek_slot, mask, ekey(a, b))
    return slot


@njit(cache=True)
def valence(S, a, b):
    s = edge_slot(S, a, b)
    if s < 0:
        return 0
    return S.e_val[s]


@njit(cache=True)
def _v3_add(S, slot):
    if S.e3_pos[slot] >= 0:
        return
    n = S.ctr[C_V3]
    S.e3_items[n] = slot
    S.e3_pos[slot] = n
    S.ctr[C_V3] = n + 1


@njit(cache=True)
def _v3_del(S, slot):
    i = S.e3_pos[slot]
    if i < 0:
        return
    n = S.ctr[C_V3] - 1
    last = S.e3_items[n]
    S.e3_items[i] = last
    S.e3_pos[last] = i
    S.e3_pos[slot] = -1
    S.ctr[C_V3] = n


@njit(cache=True)
def _edge_bump(S, a, b, d):
    """Change an edge's valence by d, creating or destroying it. Returns the edge slot (-1 if gone)."""
    mask = S.ek_key.shape[0] - 1
    key = ekey(a, b)
    i, slot = etab_find(S.ek_key, S.ek_slot, mask, key)
    if slot < 0:
        if d <= 0:
            return -1
        n = S.ctr[C_EFREE]
        if n > 0:
            slot = S.e_free[n - 1]
            S.ctr[C_EFREE] = n - 1
        else:
            slot = S.ctr[C_ETOP]
            if slot >= S.e_a.shape[0]:
                S.ctr[C_OVER] = 4
                return -1
            S.ctr[C_ETOP] = slot + 1
        S.e_a[slot] = min(a, b)
        S.e_b[slot] = max(a, b)
        S.e_val[slot] = 0
        S.e3_pos[slot] = -1
        S.ek_key[i] = key
        S.ek_slot[i] = slot
        S.ctr[C_E] += 1
        _lst_push(S.an_data, S.an_head, S.ctr, C_ANTOP, S.v_ns, S.v_nl, S.v_nc, a, b)
        _lst_push(S.an_data, S.an_head, S.ctr, C_ANTOP, S.v_ns, S.v_nl, S.v_nc, b, a)
    old = S.e_val[slot]
    new = old + d
    S.e_val[slot] = new
    if new == 3:
        _v3_add(S, slot)
    elif old == 3:
        _v3_del(S, slot)
    if new == 0:
        _v3_del(S, slot)
        etab_delete(S.ek_key, S.ek_slot, mask, key)
        _lst_remove(S.an_data, S.v_ns, S.v_nl, a, b)
        _lst_remove(S.an_data, S.v_ns, S.v_nl, b, a)
        n = S.ctr[C_EFREE]
        S.e_free[n] = slot
        S.ctr[C_EFREE] = n + 1
        S.ctr[C_E] -= 1
        return -1
    return slot


# ------------------------------------------------------------------ tetrahedra
@njit(cache=True, inline="always")
def _sort4(a, b, c, d, out):
    out[0], out[1], out[2], out[3] = a, b, c, d
    for i in range(1, 4):
        x = out[i]
        j = i - 1
        while j >= 0 and out[j] > x:
            out[j + 1] = out[j]
            j -= 1
        out[j + 1] = x


@njit(cache=True)
def tet_with4(S, a, b, c, d):
    """tid of the tetrahedron on these four vertices, or -1. Scans the shortest incidence list."""
    best, bl = a, S.v_tl[a]
    if S.v_tl[b] < bl:
        best, bl = b, S.v_tl[b]
    if S.v_tl[c] < bl:
        best, bl = c, S.v_tl[c]
    if S.v_tl[d] < bl:
        best, bl = d, S.v_tl[d]
    q = np.empty(4, dtype=np.int32)
    _sort4(a, b, c, d, q)
    s = S.v_ts[best]
    for i in range(bl):
        t = S.at_data[s + i]
        if S.tv[t, 0] == q[0] and S.tv[t, 1] == q[1] and S.tv[t, 2] == q[2] and S.tv[t, 3] == q[3]:
            return t
    return -1


@njit(cache=True)
def tet_add(S, a, b, c, d):
    q = np.empty(4, dtype=np.int32)
    _sort4(a, b, c, d, q)
    n = S.ctr[C_TFREE]
    if n > 0:
        tid = S.t_free[n - 1]
        S.ctr[C_TFREE] = n - 1
    else:
        tid = S.ctr[C_TTOP]
        if tid >= S.tv.shape[0]:
            S.ctr[C_OVER] = 3
            return -1
        S.ctr[C_TTOP] = tid + 1
    S.tv[tid, 0], S.tv[tid, 1], S.tv[tid, 2], S.tv[tid, 3] = q[0], q[1], q[2], q[3]
    S.t_alive[tid] = 1
    m = S.ctr[C_T]
    S.t_items[m] = tid
    S.t_pos[tid] = m
    S.ctr[C_T] = m + 1
    for i in range(4):
        _lst_push(S.at_data, S.at_head, S.ctr, C_ATTOP, S.v_ts, S.v_tl, S.v_tc, q[i], tid)
    k = 0
    for i in range(4):
        for j in range(i + 1, 4):
            S.te[tid, k] = _edge_bump(S, q[i], q[j], 1)
            k += 1
    return tid


@njit(cache=True)
def tet_remove(S, tid):
    v = np.empty(4, dtype=np.int32)
    v[0], v[1], v[2], v[3] = S.tv[tid, 0], S.tv[tid, 1], S.tv[tid, 2], S.tv[tid, 3]
    S.t_alive[tid] = 0
    m = S.ctr[C_T] - 1
    i = S.t_pos[tid]
    last = S.t_items[m]
    S.t_items[i] = last
    S.t_pos[last] = i
    S.ctr[C_T] = m
    n = S.ctr[C_TFREE]
    S.t_free[n] = tid
    S.ctr[C_TFREE] = n + 1
    for i in range(4):
        _lst_remove(S.at_data, S.v_ts, S.v_tl, v[i], tid)
    for i in range(4):
        for j in range(i + 1, 4):
            _edge_bump(S, v[i], v[j], -1)


# ------------------------------------------------------------------ vertices
@njit(cache=True)
def vert_new(S):
    n = S.ctr[C_VFREE]
    if n > 0:
        v = S.v_free[n - 1]
        S.ctr[C_VFREE] = n - 1
    else:
        v = S.ctr[C_VTOP]
        if v >= S.v_alive.shape[0]:
            S.ctr[C_OVER] = 5
            return -1
        S.ctr[C_VTOP] = v + 1
    S.v_alive[v] = 1
    S.v_tl[v] = 0
    S.v_nl[v] = 0
    st, cls = _lst_alloc(S.at_data, S.at_head, S.ctr, C_ATTOP, 1)
    S.v_ts[v], S.v_tc[v] = st, cls
    st, cls = _lst_alloc(S.an_data, S.an_head, S.ctr, C_ANTOP, 1)
    S.v_ns[v], S.v_nc[v] = st, cls
    S.ctr[C_V] += 1
    return v


@njit(cache=True)
def vert_free(S, v):
    S.v_alive[v] = 0
    _lst_release(S.at_data, S.at_head, S.v_ts[v], S.v_tc[v])
    _lst_release(S.an_data, S.an_head, S.v_ns[v], S.v_nc[v])
    S.v_tl[v] = 0
    S.v_nl[v] = 0
    n = S.ctr[C_VFREE]
    S.v_free[n] = v
    S.ctr[C_VFREE] = n + 1
    S.ctr[C_V] -= 1


# ------------------------------------------------------------------ the per-move edge delta
@njit(cache=True)
def edge_delta(S, base, nrem, nadd):
    """Per-edge valence change for a plan. Returns the number of touched table entries."""
    stamp = S.ctr[C_SD] + 1
    S.ctr[C_SD] = stamp
    mask = S.kd_key.shape[0] - 1
    cnt = 0
    for i in range(nrem):
        t = S.buf_rem[base + i]
        k = 0
        for p in range(4):
            for q in range(p + 1, 4):
                key = ekey(S.tv[t, p], S.tv[t, q])
                idx, found = _kfind(S.kd_key, S.kd_st, mask, key, stamp)
                if not found:
                    S.kd_st[idx] = stamp
                    S.kd_key[idx] = key
                    S.kd_val[idx] = 0
                    S.kd_slot[idx] = S.te[t, k]
                    S.kd_list[cnt] = idx
                    cnt += 1
                S.kd_val[idx] -= 1
                k += 1
    for i in range(nadd):
        for p in range(4):
            for q in range(p + 1, 4):
                key = ekey(S.buf_add[base + i, p], S.buf_add[base + i, q])
                idx, found = _kfind(S.kd_key, S.kd_st, mask, key, stamp)
                if not found:
                    S.kd_st[idx] = stamp
                    S.kd_key[idx] = key
                    S.kd_val[idx] = 0
                    _, sl = etab_find(S.ek_key, S.ek_slot, S.ek_key.shape[0] - 1, key)
                    S.kd_slot[idx] = sl
                    S.kd_list[cnt] = idx
                    cnt += 1
                S.kd_val[idx] += 1
    return cnt


@njit(cache=True, inline="always")
def _old_val(S, idx):
    sl = S.kd_slot[idx]
    if sl < 0:
        return 0
    return S.e_val[sl]


@njit(cache=True, inline="always")
def _key_a(key):
    return int64(key >> int64(32))


@njit(cache=True, inline="always")
def _key_b(key):
    return int64(key & int64(0xFFFFFFFF))


@njit(cache=True)
def n3_after(S, base, nrem, nadd):
    cnt = edge_delta(S, base, nrem, nadd)
    n3 = S.ctr[C_V3]
    for i in range(cnt):
        idx = S.kd_list[i]
        d = S.kd_val[idx]
        old = _old_val(S, idx)
        new = old + d
        n3 += (1 if new == 3 else 0) - (1 if old == 3 else 0)
    return n3


@njit(cache=True)
def delta_S(S, base, nrem, nadd, alpha, lam):
    """alpha*E + lam*sum (valence - 5.1043)^2 ; no sync term (c3f calls delta_S with gamma = 0)."""
    if alpha == 0.0 and lam == 0.0:
        return 0.0
    cnt = edge_delta(S, base, nrem, nadd)
    dS = 0.0
    for i in range(cnt):
        idx = S.kd_list[i]
        d = S.kd_val[idx]
        if d == 0:
            continue
        old = _old_val(S, idx)
        new = old + d
        if lam != 0.0:
            a1 = (new - FLAT_VALENCE) ** 2 if new > 0 else 0.0
            a0 = (old - FLAT_VALENCE) ** 2 if old > 0 else 0.0
            dS += lam * (a1 - a0)
        if alpha != 0.0:
            if old == 0 and new > 0:
                dS += alpha
            elif old > 0 and new == 0:
                dS -= alpha
    return dS


@njit(cache=True)
def allowed(S, base, nrem, nadd, pool, s_max, gone, cap):
    """(ok, born, dies, reason code). Budget, ceiling and the sync condition in one pass."""
    cnt = edge_delta(S, base, nrem, nadd)
    born = 0
    dies = 0
    stamp = S.ctr[C_SV] + 1
    S.ctr[C_SV] = stamp
    mask = S.kv_key.shape[0] - 1
    nv = 0
    nborn = 0
    for i in range(cnt):
        idx = S.kd_list[i]
        d = S.kd_val[idx]
        if d == 0:
            continue
        key = S.kd_key[idx]
        a = _key_a(key)
        b = _key_b(key)
        old = _old_val(S, idx)
        new = old + d
        if old == 0 and new > 0:
            born += 1
            S.kd_list[S.kd_list.shape[0] - 1 - nborn] = idx      # remember born edges at the far end
            nborn += 1
            dd = 1
        elif old > 0 and new == 0:
            dies += 1
            dd = -1
        else:
            continue
        for w in (a, b):
            j, found = _kfind(S.kv_key, S.kv_st, mask, w, stamp)
            if not found:
                S.kv_st[j] = stamp
                S.kv_key[j] = w
                S.kv_val[j] = 0
                S.kv_list[nv] = j
                nv += 1
            S.kv_val[j] += dd
    if born - dies > max(pool, 0):
        return False, born, dies, 1
    for i in range(nv):
        j = S.kv_list[i]
        d = S.kv_val[j]
        if d <= 0:
            continue
        w = S.kv_key[j]
        if w == gone:
            continue
        base_deg = S.v_nl[w] if S.v_alive[w] == 1 else 0
        if base_deg + d > cap:
            return False, born, dies, 2
    if s_max >= 0.0:            # -1.0 is the sentinel for 'no threshold'; 0.0 is a real one
        scale = SIGMA / K
        for i in range(nborn):
            idx = S.kd_list[S.kd_list.shape[0] - 1 - i]
            key = S.kd_key[idx]
            a = _key_a(key)
            b = _key_b(key)
            if S.v_alive[a] == 0 or S.v_alive[b] == 0:
                continue                                   # a new child inherits its parent's tick count
            if abs(S.phi[a] - S.phi[b]) / scale > s_max:
                return False, born, dies, 3
    return True, born, dies, 0


@njit(cache=True)
def gate_and_cost(S, base, nrem, nadd, pool, s_max, gone, cap, alpha, lam):
    """`allowed` and `delta_S` in ONE pass over the move's edges (ok, born, dies, why, dS).

    Attempt 7's C3f lesson applied again: walking a move's edges twice is pure waste. The two
    separate entry points above are kept because tier 1 of note 2's ladder compares them one at
    a time; the tick uses this.
    """
    cnt = edge_delta(S, base, nrem, nadd)
    born = 0
    dies = 0
    dS = 0.0
    cost = not (alpha == 0.0 and lam == 0.0)
    stamp = S.ctr[C_SV] + 1
    S.ctr[C_SV] = stamp
    mask = S.kv_key.shape[0] - 1
    nv = 0
    nborn = 0
    top = S.kd_list.shape[0] - 1
    for i in range(cnt):
        idx = S.kd_list[i]
        d = S.kd_val[idx]
        if d == 0:
            continue
        key = S.kd_key[idx]
        a = _key_a(key)
        b = _key_b(key)
        old = _old_val(S, idx)
        new = old + d
        if cost and lam != 0.0:
            a1 = (new - FLAT_VALENCE) ** 2 if new > 0 else 0.0
            a0 = (old - FLAT_VALENCE) ** 2 if old > 0 else 0.0
            dS += lam * (a1 - a0)
        if old == 0 and new > 0:
            born += 1
            S.kd_list[top - nborn] = idx
            nborn += 1
            dd = 1
            if cost and alpha != 0.0:
                dS += alpha
        elif old > 0 and new == 0:
            dies += 1
            dd = -1
            if cost and alpha != 0.0:
                dS -= alpha
        else:
            continue
        for w in (a, b):
            j, found = _kfind(S.kv_key, S.kv_st, mask, w, stamp)
            if not found:
                S.kv_st[j] = stamp
                S.kv_key[j] = w
                S.kv_val[j] = 0
                S.kv_list[nv] = j
                nv += 1
            S.kv_val[j] += dd
    if born - dies > max(pool, 0):
        return False, born, dies, 1, dS
    for i in range(nv):
        j = S.kv_list[i]
        d = S.kv_val[j]
        if d <= 0:
            continue
        w = S.kv_key[j]
        if w == gone:
            continue
        base_deg = S.v_nl[w] if S.v_alive[w] == 1 else 0
        if base_deg + d > cap:
            return False, born, dies, 2, dS
    if s_max >= 0.0:            # -1.0 is the sentinel for 'no threshold'; 0.0 is a real one
        scale = SIGMA / K
        for i in range(nborn):
            idx = S.kd_list[top - i]
            key = S.kd_key[idx]
            a = _key_a(key)
            b = _key_b(key)
            if S.v_alive[a] == 0 or S.v_alive[b] == 0:
                continue
            if abs(S.phi[a] - S.phi[b]) / scale > s_max:
                return False, born, dies, 3, dS
    return True, born, dies, 0, dS


@njit(cache=True)
def apply_plan(S, base, nrem, nadd):
    for i in range(nrem):
        tet_remove(S, S.buf_rem[base + i])
    for i in range(nadd):
        tet_add(S, S.buf_add[base + i, 0], S.buf_add[base + i, 1],
                S.buf_add[base + i, 2], S.buf_add[base + i, 3])
