"""Compiled 2+1 sampler (Allen D8: 'b, make it fast'), same rules as st3.py, ported to numba on attempt 8's engine.

Same moves (AJL's five 3D CDT moves), same proposals and Hastings factors, same weights (ED mode: linear + quadratic hold
on N0 and N22; CDT mode: exp(k0 N0) with the volume held softly). Only the speed differs; st3.py stays as the reference,
and st3f_check.py compares the two.

Events are proposed by slot (uniform over VTOP, dead slots rejected), so the vertex factors use VTOP, not N0.

Weight parameters, passed as one array W:
  W[0] mode (0 = ED, 1 = CDT)   W[1] mu0   W[2] mu22   W[3] eps   W[4] N0*   W[5] N22*   W[6] k0   W[7] epsv   W[8] N3*
"""
import os
import sys
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from p3_core import rng_float, rng_below                                   # noqa: E402
from p3_ops import (apply_plan, vert_new, vert_free, edge_slot, valence, C_T, C_V, C_VTOP, C_VFREE, C_OVER,  # noqa
                    tet_add, tet_remove)
from p3 import B_A                                                          # noqa: E402

CEIL = 60


@njit(cache=True)
def ttype(S, time, tid, Tn):
    """Returns (k, lo): k vertices in the lower slice lo, or (-1, -1) if the tetrahedron is not a layer piece."""
    a = time[S.tv[tid, 0]]
    lo = a
    hi = a
    for j in range(1, 4):
        t = time[S.tv[tid, j]]
        if t < lo:
            lo = t
        if t > hi:
            hi = t
    if lo == hi:
        return -1, -1
    if hi - lo == 1:
        base = lo
    elif lo == 0 and hi == Tn - 1:
        base = hi
    else:
        return -1, -1
    k = 0
    for j in range(4):
        if time[S.tv[tid, j]] == base:
            k += 1
    if k == 0 or k == 4:
        return -1, -1
    return k, base


@njit(cache=True)
def quad_type(time, a, b, c, d, Tn):
    lo = time[a]
    hi = time[a]
    for t in (time[b], time[c], time[d]):
        if t < lo:
            lo = t
        if t > hi:
            hi = t
    if lo == hi:
        return -1
    if hi - lo == 1:
        base = lo
    elif lo == 0 and hi == Tn - 1:
        base = hi
    else:
        return -1
    k = 0
    for t in (time[a], time[b], time[c], time[d]):
        if t == base:
            k += 1
    if k == 0 or k == 4:
        return -1
    return k


@njit(cache=True)
def _tets_with2(S, a, b, out):
    n = 0
    s = S.v_ts[a]
    for i in range(S.v_tl[a]):
        t = S.at_data[s + i]
        hit = False
        for j in range(4):
            if S.tv[t, j] == b:
                hit = True
        if hit:
            out[n] = t
            n += 1
    return n


@njit(cache=True)
def _tets_with3(S, a, b, c, out):
    n = 0
    s = S.v_ts[a]
    for i in range(S.v_tl[a]):
        t = S.at_data[s + i]
        hb = False
        hc = False
        for j in range(4):
            if S.tv[t, j] == b:
                hb = True
            if S.tv[t, j] == c:
                hc = True
        if hb and hc:
            out[n] = t
            n += 1
    return n


@njit(cache=True)
def _sdeg(S, time, v):
    n = 0
    s = S.v_ns[v]
    t0 = time[v]
    for i in range(S.v_nl[v]):
        if time[S.an_data[s + i]] == t0:
            n += 1
    return n


@njit(cache=True)
def _has_edge(S, a, b):
    sl = edge_slot(S, a, b)
    if sl < 0:
        return False
    return S.e_val[sl] > 0


@njit(cache=True)
def _lweight(W, n0, n22):
    if W[0] > 0.5:
        n3 = 4.0 * n0 + n22
        return W[6] * n0 - W[7] * (n3 - W[8]) ** 2
    d0 = n0 - W[4]
    d22 = n22 - W[5]
    return -W[1] * d0 - W[2] * d22 - W[3] * (d0 * d0 + d22 * d22)


@njit(cache=True)
def step(S, time, Tn, W, cnt, scratch):
    """One Metropolis step. cnt: [tried, accepted, N22, rejections by kind...]. Returns 1 if accepted."""
    cnt[0] += 1
    rs = S.rs
    N3 = S.ctr[C_T]
    N0 = S.ctr[C_V]
    kind = rng_below(rs, 5)
    nrem = 0
    nadd = 0
    dN0 = 0
    gone = -1
    newv = -1
    q_ratio = 1.0
    around = scratch[:64]
    tmp = scratch[64:128]
    if kind == 0:                                   # (2,6): insert an event in a spatial triangle
        tid = S.t_items[rng_below(rs, N3)]
        k, base = ttype(S, time, tid, Tn)
        if k != 3:
            cnt[3] += 1
            return 0
        a = -1
        b = -1
        c = -1
        p = -1
        for j in range(4):
            v = S.tv[tid, j]
            if time[v] == base:
                if a < 0:
                    a = v
                elif b < 0:
                    b = v
                else:
                    c = v
            else:
                p = v
        n = _tets_with3(S, a, b, c, around)
        if n != 2:
            cnt[4] += 1
            return 0
        other = around[0] if around[0] != tid else around[1]
        q = -1
        for j in range(4):
            v = S.tv[other, j]
            if v != a and v != b and v != c:
                q = v
        if _sdeg(S, time, a) + 1 > CEIL or _sdeg(S, time, b) + 1 > CEIL or _sdeg(S, time, c) + 1 > CEIL:
            cnt[5] += 1
            return 0
        dN0 = 1
        vtop_after = S.ctr[C_VTOP] if S.ctr[C_VFREE] > 0 else S.ctr[C_VTOP] + 1
        q_ratio = (1.0 / vtop_after) / (1.0 / N3)      # events are proposed by slot: 1/VTOP, dead slots rejected
        nrem = 2
        S.buf_rem[B_A] = tid
        S.buf_rem[B_A + 1] = other
        tmp[0] = a
        tmp[1] = b
        tmp[2] = c
        tmp[3] = p
        tmp[4] = q
        nadd = 6
    elif kind == 1:                                 # (6,2): remove an event
        vs = rng_below(rs, S.ctr[C_VTOP])
        if S.v_alive[vs] == 0:
            cnt[6] += 1
            return 0
        v = vs
        if S.v_tl[v] != 6:
            cnt[7] += 1
            return 0
        t0 = time[v]
        up = -1
        dn = -1
        ns = 0
        sp0 = -1
        sp1 = -1
        sp2 = -1
        ok = True
        s = S.v_ns[v]
        for i in range(S.v_nl[v]):
            w = S.an_data[s + i]
            if time[w] == t0:
                if sp0 < 0:
                    sp0 = w
                elif sp1 < 0:
                    sp1 = w
                elif sp2 < 0:
                    sp2 = w
                else:
                    ok = False
                ns += 1
            elif (time[w] - t0) % Tn == 1:
                if up >= 0:
                    ok = False
                up = w
            else:
                if dn >= 0:
                    ok = False
                dn = w
        if (not ok) or ns != 3 or up < 0 or dn < 0:
            cnt[7] += 1
            return 0
        if _tets_with3(S, sp0, sp1, sp2, around) > 0:
            cnt[8] += 1
            return 0
        s = S.v_ts[v]
        for i in range(6):
            S.buf_rem[B_A + i] = S.at_data[s + i]
        nrem = 6
        S.buf_add[B_A, 0] = sp0
        S.buf_add[B_A, 1] = sp1
        S.buf_add[B_A, 2] = sp2
        S.buf_add[B_A, 3] = up
        S.buf_add[B_A + 1, 0] = sp0
        S.buf_add[B_A + 1, 1] = sp1
        S.buf_add[B_A + 1, 2] = sp2
        S.buf_add[B_A + 1, 3] = dn
        nadd = 2
        dN0 = -1
        gone = v
        q_ratio = (1.0 / (N3 - 4)) * S.ctr[C_VTOP]
    elif kind == 2:                                 # (4,4): flip a spatial link
        tid = S.t_items[rng_below(rs, N3)]
        k, base = ttype(S, time, tid, Tn)
        if k != 3:
            cnt[3] += 1
            return 0
        b0 = -1
        b1 = -1
        b2 = -1
        for j in range(4):
            v = S.tv[tid, j]
            if time[v] == base:
                if b0 < 0:
                    b0 = v
                elif b1 < 0:
                    b1 = v
                else:
                    b2 = v
        r = rng_below(rs, 3)
        if r == 0:
            a = b0
            b = b1
        elif r == 1:
            a = b1
            b = b2
        else:
            a = b0
            b = b2
        n = _tets_with2(S, a, b, around)
        if n != 4:
            cnt[9] += 1
            return 0
        t0 = time[a]
        up_ap = -1
        dn_ap = -1
        c = -1
        d = -1
        okk = True
        for i in range(4):
            t = around[i]
            sp = -1
            ap = -1
            for j in range(4):
                w = S.tv[t, j]
                if w == a or w == b:
                    continue
                if time[w] == t0:
                    sp = w
                else:
                    ap = w
            if sp < 0 or ap < 0:
                okk = False
                break
            if (time[ap] - t0) % Tn == 1:
                if up_ap < 0:
                    up_ap = ap
                elif up_ap != ap:
                    okk = False
            else:
                if dn_ap < 0:
                    dn_ap = ap
                elif dn_ap != ap:
                    okk = False
            if c < 0:
                c = sp
            elif c != sp and d < 0:
                d = sp
            elif c != sp and d != sp:
                okk = False
        if (not okk) or up_ap < 0 or dn_ap < 0 or c < 0 or d < 0 or c == d:
            cnt[9] += 1
            return 0
        if _has_edge(S, c, d):
            cnt[10] += 1
            return 0
        if _sdeg(S, time, c) + 1 > CEIL or _sdeg(S, time, d) + 1 > CEIL:
            cnt[5] += 1
            return 0
        for i in range(4):
            S.buf_rem[B_A + i] = around[i]
        nrem = 4
        S.buf_add[B_A, 0] = c
        S.buf_add[B_A, 1] = d
        S.buf_add[B_A, 2] = a
        S.buf_add[B_A, 3] = up_ap
        S.buf_add[B_A + 1, 0] = c
        S.buf_add[B_A + 1, 1] = d
        S.buf_add[B_A + 1, 2] = b
        S.buf_add[B_A + 1, 3] = up_ap
        S.buf_add[B_A + 2, 0] = c
        S.buf_add[B_A + 2, 1] = d
        S.buf_add[B_A + 2, 2] = a
        S.buf_add[B_A + 2, 3] = dn_ap
        S.buf_add[B_A + 3, 0] = c
        S.buf_add[B_A + 3, 1] = d
        S.buf_add[B_A + 3, 2] = b
        S.buf_add[B_A + 3, 3] = dn_ap
        nadd = 4
        q_ratio = 1.0
    elif kind == 3:                                 # (2,3): two pieces sharing a timelike triangle
        tid = S.t_items[rng_below(rs, N3)]
        f = rng_below(rs, 4)
        d = S.tv[tid, f]
        r0 = -1
        r1 = -1
        r2 = -1
        for j in range(4):
            if j == f:
                continue
            w = S.tv[tid, j]
            if r0 < 0:
                r0 = w
            elif r1 < 0:
                r1 = w
            else:
                r2 = w
        if time[r0] == time[r1] and time[r1] == time[r2]:
            cnt[11] += 1
            return 0
        n = _tets_with3(S, r0, r1, r2, around)
        if n != 2:
            cnt[11] += 1
            return 0
        other = around[0] if around[0] != tid else around[1]
        e = -1
        for j in range(4):
            w = S.tv[other, j]
            if w != r0 and w != r1 and w != r2:
                e = w
        if time[d] == time[e] or _has_edge(S, d, e):
            cnt[11] += 1
            return 0
        if quad_type(time, d, e, r0, r1, Tn) < 0 or quad_type(time, d, e, r1, r2, Tn) < 0 \
                or quad_type(time, d, e, r0, r2, Tn) < 0:
            cnt[11] += 1
            return 0
        S.buf_rem[B_A] = tid
        S.buf_rem[B_A + 1] = other
        nrem = 2
        S.buf_add[B_A, 0] = d
        S.buf_add[B_A, 1] = e
        S.buf_add[B_A, 2] = r0
        S.buf_add[B_A, 3] = r1
        S.buf_add[B_A + 1, 0] = d
        S.buf_add[B_A + 1, 1] = e
        S.buf_add[B_A + 1, 2] = r1
        S.buf_add[B_A + 1, 3] = r2
        S.buf_add[B_A + 2, 0] = d
        S.buf_add[B_A + 2, 1] = e
        S.buf_add[B_A + 2, 2] = r0
        S.buf_add[B_A + 2, 3] = r2
        nadd = 3
        q_rev = (1.0 / S.ctr[C_VTOP]) * (1.0 / (S.v_nl[d] + 1) + 1.0 / (S.v_nl[e] + 1))
        q_ratio = q_rev / (1.0 / (2.0 * N3))
    else:                                           # (3,2): a timelike link of valence 3
        vs = rng_below(rs, S.ctr[C_VTOP])
        if S.v_alive[vs] == 0 or S.v_nl[vs] == 0:
            cnt[6] += 1
            return 0
        v = vs
        w = S.an_data[S.v_ns[v] + rng_below(rs, S.v_nl[v])]
        if time[v] == time[w]:
            cnt[12] += 1
            return 0
        n = _tets_with2(S, v, w, around)
        if n != 3:
            cnt[13] += 1
            return 0
        r0 = -1
        r1 = -1
        r2 = -1
        for i in range(3):
            t = around[i]
            for j in range(4):
                x = S.tv[t, j]
                if x == v or x == w:
                    continue
                if r0 < 0:
                    r0 = x
                elif x != r0 and r1 < 0:
                    r1 = x
                elif x != r0 and x != r1 and r2 < 0:
                    r2 = x
        if r2 < 0:
            cnt[13] += 1
            return 0
        if time[r0] == time[r1] and time[r1] == time[r2]:
            cnt[13] += 1
            return 0
        if _tets_with3(S, r0, r1, r2, tmp) > 0:
            cnt[8] += 1
            return 0
        if quad_type(time, r0, r1, r2, v, Tn) < 0 or quad_type(time, r0, r1, r2, w, Tn) < 0:
            cnt[13] += 1
            return 0
        for i in range(3):
            S.buf_rem[B_A + i] = around[i]
        nrem = 3
        S.buf_add[B_A, 0] = r0
        S.buf_add[B_A, 1] = r1
        S.buf_add[B_A, 2] = r2
        S.buf_add[B_A, 3] = v
        S.buf_add[B_A + 1, 0] = r0
        S.buf_add[B_A + 1, 1] = r1
        S.buf_add[B_A + 1, 2] = r2
        S.buf_add[B_A + 1, 3] = w
        nadd = 2
        q_fwd = (1.0 / S.ctr[C_VTOP]) * (1.0 / S.v_nl[v] + 1.0 / S.v_nl[w])
        q_ratio = (1.0 / (2.0 * (N3 - 1))) / q_fwd
    # N22 change
    d22 = 0
    for i in range(nrem):
        k, base = ttype(S, time, S.buf_rem[B_A + i], Tn)
        if k == 2:
            d22 -= 1
    if kind == 0:                                   # the six new pieces are all (3,1)/(1,3): no change
        pass
    else:
        for i in range(nadd):
            if quad_type(time, S.buf_add[B_A + i, 0], S.buf_add[B_A + i, 1], S.buf_add[B_A + i, 2],
                         S.buf_add[B_A + i, 3], Tn) == 2:
                d22 += 1
    la = np.log(q_ratio) + _lweight(W, N0 + dN0, cnt[2] + d22) - _lweight(W, N0, cnt[2])
    if la < 0.0 and rng_float(rs) >= np.exp(la):
        cnt[14] += 1
        return 0
    if kind == 0:                                   # allocate the new event, then fill the six pieces
        newv = vert_new(S)
        if newv < 0:
            return 0
        time[newv] = time[tmp[0]]
        a = tmp[0]
        b = tmp[1]
        c = tmp[2]
        p = tmp[3]
        q = tmp[4]
        S.buf_add[B_A, 0] = newv
        S.buf_add[B_A, 1] = a
        S.buf_add[B_A, 2] = b
        S.buf_add[B_A, 3] = p
        S.buf_add[B_A + 1, 0] = newv
        S.buf_add[B_A + 1, 1] = b
        S.buf_add[B_A + 1, 2] = c
        S.buf_add[B_A + 1, 3] = p
        S.buf_add[B_A + 2, 0] = newv
        S.buf_add[B_A + 2, 1] = a
        S.buf_add[B_A + 2, 2] = c
        S.buf_add[B_A + 2, 3] = p
        S.buf_add[B_A + 3, 0] = newv
        S.buf_add[B_A + 3, 1] = a
        S.buf_add[B_A + 3, 2] = b
        S.buf_add[B_A + 3, 3] = q
        S.buf_add[B_A + 4, 0] = newv
        S.buf_add[B_A + 4, 1] = b
        S.buf_add[B_A + 4, 2] = c
        S.buf_add[B_A + 4, 3] = q
        S.buf_add[B_A + 5, 0] = newv
        S.buf_add[B_A + 5, 1] = a
        S.buf_add[B_A + 5, 2] = c
        S.buf_add[B_A + 5, 3] = q
    apply_plan(S, B_A, nrem, nadd)
    if gone >= 0:
        vert_free(S, gone)
        time[gone] = -1
    cnt[1] += 1
    cnt[2] += d22
    cnt[16 + kind] += 1          # accepted by move kind (diagnostic)
    return 1


@njit(cache=True)
def sweep(S, time, Tn, W, cnt, scratch, nsteps):
    for _ in range(nsteps):
        step(S, time, Tn, W, cnt, scratch)
    return cnt
