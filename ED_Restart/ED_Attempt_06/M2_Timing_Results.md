# M2 timing trial: results

*ED_Attempt_06, note 14. 2026-09-15 (RD21). Ledger: C71–C73. **Timing only: no M2 readings were taken.** The budget and what to do next are Allen's call.*

## What was run

**Allen accepted M2-Q1–M2-Q3 and asked for the M2 timing trial** (D15). Two runs at the central setting (K/σ = 10, c = 1, k_max = 12), growing to 1,000 loci, seed 0, readings off:
- **Constrained:** curvature floor −0.1.
- **Control:** no floor.

Code and choices were fixed before running (`model/m2.py`, implementation notes). A smoke test checked that the code runs (not a result).

## Results

| | constrained | control |
|---|---|---|
| **Reached 1,000 loci?** | **Yes, no stall** (997 births, 0 failed) | **Yes, no stall** |
| **Finished the resting phase?** | Yes | Yes |
| **Time** | 25 s | 35 s |
| **Relations at the end** | **1,000** | 4,585 |
| **Mean links per locus** | **2.0** | 9.2 |
| **Sync pulls accepted** | **0 of 29,912** | 3,585 of 9,969 |
| **Rewires accepted** | 3,138 | 19,516 |

**Births inside relations fixed the freeze:** neither run stalled.

**But the constrained pattern is a single ring** (C71). A connected pattern with as many links as loci has exactly one loop. M2 starts from a triangle and only ever puts newborns inside links. So it grew into one ring of 1,000 loci, stretching like a rubber band and never branching. That's a count, not a formal reading.

## Why a ring (C73, a labelled follow-up)

**On a ring of any length:**
- every link has curvature exactly **0**, which passes the floor;
- the first link that closes a triangle (a sync pull) gives the new chord 0.17 and the links inside the triangle 0.42;
- **but the two ring links just outside it drop to −0.17,** below the −0.1 floor, so the pull is rejected.

**Picture:** a stretched loop of string. Pinching any two points together makes a small loop, and that bends the string sharply just outside the pinch, too sharply for the floor. So the string only gets longer.

**Across the scan:**

| curvature floor | the first triangle | so |
|---|---|---|
| **0** | rejected | ring |
| **−0.1** (central) | rejected | ring |
| **−0.2** | **allowed** (−0.17 ≥ −0.2) | **may leave the ring** |

## What it means for the pre-registered test

- **X1 (the best outcome) is out of reach for M2 too.** The central setting is a one-dimensional ring.
- **By this arithmetic, two-thirds of the scan** (floors 0 and −0.1) **stay rings.** The best open outcome is X2 ("three in a region of the knobs"), and only if most floor −0.2 settings pass.
- **Still testable:** whether settings stall (E7), whether distances grow (E8, a ring certainly stretches), and how the control behaves (E3).
- **Method flag:** revising the model again after each failure would mean trying rules until one gives three, which is a fitting risk. **I'm not proposing an M3.**

## Time for the full M2 plan

Both runs reached 1,000 loci and finished, so the estimates are valid this time:

| | core-hours (largest size 16,000) |
|---|---|
| **Constrained** (central + scan) | 13.6 |
| **Control** (central + scan) | 39.3 |
| **Total** | **about 53, roughly 6.6 wall-clock hours on 8 cores** |

**Caveat:** the constrained estimate comes from a ring. Settings with floor −0.2 that leave the ring will be denser and slower, so the real figure is likely higher.

**Budget options:** any budget of 24 hours or more keeps the largest size at 16,000 under the halving rule.

## Options (Allen decides)

| | option | what it gives |
|---|---|---|
| **(a)** | **Choose a budget and run M2 as specified:** central, scan, control, calibrated readings | A recorded verdict under the pre-registered exit rule, including whether the −0.2 floor leaves the ring, and the control and expansion results |
| **(b)** | **Stop M2 now,** recording the ring trap as its finding without runs | Saves the machine time. The −0.2 question and the control stay unmeasured |
| **(c)** | **Take stock** of the model line and of attempt 6 | Two models, two structural findings (freeze, ring), readings calibrated |

**Proposal: (a) with a 24-hour budget.** The plan is estimated near 7 hours, which leaves room for the caveat. It turns M2 into a clean recorded verdict instead of an argument, and it answers the one open question: does a looser curvature floor let the pattern leave the ring?

## Sources

No new sources. Rules and readings follow notes 9, 11, 12 and 13.
