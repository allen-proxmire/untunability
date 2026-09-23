"""Stage A (note 3, C7; Allen D3 and C-Q1..C-Q4 yes, D4): which way does counting lean?

For each slice, count the one-tick histories: the number of ways to make m = round(0.1 V) changes at distinct
events (C-Q3), each change one of ED's allowed single moves. Per event v, a_v = merges of v into a neighbour
(link condition), splits of v (3D: along one neighbour, attempt 7's edge split; 2D: along a pair of neighbours,
attempt 7's C3a split), and flip sites touching v, apportioned equally over the vertices each flip touches.
The ceiling (60 links) applies; the link budget is balanced over the tick (C-Q2) and so not applied per move
(labelled). n(S) = e_m(a_1..a_V), computed in log space. s(S) = ln n(S) / V. The move set is its own inverse
(a merge undoes a split, a flip undoes a flip), so histories into S and out of S have the same count by
construction: reported once.

Expected results, written down before this run (C7):
  A0  the counting rule matches a brute-force count (apply each candidate change to a copy and keep those that
      leave a valid slice within the ceiling) exactly on small slices, 2D and 3D.
  A1  grown slices pass the structure and budget checks exactly every tick; flat counts are deterministic.
  A2  Claude's honest expectation, low confidence: the crammed and rewired slices have the higher count.
Exit (C7):
  A0 or A1 fails: code problem, fixed and rerun, recorded.
  3D: flat higher than every non-flat slice by more than twice the seed difference -> "counting leans toward flat
      at one tick": go on to stage B.
  3D: a crammed slice higher than flat by that margin -> "with ED's slice-to-slice step, counting leans toward
      small worlds": stage B not built; what joins one slice to the next goes to Allen on paper.
  otherwise: too close; build stage B small in 2D.
  2D reported alongside; the decision is taken on 3D.
"""
import json
import math
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
A8 = os.path.join(HERE, "..", "..", "ED_Attempt_08", "model")
A9 = os.path.join(HERE, "..", "..", "ED_Attempt_09", "model")
A7 = os.path.join(HERE, "..", "..", "ED_Attempt_07", "model")
for p in (A8, A9):
    sys.path.insert(0, p)

Q = 0.1
CAP = 60
BIG = 10 ** 9
OUT = os.path.join(HERE, "sa_runs")


# ---------------------------------------------------------------- shared
def log_em(a, m):
    """ln of the elementary symmetric polynomial e_m(a) (unordered sets of m changes at distinct events)."""
    L = np.full(m + 1, -np.inf)
    L[0] = 0.0
    for x in a:
        if x <= 0:
            continue
        L[1:] = np.logaddexp(L[1:], L[:-1] + math.log(x))
    return float(L[m])


def summarise(a, deg, md, V):
    m = int(round(Q * V))
    ln_n = log_em(a, m)
    abar = float(np.mean(a))
    spread_part = log_em(a / abar, m) / V
    return dict(V=int(V), m=m, s=ln_n / V, s_density=m * math.log(abar) / V, s_spread=spread_part,
                a_mean=abar, a_sd=float(np.std(a)), deg_mean=float(np.mean(deg)), deg_sd=float(np.std(deg)),
                deg_max=int(np.max(deg)), mean_distance=md)


def mean_distance(A, seed):
    from readings import bfs_distances
    rng = np.random.default_rng(900 + seed)
    src = rng.choice(A.shape[0], size=min(200, A.shape[0]), replace=False)
    d = bfs_distances(A, src)
    return float(d[np.isfinite(d)].mean())


# ---------------------------------------------------------------- 3D
def options3(M, brute=False):
    """Per-vertex option counts (dict v -> a_v) and per-type totals. brute: also return the candidate sets."""
    from p3 import flip32_plan, B_A
    from p3_ops import C_T, C_V3
    S = M.S
    verts = [int(v) for v in M.vertices()]
    a = {v: 0.0 for v in verts}
    tot = dict(merge=0, split=0, f23=0.0, f32=0)
    sets = dict(merge=set(), split=set(), f23=set(), f32=set())
    y = M.next_free_vertex()
    for v in verts:
        for u in [int(x) for x in M.neighbours(v)]:
            if M.link_condition(v, u):
                pl = M.merge_plan(v, u)
                if pl is not None and M.allowed(pl, BIG, None, gone=v, cap=CAP)[0]:
                    a[v] += 1
                    tot["merge"] += 1
                    sets["merge"].add((v, u))
            pl = M.split_plan(v, u, y)
            if pl is not None and M.allowed(pl, BIG, None, cap=CAP)[0]:
                a[v] += 1
                tot["split"] += 1
                sets["split"].add((v, u))
    for tid in [int(t) for t in S.t_items[:S.ctr[C_T]]]:
        for f in range(4):
            pl = M.flip23_plan(tid, f)
            if pl is None or not M.allowed(pl, BIG, None, cap=CAP)[0]:
                continue
            touched = sorted(set(int(x) for x in pl[1].ravel()))
            key = tuple(touched)
            if key in sets["f23"]:
                continue                                     # the same triangle, seen from its other tet
            sets["f23"].add(key)
            tot["f23"] += 1
            for w in touched:
                a[w] += 1.0 / len(touched)
    for slot in [int(s) for s in S.e3_items[:S.ctr[C_V3]]]:
        nr, na = flip32_plan(S, slot, B_A)
        if nr < 0:
            continue
        pl = (S.buf_rem[B_A:B_A + nr].copy(), S.buf_add[B_A:B_A + na].copy())
        if not M.allowed(pl, BIG, None, cap=CAP)[0]:
            continue
        touched = sorted(set(int(x) for x in pl[1].ravel()))
        sets["f32"].add((int(S.e_a[slot]), int(S.e_b[slot])))
        tot["f32"] += 1
        for w in touched:
            a[w] += 1.0 / len(touched)
    arr = np.array([a[v] for v in verts])
    deg = np.array([len(M.neighbours(v)) for v in verts])
    return (arr, deg, tot, sets) if brute else (arr, deg, tot)


def brute3(M):
    """Apply every candidate change to a copy; valid = structure check clean and ceiling respected."""
    from h5_select import copy_state
    from p3 import flip32_plan, B_A
    from p3_ops import C_T, C_V3, vert_free
    S = M.S
    good = dict(merge=set(), split=set(), f23=set(), f32=set())

    def ok_after(C):
        if C.check():
            return False
        return max(len(C.neighbours(int(w))) for w in C.vertices()) <= CAP

    verts = [int(v) for v in M.vertices()]
    for v in verts:
        for u in [int(x) for x in M.neighbours(v)]:
            C = copy_state(M)
            pl = C.merge_plan(v, u)
            if pl is not None:
                try:
                    C.apply(pl)
                    vert_free(C.S, v)
                    if ok_after(C):
                        good["merge"].add((v, u))
                except Exception:
                    pass
            C = copy_state(M)
            try:
                C.split(v, u)
                if ok_after(C):
                    good["split"].add((v, u))
            except Exception:
                pass
    for tid in [int(t) for t in S.t_items[:S.ctr[C_T]]]:
        for f in range(4):
            pl = M.flip23_plan(tid, f)
            if pl is None:
                continue
            key = tuple(sorted(set(int(x) for x in pl[1].ravel())))
            C = copy_state(M)
            try:
                C.apply(pl)
                if ok_after(C):
                    good["f23"].add(key)
            except Exception:
                pass
    for slot in [int(s) for s in S.e3_items[:S.ctr[C_V3]]]:
        nr, na = flip32_plan(S, slot, B_A)
        if nr < 0:
            continue
        pl = (S.buf_rem[B_A:B_A + nr].copy(), S.buf_add[B_A:B_A + na].copy())
        C = copy_state(M)
        try:
            C.apply(pl)
            if ok_after(C):
                good["f32"].add((int(S.e_a[slot]), int(S.e_b[slot])))
        except Exception:
            pass
    return good


def fresh3(n, seed):
    from p9 import Slice9P
    from p3_core import SIGMA, FLAT_LINKS_PER_EVENT
    M = Slice9P(n)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    return M, BL - M.E, BL, V0


def grow3(M, pool, BL, V0, ticks, q, ok):
    for _ in range(ticks):
        r, pool, k, a = M.tick9(0.0, 0.0, pool, q=q, flip_frac=1.0)
        if M.check():
            ok["structure"] = False
        if abs(float(M.S.b[M.vertices()].sum()) - V0) > 1e-9 * V0:
            ok["budget"] = False
        if M.E + pool != BL:
            ok["link"] = False
    return pool


def paired_randomize(M, sweeps):
    """Flat with random PAIRED flips (note 3): link-neutral, as the tick's flip phase with no cost, sweeps x V/2
    attempts. (The calibration randomizer flip_randomize uses single flips and crumples; not what note 3 names.)"""
    from p3 import paired_flip_plan, B_C
    from p3_ops import n3_after, apply_plan, C_V3, C_V
    from p3_core import rng_float
    S = M.S
    acc = 0
    for _ in range(sweeps * int(S.ctr[C_V]) // 2):
        nr, na = paired_flip_plan(S, S.rs)
        if nr < 0:
            continue
        pl = (S.buf_rem[B_C:B_C + nr].copy(), S.buf_add[B_C:B_C + na].copy())
        if not M.allowed(pl, BIG, None, cap=CAP)[0]:
            continue
        n3a = max(int(n3_after(S, B_C, nr, na)), 1)
        corr = S.ctr[C_V3] / n3a
        if corr >= 1.0 or rng_float(S.rs) < corr:
            apply_plan(S, B_C, nr, na)
            acc += 1
    return acc


def slice3(kind, n, seed):
    if kind == "FRc":
        # REVISION (recorded before any result was read): the flat grid has no 3-2 sites, so paired flips cannot
        # move it and FR equals flat. The rewired stand-in is attempt 8's calibration randomised slice (single
        # uniform flips, 50 sweeps, seed 7, raised capacities as f1_calibrate.py), crumpled and off the link budget.
        from p9 import Slice9P
        M = Slice9P(n, t_cap=24 * n ** 3, e_cap=24 * n ** 3)
        M.seed(7)
        M.flip_randomize(50)
        return M, dict(structure=not M.check())
    M, pool, BL, V0 = fresh3(n, seed)
    ok = dict(structure=True, budget=True, link=True)
    if kind == "FR":
        paired_randomize(M, 50)
    elif kind == "F1":
        grow3(M, pool, BL, V0, 150, Q, ok)
    elif kind == "W1":
        pool = grow3(M, pool, BL, V0, 150, 1.0, ok)
        grow3(M, pool, BL, V0, 150, Q, ok)
    return M, ok


# ---------------------------------------------------------------- 2D
def _c3a():
    if A7 not in sys.path:
        sys.path.insert(0, A7)
    import c3a
    return c3a


def flip2_valid(T, v, a):
    R = T.ring[v]
    if len(R) < 4 or len(T.ring[a]) < 4:
        return None
    p = R.index(a)
    c1, c2 = R[(p + 1) % len(R)], R[p - 1]
    if c1 == c2 or c2 in T.ring[c1]:
        return None
    if len(T.ring[c1]) + 1 > CAP or len(T.ring[c2]) + 1 > CAP:
        return None
    return c1, c2


def flip2_apply(T, v, a):
    R = T.ring[v]
    p = R.index(a)
    c1, c2 = R[(p + 1) % len(R)], R[p - 1]
    R.remove(a)
    T.ring[a].remove(v)
    r1 = T.ring[c1]
    r1.insert(r1.index(v) + 1, c2)
    r2 = T.ring[c2]
    r2.insert(r2.index(a) + 1, c1)


def split2_ok(T, v, i, j):
    k = len(T.ring[v])
    return j - i + 2 <= CAP and k - (j - i) + 2 <= CAP and \
        len(T.ring[T.ring[v][i]]) + 1 <= CAP and len(T.ring[T.ring[v][j]]) + 1 <= CAP


def collapse2_ok(T, v, a):
    return T.collapse_ok(v, a) and len(T.ring[v]) + len(T.ring[a]) - 4 <= CAP


def options2(T, brute=False):
    a = {v: 0.0 for v in T.ring}
    tot = dict(merge=0, split=0, flip=0)
    sets = dict(merge=set(), split=set(), flip=set())
    for v, R in T.ring.items():
        for (i, j, _, _) in T.split_options(v):
            if split2_ok(T, v, i, j):
                a[v] += 1
                tot["split"] += 1
                sets["split"].add((v, i, j))
        for u in R:
            if collapse2_ok(T, v, u):
                a[v] += 1
                tot["merge"] += 1
                sets["merge"].add((v, u))
            if v < u:
                c = flip2_valid(T, v, u)
                if c is not None:
                    tot["flip"] += 1
                    sets["flip"].add((v, u))
                    for w in (v, u, c[0], c[1]):
                        a[w] += 0.25
    ids = list(T.ring)
    arr = np.array([a[v] for v in ids])
    deg = np.array([len(T.ring[v]) for v in ids])
    return (arr, deg, tot, sets) if brute else (arr, deg, tot)


def copy2(T):
    c3a = _c3a()
    C = c3a.Torus.__new__(c3a.Torus)
    C.ring = {k: list(v) for k, v in T.ring.items()}
    C.next_id = T.next_id
    return C


def brute2(T):
    good = dict(merge=set(), split=set(), flip=set())

    def ok_after(C):
        return not C.check() and max(len(r) for r in C.ring.values()) <= CAP

    for v, R in T.ring.items():
        for (i, j, _, _) in T.split_options(v):
            C = copy2(T)
            try:
                C.split(v, i, j)
                if ok_after(C):
                    good["split"].add((v, i, j))
            except Exception:
                pass
        for u in R:
            C = copy2(T)
            try:
                C.collapse(v, u)
                if ok_after(C):
                    good["merge"].add((v, u))
            except Exception:
                pass
            if v < u:
                C = copy2(T)
                try:
                    if len(C.ring[v]) >= 2:
                        flip2_apply(C, v, u)
                        if ok_after(C):
                            good["flip"].add((v, u))
                except Exception:
                    pass
    return good


def slice2(kind, n, seed):
    c3a = _c3a()
    T = c3a.Torus(n)
    ok = dict(structure=True, budget=True)
    if kind == "R":
        c3a.flip_randomize(T, 200, np.random.default_rng(7))
    elif kind in ("U", "Q1"):
        lam = None if kind == "U" else 1.0
        b = {v: 1.0 for v in T.ring}
        rng = np.random.default_rng(seed)
        L = n * n
        for _ in range(1000):
            c3a.grow_tick(T, b, rng, lam)
            if T.check():
                ok["structure"] = False
            if abs(sum(b.values()) - L) > 1e-9 * L:
                ok["budget"] = False
    return T, ok


# ---------------------------------------------------------------- jobs
def a0_job(dim):
    """Brute-force check on small slices: flat, randomized, grown."""
    res = []
    if dim == 3:
        for kind in ("flat", "rand", "grown"):
            M, pool, BL, V0 = fresh3(6, 5)
            if kind == "rand":
                M.flip_randomize(50)
            elif kind == "grown":
                grow3(M, pool, BL, V0, 30, 1.0, dict(structure=True, budget=True, link=True))
            arr, deg, tot, sets = options3(M, brute=True)
            good = brute3(M)
            res.append(dict(kind=kind, V=M.V, counted={k: len(v) for k, v in sets.items()},
                            brute={k: len(v) for k, v in good.items()},
                            match={k: sets[k] == good[k] for k in sets}))
    else:
        c3a = _c3a()
        for kind in ("flat", "rand", "grown"):
            T = c3a.Torus(8)
            if kind == "rand":
                c3a.flip_randomize(T, 200, np.random.default_rng(7))
            elif kind == "grown":
                b = {v: 1.0 for v in T.ring}
                rng = np.random.default_rng(3)
                for _ in range(50):
                    c3a.grow_tick(T, b, rng, None)
            arr, deg, tot, sets = options2(T, brute=True)
            good = brute2(T)
            res.append(dict(kind=kind, V=len(T.ring), counted={k: len(v) for k, v in sets.items()},
                            brute={k: len(v) for k, v in good.items()},
                            match={k: sets[k] == good[k] for k in sets}))
    return res


def do_job(job):
    dim, kind, seed = job
    path = os.path.join(OUT, "%dD_%s_s%d.json" % (dim, kind, seed))
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    if dim == 3:
        M, ok = slice3(kind, 24, seed)
        arr, deg, tot = options3(M)
        A = M.adjacency()[0]
        out = summarise(arr, deg, mean_distance(A, seed), M.V)
        if kind == "FL":                                  # determinism: count twice
            arr2, _, _ = options3(M)
            ok["deterministic"] = bool(np.array_equal(arr, arr2))
    else:
        T, ok = slice2(kind, 80, seed)
        arr, deg, tot = options2(T)
        A = T.adjacency()[0]
        out = summarise(arr, deg, mean_distance(A, seed), len(T.ring))
        if kind == "F":
            arr2, _, _ = options2(T)
            ok["deterministic"] = bool(np.array_equal(arr, arr2))
    out.update(dim=dim, kind=kind, seed=seed, ok=ok, totals=tot, seconds=time.perf_counter() - t0)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(out, f)
    os.replace(tmp, path)
    return path, out["seconds"]


JOBS = [(3, "FL", 0), (3, "FR", 0), (3, "FRc", 0), (3, "F1", 0), (3, "F1", 1), (3, "W1", 0), (3, "W1", 1),
        (2, "F", 0), (2, "R", 0), (2, "U", 0), (2, "U", 1), (2, "Q1", 0), (2, "Q1", 1)]


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.perf_counter()
    a0p = os.path.join(OUT, "A0.json")
    if not os.path.exists(a0p):
        with Pool(2) as p:
            r3, r2 = p.map(a0_job, [3, 2])
        json.dump(dict(d3=r3, d2=r2), open(a0p, "w", encoding="utf-8"), indent=1)
    a0 = json.load(open(a0p, encoding="utf-8"))
    print("A0", json.dumps(a0), flush=True)
    order = sorted(JOBS, key=lambda j: (j[1] in ("Q1", "W1", "F1", "U", "FRc")), reverse=True)
    with Pool(6) as p:
        for path, sec in p.imap_unordered(do_job, order):
            print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec, (time.perf_counter() - t0) / 3600),
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
