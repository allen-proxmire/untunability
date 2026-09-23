"""Arithmetic check for road J part 2 (note 3). Not a model of ED: it checks the geometry of counting relations (edges) that cross a
surface in short-range patterns, which note 3's reasoning leans on.

Paper result being checked (note 3, step 1): for a statistically homogeneous, isotropic pattern of straight relations with total length
L_V per unit volume, the expected number crossing a surface is (L_V / 2) x area (the stereological relation P_A = L_V / 2). For a random
pattern with point density rho and links between all pairs closer than r: L_V = rho^2 pi r^4 / 2, so crossings per unit area = rho^2 pi r^4 / 4,
and a sphere of radius R >> r is crossed by about pi^2 rho^2 r^4 R^2 relations.

Settings fixed before the first run (2026-09-15); an earlier draft of this file was revised before it was ever run, to widen sample sizes
(K1, K2) and to set K4 where the ball stays small against the box, after a paper estimate showed the draft K4 range could not be met.

Expected results, written down before the first run (2026-09-15):
  K1 isotropic segments (2,000,000 Poisson centres, uniform random directions, length 1, box side 60) crossing the mid plane:
     count per unit area / (L_V / 2) within 0.97 and 1.03.
  K2 cubic nearest-neighbour lattice (spacing 1): crossings per unit area of a plane with unit normal n, counted over a disc of radius 20
     and averaged over 16 random offsets, equal |n_x| + |n_y| + |n_z|: 1.000 for (0,0,1), 1.414 for (1,1,0)/sqrt2, 1.732 for
     (1,1,1)/sqrt3, each within 3%. The count depends on the surface's direction.
  K3 random short-range pattern (rho = 1, r = 1.5, box side 44): edges crossing a sphere of radius R = 16 / (pi^2 rho^2 r^4 R^2) within
     0.95 and 1.05; fitted exponent of crossings against R over R = 8, 10, 12, 14, 16 within 1.85 and 2.15 (area law).
  K4 the same points with long-range relations only (each linked to one partner chosen uniformly anywhere in the box): fitted exponent
     over R = 4, 5, 6, 7, 8 within 2.8 and 3.1 (grows like volume, not area).
Exit code: 0 if it completes.
"""
import math
import sys

import numpy as np
from scipy.spatial import cKDTree


def k1(rng):
    side, n, ell = 60.0, 2_000_000, 1.0
    centres = rng.uniform(0, side, (n, 3))
    v = rng.standard_normal((n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    az = centres[:, 2] - 0.5 * ell * v[:, 2]
    bz = centres[:, 2] + 0.5 * ell * v[:, 2]
    z0 = side / 2
    cross = np.sum((az - z0) * (bz - z0) < 0)
    LV = n * ell / side ** 3
    return (cross / (side * side)) / (LV / 2)


def plane_disc_count(nvec, rng, L=56, rho0=20.0, trials=16):
    nv = np.array(nvec, float)
    nv /= np.linalg.norm(nv)
    g = np.indices((L, L, L)).reshape(3, -1).T.astype(float)
    counts = []
    for _ in range(trials):
        c = np.full(3, L / 2) + rng.uniform(0, 1, 3)
        sp = (g - c) @ nv
        tot = 0
        for axis in range(3):
            step = np.zeros(3)
            step[axis] = 1.0
            sq = sp + nv[axis]
            crosses = sp * sq < 0
            mid = g + 0.5 * step - c
            inplane = mid - np.outer(mid @ nv, nv)
            inside = np.einsum("ij,ij->i", inplane, inplane) < rho0 ** 2
            tot += np.sum(crosses & inside)
        counts.append(tot)
    return float(np.mean(counts)) / (math.pi * rho0 ** 2)


def sphere_crossings(points, pairs, centre, R):
    inside = np.linalg.norm(points - centre, axis=1) <= R
    return int(np.sum(inside[pairs[:, 0]] != inside[pairs[:, 1]]))


def main():
    rng = np.random.default_rng(20260915)

    r1 = k1(rng)
    print("K1 isotropic segments: crossings per area / (L_V/2) = %.4f" % r1)

    k2v = {name: plane_disc_count(nv, rng) for name, nv in (("(0,0,1)", (0, 0, 1)), ("(1,1,0)", (1, 1, 0)), ("(1,1,1)", (1, 1, 1)))}
    print("K2 cubic lattice crossings per unit area: " + ", ".join("%s %.3f" % (k, v) for k, v in k2v.items()))

    side, rho, r = 44.0, 1.0, 1.5
    n = int(rho * side ** 3)
    pts = rng.uniform(0, side, (n, 3))
    pairs = cKDTree(pts).query_pairs(r, output_type="ndarray")
    centre = np.full(3, side / 2)
    radii = np.array([8.0, 10.0, 12.0, 14.0, 16.0])
    cross = np.array([sphere_crossings(pts, pairs, centre, R) for R in radii], float)
    pred16 = math.pi ** 2 * rho ** 2 * r ** 4 * 16.0 ** 2
    ratio16 = cross[-1] / pred16
    slope = np.polyfit(np.log(radii), np.log(cross), 1)[0]
    print("K3 short-range: crossings %s; at R=16 predicted %.0f, ratio %.4f; exponent %.3f" % (cross.astype(int).tolist(), pred16, ratio16, slope))

    longpairs = np.column_stack([np.arange(n), rng.integers(0, n, n)])
    radii4 = np.array([4.0, 5.0, 6.0, 7.0, 8.0])
    cross_long = np.array([sphere_crossings(pts, longpairs, centre, R) for R in radii4], float)
    slope_long = np.polyfit(np.log(radii4), np.log(cross_long), 1)[0]
    print("K4 long-range only: crossings %s; exponent %.3f" % (cross_long.astype(int).tolist(), slope_long))

    checks = (
        ("K1 isotropic crossings = L_V/2 per area", 0.97 <= r1 <= 1.03),
        ("K2 cubic lattice count depends on direction (1, 1.414, 1.732)",
         abs(k2v["(0,0,1)"] - 1.0) < 0.03 and abs(k2v["(1,1,0)"] / math.sqrt(2) - 1) < 0.03 and abs(k2v["(1,1,1)"] / math.sqrt(3) - 1) < 0.03),
        ("K3 short-range sphere crossings match pi^2 rho^2 r^4 R^2 and scale as area", 0.95 <= ratio16 <= 1.05 and 1.85 <= slope <= 2.15),
        ("K4 long-range relations scale like volume", 2.8 <= slope_long <= 3.1),
    )
    print("\nExpected results:")
    for label, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
