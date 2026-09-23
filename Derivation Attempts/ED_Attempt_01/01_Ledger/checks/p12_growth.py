"""Check C185: does seeded growth with even births and P12-driven rewiring give 3D space? (RD29, RD32, RD33)

The world (test settings, not ED rules, unless marked):
  Seed: 4 loci, all linked to each other.
  Birth (RD29, even everywhere): pick an existing locus v uniformly at random; a new locus links to v
    and to 2 random loci within 2 steps of v (local, so no long shortcuts). Every birth adds 3 links,
    so the average is 6 links per locus. Growth stops at 1,728 loci (a 12^3 lattice's count).
  Rewiring (RD32): a locus u moves one of its links u-v to a locus w two steps away. New links get
    a random phase (P09). Accepted if the P12 score improves, or with chance exp(-change / T).
  Phase settling (P09): a random link's phase shifts by up to +-pi/2 under the same rule.
  Schedule: 10 rewiring and 10 phase moves after every birth, then 15 sweeps (15 x links) of each.
  T = 0.3 throughout (ED has no temperature; a setting).

P12 for links (C184, accepted by Allen as RD33). Energy E, lower preferred:
  E = 1.0 x Str + 1.0 x Grad - 0.25 x Coh
  Str  = sum over loci of (links - 6)^2                       (link load against a comfortable load of 6: a setting)
  Grad = sum over links x-y of (links_x - links_y)^2 + 0.1 x (squares_x - squares_y)^2   (difference from neighbours)
  Coh  = sum over square loops of cos(flux)          "sum" reading: more loops that fit is better
     or  -(sum over square loops of (1 - cos(flux)))  "Wilson" reading: only misfit counts (C181)
  flux = sum of the four link phases around the loop.

Runs: FULL (Str + Grad + Coh sum), NO_COH, NO_GRAD, NO_STR, WILSON (Str + Grad + Coh Wilson).
Control: 12^3 periodic cubic lattice; growth dimension from a 6^3 to a 12^3 lattice.
Measured: pieces, share in the largest piece, exact mean distance in the largest piece, spectral
dimension d_s (lazy walk, t = 16 to 64, up to 40 starts), squares per locus, perfect-lattice share,
link spread, growth dimension D_g = ln 8 / ln(mean distance at 1,728 / mean distance at 216).
"3D-like" means: largest piece > 90%, d_s within 0.5 of control, mean distance within 30% of
control, and D_g within 0.7 of 3.

Predictions frozen before the first run (2026-09-13):
  P0  Control: perfect lattice, mean distance 9 x 1728 / 1727 = 9.00521.
  P1  FULL clumps: largest piece below 50% or more than 20 squares per locus.
      (The sum reading rewards dense pockets full of fitting squares.) Medium-high confidence.
  P2  NO_COH is a tangle: fewer than 3 squares per locus and mean distance below 0.8 x control. Medium.
  P3  NO_GRAD clumps (as P1). High.
  P4  NO_STR clumps (as P1). Medium.
  P5  WILSON is a tangle (as P2): with Wilson's cost, nothing rewards having loops. Medium.
  P6  None of the five runs is 3D-like. Medium-high.

Changes after freezing (2026-09-13):
  1. Before the first run, a garbled flux line in phase_move was fixed (predictions unchanged).
  2. First run (p12_growth_run1.txt): P0 and P6 RIGHT; P1-P5 WRONG. No run clumped or tangled:
     all five came out connected, glass-like and too high-dimensional (growth dimension 4.2-5.1).
     The original verdicts are still printed. The exit code now checks that the recorded
     first-run results reproduce (Q0-Q5), not whether the predictions were right.
"""
import math
import sys

import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components, shortest_path

N_FINAL, SNAP = 1728, 216
T = 0.3
W_STR, W_GRAD, W_COH = 1.0, 1.0, 0.25
MOVES_PER_BIRTH, RELAX_SWEEPS = 10, 15


class World:
    def __init__(self, rng, use_str, use_grad, coh):
        self.rng, self.use_str, self.use_grad, self.coh = rng, use_str, use_grad, coh
        self.adj, self.d, self.q, self.phase = [], [], [], {}
        for _ in range(4):
            self.adj.append(set()); self.d.append(0); self.q.append(0)
        for a in range(4):
            for b in range(a + 1, 4):
                self.add_link(a, b, rng.uniform(-math.pi, math.pi))
        self.acc = [0, 0]
        self.tries = [0, 0]

    # phases on oriented links
    def ph(self, a, b):
        return self.phase[(a, b)] if a < b else -self.phase[(b, a)]

    def set_ph(self, a, b, x):
        if a < b:
            self.phase[(a, b)] = x
        else:
            self.phase[(b, a)] = -x

    def f(self, flux):
        return math.cos(flux) if self.coh == "sum" else -(1 - math.cos(flux))

    def squares(self, u, v):
        out = []
        Nv = self.adj[v]
        for a in self.adj[u]:
            if a == v:
                continue
            for b in self.adj[a] & Nv:
                if b != u:
                    out.append((a, b))
        return out

    def add_link(self, x, y, phi):
        self.adj[x].add(y); self.adj[y].add(x)
        self.set_ph(x, y, phi)
        self.d[x] += 1; self.d[y] += 1
        for a, b in self.squares(x, y):
            for z in (x, y, a, b):
                self.q[z] += 1

    def birth(self):
        rng = self.rng
        v = int(rng.integers(len(self.adj)))
        w = len(self.adj)
        cand = set(self.adj[v])
        for x in self.adj[v]:
            cand |= self.adj[x]
        cand.discard(v)
        cand = list(cand)
        chosen = list(rng.choice(cand, size=min(2, len(cand)), replace=False)) if cand else []
        self.adj.append(set()); self.d.append(0); self.q.append(0)
        for y in [v] + [int(c) for c in chosen]:
            self.add_link(w, y, rng.uniform(-math.pi, math.pi))

    def grad_term(self, x, y, dd, dq):
        dx = self.d[x] + dd.get(x, 0); dy = self.d[y] + dd.get(y, 0)
        qx = self.q[x] + dq.get(x, 0); qy = self.q[y] + dq.get(y, 0)
        return (dx - dy) ** 2 + 0.1 * (qx - qy) ** 2

    def accept(self, dE):
        return dE <= 0 or self.rng.random() < math.exp(-dE / T)

    def rewire(self):
        rng, adj = self.rng, self.adj
        n = len(adj)
        u = int(rng.integers(n))
        if len(adj[u]) < 2:
            return
        nb = list(adj[u])
        v = nb[int(rng.integers(len(nb)))]
        x = nb[int(rng.integers(len(nb)))]
        xn = list(adj[x])
        w = xn[int(rng.integers(len(xn)))]
        if w == u or w in adj[u] or len(adj[v]) < 2:
            return
        self.tries[0] += 1
        phi = rng.uniform(-math.pi, math.pi)
        old = self.squares(u, v)
        new = [(a, b) for a in adj[u] if a != v for b in adj[a] & adj[w] if b != u]
        dq = {}
        for a, b in old:
            for z in (u, v, a, b):
                dq[z] = dq.get(z, 0) - 1
        for a, b in new:
            for z in (u, w, a, b):
                dq[z] = dq.get(z, 0) + 1
        dd = {v: -1, w: 1}
        dE = 0.0
        if self.use_str:
            dE += W_STR * sum((self.d[z] + c - 6) ** 2 - (self.d[z] - 6) ** 2 for z, c in dd.items())
        if self.use_grad:
            aff = {u, v, w} | set(dq)
            before = {(min(z, y), max(z, y)) for z in aff for y in adj[z]}
            after = (before - {(min(u, v), max(u, v))}) | {(min(u, w), max(u, w))}
            g0 = sum(self.grad_term(a, b, {}, {}) for a, b in before)
            g1 = sum(self.grad_term(a, b, dd, dq) for a, b in after)
            dE += W_GRAD * (g1 - g0)
        if self.coh:
            c_old = sum(self.f(self.ph(u, a) + self.ph(a, b) + self.ph(b, v) + self.ph(v, u)) for a, b in old)
            c_new = sum(self.f(self.ph(u, a) + self.ph(a, b) + self.ph(b, w) - phi) for a, b in new)
            dE -= W_COH * (c_new - c_old)
        if self.accept(dE):
            self.acc[0] += 1
            adj[u].discard(v); adj[v].discard(u)
            del self.phase[(min(u, v), max(u, v))]
            adj[u].add(w); adj[w].add(u)
            self.set_ph(u, w, phi)
            for z, c in dd.items():
                self.d[z] += c
            for z, c in dq.items():
                self.q[z] += c

    def phase_move(self):
        if not self.coh:
            return
        rng, adj = self.rng, self.adj
        u = int(rng.integers(len(adj)))
        if not adj[u]:
            return
        nb = list(adj[u])
        v = nb[int(rng.integers(len(nb)))]
        self.tries[1] += 1
        old = self.ph(u, v)
        new = old + rng.uniform(-math.pi / 2, math.pi / 2)
        dC = 0.0
        for a, b in self.squares(u, v):
            # flux around u->a->b->v->u = ph(u,a) + ph(a,b) + ph(b,v) + ph(v,u), with ph(v,u) = -ph(u,v)
            base = self.ph(u, a) + self.ph(a, b) + self.ph(b, v)
            dC += self.f(base - new) - self.f(base - old)
        if self.accept(-W_COH * dC):
            self.acc[1] += 1
            self.set_ph(u, v, new)

    def run(self):
        snap = None
        while len(self.adj) < N_FINAL:
            self.birth()
            for _ in range(MOVES_PER_BIRTH):
                self.rewire()
                self.phase_move()
            if len(self.adj) == SNAP:
                snap = exact_mean_distance(self.adj)[0]
        links = sum(self.d) // 2
        for _ in range(RELAX_SWEEPS * links):
            self.rewire()
            self.phase_move()
        return snap


def to_csr(adj):
    n = len(adj)
    rows = np.repeat(np.arange(n), [len(s) for s in adj])
    cols = np.fromiter((u for s in adj for u in s), dtype=np.int64, count=len(rows))
    return csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))


def exact_mean_distance(adj):
    A = to_csr(adj)
    ncomp, labels = connected_components(A, directed=False)
    big = np.bincount(labels).argmax()
    keep = np.flatnonzero(labels == big)
    Ak = A[keep][:, keep]
    nk = len(keep)
    if nk < 2:
        return float("nan"), Ak, ncomp, nk
    D = shortest_path(Ak, method="D", unweighted=True)
    return D.sum() / (nk * nk - nk), Ak, ncomp, nk


def lattice(n):
    adj = []
    for x in range(n):
        for y in range(n):
            for z in range(n):
                nb = set()
                for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    nb.add(((x + dx) % n) * n * n + ((y + dy) % n) * n + (z + dz) % n)
                adj.append(nb)
    return adj


def squares_per_locus(adj):
    q = np.zeros(len(adj))
    for u in range(len(adj)):
        Nu = list(adj[u])
        for i in range(len(Nu)):
            for j in range(i + 1, len(Nu)):
                q[u] += len(adj[Nu[i]] & adj[Nu[j]]) - 1
    return q


def measure(adj, rng, snap_dist=None):
    n = len(adj)
    mean_dist, Ak, ncomp, nk = exact_mean_distance(adj)
    d_s = float("nan")
    if nk >= 2:
        S = min(40, nk)
        src = rng.choice(nk, size=S, replace=False)
        deg = np.asarray(Ak.sum(axis=1)).ravel()
        M = (0.5 * (diags(1.0 / deg) @ Ak)).T.tocsr()
        p = np.zeros((nk, S))
        p[src, np.arange(S)] = 1.0
        ret = {}
        for t in range(1, 65):
            p = 0.5 * p + M @ p
            if t in (16, 64):
                ret[t] = p[src, np.arange(S)].mean()
        d_s = -2 * math.log(ret[64] / ret[16]) / math.log(4)
    q = squares_per_locus(adj)
    degs = np.array([len(s) for s in adj])
    tri = np.array([sum(len(adj[a] & adj[u]) for a in adj[u]) // 2 for u in range(n)])
    perfect = float(np.mean((degs == 6) & (q == 12) & (tri == 0)))
    D_g = float("nan")
    if snap_dist and mean_dist == mean_dist and mean_dist > 1.01 * snap_dist:
        D_g = math.log(8) / math.log(mean_dist / snap_dist)
    return {"pieces": ncomp, "largest": nk / n, "distance": mean_dist, "d_s": d_s,
            "squares": q.mean(), "perfect": perfect, "spread": degs.std(), "D_g": D_g}


rng_m = np.random.default_rng(31)
small = exact_mean_distance(lattice(6))[0]
res = {"control": measure(lattice(12), rng_m, small)}
runs = {"FULL": (True, True, "sum"), "NO_COH": (True, True, None), "NO_GRAD": (True, False, "sum"),
        "NO_STR": (False, True, "sum"), "WILSON": (True, True, "wilson")}
acc = {}
for name, (s, g, c) in runs.items():
    world = World(np.random.default_rng(77), s, g, c)
    snap = world.run()
    res[name] = measure(world.adj, rng_m, snap)
    acc[name] = (world.acc[0] / max(1, world.tries[0]), world.acc[1] / max(1, world.tries[1]))

keys = ["pieces", "largest", "distance", "d_s", "squares", "perfect", "spread", "D_g"]
print("%-9s" % "run" + "".join("%11s" % k for k in keys))
for name, m in res.items():
    print("%-9s" % name + "".join("%11.4f" % m[k] for k in keys))
for name, (ar, ap) in acc.items():
    print("acceptance %-8s rewire %.3f  phase %.3f" % (name, ar, ap))

c = res["control"]


def clumps(m):
    return m["largest"] < 0.5 or m["squares"] > 20


def tangle(m):
    return m["squares"] < 3 and m["distance"] < 0.8 * c["distance"]


def three_d(m):
    return (m["largest"] > 0.9 and abs(m["d_s"] - c["d_s"]) < 0.5
            and abs(m["distance"] - c["distance"]) < 0.3 * c["distance"] and abs(m["D_g"] - 3) < 0.7)


checks = [
    ("P0 control perfect, distance 9.00521", c["perfect"] == 1.0 and abs(c["distance"] - 9 * 1728 / 1727) < 1e-9),
    ("P1 FULL clumps", clumps(res["FULL"])),
    ("P2 NO_COH tangle", tangle(res["NO_COH"])),
    ("P3 NO_GRAD clumps", clumps(res["NO_GRAD"])),
    ("P4 NO_STR clumps", clumps(res["NO_STR"])),
    ("P5 WILSON tangle", tangle(res["WILSON"])),
    ("P6 none 3D-like", not any(three_d(res[k]) for k in runs)),
]
print("\nOriginal frozen predictions (first-run verdicts are the record: P1-P5 were WRONG):")
for name, passed in checks:
    print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
for k in runs:
    print("  %-8s 3D-like: %s" % (k, three_d(res[k])))


def near(x, target, rel=1e-3):
    return abs(x - target) <= rel * abs(target)


def rec(m, pieces, dist, d_s, sq, D_g):
    return (m["pieces"] == pieces and near(m["distance"], dist) and near(m["d_s"], d_s)
            and near(m["squares"], sq) and near(m["D_g"], D_g))


recorded = [
    ("Q0 control: distance 9.00521, d_s 3.0333, D_g 3.0177",
     abs(c["distance"] - 9 * 1728 / 1727) < 1e-9 and near(c["d_s"], 3.0333) and near(c["D_g"], 3.0177)),
    ("Q1 FULL: 1 piece, distance 5.3724, d_s 4.0884, squares 4.4838, D_g 5.0128", rec(res["FULL"], 1, 5.3724, 4.0884, 4.4838, 5.0128)),
    ("Q2 NO_COH: 2 pieces, distance 5.3657, d_s 3.6762, squares 4.6968, D_g 4.8058", rec(res["NO_COH"], 2, 5.3657, 3.6762, 4.6968, 4.8058)),
    ("Q3 NO_GRAD: 1 piece, distance 5.8508, d_s 3.6569, squares 9.2546, D_g 4.2447", rec(res["NO_GRAD"], 1, 5.8508, 3.6569, 9.2546, 4.2447)),
    ("Q4 NO_STR: 7 pieces, distance 5.3666, d_s 4.0919, squares 4.8657, D_g 5.1289", rec(res["NO_STR"], 7, 5.3666, 4.0919, 4.8657, 5.1289)),
    ("Q5 WILSON: 1 piece, distance 5.3268, d_s 4.1621, squares 4.2639, D_g 5.0298", rec(res["WILSON"], 1, 5.3268, 4.1621, 4.2639, 5.0298)),
]
ok = True
print("\nRecorded results reproduce:")
for name, passed in recorded:
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
