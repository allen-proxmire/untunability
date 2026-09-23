"""Stage B starts (note 14, C24): the flat reference at ED's density for any n, and the crowded start (same slice,
randomized by single flips at fixed V with the link count in a window, ended exactly at E)."""
import math
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sa_count as sc                                           # noqa: E402


def flat_reference(n, seed=0):
    """Grid of side n with valence-6 then valence-4 edge splits (ED's own move) until links = round(F V) exactly."""
    from p3_core import FLAT_LINKS_PER_EVENT as F
    from p10 import Slice10P
    M, pool, BL, V0 = sc.fresh3(n, seed)
    E0 = M.E
    plan = None
    for b in range(0, 40):
        for a in range(0, V0):
            if E0 + 5 * a + 7 * b == round(F * (V0 + a + b)):
                plan = (a, b)
                break
            if E0 + 5 * a + 7 * b < F * (V0 + a + b) - 10:
                break
        if plan:
            break
    if plan is None:
        raise RuntimeError("no exact split plan for n=%d" % n)
    a_need, b_need = plan
    edges = M.edges()
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(edges))
    used = set()
    for val, need in ((6, b_need), (4, a_need)):
        done = 0
        for i in order:
            if done == need:
                break
            x, u = int(edges[i, 0]), int(edges[i, 1])
            if x in used or u in used or M.valence(x, u) != val:
                continue
            M.split(x, u)
            used.update((x, u))
            done += 1
        if done != need:
            raise RuntimeError("ran out of valence-%d links" % val)
    M.__class__ = Slice10P
    vs = M.vertices()
    M.S.b[vs] = 1.0
    M.S.phi[vs] = 0.0
    M.S.omega[vs] = 1.0
    assert M.E == round(F * M.V) and not M.check()
    return M


def crowded(M0, seed=1, sweeps=100, window=None):
    """Single 2-3 / 3-2 flips with uniform-measure corrections (as A8's flip_randomize), links held in [E, E + window]
    (default 5 per cent of E), within the ceiling; then biased flips (note 5's construction, beta 6) down to E exactly.
    REVISION: a window of 8 barely moved the slice, and 3-2-only descent could stall."""
    from h5_select import copy_state
    from p3 import flip23_plan, flip32_plan, B_A
    from p3_ops import n3_after, apply_plan, C_T, C_V3, C_E, C_V
    from p10 import Slice10P
    M = copy_state(M0)
    M.__class__ = Slice10P
    S = M.S
    E0 = int(S.ctr[C_E])
    if window is None:
        window = int(0.05 * E0)
    rng = np.random.default_rng(seed)
    for _ in range(sweeps * int(S.ctr[C_V])):
        if rng.random() < 0.5:
            if S.ctr[C_E] >= E0 + window:
                continue
            tid = S.t_items[int(rng.integers(S.ctr[C_T]))]
            nr, na = flip23_plan(S, tid, int(rng.integers(4)), B_A)
            if nr < 0:
                continue
            corr = 2.0 * S.ctr[C_T] / max(int(n3_after(S, B_A, nr, na)), 1)
        else:
            if S.ctr[C_V3] == 0 or S.ctr[C_E] <= E0:
                continue
            slot = S.e3_items[int(rng.integers(S.ctr[C_V3]))]
            nr, na = flip32_plan(S, slot, B_A)
            if nr < 0:
                continue
            corr = S.ctr[C_V3] / (2.0 * (S.ctr[C_T] - 1))
        pl = (S.buf_rem[B_A:B_A + nr].copy(), S.buf_add[B_A:B_A + na].copy())
        if not M.allowed(pl, 10 ** 9, None, cap=60)[0]:
            continue
        nr, na = M._load(pl)
        if corr >= 1.0 or rng.random() < corr:
            apply_plan(S, B_A, nr, na)
    import sa_flatref as fr                                  # descend to E exactly: biased flips, as note 5
    fr.to_budget(M, E0, seed, beta=6.0, max_attempts=20_000_000)
    if S.ctr[C_E] != E0 or M.check():
        raise RuntimeError("crowded start failed: E %d vs %d" % (S.ctr[C_E], E0))
    return M


def crowded_grown(target, seed=0, T=150, n_grid=None):
    """Strongly crowded start at EXACT counts (note 16 option (a), D16): attempt 9's growth (tick with general merges, q = 1,
    flips on - the H1/W1 recipe) from a grid of side n_grid, with the link budget set from the start to the target's link
    count; then the event count brought to the target exactly (general link-condition merges of random events, or edge
    splits), then the link count exactly (flips biased toward the target)."""
    from p10 import Slice10P
    from p3_core import SIGMA
    import math as _m
    V_t, E_t = target.V, target.E
    if n_grid is None:
        n_grid = int(round(V_t ** (1 / 3))) + 1
    M = Slice10P(n_grid, t_cap=24 * n_grid ** 3, e_cap=24 * n_grid ** 3)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = V_t / V0                                  # budget total = target events, so the balance aims there
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    pool = E_t - M.E
    for _ in range(T):
        r, pool, k, a = M.tick10(0.0, 0.0, pool, q=1.0, flip_frac=1.0, narrow=False)
    grown = dict(V=M.V, E=M.E)
    # events to the target exactly
    tries = 0
    while M.V != V_t and tries < 10 ** 6:
        tries += 1
        vs = M.vertices()
        v = int(vs[int(rng.integers(len(vs)))])
        nb = M.neighbours(v)
        a = int(nb[int(rng.integers(len(nb)))])
        if M.V > V_t:
            if M.link_condition(v, a):
                pl = M.merge_plan(v, a)
                if pl is not None and M.allowed(pl, 10 ** 9, None, gone=v, cap=60)[0]:
                    M.merge(v, a)
        else:
            pl = M.split_plan(v, a, M.next_free_vertex())
            if pl is not None and M.allowed(pl, 10 ** 9, None, cap=60)[0]:
                M.split(v, a)
    # links to the target exactly: biased single flips toward E_t
    from p3 import flip23_plan, flip32_plan, B_A
    from p3_ops import apply_plan, C_T, C_V3, C_E
    S = M.S
    tries = 0
    while S.ctr[C_E] != E_t and tries < 5 * 10 ** 7:
        tries += 1
        up = S.ctr[C_E] < E_t
        if up:
            tid = S.t_items[int(rng.integers(S.ctr[C_T]))]
            nr, na = flip23_plan(S, tid, int(rng.integers(4)), B_A)
        else:
            if S.ctr[C_V3] == 0:
                tid = S.t_items[int(rng.integers(S.ctr[C_T]))]       # make a 3-2 site when none exists
                nr, na = flip23_plan(S, tid, int(rng.integers(4)), B_A)
            else:
                nr, na = flip32_plan(S, S.e3_items[int(rng.integers(S.ctr[C_V3]))], B_A)
        if nr < 0:
            continue
        pl = (S.buf_rem[B_A:B_A + nr].copy(), S.buf_add[B_A:B_A + na].copy())
        if not M.allowed(pl, 10 ** 9, None, cap=60)[0]:
            continue
        nr, na = M._load(pl)
        apply_plan(S, B_A, nr, na)
    vs = M.vertices()
    M.S.b[vs] = 1.0
    M.S.phi[vs] = 0.0
    M.S.omega[vs] = 1.0
    if M.V != V_t or M.E != E_t or M.check():
        raise RuntimeError("crowded_grown failed: V %d/%d E %d/%d" % (M.V, V_t, M.E, E_t))
    M.grown = grown
    return M
