"""Fast against slow (D8): the compiled sampler must reproduce the reference sampler's statistics.

Same system (L = 8, T = 6, ED mode), different random streams. Compared: the time-averaged event and (2,2) counts and the
slice mean distance, each with an error bar. Pass (written before running): the three means agree within 3 standard errors
of their difference, and both structure checks are clean.
ACCEPTANCE IS NOT COMPARED (revision, recorded): the compiled version proposes an event by slot and rejects empty slots,
so its denominator counts those; the reference version picks among live events. Both are valid proposals - the compiled
one uses VTOP in its Hastings factors - but their acceptance rates are not the same quantity.
"""
import math
import sys, time
import numpy as np
sys.path.insert(0, ".")
from st3 import Spacetime                      # noqa: E402
from st3f_run import Fast                      # noqa: E402
import st3_run as R                            # noqa: E402


def sem(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))

SW_SLOW, SW_FAST = 600, 6000


def slow(L=8, T=6, seed=3, SW=None):
    SW = SW or SW_SLOW
    X = Spacetime(L, T, eps=0.1, seed=seed)
    n0, n22, md = [], [], []
    t0 = time.time()
    for sw in range(SW):
        for _ in range(X.N3()):
            X.step()
        if sw % 20 == 19:
            n0.append(X.N0()); n22.append(X.N22_cur)
            md.append(np.mean([m for _, _, m in R.slice_readings(X, sw) if m]))
    return dict(acc=X.acc / X.tried, N0=float(np.mean(n0)), N22=float(np.mean(n22)), md=float(np.mean(md)),
                sem=(sem(n0), sem(n22), sem(md)), check=X.check(), secs=time.time() - t0, sweeps=SW)


def fast(L=8, T=6, seed=4, SW=None):
    SW = SW or SW_FAST
    F = Fast(L, T, mode="ed", eps=0.1, seed=seed)
    n0, n22, md = [], [], []
    t0 = time.time()
    for sw in range(SW):
        F.sweeps(1)
        if sw % 20 == 19:
            n0.append(F.X.N0()); n22.append(int(F.cnt[2]))
            md.append(np.mean([m for _, _, m in R.slice_readings(F.X, sw) if m]))
    return dict(acc=F.cnt[1] / F.cnt[0], N0=float(np.mean(n0)), N22=float(np.mean(n22)), md=float(np.mean(md)),
                sem=(sem(n0), sem(n22), sem(md)), check=F.check(), secs=time.time() - t0, sweeps=SW)


if __name__ == "__main__":
    a, b = slow(), fast()
    zs = []
    for i, k in enumerate(("N0", "N22", "md")):
        se = math.sqrt(a["sem"][i] ** 2 + b["sem"][i] ** 2)
        zs.append((k, (a[k] - b[k]) / se if se > 0 else 0.0))
    ok = all(abs(z) <= 3 for _, z in zs) and not a["check"] and not b["check"]
    print("z:", [(k, round(z, 2)) for k, z in zs])
    print("slow", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in a.items()})
    print("fast", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in b.items()})
    print("speedup %.0fx | PASS %s" % (a["secs"] / b["secs"], ok))
