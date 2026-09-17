"""Check C20: in the simulation's rule, the hop fractions at different sites end up
independent, so no preferred direction spreads along the ring.

Setting: N = 1 lane, a ring of L sites, forward strength F[x] (x -> x+1) and backward
strength G[x-1] (x -> x-1) both start at 1, and a chosen hop gains 1. The choices made
at each site then form a Polya urn with Beta(1, 1) limit, independent across sites,
however many walkers there are and in whatever order they visit (exchangeability;
the walk is a random walk in a Dirichlet environment).

Measured: q_x = F[x] / (F[x] + G[x-1]), the forward fraction at site x.
  walkers model:   mean ~ 0.5, variance ~ 1/12, neighbour correlation ~ 0
  null model:      sites drawn at random with no walkers; same expectations
  coupled control: a forward hop at x also reinforces forward at x+1; the neighbour
                   correlation must be clearly positive, which shows the test can see
                   correlation when it is there
Thresholds were set before this script was first run.
"""
import sys
import numpy as np

L, K, STEPS, SEEDS = 6, 6, 3000, 300


def run(rng, model):
    F = np.ones(L)
    G = np.ones(L)  # G[x]: backward hop x+1 -> x
    pos = rng.integers(0, L, size=K)
    for _ in range(STEPS):
        if model == "null":
            x = rng.integers(0, L)
        else:
            w = rng.integers(0, K)
            x = pos[w]
        f, b = F[x], G[(x - 1) % L]
        if rng.random() < f / (f + b):
            F[x] += 1
            if model == "coupled":
                F[(x + 1) % L] += 1
            step = 1
        else:
            G[(x - 1) % L] += 1
            step = -1
        if model != "null":
            pos[w] = (x + step) % L
    return F / (F + np.roll(G, 1))


def stats(model):
    rng = np.random.default_rng(12345)
    q = np.array([run(rng, model) for _ in range(SEEDS)])
    a = q.ravel()
    b = np.roll(q, -1, axis=1).ravel()
    r = np.corrcoef(a, b)[0, 1]
    return a.mean(), a.var(), r


ok = True
for model in ("walkers", "null", "coupled"):
    mean, var, r = stats(model)
    print("%-8s  mean %.3f  variance %.4f  neighbour correlation %+.3f" % (model, mean, var, r))
    if model == "coupled":
        ok &= r > 0.2
    else:
        ok &= abs(mean - 0.5) < 0.03 and 0.06 < var < 0.095 and abs(r) < 0.1

print("C20 holds" if ok else "C20 FAILED")
sys.exit(0 if ok else 1)
