"""Check C147: does random local splitting keep a 3D space 3D? (G30)

Start: a 3D periodic cubic lattice of side 16 (4,096 loci, each with 6 neighbours).
Grow by 28,672 births to 32,768 loci. Each birth picks an existing locus v uniformly at random
and splits it into v and a new locus w. Three readings of "the pair shares its old connections":

  S1 share:            w takes a random half of v's neighbours (moved from v); v and w are linked.
  S2 share + triangle: as S1, then w also links to 2 random neighbours that stayed with v.
                       (The "2" keeps the average number of neighbours at 6. It is a tuned choice.)
  S3 copy:             w links to all of v's neighbours (v keeps them too); v and w are linked.

Control: a plain 3D periodic lattice of side 32 (also 32,768 loci).

Measured on each graph:
  mean degree         average number of neighbours
  mean distance       average graph distance from 40 random loci to every locus
  spectral dimension  d_s = -2 dlog P(t) / dlog t, P = return probability of a lazy random walk
                      (stay with probability 1/2), from t = 16 to t = 64, averaged over 40 starts
  hub ratio           largest degree / median degree

Predictions frozen before the first run (2026-09-13):
  P0  Control: mean degree 6; mean distance 24 (exact for this lattice) to 1e-9;
      d_s within 0.5 of 3.
  P1  S1: mean degree exactly 2.5 (every birth adds one link); d_s below control - 0.5;
      mean distance above 1.3 x control. (Space turns into chains.)
  P2  S2: mean degree within 0.1 of 6; d_s within 0.5 of control; mean distance within
      30% of control. (Low confidence.)
  P3  S3: mean degree above 20; mean distance below 0.5 x control; hub ratio above 10.
      (Space becomes a small world with hubs.)

Changes after freezing (2026-09-13, after the first run):
  First run: P1 S1 distance, P2 S2 distance, P3 S3 hub ratio were WRONG predictions, and P0 failed
  on Claude's arithmetic: the mean distance excludes each source's zero distance to itself, so the
  exact control value is 24 x 32768 / 32767 = 24.00073, not 24. The wrong predictions stand as
  findings (ledger C147-C149) and are still printed below with their original verdicts.
  Added: the starting lattice (side 16) is measured too, and a growth dimension
  D_g = ln(N / N0) / ln(mean distance / starting mean distance) says how loci count grows with
  extent (a 3D space doubling in size has D_g = 3).
  The script's exit code now checks that the recorded first-run results reproduce (R0-R4), not
  whether the original predictions were right.
"""
import sys

import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import shortest_path

N0_SIDE, SIDE = 16, 32
N_FINAL = SIDE ** 3
SOURCES = 40


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


def grow(adj, rule, rng):
    while len(adj) < N_FINAL:
        v = int(rng.integers(len(adj)))
        w = len(adj)
        nb = list(adj[v])
        if rule == "copy":
            adj.append(set(nb) | {v})
            for u in nb:
                adj[u].add(w)
            adj[v].add(w)
            continue
        rng.shuffle(nb)
        moved = nb[: len(nb) // 2]
        for u in moved:
            adj[u].discard(v)
            adj[u].add(w)
            adj[v].discard(u)
        adj.append(set(moved) | {v})
        adj[v].add(w)
        if rule == "triangle":
            stayers = [u for u in adj[v] if u != w]
            for u in rng.choice(stayers, size=min(2, len(stayers)), replace=False):
                adj[w].add(int(u))
                adj[int(u)].add(w)
    return adj


def measure(adj, rng):
    n = len(adj)
    rows = np.repeat(np.arange(n), [len(s) for s in adj])
    cols = np.fromiter((u for s in adj for u in s), dtype=np.int64, count=len(rows))
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    deg = np.asarray(A.sum(axis=1)).ravel()
    src = rng.choice(n, size=SOURCES, replace=False)
    dist = shortest_path(A, method="D", unweighted=True, indices=src)
    mean_dist = dist[np.isfinite(dist)].sum() / (np.isfinite(dist).sum() - SOURCES)
    # lazy walk, row vectors: p <- 0.5 p + 0.5 (p / deg) A
    Dinv = diags(1.0 / deg)
    M = (0.5 * (Dinv @ A)).T.tocsr()
    p = np.zeros((n, SOURCES))
    p[src, np.arange(SOURCES)] = 1.0
    ret = {}
    for t in range(1, 65):
        p = 0.5 * p + M @ p
        if t in (16, 64):
            ret[t] = p[src, np.arange(SOURCES)].mean()
    d_s = -2 * np.log(ret[64] / ret[16]) / np.log(4)
    return {"mean degree": deg.mean(), "mean distance": mean_dist, "d_s": d_s,
            "hub ratio": deg.max() / np.median(deg)}


rng = np.random.default_rng(2026)
res = {"control": measure(lattice(SIDE), rng)}
for name, rule in (("S1 share", "share"), ("S2 share + triangle", "triangle"), ("S3 copy", "copy")):
    res[name] = measure(grow(lattice(N0_SIDE), rule, rng), rng)

print("%-22s %12s %14s %8s %10s" % ("graph", "mean degree", "mean distance", "d_s", "hub ratio"))
for name, m in res.items():
    print("%-22s %12.4f %14.4f %8.3f %10.2f" % (name, m["mean degree"], m["mean distance"], m["d_s"], m["hub ratio"]))

c, s1, s2, s3 = res["control"], res["S1 share"], res["S2 share + triangle"], res["S3 copy"]
checks = [
    ("P0 control degree 6, distance 24, d_s near 3",
     abs(c["mean degree"] - 6) < 1e-12 and abs(c["mean distance"] - 24) < 1e-9 and abs(c["d_s"] - 3) < 0.5),
    ("P1 S1 degree 2.5", abs(s1["mean degree"] - 2.5) < 1e-12),
    ("P1 S1 d_s below control - 0.5", s1["d_s"] < c["d_s"] - 0.5),
    ("P1 S1 distance above 1.3 x control", s1["mean distance"] > 1.3 * c["mean distance"]),
    ("P2 S2 degree within 0.1 of 6", abs(s2["mean degree"] - 6) < 0.1),
    ("P2 S2 d_s within 0.5 of control", abs(s2["d_s"] - c["d_s"]) < 0.5),
    ("P2 S2 distance within 30% of control", abs(s2["mean distance"] - c["mean distance"]) < 0.3 * c["mean distance"]),
    ("P3 S3 degree above 20", s3["mean degree"] > 20),
    ("P3 S3 distance below 0.5 x control", s3["mean distance"] < 0.5 * c["mean distance"]),
    ("P3 S3 hub ratio above 10", s3["hub ratio"] > 10),
]
print("\nOriginal frozen predictions (first-run verdicts are the record):")
for name, passed in checks:
    print("  %-5s %s" % ("RIGHT" if passed else "WRONG", name))

start = measure(lattice(N0_SIDE), np.random.default_rng(1))
print("\nstarting lattice (side 16): mean distance %.5f" % start["mean distance"])
for name in ("control", "S1 share", "S2 share + triangle", "S3 copy"):
    ratio = res[name]["mean distance"] / start["mean distance"]
    if ratio > 1.01:
        print("  %-22s growth dimension D_g = %.2f" % (name, np.log(8) / np.log(ratio)))
    else:
        print("  %-22s no growth in extent (distance ratio %.4f)" % (name, ratio))


def near(x, target, rel=1e-3):
    return abs(x - target) <= rel * abs(target)


dg = lambda name: np.log(8) / np.log(res[name]["mean distance"] / start["mean distance"])
recorded = [
    ("R0 control: degree 6, distance 24.00073, d_s 3.046",
     abs(c["mean degree"] - 6) < 1e-12 and abs(c["mean distance"] - 24 * 32768 / 32767) < 1e-9 and near(c["d_s"], 3.046)),
    ("R1 S1: degree 2.5, distance 22.9575, d_s 1.982, D_g about 3.2",
     abs(s1["mean degree"] - 2.5) < 1e-12 and near(s1["mean distance"], 22.9575) and near(s1["d_s"], 1.982) and 3.0 < dg("S1 share") < 3.4),
    ("R2 S2: degree 6.0, distance 13.6084, d_s 2.877, D_g above 10",
     near(s2["mean degree"], 6.0) and near(s2["mean distance"], 13.6084) and near(s2["d_s"], 2.877) and dg("S2 share + triangle") > 10),
    ("R3 S3: degree 61.648, distance 11.9976 (no growth in extent), hub ratio 2.76",
     near(s3["mean degree"], 61.6479) and near(s3["mean distance"], 11.9976) and near(s3["hub ratio"], 2.76, 1e-2)
     and s3["mean distance"] < 1.01 * start["mean distance"]),
    ("R4 starting lattice distance 12.00293", abs(start["mean distance"] - 12 * 4096 / 4095) < 1e-9),
]
ok = True
print("\nRecorded results reproduce:")
for name, passed in recorded:
    ok &= passed
    print("%-4s %s" % ("PASS" if passed else "FAIL", name))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
