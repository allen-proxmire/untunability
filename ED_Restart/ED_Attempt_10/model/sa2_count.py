"""Recount with general splits (note 9, C18; Allen D10 choice (ii); 'a' = run as specified, D11).

Moves: general vertex split (simple cycle C, length >= 3, in the link sphere Lk(x); the child y takes one of the two discs),
link-condition merge, 2-3 and 3-2 flips. Self-inverse, so one count covers histories into and out of a slice.
a_v = split options of v + merge options of v + flip sites touching v (apportioned). s = ln e_m(a) / V, m = round(0.1 V).

Split options of x: sum over simple cycles C of Lk(x) avoiding link vertices already at the ceiling (they would gain y),
of the number of sides D with deg(y) = |V(D)| + 1 <= 60 and deg(x) = |V(D')| + 1 <= 60. For deg(x) < 60 both sides always
pass, so options = 2 x #cycles. For deg(x) = 60 a side passes iff the OTHER side has an interior vertex (flood fill).
Exact DFS for deg(x) <= DEG_EXACT; Knuth (1975) random-probe estimate above, PROBES probes; floor: cycles of length <= 6.

Checks, expectations and exit (C18), written before this run:
  R0  on n = 6 slices (flat; grown 30 ticks at q = 1), every counted split applied to a copy gives a clean structure
      check, merging the child back restores the original exactly, and every allowed merge's reverse is among the
      counted splits (bijection).
  R1  for vertices of degree <= 10, 2 x #cycles equals a brute-force count of link-triangle subsets forming a disc with
      a simple boundary cycle.
  R2  at degree 18-24, the Knuth estimate is within 3 standard errors of the exact count.
  Expectation (about 75 per cent): grown slices far above the flat reference FREF2.
  Margin = 2 x seed difference + 2 x per-event estimation error.
  R0-R2 fail -> code problem, fixed and rerun, recorded.
  every grown slice above FREF2 by the margin -> 'with general splits, counting leans toward crowded slices at one tick';
      stage B not built as specified; take stock of road S on paper with Allen.
  FREF2 above every grown slice by the margin -> 'counting leans toward flat at one tick'; stage B with general splits.
  otherwise -> too close; take stock.
"""
import json
import math
import os
import sys
import time
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sa_count as sc                                           # noqa: E402

CAP = 60
DEG_EXACT = 24
PROBES = 20000
FLOOR_LEN = 6
OUT = os.path.join(HERE, "sa2_runs")
ONE = np.uint64(1)


# ------------------------------------------------------------------ link sphere
def link_of(M, x):
    """Local link sphere of x: vertex list, adjacency masks, triangles (local), triangle neighbours across edges."""
    tets = [M.tet(int(t)) for t in M.tets_of(x)]
    tris = [tuple(w for w in t if w != x) for t in tets]
    verts = sorted(set(w for tr in tris for w in tr))
    idx = {w: i for i, w in enumerate(verts)}
    n = len(verts)
    adj = np.zeros(n, dtype=np.uint64)
    T = np.array([[idx[a], idx[b], idx[c]] for a, b, c in tris], dtype=np.int64)
    for a, b, c in T:
        for p, q in ((a, b), (b, c), (a, c)):
            adj[p] |= ONE << np.uint64(q)
            adj[q] |= ONE << np.uint64(p)
    edge_tris = {}
    for i, (a, b, c) in enumerate(T):
        for p, q in ((a, b), (b, c), (a, c)):
            edge_tris.setdefault((min(p, q), max(p, q)), []).append(i)
    nb = np.full((len(T), 3), -1, dtype=np.int64)
    for i, (a, b, c) in enumerate(T):
        for k, (p, q) in enumerate(((a, b), (b, c), (a, c))):
            o = [j for j in edge_tris[(min(p, q), max(p, q))] if j != i]
            nb[i, k] = o[0]
    return verts, adj, T, nb, tets


@njit(cache=True)
def _popc(x):
    c = 0
    while x:
        x &= x - np.uint64(1)
        c += 1
    return c


@njit(cache=True)
def _lowbit(x):
    i = 0
    while not (x >> np.uint64(i)) & np.uint64(1):
        i += 1
    return i


@njit(cache=True)
def _nth_bit(x, k):
    c = 0
    for i in range(64):
        if (x >> np.uint64(i)) & np.uint64(1):
            if c == k:
                return i
            c += 1
    return -1


@njit(cache=True)
def _sides(path, L, n, T, nb):
    """Interior-vertex counts of the two sides of cycle path[0..L-1]: (int_A, int_B)."""
    pos = np.full(n, -1, dtype=np.int64)
    for i in range(L):
        pos[path[i]] = i
    nt = T.shape[0]
    side = np.full(nt, -1, dtype=np.int64)
    stack = np.empty(nt, dtype=np.int64)
    ncomp = 0
    for st in range(nt):
        if side[st] >= 0:
            continue
        side[st] = ncomp
        sp = 0
        stack[sp] = st
        sp += 1
        while sp > 0:
            sp -= 1
            t = stack[sp]
            for k in range(3):
                if k == 0:
                    p, q = T[t, 0], T[t, 1]
                elif k == 1:
                    p, q = T[t, 1], T[t, 2]
                else:
                    p, q = T[t, 0], T[t, 2]
                a, b = pos[p], pos[q]
                if a >= 0 and b >= 0 and (abs(a - b) == 1 or abs(a - b) == L - 1):
                    continue                                  # a cycle edge: do not cross
                o = nb[t, k]
                if side[o] < 0:
                    side[o] = ncomp
                    stack[sp] = o
                    sp += 1
        ncomp += 1
    va = np.zeros(n, dtype=np.uint8)
    for t in range(nt):
        if side[t] == 0:
            for j in range(3):
                va[T[t, j]] = 1
    ia = 0
    ib = 0
    for v in range(n):
        if pos[v] >= 0:
            continue
        if va[v]:
            ia += 1
        else:
            ib += 1
    return ia, ib, ncomp


@njit(cache=True)
def count_exact(adj, n, ok, maxlen, full_x, T, nb):
    """Sum over simple cycles (length 3..maxlen) avoiding ~ok vertices of the number of valid sides.
    full_x: x is at the ceiling (side valid iff the other side has an interior vertex)."""
    total = 0
    path = np.empty(n + 1, dtype=np.int64)
    cand = np.zeros(n + 1, dtype=np.uint64)
    for s in range(n):
        if not (ok >> np.uint64(s)) & ONE:
            continue
        above = ok & ~((ONE << np.uint64(s + 1)) - ONE) if s < 63 else np.uint64(0)
        path[0] = s
        visited = ONE << np.uint64(s)
        cand[0] = adj[s] & above
        d = 0
        while d >= 0:
            if cand[d] == 0:
                if d > 0:
                    visited &= ~(ONE << np.uint64(path[d]))
                d -= 1
                continue
            w = _lowbit(cand[d])
            cand[d] &= ~(ONE << np.uint64(w))
            d += 1
            path[d] = w
            visited |= ONE << np.uint64(w)
            if d >= 2 and (adj[w] >> np.uint64(s)) & ONE:
                if full_x:
                    ia, ib, nc = _sides(path, d + 1, n, T, nb)
                    total += (1 if ib > 0 else 0) + (1 if ia > 0 else 0)
                else:
                    total += 2
            if d + 1 < maxlen:
                cand[d] = adj[w] & above & ~visited
            else:
                cand[d] = np.uint64(0)
    return total // 2            # each cycle closed in both directions


@njit(cache=True)
def count_knuth(adj, n, ok, full_x, T, nb, probes, seed):
    """Knuth estimate of the same sum (all lengths). Returns (mean, standard error)."""
    np.random.seed(seed)
    starts = np.empty(n, dtype=np.int64)
    ns = 0
    for s in range(n):
        if (ok >> np.uint64(s)) & ONE:
            starts[ns] = s
            ns += 1
    if ns == 0:
        return 0.0, 0.0
    path = np.empty(n + 1, dtype=np.int64)
    acc = 0.0
    acc2 = 0.0
    for _ in range(probes):
        s = starts[np.random.randint(ns)]
        W = float(ns)
        above = ok & ~((ONE << np.uint64(s + 1)) - ONE) if s < 63 else np.uint64(0)
        path[0] = s
        visited = ONE << np.uint64(s)
        cand = adj[s] & above
        d = 0
        est = 0.0
        while cand:
            k = _popc(cand)
            W *= k
            w = _nth_bit(cand, np.random.randint(k))
            d += 1
            path[d] = w
            visited |= ONE << np.uint64(w)
            if d >= 2 and (adj[w] >> np.uint64(s)) & ONE:
                if full_x:
                    ia, ib, nc = _sides(path, d + 1, n, T, nb)
                    est += W * ((1 if ib > 0 else 0) + (1 if ia > 0 else 0))
                else:
                    est += W * 2
            cand = adj[w] & above & ~visited
        est *= 0.5
        acc += est
        acc2 += est * est
    mean = acc / probes
    var = max(acc2 / probes - mean * mean, 0.0)
    return mean, math.sqrt(var / probes)


def split_options(M, x, deg_of, exact_max=DEG_EXACT, probes=PROBES, seed=0, floor_len=FLOOR_LEN):
    verts, adj, T, nb, _ = link_of(M, x)
    n = len(verts)
    ok = np.uint64(0)
    for i, w in enumerate(verts):
        if deg_of(w) < CAP:
            ok |= ONE << np.uint64(i)
    full_x = n >= CAP
    floor = count_exact(adj, n, ok, floor_len, full_x, T, nb)
    if n <= exact_max:
        v = count_exact(adj, n, ok, n + 1, full_x, T, nb)
        return float(v), 0.0, floor, True
    m, se = count_knuth(adj, n, ok, full_x, T, nb, probes, seed)
    return m, se, floor, False


# ------------------------------------------------------------------ apply a general split (for R0)
def split_general(M, x, cycle_local, side, verts, T, nb):
    """Apply the split of x along cycle (local indices, in order) giving side 'side' (0/1 flood component) to new y."""
    from p3_ops import vert_new
    L = len(cycle_local)
    path = np.array(cycle_local, dtype=np.int64)
    pos = {c: i for i, c in enumerate(cycle_local)}
    nt = len(T)
    comp = [-1] * nt
    c = 0
    for st in range(nt):
        if comp[st] >= 0:
            continue
        comp[st] = c
        stack = [st]
        while stack:
            t = stack.pop()
            for k, (p, q) in enumerate(((T[t, 0], T[t, 1]), (T[t, 1], T[t, 2]), (T[t, 0], T[t, 2]))):
                if p in pos and q in pos and abs(pos[p] - pos[q]) in (1, L - 1):
                    continue
                o = int(nb[t, k])
                if comp[o] < 0:
                    comp[o] = c
                    stack.append(o)
        c += 1
    tids = [int(t) for t in M.tets_of(x)]
    y = int(vert_new(M.S))
    rem, add = [], []
    for i, tid in enumerate(tids):
        if comp[i] == side:
            rem.append(tid)
            a, b, cc = (verts[j] for j in T[i])
            add.append((y, a, b, cc))
    for i in range(L):
        p, q = verts[cycle_local[i]], verts[cycle_local[(i + 1) % L]]
        add.append((x, y, p, q))
    M.apply((np.array(rem, dtype=np.int32), np.array(add, dtype=np.int32)))
    return y


def enumerate_cycles(adj, n, ok):
    """All simple cycles (as local-index lists), each once."""
    out = []

    def dfs(s, path, visited):
        w = path[-1]
        for u in range(s + 1, n):
            if not (int(adj[w]) >> u) & 1 or not (int(ok) >> u) & 1 or (visited >> u) & 1:
                continue
            path.append(u)
            if len(path) >= 3 and (int(adj[u]) >> s) & 1 and path[1] < path[-1]:
                out.append(list(path))
            dfs(s, path, visited | (1 << u))
            path.pop()

    for s in range(n):
        if (int(ok) >> s) & 1:
            dfs(s, [s], 1 << s)
    return out


# ------------------------------------------------------------------ R0, R1, R2
def check_R(seed=5):
    from h5_select import copy_state
    res = dict(R0=[], R1=[], R2=[])
    slices = []
    M, pool, BL, V0 = sc.fresh3(6, seed)
    slices.append(("flat", M))
    G, pool, BL, V0 = sc.fresh3(6, seed)
    sc.grow3(G, pool, BL, V0, 30, 1.0, dict(structure=True, budget=True, link=True))
    slices.append(("grown", G))
    for name, M in slices:
        deg = {int(v): len(M.neighbours(int(v))) for v in M.vertices()}
        nsplit = nbad = nrestore_bad = 0
        rng = np.random.default_rng(17)
        targets = [v for v in deg if deg[v] <= 16][:20]
        cyc_sets = {}
        for x in targets:
            verts, adj, T, nb, _ = link_of(M, x)
            n = len(verts)
            ok = np.uint64(0)
            for i, w in enumerate(verts):
                if deg[w] < CAP:
                    ok |= ONE << np.uint64(i)
            cyc = enumerate_cycles(adj, n, ok)
            cyc_sets[x] = set(frozenset(verts[i] for i in cy) for cy in cyc)
            cnt = count_exact(adj, n, ok, n + 1, n >= CAP, T, nb)
            if cnt != 2 * len(cyc):
                nbad += 1
            before = sorted(tuple(sorted(M.tet(int(t)))) for t in M.S.t_items[:M.T])
            pick = rng.choice(len(cyc), size=min(150, len(cyc)), replace=False)   # SAMPLE (revision: all is hours)
            for ci in pick:
                cy = cyc[int(ci)]
                for side in (0, 1):
                    C = copy_state(M)
                    y = split_general(C, x, cy, side, verts, T, nb)
                    nsplit += 1
                    if C.check() or max(len(C.neighbours(int(w))) for w in C.vertices()) > CAP:
                        nbad += 1
                        continue
                    if not C.link_condition(y, x):
                        nrestore_bad += 1
                        continue
                    C.merge(y, x)
                    after = sorted(tuple(sorted(C.tet(int(t)))) for t in C.S.t_items[:C.T])
                    if after != before:
                        nrestore_bad += 1
        # reverse direction (sampled, 200 merges): apply an allowed merge v -> a to a copy; in the merged slice, Lk(va)
        # must be a counted cycle of a (simple cycle of ok vertices), and the split along it giving v's side back must
        # restore the original slice exactly.
        miss = 0
        nmerge = 0
        before = sorted(tuple(sorted(M.tet(int(t)))) for t in M.S.t_items[:M.T])
        allm = []
        for v in list(deg):
            for a in [int(u) for u in M.neighbours(v)]:
                if M.link_condition(v, a):
                    pl = M.merge_plan(v, a)
                    if pl is not None and M.allowed(pl, sc.BIG, None, gone=v, cap=CAP)[0]:
                        allm.append((v, a))
        for j in rng.choice(len(allm), size=min(200, len(allm)), replace=False):
            v, a = allm[int(j)]
            nmerge += 1
            common = set(int(w) for w in M.neighbours(v)) & set(int(w) for w in M.neighbours(a))
            vside = set(int(w) for w in M.neighbours(v)) - common - {a}
            C = copy_state(M)
            C.merge(v, a)
            verts, adj, T, nb, _ = link_of(C, a)
            idx = {w: i for i, w in enumerate(verts)}
            cdeg = {int(w): len(C.neighbours(int(w))) for w in verts}
            # the cycle's order comes from the link of the edge va in the original slice (tets holding both v and a)
            cedges = [tuple(w for w in M.tet(int(t)) if w not in (v, a)) for t in M.tets_of(v) if a in M.tet(int(t))]
            nbr = {}
            for p_, q_ in cedges:
                nbr.setdefault(p_, []).append(q_)
                nbr.setdefault(q_, []).append(p_)
            okc = all(cdeg[w] < CAP for w in common) and all(len(x_) == 2 for x_ in nbr.values())
            if not okc or set(nbr) != common:
                miss += 1
                continue
            seq = [next(iter(common))]
            while len(seq) < len(common):
                nx_ = [u for u in nbr[seq[-1]] if u not in seq]
                if not nx_:
                    break
                seq.append(nx_[0])
            order = [idx[w] for w in seq]
            if len(order) != len(common) or not all((int(adj[order[i]]) >> order[(i + 1) % len(order)]) & 1
                                                    for i in range(len(order))):
                miss += 1
                continue
            restored = False
            for side in (0, 1):
                D = copy_state(C)
                y = split_general(D, a, order, side, verts, T, nb)
                ny = set(int(w) for w in D.neighbours(y)) - common - {a}
                if ny == vside:
                    got = sorted(tuple(sorted(v if w == y else w for w in D.tet(int(t)))) for t in D.S.t_items[:D.T])
                    restored = got == before
                    break
            if not restored:
                miss += 1
        res["R0"].append(dict(slice=name, splits_applied=nsplit, bad=nbad, restore_bad=nrestore_bad,
                              merges=nmerge, merges_missing=miss))
        # R1: brute-force discs for degree <= 10
        for x in [v for v in deg if deg[v] <= 10][:25]:
            verts, adj, T, nb, _ = link_of(M, x)
            n = len(verts)
            ok = np.uint64(0)
            for i, w in enumerate(verts):
                if deg[w] < CAP:
                    ok |= ONE << np.uint64(i)
            cnt = count_exact(adj, n, ok, n + 1, False, T, nb)
            res["R1"].append(dict(slice=name, deg=n, dfs=int(cnt), brute=brute_discs(T, n, ok)))
    # R2: exact vs Knuth at degree 18-24, on a W1-type slice at n = 10
    G, pool, BL, V0 = sc.fresh3(10, 3)
    sc.grow3(G, pool, BL, V0, 60, 1.0, dict(structure=True, budget=True, link=True))
    deg = {int(v): len(G.neighbours(int(v))) for v in G.vertices()}
    picks = [v for v in deg if 18 <= deg[v] <= 24][:12]
    for x in picks:
        verts, adj, T, nb, _ = link_of(G, x)
        n = len(verts)
        ok = np.uint64(0)
        for i, w in enumerate(verts):
            if deg[w] < CAP:
                ok |= ONE << np.uint64(i)
        ex = count_exact(adj, n, ok, n + 1, False, T, nb)
        m, se = count_knuth(adj, n, ok, False, T, nb, PROBES, 11)
        res["R2"].append(dict(deg=n, exact=int(ex), est=m, se=se, z=(m - ex) / se if se > 0 else 0.0))
    return res


def brute_discs(T, n, ok):
    """Count link-triangle subsets forming a disc with a simple boundary cycle whose vertices are all 'ok'."""
    nt = len(T)
    edges_of = [((T[i, 0], T[i, 1]), (T[i, 1], T[i, 2]), (T[i, 0], T[i, 2])) for i in range(nt)]
    cnt = 0
    for mask in range(1, (1 << nt) - 1):
        sel = [i for i in range(nt) if (mask >> i) & 1]
        ec = {}
        for i in sel:
            for p, q in edges_of[i]:
                k = (min(p, q), max(p, q))
                ec[k] = ec.get(k, 0) + 1
        bd = [k for k, c in ec.items() if c == 1]
        if len(bd) < 3:
            continue
        bdeg = {}
        for p, q in bd:
            bdeg[p] = bdeg.get(p, 0) + 1
            bdeg[q] = bdeg.get(q, 0) + 1
        if any(d != 2 for d in bdeg.values()):
            continue
        if any(not (int(ok) >> int(p)) & 1 for p in bdeg):
            continue
        # boundary connected (one cycle)
        adjb = {}
        for p, q in bd:
            adjb.setdefault(p, []).append(q)
            adjb.setdefault(q, []).append(p)
        start = bd[0][0]
        seen = {start}
        st = [start]
        while st:
            u = st.pop()
            for w in adjb[u]:
                if w not in seen:
                    seen.add(w)
                    st.append(w)
        if len(seen) != len(bdeg):
            continue
        # triangles connected across interior edges, and Euler characteristic 1
        sset = set(sel)
        vs = set(p for i in sel for p in T[i])
        if len(vs) - len(ec) + len(sel) != 1:
            continue
        cnt += 1
    return cnt


# ------------------------------------------------------------------ the count
def options3g(M, seed):
    """a_v with general splits: merges and flips as in sa_count.options3 (edge splits dropped), plus split options."""
    arr0, deg, tot = sc.options3(M)
    verts = [int(v) for v in M.vertices()]
    dmap = {v: int(d) for v, d in zip(verts, deg)}
    # remove sa_count's edge-split options (one per allowed neighbour) from arr0
    from p3_ops import vert_new  # noqa: F401
    y = M.next_free_vertex()
    esplit = np.zeros(len(verts))
    for i, v in enumerate(verts):
        for u in [int(w) for w in M.neighbours(v)]:
            pl = M.split_plan(v, u, y)
            if pl is not None and M.allowed(pl, sc.BIG, None, cap=CAP)[0]:
                esplit[i] += 1
    base = arr0 - esplit
    sp = np.zeros(len(verts))
    se = np.zeros(len(verts))
    fl = np.zeros(len(verts))
    exact = np.zeros(len(verts), dtype=bool)
    for i, v in enumerate(verts):
        m, s, f, ex = split_options(M, v, lambda w: dmap[w], seed=seed * 100003 + i)
        sp[i], se[i], fl[i], exact[i] = m, s, f, ex
    return base, sp, se, fl, exact, deg, tot


def summarise_g(base, sp, se, fl, exact, deg, md, V):
    a = base + sp
    a_floor = base + fl
    m = int(round(sc.Q * V))
    s = sc.log_em(a, m) / V
    s_floor = sc.log_em(a_floor, m) / V
    rel = np.where(a > 0, se / np.maximum(a, 1e-300), 0.0)
    err = float(np.sum(np.log1p(np.minimum(rel, 1e6))) / V)          # conservative per-event error of s
    return dict(V=int(V), m=m, s=s, s_floor=s_floor, s_err=err, ln_split_mean=float(np.mean(np.log(np.maximum(sp, 1)))),
                ln_split_max=float(np.max(np.log(np.maximum(sp, 1)))), frac_exact=float(exact.mean()),
                rel_se_max=float(rel.max()), deg_mean=float(np.mean(deg)), deg_sd=float(np.std(deg)),
                deg_max=int(np.max(deg)), mean_distance=md)


def do_job(job):
    kind, seed = job
    path = os.path.join(OUT, "3D_%s_s%d.json" % (kind, seed))
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    if kind == "FREF2":
        import sa_flatref2 as fr
        M, _, _, _ = fr.build(0)
        ok = dict(structure=not M.check())
    else:
        M, ok = sc.slice3(kind, 24, seed)
    base, sp, se, fl, exact, deg, tot = options3g(M, seed)
    out = summarise_g(base, sp, se, fl, exact, deg, sc.mean_distance(M.adjacency()[0], seed), M.V)
    out.update(kind=kind, seed=seed, ok=ok, seconds=time.perf_counter() - t0)
    json.dump(out, open(path, "w", encoding="utf-8"))
    return path, out["seconds"]


JOBS = [("FREF2", 0), ("FL", 0), ("F1", 0), ("F1", 1), ("W1", 0), ("W1", 1)]


def report():
    L = []
    rp = os.path.join(OUT, "R.json")
    if os.path.exists(rp):
        R = json.load(open(rp, encoding="utf-8"))
        r0 = all(r["bad"] == 0 and r["restore_bad"] == 0 and r["merges_missing"] == 0 for r in R["R0"])
        r1 = all(r["dfs"] == r["brute"] for r in R["R1"])
        r2 = all(abs(r["z"]) <= 3 for r in R["R2"])
        L.append("R0 %s %s" % (r0, R["R0"]))
        L.append("R1 %s (%d vertices) %s" % (r1, len(R["R1"]), [(r["deg"], r["dfs"], r["brute"]) for r in R["R1"]]))
        L.append("R2 %s %s" % (r2, [(r["deg"], r["exact"], round(r["est"]), round(r["z"], 2)) for r in R["R2"]]))
        rok = r0 and r1 and r2
    else:
        rok = False
    rows = {}
    for kind, seed in JOBS:
        p = os.path.join(OUT, "3D_%s_s%d.json" % (kind, seed))
        if os.path.exists(p):
            rows[(kind, seed)] = json.load(open(p, encoding="utf-8"))
    for (k, s), r in rows.items():
        L.append("%-5s s%d V %5d s %.5f floor %.5f err %.5f | ln(split) mean %.2f max %.2f | exact %.2f relse_max %.3f | "
                 "deg %.2f sd %.2f max %d | md %.3f | ok %s" % (k, s, r["V"], r["s"], r["s_floor"], r["s_err"],
                                                                r["ln_split_mean"], r["ln_split_max"], r["frac_exact"],
                                                                r["rel_se_max"], r["deg_mean"], r["deg_sd"], r["deg_max"],
                                                                r["mean_distance"], all(r["ok"].values())))
    if len(rows) == len(JOBS):
        ref = rows[("FREF2", 0)]
        grown = {"%s_s%d" % k: rows[k] for k in (("F1", 0), ("F1", 1), ("W1", 0), ("W1", 1))}
        spread = max(abs(rows[("F1", 0)]["s"] - rows[("F1", 1)]["s"]), abs(rows[("W1", 0)]["s"] - rows[("W1", 1)]["s"]))
        est = max(r["s_err"] for r in rows.values())
        margin = 2 * spread + 2 * est
        L.append("seed spread %.5f, max est err %.5f, margin %.5f" % (spread, est, margin))
        L.append("grown - FREF2: " + ", ".join("%s %+.5f (floor %+.5f)" % (g, r["s"] - ref["s"], r["s_floor"] - ref["s"])
                                               for g, r in grown.items()))
        if not rok:
            L.append("VERDICT: R0-R2 failed - code problem.")
        elif all(r["s"] - ref["s"] > margin for r in grown.values()):
            L.append("VERDICT: with general splits, counting leans toward crowded slices at one tick -> take stock of road S.")
        elif all(ref["s"] - r["s"] > margin for r in grown.values()):
            L.append("VERDICT: counting leans toward flat at one tick -> stage B with general splits.")
        else:
            L.append("VERDICT: too close -> take stock.")
    text = "\n".join(L)
    open(os.path.join(HERE, "sa2_count.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    rp = os.path.join(OUT, "R.json")
    if not os.path.exists(rp):
        R = check_R()
        json.dump(R, open(rp, "w", encoding="utf-8"), default=float)
    report()
    if "--checks-only" in sys.argv:
        return 0
    from multiprocessing import Pool
    t0 = time.perf_counter()
    with Pool(6) as p:
        for path, sec in p.imap_unordered(do_job, sorted(JOBS, key=lambda j: j[0] in ("W1", "F1"), reverse=True)):
            print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec, (time.perf_counter() - t0) / 3600),
                  flush=True)
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
