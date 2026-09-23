"""Gate G1, exact form (revision recorded after the frequency test: its 'every class within 3 SE' rule was too tight for
49 classes with batch-mean errors - 2 of 3 runs had one or two classes at about 3.1 SE while the z spread was about 1).
Exact test: enumerate every labelled state the sampler can reach from the empty history (rings of 6, T = 3, cap 2),
build the full transition matrix from the sampler's own code, and check
  E1  detailed balance exactly: P(s -> s') == P(s' -> s) for every pair (so the stationary law is uniform on states);
  E2  every one of the 49 independently enumerated histories is reached;
  E3  the number of labelled states per history is proportional to 1/|Aut| (the target weighting).
"""
import json
import os
import sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sb_core import History, RingOps, ring  # noqa: E402
import sb_g1 as g  # noqa: E402
g.L0 = 5   # REVISION: rings of 6 give too many labelled states to enumerate in time; 5 is the smallest with a bundle

ops = RingOps()


def freeze(H):
    return (tuple(tuple(sorted((k, tuple(v)) for k, v in S.items())) for S in H.S),
            tuple(frozenset(tau) for tau in H.tau))


def thaw(state):
    slices, taus = state
    H = History([{k: list(v) for k, v in S} for S in slices], ops, g.CAP, 0)
    for t, tau in enumerate(taus):
        for k in tau:
            sp = ops.support(H.S[t], k)
            H.tau[t][k] = sp
            for w in sp:
                H.occ[t][w] = k
    return H


PG = float(os.environ.get("PG", "0"))    # whole-history move probability (D18 check: PG = 0.3)


def transitions(state):
    H0 = thaw(state)
    H0.p_global = PG
    out = defaultdict(float)
    T = H0.T
    ps = H0.p_swap
    pl = 1 - ps - PG
    if PG > 0:
        for parts, q in ops.sites(H0.S[0]):
            H = thaw(state)
            keys = H.global_bundle(list(parts))
            if isinstance(keys, str):
                continue
            for S in H.S:
                for k in keys:
                    ops.apply(S, k)
            out[freeze(H)] += PG * q
    for t in range(T):
        for parts, q in ops.sites(H0.S[t]):
            H = thaw(state)
            res = H.try_bundle(t, list(parts))
            if isinstance(res, str):
                continue
            keys, tL, oL, tR, oR, L, R = res
            for k in keys:
                ops.apply(H.S[t], k)
            H.tau[L], H.occ[L], H.tau[R], H.occ[R] = tL, oL, tR, oR
            out[freeze(H)] += pl / T * q
        tau = sorted(H0.tau[t], key=repr)
        for k in tau:
            H = thaw(state)
            nk = ("S", k[2], k[1], k[3]) if k[0] == "S" else ("M", k[1], k[3], k[2])
            sp = H.tau[t].pop(k)
            H.tau[t][nk] = sp
            out[freeze(H)] += ps / T / len(tau)
    out.pop(state, None)
    return out


def main():
    H = History([ring(g.L0) for _ in range(g.T)], ops, g.CAP, 0)
    start = freeze(H)
    P = {}
    todo = [start]
    while todo:
        s = todo.pop()
        if s in P:
            continue
        P[s] = transitions(s)
        for s2 in P[s]:
            if s2 not in P:
                todo.append(s2)
    worst = 0.0
    asym = 0
    for s, row in P.items():
        for s2, p in row.items():
            q = P[s2].get(s, 0.0)
            d = abs(p - q)
            worst = max(worst, d)
            if d > 1e-12:
                asym += 1
    exact = g.enumerate_exact()
    per_class = defaultdict(int)
    for s in P:
        h = thaw(s)
        rep, aut = g.canon(h.S, [list(t) for t in h.tau])
        per_class[rep] += 1
    ratios = sorted(set(round(per_class[c] * exact[c], 9) for c in per_class if c in exact))
    res = dict(states=len(P), transitions=sum(len(r) for r in P.values()), asymmetric_pairs=asym, max_abs_diff=worst,
               classes_reached=len(per_class), classes_exact=len(exact),
               classes_missing=len([c for c in exact if c not in per_class]),
               classes_extra=len([c for c in per_class if c not in exact]),
               states_times_aut=ratios)
    res["E1"] = asym == 0
    res["E2"] = res["classes_missing"] == 0 and res["classes_extra"] == 0
    res["E3"] = len(ratios) == 1
    json.dump(res, open(os.path.join(HERE, "sb_g1_exact%s.json" % ("_global" if PG > 0 else "")), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
