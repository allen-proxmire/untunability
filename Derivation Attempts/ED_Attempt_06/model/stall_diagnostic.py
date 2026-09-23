"""Follow-up diagnostic for the timing trial (NOT pre-registered).

The timing trial (central setting, N_final = 1,000, seed 0) stalled at 50 loci:
10,000 consecutive failed births. This script reproduces the same run
(deterministic seed) up to the stall, saves the pattern, and classifies every
relation as a possible birth site:
  * cap: one or both ends already have k_max relations;
  * curvature: both ends have room, but adding the newborn would put some
    relation touching {newborn, a, b} below kappa_min (which relation, its
    curvature);
  * allowed.
It also reports the degree distribution, and how many sync pulls and rewires
were accepted. No process reading is taken; no rule changes.
"""
import json
import numpy as np
from collections import Counter
from cgp import CGP


def main():
    g = CGP(K_over_sigma=10, c=1.0, k_max=12, kappa_min=-0.1, N_final=1000, seed=0)
    while g.n < g.N_final and not g.stalled:
        g.tick(births=True)
    n, m = g.n, g.m
    deg = np.array([len(g.adj[x]) for x in range(n)])
    print(f"stalled={g.stalled} at tick {g.t}: loci {n}, relations {m}, mean degree {2*m/n:.2f}")
    print("degree counts:", dict(sorted(Counter(deg.tolist()).items())))
    print("counts:", g.counts)
    kinds = Counter()
    fail_edges = Counter()
    kappas = []
    for p in range(m):
        a, b = int(g.ei[p]), int(g.ej[p])
        if deg[a] >= g.k_max or deg[b] >= g.k_max:
            kinds["cap"] += 1
            continue
        z = g._new_locus()
        g._add_edge(z, a)
        g._add_edge(z, b)
        worst = None
        seen = set()
        for u in (z, a, b):
            for v in g.adj[u]:
                key = (u, v) if u < v else (v, u)
                if key in seen:
                    continue
                seen.add(key)
                k = g.curvature(u, v)
                if worst is None or k < worst[0]:
                    worst = (k, "newborn relation" if z in key else "existing relation at a parent")
        g._remove_edge(z, a)
        g._remove_edge(z, b)
        g.n -= 1
        if worst[0] < g.kappa_min:
            kinds["curvature"] += 1
            fail_edges[worst[1]] += 1
            kappas.append(worst[0])
        else:
            kinds["allowed"] += 1
    print("birth sites:", dict(kinds))
    print("curvature failures by worst relation:", dict(fail_edges))
    if kappas:
        print(f"worst curvature among curvature-blocked sites: min {min(kappas):.3f}, median {float(np.median(kappas)):.3f}, max {max(kappas):.3f}")
    with open("stall_diagnostic.json", "w", encoding="utf-8") as f:
        json.dump(dict(n=n, m=m, degrees=deg.tolist(),
                       edges=[[int(g.ei[p]), int(g.ej[p])] for p in range(m)],
                       kinds=dict(kinds), fail_edges=dict(fail_edges), counts=g.counts), f)


if __name__ == "__main__":
    main()
