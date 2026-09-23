# Literature gate: simulation of a spontaneous preferred direction

*Done 2026-09-13. Ledger: C18, C20–C25, A6.*

## Verdict: the gate fails. Don't write code for this spec.

1. **The question is already answered** for the rule the spec describes, by known results in probability theory.
2. **The answer depends on a setting ED doesn't fix.** With one reinforcement law no preferred direction forms; with another, a preferred direction forms every time. ED's primitives don't say which law applies (A6). So running the simulation would test the choice of law, not an ED idea (Rule 5: settings are not laws).

---

## What is known

### 1. The spec's rule is a random walk in a Dirichlet random environment

In the spec, a walker at a site picks one of that site's outgoing hops with probability proportional to its strength, and the chosen hop's strength grows by a fixed amount. That is **linear reinforcement on directed edges**.

For one walker, this is known to be equivalent to a walk in a random environment: each site gets its own fixed, random hop probabilities, drawn independently from a Dirichlet distribution, and the walker then moves by those probabilities.

> "the annealed law is that of a reinforced random walk, with linear reinforcement on directed edges"
> — C. Sabot and L. Tournier, "Random walks in Dirichlet environment: an overview", *Annales de la Faculté des sciences de Toulouse* 26 (2017) 463–509, arXiv:1601.08219. Abstract checked 2026-09-13.

The idea goes back to R. Pemantle, "Phase transition in reinforced random walk and RWRE on trees", *Annals of Probability* 16 (1988) 1229–1241 (details checked 2026-09-13).

**Many walkers change nothing about the environment.** The choices made at one site depend only on earlier choices at that same site. So each site's sequence of choices is its own Pólya urn, and the urns at different sites are independent, however many walkers there are and in whatever order they arrive. (This is the same argument as for one walker; the argument is written out by Claude and backed by check C20, not by a published source for many walkers.)

**Consequence.** Each site's hop probabilities settle to independent random values. Nothing links one site's direction to its neighbour's, so **no global preferred direction forms**, and there are no real domains either.

**Check C20** (`01_Ledger/checks/errw_exchangeability.py`, thresholds set before its first run): with 1 lane, 6 sites, 6 walkers and 300 seeds, the correlation between neighbouring sites' forward fractions was +0.021 with walkers and +0.009 for the null model, both consistent with zero. A deliberately coupled control gave +0.350, showing the test does detect correlation when it is there.

### 2. In one dimension, walkers get stuck in valleys

With left and right treated alike, the random environment is balanced on average. For a one-dimensional walk in an i.i.d. random environment, that balance makes the walk recurrent (Solomon, 1975), and it spreads only as far as about (log t)² after time t instead of √t (Sinai, 1982). Walkers pile up in "valleys" of the random landscape.

Source checked: M. El Bouchattaoui, "Random Walk in Random Environment: A short introduction", arXiv:2407.04758, 2026-09-13. The 1975 and 1982 originals were not read.

This applies directly to 1 lane. For 2 or more lanes the chain is a strip, which was not checked.

### 3. A different reinforcement law does pick a direction

D. Erhard, T. Franco and G. Reis, "The directed edge reinforced random walk: the ant mill phenomenon", *Journal of Statistical Physics* (2022), DOI 10.1007/s10955-022-03031-0, arXiv:1911.07295. Read 2026-09-13 (v2, pages 1–4).

- **Their rule:** a walker's weight for a hop is exp(β × net crossings), where net crossings = times crossed forward minus times crossed back. Crossing back cancels a crossing forward.
- **Theorem 2.2:** on any finite connected graph that is not a tree, the walker is eventually trapped in a circuit and follows it forever. A circuit has distinct vertices, so on a ring of 3 or more sites the only circuits are the whole ring, one way or the other. **On a ring, the walker ends up going around in one direction forever.**
- **Proposition 2.1:** on an infinite line, the walker escapes to +∞ or −∞, each with probability 1/2.

So under this law a preferred direction appears spontaneously, chosen at random. The paper covers a single walker only.

---

## What this means

| reinforcement law | records can be cancelled? | growth | preferred direction? | status |
|---|---|---|---|---|
| The spec's rule | No, strengths only grow | Linear | No: independent random sites | Known (C18, C21) |
| Ant mill rule | Yes, crossing back cancels | Exponential | Yes: one direction, chosen at random | Known (C24) |

- **Both outcomes are already known.** Whether chance plus reinforcement picks a direction is decided by the reinforcement law.
- **ED doesn't fix the law.** Nothing in P11 or the other primitives says whether records add linearly, grow exponentially, or can be cancelled (A6).
- **An observation, not a finding.** The law closer to "can't be undone" (the spec's, where strengths only grow) is the one that *doesn't* pick a direction. But it also differs in growth rate (linear against exponential), so the two effects are mixed together, and nothing can be concluded from this comparison.

## About the frozen prediction

Claude predicted outcome (b), domains. The known answer is independent sites with no domain structure. The spec's criteria for (b) (a domain count that grows with L, drift that shrinks with L) would probably have labelled that "domains" anyway, because they don't check how long the domains are. That is a flaw in the criteria, recorded here so it isn't repeated: **an outcome label needs a criterion that separates the cases that actually matter.**

## Not known (checked only briefly)

- Many walkers under the ant mill rule.
- Strips of 2 or more lanes under either rule.
- Laws in between: linear reinforcement with cancellation, or growth faster than linear without cancellation. Studies of "strength of reinforcement" exist, but were not checked.

## What would make a simulation question worth running

It would need an ingredient that:

1. **ED actually fixes**, so the answer isn't a setting chosen by hand; and
2. **reinforced random walks don't already have.**

The obvious candidate is P09: complex phases that can interfere, which no reinforced walk has. Before building anything on that, check the literature on non-Hermitian quantum walks. That area is active, and the answer may be known there too.

## Sources

- Sabot and Tournier, overview of random walks in Dirichlet environment: https://arxiv.org/abs/1601.08219
- Pemantle (1988): https://projecteuclid.org/journals/annals-of-probability/volume-16/issue-3/Phase-Transition-in-Reinforced-Random-Walk-and-RWRE-on-Trees/10.1214/aop/1176991687.full
- Erhard, Franco and Reis, the ant mill: https://arxiv.org/abs/1911.07295
- El Bouchattaoui, introduction to random walk in random environment (Solomon, Sinai): https://arxiv.org/html/2407.04758v1
- Gantert, Michel and Reis, interacting edge-reinforced random walks: https://arxiv.org/abs/2311.08796
