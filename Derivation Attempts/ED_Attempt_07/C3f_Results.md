# C3f results: sync as a condition, judged on the spacetime

*ED_Attempt_07, note 28. 2026-09-19 (RD49). Ledger: C95, C96. Run `model/c3f_run.py`: calibration gate, 16 growth runs, 4.8 h on 3 workers. Expected results, classification and exit rule fixed in note 27 and its D41 threshold revision, before any results.*

## As pre-registered (C95)

**The gate passed,** and the new category worked: the flat slice reads flat 3D at both sizes, while the randomized slice reads **"too small to measure"** (diameters 8 and 9) instead of being mislabelled as it was in C3d and C3e.

| setting | events vs start | links per event (flat 6.70) | slice diameter (flat 15 / 18) | slice shape | **spacetime d_H** (flat 3+1 ≈ 4) |
|---|---|---|---|---|---|
| **A** commitment + curvature | 1.00 | 5.15 | 10.5 / 12.5 | too small to measure | **5.98 / 6.44** |
| **B** the same + sync condition | 1.00 | 5.15 | 10.5 / 12.5 | too small to measure | **5.98 / 6.44** |
| **C** sync alone | 0.94 | 7.15 | 9.0 / 10.5 | too small to measure | **5.52 / 5.80** |
| **D** no pressure | 0.94 | 7.15 | 9.0 / 10.5 | too small to measure | **5.52 / 5.80** |

| | result | |
|---|---|---|
| **E0** gate | Passed at both sizes | **As expected** |
| **E1** structure, budgets, ceiling, flips, **size in A and D** | All exact; **event counts held at 1.00 and 0.94** | **As expected** |
| **E2** B and C hold their counts | They do | **As expected** |
| **E3** B's spacetime in [3.3, 4.7] | **5.98 and 6.44** | **Not as expected** |
| **E4** D's spacetime not in range | 5.52 and 5.80, not in range | **As expected** |
| **E5** every setting measurable | Every slice too small to measure | **Not as expected** |

**Exit, by the rule as written: "Too small to measure at these sizes."**

## Two things this run settled (C96)

**1. The balances hold. That part of the machinery is finished.**
- Event counts stayed at 1.00 (A, B) and 0.94 (C, D) of the start.
- Structure, both budgets, the ceiling and flip neutrality were exact in all 16 runs.
- Merges and splits ran neck and neck, about 4,700 and 8,100 per tick, with almost no forced keeps.
- **Nothing that broke C3c, C3d or C3e broke here.**

**2. Sync as a condition is toothless, and the reason is structural.**
- **A and B are identical, to the last digit.** So are C and D. **The sync condition never fired once**, at either threshold.
- **Why:** the condition refuses a move that would *create* a link carrying too much strain, but every move creates links between events that are already neighbours or share a parent, and those have nearly equal tick counts. The high-strain links are old ones the condition never re-examines.
- **So the reading tested was not really tested.** What was tested is commitment and curvature, twice each.

## What the spacetime says

- **Every setting's grown spacetime reads d_H between 5.5 and 6.4**, where flat 3+1 space should read about 4.
- **Slices are too small across to measure:** diameters 9–12.5 against the flat 15 and 18.
- **Taken together, the pattern is more tightly connected than flat space**, in every setting, with or without pressures.
- **The pressures do change things, just not toward flatness:** commitment and curvature give sparser slices (5.15 links per event against 7.15) that are nonetheless *more* connected in spacetime (6.44 against 5.80).

## Where this leaves road C

**The counts are solved; the geometry is not.** Six 3D runs now, and this one removed the last bookkeeping excuse:

| run | wall |
|---|---|
| C3c | Density ran away |
| C3d | The ceiling blocked growth |
| C3e | Sync's reward collapsed the slice |
| **C3f** | **Everything holds, and the grown pattern is still not flat** |

**The honest reading, in the words the exit rule offered:** with the counts holding and no setting in range, the wall is **"ED's local weights don't select smooth geometry against entropy."** The exit rule's "too small to measure" branch fired first because of the slice readings, but the spacetime readings were defined everywhere and tell the same story.

**Inputs unchanged (3).**

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Record the wall and conclude road C**, then a full attempt 7 write-up and stock-take | Six runs, four passes earlier in the road, and the last three walls all point the same way |
| **(b)** | **Give sync teeth:** re-read the condition so it applies to links that *exist* after a move, not only to links created — then rerun B against A | It tests the reading that was never actually tested. About 5 hours |
| **(c)** | **Larger slices** so the slice readings resolve (say 27,000 and 46,000 events) | Costly, and the spacetime reading already answers the question |

**Proposal: (b), then (a) regardless of its outcome.** One clean test of the untested reading, then close the road honestly.
