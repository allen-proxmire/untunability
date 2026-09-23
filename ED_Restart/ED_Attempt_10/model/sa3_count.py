"""Recount under choice (i), NARROW BOTH WAYS (note 11, option (a); Allen: 'can we just do what will make it work').

Moves: edge split (one per allowed link neighbour, as the port), NARROW merge (v merges into a only if merging is the exact
reverse of an edge split of (a, u): v's neighbours are a, u and the cycle R = Lk(va), deg v = |R| + 2, u adjacent to every
vertex of R, u not adjacent to a; link condition and ceiling as before), 2-3 and 3-2 flips. Self-inverse by construction.
a_v = edge splits + narrow merges + apportioned flip sites; s = ln e_m(a) / V as before. This is a TEST of choice (i); it
does not change D10 unless Allen adopts (i).

Checks, expectation and exit, written before this run:
  N0  on n = 6 flat and grown slices: every counted narrow merge, applied to a copy and followed by the edge split of (a, u)
      with the child reusing v's position, restores the original exactly; every edge split, applied, leaves a child that
      is counted as narrow-mergeable back into its parent (bijection both ways).
  Expectation (about 65 per cent): the flat reference FREF2 above every grown slice by the margin.
  Reported, no pass rule: the share of events able to merge in each slice (the 'too rigid' question).
  Margin = 2 x seed difference (all counts exact).
  N0 fails -> code problem, fixed and rerun, recorded.
  FREF2 above every grown slice by the margin -> 'narrow both ways: counting leans toward flat at one tick' -> to Allen:
      adopt (i) (revising D10) and build stage B with narrow moves?
  every grown slice above FREF2 by the margin -> 'narrow both ways: counting leans toward crowded slices' -> road S
      options (b)/(c).
  otherwise -> too close -> to Allen.
"""
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sa_count as sc                                           # noqa: E402

OUT = os.path.join(HERE, "sa3_runs")


def narrow_merges(M, v, nbr):
    """Targets a such that merging v into a is the exact reverse of an edge split of (a, u)."""
    out = []
    Nv = nbr[v]
    for a in Nv:
        if not M.link_condition(v, a):
            continue
        R = Nv & nbr[a]
        if len(Nv) != len(R) + 2:
            continue
        rest = Nv - R - {a}
        if len(rest) != 1:
            continue
        u = next(iter(rest))
        if u in nbr[a] or not R <= nbr[u] or M.valence(v, u) != len(R) or len(M.tets_of(v)) != 2 * len(R):
            continue                  # FIX (N0 caught it): Lk(vu) must be the whole ring R, i.e. Lk(v) a suspension
        pl = M.merge_plan(v, a)
        if pl is None or not M.allowed(pl, sc.BIG, None, gone=v, cap=sc.CAP)[0]:
            continue
        out.append((a, u))
    return out


def options_narrow(M):
    arr0, deg, tot = sc.options3(M)                              # general merges + edge splits + flips
    verts = [int(v) for v in M.vertices()]
    nbr = {v: set(int(w) for w in M.neighbours(v)) for v in verts}
    gen = np.zeros(len(verts))
    nar = np.zeros(len(verts))
    for i, v in enumerate(verts):
        for a in nbr[v]:
            if M.link_condition(v, a):
                pl = M.merge_plan(v, a)
                if pl is not None and M.allowed(pl, sc.BIG, None, gone=v, cap=sc.CAP)[0]:
                    gen[i] += 1
        nar[i] = len(narrow_merges(M, v, nbr))
    return arr0 - gen + nar, deg, int(nar.sum()), float((nar > 0).mean())


def check_N0():
    from h5_select import copy_state
    res = []
    for name in ("flat", "grown"):
        M, pool, BL, V0 = sc.fresh3(6, 5)
        if name == "grown":
            sc.grow3(M, pool, BL, V0, 30, 1.0, dict(structure=True, budget=True, link=True))
        before = sorted(tuple(sorted(M.tet(int(t)))) for t in M.S.t_items[:M.T])
        verts = [int(v) for v in M.vertices()]
        nbr = {v: set(int(w) for w in M.neighbours(v)) for v in verts}
        bad_m = n_m = 0
        for v in verts:
            for a, u in narrow_merges(M, v, nbr):
                n_m += 1
                C = copy_state(M)
                C.merge(v, a)
                y = C.split(a, u)
                got = sorted(tuple(sorted(v if w == y else w for w in C.tet(int(t)))) for t in C.S.t_items[:C.T])
                if got != before or C.check():
                    bad_m += 1
        bad_s = n_s = 0
        for x in verts[:60]:
            for u in sorted(nbr[x]):
                pl = M.split_plan(x, u, M.next_free_vertex())
                if pl is None or not M.allowed(pl, sc.BIG, None, cap=sc.CAP)[0]:
                    continue
                n_s += 1
                C = copy_state(M)
                y = C.split(x, u)
                cv = [int(w) for w in C.vertices()]
                cn = {w: set(int(z) for z in C.neighbours(w)) for w in cv}
                if (x, u) not in narrow_merges(C, y, cn):
                    bad_s += 1
        res.append(dict(slice=name, merges=n_m, merge_bad=bad_m, splits=n_s, split_bad=bad_s))
    return res


def do_job(job):
    kind, seed = job
    path = os.path.join(OUT, "3D_%s_s%d.json" % (kind, seed))
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    if kind == "FREF2":
        import sa_flatref2 as fr
        M, _, _, _ = fr.build(0)
        ok = dict(structure=not M.check())
    else:
        M, ok = sc.slice3(kind, 24, seed)
    a, deg, nmerge, share = options_narrow(M)
    out = sc.summarise(a, deg, sc.mean_distance(M.adjacency()[0], seed), M.V)
    out.update(kind=kind, seed=seed, ok=ok, narrow_merges=nmerge, share_mergeable=share,
               seconds=time.perf_counter() - t0)
    json.dump(out, open(path, "w", encoding="utf-8"))
    return path, out["seconds"]


JOBS = [("FREF2", 0), ("FL", 0), ("F1", 0), ("F1", 1), ("W1", 0), ("W1", 1)]


def report():
    L = []
    n0 = json.load(open(os.path.join(OUT, "N0.json"), encoding="utf-8"))
    n0ok = all(r["merge_bad"] == 0 and r["split_bad"] == 0 for r in n0)
    L.append("N0 %s %s" % (n0ok, n0))
    rows = {}
    for k, s in JOBS:
        p = os.path.join(OUT, "3D_%s_s%d.json" % (k, s))
        if os.path.exists(p):
            rows[(k, s)] = json.load(open(p, encoding="utf-8"))
    for (k, s), r in rows.items():
        L.append("%-5s s%d V %5d s %.5f a_mean %.3f a_sd %.3f | narrow merges %d, share of events able to merge %.3f | "
                 "deg sd %.2f max %d | md %.3f | ok %s" % (k, s, r["V"], r["s"], r["a_mean"], r["a_sd"], r["narrow_merges"],
                                                           r["share_mergeable"], r["deg_sd"], r["deg_max"],
                                                           r["mean_distance"], all(r["ok"].values())))
    if len(rows) == len(JOBS):
        ref = rows[("FREF2", 0)]["s"]
        g = {"%s_s%d" % k: rows[k]["s"] for k in (("F1", 0), ("F1", 1), ("W1", 0), ("W1", 1))}
        spread = max(abs(g["F1_s0"] - g["F1_s1"]), abs(g["W1_s0"] - g["W1_s1"]))
        margin = 2 * spread
        L.append("margin %.5f; grown - FREF2: %s" % (margin, ", ".join("%s %+.5f" % (k, v - ref) for k, v in g.items())))
        if not n0ok:
            L.append("VERDICT: N0 failed - code problem.")
        elif all(ref - v > margin for v in g.values()):
            L.append("VERDICT: narrow both ways: counting leans toward flat at one tick -> to Allen (adopt (i)?).")
        elif all(v - ref > margin for v in g.values()):
            L.append("VERDICT: narrow both ways: counting leans toward crowded slices -> road S options (b)/(c).")
        else:
            L.append("VERDICT: too close -> to Allen.")
    text = "\n".join(L)
    open(os.path.join(HERE, "sa3_count.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    n0p = os.path.join(OUT, "N0.json")
    if not os.path.exists(n0p):
        json.dump(check_N0(), open(n0p, "w", encoding="utf-8"))
    print(open(n0p, encoding="utf-8").read(), flush=True)
    from multiprocessing import Pool
    with Pool(6) as p:
        for path, sec in p.imap_unordered(do_job, sorted(JOBS, key=lambda j: j[0] in ("W1", "F1"), reverse=True)):
            print("  %s %.0f s" % (os.path.basename(path), sec), flush=True)
    report()


if __name__ == "__main__":
    main()
