# The revised growth model, M2: specification (on paper)

*ED_Attempt_06, note 13. 2026-09-15 (RD19). Ledger: C67–C69. **A specification only: no M2 code written, nothing run.** Meaning questions M2-Q1–M2-Q3, the expected results and the exit rule are for Allen to confirm. **Running is a separate yes.***

## Why a revision

**The first model (CGP, note 11) froze at 50 loci in its central setting** (C63, C64):
- sync pulls filled every locus's 12 link slots;
- a newborn needed a link with room at both ends;
- none was left.

**That freeze is recorded as CGP's own finding** (C66). It isn't repaired inside CGP.

**M2 changes one rule, and only one,** so any difference from CGP can be traced to it.

## The one change: a newborn goes *into* a relation

| | CGP (note 11) | **M2** |
|---|---|---|
| **Birth** (every B ticks) | New locus z linked to **both ends** of a random relation a–b (a triangle). Needs room at a and b | **Relation a–b is cut, and z is placed between: a–z–b.** a and b keep their counts, so **no room is needed** |

**Why this one:**
- **It removes the freeze's cause.** A birth never needs a free slot.
- **It stretches distances.** Adding alone can't expand (C17), but putting a new locus inside a relation lengthens every path that used that relation. Births happen everywhere, so the pattern expands everywhere, with no edge.
- **It reads ED's "cut and rejoin in pairs"** (A5 D10): one relation is cut, and its two ends are rejoined through the newborn. That's a reading, labelled (M2-Q1).
- **The newborn starts with two links.** Sync pulls can close triangles around it, which builds the short loops smoothness needs.

**Everything else is exactly as in CGP** (note 11):
- clocks, rates, sync pull, paired rewire;
- neighbour cap, curvature floor, connectivity;
- the no-floor control;
- fixed choices, the four scanned knobs and their 108 settings;
- sizes, seeds, resting phase and checkpoints.

**The curvature floor applies to births too:** every relation touching z, a or b after the birth.

**On paper, the floor may still block some births.** A newborn in a–z–b has only two links. If a and b share few neighbours, the relation a–z is negatively curved, roughly −0.25 + 1/k in the worst case, below −0.1 for any k. So M2 can still stall at some settings, and the expected results include that.

## Readings

**M2 uses readings v2** (Allen D14):
- dimensions are read over radii ⌈r_max/2⌉ to r_max;
- the walk is read over the same scales.

**Only if calibration run 2 meets E0 for all six patterns.** If it doesn't, X0 applies to M2 as it did to CGP.

**Update (C70): calibration run 2 met E0 for all six patterns,** including both held-out ones. Readings v2 are cleared for M2.

R1–R9 are otherwise as in note 11.

**One new reading:**

| | reading | procedure |
|---|---|---|
| **R10** | **Expansion** | At the start of rest, pick 200 random pairs of loci present then. Record their mean hop distance at each resting checkpoint. During growth, record the same for pairs present at 25% of N_final, at 50%, 75% and 100% of N_final |

## Expected results, written down before any M2 code

| | expected | on what grounds |
|---|---|---|
| **E1** | Stuck share equals 1 − 2/(mean neighbours) + 1/(2·relations) at every checkpoint | Algebra (C49) |
| **E2** | Mean leakage per rewire between 10⁻⁴ and 10⁻² at N_final = 1,000 | As note 11 |
| **E3** (control) | In at least half of settings, at rest: small-world flag, or d_H in [2.0, 2.7] with d_w > 2.2 | C36, as note 11 (kept for comparison) |
| **E4** | In at least half of settings: constrained d_w closer to 2 than the matching control | C43, C45 |
| **E5** (the bar) | **Constrained M2 fails "smooth three at rest" in at least half of settings** | A4 C59 |
| **E6** | At K/σ = 30, R7 ≥ 0.9 at rest in both | C28 |
| **E7** (freezes, new) | Constrained M2 stalls in **fewer than half** of settings. The control stalls in **none** | Births need no room. Only the curvature floor can block them, and the control has none |
| **E8** (expansion, new) | During growth, the mean hop distance between pairs present at 25% of N_final **increases** by 100% of N_final in at least half of settings, constrained and control | Births inside relations lengthen paths (C17) |

## Exit rule (fixed before any M2 code; nothing changes after M2's first run)

**"Smooth three at rest"** is defined as in note 11, with readings v2.

| | outcome | recorded as |
|---|---|---|
| **X0** | Calibration run 2 misses E0 | No M2 result counts until the readings pass. M2's rules and ranges stay unchanged |
| **X1** | Smooth three at rest at all three central sizes, **and** in ≥ 75% of settings | "**Model result:** M2 (births inside relations) grows a smooth, direction-free, three-dimensional pattern that stays that way, conditional on M-Q2–M-Q5 and M2-Q1; not a derivation; knobs counted" |
| **X2** | In 25–75% of settings | "Three in a region of the knobs; recorded as tuning" |
| **X3** | At some checkpoints only | "Three at a moment, not at rest" |
| **X4** | Otherwise, **including settings that stall** (a stalled run has no rest) | "Births inside relations, with ED's other rules as read, don't grow a smooth three" |
| **X5, X6** | Control against E3; leakage against E2; sync against E6; freezes against E7; expansion against E8 | Recorded as measured |

**Follow-ups after a run are labelled not pre-registered.**

## Running order (when Allen says run)

1. A timing trial of M2 at N_final = 1,000, central setting, readings off, **and** the no-floor control at the same setting. Timing only.
2. **The budget decision** (Allen's call), then the size-halving rule as in note 11.
3. M2 runs, only after calibration run 2 has met E0.

## Census note

Same as note 11: four scanned knobs and six fixed choices.
- **M2-Q1 is a reading, not a knob.**
- **Even X1 adds a rule with knobs.** It can't shorten ED's input list.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **M2-Q1** | **Is a birth a newborn placed inside a relation** (a–b becomes a–z–b), read as ED's paired cut-and-rejoin? | **Yes, labelled reading** | It removes CGP's freeze, stretches distances everywhere (expansion without an edge), and needs no free slot |
| **M2-Q2** | **Is everything else kept exactly as CGP?** | **Yes** | One change at a time, so the result can be traced |
| **M2-Q3** | **Is CGP's freeze recorded as CGP's finding:** under births onto a relation with room at both ends, sync fills every locus before growth can continue? | **Yes** | It's what the one central run showed. The rules weren't changed to hide it |

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide M2-Q1–M2-Q3** and confirm E1–E8 and the exit rule | Fixes M2 before any code |
| **(b)** | **Then, if you say run:** M2 timing trial (with control), budget, runs | The test |
| **(c)** | **Revise M2** before confirming | If a rule looks wrong |
| **(d)** | **Stop the model line** | Record CGP's freeze and the readings calibration, take stock |

**Proposal: (a),** then decide on (b) once calibration run 2's result is in.

## Sources

No new sources. Rules and readings follow notes 9, 11 and 12.
