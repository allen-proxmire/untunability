"""Standing phase, attempt 1 (RD52): does P12's coherence part, as read in RD33 (Wilson's form: phases should close
around small loops), fix a small-loop phase that is neither 0 nor pi (the condition for a hand, C283, C290)?

ED's lane graph. Nodes (locus, channel) on a periodic lattice in dimension d; channels: Internal plus 2d lanes (+axis,
-axis). Edges: lane mixing at every locus between every pair of channels (Grover off-diagonal 2/n, n = 2d + 1, as in
the real rule), and lane hops: lane +a hops to u + e_a, lane -a to u - e_a, each with amplitude i (as in the real
rule's generator, own-direction hop +i). Phase variables, uniform in space: one per lane hop (2d) and one per channel
pair for mixing (n(n-1)/2, antisymmetric). Amplitude on an edge = base amplitude times e^{i variable}.

Small loops: all simple cycles of length 3 and 4 in this graph (ring size 5, so no loop wraps around the lattice).
Costs: Wilson (coherence as read) = sum over small loops of (1 - cos flux); a 'pi-preferring' variant (exploratory,
no ED motivation beyond the real rule's lane loops sitting at pi) = sum of (1 + cos flux).
Minimized from 20 random starts (L-BFGS, analytic gradient). A minimum is time-reversal symmetric (no hand possible,
C275 analysis B) if every small-loop flux is 0 or pi.

Predictions frozen before the first run (2026-09-14):
  S1 (code) At zero variables, the real rule's structure: every on-site triangle has flux 0 and every lane loop
     (hop, mix, hop back, mix) has flux pi, in 1D and 3D.
  S2 Wilson, 1D: minimum cost < 1e-8 and every small-loop flux within 1e-4 of 0, in 20 of 20 starts.
  S3 Wilson, 3D: the same.
  S4 pi-preferring, 1D: minimum cost < 1e-8 and every small-loop flux within 1e-4 of pi, in 20 of 20 starts.
  S5 pi-preferring, 3D (exploratory): frustrated: every start ends with cost > 1e-3, and at least one small-loop flux
     with |sin flux| > 0.1 (neither 0 nor pi).
Reading rule: if S2 and S3 hold, coherence as read fixes a time-reversal-symmetric phase, so attempt 1 does not give a
hand. S5, if it holds, is a lead for a later attempt, not a result.
Exit code: S1.

Changes after freezing (2026-09-14):
  1. Run 1 (attempt1_run1.txt): S1, S2, S4, S5 RIGHT; S3 WRONG. In 3D with the Wilson cost the best start reached
     cost 0 with every small-loop flux 0, but some starts stopped at local minima (cost up to 8,750), so 'in 20 of 20
     starts' failed. Every start's fluxes, local minima included, were 0 or pi (largest |sin flux| 0.000), so the
     reading rule's conclusion holds: coherence as read fixes a time-reversal-symmetric phase. S3's criterion (every
     start reaches the global minimum) was Claude's error. In 3D with the pi-preferring cost every start ended at cost
     13,930 with some fluxes neither 0 nor pi (|sin| up to 0.992), while the best start's lane-loop fluxes stayed at pi.
  2. The exit code now checks S1 and that run 1's recorded results reproduce.
  3. Diagnostic attempt1_frustration_diagnostic.py (not pre-registered): which loops carry the in-between fluxes.
"""
import itertools
import sys

import numpy as np
from scipy.optimize import minimize

L = 5


def build(d):
    sites = list(itertools.product(range(L), repeat=d))
    n = 2 * d + 1
    chans = ["I"] + [s + str(a) for a in range(d) for s in "+-"]
    index = {}
    for si, s in enumerate(sites):
        for ci in range(n):
            index[(s, ci)] = len(index)
    pairs = list(itertools.combinations(range(n), 2))
    nvar = 2 * d + len(pairs)
    edges = {}  # (u, v) -> (base phase, var coefficient vector) for amplitude H[v, u]

    def add(u, v, base, coeff):
        edges[(u, v)] = (base, coeff)
        edges[(v, u)] = (-base, -coeff)

    for s in sites:
        for pi_, (c1, c2) in enumerate(pairs):
            coeff = np.zeros(nvar)
            coeff[2 * d + pi_] = 1.0
            add(index[(s, c1)], index[(s, c2)], 0.0, coeff)
        for a in range(d):
            for k, sign in enumerate((1, -1)):
                ci = 1 + 2 * a + k
                t = list(s)
                t[a] = (t[a] + sign) % L
                coeff = np.zeros(nvar)
                coeff[2 * a + k] = 1.0
                add(index[(s, ci)], index[(tuple(t), ci)], np.pi / 2, coeff)
    adj = {}
    for (u, v) in edges:
        adj.setdefault(u, []).append(v)
    return index, edges, adj, nvar, n, chans


def cycles(adj, maxlen=4):
    found = []
    for s in adj:
        stack = [(s, [s])]
        while stack:
            node, path = stack.pop()
            for nb in adj[node]:
                if nb == s and 3 <= len(path) <= maxlen:
                    if path[1] < path[-1]:
                        found.append(list(path))
                elif nb > s and nb not in path and len(path) < maxlen:
                    stack.append((nb, path + [nb]))
    return found


def flux_system(cyc, edges, nvar):
    base = np.zeros(len(cyc))
    M = np.zeros((len(cyc), nvar))
    for i, c in enumerate(cyc):
        for u, v in zip(c, c[1:] + c[:1]):
            b, co = edges[(u, v)]
            base[i] += b
            M[i] += co
    return base, M


def minimize_cost(base, M, sign, rng, starts=20):
    def f(x):
        fl = base + M @ x
        return float(np.sum(1 - sign * np.cos(fl)))

    def g(x):
        fl = base + M @ x
        return M.T @ (sign * np.sin(fl))

    out = []
    for _ in range(starts):
        x0 = rng.uniform(-np.pi, np.pi, M.shape[1])
        r = minimize(f, x0, jac=g, method="L-BFGS-B", options={"maxiter": 5000, "gtol": 1e-12, "ftol": 1e-15})
        fl = np.angle(np.exp(1j * (base + M @ r.x)))
        out.append((r.fun, fl))
    return out


def main():
    rng = np.random.default_rng(52)
    ok_s1 = True
    verdicts = {}
    for d in (1, 3):
        index, edges, adj, nvar, n, chans = build(d)
        cyc = cycles(adj)
        base, M = flux_system(cyc, edges, nvar)
        fl0 = np.angle(np.exp(1j * base))
        site_of = {v: k[0] for k, v in index.items()}
        tri = [i for i, c in enumerate(cyc) if len(c) == 3]
        lane = [i for i, c in enumerate(cyc) if len(c) == 4 and len({site_of[x] for x in c}) == 2]
        onsite4 = [i for i, c in enumerate(cyc) if len(c) == 4 and len({site_of[x] for x in c}) == 1]
        s1 = (np.all(np.abs(np.sin(fl0[tri])) < 1e-12) and np.all(np.cos(fl0[tri]) > 0)
              and np.all(np.abs(np.sin(fl0[lane])) < 1e-12) and np.all(np.cos(fl0[lane]) < 0))
        ok_s1 &= bool(s1)
        print("d = %d: %d channels, %d variables, small loops %d (triangles %d, lane loops %d, on-site 4-loops %d, other %d); "
              "S1 triangles flux 0 and lane loops flux pi: %s"
              % (d, n, nvar, len(cyc), len(tri), len(lane), len(onsite4), len(cyc) - len(tri) - len(lane) - len(onsite4), s1), flush=True)
        for sign, name in ((1, "Wilson"), (-1, "pi-preferring")):
            res = minimize_cost(base, M, sign, rng)
            costs = np.array([r[0] for r in res])
            target = 0.0 if sign == 1 else np.pi
            dev = [float(np.max(np.abs(np.angle(np.exp(1j * (fl - target)))))) for _, fl in res]
            maxsin = [float(np.max(np.abs(np.sin(fl)))) for _, fl in res]
            best = int(np.argmin(costs))
            lane_fl = res[best][1][lane]
            print("  %s: min cost %.3e, max cost %.3e; largest distance from target %.2e (best start %.2e); "
                  "largest |sin flux| %.3f; best start's lane-loop fluxes (distinct, rounded) %s"
                  % (name, costs.min(), costs.max(), max(dev), dev[best], max(maxsin),
                     sorted(set(np.round(lane_fl, 3)))[:8]), flush=True)
            verdicts[(d, name)] = (costs, dev, maxsin)

    c, dv, _ = verdicts[(1, "Wilson")]
    s2 = bool(np.all(c < 1e-8) and max(dv) < 1e-4)
    c, dv, _ = verdicts[(3, "Wilson")]
    s3 = bool(np.all(c < 1e-8) and max(dv) < 1e-4)
    c, dv, _ = verdicts[(1, "pi-preferring")]
    s4 = bool(np.all(c < 1e-8) and max(dv) < 1e-4)
    c, _, ms = verdicts[(3, "pi-preferring")]
    s5 = bool(np.all(c > 1e-3) and all(m > 0.1 for m in ms))
    print("\nFrozen predictions:")
    for name, passed in (("S1 real rule's structure (triangles 0, lane loops pi)", ok_s1),
                         ("S2 Wilson 1D: fluxes all 0", s2), ("S3 Wilson 3D: fluxes all 0", s3),
                         ("S4 pi-preferring 1D: fluxes all pi", s4), ("S5 pi-preferring 3D: frustrated, some flux neither 0 nor pi", s5)):
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    cw, _, msw = verdicts[(3, "Wilson")]
    cp, _, msp = verdicts[(3, "pi-preferring")]
    recorded = ok_s1 and s2 and s4 and s5 and float(cw.min()) < 1e-8 and max(msw) < 1e-6 and abs(float(cp.min()) - 13930) < 5
    print("RECORDED RESULTS REPRODUCE" if recorded else "RECORDED RESULTS DO NOT REPRODUCE")
    return ok_s1 and recorded


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
