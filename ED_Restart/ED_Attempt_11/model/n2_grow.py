"""Road N, step 2: ED's own patterns (note 10, C19; D12, D13).

Grow a pattern of events carrying natural rates, with no space anywhere in the rules:
  - events are added one batch at a time, each arriving with a single relation to a random existing event;
  - after each batch, relations are added ONLY while the pattern cannot hold its clocks together at a fixed pull,
    and stopped as soon as it can (D13: fewest relations that still hold);
  - relations stick once made (D12); the ceiling caps how many an event may carry;
  - the pull is measured in units of the rate spread (D13), and is held at K0 = 1 while the pattern grows, so the
    question "can this pattern hold at a fixed pull as it grows?" is exactly attempt 6's floor.

REVISIONS after the first smoke test (recorded before the real run, RD16):
  R1  Relations are added WHERE THE STRAIN IS, not between random pairs. Adding at random is not "the fewest
      relations" at all: the first version saturated at 30.8 relations per event and still did not hold.
      Strain = the linear solve x (how much each relation is asked to carry); the most strained events get the
      new relations, and the partner is drawn from events strained the other way, which is what relieves them.
  R2  The linear test is a proxy only. At the first smoke test it said "feasible" while the full phase dynamics
      said the clocks did not lock. So: the proxy is tightened to THRESH = 1.2 during growth, and the FULL
      dynamics is the arbiter at the end - relations keep being added until the clocks really hold.
  R3  Two readings of "fewest directions" (D13 / N-Q7 left the partner unspecified), both run and both reported:
        far   a strained event may reach ANY event in the pattern. Least structure; nothing in ED's rules
              prefers a near partner.
        near  a strained event may only reach events already within NEAR hops of it. Also least structure in a
              different sense: joining something already nearby opens no new direction.
      Nothing else differs between the two.

Expected results, fixed in note 10 before any code:
  N1  ED's grown patterns hold together at all (moderate confidence)
  N2  MAIN CLAIM: a pattern carrying as few relations as it can, while holding together, reads between 2.5 and 3.5
      on the ball-growth dimension and the patch-edge exponent, at two sizes (about 40 per cent)
  N3  reported, no expectation: relations per event, against ED's link budget of 6.7
Controls: the same readings on step 1's known patterns at the same sizes (ring, square grid, cubic grid, regular web).
"""
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import cg
from scipy.sparse.csgraph import breadth_first_order

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
OUT = os.path.join(HERE, "n2_runs")
CEIL = 60
K0 = 1.0
SIZES = (2000, 4000, 8000)
BATCH = 0.02          # events added per batch, as a share of the target
CHUNK = 8             # relations added between strain solves
THRESH = 1.2          # tightened proxy during growth (R2); the full dynamics is the arbiter at the end
NEAR = 3              # "near" variant: a strained event may only reach events within this many hops


def laplacian(A):
    d = np.asarray(A.sum(axis=1)).ravel()
    return sp.diags(d) - A


def strain(A, omega, K=K0):
    """Linear solve: how much each relation is asked to carry. Returns (x, worst)."""
    L = laplacian(A).tocsr()
    b = omega / K
    b = b - b.mean()
    x, info = cg(L, b, rtol=1e-8, maxiter=2000)
    x = x - x.mean()
    r, c = sp.triu(A, 1).nonzero()
    worst = float(np.abs(x[r] - x[c]).max()) if len(r) else np.inf
    return x, worst


def _ball(A, i, hops=NEAR):
    """Events within `hops` relations of i (used by the 'near' variant only)."""
    order, pred = breadth_first_order(A, i, directed=False, return_predecessors=True)
    d = np.full(A.shape[0], -1, dtype=np.int64)
    d[i] = 0
    for v in order[1:]:
        d[v] = d[pred[v]] + 1
        if d[v] > hops:
            d[v] = -1
    return np.flatnonzero(d > 0)


def _add_where_strained(A, x, rows, cols, deg, n, rng, ceil, mode, budget):
    """Give the most strained events one more relation each, to a partner strained the other way."""
    order = np.argsort(-np.abs(x))
    added = 0
    for i in order:
        i = int(i)
        if deg[i] >= ceil:
            continue
        opposite = (x < 0) if x[i] > 0 else (x > 0)
        free = deg[:n] < ceil
        if mode == "near":
            cand = _ball(A, i)
            mask = np.zeros(n, dtype=bool)
            mask[cand[cand < n]] = True
            pool = np.flatnonzero(mask & free & opposite)
            if len(pool) == 0:
                pool = np.flatnonzero(mask & free)
        else:
            pool = np.flatnonzero(free & opposite)
            if len(pool) == 0:
                pool = np.flatnonzero(free)
        pool = pool[pool != i]
        if len(pool) == 0:
            continue
        j = int(pool[int(rng.integers(len(pool)))])
        rows += [i, j]
        cols += [j, i]
        deg[i] += 1
        deg[j] += 1
        added += 1
        if added >= budget:
            break
    return added


def grow(n_target, seed=0, ceil=CEIL, mode="far"):
    import n1_sync as N1
    rng = np.random.default_rng(seed)
    omega = rng.normal(0, 1, n_target)
    omega -= omega.mean()
    rows = [0, 1]
    cols = [1, 0]
    deg = np.zeros(n_target, dtype=np.int64)
    deg[0] = deg[1] = 1
    n = 2
    hist = []
    step = max(20, int(BATCH * n_target))
    while n < n_target:
        add = min(step, n_target - n)
        for _ in range(add):                                  # each new event arrives with one relation
            j = int(rng.integers(n))
            rows += [n, j]
            cols += [j, n]
            deg[n] += 1
            deg[j] += 1
            n += 1
        A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
        om = omega[:n] - omega[:n].mean()
        guard = 0
        while True:
            x, worst = strain(A, om)
            if worst <= THRESH or guard > 40 * n:
                break
            got = _add_where_strained(A, x, rows, cols, deg, n, rng, ceil, mode, CHUNK)
            if got == 0:
                break
            guard += got
            A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
        hist.append((n, len(rows) // 2, float(worst)))
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n_target, n_target))
    A.data[:] = 1.0
    for _ in range(80):                                       # R2: the full dynamics is the arbiter
        ok, spread = N1.holds(A, omega, K0)
        if ok:
            break
        x, worst = strain(A, omega)
        got = _add_where_strained(A, x, rows, cols, deg, n_target, rng, ceil, mode,
                                  max(8, n_target // 200))
        if got == 0:
            break
        A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n_target, n_target))
        A.data[:] = 1.0
    return A, omega, hist


def readings(A, seed=0):
    from c3b import mass_and_cut, bfs_distances
    n = A.shape[0]
    rng = np.random.default_rng(seed)
    centres = rng.choice(n, size=min(50, n), replace=False)
    d = bfs_distances(A, centres)
    r = mass_and_cut(A, d)
    md = float(d[np.isfinite(d)].mean())
    deg = np.asarray(A.sum(axis=1)).ravel()
    return dict(d_H=r.get("d_H"), beta=r.get("beta"), small_world=bool(r.get("small_world")), md=md,
                r_lo=r.get("r_lo"), r_max=r.get("r_max"), deg_mean=float(deg.mean()), deg_max=int(deg.max()))


def main():
    os.makedirs(OUT, exist_ok=True)
    import n1_sync as N1
    res = {}
    path = os.path.join(OUT, "step2.json")
    for mode in ("far", "near"):
        for n in SIZES:
            t0 = time.time()
            A, omega, hist = grow(n, seed=5, mode=mode)
            rr = readings(A, 1)
            holds, spread = N1.holds(A, omega, K0)
            rr.update(n=n, relations=int(A.nnz // 2), per_event=float(A.nnz / n), holds_full=bool(holds),
                      spread=spread, secs=round(time.time() - t0, 1), hist=hist[-4:], mode=mode)
            res["ed_%s_%d" % (mode, n)] = rr
            print("ED", mode, n, {k: rr[k] for k in ("d_H", "beta", "md", "per_event", "deg_max", "holds_full",
                                                     "small_world")}, "%.0fs" % (time.time() - t0), flush=True)
            json.dump(res, open(path, "w"), indent=1, default=str)
    rng = np.random.default_rng(1)                            # controls at matched sizes
    for name, fn, sizes in (("ring", N1.ring, [2000, 4000, 8000]), ("torus2", N1.torus2, [45, 63, 89]),
                            ("torus3", N1.torus3, [13, 16, 20]), ("web", N1.rand_regular, [2000, 4000, 8000])):
        for s in sizes:
            A = fn(s, rng)
            rr = readings(A, 1)
            rr.update(n=A.shape[0], per_event=float(A.nnz / A.shape[0]))
            res["%s_%d" % (name, A.shape[0])] = rr
            print(name, A.shape[0], {k: rr[k] for k in ("d_H", "beta", "md", "per_event")}, flush=True)
    json.dump(res, open(path, "w"), indent=1, default=str)
    lines = []
    for k, v in res.items():
        lines.append("%-14s n %6d | d_H %s beta %s | md %.2f | relations per event %.2f (max %s) | small world %s%s"
                     % (k, v["n"], None if v["d_H"] is None else round(v["d_H"], 3),
                        None if v.get("beta") is None else round(v["beta"], 3), v["md"], v["per_event"],
                        v.get("deg_max"), v.get("small_world"),
                        "" if "holds_full" not in v else " | holds at K0 %s (spread %.4f)" % (v["holds_full"], v["spread"])))
    for mode in ("far", "near"):
        eds = [res[k] for k in res if k.startswith("ed_%s_" % mode)]
        if len(eds) >= 2:
            n1_ok = all(e["holds_full"] for e in eds)
            dhs = [e["d_H"] for e in eds if e["d_H"] is not None]
            n2_ok = len(dhs) >= 2 and all(2.5 <= x <= 3.5 for x in dhs)
            lines.append("[%s] N1 (patterns hold together) %s | N2 (ball growth 2.5-3.5 at two sizes) %s | "
                         "N3 relations per event %s" % (mode, n1_ok, n2_ok, [round(e["per_event"], 2) for e in eds]))
    text = "\n".join(lines)
    open(os.path.join(HERE, "n2_grow.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
