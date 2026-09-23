# C3a results: growing a surface slice

*ED_Attempt_07, note 14. 2026-09-17 (RD25). Ledger: C51, C52. Run `model/c3a_run.py`: 42 jobs, 6 workers, 10,289 s. Expected results and exit rule in note 13 (with its revision before any run) and in the runner's header, fixed before running.*

## Run 1, as pre-registered (C51)

**Slice mass dimension d_H at T = 1,000** (median of 3 seeds; flat is about 2, random surfaces read higher and rise with size):

| | L\* = 1,600 | 6,400 | 25,600 | global D (from width) |
|---|---|---|---|---|
| **F, flat grid** (calibration) | 1.78 | 1.90 | 1.95 | 2 (eccentricity 26, 53, 106) |
| **R, randomized surface** (calibration) | **2.38** ✗ | 2.69 | 3.13 | about 3.7 |
| **U, uniform growth** | 2.54 | 2.98 | 3.20 | 3.39 |
| **Q0.5** | **2.19** | 2.47 | 2.76 | 3.52 |
| **Q1** | **2.23** | 2.48 | 2.70 | 2.58 |
| **Q2** | **2.15** | 2.48 | 2.66 | 3.33 |

**Spectral dimension d_s** stayed between 1.75 and 2.0 in every setting, as expected for surfaces. So it doesn't separate flat from random here.

**Local curvature:**

| | mean (degree − 6)² | largest degree |
|---|---|---|
| **U** | 12.4–13.1 | 47–79 |
| **Q** | 1.8–2.2 | 11–13 |

| | result | |
|---|---|---|
| **E0** calibrations | Flat reads 1.78–1.95 at every size. The randomized surface reads 2.69 and 3.13 at the two larger sizes, but **only 2.38 at 1,600** (needed > 2.6) | **Not as expected** |
| **E1** structure, budget, survival, size | All exact; all 36 runs survived; late size 0.997–1.003 of L\*; no forced keeps | **As expected** |
| **E2** U not flat at 25,600 | d_H 3.20 | **As expected** |
| **E3** Q2 flat at all sizes | Flat at 1,600 (2.15), not at 6,400 (2.48) or 25,600 (2.66) | **Not as expected** |
| **E4** Q settled | Every Q setting settled (changes ≤ 0.06) | **As expected** |

**Exit, by the rule as written: "E0 failed: readings or sizes revision (recorded)."**

**Also recorded:**
- **Run time:** 2.9 hours, not the estimated 1. Readings at 25,600 events take about 100 s each, which the timing trial didn't measure.
- **U at 1,600:** readings were undefined at two checkpoints. Its slices were too small across for three ball radii, so settling there couldn't be read.
- **Spacetime readings** (reported only, at 1,600): d_H 3.2–3.5, d_s 2.6–3.1.

## What the numbers show (C52; diagnostic reading, not pre-registered)

- **At 1,600 events, the readings barely tell flat from random.** The random calibration reads only 2.38 there, just above the flat range. So the Q rules "flat at 1,600" (2.15–2.23) can't be taken as flat.
- **At the two sizes where both calibrations pass (6,400 and 25,600):**
  - **Uniform growth** reads like the randomized surface (2.98, 3.20 against 2.69, 3.13). Growth with no preference makes a random, crumpled surface, as the equilibrium literature suggested.
  - **The curvature cost works locally:** degrees stay between about 5 and 7, and the largest degree is 12 instead of 79.
  - **But it doesn't keep the surface flat at large scales.** Every Q rule reads between flat and random (2.47–2.48 at 6,400 and 2.66–2.76 at 25,600), and roughens as the surface grows. **Stronger cost barely helps** (λ = 2 reads 2.66 against 2.76 for λ = 0.5).
  - **This is the pattern Bowick, Catterall and Thorleifsson found for equilibrium surfaces:** suppressing local curvature doesn't stop large-scale roughness.
- **Read at the sizes where the calibrations pass,** no rule is flat at any size. The exit rule's table then gives **"growing a flat 2D slice isn't reached with ED's local moves."**
  - **Read with 1,600 included** (where calibration failed), it would give "flat up to a crossover."
  - Both readings agree that **2D isn't reached at large scales.**
- **It fits what note 12 worked out on paper** (C44). In 2D, sync is borderline and gives no large-scale flattening push, and a local cost only acts locally. **Something has to act at large scales.** In 3D that's what the sync floor does (C45, C39).

## Options (Allen decides)

| | option |
|---|---|
| **(a)** | **Revise the sizes to where the calibrations pass** (6,400 and 25,600) and apply the exit rule to these runs. Record "growing a flat 2D slice isn't reached with ED's local moves; the quadratic cost flattens locally but not at large scales" (a recorded revision). No rerun: the margins are wide (Q reads 2.47 or more against a limit of 2.3). **Then 3D on paper:** the two-bad-phases lead (C45), with sync as the large-scale ingredient |
| **(b)** | **A larger run** (102,400 events) to test for a crossover. Roughly 10 hours or more |
| **(c)** | **Take stock of road C3** before deciding on 3D |

**Proposal: (a).** The 2D outcome is clear at the sizes that can be read, and it matches the equilibrium literature and note 12's paper expectation. The open question is whether sync can act at large scales in 3D, which is where ED's meanings point.

## Allen's decision: (a) (C53)

**Allen chose (a)** (D21). The sizes are revised to the two where both calibrations pass (6,400 and 25,600), and the exit rule is applied to run 1's runs. This is a recorded revision made after seeing the run. No rerun, since the margins are wide.
- **At 6,400,** no rule is flat (U 2.98; Q 2.47–2.48).
- **At 25,600,** no rule is flat (U 3.20; Q 2.66–2.76).
- **So the verdict** is the last row of the table.

**Recorded:**
> **"Growing a flat 2D slice isn't reached with ED's local moves; the quadratic curvature cost flattens locally but not at large scales."**

**Next:** 3D on paper (note 15).
