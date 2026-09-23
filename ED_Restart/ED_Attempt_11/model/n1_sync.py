"""Road N, step 1: the instrument check (note 10, C19; D12, D13).

Does our test of 'the clocks hold together' reproduce the published behaviour on patterns whose answers are known?

The test, ratio-free (D13: the rate spread is the unit): each event i has a natural rate drawn from a spread of 1 and a
phase; phases follow theta_i' = omega_i + K sum_j sin(theta_j - theta_i) over the relations. After transients, the pattern
HOLDS TOGETHER if every event's long-run rate is the same within tolerance. For each pattern and size we find K_c, the
weakest pull that still holds it, by bisection, and watch K_c against size.

Expected results, written down before this run (N0):
  ring (1D)        K_c rises without limit with N (published: Strogatz-Mirollo 1988, K_c ~ sqrt(N))
  square torus (2D) K_c rises with N (the tie lost by a hair; Hong-Park-Choi 2005)
  cubic torus (3D)  K_c settles as N grows
  random web        K_c settles
Failure: if the 3D grid or the random web do not settle, or the ring does not rise, the test is wrong and nothing later counts.
"""
import json, os, sys, time
import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "n1_runs")
DT, T_TRANS, T_MEAS = 0.05, 200.0, 200.0
TOL = 0.02          # spread of long-run rates counted as "the same", in units of the natural spread


def ring(n, rng):
    i = np.arange(n)
    return sp.csr_matrix((np.ones(2 * n), (np.r_[i, i], np.r_[(i + 1) % n, (i - 1) % n])), shape=(n, n))


def torus2(L, rng):
    n = L * L
    idx = lambda i, j: (i % L) * L + (j % L)
    r, c = [], []
    for i in range(L):
        for j in range(L):
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                r.append(idx(i, j)); c.append(idx(i + di, j + dj))
    return sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(n, n))


def torus3(L, rng):
    n = L ** 3
    idx = lambda i, j, k: ((i % L) * L + (j % L)) * L + (k % L)
    r, c = [], []
    for i in range(L):
        for j in range(L):
            for k in range(L):
                for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    r.append(idx(i, j, k)); c.append(idx(i + d[0], j + d[1], k + d[2]))
    return sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(n, n))


def rand_regular(n, rng, deg=6):
    """A random web in which every event carries the same number of relations (configuration model, simple graph).
    REVISION (recorded, run 1 kept in n1_sync_run1.txt): the Erdos-Renyi web used first has isolated and single-relation
    events, which can never hold with the rest at any pull, so the whole web never locked - a flaw in the test object,
    not in the test. Every event now carries deg relations."""
    stubs = np.repeat(np.arange(n), deg)
    rng.shuffle(stubs)
    a, b = stubs[0::2].copy(), stubs[1::2].copy()
    for _ in range(200):                      # repair self-loops and repeats by swapping ends with random edges
        keys = np.minimum(a, b) * n + np.maximum(a, b)
        bad = np.flatnonzero((a == b) | np.isin(np.arange(len(a)), np.flatnonzero(np.r_[False, keys[1:] == np.sort(keys)[:-1]])) )
        seen = {}
        bad = []
        for i, (x, y) in enumerate(zip(a, b)):
            k = (min(x, y), max(x, y))
            if x == y or k in seen:
                bad.append(i)
            else:
                seen[k] = i
        if not bad:
            break
        for i in bad:
            j = int(rng.integers(len(a)))
            a[i], a[j] = a[j], a[i]
    keep = a != b
    r = np.r_[a[keep], b[keep]]
    c = np.r_[b[keep], a[keep]]
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(n, n))
    A.data[:] = 1.0
    return A


def erdos(n, rng, deg=6):
    m = int(n * deg / 2)
    a = rng.integers(0, n, m); b = rng.integers(0, n, m)
    keep = a != b
    a, b = a[keep], b[keep]
    A = sp.csr_matrix((np.ones(2 * len(a)), (np.r_[a, b], np.r_[b, a])), shape=(n, n))
    A.data[:] = 1.0
    return A


def holds(A, omega, K, seed=0):
    """Integrate the phase dynamics; True if all long-run rates agree within TOL.
    FIX (first run: the 3D grid would not lock even at maximum pull): the step must shrink as the pull grows, or the
    integration blows up. dt = min(DT, 0.2 / (K * max degree))."""
    n = A.shape[0]
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, n)
    dmax = float(np.asarray(A.sum(axis=1)).max())
    DTk = min(DT, 0.2 / max(K * dmax, 1e-9))
    nt, nm = int(T_TRANS / DTk), int(T_MEAS / DTk)

    def dth(t):
        s, c = np.sin(t), np.cos(t)
        return omega + K * (c * (A @ s) - s * (A @ c))
    for _ in range(nt):
        th = th + DTk * dth(th)
    th0 = th.copy()
    for _ in range(nm):
        th = th + DTk * dth(th)
    Om = (th - th0) / T_MEAS
    return bool(Om.max() - Om.min() < TOL), float(Om.max() - Om.min())


def k_c(A, omega, lo=0.0, hi=64.0, steps=9, seed=0):
    ok, _ = holds(A, omega, hi, seed)
    if not ok:
        return None
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if holds(A, omega, mid, seed)[0]:
            hi = mid
        else:
            lo = mid
    return hi


FAMILIES = {"ring": (ring, [2000, 4000, 8000, 16000]),
            "torus2": (torus2, [45, 63, 89, 126]),
            "torus3": (torus3, [13, 16, 20, 25]),
            "web": (rand_regular, [2000, 4000, 8000, 16000])}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    prev = {}
    pj = os.path.join(OUT, "step1.json")
    if os.path.exists(pj):
        prev = json.load(open(pj))
    res = dict(prev)
    for name, (fn, sizes) in FAMILIES.items():
        if only and name not in only:
            continue
        res[name] = []
        for s in sizes:
            rng = np.random.default_rng(1)
            A = fn(s, rng)
            n = A.shape[0]
            omega = rng.normal(0, 1, n)
            omega -= omega.mean()
            t0 = time.time()
            kc = k_c(A, omega)
            res[name].append(dict(size=n, K_c=kc, secs=round(time.time() - t0, 1)))
            print(name, n, "K_c", kc, "%.0fs" % (time.time() - t0), flush=True)
            json.dump(res, open(os.path.join(OUT, "step1.json"), "w"), indent=1)
    lines = []
    for name in FAMILIES:
        ks = [r["K_c"] for r in res[name]]
        ns = [r["size"] for r in res[name]]
        rise = None
        if all(k is not None for k in ks):
            rise = float(np.polyfit(np.log(ns), np.log(ks), 1)[0])
        lines.append("%-7s sizes %s | K_c %s | growth exponent %s"
                     % (name, ns, [None if k is None else round(k, 3) for k in ks],
                        None if rise is None else round(rise, 3)))
    ok = True
    for name, expect_rise in (("ring", True), ("torus2", True), ("torus3", False), ("web", False)):
        ks = [r["K_c"] for r in res[name]]
        if any(k is None for k in ks):
            rose = True
        else:
            rose = ks[-1] > 1.3 * ks[0]
        ok &= (rose == expect_rise)
        lines.append("%-7s rises: %s (expected %s)" % (name, rose, expect_rise))
    lines.append("N0 %s" % ok)
    text = "\n".join(lines)
    open(os.path.join(HERE, "n1_sync.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
