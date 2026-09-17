"""Allen's corner picture (D17): cones or pyramids in the corner between the x, y, z axes, tips at the origin. Geometry check only.

Round cones: a cone of half-angle a about unit direction u fits inside the corner (x, y, z >= 0) iff every component of u is at least
sin(a) (angular distance to each wall is arcsin(u_i)); two cones do not overlap iff the angle between their centres is at least 2a.
Three equal cones, placed symmetrically: centres (p, q, q), (q, p, q), (q, q, p) with p^2 + 2 q^2 = 1.
Pyramids: region k = the directions whose k-th coordinate is the largest (a square pyramid over one cube face).

Expected results, written down before the first run (2026-09-15):
  O1 three symmetric round cones leaning toward the axes (p > q): largest half-angle 20.94 degrees (to 0.05), full opening 41.9;
     leaning toward the walls' middles (p < q): smaller, about 16.3 degrees (to 0.5).
  O2 a random search over non-symmetric placements of three equal cones finds nothing above 21.0 degrees.
  O3 one round cone on the diagonal fits with half-angle 35.26 degrees (to 0.01).
  O4 the three 20.94-degree cones cover about 79% of the corner's directions (to 1%).
  O5 the three 'largest coordinate' pyramids tile the corner: 1,000,000 random corner directions each fall in exactly one
     (ties have zero measure), and the walls between them are the 45-degree planes x = y, y = z, x = z.
  O6 one double pyramid per axis (regions 'the k-th coordinate is largest in size') covers every direction exactly once in 2, 3 and 4
     dimensions (500,000 random directions each).
Exit code: 0 if it completes.
"""
import math
import sys

import numpy as np


def sym_best(branch):
    best = 0.0
    for q in np.linspace(1e-6, 1 / math.sqrt(2) - 1e-6, 400001):
        p2 = 1 - 2 * q * q
        if p2 <= 0:
            continue
        p = math.sqrt(p2)
        if branch == "axes" and not p > q:
            continue
        if branch == "walls" and not p < q:
            continue
        wall = math.asin(min(p, q))
        cosang = min(1.0, max(-1.0, 2 * p * q + q * q))
        pair = math.acos(cosang) / 2
        best = max(best, min(wall, pair))
    return math.degrees(best)


def score(U):
    wall = np.arcsin(np.clip(U.min(axis=1), -1, 1)).min()
    pairs = []
    for i in range(3):
        for j in range(i + 1, 3):
            pairs.append(math.acos(max(-1.0, min(1.0, float(U[i] @ U[j])))) / 2)
    return min(float(wall), min(pairs))


def main():
    a_axes = sym_best("axes")
    a_walls = sym_best("walls")
    print("O1 symmetric three cones: toward axes %.3f deg (full %.2f); toward wall middles %.3f deg" % (a_axes, 2 * a_axes, a_walls), flush=True)

    rng = np.random.default_rng(1729)
    best = 0.0
    for _ in range(4000):
        U = np.abs(rng.standard_normal((3, 3)))
        U /= np.linalg.norm(U, axis=1, keepdims=True)
        s = score(U)
        step = 0.2
        for _ in range(60):
            V = np.abs(U + step * rng.standard_normal((3, 3)))
            V /= np.linalg.norm(V, axis=1, keepdims=True)
            sv = score(V)
            if sv > s:
                U, s = V, sv
            else:
                step *= 0.93
        best = max(best, s)
    best_deg = math.degrees(best)
    print("O2 random search, best non-symmetric half-angle %.3f deg" % best_deg, flush=True)

    a_diag = math.degrees(math.asin(1 / math.sqrt(3)))
    print("O3 one cone on the diagonal: %.4f deg" % a_diag, flush=True)

    a = math.radians(a_axes)
    q = math.sin(a)
    p = math.sqrt(1 - 2 * q * q)
    C = np.array([[p, q, q], [q, p, q], [q, q, p]])
    D = np.abs(rng.standard_normal((1000000, 3)))
    D /= np.linalg.norm(D, axis=1, keepdims=True)
    covered = ((D @ C.T) >= math.cos(a)).any(axis=1).mean()
    print("O4 corner directions covered by the three cones: %.4f" % covered, flush=True)

    counts = np.stack([(D[:, k] > np.delete(D, k, axis=1).max(axis=1)) for k in range(3)], axis=1).sum(axis=1)
    exactly_one = float((counts == 1).mean())
    boundary_ok = all(abs(math.degrees(math.acos(np.dot(n1, n2) / (np.linalg.norm(n1) * np.linalg.norm(n2)))) - 45.0) < 1e-9
                      for n1, n2 in (((1, 0, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1)), ((1, 0, 0), (1, 0, 1))))
    print("O5 pyramids: share of corner directions in exactly one pyramid %.6f; walls at 45 degrees between neighbouring axes: %s" % (exactly_one, boundary_ok), flush=True)

    o6 = {}
    for d in (2, 3, 4):
        X = rng.standard_normal((500000, d))
        A = np.abs(X)
        m = A.max(axis=1, keepdims=True)
        o6[d] = float(((A == m).sum(axis=1) == 1).mean())
    print("O6 one double pyramid per axis, share of directions in exactly one: 2D %.6f, 3D %.6f, 4D %.6f" % (o6[2], o6[3], o6[4]), flush=True)

    checks = (
        ("O1 symmetric cones 20.94 toward axes, about 16.3 toward walls", abs(a_axes - 20.94) < 0.05 and abs(a_walls - 16.3) < 0.5),
        ("O2 no non-symmetric placement above 21.0", best_deg <= 21.0),
        ("O3 diagonal cone 35.26", abs(a_diag - 35.26) < 0.01),
        ("O4 coverage about 79%", abs(covered - 0.79) < 0.01),
        ("O5 three pyramids tile the corner, 45-degree walls", exactly_one == 1.0 and boundary_ok),
        ("O6 one double pyramid per axis tiles 2D, 3D, 4D", all(v == 1.0 for v in o6.values())),
    )
    print("\nExpected results:")
    for label, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
