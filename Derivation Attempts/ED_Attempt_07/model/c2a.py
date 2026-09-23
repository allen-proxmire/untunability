"""C2a model (note 6): C1's causal structure with offspring set by ED's budget.

reading "B": budget passed forward and conserved; mean offspring 1 + k(b/b_ref - 1).
reading "A": links held use up budget; mean offspring 1 - k(p - 2), p = past links.
"""
import numpy as np


def grow_budget(T, Lstar, k, seed, reading="B", keep_offspring=False):
    rng = np.random.default_rng(seed)
    L = Lstar
    b = np.ones(L)                 # b_ref = B / L* = 1
    p = np.full(L, 2.0)            # balanced past-link count for slice 0 (reading A)
    B = float(L)
    lengths = [L]
    offspring = [] if keep_offspring else None
    budget_ok = True
    status = "survived"
    for t in range(T - 1):
        if reading == "B":
            mu = np.maximum(0.0, 1.0 + k * (b - 1.0))
        else:
            mu = np.maximum(0.0, 1.0 - k * (p - 2.0))
        c = rng.geometric(1.0 / (1.0 + mu)) - 1      # P(c) = q(1-q)^c, mean mu
        Ln = int(c.sum())
        if keep_offspring:
            offspring.append(c)
        if Ln == 0:
            lengths.append(0)
            status = "died"
            break
        if Ln > 10 * Lstar:
            lengths.append(Ln)
            status = "ran away"
            break
        starts = np.concatenate([[0], np.cumsum(c)[:-1]])
        runs = c + 1
        src = np.repeat(np.arange(L), runs)
        j = np.arange(runs.sum()) - np.repeat(np.cumsum(runs) - runs, runs)
        tgt = (starts[src] + j) % Ln
        if reading == "B":
            share = np.repeat(b / runs, runs)
            bn = np.zeros(Ln)
            np.add.at(bn, tgt, share)
            if abs(bn.sum() - B) > 1e-9 * B:
                budget_ok = False
            b = bn
        pn = np.zeros(Ln)
        np.add.at(pn, tgt, 1.0)
        p = pn
        L = Ln
        lengths.append(L)
    return dict(lengths=lengths, offspring=offspring, status=status, budget_ok=budget_ok)


def balance_stats(lengths, T):
    Ls = np.array(lengths, dtype=float)
    lo = T // 2
    if len(Ls) < T:
        return float("nan"), float("nan")
    ratios = Ls[lo + 1:T] / Ls[lo:T - 1]
    return float(ratios.mean()), float(Ls[lo:T].mean())
