"""Road P: does ED destroy what cannot hold its clocks together? (note 3 `P_Model_Spec.md`, C3; D2.)

Each generation, built only from ED's own parts:
  - every event passes on ONCE and is then spent (D2 P-Q3); one child each, a share have two, so the frontier grows;
  - spent events keep every relation and their child links (P-Q5) - that is the accumulated pattern, the past;
  - the new generation INHERITS neighbourhoods (A11 D4): siblings are linked, every parent relation is inherited
    exactly once, and relations per event is then held at its starting value by ED's conserved link budget (A7 C4).
    This is the RD5 revision: A11's probe leaked relations (4.0 -> 2.2 per event) and road P's first build inflated
    them (2 -> 12.6 for a ring); conserving them per event is ED's own rule and does neither;
  - THE FILTER (D2 P-Q2): a generation whose clocks cannot hold together is not allowed as it is. While it fails,
    relations are added where the strain is worst, up to the ceiling. Three outcomes: holds as inherited, holds
    after repair (how many recorded), or cannot be made to hold at all - DESTROYED, and the run ends there.
  - readings on the frontier (P-Q4, space now) and on the accumulated pattern alongside.

Four starts - ring, square torus, cubic torus, random 6-regular web (the objects calibrated in A11 C21) - at about
2,000 events, grown to four times that, three seeds, in TWO ARMS: filter on, and filter off as the control.

EXPECTATIONS, fixed in note 3 before this file was written:
  P0  the 3D grid and the web hold their clocks at every generation                                     high
  P1  MAIN: the line and the flat grid do NOT survive as themselves - forced above two dimensions by
      the repairs, or unable to hold at all                                                             about 55%
  P2  the 3D grid survives as itself, ball growth within 0.3 of its starting value                      about 40%
  P3  reported, no expectation: what the web start becomes; relations per event against ED's 6.7; how many
      relations the filter adds per generation and whether that grows with size
  P4  CONTROL: with the filter off, all four starts keep their shapes. IF THE LINE DIES HERE TOO, P1 IS VOID   high
Pass rule: "survives as itself" = |d_H(final) - d_H(start)| <= 0.3 with the clocks holding at every generation.

Labelled as Claude's (note 3): the growth share q, the start sizes, three seeds, the 0.3 tolerance, the bell-curve
rate spread, and "where the strain is worst, partnered near" as the repair rule - carried unchanged from A11 C22 so
the two attempts compare.
"""
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_11", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
import n1_sync as N1                                        # noqa: E402
import n2_grow as G                                         # noqa: E402

OUT = os.path.join(HERE, "p_runs")
CEIL = 60
K0 = 1.0
Q = 0.1               # share of parents with two children -> frontier grows about 1.1 per generation
TOL = 0.3             # P-Q1's tolerance on the reading
SEEDS = (1, 2, 3)
START = 2000
GROW = 4.0
REPAIR_MODE = "near"  # partners within three relations, the least shape-destroying repair


def to_adj(A):
    A = A.tocsr()
    return [set(A.indices[A.indptr[i]:A.indptr[i + 1]].tolist()) for i in range(A.shape[0])]


def to_A(adj, n=None):
    n = len(adj) if n is None else n
    rows, cols = [], []
    for i, s in enumerate(adj):
        for j in s:
            rows.append(i)
            cols.append(j)
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    A.data[:] = 1.0
    return A


def inherit(adj, rng, q=Q, ceil=CEIL):
    """One generation: every parent passes on once and is spent; children inherit the parents' neighbourhoods.

    REVISION (RD5, recorded before the rerun). The first version applied the cousin rule from BOTH parents' sides,
    so relations multiplied as the pattern grew - a ring ended up carrying 12.6 relations per event and the 3D grid
    28, against ED's link budget of 6.7. That inflation is Claude's, not ED's, and it makes locking easier, which
    flatters exactly the result P2 is testing. The rule now uses ED's own conserved link budget (A7 C4) instead:

      base      one child relation per parent relation, plus the sibling relations - every parent relation is
                inherited exactly once, so nothing is lost and the pattern cannot be cut apart;
      top-up    relations per event is then held at the starting value by adding extra cousin relations at random
                until the generation carries the same number per event as the one before it.

    So the inherited pattern conserves relations per event exactly. The filter may still add more on top - and how
    far above the budget that pushes it is P3, the thing being reported.
    """
    n_old = len(adj)
    r_old = sum(len(s) for s in adj)
    kids, m = [], 0
    for _ in range(n_old):
        c = 2 if rng.random() < q else 1
        kids.append(list(range(m, m + c)))
        m += c
    new = [set() for _ in range(m)]

    def link(a, b):
        if a != b and b not in new[a] and len(new[a]) < ceil and len(new[b]) < ceil:
            new[a].add(b)
            new[b].add(a)
            return 1
        return 0

    count = 0
    extras = []
    for p in range(n_old):
        ks = kids[p]
        for i in range(len(ks)):                            # siblings
            for j in range(i + 1, len(ks)):
                count += link(ks[i], ks[j])
        for qn in adj[p]:
            if qn <= p:
                continue
            kq = kids[qn]
            mm = max(len(ks), len(kq))
            count += link(ks[int(rng.integers(len(ks)))],    # base: one per parent relation
                          kq[int(rng.integers(len(kq)))])
            for i in range(mm):                             # the rest are candidates for the top-up
                extras.append((ks[i % len(ks)], kq[i % len(kq)]))
    target = int(round(r_old / 2.0 * m / n_old))            # conserve relations per event
    if extras and count < target:
        order = rng.permutation(len(extras))
        for k in order:
            if count >= target:
                break
            a, b = extras[int(k)]
            count += link(a, b)
    return new, kids


def repair(adj, omega, rng, ceil=CEIL):
    """The filter: while the clocks cannot hold, add relations where the strain is worst. Returns (adj, added, ok).

    IMPLEMENTATION NOTE (recorded before the run; it does not change the rule): the arbiter is still the full phase
    dynamics, but calling it after every handful of relations is far too slow at these sizes. So relations are added
    until the cheap linear test is satisfied, and only then are the clocks actually run; if they still fail, the
    linear bar is tightened and the cycle repeats. Same filter, fewer runs of the dynamics.
    """
    n = len(adj)
    rows, cols = [], []
    for i, s in enumerate(adj):
        for j in s:
            rows.append(i)
            cols.append(j)
    deg = np.array([len(s) for s in adj], dtype=np.int64)
    A = to_A(adj)
    added = 0
    bar = G.THRESH
    for _ in range(40):
        ok, spread = N1.holds(A, omega, K0)
        if ok:
            return to_adj(A), added, True
        while True:                                          # cheap linear test first, dynamics as the arbiter
            if int(deg.min()) >= ceil or added > 20 * n:
                return to_adj(A), added, False
            x, worst = G.strain(A, omega)
            if worst <= bar:
                break
            got = G._add_where_strained(A, x, rows, cols, deg, n, rng, ceil, REPAIR_MODE, max(16, n // 100))
            if got == 0:
                return to_adj(A), added, False
            added += got
            A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
            A.data[:] = 1.0
        bar *= 0.85
    return to_adj(A), added, False


def read(A, seed=1):
    r = G.readings(A, seed)
    return dict(d_H=None if r["d_H"] is None or np.isnan(r["d_H"]) else round(float(r["d_H"]), 3),
                beta=None if r["beta"] is None or np.isnan(r["beta"]) else round(float(r["beta"]), 3),
                md=round(r["md"], 2), small_world=r["small_world"], per_event=round(r["deg_mean"], 2),
                deg_max=r["deg_max"])


def reference(name, n, rng):
    """The same kind of object, freshly built at the size the run ended at.

    REVISION (RD5, recorded before the rerun). The pass rule compared the final reading with the STARTING reading,
    but the ball-growth reading drifts with size on a fixed shape - a cubic torus reads 2.36 at 2,200 events and
    2.67 at 8,000 (A11 C22's controls). Comparing a grown pattern with its own small starting value therefore
    charges the instrument's size bias against the pattern. "Kept its shape" is now judged against a fresh object
    of the same kind at the SAME final size, with the same tolerance of 0.3.
    """
    A = {"ring": lambda: N1.ring(n, rng), "grid2D": lambda: N1.torus2(int(round(n ** 0.5)), rng),
         "grid3D": lambda: N1.torus3(int(round(n ** (1.0 / 3.0))), rng),
         "web": lambda: N1.rand_regular(n, rng)}[name]()
    return read(A)["d_H"]


def run(name, seed, filter_on):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(START, rng), "grid2D": lambda: N1.torus2(45, rng),
          "grid3D": lambda: N1.torus3(13, rng), "web": lambda: N1.rand_regular(START, rng)}[name]()
    adj = to_adj(A0)
    omega = rng.normal(0, 1, len(adj))
    omega -= omega.mean()
    start = read(to_A(adj))
    target = GROW * len(adj)
    trail, held_every, destroyed, repairs, gen = [], True, False, [], 0
    t0 = time.time()
    while len(adj) < target:
        adj, kids = inherit(adj, rng)
        omega = rng.normal(0, 1, len(adj))
        omega -= omega.mean()
        if filter_on:
            adj, added, ok = repair(adj, omega, rng)
            repairs.append(added)
            if not ok:
                held_every = False
                destroyed = True
                break
        gen += 1
        if len(adj) >= target or gen % 4 == 0:
            trail.append((len(adj), read(to_A(adj))["d_H"]))
    A = to_A(adj)
    final = read(A)
    holds_end = None
    if not filter_on:                                       # the control arm asks about SHAPE only (note 3, P4);
        holds_end = bool(N1.holds(A, omega, K0)[0])         # whether it locks is reported, not required
    ref = reference(name, len(adj), np.random.default_rng(1000 + seed))
    kept = (ref is not None and final["d_H"] is not None and abs(final["d_H"] - ref) <= TOL)
    if ref is None and final["d_H"] is None:
        kept = True                                         # no dimension at either end (the web): shape unchanged
    survives = bool(kept and (held_every if filter_on else True))
    return dict(start_name=name, seed=seed, filter_on=filter_on, n0=A0.shape[0], n=len(adj),
                start=start, final=final, ref_d_H=ref, survives=bool(survives), kept=bool(kept), holds_end=holds_end,
                destroyed=bool(destroyed),
                held_every=bool(held_every), repairs=repairs, trail=trail, secs=round(time.time() - t0, 1))


def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "roadP.json")
    res = []
    for filter_on in (True, False):
        for name in ("ring", "grid2D", "grid3D", "web"):
            for seed in SEEDS:
                r = run(name, seed, filter_on)
                res.append(r)
                print("%-6s seed %d filter %-5s | n %5d -> %5d | d_H %s -> %s (same shape at that size: %s) | "
                      "kept %s survives %s destroyed %s | relations/event %s -> %s | repairs %s | %.0fs"
                      % (name, seed, filter_on, r["n0"], r["n"], r["start"]["d_H"], r["final"]["d_H"], r["ref_d_H"],
                         r["kept"], r["survives"], r["destroyed"], r["start"]["per_event"], r["final"]["per_event"],
                         sum(r["repairs"]), r["secs"]), flush=True)
                json.dump(res, open(path, "w"), indent=1, default=str)
    lines = []
    for r in res:
        lines.append("%-6s seed %d filter %-5s | n %5d -> %5d | d_H %s -> %s (same shape at that size %s) | "
                     "md %.1f -> %.1f | small world %s -> %s | relations/event %.2f -> %.2f | kept %s | survives %s"
                     " | destroyed %s | repairs %d"
                     % (r["start_name"], r["seed"], r["filter_on"], r["n0"], r["n"], r["start"]["d_H"],
                        r["final"]["d_H"], r["ref_d_H"], r["start"]["md"], r["final"]["md"],
                        r["start"]["small_world"], r["final"]["small_world"], r["start"]["per_event"],
                        r["final"]["per_event"], r["kept"], r["survives"], r["destroyed"], sum(r["repairs"])))

    def arm(name, on):
        return [r for r in res if r["start_name"] == name and r["filter_on"] is on]
    p0 = all(r["held_every"] for n in ("grid3D", "web") for r in arm(n, True))
    p1 = all(not r["survives"] for n in ("ring", "grid2D") for r in arm(n, True))
    p2 = all(r["survives"] for r in arm("grid3D", True))
    p4 = all(r["kept"] for n in ("ring", "grid2D", "grid3D", "web") for r in arm(n, False))
    void = any(not r["kept"] for n in ("ring", "grid2D") for r in arm(n, False))
    lines.append("P0 (3D grid and web hold at every generation) %s" % p0)
    lines.append("P1 (line and flat grid do NOT survive as themselves) %s%s"
                 % (p1, "  ** VOID: they do not survive with the filter OFF either **" if void else ""))
    lines.append("P2 (3D grid survives within %.1f) %s" % (TOL, p2))
    lines.append("P3 relations per event, filter on: %s"
                 % {n: round(float(np.mean([r["final"]["per_event"] for r in arm(n, True)])), 2)
                    for n in ("ring", "grid2D", "grid3D", "web")})
    lines.append("P4 (control: all four keep their shapes with the filter off) %s" % p4)
    text = "\n".join(lines)
    open(os.path.join(HERE, "p_persist.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
