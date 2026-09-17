"""Diagnostic after attempt 1 (not pre-registered): in the 3D pi-preferring (frustrated) minimum, which small loops carry
fluxes neither 0 nor pi, and does the 1D block (Internal, +x, -x) carry any? Also: are the Wilson local minima
time-reversal symmetric? Same graph, seed and optimizer as attempt1_coherence.py."""
import numpy as np

import attempt1_coherence as a1

rng = np.random.default_rng(52)
index, edges, adj, nvar, n, chans = a1.build(3)
cyc = a1.cycles(adj)
base, M = a1.flux_system(cyc, edges, nvar)
site_of = {v: k[0] for k, v in index.items()}
chan_of = {v: k[1] for k, v in index.items()}
kind = []
for c in cyc:
    if len(c) == 3:
        kind.append("triangle")
    elif len({site_of[x] for x in c}) == 2:
        kind.append("lane loop")
    else:
        kind.append("on-site 4-loop")
kind = np.array(kind)
block = np.array([len(c) == 3 and {chan_of[x] for x in c} == {0, 1, 2} for c in cyc])

for sign, name in ((1, "Wilson"), (-1, "pi-preferring")):
    res = a1.minimize_cost(base, M, sign, rng, starts=20)
    costs = np.array([r[0] for r in res])
    best = int(np.argmin(costs))
    fl = res[best][1]
    other = np.abs(np.sin(fl)) > 0.1
    print("%s: best cost %.4g; costs over starts: %s" % (name, costs.min(), " ".join("%.4g" % c for c in sorted(set(np.round(costs, 3))))))
    for k in ("triangle", "lane loop", "on-site 4-loop"):
        m = kind == k
        vals = sorted(set(np.round(np.abs(fl[m & other]), 3)))
        print("  %s: %d of %d with flux neither 0 nor pi; distinct |flux| among those: %s" % (k, int(np.sum(m & other)), int(np.sum(m)), vals[:6]))
    bf = fl[block]
    print("  1D block triangle (Internal, +x, -x): fluxes %s" % sorted(set(np.round(bf, 3))))
    all_other = [int(np.sum(np.abs(np.sin(r[1])) > 0.1)) for r in res]
    print("  loops with flux neither 0 nor pi, per start: %s" % all_other)
