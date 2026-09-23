"""Standing phase, attempt 3 (RD54, the last under the exit rule): longer loops.

Coherence scores, in 3D (Internal plus 6 lanes, every pair of channels mixing at a locus, lanes hopping with amplitude i
in their own direction), each loop counted once per locus:
  on-site triangles (35) and on-site 4-loops (105): mixing only;
  lane loops (3): hop +a, switch to -a, hop -a back, switch to +a; flux pi + h(+a) + h(-a);
  spatial squares (48): around the unit square u, u+e_a, u+e_a+e_b, u+e_b (a < b), each side traversed by one of the
    two lanes along that axis (forward in its own direction or backward), switching lanes at the corners.
Phase variables, uniform in space: one per lane hop (6), one per channel pair (21). Costs: Wilson (1 - cos flux) and
pi-preferring (1 + cos flux), 20 random starts each (L-BFGS). Square weight 1 is the reading tested; weights 0.25 and 4
are reported only.
A lane-loop flux neither 0 nor pi is the standing phase the hand needs (C288, C300).
Stage 2, run only if some cost's best minimum has a lane-loop flux neither 0 nor pi: put its lane phase theta = (h(+x) +
h(-x)) / 2 (lane-loop flux pi + 2 theta) and its mixing flux F on the (Internal, +x, -x) triangle into the 1D rule, and
run the tuned dynamic test (L 24, D 2, Gamma 0.3, V0 0.03, g = +-0.9, transfer meetings, dt 0.02, t 600, C288's starts).

Predictions frozen before the first run (2026-09-14):
  T1 (code) At zero variables every loop flux is 0 or pi (triangles and on-site loops 0, lane loops pi, squares 0 or pi).
  T2 Wilson, square weight 1: the best minimum has every loop flux within 1e-4 of 0 (time-reversal symmetric; no hand).
  T3 pi-preferring, square weight 1: the best minimum has a lane-loop flux with |sin flux| > 0.1.
  T4 (if stage 2 runs) for at least one sign of g, at least 8 of 10 runs end with |J(600)| > 1e-3.
Reading rule: attempt 3 fixes the standing phase from coherence (under that cost's reading) only if T3 (or T2's
negation) gives a lane-loop flux neither 0 nor pi AND T4 holds. Otherwise attempt 3 has failed, and under the exit rule
ED is written up as an interpretation.
Exit code: T1.

Changes after freezing (2026-09-14):
  1. Run 1 (attempt3_run1.txt): T1 and T2 RIGHT, T3 WRONG, T4 not run. Loop counts per locus: 35 triangles, 105
     on-site 4-loops, 3 lane loops, 48 squares. Wilson (square weights 0.25, 1, 4): every loop flux 0. pi-preferring:
     frustrated (best costs 117.80, 135.99, 208.07 for weights 0.25, 1, 4; 133-148 of 191 loops neither 0 nor pi;
     square fluxes +-2.80 to +-3.11 among 0 and pi; 1D triangle flux +-2.76 to +-2.87), but every lane-loop flux stayed
     at +-pi. No lane-loop flux neither 0 nor pi, so stage 2 did not run and the reading rule gives: attempt 3 fails.
  2. The exit code now checks T1 and that the recorded verdicts reproduce.
"""
import itertools
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("../Commitment_Rule/v4", "../Commitment_Rule/v2b", "../Commitment_Rule/v2", "../Commitment_Rule/v1_budget"):
    sys.path.insert(0, os.path.join(HERE, sub))

NCH = 7  # 0 Internal; lanes 1..6: (+x, -x, +y, -y, +z, -z)
PAIRS = list(itertools.combinations(range(NCH), 2))
PIDX = {p: k for k, p in enumerate(PAIRS)}
NVAR = 6 + len(PAIRS)


def lane_ch(axis, sign):
    return 1 + 2 * axis + (0 if sign > 0 else 1)


def mix(c1, c2):
    v = np.zeros(NVAR)
    if c1 < c2:
        v[6 + PIDX[(c1, c2)]] = 1.0
    else:
        v[6 + PIDX[(c2, c1)]] = -1.0
    return v


def hop(axis, sign, forward):
    """Traverse the hop edge of lane (axis, sign): forward gives phase pi/2 + h, backward -(pi/2 + h)."""
    v = np.zeros(NVAR)
    k = 2 * axis + (0 if sign > 0 else 1)
    s = 1.0 if forward else -1.0
    v[k] = s
    return s * math.pi / 2, v


def families():
    fam = {"triangle": [], "onsite4": [], "lane": [], "square": []}
    for tri in itertools.combinations(range(NCH), 3):
        a, b, c = tri
        fam["triangle"].append((0.0, mix(a, b) + mix(b, c) + mix(c, a)))
    for quad in itertools.combinations(range(NCH), 4):
        a = quad[0]
        for rest in itertools.permutations(quad[1:]):
            if rest[0] < rest[2]:
                cyc = (a,) + rest
                v = sum(mix(cyc[i], cyc[(i + 1) % 4]) for i in range(4))
                fam["onsite4"].append((0.0, v))
    for axis in range(3):
        b1, v1 = hop(axis, +1, True)
        b2, v2 = hop(axis, -1, True)
        fam["lane"].append((b1 + b2, v1 + v2 + mix(lane_ch(axis, 1), lane_ch(axis, -1)) + mix(lane_ch(axis, -1), lane_ch(axis, 1))))
    for a, b in itertools.combinations(range(3), 2):
        sides = [(a, +1), (b, +1), (a, -1), (b, -1)]  # direction of travel along each side
        for choice in itertools.product((0, 1), repeat=4):
            base, vec, chans = 0.0, np.zeros(NVAR), []
            for (axis, move), ch in zip(sides, choice):
                if ch == 0:  # lane moving in the travel direction, traversed forward
                    lane_sign, fwd = move, True
                else:  # the opposite lane, traversed backward
                    lane_sign, fwd = -move, False
                bb, vv = hop(axis, lane_sign, fwd)
                base += bb
                vec = vec + vv
                chans.append(lane_ch(axis, lane_sign))
            for i in range(4):
                vec = vec + mix(chans[i], chans[(i + 1) % 4])
            fam["square"].append((base, vec))
    return fam


def system(fam, weights):
    base, M, w, kind = [], [], [], []
    for name, loops in fam.items():
        for b, v in loops:
            base.append(b)
            M.append(v)
            w.append(weights[name])
            kind.append(name)
    return np.array(base), np.array(M), np.array(w), np.array(kind)


def minimize_cost(base, M, w, sign, rng, starts=20):
    def f(x):
        return float(np.sum(w * (1 - sign * np.cos(base + M @ x))))

    def g(x):
        return M.T @ (w * sign * np.sin(base + M @ x))

    res = []
    for _ in range(starts):
        r = minimize(f, rng.uniform(-np.pi, np.pi, NVAR), jac=g, method="L-BFGS-B",
                     options={"maxiter": 20000, "gtol": 1e-12, "ftol": 1e-15})
        res.append((r.fun, r.x))
    return sorted(res, key=lambda t: t[0])


def wrap(x):
    return np.angle(np.exp(1j * x))


def stage2(theta, F):
    from rule_v4 import kraus, lane_channels, unitary
    from rule_v2b import INTERNAL, RIGHT, RuleB, pure
    from rule_v2 import max_winding, real_rule
    L, D, dt, T = 24, 2, 0.02, 600.0
    H = real_rule(L, theta=theta).astype(complex)
    for u in range(L):
        i, r = 3 * u + INTERNAL, 3 * u + RIGHT
        H[r, i] *= np.exp(1j * F)
        H[i, r] *= np.exp(-1j * F)
    U = unitary(H, dt)
    lane, dest = lane_channels(L, D)
    srng = np.random.default_rng(1357)
    starts = [pure(1 + 0.1 * (srng.standard_normal(3 * L) + 1j * srng.standard_normal(3 * L)) / math.sqrt(2)) for _ in range(10)]
    out = {}
    for g in (0.9, -0.9):
        Js, ws = [], []
        for i in range(10):
            rule = RuleB(L, D, 0.3, g, theta, 0.03, phase_mode="const")
            rule.theta = np.full(L, float(theta))
            rho = starts[i].copy()
            for _ in range(int(round(T / dt))):
                _, d = rule.settings(rho)
                rho = kraus(U @ rho @ U.conj().T, lane, dest, d[lane] * dt)
            Js.append(float(np.sum(rule.currents(rho, rule.theta))))
            ws.append(max_winding(H, d, L, np.random.default_rng(99), nphi=200, npts=10))
        print("stage 2 g %+.1f: J(600) %s; windings %s" % (g, " ".join("%+.3e" % j for j in Js), ws), flush=True)
        out[g] = (Js, ws)
    return out


def main():
    fam = families()
    counts = {k: len(v) for k, v in fam.items()}
    base, M, w, kind = system(fam, {"triangle": 1, "onsite4": 1, "lane": 1, "square": 1})
    fl0 = wrap(base)
    t1 = bool(np.all(np.minimum(np.abs(fl0), np.abs(np.abs(fl0) - np.pi)) < 1e-12)
              and np.all(np.abs(fl0[kind == "lane"]) > 3.14) and np.all(np.abs(fl0[kind == "triangle"]) < 1e-12))
    print("loop counts per locus: %s; T1 zero-variable fluxes 0 or pi (lane loops pi): %s" % (counts, t1), flush=True)

    rng = np.random.default_rng(54)
    best = {}
    for sqw in (1.0, 0.25, 4.0):
        base, M, w, kind = system(fam, {"triangle": 1, "onsite4": 1, "lane": 1, "square": sqw})
        for sign, name in ((1, "Wilson"), (-1, "pi-preferring")):
            res = minimize_cost(base, M, w, sign, rng)
            fun, x = res[0]
            fl = wrap(base + M @ x)
            lane_fl = fl[kind == "lane"]
            tri = fl[kind == "triangle"]
            sq = fl[kind == "square"]
            n_other = int(np.sum(np.abs(np.sin(fl)) > 0.1))
            print("square weight %.2f, %s: best cost %.4f (next %.4f); loops neither 0 nor pi %d of %d; lane-loop fluxes %s; "
                  "square fluxes (distinct, rounded) %s; 1D triangle (I,+x,-x) flux %.3f"
                  % (sqw, name, fun, res[1][0], n_other, len(fl), np.round(lane_fl, 4), sorted(set(np.round(sq, 2)))[:8], tri[0]),
                  flush=True)
            best[(sqw, name)] = (fun, x, fl, kind)

    def lane_off(key):
        fl, kind = best[key][2], best[key][3]
        return bool(np.any(np.abs(np.sin(fl[kind == "lane"])) > 0.1))

    fW, _, flW, kW = best[(1.0, "Wilson")]
    t2 = bool(np.all(np.abs(wrap(flW)) < 1e-4))
    t3 = lane_off((1.0, "pi-preferring"))
    t4 = None
    cand = [k for k in ((1.0, "pi-preferring"), (1.0, "Wilson")) if lane_off(k)]
    if cand:
        fun, x, fl, kind = best[cand[0]]
        theta = float(wrap(x[0] + x[1]) / 2)
        tri_idx = [i for i, (b, v) in enumerate(fam["triangle"])]
        F = float(fl[kind == "triangle"][0])
        print("stage 2 from %s: lane-loop flux %.4f, theta %.4f, triangle flux F %.4f" % (cand[0], float(fl[kind == "lane"][0]), theta, F), flush=True)
        out = stage2(theta, F)
        t4 = any(sum(abs(j) > 1e-3 for j in out[g][0]) >= 8 for g in out)
    print("\nFrozen predictions:")
    rows = [("T1 zero-variable fluxes 0 or pi", t1), ("T2 Wilson: all fluxes 0", t2),
            ("T3 pi-preferring: a lane-loop flux neither 0 nor pi", t3)]
    if t4 is not None:
        rows.append(("T4 stage 2: lasting flow for one sign of g (8 of 10)", t4))
    else:
        print("  (T4 not run: no lane-loop flux neither 0 nor pi)")
    for name, passed in rows:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    success = bool(cand) and bool(t4)
    print("READING RULE: attempt 3 %s" % ("FIXES the standing phase (under this reading)" if success else "FAILS"))
    recorded = t1 and t2 and not t3 and t4 is None
    print("RECORDED RESULTS REPRODUCE" if recorded else "RECORDED RESULTS DO NOT REPRODUCE")
    return recorded


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
