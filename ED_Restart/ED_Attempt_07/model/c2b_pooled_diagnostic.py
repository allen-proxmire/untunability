"""Follow-up diagnostic for C2b run 2 (NOT pre-registered).

Run 2's exponent beta was the median over seeds of per-seed slopes of ln W
against ln n, one realisation per size. In 1D a few longest waves set W, so
per-seed slopes scatter widely. Here: (i) the exact linear-regime expectation
<W^2> on the grids from the discrete Laplacian's eigenvalues (no simulation),
and its slope over the four sizes; (ii) the pooled estimator: slope of
ln sqrt(mean over seeds of W^2) against ln n, and pooled tilt ratios; (iii) the
per-seed scatter. Run 2's verdict stands.
"""
import json, glob, math
import numpy as np
from c2b import SIZES, K

def exact_grid_W2(d, n, sigma):
    # linear steady state: psi_k = omega_k / (K * lambda_k), lambda_k = (1/d) sum_i (1 - cos k_i)
    ks = 2 * np.pi * np.arange(n) / n
    grids = np.meshgrid(*([ks] * d), indexing="ij")
    lam = sum(1 - np.cos(g) for g in grids) / d
    lam = lam.ravel()[1:]
    return float(np.sum(sigma ** 2 / (K * lam) ** 2) / n ** d)

runs = {}
for f in glob.glob("c2b_runs2/*.json"):
    r = json.load(open(f))
    runs[(r["d"], r["n"], r["kind"], r["fresh"], r["seed"])] = r
seeds = list(range(3, 13))
slope = lambda x, y: float(np.polyfit(np.log(x), np.log(y), 1)[0])
print("exact grid expectation (persistent, sigma 0.0005):")
for d in (1, 2, 3):
    ns = SIZES[d]
    W = [math.sqrt(exact_grid_W2(d, n, 0.0005)) for n in ns]
    print(f"  d={d}: sqrt<W^2> {', '.join(f'{w:.4g}' for w in W)}; slope {slope(ns, W):.3f}; tilt ratio {(W[-1]/ns[-1])/(W[0]/ns[0]):.3f}")
for fresh in (False, True):
    for kind in ("G", "R"):
        out = []
        for d in (1, 2, 3):
            ns = SIZES[d]
            Wp = [math.sqrt(np.mean([runs[(d, n, kind, fresh, s)]["W"] ** 2 for s in seeds])) for n in ns]
            b = [slope(ns, [runs[(d, n, kind, fresh, s)]["W"] for n in ns]) for s in seeds]
            out.append(f"d={d} pooled beta {slope(ns, Wp):.3f}, pooled tilt ratio {(Wp[-1]/ns[-1])/(Wp[0]/ns[0]):.3f}, per-seed beta median {np.median(b):.3f} sd {np.std(b, ddof=1):.3f}")
        print(f"{'fresh' if fresh else 'persistent'} {kind}: " + " | ".join(out))
