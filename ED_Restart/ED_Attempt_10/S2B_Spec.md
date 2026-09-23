# Stage B: counting whole histories in 3D, on paper

*ED_Attempt_10, note 7. 2026-09-21 (RD7). Ledger: C15, C16, D7. Specification only; nothing built or run. Written plainly; technical detail in the box at the end and in C16.*

## What stage B asks

Stage A showed that **one tick at a time**, flat slices have far more ways to have happened than the small worlds ED grows. **Stage B asks whether that still wins when whole histories are counted**, against the fact that there are vastly more small-world slices than flat ones.

## Why there's reason for hope (C15, my reading)

**Growing forward and counting histories weigh a slice differently:**
- **Growing forward, one step at a time** (what attempts 7–9 did): a slice is favoured roughly in proportion to its number of one-tick options — **once.**
- **Counting whole histories:** a slice is favoured for its options **at every tick it persists.** Your "mostly one child" decision (A9 D11) makes slices persist for many ticks.

So the push stage A measured gets **multiplied by roughly how long a slice lasts.** That's a known feature of counting paths (the maximal entropy random walk, from note 3). It could be why growing forward lost to the small worlds while counting might not.

**It's an argument, not a result.** The small worlds' sheer number still counts against flat. Stage B measures who wins.

## What gets built

**A program that visits whole ED spacetimes, each allowed one equally often:**
- a stack of slices, time looping round (C-Q4);
- every slice with exactly the same number of events (C-Q2) and exactly ED's link count (B-Q1);
- neighbouring slices joined by one tick of ED's changes: at most 10% of events changing (C-Q3), each change at its own place (B-Q2).

**How it moves between histories:** it makes one small change to one slice at a time — two flips together, or a split paired with a merge — and keeps the change only if the ticks on either side still follow ED's rules. **A change can drift forward or back in time this way**, and short-lived back-and-forth changes appear and disappear. Those are the program's moves, not ED's physics (note 2).

A handy fact makes the counts balance: **splitting a link and merging a link that had the same number of tetrahedra around it change neither the event count nor the link count.** So the program can hold both counts exactly.

## Checks, in order, each a gate

| | check | pass |
|---|---|---|
| **G1** | **Rings as slices, tiny sizes:** the program's history counts against an exact count done by hand-free enumeration | Frequencies match the exact count within statistical error |
| **G2** | **Structure every step:** every slice valid, both counts exact, every tick within ED's rules | Exact, always |
| **G3** | **The readings can tell flat from small world at these sizes:** a flat stack against a small-world stack | Clearly separated (below); else sizes go up, recorded |

**A change from note 3, flagged:** note 3 planned to check the ring version against 2D CDT's exact solution. That holds only without the 10% limit. With ED's limit, the ring version is ED's own count, not CDT's. **So the ring check becomes a check of the program against an exact count, not a comparison with CDT** (B-Q3).

## The runs

- **Two sizes:** 12×12×12 slices (1,728 events) and 16×16×16 (4,096 events), 32 ticks round the loop.
- **Two starts at each size:** every slice flat, and every slice a small world (grown as attempt 9's W1).
- **Run until settled:** the readings change by less than 5% over the last third of the run.

## Readings and the pass rule, fixed now

**Readings:**
1. **How distance grows with size:** a slice's average distance at the two sizes, as a growth rate. Flat grows like size^(1/3), about 0.33; ED's small worlds about 0.15.
2. **The spacetime reading** (ball growth across the whole history, as attempt 9 used), against a flat stack at the same size.

**G3's separation requirement:** the flat and small-world calibration stacks must differ by at least 0.1 in growth rate and 1.0 in the spacetime reading.

**Pass — counting whole histories gives extended 3D space:**
- the growth rate is within 0.05 of the flat stack's;
- the spacetime reading is within 0.5 of the flat stack's;
- **both starts end in the same place** (growth rates within 0.05, spacetime readings within 0.3). This is the decisive part: counting would be *choosing* flat, not keeping it.

**Other outcomes, fixed now:**

| outcome | recorded as |
|---|---|
| Both starts end as small worlds | "Counting whole histories with ED's rules gives small worlds" → take stock |
| The starts end in different places | "Not settled, or the program doesn't reach every history" → longer runs, then take stock |
| Both end between flat and small world | Reported as it reads → take stock |

**My expectation:** close to a coin toss. The persistence argument leans toward flat; the small worlds' numbers lean against. If forced, flat, with low confidence.

## Cost, honestly

**Building:** this is the biggest piece of code in the project. It has to be fast (compiled), because a run needs on the order of 100 million small changes. I'd build it in three steps, each checked before the next: the ring version with its exact count; the 3D moves with the structure checks; then the runs. **Expect a day or two of work and runs, over several sessions.**

**Running:** each size and start about 1–3 hours once built. Memory is small at these sizes.

## Questions for you (defaults proposed)

| | question | default | why |
|---|---|---|---|
| **B-Q1** | **Every slice has exactly ED's link count**, as it has exactly its event count | **Yes** | The link budget is conserved; matches C-Q2 |
| **B-Q2** | **Changes in one tick sit at separate places**, so their order doesn't matter | **Yes** | Follows C-Q1 (the order of changes in a tick isn't a new history) |
| **B-Q3** | **The ring stage checks the program against an exact count**, instead of comparing with CDT | **Yes** | With ED's 10% limit, ED's ring rules differ from 2D CDT's |

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Decide B-Q1 to B-Q3 and start building**, gate by gate, reporting at each gate |
| **(b)** | Take stock first |

**Proposal: (a).**

---

### Technical box

- **State:** T = 32 slices (Slice3P, periodic), plus for each tick t the change set τ_t (S_t → S_{t+1}), each change stored with its support (the events it touches) in both slices.
- **Update:** pick a slice S_t and propose a local V- and E-neutral compound c:
  - a paired flip (a 2–3 at one place, a 3–2 at another), or
  - an edge split of valence k at one place plus a link-condition merge of valence k at another. A split adds 1 + k links and such a merge removes 1 + k, so the pair is exactly neutral.
- **What c does to the ticks:**
  - It sets S_t' = c(S_t), τ_{t−1}' = c ∘ τ_{t−1} and τ_t' = τ_t ∘ c⁻¹.
  - Each part of c either cancels a matching inverse change already in that tick, or joins it at a support disjoint from the tick's other changes (B-Q2).
  - The tick's change count must stay ≤ round(0.1 V) (C-Q3), and the ceiling (60) must hold.
- **Target and acceptance:**
  - The target is uniform over valid histories (C-Q1).
  - The Metropolis acceptance is min(1, q_rev / q_fwd), with proposal probabilities from the site counts (as in attempt 8's flip corrections).
  - Detailed balance is checked numerically in G1.
- **Ergodicity:** not proven. Tested indirectly by the start-independence requirement, and exactly for rings in G1.
- **G1:** rings of length ≤ 8, T ≤ 4, ED's ring changes (insert a child, contract a link) at distinct events with the cap. The exact distribution comes from transfer-matrix enumeration. The sampler's frequencies of histories, grouped by class, must match within 3 standard errors.
- **Readings:**
  - Slice mean distance from 200 BFS sources, averaged over slices and over the last third of the run.
  - The growth rate is ln(md₁₆/md₁₂) / ln(4096/1728).
  - The spacetime reading uses A9's ball-growth method (`p3_readings.spacetime_readings`) on the sampled stack. The flat stack is the flat slice copied T times with the identity parent map; the small-world stack is W1 copied likewise.
- **Settling:** readings every 50 sweeps (1 sweep = V·T proposals); settled when the last third's readings change by ≤ 5%.
- **Literature:** the path-counting amplification is the stationary measure ψ² of the maximal entropy random walk against the degree-proportional measure of the simple random walk (Burda, Duda, Luck, Waclaw, PRL 102, 160602, 2009; [arXiv:0810.4113](https://arxiv.org/abs/0810.4113)).
