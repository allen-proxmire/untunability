"""The mechanism: does RANDOM splitting of a parent's neighbourhood decohere higher dimensions? (C14.)

Established: a clean cubic torus reads exactly 3 at every thickness, and survives having 100% of its relations
re-pointed locally. A clean ring reads exactly 1 at every thickness, but loses its reading at 5% local rewiring.
Yet under ED's growth the ring survives 16 times out of 16 and the cubic torus fails 7 times out of 8. Each shape
fails what the other survives, so the asymmetry is not generic noise, not thickness, and not fragility.

The hypothesis: when a parent has two children, the parent's neighbourhood is split between them AT RANDOM. For a
ring that does not matter - however the loop is split it is still a loop, and there is one way round. For a cubic
torus the three independent directions must stay mutually coherent across every generation, and random splitting
decoheres them a little each time.

The test: grow from a cubic torus and read the directions every generation, in two arms.
    RANDOM     the current rule - each parent relation is inherited by a randomly chosen pair of children
    COHERENT   the same growth, but children are paired BY INDEX - the first child of p to the first child of q -
               so a parent's neighbourhood is passed on consistently rather than split at random
Nothing else differs: same thickness, same rates passing on and diffusing, same sizes, same instrument.

EXPECTATIONS, fixed before this file was run:
  M1  under RANDOM pairing the reading degrades as generations pass - the gap falls and the reading stops being
      definite before the end                                                                       high
  M2  MAIN: under COHERENT pairing the reading stays 3.0 with a healthy gap throughout                about 60%
  M3  reported: the generation at which random pairing loses it, and the gap trajectory in both arms
If M2 holds, the cause is pinned: random splitting of a parent's neighbourhood is what decoheres higher dimensions,
and the statement becomes "ED's passing-on can carry one independent direction indefinitely but not three".
If M2 fails, something else in the growth is responsible, and it gets reported without a guess attached.
"""
import io
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for rel in (("..", "..", "ED_Attempt_12", "model"), ("..", "..", "ED_Attempt_11", "model"),
            ("..", "..", "ED_Attempt_08", "model")):
    sys.path.insert(0, os.path.join(HERE, *rel))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402
import g_grad as G                                          # noqa: E402
import w_web as W                                           # noqa: E402

OUT = os.path.join(HERE, "e_runs")
RHO = 25
SEEDS = (1, 2, 3)
GROW = 4.0


def inherit(adj, omega, rng, rho, sigma_pass, pairing):
    """One generation. `pairing` is 'random' (the current rule) or 'coherent' (children paired by index)."""
    n_old = len(adj)
    kids, m = [], 0
    for _ in range(n_old):
        c = 2 if rng.random() < P.Q else 1
        kids.append(list(range(m, m + c)))
        m += c
    new = [set() for _ in range(m)]

    def link(a, b):
        if a != b and b not in new[a] and len(new[a]) < P.CEIL and len(new[b]) < P.CEIL:
            new[a].add(b)
            new[b].add(a)
            return 1
        return 0

    target = int(round(rho / 2.0 * m))
    count, extras, base = 0, [], []
    for p in range(n_old):
        ks = kids[p]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                base.append((ks[i], ks[j]))
        for qn in adj[p]:
            if qn <= p:
                continue
            kq = kids[qn]
            mm = max(len(ks), len(kq))
            if pairing == "coherent":
                base.append((ks[0], kq[0]))                  # the parent's neighbourhood passed on consistently
            else:
                base.append((ks[int(rng.integers(len(ks)))], kq[int(rng.integers(len(kq)))]))
            for i in range(mm):
                extras.append((ks[i % len(ks)], kq[i % len(kq)]))
    for a, b in base:
        if count >= target:
            break
        count += link(a, b)
    if extras and count < target:
        order = range(len(extras)) if pairing == "coherent" else rng.permutation(len(extras))
        for k in order:
            if count >= target:
                break
            a, b = extras[int(k)]
            count += link(a, b)
    child = np.empty(m)
    for p in range(n_old):
        for a in kids[p]:
            child[a] = omega[p] + rng.normal(0, sigma_pass)
    return new, child


def run(pairing, seed):
    rng = np.random.default_rng(seed)
    A0 = N1.torus3(13, rng)
    adj = P.to_adj(A0)
    omega = rng.normal(0, 1, len(adj))
    omega -= omega.mean()
    sp_pass = G.SIGMA_PASS * float(omega.std())
    trail, gen, t0 = [], 0, time.time()
    A, _ = W.giant(P.to_A(adj))
    d, det = W.directions_robust(A)
    trail.append((0, len(adj), d, det.get("gap_ratio"), det.get("groups")))
    while len(adj) < GROW * A0.shape[0]:
        adj, omega = inherit(adj, omega, rng, RHO, sp_pass, pairing)
        omega = G.diffuse(adj, omega, G.ALPHA)
        omega -= omega.mean()
        gen += 1
        if gen % 3 == 0 or len(adj) >= GROW * A0.shape[0]:
            A, _ = W.giant(P.to_A(adj))
            d, det = W.directions_robust(A)
            trail.append((gen, len(adj), d, det.get("gap_ratio"), det.get("groups")))
    return dict(pairing=pairing, seed=seed, trail=trail, final=trail[-1][2], secs=round(time.time() - t0, 1))


def main():
    os.makedirs(OUT, exist_ok=True)
    res, lines = [], []
    for pairing in ("random", "coherent"):
        for seed in SEEDS:
            r = run(pairing, seed)
            res.append(r)
            lines.append("%-8s seed %d | " % (pairing, seed)
                         + " -> ".join("gen %d (n %d): %s [gap %s]" % (g, n, d, gp) for g, n, d, gp, _ in r["trail"]))
            print(lines[-1], flush=True)
            json.dump(res, open(os.path.join(OUT, "mech.json"), "w"), indent=1, default=str)
    def finals(p):
        return [r["final"] for r in res if r["pairing"] == p]
    m1 = all(f is None for f in finals("random"))
    m2 = all(f == 3.0 for f in finals("coherent"))
    lines.append("")
    lines.append("M1 (random pairing loses the reading) %s   finals %s" % (m1, finals("random")))
    lines.append("M2 (coherent pairing keeps 3.0 throughout) %s   finals %s" % (m2, finals("coherent")))
    if m2 and m1:
        lines.append("** The cause is pinned: RANDOM SPLITTING of a parent's neighbourhood is what decoheres higher "
                     "dimensions. Pass the neighbourhood on consistently and three survives; split it at random and "
                     "it does not. ED's passing-on can carry one independent direction indefinitely, but not three, "
                     "unless it says HOW a neighbourhood is divided between children. **")
    elif not m2:
        lines.append("** Coherent pairing does NOT rescue three dimensions, so random splitting is not the cause. "
                     "Reported without a guess attached. **")
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "m_mech.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
