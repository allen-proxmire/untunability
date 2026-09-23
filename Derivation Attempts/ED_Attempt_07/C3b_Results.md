# C3b results: does each ED meaning catch its bad 3D shape?

*ED_Attempt_07, note 17. 2026-09-17 (RD31). Ledger: C63, C64. Run `model/c3b_run.py`: 45 jobs, 6 workers, 47 s. Expected results and exit rule in note 16 and in the runner's header, fixed before running.*

## Run 1, as pre-registered (C63)

**Pooled over 3 seeds, at N ≈ 1,000 / 8,000 / 27,000:**

| stand-in | largest single-link tick difference | **neck tilt ratio** (sync) | mean degree | **degree ratio** (commitment) | **exponential growth at the largest size** (curvature proxy) | d_H at largest |
|---|---|---|---|---|---|---|
| **F** flat grid | 5.90, 6.81, 7.88 | **1.34** | 6, 6, 6 | **1.00** | **no** (0 of 3) | 2.80 |
| **FR** flat random | 6.40, 7.98, 8.93 | **1.40** | 14.1, 13.9, 14.0 | **0.99** | **no** (0 of 3) | 2.94 |
| **B** branched | 116, 383, 481 | **4.14** | 4.53 | **1.00** | **no** (0 of 3) | 1.73–1.89 |
| **H** hyperbolic | 5.65, 6.38, 7.03 | **1.25** | 6, 6, 6 | **1.00** | **yes** (3 of 3) | 4.60 |
| **Cr** crumpled | 5.93, 6.65, 6.78 | **1.14** | 31.6, 89.4, 164.3 | **5.20** | **yes** (3 of 3) | undefined (too small across) |

**Also reported:**
- **Where the largest tick difference sits in B:** on a neck link in **9 of 9** runs.
- **How the wobble grows with side length:** exponent 0.53 (F) and 0.47 (FR), the same 3D value as C2b's (0.5). H and Cr show no growth.

| | result | |
|---|---|---|
| **E1** construction | Every stand-in connected and built as designed; every solve exact | **As expected** |
| **E2** sync | B 4.14 (≥ 3); F 1.34, FR 1.40, H 1.25, Cr 1.14 (all ≤ 1.5) | **As expected** |
| **E3** commitment | Cr 5.20 (≥ 3); all others 0.99–1.00 (≤ 1.2) | **As expected** |
| **E4** curvature proxy | H flagged; F, FR, B not flagged | **As expected** |
| **Extra flags** (allowed) | The growth flag also catches crumpled | Reported |

**Exit: PASS.**
> **"Each bad 3D shape is flagged by one existing ED meaning, and a flat 3D slice by none: consistent, not derived."**

## What it means (C64)

**In pictures:**
- **Branched slices tear at their necks.** The sync signal found its largest strain on a neck link every time, and the strain grew about 4× as the slices grew. On flat slices the largest strain barely grows (1.3–1.4×, just the largest of many small local differences).
- **Crumpled slices are expensive.** Links per event grew 5× while every other shape stayed flat. That's what commitment's cost acts on.
- **Hyperbolic slices balloon.** Their volume grows exponentially, which the curvature proxy flags. Neither sync nor commitment catches them: the degree is fixed and sync is easy on them. So **quadratic energy is needed.** (The growth flag also catches crumpled, which is allowed.)
- **Flat 3D slices, grid or random, trip nothing.**

**So the paper lead (C56, C57) holds up in a direct check.** Each of ED's three existing meanings catches exactly the bad shape it was matched to, and none of them catches a flat 3D slice.

**Honest limits:**
- **The stand-ins were built to have each shape's defining feature.** This checks that the signals read those features correctly and separately. It doesn't show a growing slice will avoid the bad shapes.
- **The sync signal is the linear precursor of unlocking,** and the curvature signal is a proxy. Only the grid is a true triangulation.
- **No balance between the three pressures was tested,** and their strengths remain knobs.
- **Consistent, not derived. Inputs unchanged (3).**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Spec C3c on paper:** growing a 3D slice (triangulated 3-torus; link-condition merges, splits and flips; budget; commitment, curvature and sync in the move weights), with an honest cost plan | The real test the static check was preparing for; the exit rule says go on to it |
| **(b)** | **Take stock of road C3 and attempt 7** | A natural pause: 2D not reached, 3D lead confirmed statically |
| **(c)** | **Update the attempt 7 write-up** with C3 so far | Keeps the plain-language version current |

**Proposal: (a).** The expected cost of 3D growth is the main unknown, and writing the spec will pin it down before any code.
