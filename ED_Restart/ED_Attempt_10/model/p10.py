"""Attempt 10's growth tick: attempt 9's tick9 (copied from ../../ED_Attempt_09/model/p9.py, a closed record) with one
switchable change, D14 (Allen: 'adopt narrow both ways'):

NARROW MERGE. A childless event v may merge into neighbour a only if the merge is the exact reverse of an edge split of
(a, u): deg v = val(va) + 2, v has exactly one neighbour u (other than a) not linked to a, val(vu) = val(va), and v lies
in exactly 2 val(va) tetrahedra (its link is the suspension of Lk(va) with poles a and u). Splits stay edge splits.
narrow = 0 reproduces attempt 9's tick9 bit for bit.
"""
import os
import sys
import time
import numpy as np
from numba import njit, int64, objmode

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

import p3 as _p3                                   # noqa: E402
import p3_ops as _ops                              # noqa: E402
import p3_core as _core                            # noqa: E402
from p3 import Slice3P                             # noqa: E402

for _m in (_core, _ops, _p3):
    for _k, _v in vars(_m).items():
        if not _k.startswith('__'):
            globals().setdefault(_k, _v)


@njit(cache=True)
def narrow_ok(S, v, a):
    k = valence(S, v, a)
    if S.v_nl[v] != k + 2 or S.v_tl[v] != 2 * k:
        return False
    u = -1
    sn = S.v_ns[v]
    for i in range(S.v_nl[v]):
        w = S.an_data[sn + i]
        if w == a:
            continue
        if edge_slot(S, w, a) < 0:
            if u >= 0:
                return False
            u = w
    if u < 0:
        return False
    return valence(S, v, u) == k



@njit(cache=True)
def tick10(S, rs, alpha, lam, pool, s_max, cap, q, flip_frac, narrow, out, kids_out, abs_out, tm):
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
        # D11: mostly exactly one child. With probability q the event draws from the old spread
        # (geometric, mean mu, as A7 C1 took from CDT); otherwise it has exactly one child.
        if q >= 1.0 or rng_float(rs) < q:        # q = 1 consumes no extra draw, so it is attempt 8 bit for bit
            cntv[v] = rng_geometric(rs, 1.0 / (1.0 + mu)) - 1
        else:
            cntv[v] = 1
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
            if narrow and not narrow_ok(S, v, a):
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
    sweeps = int(S.ctr[C_V] * flip_frac) // 2
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


class Slice10P(Slice3P):
    """Slice3P with attempt 9's tick: q (share drawing from the old spread) and flip_frac."""

    def tick10(self, alpha, lam, pool, q=1.0, flip_frac=1.0, narrow=True, s_max=None, cap=None):
        S = self.S
        cap = CEILING if cap is None else cap
        out = np.zeros(16, dtype=np.int64)
        room = 4 * S.ctr[C_V] + 1024
        kids = np.zeros((room, 2), dtype=np.int32)
        absd = np.zeros((room, 2), dtype=np.int32)
        sm = -1.0 if s_max is None else float(s_max)
        self.phases = np.zeros(8)
        pool = tick10(S, S.rs, float(alpha), float(lam), int(pool), sm, int(cap), float(q), float(flip_frac), bool(narrow),
                     out, kids, absd, self.phases)
        if S.ctr[C_OVER]:
            raise RuntimeError("capacity overflow in tick10: code %d" % int(S.ctr[C_OVER]))
        r = dict(forced=int(out[0]), merges=int(out[1]), splits=int(out[2]), flips_accepted=int(out[3]),
                 size=int(out[4]), refused_budget=int(out[5]), refused_cap=int(out[6]),
                 refused_sync=int(out[7]), split_refused=int(out[8]), links=int(out[9]),
                 pool=int(out[10]), flips_link_neutral=bool(out[11]))
        return r, int(pool), kids[:out[12]], absd[:out[13]]
