# C3f: sync as a condition, judged on the spacetime (specification, on paper)

*ED_Attempt_07, note 27. 2026-09-18 (RD46). Ledger: C91, C92. **A specification only: no code, nothing run.** Implementation questions C3f-Q1–C3f-Q5 and the expected results are for Allen to confirm; running is a separate yes.*

## Accepted (C91)

**Allen accepted C5-Q1–C5-Q4 and note 26's exit rule** (D40):
- **sync in growth is a condition, not a reward;**
- a locality-capped reward would be the contrast;
- **the grown spacetime is what gets judged,** not the slice alone;
- a no-sync control is kept.

## A correction to note 26, before building on it (C92)

**Note 26 said the specced sync "rewards shortcuts."** Checking the move set: **every C3e move is already local.** A split joins events that were within two hops; a 2–3 flip joins the two apexes of neighbouring tetrahedra, also two hops apart; merges only remove. **No move can create a long-range link.**

**So:**
- **the locality cap (reading ii) is already satisfied** and would change nothing. It's dropped as a contrast;
- **what sync actually does is bias which local links exist and which merges happen,** and the observed result was fewer events, more links each, and smaller diameters;
- **the exact route from "reward strain relief" to "slice shrinks" is not established.** C3f therefore **measures** it rather than assuming it: the per-tick balance of merges, splits, forced keeps and refusals is recorded.

**Recorded as a correction to C88's wording.** The evidence that sync collapses the slice stands; the mechanism named there was a guess.

## The model (C92)

**C3e's model** (paired flips, conserved link budget, ceiling 60, guards, calibration gate) **with three changes.**

### 1. Sync becomes a condition

- **The rule:** a move is refused if it would leave any link with a tick difference above **s_max**.
- **s_max = 3 × the flat calibration's largest single-link tick difference at that size** (the same factor the "branched" flag uses).
- **Why relative:** with σ/K at 0.001, the absolute space-like limit (a whole tick across one hop) is nowhere near, so an absolute threshold would never bite. The scaled version is a stand-in for "the pattern keeps a common now," and **the factor 3 is a knob, recorded as such.**
- **Refusals are counted** separately from budget and ceiling refusals.

### 2. The grown spacetime is the main reading

- **The pattern:** events from the last **30 ticks** (smaller size) or **20 ticks** (larger size), with in-slice links and forward links, as C1 and C3a built theirs.
- **The reading:** ball growth only (mass dimension and the growth flag). The walk reading is left off for cost.
- **Flat 3+1 space grown in time should read about 4.**
- **Slice readings are still taken and reported,** but they no longer decide the verdict.

### 3. The labels are fixed

| | C3d/C3e (broken) | **C3f** |
|---|---|---|
| **Crumpled** | Largest degree ≥ 3× the flat calibration's (42), which sits **below the ceiling** (60), so any slice touching the ceiling read crumpled | **Mean degree ≥ 2× the flat mean (26.8), or tetrahedra per event ≥ 2× flat (11.4).** Largest degree is reported, not used |
| **Too small to measure** | Not a category, so unmeasurable runs were labelled hyperbolic | **A category:** if the slice's mass dimension is undefined, or its diameter is below 8, the run is recorded as **"too small to measure"** and given no shape |
| **Branched, hyperbolic, flat** | As before | As before, but only applied when the run is measurable |

### Settings

| | setting | α | λ | sync |
|---|---|---|---|---|
| **A** | Commitment and curvature | 1 | 1 | off |
| **B** | **The candidate:** the same, with sync as a condition | 1 | 1 | condition |
| **C** | Sync alone, as a condition | 0 | 0 | condition |
| **D** | No pressure | 0 | 0 | off |

- **Sizes:** 8,000 and 13,824 events. **T = 150.** **Two seeds.** So **16 growth runs** plus 4 calibrations.
- **Per-tick bookkeeping added:** merges, splits, forced keeps, and refusals split by cause (budget, ceiling, sync), so the mechanism behind any drift is visible.

## Expected results, written down before any code

| | expected | why |
|---|---|---|
| **E0** calibration gate | Flat reads flat 3D at both sizes; randomized doesn't | Passed in C3d and C3e |
| **E1** structure, budgets, ceiling, flips, size | All exact; **event count within ±10% of the start in settings A and D** | A and D held in C3e (0.98–1.00 and 0.94) |
| **E2** sync's cost | **Settings B and C hold their event counts too** (within ±10%), unlike C3e's sync settings | A condition only refuses; it doesn't pay for links |
| **E3** the spacetime | **Setting B's grown spacetime reads a mass dimension in [3.3, 4.7]**, with at least three usable radii | The hypothesis, low confidence |
| **E4** the control | Setting D's spacetime does **not** read in that range | Entropy without pressures |
| **E5** measurability | Every setting is measurable (a defined mass dimension and diameter ≥ 8) at both sizes | The label fix plus the condition should keep slices wide enough |

## Exit rule

**First:**
- **E0 fails:** readings revision (recorded), growth runs not started.
- **E1 fails on structure, a budget, the ceiling or flip neutrality:** a code bug.
- **E1 or E2 fails only on the event count:** recorded as **"the counts still drift under ⟨setting⟩"**, with the per-tick bookkeeping naming the cause.

**Then:**

| outcome | record |
|---|---|
| **B's spacetime in range and D's not** | **"With the link balance, paired cut-and-rejoin and sync as a condition, ED's growth gives a four-dimensional pattern at the sizes run: consistent, not derived; the density, the ceiling, the sync threshold and the strengths are knobs."** Then larger sizes and a knob scan |
| **A's spacetime in range as well** | The same, with sync not needed for it. Recorded plainly |
| **D's spacetime in range** | "Growth alone gives a four-dimensional pattern at these sizes"; the pressures aren't doing the work. Take stock |
| **No setting in range, counts holding** | **"ED's local weights don't select smooth geometry against entropy; the wall is the ensemble, not the meanings."** Take stock of road C |
| **Runs unmeasurable** | "Too small to measure at these sizes," with what that needs recorded. Take stock |

## Cost plan

- **Growth:** 16 runs at C3e's measured pace, so about **4.5–5 h on 3 workers.**
- **Spacetime readings:** roughly 240,000–280,000 events per run, ball growth only. The timing trial measures this; if a reading exceeds about 5 minutes, the number of ticks in the pattern drops to 20 and 15 and that's recorded before any run.
- **Total:** about **6 hours**, with the timing trial confirming first.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3f-Q1** | **Sync's condition as "no link above 3× the flat calibration's largest tick difference"?** | **Yes, a knob** | The absolute limit never bites at this σ/K; the factor matches the branched flag |
| **C3f-Q2** | **Drop the locality-capped contrast,** since every move is already local? | **Yes** | It would test nothing |
| **C3f-Q3** | **Spacetime from the last 30 and 20 ticks, read by ball growth only?** | **Yes** | Cost; the walk reading is slow on patterns this size |
| **C3f-Q4** | **Crumpled by mean degree and tetrahedra per event, with "too small to measure" as its own outcome?** | **Yes** | Fixes the two label faults C3e exposed |
| **C3f-Q5** | **Four settings, two sizes, two seeds, T = 150?** | **Yes** | Cost-bounded; the contrast that matters is B against D |

## Next step

**If the defaults hold:** code it, run the move tests and the timing trial, then the calibration gate. **The growth runs need a separate yes.**

## Threshold set from a diagnostic, before any run (D41)

*The timing trial showed the sync condition never firing at 3× the flat strain. A labelled diagnostic (not pre-registered, `model/c3f_strain_diagnostic.py`) measured what strains the model actually produces at 8,000 events over 40 ticks.*

| | commitment + curvature | no pressure |
|---|---|---|
| **Largest link strain at tick 5** | 1.13× flat | 1.04× flat |
| **at tick 20** | 1.91× | 1.16× |
| **at tick 40** | **2.36×** | 1.11× |
| **Links over 1.5× flat at tick 40** | **120 of 42,718** | 0 |
| **Links over 2× flat at tick 40** | 25 | 0 |
| **Links over 3× flat, ever** | 0 | 0 |

**What it shows:**
- **Strain climbs steadily where the pressures act** and stays flat where they don't, so the condition would bind in the settings it's meant for and leave the baseline alone.
- **3× can't fire** within the run length. **2×** touches a handful of links late. **1.5×** acts on the growing tail from about tick 20 on.

**Revision, recorded before any run:** **s_max = 1.5 × the flat calibration's largest link strain** at that size, replacing 3×. It remains a knob, now set from measurement rather than from a guess.
