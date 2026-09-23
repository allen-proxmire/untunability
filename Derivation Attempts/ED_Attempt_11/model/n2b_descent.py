"""Road N, step 2b: attachment by descent (A11 D4, "passing on reaches a neighbourhood").

Step 2 (C22) found that ED's grown patterns hold their clocks together but are small worlds with no dimension,
and that the shape was fixed by the arrival rule - a new event attached to a RANDOM existing event - before the
sync rule got a say. This is the same model with exactly one change, and it is a change ED already decided:

    A11 D4: passing on reaches a NEIGHBOURHOOD.
    So a new event attaches to its parent AND to M of the parent's current neighbours, not to a random event.

Nothing else differs from n2_grow.py: relations stick (D12), the ceiling caps degree, relations are added only
where the strain is and only while the clocks fail to hold, stopped as soon as they hold (D13), the pull is fixed
at K0 = 1 in units of the rate spread, and the full phase dynamics is the arbiter.

Note that NO locality is assumed by this: the parent is still drawn uniformly from all events. What changes is
that a new event is glued into an existing neighbourhood instead of hanging off one event, so arrival can no
longer create a shortcut between two far-apart parts of the pattern.

Variants run (all reported):
    M = 1   parent + one of the parent's neighbours (triangle closure); arrival costs 2 relations
    M = 2   parent + two of them; arrival costs 3 relations
    partner rule for the strain-driven additions: "near" (within 3 relations) and "far" (anywhere), as in step 2

EXPECTATIONS, fixed here before the run (Claude's, labelled; N1-N3 are closed by C22 and are not re-opened):
  N4  the patterns still hold their clocks together at every size          high confidence
  N5  MAIN ONE: with descent attachment, mean distance grows like a POWER of size rather than its logarithm,
      the ball-growth reading is defined at 4,000 and 8,000, and the small-world flag is clear    about 45%
  N6  given N5: the ball-growth reading lands between 2.5 and 3.5 at two sizes                    about 30%
  N7  reported, no expectation: relations per event against ED's link budget of 6.7
What each outcome means:
  N5 and N6 hold      -> ED's own content (clocks + budget + commitment + passing on to a neighbourhood) makes a
                         three-dimensional pattern with no geometry assumed anywhere. The result road N was for.
  N5 holds, N6 fails  -> descent gives a pattern with a definite dimension, but not three; something else sets
                         which dimension, and "fewest directions" is not it.
  N5 fails            -> gluing into a neighbourhood is not enough either; the small world is coming from the
                         uniform choice of parent, and ED needs to say something about WHICH event passes on.
"""
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
OUT = os.path.join(HERE, "n2_runs")
CEIL = 60
K0 = 1.0
SIZES = (2000, 4000, 8000)
BATCH = 0.02
CHUNK = 8


def grow_descent(n_target, seed=0, ceil=CEIL, m=1, mode="near"):
    import n1_sync as N1
    import n2_grow as G
    rng = np.random.default_rng(seed)
    omega = rng.normal(0, 1, n_target)
    omega -= omega.mean()
    adj = [set() for _ in range(n_target)]
    rows, cols = [0, 1], [1, 0]
    adj[0].add(1)
    adj[1].add(0)
    deg = np.zeros(n_target, dtype=np.int64)
    deg[0] = deg[1] = 1
    n = 2
    hist = []
    step = max(20, int(BATCH * n_target))

    def link(a, b):
        if a == b or b in adj[a] or deg[a] >= ceil or deg[b] >= ceil:
            return
        adj[a].add(b)
        adj[b].add(a)
        rows.append(a)
        cols.append(b)
        rows.append(b)
        cols.append(a)
        deg[a] += 1
        deg[b] += 1

    while n < n_target:
        add = min(step, n_target - n)
        for _ in range(add):
            p = int(rng.integers(n))                        # any event may pass on (no locality assumed here)
            link(n, p)
            nb = [v for v in adj[p] if v != n and deg[v] < ceil]
            if nb:
                for v in rng.permutation(nb)[:m]:           # D4: passing on reaches the parent's neighbourhood
                    link(n, int(v))
            n += 1
        A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
        om = omega[:n] - omega[:n].mean()
        guard = 0
        while True:
            x, worst = G.strain(A, om)
            if worst <= G.THRESH or guard > 40 * n:
                break
            got = G._add_where_strained(A, x, rows, cols, deg, n, rng, ceil, mode, CHUNK)
            if got == 0:
                break
            for k in range(len(rows) - 2 * got, len(rows), 2):
                adj[rows[k]].add(cols[k])
                adj[cols[k]].add(rows[k])
            guard += got
            A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
        hist.append((n, len(rows) // 2, float(worst)))
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n_target, n_target))
    A.data[:] = 1.0
    for _ in range(80):
        ok, spread = N1.holds(A, omega, K0)
        if ok:
            break
        x, worst = G.strain(A, omega)
        got = G._add_where_strained(A, x, rows, cols, deg, n_target, rng, ceil, mode, max(8, n_target // 200))
        if got == 0:
            break
        A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n_target, n_target))
        A.data[:] = 1.0
    return A, omega, hist


def main():
    os.makedirs(OUT, exist_ok=True)
    import n1_sync as N1
    import n2_grow as G
    res = {}
    path = os.path.join(OUT, "step2b.json")
    for m, mode in ((1, "near"), (2, "near"), (1, "far")):
        for n in SIZES:
            t0 = time.time()
            A, omega, hist = grow_descent(n, seed=5, m=m, mode=mode)
            rr = G.readings(A, 1)
            holds, spread = N1.holds(A, omega, K0)
            rr.update(n=n, relations=int(A.nnz // 2), per_event=float(A.nnz / n), holds_full=bool(holds),
                      spread=spread, secs=round(time.time() - t0, 1), m=m, mode=mode, hist=hist[-4:])
            res["d%d_%s_%d" % (m, mode, n)] = rr
            print("descent m=%d %s" % (m, mode), n,
                  {k: rr[k] for k in ("d_H", "beta", "md", "per_event", "deg_max", "holds_full", "small_world")},
                  "%.0fs" % (time.time() - t0), flush=True)
            json.dump(res, open(path, "w"), indent=1, default=str)
    lines = []
    for k, v in res.items():
        lines.append("%-14s n %6d | d_H %s beta %s | md %.2f | relations per event %.2f (max %s) | small world %s "
                     "| holds %s" % (k, v["n"], None if v["d_H"] is None else round(v["d_H"], 3),
                                     None if v.get("beta") is None else round(v["beta"], 3), v["md"], v["per_event"],
                                     v.get("deg_max"), v.get("small_world"), v["holds_full"]))
    for key in ("d1_near", "d2_near", "d1_far"):
        run = [res[k] for k in res if k.startswith(key + "_")]
        if len(run) >= 2:
            n4 = all(r["holds_full"] for r in run)
            mds = [r["md"] for r in run]
            defined = [r["d_H"] for r in run if r["d_H"] is not None and not np.isnan(r["d_H"])]
            sw = [r["small_world"] for r in run]
            # N5: mean distance growing like a power of size, read as the slope of log md against log n
            sl = float(np.polyfit(np.log([r["n"] for r in run]), np.log(mds), 1)[0])
            n5 = (sl > 0.15) and len(defined) >= 2 and not all(sw)
            n6 = len(defined) >= 2 and all(2.5 <= x <= 3.5 for x in defined)
            lines.append("[%s] N4 hold %s | N5 shape has a size (md slope %.3f, defined %d, small world %s) %s | "
                         "N6 ball growth 2.5-3.5 %s | N7 relations per event %s"
                         % (key, n4, sl, len(defined), sw, n5, n6, [round(r["per_event"], 2) for r in run]))
    text = "\n".join(lines)
    open(os.path.join(HERE, "n2b_descent.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
