"""Check C176: can local rewiring settle random links into 3D space? (G30 option C, RD32)

Loci: N = 3,375 (the count of a 15^3 lattice), with 3N links placed at random, so the average is
6 links per locus. The start is a random graph: a "small world" with no geometry.

Rewiring (option C): each move picks a random locus u, one of its links u-v, and a locus w two
steps away (a neighbour of one of u's neighbours, not already linked to u). The link u-v is
dropped and u-w is formed if the local preference improves, or with chance exp(-change / T)
otherwise. The temperature-like setting T falls from 3 to 0.02 over 60 sweeps (60 x 3N moves).
Total links never change. These settings are test choices, not ED rules.

Two local preferences (energy, lower is preferred; q(x) = number of square loops through locus x):
  R1 "favour squares":        sum over loci of (links - 6)^2  -  (number of squares)
  R2 "squares like a lattice": sum over loci of (links - 6)^2  +  0.1 x sum over loci of (q - 12)^2
     (a cubic lattice locus has 6 links and 12 squares through it)

Control: the 15^3 periodic cubic lattice.

Measured: mean distance within the largest connected piece; share of loci in that piece;
spectral dimension d_s (lazy walk, t = 16 to 64, 40 starts, as in split_dimension.py);
mean squares per locus; share of "perfect lattice" loci (6 links, 12 squares, no triangles).

Predictions frozen before the first run (2026-09-13):
  P0  Control: 6 links, 12 squares and perfect at every locus; mean distance 11.2 x 3375/3374
      = 11.20332 to 1e-9.
  P1  R1 clumps: squares per locus rise above 5 x the start, but space does not become 3D:
      mean distance below 0.6 x control, or largest piece below 90% of loci.
      (Expected: dense bipartite pockets that are full of squares.) Medium confidence.
  P2  R2:
      a. mean squares per locus within 3 of 12 (medium);
      b. mean distance above 1.5 x the random start (less of a small world) (medium);
      c. 3D-like: d_s within 0.5 of control AND mean distance within 30% of control (LOW);
      d. not a perfect crystal: perfect-lattice share below 0.9 (medium).

Changes after freezing (2026-09-13):
  1. The first attempt crashed inside measure() before printing any result: R1's largest piece had
     fewer than 40 loci. Fixed to use up to 40 starts, and a piece count was added. Predictions unchanged.
  2. First complete run (rewire_dimension_run1.txt): P0, P1, P2a, P2b, P2d RIGHT; P2c WRONG
     (R2's d_s was within 0.5 of control, but its mean distance was 35% below control).
     The original verdicts are still printed below. The exit code now checks that the recorded
     first-run results reproduce (Q0-Q2), not whether the predictions were right.
"""
import math
import sys

import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components, shortest_path

SIDE = 15
N = SIDE ** 3
SWEEPS = 60
T_START, T_END = 3.0, 0.02


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


def random_graph(rng):
    adj = [set() for _ in range(N)]
    count = 0
    while count < 3 * N:
        a, b = int(rng.integers(N)), int(rng.integers(N))
        if a != b and b not in adj[a]:
            adj[a].add(b)
            adj[b].add(a)
            count += 1
    return adj


def squares_through(adj, u, v):
    """Square loops u-a-b-v(-u) through the pair u, v (whether or not u-v is a link now)."""
    out = []
    Nv = adj[v]
    for a in adj[u]:
        if a == v:
            continue
        for b in adj[a] & Nv:
            if b != u:
                out.append((a, b))
    return out


def square_counts_exact(adj):
    """Squares through each locus, counting each square once per locus."""
    q = np.zeros(len(adj))
    for u in range(len(adj)):
        Nu = list(adj[u])
        # squares through u: pairs of neighbours a, c with a common neighbour b != u
        for i in range(len(Nu)):
            for j in range(i + 1, len(Nu)):
                common = adj[Nu[i]] & adj[Nu[j]]
                q[u] += len(common) - 1  # minus u itself
    return q


def triangles_through(adj, u):
    Nu = list(adj[u])
    return sum(len(adj[Nu[i]] & adj[u]) for i in range(len(Nu))) // 2


def settle(adj, rule, rng):
    deg = np.array([len(s) for s in adj], dtype=float)
    q = square_counts_exact(adj)
    E_links = 3 * N
    n_moves = SWEEPS * E_links
    accepted = 0
    for m in range(n_moves):
        T = T_START * (T_END / T_START) ** (m / n_moves)
        u = int(rng.integers(N))
        if len(adj[u]) < 2:
            continue
        nbrs = list(adj[u])
        v = nbrs[int(rng.integers(len(nbrs)))]
        x = nbrs[int(rng.integers(len(nbrs)))]
        xn = list(adj[x])
        w = xn[int(rng.integers(len(xn)))]
        if w == u or w in adj[u] or len(adj[v]) < 2:
            continue
        old = squares_through(adj, u, v)
        adj[u].discard(v)
        adj[v].discard(u)
        new = squares_through(adj, u, w)
        dq = {}
        for a, b in old:
            for y in (u, v, a, b):
                dq[y] = dq.get(y, 0) - 1
        for a, b in new:
            for y in (u, w, a, b):
                dq[y] = dq.get(y, 0) + 1
        dE = ((deg[v] - 1 - 6) ** 2 - (deg[v] - 6) ** 2) + ((deg[w] + 1 - 6) ** 2 - (deg[w] - 6) ** 2)
        if rule == "R1":
            dE += -(len(new) - len(old))
        else:
            dE += 0.1 * sum((q[y] + d - 12) ** 2 - (q[y] - 12) ** 2 for y, d in dq.items())
        if dE <= 0 or rng.random() < math.exp(-dE / T):
            adj[u].add(w)
            adj[w].add(u)
            deg[v] -= 1
            deg[w] += 1
            for y, d in dq.items():
                q[y] += d
            accepted += 1
        else:
            adj[u].add(v)
            adj[v].add(u)
    return adj, accepted / n_moves


def measure(adj, rng):
    n = len(adj)
    rows = np.repeat(np.arange(n), [len(s) for s in adj])
    cols = np.fromiter((u for s in adj for u in s), dtype=np.int64, count=len(rows))
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    ncomp, labels = connected_components(A, directed=False)
    big = np.bincount(labels).argmax()
    keep = np.flatnonzero(labels == big)
    Ak = A[keep][:, keep]
    nk = len(keep)
    # (fix after a crash on the first attempt, before any result was printed: the largest piece can
    #  have fewer than 40 loci, so use up to 40 starts; predictions unchanged)
    S = min(40, nk)
    if nk < 2:
        mean_dist, d_s = float("nan"), float("nan")
    else:
        src = rng.choice(nk, size=S, replace=False)
        dist = shortest_path(Ak, method="D", unweighted=True, indices=src)
        mean_dist = dist.sum() / (dist.size - S)
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
    q = square_counts_exact(adj)
    degs = np.array([len(s) for s in adj])
    perfect = np.mean([(degs[u] == 6 and q[u] == 12 and triangles_through(adj, u) == 0) for u in range(n)])
    return {"pieces": ncomp, "largest piece": nk / n, "mean distance": mean_dist, "d_s": d_s,
            "squares per locus": q.mean(), "perfect share": perfect, "links spread": degs.std()}


rng = np.random.default_rng(2027)
res = {"control": measure(lattice(SIDE), rng)}
start = random_graph(np.random.default_rng(5))
res["random start"] = measure([set(s) for s in start], rng)
acc = {}
for rule in ("R1", "R2"):
    g, acc[rule] = settle([set(s) for s in start], rule, np.random.default_rng(9))
    res[rule] = measure(g, rng)

keys = ["pieces", "largest piece", "mean distance", "d_s", "squares per locus", "perfect share", "links spread"]
print("%-14s" % "graph" + "".join("%18s" % k for k in keys))
for name, m in res.items():
    print("%-14s" % name + "".join("%18.4f" % m[k] for k in keys))
print("acceptance: R1 %.3f, R2 %.3f" % (acc["R1"], acc["R2"]))

c, s0, r1, r2 = res["control"], res["random start"], res["R1"], res["R2"]
checks = [
    ("P0 control perfect lattice, distance 11.20332",
     c["perfect share"] == 1.0 and abs(c["squares per locus"] - 12) < 1e-12 and abs(c["mean distance"] - 11.2 * 3375 / 3374) < 1e-9),
    ("P1 R1 squares above 5 x start", r1["squares per locus"] > 5 * max(s0["squares per locus"], 1e-9)),
    ("P1 R1 not 3D (distance < 0.6 x control or largest piece < 0.9)",
     r1["mean distance"] < 0.6 * c["mean distance"] or r1["largest piece"] < 0.9),
    ("P2a R2 squares per locus within 3 of 12", abs(r2["squares per locus"] - 12) < 3),
    ("P2b R2 distance above 1.5 x random start", r2["mean distance"] > 1.5 * s0["mean distance"]),
    ("P2c R2 3D-like (d_s within 0.5, distance within 30% of control)",
     abs(r2["d_s"] - c["d_s"]) < 0.5 and abs(r2["mean distance"] - c["mean distance"]) < 0.3 * c["mean distance"]),
    ("P2d R2 not a perfect crystal (perfect share below 0.9)", r2["perfect share"] < 0.9),
]
print("\nOriginal frozen predictions (first-run verdicts are the record: P2c was WRONG):")
for name, passed in checks:
    print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))


def near(x, target, rel=1e-3):
    return abs(x - target) <= rel * abs(target)


recorded = [
    ("Q0 control: perfect lattice, distance 11.20332, d_s 3.0461",
     c["perfect share"] == 1.0 and abs(c["mean distance"] - 11.2 * 3375 / 3374) < 1e-9 and near(c["d_s"], 3.0461)),
    ("Q1 R1 shatters: 417 pieces, largest 0.0056, 77.7588 squares per locus",
     r1["pieces"] == 417 and near(r1["largest piece"], 0.0056, 1e-2) and near(r1["squares per locus"], 77.7588)),
    ("Q2 R2: 7 pieces, largest 0.9982, distance 7.3052, d_s 3.3745, squares 11.8459, perfect 0.0033",
     r2["pieces"] == 7 and near(r2["largest piece"], 0.9982) and near(r2["mean distance"], 7.3052)
     and near(r2["d_s"], 3.3745) and near(r2["squares per locus"], 11.8459) and near(r2["perfect share"], 0.0033, 2e-2)),
]
ok = True
print("\nRecorded results reproduce:")
for name, passed in recorded:
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
