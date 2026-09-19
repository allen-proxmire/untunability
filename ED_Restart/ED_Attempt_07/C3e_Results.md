# C3e results: paired flips

*ED_Attempt_07, note 24. 2026-09-18 (RD43). Ledger: C84, C85. Run `model/c3e_run.py`: calibration gate, 20 growth runs and 2 contrast runs, 6.4 h on 3 workers. Expected results, classification and exit rule fixed in note 23, before any results.*

## As pre-registered (C84)

**The gate passed again** (same calibrations as C3d): flat reads flat 3D at both sizes, randomized reads crumpled and hyperbolic.

**Paired flips did what they were meant to do:**
- **Link-neutral in every tick of every run** (E5 checked).
- **Rewiring did not stop:** 126 to 674 accepted pairs per tick.
- **Splits stopped being starved:** for no pressure, commitment and curvature, abandoned splits fell to 0.2–211 per tick from C3d's hundreds-to-thousands, and **their event counts held:** 0.94, 0.98 and 1.00 of the start.

**But the sync settings still collapse:**

| setting at 13,824 | events vs start | links per event (flat 6.70) | mean degree | diameter (flat 18) | shape read |
|---|---|---|---|---|---|
| **S0** no pressure | 0.94 | 7.15 | 14.3 | 10.5 | crumpled + hyperbolic |
| **S1** commitment | 0.98 | 4.53 | 9.1 | 12.0 | crumpled + hyperbolic + branched |
| **S2** curvature | 1.00 | 5.41 | 10.8 | 13.5 | crumpled + hyperbolic |
| **S3** sync | **0.37** | 20.63 | 41.3 | 8.0 | crumpled + hyperbolic |
| **S4** all three | **0.53** | 14.51 | 29.0 | 8.0 | crumpled + hyperbolic |

**Contrast runs, no ceiling:** no pressure ended at 0.76 of the start with a diameter of 15, the flat value; all three hit the densification guard at 0.32 with 21 links per event.

| | result | |
|---|---|---|
| **E0** gate | Passed at both sizes | **As expected** |
| **E1** structure, budgets, ceiling, flips, size | **0 structure failures, 0 budget failures, 0 ceiling violations, 0 flip-neutrality failures.** 9 of 22 runs outside ±10% of the starting event count, all of them sync settings plus one contrast run | **Not as expected** (size only) |
| **E2** S0 not flat at the larger size | Not flat | **As expected** |
| **E3** S4 flat at both sizes | Not flat | **Not as expected** |
| **E4** all settled | None settled | **Not as expected** |
| **E5** flips still accepted | 126–674 pairs per tick | **As expected** |

**Exit, by the rule as written: "E1 failed: code bug (recorded)."** Again it isn't one: the only miss is the event count, in the sync settings.

## What this run tells us (C85)

**1. The paired-flip fix worked, and it was the right diagnosis.** Three of five settings now hold their event count. In C3d none did.

**2. Sync is what collapses the slice.** It isn't the ceiling, and it isn't rewiring. Wherever sync is switched on, the event count falls to a third or a half and the remaining events crowd together at 20 and 14 links each. That's the same direction the counting on paper predicted (C66): **sync rewards links, so unopposed it pushes toward crowding.** What's new is that commitment and curvature at unit strength **don't hold it back.**

**3. My shape rule has a flaw.** "Crumpled" is defined as the largest degree reaching 3× the flat calibration's, which is 42. The ceiling is 60. **So any slice that touches the ceiling is automatically labelled crumpled**, which is what happened in every setting. The labels in the table above are therefore unreliable, and that's my spec error, not a result.

**4. Nothing could be measured for dimension.** Every run's mass and spectral dimension came out undefined, because diameters fell to 7.5–13.5 against the flat 15 and 18. The one exception points the way: the **no-ceiling contrast for no pressure kept a diameter of 15,** the flat value.

## Where road C3 now stands

**Three 3D attempts, three different walls, each understood:**

| run | wall | cause |
|---|---|---|
| **C3c** | Density ran away | Nothing balanced links |
| **C3d** | Slices shrank | The ceiling blocked splits |
| **C3e** | Sync settings shrink; nothing measurable | Sync's own pull, plus a ceiling-tangled shape rule |

**What's been fixed and stayed fixed:** the link balance, the readings' calibration gate, and rewiring that doesn't steal from growth.

**What's unresolved:** whether ED's three pressures can balance at all at fixed density, and how to measure a slice that keeps shrinking in diameter.

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Take stock of road C and attempt 7** | Three attempts, three understood walls, and a growing list of my own spec errors. A stock-take would set what counts as reached, what's put in, and whether a fourth attempt is worth it |
| **(b)** | **C3f: fix the shape rule** (separate the crumpled test from the ceiling), **and scan sync's strength** (γ below 1), since sync at strength 1 is what collapses the slice | A focused fourth attempt; roughly 7 hours |
| **(c)** | **Paper work first on sync's form** in the move cost: whether rewarding links across strain is the right reading of C3-Q7, or whether sync should act another way | Cheap, and it questions the ingredient that's failing rather than tuning it |

**Proposal: (a), and if a fourth attempt follows, (c) before (b).**
