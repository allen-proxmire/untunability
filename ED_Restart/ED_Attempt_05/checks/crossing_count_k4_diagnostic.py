"""Follow-up diagnostic for crossing_count_check.py K4 (run 1: NOT AS EXPECTED, exponent 3.198 against a pre-set range 2.8-3.1).
NOT pre-registered; it does not change K4's recorded outcome. It asks why the fitted exponent came out above 3.

For long-range relations with partners chosen uniformly, a ball holding N_in of the n points is crossed, given N_in, by an expected
2 N_in (n - N_in) / n relations. Run 1 used one ball centre, so N_in itself fluctuates (Poisson), strongly at small R. This diagnostic
(a) regenerates run 1's points and partners with the same seed and draw order, and compares each observed crossing count to
2 N_in (n - N_in) / n using the realised N_in; (b) repeats with 40 random ball centres and fits the exponent of the mean crossings.
"""
import math

import numpy as np
from scipy.spatial import cKDTree


def main():
    rng = np.random.default_rng(20260915)
    # reproduce run 1's draw order: K1 draws, K2 draws, then K3 points and K4 partners
    side1, n1 = 60.0, 2_000_000
    rng.uniform(0, side1, (n1, 3))
    rng.standard_normal((n1, 3))
    for _ in range(3):
        for _ in range(16):
            rng.uniform(0, 1, 3)
    side, rho, r = 44.0, 1.0, 1.5
    n = int(rho * side ** 3)
    pts = rng.uniform(0, side, (n, 3))
    cKDTree(pts).query_pairs(r, output_type="ndarray")
    partners = rng.integers(0, n, n)
    longpairs = np.column_stack([np.arange(n), partners])

    centre = np.full(3, side / 2)
    radii = np.array([4.0, 5.0, 6.0, 7.0, 8.0])
    print("(a) run-1 centre: R, N_in, observed crossings, 2 N_in (n - N_in)/n, ratio")
    for R in radii:
        inside = np.linalg.norm(pts - centre, axis=1) <= R
        nin = int(inside.sum())
        obs = int(np.sum(inside[longpairs[:, 0]] != inside[longpairs[:, 1]]))
        exp = 2 * nin * (n - nin) / n
        print("   %4.1f %6d %6d %9.1f %6.3f" % (R, nin, obs, exp, obs / exp))

    drng = np.random.default_rng(99)
    centres = drng.uniform(10.0, side - 10.0, (40, 3))
    means = []
    for R in radii:
        vals = []
        for c in centres:
            inside = np.linalg.norm(pts - c, axis=1) <= R
            vals.append(np.sum(inside[longpairs[:, 0]] != inside[longpairs[:, 1]]))
        means.append(np.mean(vals))
    means = np.array(means, float)
    slope = np.polyfit(np.log(radii), np.log(means), 1)[0]
    f = (4 / 3) * math.pi * radii ** 3 / side ** 3
    theory = 2 * n * f * (1 - f)
    tslope = np.polyfit(np.log(radii), np.log(theory), 1)[0]
    print("(b) 40 centres: mean crossings %s; exponent %.3f; expectation 2 n f (1 - f) %s, exponent %.3f"
          % (np.round(means).astype(int).tolist(), slope, np.round(theory).astype(int).tolist(), tslope))


if __name__ == "__main__":
    main()
