# Simulation spec: does a preferred direction appear spontaneously?

*Written 2026-09-13, before any code. Everything in this file is frozen once the first main run starts. Changes after that go in a dated section at the bottom, and the runs are repeated from scratch.*

> **Status 2026-09-13: suspended at the literature gate. No code will be written for this spec as it stands.** The rule's behaviour is already known from probability theory, and whether a preferred direction appears depends on the reinforcement law, which ED does not fix. See [Literature_Gate.md](Literature_Gate.md).

## The question

In a uniform world whose rules are mirror-symmetric and irreversible, and whose only source of difference is chance, does a preferred direction of transport appear? If so, does it pick a side at random, cover the whole world, and last?

## What the theorem guarantees

From the handedness result (https://github.com/allen-proxmire/event-density-streamlined):

- **Mirror-symmetric transport has winding number zero.** So the uniform start has W = 0, and so does anything the rule produces without breaking the symmetry.
- **Reversible transport has winding number zero.** So the reversible control must give W = 0 at all times.

Any nonzero winding in the main run is a symmetry broken by chance.

## Gates before any code

The spec may not move to code until each gate is ticked and logged in `../../01_Ledger/Log.md`.

- [x] **Literature check — done 2026-09-13: FAILED.** See [Literature_Gate.md](Literature_Gate.md). Original item: The rule in Section 1 is an *edge-reinforced random walk* with many walkers and direction-specific reinforcement. That is a studied class of models in probability theory (for example N. Gantert, F. Michel and G. Reis, "Interacting Edge-Reinforced Random Walks", arXiv:2311.08796, 2023). The answer to this spec's question may already be known. Search for directed or multi-walker edge-reinforced random walks on a ring, or ask a probabilist. If the answer is known, record it (ledger C17, C18) and decide whether the run is still worth doing.
- [ ] **Assumptions recorded.** Every modelling choice in Section 1 is in the ledger's assumptions register (S1–S7), including the fact that "strengths never decrease" is an interpretation of P11, not what P11 says.
- [ ] **Predictions frozen.** Section 7 has both predictions, dated.
- [ ] **Checks pass.** `python run_checks.py` in `../../01_Ledger` passes, including the facts this spec relies on (C14–C16).

---

## 1. The model

### State

- **A ring of L sites**, x = 0, 1, …, L−1, with periodic boundaries.
- **N lanes** at each site.
- **Hop strengths on each edge** (x, x+1):
  - F_x[i, j] ≥ 0: the strength of a forward hop from lane i at site x to lane j at site x+1.
  - G_x[i, j] ≥ 0: the strength of a backward hop from lane i at site x+1 to lane j at site x.
- **K walkers**, each at a site and a lane.

Hop strengths are real and non-negative in this version. Phases (P09) are left out. That is a modelling choice, and adding them is a separate later variant.

### Start: maximum uniformity

- On every edge, staying in the same lane has strength 2s₀ and switching lanes has strength s₀, forward and backward alike: F_x = G_x = s₀(I + J), where I is the identity and J the all-ones matrix.
- Walkers are placed at random sites and lanes, uniformly.

The start is uniform along the ring and mirror-symmetric. Strengths are not all equal because an all-equal start (F = G = s₀J) makes det H(k) exactly zero for N ≥ 2, so the winding number would be undefined.

### Rule: one step

1. **Pick a walker** uniformly at random. Say it is at site x in lane i.
2. **List its options.** Forward hops into each lane j, with strengths F_x[i, j]. Backward hops into each lane j, with strengths G_{x−1}[i, j].
3. **Commit.** Choose one option with probability proportional to its strength. This is the only random element.
4. **Move** the walker along the chosen hop.
5. **Record irreversibly.** Add δ to the strength of the chosen hop. Strengths never decrease.

One **sweep** is K steps.

### The mirror

The mirror sends site x to −x (mod L), lane i to N+1−i, and swaps forward with backward. A forward hop F_x[i, j] maps to the backward hop G_{−x−1}[N+1−i, N+1−j]. The rule treats every option only through its strength, and the start is uniform, so the rule and the start are both mirror-symmetric.

---

## 2. Measurements

All taken at the end of each run, and also at the halfway point.

| quantity | definition |
|---|---|
| **Local drift** d_x | (ΣF_x − ΣG_x) / (ΣF_x + ΣG_x), summing over all lane pairs on edge x. Between −1 and 1. |
| **Global drift** D | The mean of d_x over the ring. |
| **Domain count** n_dom | The number of sign changes of d_x around the ring, counting only edges with \|d_x\| ≥ 0.05. |
| **Correlation length** ξ | The smallest r ≥ 1 with C(r) < 1/e, where C(r) = ⟨d_x d_{x+r}⟩ / ⟨d_x²⟩. Set ξ = L/2 if none. |
| **Winding** W | A = mean over x of F_x, and B = mean over x of G_x. f(k) = det(e^{ik}A + e^{−ik}B) at 4000 evenly spaced k in [−π, π). c₀ = the mean of f over k. The reference point is z₀ = c₀ + i·10⁻³·max\|f\|. W = the winding number of f about z₀, computed as in `tools/check_result.py`. |

With these conventions, forward-only transport (B = 0) gives W = +N.

**W is recorded as undefined** if max|f| = 0 or if the curve passes within 10⁻⁶·max|f| of z₀. Undefined values are logged and counted separately, never as 0.

---

## 3. Parameters

| parameter | values |
|---|---|
| lanes N | 1, 2, 3 |
| ring length L | 16, 64, 256 |
| walkers K | K = L |
| initial strength s₀ | 1 |
| reinforcement δ | 0.1, 1.0 |
| run length | 1000 sweeps |
| seeds per setting | 50 |

Run length and seed count may be reduced for compute reasons only before the first main run, and the reduction is recorded here.

---

## 4. Controls

Each has a known correct answer. **If any control fails, the code is wrong. Fix it and rerun everything.**

| | control | change to the rule | pass criterion |
|---|---|---|---|
| **C1** | Reversible | Whenever F_x[i, j] is reinforced, G_x[j, i] is reinforced by the same δ, and vice versa. Then B = Aᵀ at all times. | In every run: D = 0 (to 10⁻¹²) and W = 0. |
| **C2** | No chance | Replace the random step: each sweep, add δ to every hop. | In every run: every d_x = 0 (to 10⁻¹²) and W = 0. |
| **C3** | Lopsided rule | Multiply every forward option's weight by 1.2 when choosing. | D > 0 in at least 95% of seeds for each setting. |
| **C4** | No built-in sign | The main rule, as is. | In each setting, \|mean of D over seeds\| < 3 × its standard error. |

## 5. Null model

**N0: reinforcement with no walkers.** Each step, pick an edge at random, choose forward or backward with probability proportional to the edge totals, and add δ to one hop of the chosen kind (lanes chosen proportionally). Each edge is then an independent Pólya urn, so there is no coupling between edges.

Run N0 at every setting with the same seeds and measurements.

**ED differs from the null** at a setting if the median ξ of the main run is at least 3 times the median ξ of N0.

Differing from the null means the walkers couple the edges. It does not mean the effect is specific to ED: reinforcement by moving walkers is a known generic class (edge-reinforced random walks; see the literature gate above).

---

## 6. Outcomes, decided per setting (N, L, δ)

| outcome | criterion (all parts must hold) |
|---|---|
| **(a) Global direction** | \|D\| ≥ 0.5 in at least 80% of seeds. n_dom = 0 in at least 80% of seeds. The fraction of seeds with D > 0 is between 35% and 65%. The sign of D at the halfway point equals the sign at the end in at least 90% of seeds. |
| **(b) Domains** | Not (a). The median n_dom ≥ 2. The median n_dom increases with L at fixed N and δ. The median \|D\| decreases with L. |
| **(c) Nothing** | The median of max_x \|d_x\| is below 0.1. |
| **Unclassified** | None of the above. Recorded as unclassified. It is not reinterpreted. |

---

## 7. Predictions (written before any code)

### Claude's prediction, 2026-09-13

- **Controls:** C1–C4 all pass.
- **L = 64 and L = 256:** outcome (b), domains, for every N and both δ. The median \|W\| is 0.
- **L = 16:** outcome (a) is possible for δ = 1.0 as a small-size effect. Otherwise (b).
- **Null model:** the main run differs from N0 (ξ at least 3 times larger) at every setting.
- **Confidence:** low. One dimension usually forbids global order for local rules, but irreversible, out-of-equilibrium dynamics can break that expectation.

### Allen's prediction

*(Fill in and date before any code is run.)*

---

## 8. What each outcome would mean

- **(a) Global direction:** chance plus irreversibility is enough to pick a world-wide direction spontaneously, even in one dimension. It would be a second result that builds on the first.
- **(b) Domains:** chance plus irreversibility breaks the symmetry locally but not globally. The next question is what else is needed: longer-range coupling or more dimensions, one change at a time.
- **(c) Nothing:** reinforcement at these settings is too weak to break the symmetry. Try larger δ before concluding anything, and record that as a change.
- **Unclassified:** the criteria missed what happened. Describe it, write new criteria, and rerun from scratch under them.

## 9. What this does not test

- Nothing about nature. It tests whether this rule does what the commitments suggest it should.
- Nothing about phases (P09), which this version leaves out.
- Nothing about particles, forces or the Standard Model.

## 10. Record keeping

- Every run is logged: setting, seed, D, n_dom, ξ, W, at the halfway point and the end.
- Controls run first. No main-run result is looked at until all controls pass.
- Thresholds are never changed after the data has been seen.

---

## Changes after freezing

2026-09-13 (before any code): suspended at the literature gate. The rule is linear reinforcement on directed edges, which is equivalent to a walk in an independent random environment, so no global direction forms; a different, known law (the ant mill rule) does produce one. The outcome is set by the choice of law, which ED does not fix. The outcome criteria were also found to be unable to tell real domains from independent sites. See [Literature_Gate.md](Literature_Gate.md).
