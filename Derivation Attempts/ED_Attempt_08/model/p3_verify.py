"""Tier 1 and tier 2 of note 2's C5 validation ladder, for the port `p3.Slice3P` (E2).

Tier 1 - predicates and costs. For one shared state and one shared proposed move, the port agrees with
attempt 7's `c3c`/`c3f` exactly: the link condition, the four move plans, `n3_after_exact`, `delta_S`
(to 1e-12) and `allowed`'s budget, ceiling and sync gates together with their reason strings.

Tier 2 - scripted move sequences. A deterministic script of merges, splits, 2-3 flips and 3-2 flips,
chosen from vertex ids alone, leaves both codes on the same complex after every single move.

The two codes number tetrahedra differently and iterate sets in different orders (C5), so nothing here
is driven by a tetrahedron id or by set order: a tetrahedron is named by its sorted 4-tuple of vertex
ids, a face by the vertex it drops, an edge by its vertex pair, and a split's new vertex is carried in
a port-id -> reference-id dictionary that is translated in both directions.

No per-tick time is quoted for the port until both tiers pass.
"""
import os
import sys
import random
import traceback

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "ED_Attempt_07", "model"))
for _d in (REF_DIR, HERE):
    if _d not in sys.path:
        sys.path.insert(0, _d)

if not os.path.isfile(os.path.join(HERE, "p3.py")):
    print("p3.py is not in " + HERE + " yet. Nothing to verify; write the port first.")
    sys.exit(2)
try:
    import c3c
    import c3f
except Exception:
    print("attempt 7's reference did not import from " + REF_DIR)
    traceback.print_exc()
    sys.exit(2)
try:
    from p3 import Slice3P
except Exception:
    print("p3.py is there but `from p3 import Slice3P` failed.")
    traceback.print_exc()
    sys.exit(2)

SIZES = (6, 8)
SEED = 20260919
RAND_STEPS = 80                  # moves used to leave the pristine grid before either tier compares
T2_MOVES = 220                   # successful scripted moves per size (the ladder asks for 200)
MAX_SHOW = 2                     # mismatches printed in full, per kind, so no kind hides behind another
MAX_SHOW_ALL = 12
DS_PER_KIND = 150                # plans per move kind sent through n3_after_exact and delta_S
GATE_PER_KIND = 30               # plans per move kind sent through the gates
TOL = 1e-12
NEW = -(10 ** 9)                 # common label for the vertex a split has not created yet
UNMAPPED = 10 ** 9               # a port vertex the harness has no reference id for (a mapping bug)
POOLS = (-3, 0, 2, 10 ** 9)      # negative, zero, biting, never biting
SMAXES = (None, 0.0, 2.0, 1e9)   # off, refuses any strain, bites, never bites
CAPS = (60, 10)                  # the run's ceiling, and one that bites at grid degree 14
COSTS = ((1.0, 1.0), (1.0, 0.0), (0.0, 1.0))


# ---------------------------------------------------------------- reporting
class Report:
    """one tier's comparisons: how many, which kinds disagreed, the first few in full."""

    def __init__(self, name):
        self.name = name
        self.n = 0
        self.kinds = {}
        self.bad = []
        self.maxdiff = 0.0
        self.dsmax = 0.0
        self.crashes = []
        self.lines = []

    def show(self, kind, what, ref, port):
        seen = self.kinds.get(kind, 0)
        self.kinds[kind] = seen + 1
        if seen < MAX_SHOW and len(self.bad) < MAX_SHOW_ALL:
            self.bad.append((kind, what, ref, port))

    def cmp(self, kind, what, ref, port):
        self.n += 1
        if ref == port:
            return True
        self.show(kind, what, ref, port)
        return False

    def cmpf(self, kind, what, ref, port, tol=TOL):
        self.n += 1
        d = abs(float(ref) - float(port))
        if d == d and d > self.maxdiff:       # nan never raises the recorded maximum
            self.maxdiff = d
        if d == d and kind == "delta_S" and d > self.dsmax:
            self.dsmax = d
        if d <= tol:
            return True
        self.show(kind, what, "%.17g" % float(ref), "%.17g" % float(port))
        return False

    def crash(self, where):
        self.crashes.append((where, traceback.format_exc()))

    def ok(self):
        return not self.kinds and not self.crashes

    def summary(self):
        out = ["%s: %s, %d comparisons" % (self.name, "PASS" if self.ok() else "FAIL", self.n)]
        out.extend("  " + s for s in self.lines)
        if self.maxdiff:
            out.append("  largest absolute delta_S difference %.3e, largest float difference of any kind "
                       "%.3e (tolerance %.0e)" % (self.dsmax, self.maxdiff, TOL))
        for kind in sorted(self.kinds):
            out.append("  MISMATCH %s x%d" % (kind, self.kinds[kind]))
        for kind, what, ref, port in self.bad:
            out.append("  first detail [%s] at %r" % (kind, what))
            out.append("    reference: %r" % (ref,))
            out.append("    port     : %r" % (port,))
        for where, tb in self.crashes[:MAX_SHOW_ALL]:
            out.append("  CRASH in %s" % where)
            out.extend("    " + s for s in tb.rstrip().splitlines())
        return out


# ---------------------------------------------------------------- common labels
def mapv(p2r, x):
    return p2r.get(int(x), UNMAPPED + int(x))


def rkey(t, ynew=None):
    """a reference tetrahedron as a sorted 4-tuple in common labels."""
    return tuple(sorted(NEW if int(x) == ynew else int(x) for x in t))


def pkey(t, p2r, ynew=None):
    """a port tetrahedron in the same common labels."""
    return tuple(sorted(NEW if int(x) == ynew else mapv(p2r, x) for x in t))


def ref_plan_keys(Mref, plan, ynew=None):
    """(removed, added) as sorted lists of common-label 4-tuples; tids are not comparable across codes."""
    rem = sorted(rkey(Mref.tets[tid]) for tid in plan[0])
    add = sorted(rkey(t, ynew) for t in plan[1])
    return rem, add


def port_plan_keys(Mport, plan, p2r, ynew=None):
    rem = sorted(pkey(Mport.tet(int(tid)), p2r) for tid in plan[0])
    add = sorted(pkey(row, p2r, ynew) for row in np.asarray(plan[1]).reshape(-1, 4))
    return rem, add


def port_tid(Mport, key, r2p):
    """the port's tid for the tetrahedron named by a reference-space sorted 4-tuple."""
    t = tuple(sorted(r2p[x] for x in key))
    for tid in Mport.tets_of(t[0]):
        if tuple(int(z) for z in Mport.tet(int(tid))) == t:
            return int(tid)
    return -1


def port_tids(Mport):
    seen = set()
    for v in Mport.vertices():
        for tid in Mport.tets_of(int(v)):
            seen.add(int(tid))
    return seen


def port_edges(Mport, p2r):
    """{common-label vertex pair: valence}, walked from vertices and neighbour lists only."""
    out = {}
    for v in Mport.vertices():
        v = int(v)
        for a in Mport.neighbours(v):
            a = int(a)
            if a > v:
                ra, rb = mapv(p2r, v), mapv(p2r, a)
                out[(ra, rb) if ra < rb else (rb, ra)] = int(Mport.valence(v, a))
    return out


def ref_val3(Mref):
    return sorted(e for e, c in Mref.val.items() if c == 3)


# ---------------------------------------------------------------- state comparison
def compare_state(Mref, Mport, p2r, rep, tag):
    """everything the ladder's tier 2 names, after one move."""
    rep.cmp("V", tag, len(Mref.vt), int(Mport.V))
    rep.cmp("E", tag, len(Mref.val), int(Mport.E))
    rep.cmp("T", tag, len(Mref.tets), int(Mport.T))
    pv = [int(v) for v in Mport.vertices()]
    rep.cmp("vertices ascending", tag, True, pv == sorted(pv))
    rep.cmp("vertex set", tag, sorted(Mref.vt), sorted(mapv(p2r, v) for v in pv))
    rep.cmp("degree sequence", tag, sorted(len(Mref.nbrs[v]) for v in Mref.vt),
            sorted(int(Mport.degree(v)) for v in pv))
    pe = port_edges(Mport, p2r)
    rep.cmp("edge count", tag, len(Mref.val), len(pe))
    rep.cmp("valence multiset", tag, sorted(Mref.val.values()), sorted(pe.values()))
    rep.cmp("edge set", tag, sorted(Mref.val), sorted(pe))
    rep.cmp("n3", tag, len(Mref.val3), int(Mport.n3()))
    rep.cmp("n3 agrees with the valences", tag, len(Mref.val3), len(ref_val3(Mref)))
    ptids = port_tids(Mport)
    rep.cmp("tet count", tag, len(Mref.tets), len(ptids))
    rep.cmp("tetrahedra", tag, sorted(Mref.tets.values()),
            sorted(pkey(Mport.tet(tid), p2r) for tid in ptids))
    rep.cmp("check reference clean", tag, [], list(Mref.check()))
    rep.cmp("check port clean", tag, [], [str(s) for s in Mport.check()])


def compare_adjacency(Mref, Mport, p2r, rep, tag):
    """`adjacency()` returns its vertices in each code's own order, so compare the graph, not the order."""
    Ar, idr, posr, eir, ejr = Mref.adjacency()
    Ap, idp, posp, eip, ejp = Mport.adjacency()
    idr = [int(x) for x in idr]
    idp = [int(x) for x in idp]
    er = sorted(tuple(sorted((idr[int(i)], idr[int(j)]))) for i, j in zip(eir, ejr))
    ep = sorted(tuple(sorted((mapv(p2r, idp[int(i)]), mapv(p2r, idp[int(j)])))) for i, j in zip(eip, ejp))
    rep.cmp("adjacency shape", tag, tuple(Ar.shape), tuple(Ap.shape))
    rep.cmp("adjacency edges", tag, er, ep)
    rep.cmp("adjacency matches val", tag, sorted(Mref.val), er)
    rep.cmp("adjacency pos", tag, True, all(int(posp[v]) == i for i, v in enumerate(idp)))
    rep.cmp("adjacency degrees", tag,
            sorted(int(x) for x in np.asarray(Ar.sum(axis=1)).ravel()),
            sorted(int(x) for x in np.asarray(Ap.sum(axis=1)).ravel()))


# ---------------------------------------------------------------- shared move choices
def pick_merge(Mref, rng):
    """(v, a) in reference ids, from sorted lists only; None if this vertex has no contractible edge."""
    ids = sorted(Mref.vt)
    v = ids[rng.randrange(len(ids))]
    cands = [a for a in sorted(Mref.nbrs[v]) if Mref.link_condition(v, a)]
    if not cands:
        return None
    return v, cands[rng.randrange(len(cands))]


def pick_split(Mref, rng):
    ids = sorted(Mref.vt)
    x = ids[rng.randrange(len(ids))]
    opts = sorted(Mref.nbrs[x])
    if not opts:
        return None
    return x, opts[rng.randrange(len(opts))]


def pick_face(Mref, rng):
    """(sorted 4-tuple, the vertex the face drops) - a tetrahedron reached through a vertex, not a tid."""
    ids = sorted(Mref.vt)
    v = ids[rng.randrange(len(ids))]
    keys = sorted(Mref.tets[tid] for tid in Mref.vt[v])
    if not keys:
        return None
    key = keys[rng.randrange(len(keys))]
    return key, key[rng.randrange(4)]


def pick_val3(Mref, rng):
    v3 = ref_val3(Mref)
    if not v3:
        return None
    return v3[rng.randrange(len(v3))]


def flip23_pair(Mref, Mport, p2r, r2p, key, d, rep, label):
    """the same 2-3 in both codes. the face is named by the vertex it drops: each code sorts a
    tetrahedron by its own vertex ids, so a face index would not mean the same face after a split."""
    tid_p = port_tid(Mport, key, r2p)
    if not rep.cmp("tet lookup", label, True, tid_p >= 0):
        return None, None
    kp = tuple(int(z) for z in Mport.tet(tid_p))
    if not rep.cmp("tet contents", label, key, tuple(sorted(mapv(p2r, z) for z in kp))):
        return None, None
    ar = Mref.flip23_plan(Mref.tetkey[key], key.index(d))
    ap = Mport.flip23_plan(tid_p, kp.index(r2p[d]))
    if not rep.cmp("flip23 is None", label, ar is None, ap is None):
        return None, None
    return ar, ap


def flip32_pair(Mref, Mport, p2r, r2p, e, rep, label):
    rep.cmp("valence of the 3-2 edge", label, 3, int(Mport.valence(r2p[e[0]], r2p[e[1]])))
    br = Mref.flip32_plan(e)
    bp = Mport.flip32_plan(r2p[e[0]], r2p[e[1]])
    if not rep.cmp("flip32 is None", label, br is None, bp is None):
        return None, None
    return br, bp


# ---------------------------------------------------------------- scripted moves
def do_merge(Mref, Mport, p2r, r2p, rng, rep):
    pick = pick_merge(Mref, rng)
    if pick is None:
        return False
    v, a = pick
    if not rep.cmp("link_condition on a scripted merge", (v, a), True,
                   bool(Mport.link_condition(r2p[v], r2p[a]))):
        return False
    pr, pp = Mref.merge_plan(v, a), Mport.merge_plan(r2p[v], r2p[a])
    rep.cmp("merge_plan", (v, a), ref_plan_keys(Mref, pr), port_plan_keys(Mport, pp, p2r))
    Mref.merge(v, a)
    Mport.merge(r2p[v], r2p[a])
    del p2r[r2p[v]]
    del r2p[v]
    return True


def do_split(Mref, Mport, p2r, r2p, rng, rep):
    pick = pick_split(Mref, rng)
    if pick is None:
        return False
    x, u = pick
    want_r, want_p = Mref.next_id, int(Mport.next_free_vertex())
    pr = Mref.split_plan(x, u, want_r)
    pp = Mport.split_plan(r2p[x], r2p[u], want_p)
    rep.cmp("split_plan", (x, u), ref_plan_keys(Mref, pr, want_r), port_plan_keys(Mport, pp, p2r, want_p))
    yr = int(Mref.split(x, u))
    yp = int(Mport.split(r2p[x], r2p[u]))
    rep.cmp("next_id", (x, u), want_r, yr)
    rep.cmp("next_free_vertex", (x, u), True, yp == want_p)
    p2r[yp] = yr
    r2p[yr] = yp
    return True


def do_flip23(Mref, Mport, p2r, r2p, rng, rep):
    pick = pick_face(Mref, rng)
    if pick is None:
        return False
    key, d = pick
    ar, ap = flip23_pair(Mref, Mport, p2r, r2p, key, d, rep, (key, d))
    if ar is None or ap is None:
        return False
    if not rep.cmp("flip23_plan", (key, d), ref_plan_keys(Mref, ar), port_plan_keys(Mport, ap, p2r)):
        return False
    Mref.apply(ar[0], ar[1])
    Mport.apply(ap)
    return True


def do_flip32(Mref, Mport, p2r, r2p, rng, rep):
    e = pick_val3(Mref, rng)
    if e is None:
        return False
    br, bp = flip32_pair(Mref, Mport, p2r, r2p, e, rep, e)
    if br is None or bp is None:
        return False
    if not rep.cmp("flip32_plan", e, ref_plan_keys(Mref, br), port_plan_keys(Mport, bp, p2r)):
        return False
    Mref.apply(br[0], br[1])
    Mport.apply(bp)
    return True


def do_paired(Mref, Mport, p2r, r2p, rng, rep):
    """c3e's paired flip: one 2-3 and one 3-2 at disjoint places, applied as a single plan."""
    pick = pick_face(Mref, rng)
    if pick is None:
        return False
    key, d = pick
    ar, ap = flip23_pair(Mref, Mport, p2r, r2p, key, d, rep, (key, d))
    if ar is None or ap is None:
        return False
    e = pick_val3(Mref, rng)
    if e is None:
        return False
    br, bp = flip32_pair(Mref, Mport, p2r, r2p, e, rep, e)
    if br is None or bp is None:
        return False
    # the pairing rules, decided in common labels so both codes get the same answer
    if set(rkey(Mref.tets[t]) for t in ar[0]) & set(rkey(Mref.tets[t]) for t in br[0]):
        return False
    tri = set(br[1][0]) & set(br[1][1])
    for t in ar[1]:
        if tri <= set(t):
            return False
    plan_r = (list(ar[0]) + list(br[0]), list(ar[1]) + list(br[1]))
    plan_p = (np.concatenate([np.asarray(ar_p) for ar_p in (ap[0], bp[0])]).astype(np.int32),
              np.concatenate([np.asarray(ap[1]).reshape(-1, 4), np.asarray(bp[1]).reshape(-1, 4)]).astype(np.int32))
    if not rep.cmp("paired flip plan", (key, d, e),
                   ref_plan_keys(Mref, plan_r), port_plan_keys(Mport, plan_p, p2r)):
        return False
    Mref.apply(plan_r[0], plan_r[1])
    Mport.apply(plan_p)
    return True


SCRIPT = {"merge": do_merge, "split": do_split, "flip23": do_flip23, "flip32": do_flip32}
KINDS = ("merge", "split", "flip23", "flip32")


# ---------------------------------------------------------------- randomise
def randomise(Mref, Mport, seed, steps=RAND_STEPS, rep=None):
    """Leave the pristine grid in both codes at once.

    Paired flips and splits/merges, every choice made from vertex ids and sorted lists only, so the two
    codes take the same sequence of moves and land on the same complex - which is then verified. Returns
    (p2r, r2p): the port-id -> reference-id map and its inverse, identity at the start and kept in step
    by hand through every split and merge.
    """
    own = rep if rep is not None else Report("randomise")
    rng = random.Random(seed)
    p2r = {v: v for v in sorted(Mref.vt)}
    r2p = dict(p2r)
    own.cmp("randomise start", "vertices", sorted(Mref.vt), sorted(int(v) for v in Mport.vertices()))
    done = {"paired": 0, "split": 0, "merge": 0}
    tries = 0
    plan = ("paired", "paired", "paired", "split", "merge")
    while sum(done.values()) < steps and tries < steps * 40:
        tries += 1
        kind = plan[rng.randrange(len(plan))]
        if kind == "paired":
            ok = do_paired(Mref, Mport, p2r, r2p, rng, own)
        elif kind == "split":
            ok = do_split(Mref, Mport, p2r, r2p, rng, own)
        else:
            ok = do_merge(Mref, Mport, p2r, r2p, rng, own)
        if ok:
            done[kind] += 1
    compare_state(Mref, Mport, p2r, own, "after randomise")
    compare_adjacency(Mref, Mport, p2r, own, "after randomise")
    own.lines.append("randomise seed %d: %d paired flips, %d splits, %d merges in %d attempts; "
                     "V %d E %d T %d" % (seed, done["paired"], done["split"], done["merge"], tries,
                                         len(Mref.vt), len(Mref.val), len(Mref.tets)))
    return p2r, r2p


# ---------------------------------------------------------------- tier 1
def take(plans, rng, per_kind):
    """a deterministic stratified sample, so every move kind reaches the costs and the gates."""
    by = {}
    for i, p in enumerate(plans):
        by.setdefault(p["kind"], []).append(i)
    keep = []
    for k in sorted(by):
        idx = by[k]
        if len(idx) > per_kind:
            idx = [idx[j] for j in sorted(rng.sample(range(len(idx)), per_kind))]
        keep.extend(idx)
    return [plans[i] for i in sorted(keep)]


def tier1(n, rep):
    Mref = c3c.Slice3(n)
    Mport = Slice3P(n)
    rep.cmp("start V", n, len(Mref.vt), int(Mport.V))
    rep.cmp("start T", n, len(Mref.tets), int(Mport.T))
    rep.cmp("start vertices", n, n ** 3, len(Mref.vt))
    rep.cmp("start tetrahedra", n, 6 * n ** 3, len(Mref.tets))
    p2r, r2p = randomise(Mref, Mport, SEED + n, rep=rep)
    rng = random.Random(SEED * 7 + n)

    # tick counts, the same in both codes, spread so the sync gate has something to refuse
    phi = {}
    for v in sorted(Mref.vt):
        x = 0.01 * rng.random()            # /(SIGMA/K) = up to about 10 normalized units
        phi[v] = x
        Mport.set_phi(r2p[v], x)
        Mport.set_b(r2p[v], 1.0 + (v % 3) * 0.25)
        Mport.set_omega(r2p[v], 1.0)
    for v in sorted(Mref.vt):
        rep.cmpf("set_phi/get_phi", v, phi[v], float(Mport.get_phi(r2p[v])), 0.0)
        rep.cmpf("set_b/get_b", v, 1.0 + (v % 3) * 0.25, float(Mport.get_b(r2p[v])), 0.0)

    verts = sorted(Mref.vt)
    plans = []

    # accessors and the link condition over every vertex and every neighbour
    for v in verts:
        nb = [int(a) for a in Mport.neighbours(r2p[v])]
        rep.cmp("neighbours ascending", v, True, nb == sorted(nb))
        rep.cmp("neighbours", v, sorted(Mref.nbrs[v]), sorted(mapv(p2r, a) for a in nb))
        rep.cmp("degree", v, len(Mref.nbrs[v]), int(Mport.degree(r2p[v])))
        rep.cmp("tets_of", v, sorted(rkey(Mref.tets[t]) for t in Mref.vt[v]),
                sorted(pkey(Mport.tet(int(t)), p2r) for t in Mport.tets_of(r2p[v])))
        for a in sorted(Mref.nbrs[v]):
            rep.cmp("valence", (v, a), Mref.val[c3c.ekey(v, a)], int(Mport.valence(r2p[v], r2p[a])))
            lr = bool(Mref.link_condition(v, a))
            lp = bool(Mport.link_condition(r2p[v], r2p[a]))
            if not rep.cmp("link_condition", (v, a), lr, lp) or not lr:
                continue
            pr, pp = Mref.merge_plan(v, a), Mport.merge_plan(r2p[v], r2p[a])
            rep.cmp("merge_plan", (v, a), ref_plan_keys(Mref, pr), port_plan_keys(Mport, pp, p2r))
            plans.append(dict(kind="merge", label=("merge", v, a), pr=pr, pp=pp,
                              gone_r=(v,), gone_p=r2p[v], xr=None, xp=(-1, 0.0)))

    # the valence of a pair that is not an edge is 0 in both
    for _ in range(200):
        a, b = verts[rng.randrange(len(verts))], verts[rng.randrange(len(verts))]
        if a == b:
            continue
        rep.cmp("valence of any pair", (a, b), Mref.val.get(c3c.ekey(a, b), 0),
                int(Mport.valence(r2p[a], r2p[b])))

    # split plans: every neighbour of a sample of vertices, the unborn child under a common label
    want_r, want_p = Mref.next_id, int(Mport.next_free_vertex())
    rep.cmp("next vertex is free in the port", n, False, want_p in p2r)
    sample = verts if len(verts) <= 40 else [verts[i] for i in sorted(rng.sample(range(len(verts)), 40))]
    for x in sample:
        for u in sorted(Mref.nbrs[x]):
            pr = Mref.split_plan(x, u, want_r)
            pp = Mport.split_plan(r2p[x], r2p[u], want_p)
            rep.cmp("split_plan", (x, u), ref_plan_keys(Mref, pr, want_r),
                    port_plan_keys(Mport, pp, p2r, want_p))
            plans.append(dict(kind="split", label=("split", x, u), pr=pr, pp=pp,
                              gone_r=(), gone_p=-1, xr={want_r: phi[x]}, xp=(want_p, phi[x])))

    # 2-3 flips over a sample of (tetrahedron, dropped vertex)
    seen = set()
    for _ in range(600):
        pick = pick_face(Mref, rng)
        if pick is None or pick in seen:
            continue
        seen.add(pick)
        key, d = pick
        ar, ap = flip23_pair(Mref, Mport, p2r, r2p, key, d, rep, (key, d))
        if ar is None or ap is None:
            continue
        rep.cmp("flip23_plan", (key, d), ref_plan_keys(Mref, ar), port_plan_keys(Mport, ap, p2r))
        plans.append(dict(kind="flip23", label=("flip23", key, d), pr=ar, pp=ap,
                          gone_r=(), gone_p=-1, xr=None, xp=(-1, 0.0)))

    # 3-2 flips over every valence-3 edge
    v3 = ref_val3(Mref)
    rep.cmp("n3", n, len(Mref.val3), int(Mport.n3()))
    rep.cmp("n3 agrees with the valences", n, len(Mref.val3), len(v3))
    for e in v3:
        br, bp = flip32_pair(Mref, Mport, p2r, r2p, e, rep, e)
        if br is None or bp is None:
            continue
        rep.cmp("flip32_plan", e, ref_plan_keys(Mref, br), port_plan_keys(Mport, bp, p2r))
        plans.append(dict(kind="flip32", label=("flip32", e), pr=br, pp=bp,
                          gone_r=(), gone_p=-1, xr=None, xp=(-1, 0.0)))

    # the counts and the costs
    for p in take(plans, rng, DS_PER_KIND):
        rep.cmp("n3_after_exact", p["label"], c3c.n3_after_exact(Mref, p["pr"]),
                int(Mport.n3_after_exact(p["pp"])))
        for alpha, lam in COSTS:
            dr = Mref.delta_S(p["pr"][0], p["pr"][1], alpha, lam, 0.0, phi, p["xr"])
            dp = float(Mport.delta_S(p["pp"], alpha, lam, p["xp"][0], p["xp"][1]))
            rep.cmpf("delta_S", (p["label"], alpha, lam), dr, dp)

    # the gates, with their reasons
    why = {}
    for p in take(plans, rng, GATE_PER_KIND):
        for pool in POOLS:
            for s_max in SMAXES:
                for cap in CAPS:
                    a = c3f.allowed(Mref, p["pr"], pool, phi, s_max, gone=p["gone_r"], cap=cap)
                    b = Mport.allowed(p["pp"], pool, s_max, gone=p["gone_p"], cap=cap)
                    why[a[3] or "passed"] = why.get(a[3] or "passed", 0) + 1
                    rep.cmp("allowed (%s)" % p["kind"], (p["label"], pool, s_max, cap),
                            (bool(a[0]), int(a[1]), int(a[2]), str(a[3])),
                            (bool(b[0]), int(b[1]), int(b[2]), str(b[3])))
    rep.lines.append("n=%d: gate outcomes compared - %s"
                     % (n, ", ".join("%s %d" % (k, why[k]) for k in sorted(why))))
    for k in ("budget", "cap", "sync", "passed"):
        rep.cmp("the %s gate was exercised" % k, n, True, why.get(k, 0) > 0)

    kinds = {}
    for p in plans:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    rep.lines.append("n=%d: %d plans built (%s); %d vertices, %d edges, %d tetrahedra, %d valence-3 edges"
                     % (n, len(plans), ", ".join("%s %d" % (k, kinds[k]) for k in sorted(kinds)),
                        len(Mref.vt), len(Mref.val), len(Mref.tets), len(v3)))
    rep.cmp("every move kind reached tier 1", n, set(KINDS), set(kinds))


# ---------------------------------------------------------------- tier 2
def tier2(n, rep):
    Mref = c3c.Slice3(n)
    Mport = Slice3P(n)
    p2r, r2p = randomise(Mref, Mport, SEED + n, rep=rep)
    rng = random.Random(SEED * 13 + n)
    lo, hi = n ** 3 // 2, 2 * n ** 3
    done = {k: 0 for k in KINDS}
    applied = tries = 0
    while applied < T2_MOVES and tries < T2_MOVES * 60:
        tries += 1
        kind = KINDS[rng.randrange(4)]
        if kind == "merge" and len(Mref.vt) <= lo:      # keep the complex from draining away
            kind = "split"
        elif kind == "split" and len(Mref.vt) >= hi:
            kind = "merge"
        if not SCRIPT[kind](Mref, Mport, p2r, r2p, rng, rep):
            continue
        applied += 1
        done[kind] += 1
        compare_state(Mref, Mport, p2r, rep, "n=%d move %d %s" % (n, applied, kind))
        if applied % 50 == 0:
            print("  n=%d: %d moves scripted, V=%d E=%d T=%d" %
                  (n, applied, len(Mref.vt), len(Mref.val), len(Mref.tets)), flush=True)
    compare_adjacency(Mref, Mport, p2r, rep, "n=%d end of script" % n)
    rep.cmp("200 successful moves", n, True, applied >= 200)
    rep.cmp("every move kind scripted", n, True, all(done[k] > 0 for k in KINDS))
    rep.lines.append("n=%d: %d moves applied in %d attempts (%s); ends at V %d E %d T %d"
                     % (n, applied, tries, ", ".join("%s %d" % (k, done[k]) for k in KINDS),
                        len(Mref.vt), len(Mref.val), len(Mref.tets)))


# ---------------------------------------------------------------- main
def main():
    lines = ["p3 verification: tier 1 and tier 2 of note 2's C5 ladder",
             "reference %s" % REF_DIR,
             "port      %s" % os.path.join(HERE, "p3.py"),
             "seed %d, sizes %s, %d randomising moves, %d scripted moves per size"
             % (SEED, ", ".join("n=%d" % n for n in SIZES), RAND_STEPS, T2_MOVES), ""]
    reps = []
    for tier, fn in ((1, tier1), (2, tier2)):
        for n in SIZES:
            rep = Report("tier %d, n=%d" % (tier, n))
            print("running %s ..." % rep.name, flush=True)
            try:
                fn(n, rep)
            except Exception:
                rep.crash(rep.name)
            reps.append((tier, rep))
            print("\n".join(rep.summary()), flush=True)

    for tier in (1, 2):
        rs = [r for t, r in reps if t == tier]
        total = sum(r.n for r in rs)
        worst = max([r.dsmax for r in rs] + [0.0])
        lines.append("TIER %d: %s, %d comparisons" % (tier, "PASS" if all(r.ok() for r in rs) else "FAIL", total))
        for r in rs:
            lines.extend(r.summary())
        if tier == 1:
            lines.append("largest absolute delta_S difference over tier 1: %.3e (tolerance %.0e)" % (worst, TOL))
        lines.append("")

    ok = all(r.ok() for _, r in reps)
    lines.append("RESULT: %s. %s" % ("both tiers pass" if ok else "a tier failed",
                                     "Tier 3 and timings may follow." if ok else
                                     "Any tier-1 or tier-2 disagreement is a port bug; no timing is quoted."))
    text = "\n".join(lines) + "\n"
    print()
    print(text, end="")
    open(os.path.join(HERE, "p3_verify.txt"), "w", encoding="utf-8").write(text)
    return 0 if ok else 1


sys.exit(main())
