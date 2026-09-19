# C3d results: growing a 3D slice with the link balance

*ED_Attempt_07, note 22. 2026-09-18 (RD39). Ledger: C78, C79. Run `model/c3d_run.py`: calibration gate, then 20 growth runs, 5.6 h on 3 workers. Expected results, classification and exit rule fixed in note 21, before any results.*

## The calibration gate passed (C78)

| | flat start | randomized |
|---|---|---|
| **8,000 events** | **flat 3D:** d_H 2.63, d_s 3.06, diameter 15 | crumpled + hyperbolic: diameter 8, 13.6 tetrahedra per event |
| **13,824 events** | **flat 3D:** d_H 2.66, d_s 3.05, diameter 18 | crumpled + hyperbolic: diameter 9, 13.7 tetrahedra per event |

**So the readings repair worked.** C3c's measurement problem is fixed: flat and random now read apart cleanly at both sizes.

## The growth runs

| setting | shape at 13,824 | links per event (flat 6.70) | mean degree (flat 13.4) | largest degree | diameter (flat 18) | events vs start |
|---|---|---|---|---|---|---|
| **S0** no pressure | hyperbolic | 8.36 | 16.7 | **30 (the ceiling)** | 12.5 | **0.73** |
| **S1** commitment | hyperbolic + branched | 4.81 | 9.6 | **30** | 13.0 | 0.95 |
| **S2** curvature | hyperbolic + branched | 5.38 | 10.8 | **30** | 15.0 | 1.00 |
| **S3** sync | hyperbolic | 11.75 | 23.5 | **30** | 11.5 | **0.60** |
| **S4** all three | hyperbolic | 9.71 | 19.4 | **30** | 11.5 | **0.74** |

| | result | |
|---|---|---|
| **E0** calibration gate | Flat reads flat, random doesn't, at both sizes | **As expected** |
| **E1** structure, budgets, ceiling, size | **Structure exact, both budgets exact, nobody over the ceiling, every run survived 200 ticks.** But 12 of 20 runs ended outside ±10% of the starting event count | **Not as expected** (size only) |
| **E2** S0 not flat at the larger size | Hyperbolic | **As expected** |
| **E3** S4 flat at both sizes | Hyperbolic at both | **Not as expected** |
| **E4** all settled | Only one setting settled | **Not as expected** |

**Exit, by the rule as written: "E1 failed: code bug (recorded)."**

**It isn't a code bug.** Checked across all 20 runs: **0 structure failures, 0 budget failures, 0 link-budget failures, 0 ceiling violations, 0 runs stopped by a guard.** The only E1 miss is the event count drifting, in the settings where it drifted down to 0.60–0.75 of the start.

## What actually happened (C79)

**The ceiling did all the work, and it did too much.**
- **Every setting, at both sizes, ended with its largest degree at exactly 30,** the ceiling.
- **Refusals were enormous:** 14,000 to 62,000 moves per tick refused by the ceiling alone.
- **Splits were the ones refused.** Between 28 and 1,900 splits per tick were abandoned because every option was blocked.

**That broke the event balance.**
- **The budget wants to restore the event count:** fewer events means more budget each, which means more children.
- **But children can't be made if every split is refused.** Merges still go through, so the slice **shrinks**: down to 0.60 of the start for sync only, 0.73–0.74 for no pressure and all three.
- **Link density then rises** even though total links are pinned, because the same links are shared among fewer events: 8.4, 9.7, even 11.8 links per event, against the flat 6.70.

**And the shapes read wrong for the same reason.**
- **Diameters collapsed** from 18 to 11–15, so ball readings often can't fit three radii and the dimension comes out undefined again.
- **Everything reads "hyperbolic,"** which at these diameters mostly means "too small across to measure."
- **The two settings that stayed near their starting size,** commitment only and curvature only, are the two that could be measured: d_H 3.87 and 4.32 with d_s 1.59 and 1.61, which reads branched.

**So the link balance did its job, and the ceiling spoiled it.** Density no longer runs away, which was C3c's failure. But a ceiling of 30 sits close enough to the working range that it blocks the moves the event balance needs, and the slice shrinks instead.

## What's honest here

- **Three of ED's four ingredients now behave:** the event budget, the link budget, and the readings.
- **The fourth, "no infinities," is doing harm at this value.** It's a knob, and 30 was chosen as about 2.2× the flat mean without evidence.
- **Nothing in this run measured shape properly** except commitment only and curvature only, and both read branched.
- **No flat 3D slice was grown.** Inputs unchanged (3).

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **A short diagnostic, labelled and not pre-registered:** repeat two settings (no pressure and all three) at one size with T = 100, with the ceiling raised to 60 and then removed, to see whether the event count holds and the diameters recover. About 40 minutes | It isolates the one knob that dominated everything |
| **(b)** | **Take stock of road C and attempt 7** | Two 3D growth attempts, each ending in a recorded wall, with the causes understood |
| **(c)** | **Respec C3e now** with a looser ceiling and a size guard, and rerun in full | Costlier, and without (a) the new ceiling value would be another guess |

**Proposal: (a), then (b) or (c) depending on what it shows.**
