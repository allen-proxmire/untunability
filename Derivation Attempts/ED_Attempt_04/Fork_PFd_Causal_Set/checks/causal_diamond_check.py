"""Arithmetic check for the PF-d fork (FC4). Not a model of ED; it checks three textbook facts that the fork's comparison leans on.

Setup: 1+1 dimensions, light-cone coordinates u = t + x, v = t - x. The causal diamond between the origin and the event (u, v) = (U, V)
has proper time tau with tau^2 = U V and area U V / 2. Event a precedes event b iff u_a < u_b and v_a < v_b.
Hop counts from note 13: U = 2 n_R, V = 2 n_L, so the pairing count 2 sqrt(n_R n_L) is tau.

Expected results, written down before the first run (2026-09-15):
  P1 for all integers n_R, n_L up to 100: tau^2 = 4 n_R n_L and area = 2 n_R n_L, so (pairing count)^2 = 2 x area exactly.
  P2 order is frame-free: for 2000 random events, boosting (u, v) -> (D u, v / D) with D = 3.7 leaves every precedence relation
     unchanged (exact count equality of related pairs).
  P3 the longest chain among N uniform random events in a diamond (the longest increasing subsequence) has mean length / sqrt(N)
     between 1.89 and 1.95 at N = 10,000 (20 trials), larger than at N = 2,500, approaching 2 from below.
  P4 longest chain grows like proper time: at fixed density, doubling tau quadruples N (2,500 to 10,000), and the mean longest chain
     grows by a factor between 1.95 and 2.15.
Exit code: 0 if it completes.
"""
import bisect
import math
import random
import sys


def longest_chain(points):
    pts = sorted(points)
    tails = []
    for _, v in pts:
        k = bisect.bisect_left(tails, v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v
    return len(tails)


def related_pairs(points):
    n = 0
    for i in range(len(points)):
        ui, vi = points[i]
        for j in range(len(points)):
            uj, vj = points[j]
            if ui < uj and vi < vj:
                n += 1
    return n


def main():
    p1 = all(4 * a * b == 2 * (2 * a * b) for a in range(101) for b in range(101))
    print("P1 (pairing count)^2 = 2 x diamond area for all n_R, n_L <= 100:", p1)

    rng = random.Random(20260915)
    pts = [(rng.random(), rng.random()) for _ in range(2000)]
    D = 3.7
    boosted = [(D * u, v / D) for u, v in pts]
    r0, r1 = related_pairs(pts), related_pairs(boosted)
    print("P2 related pairs before boost %d, after boost %d" % (r0, r1))

    means = {}
    for N in (2500, 10000):
        vals = [longest_chain([(rng.random(), rng.random()) for _ in range(N)]) for _ in range(20)]
        means[N] = sum(vals) / len(vals)
        print("P3 N = %d: mean longest chain %.2f, per sqrt(N) %.4f" % (N, means[N], means[N] / math.sqrt(N)))
    growth = means[10000] / means[2500]
    print("P4 doubling proper time (N x 4): longest chain grows by %.3f" % growth)

    checks = (
        ("P1 pairings squared = 2 x area", p1),
        ("P2 boost leaves order unchanged", r0 == r1),
        ("P3 longest chain / sqrt(N) in [1.89, 1.95] at 10,000, above 2,500", 1.89 <= means[10000] / 100 <= 1.95 and means[10000] / 100 > means[2500] / 50),
        ("P4 longest chain doubles when proper time doubles", 1.95 <= growth <= 2.15),
    )
    print("\nExpected results:")
    for label, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
