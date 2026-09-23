# The C3a model: growing a surface slice (specification, on paper)

*ED_Attempt_07, note 13. 2026-09-16 (RD22). Ledger: C47–C49. **A specification only: no code, nothing run.** Implementation questions C3a-Q1–C3a-Q4 and the expected results are for Allen to confirm; running is a separate yes.*

## Accepted in note 12 (C47)

**Allen accepted C3-Q1–C3-Q5 and the draft exit rule** (D18: "defaults are fine, spec C3a"). So:
- **Topology:** a slice with more than one dimension never changes its topology. Its only moves are vertex splits and collapses that pass the link condition.
- **Offspring** follow C2a's budget: no child means a collapse, and extra children mean splits.
- **Curvature cost** on a surface is quadratic in (6 − degree). A labelled reading of quadratic energy.
- **Baseline:** the uniform choice runs alongside.
- **The 2D torus is the machinery test;** 3D is the target.

## First, on paper: the budget on a surface (C48)

**In C2a,** an event split its budget over its c + 1 forward links, one of them shared with a neighbour. On a surface there's no single "next" neighbour, so C3a uses the simplest conserved form:
- **An event with c ≥ 1 children** splits its budget equally among them.
- **An event with no children** passes its whole budget to the neighbour it collapses into.

**The balance still holds, by the same arithmetic as C14.**
- **Mean offspring** is μ = 1 + k(b − 1), with b the budget per event over its reference value.
- **Per child,** the budget becomes about b/μ.
- **Near the balance,** b′ ≈ b / (1 + k(b − 1)). Its slope at b = 1 is **1 − k**.
- **So the stability window is 0 < k < 2,** the same as C2a. C3a uses **k = 1**, which sat in the middle of C2a's passing range.

## The model (C49)

### The slice

- **A triangulated torus.**
- **Start:** a flat triangular grid of n × n events, so L\* = n²: **n = 20, 40, 80** gives **L\* = 400, 1,600, 6,400**. Every event has degree 6 and budget 1.

### Each tick

1. **Offspring:** each event v draws c with mean μ_v = max(0, 1 + k(b_v − 1)), geometric as in C2a.
2. **Copy:** slice t+1 starts as a copy of slice t, with each event standing for its first child.
3. **Collapses, in random order:** each event with c = 0 merges into one neighbour a.
   - **Allowed only under the link condition:** v and a share exactly two neighbours (the tips of their two triangles), each of degree ≥ 4.
   - **If no neighbour qualifies,** v keeps one child instead. These **forced keeps** are counted.
   - **Budget:** v's budget passes to a.
4. **Splits, in random order:** each event with c ≥ 2 gets c − 1 splits, applied to its newest child.
   - **A split picks two distinct neighbours u, w.** They cut the neighbour ring into two arcs, one for each child. The two children link to each other and to u and w.
   - **Budget** is shared equally among the children.
5. **Forward links** (for the spacetime reading): each event links to its children, and a collapsed event links to the child that absorbed it.

### Two choice rules

| rule | collapse partner a | split pair u, w |
|---|---|---|
| **U, uniform** (C3-Q4) | Uniform among the allowed neighbours | Uniform among unordered pairs |
| **Q, quadratic curvature cost** (C3-Q3), λ ∈ {0.5, 1, 2} | Weight e^(−λΔE) among the allowed neighbours | Weight e^(−λΔE) among pairs |

**ΔE** is the change in E = Σ (degree − 6)², summed over the events a move touches:
- **a split** touches v's two children, u and w;
- **a collapse** touches v, a, and the two shared neighbours.

**Stopping:** a slice outside [L\*/10, 10·L\*] stops the run, recorded as died or ran away.

### Runs

| | settings | seeds | ticks |
|---|---|---|---|
| **Growth runs** | {U, Q0.5, Q1, Q2} × L\* {400, 1,600, 6,400} = 12 settings | 3 each (0, 1, 2) | **T = 1,000** (may be lowered by the timing trial, recorded before any run) |
| **Calibration F** | The flat grid torus, n = 80 | — | — |
| **Calibration R** | A torus of 6,400 events randomized by uniform edge flips (the standard dynamical-triangulation sampler, fixed topology), 200 sweeps | 1 | — |

### Readings

| reading | what it is | when |
|---|---|---|
| **Slice mass dimension d_H and spectral dimension d_s** | Readings v2 on the slice's link pattern (radii ⌈r_max/2⌉…r_max) | At ticks T/4, T/2, 3T/4, T; the T values are the results |
| **Global dimension D** | Mean graph eccentricity from 20 random events, at the three sizes; D = 1/slope of ln(eccentricity) against ln L\* (flat: about 2; random surfaces: about 4) | At T |
| **Settled** | \|d_H(T) − d_H(3T/4)\| ≤ 0.15 in the median over seeds | — |
| **Degree spread** | Standard deviation of degree; mean of (degree − 6)² | At each checkpoint, reported |
| **Balance** | Mean slice size over ticks T/2…T relative to L\*; forced keeps per tick | Reported; E1 |
| **Spacetime** (reported only) | Readings v2 on slices T − 100…T with forward and in-slice links, L\* = 400 only | At T |

**Structure checks, every tick** (exact):
- V − E + F = 0;
- every edge lies in exactly two triangles;
- every event's neighbours form a single ring;
- no repeated links;
- budget conserved to 10⁻⁹.

**Seeds:**
- growth seed s;
- calibration R seed 7;
- readings centres from seed 3000 + 10·s + size index.

## Expected results, written down before any code

**"Flat at a size"** means the median over seeds has slice d_H and d_s both in **[1.7, 2.3]**, and the size is settled.

| | expected | why, and how sure |
|---|---|---|
| **E0** calibrations | **F:** d_H and d_s in [1.7, 2.3]. **R:** d_H > 2.6 | The readings must tell flat from fractal at these sizes. Random surfaces have d_H = 4; finite size reads lower |
| **E1** structure and balance | Every structure check exact in every run; budget conserved; every run survives; mean size within ±10% of L\* | The moves keep the topology (C43); the balance window holds (C48) |
| **E2** uniform rule U | **Not flat at L\* = 6,400** (d_H > 2.3, or d_s outside [1.7, 2.3], or D > 2.4) | From equilibrium random surfaces (C42). **Low confidence:** growth isn't equilibrium |
| **E3** cost rule Q2 | **Flat at all three sizes, and D in [1.7, 2.4]** | Quadratic cost suppresses curvature; a crossover may lie beyond 6,400. **Low confidence** |
| **E4** settling | Every Q run settled at every size | Local moves at this churn rate (about half of events move each tick) |
| Q0.5, Q1 | Reported; no expected value | To see where flatness sets in |

## Exit rule (note 12's, made exact)

**First:**
- **E1 fails:** a code bug, fixed and rerun (recorded).
- **E0 fails:** the readings can't tell flat from fractal at these sizes; revise the readings or sizes (recorded).
- **The runs that decide the verdict aren't settled:** record "not settled in T ticks"; revise T (recorded).

**Then, in order:**

| outcome | record |
|---|---|
| **U flat at all sizes, with D in [1.7, 2.4]** | "Growth alone keeps a surface flat." |
| **Else, some Q flat at all sizes, with D in [1.7, 2.4]** | **"Quadratic energy keeps a grown surface flat at the sizes run: consistent, not derived; λ a knob."** Then 3D on paper |
| **Else, some Q flat at L\* = 400 but not at the largest size** | "Flat up to a crossover, as in equilibrium; 2D not reached at large scales." Then 3D on paper |
| **Else** | "Growing a flat 2D slice isn't reached with ED's local moves." Take stock |

**E2–E4 not as expected** are recorded as findings. The verdict follows the table.

## Running order

1. **Code** (`model/c3a.py`, runner, timing), with implementation notes written before any run.
2. **Timing trial:** 20 ticks at each size for U and Q2, plus readings on one slice per size. **Timing only.** If T = 1,000 doesn't fit in about 3 hours on 6 workers, lower T and record it before running.
3. **Calibrations**, then the growth runs. Resumable, one result file per run.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3a-Q1** | **Budget on a surface:** shared equally among an event's children, or passed whole to the neighbour a childless event merges into? | **Yes** | Conserved and local; same stability window as C2a (C48) |
| **C3a-Q2** | **Order within a tick:** collapses first, then splits, each in random order; a childless event with no allowed partner keeps one child (counted)? | **Yes** | Simple and symmetric; forced keeps are visible in the record |
| **C3a-Q3** | **Cost weights e^(−λΔE)** over the events a move touches, used for both splits and collapses? | **Yes** | The direct form of C3-Q3; local |
| **C3a-Q4** | **Flat start, with a settling check and two calibrations** (flat grid; flip-randomized surface)? | **Yes** | A flat start could hide fractalization, so the settling check and the fractal calibration guard against that |

## Next step

**If the defaults hold:** write the code and implementation notes, and run the timing trial. **Running needs a separate yes.**

## Revision before any run (D20)

*The timing trial (C50) found that slice readings are undefined at L\* = 400: a 20 × 20 torus allows fewer than three ball radii under the N/10 limit. Allen accepted the proposed fix and said run (D20). Recorded before any run.*

- **Sizes:** n = **40, 80, 160** (L\* = **1,600, 6,400, 25,600**).
- **Calibrations F and R at every size.** E0 applies at every size.
- **Exit rule:** "flat at L\* = 400" reads **"flat at the smallest size (1,600)."**
- **E2** reads "not flat at the largest size (25,600)."
- **Spacetime readings** (reported only) at the smallest size, 1,600, over ticks T − 100…T.
- **Unchanged:** everything else, including the rules, k = 1, T = 1,000, seeds, readings, settling check, the expected-result ranges and the order of the exit rule.
