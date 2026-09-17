# C2b results: the wobble of "now"

*ED_Attempt_07, note 10. 2026-09-16 (RD14). Ledger: C32, C33. Run `model/c2b_run.py` (144 runs, 5 workers, 1,954 s); expected results in note 9 and the runner's header, fixed before running.*

## Run 1, as pre-registered (C32)

**Wobble exponent β** (median over 3 seeds; how the wobble of "now" grows with slice size):

| | d = 1 | d = 2 | d = 3 | expected (persistent) |
|---|---|---|---|---|
| **Grids, persistent** | **1.40** | **0.95** | **0.52** | 1.5, 1, 0.5 |
| **Random slices, persistent** | **1.96** ✗ | **1.20** | **0.64** | 1.5, 1, 0.5 |
| Grids, fresh each tick | 0.42 | 0.10 | 0.02 | 0.5, ≈0, ≈0 |
| Random, fresh each tick | 0.66 ✗ (edge 0.65) | 0.12 | 0.05 | 0.5, ≈0, ≈0 |

**Tilt ratio** (tilt at the largest size ÷ the smallest):

| | d = 1 | d = 2 | d = 3 |
|---|---|---|---|
| **Grids, persistent** | 2.49 (grows) | 0.89 (holds) | 0.50 (shrinks) |
| **Random, persistent** | 8.82 (grows) | **1.39** ✗ (range 0.8–1.25) | 0.57 (shrinks) |
| Fresh each tick, grids / random | 0.31 / 0.52 | 0.15 / 0.16 | 0.26 / 0.27 |

| | result | |
|---|---|---|
| **E1** structure and regime | Grids exact; random slices connected, degree in range; every run settled (rate spread ≤ 2 × 10⁻⁵ σ, W change ≤ 0.13%). **But two 1D random-slice runs at n = 512 left the linear regime:** largest neighbour difference 0.81 and 0.88, over the 0.3 limit | **Not as expected** |
| **E2** grids | 1.40, 0.95, 0.52, all in range | **As expected** |
| **E3** random slices | d = 1 at 1.96 is out of range; d = 2 and 3 in range | **Not as expected** |
| **E4** tilt | All as expected except random d = 2 (1.39) | **Not as expected** |
| **E5** control | All as expected except random d = 1 (β 0.66, just over 0.65) | **Not as expected** (not blocking) |
| **Separation** | Exponents separate by ≥ 0.3 in **both** grids and random slices | Yes |

**Exit, by the rule as written: "E1 failed: fix and rerun (recorded)."**

## The frame-jitter reading (reported only, D11)

**The slope of tilt against distance r within a slice,** at the largest size:

| | d = 1 | d = 2 | d = 3 | expected shape |
|---|---|---|---|---|
| **Grids, persistent** | **−0.04** (flat) | **−0.23** (slowly falling) | **−0.58** | flat, slow, about −0.5 |
| **Random, persistent** | +0.19 | −0.14 | **−0.43** | same |
| Grids, fresh | −0.55 | −0.86 | −0.93 | about −0.5, −1, −1 |
| Random, fresh | −0.55 | −0.85 | −0.92 | same |

**Every shape is as expected.** In three dimensions, with persistent rates, the local frame jitter fades with distance at about r^(−0.5) (grids −0.58, random −0.43). In one dimension it doesn't fade at all.

## What caused the misses (C33)

| miss | cause | evidence |
|---|---|---|
| **E1** (and E3 at d = 1) | **The regime, not a code bug.** In 1D random slices some stretches have few links, so tick-count steps pile up there. At n = 512, two runs reached neighbour differences of 0.8–0.9, where the tanh pull flattens out and the linear calculation no longer applies. Those same runs push the 1D random exponent up (W jumps 0.42 → 3.39 across seeds) | Largest differences 0.25, 0.81, 0.88 at n = 512 against ≤ 0.14 everywhere else. My linearity estimate (0.1) was for grids, not random 1D slices |
| **Seed-to-seed scatter in 1D** | **Too few seeds for d = 1.** A 1D slice's wobble is set by its few longest waves, so W varies a lot from seed to seed: at grid n = 64, W is 0.036, 0.069, 0.24 | Per-seed β for 1D grids: 1.30, 2.26, 1.40 |
| **E4, random d = 2** (tilt ratio 1.39) | **Still in the linear regime** (largest difference 0.14), so a smaller σ won't change it. d = 2 is the marginal case, and β_R = 1.20 sits at the edge of its range. Small random slices (256 points) may be less two-dimensional at short range. **Not yet explained** | — |
| **E5, random d = 1** (0.66 vs 0.65) | Just over the edge, with 3 seeds | — |

## What it shows so far (C33)

- **On grids, the floor shows up just as calculated:**
  - the wobble exponents come out 1.40, 0.95, 0.52;
  - "now" tilts more with size in 1D, holds in 2D, and flattens in 3D;
  - with fresh-each-tick rates every dimension keeps a "now," so **the floor comes from persistence**, as C2-Q5 decided.
- **On random slices, the three dimensions separate just as clearly** (1.96, 1.20, 0.64), but two ranges were missed, and one 1D case left the regime the calculation covers.
- **The frame jitter** fades like about r^(−0.5) in 3D and not at all in 1D, the shapes note 8 worked out.
- **But the pre-registered verdict is "fix and rerun."** No pass is recorded.

## Proposed revision and retest (Allen decides)

| | change | why |
|---|---|---|
| **R1** | **σ = 0.0005** (from 0.002) | Neighbour differences scale with σ in the linear regime, so the largest (0.88) becomes about 0.22, under 0.3 |
| **R2** | **10 seeds** (from 3), fresh seeds 3–12 | Tames the 1D seed-to-seed scatter; medians become stable |
| **Unchanged** | Everything else: sizes, readings, ranges, E1–E5, exit rule, tilt reading | Revise and retest, not re-aim |

- **Cost:** about 10/3 of this run, roughly 1.8 hours with 5 workers.
- **Note:** in the linear regime W simply scales with σ, so R1 alone would only change the runs that left the regime. The random 2D tilt miss, if it's real, would stay.

## Next steps

| | step |
|---|---|
| **(a)** | **Rerun with R1 and R2** (revise and retest, recorded) |
| **(b)** | Rerun with R1 only (3 seeds, about 33 min) |
| **(c)** | Take the grid result as it stands and take stock of road C |

**Proposal: (a).** Allen chose (a) (D13).

---

# Run 2: revise and retest (C34–C36)

*2026-09-16 (RD16). Allen chose (a) (D13): σ = 0.0005 and 10 fresh seeds (3–12), everything else unchanged. `model/c2b_run2.py`, 480 runs, 6 workers, 5,377 s. Expected results and exit rule as in note 9, repeated in the script header before running.*

## As pre-registered (C34)

**Median over seeds of the per-seed wobble exponent β:**

| | d = 1 | d = 2 | d = 3 |
|---|---|---|---|
| **Grids, persistent** (E2: 1.35–1.65, 0.85–1.15, 0.35–0.65) | **1.32** ✗ | 1.06 | 0.46 |
| **Random, persistent** (E3: 1.3–1.7, 0.8–1.2, 0.3–0.7) | **1.71** ✗ | 0.85 | 0.57 |
| Grids, fresh | 0.50 | 0.11 | 0.02 |
| Random, fresh | 0.57 | 0.13 | 0.05 |

**Tilt ratio:**

| | d = 1 | d = 2 | d = 3 |
|---|---|---|---|
| **Grids, persistent** | 1.70 | 1.08 | 0.48 |
| **Random, persistent** | 5.19 | **0.73** ✗ (range 0.8–1.25) | 0.54 |

| | result | |
|---|---|---|
| **E1** | **The regime is now clean:** largest neighbour difference 0.164, every run settled. **But one 1D random slice at n = 64 had mean degree 11.25** (range 9–11) | **Not as expected** |
| **E2** | d = 1 at 1.32, just under 1.35 | **Not as expected** |
| **E3** | d = 1 at 1.71, just over 1.7 | **Not as expected** |
| **E4** | Random d = 2 at 0.73 | **Not as expected** |
| **E5** control | All in range | **As expected** |
| **Separation** | Grids: 1D−2D gap 0.27 (< 0.3). Random: 2D−3D gap 0.29 (< 0.3) | Not separated, by the rule |

**Also found:** the random-slice seed formula (1000 + 10·seed + redraw) gave the **same slice** to seeds 3, 4, 5 and to seeds 11, 12 (1D, n = 512), and to seeds 5, 6 and 7, 8 (3D, n = 32). Those slices needed 10 or more redraws to be connected. Their rates were still independent.

**Exit, by the rule as written: "E1 failed: fix and rerun (recorded)."**

## What the misses come from (C35; diagnostic, not pre-registered)

**The exact answer for grids, computed with no simulation** from the grid's wave frequencies (`model/c2b_pooled_diagnostic.py`):

| grids, persistent | exact slope over these sizes | exact tilt ratio |
|---|---|---|
| d = 1 | **1.499** | 2.83 |
| d = 2 | **0.987** | 0.97 |
| d = 3 | **0.471** | 0.48 |

**So the calculation holds at these sizes, and the problem is the statistic.**
- **Seed-to-seed scatter:** the median of per-seed slopes is noisy in 1D, with a spread of 0.29 on grids and 0.48 on random slices. A few of the longest waves set each slice's wobble.
- **The same lesson as C2a and Allen's prime triangles: averaging in the wrong coordinates.** Wobbles add as **squares**, so the right average is the mean of W² over seeds, with the slope taken after that.

**The pooled measure** (slope of √(mean over seeds of W²) against n), on run 2's own runs:

| | d = 1 | d = 2 | d = 3 | gaps |
|---|---|---|---|---|
| **Grids, persistent** | **1.46** | **1.08** | **0.46** | 0.37, 0.63 |
| **Random, persistent** | **1.68** | **0.90** | **0.56** | 0.78, 0.34 |
| Pooled tilt ratio, grids | 2.58 | 1.16 | 0.46 | |
| Pooled tilt ratio, random | 4.34 | 0.81 | 0.54 | |
| Grids, fresh | 0.48 | 0.11 | 0.02 | |
| Random, fresh | 0.57 | 0.12 | 0.04 | |

**With the pooled measure, every exponent and tilt ratio falls inside the ranges fixed in note 9, and the dimensions separate on both grids and random slices.**
- **Grids** match the exact answer to within about 0.1.
- **Close to an edge:** random d = 2 tilt ratio 0.81 (edge 0.8) and the random 2D–3D gap 0.34 (edge 0.3).

**The two harness misses:**
- **Mean degree 11.25 at N = 64:** a small slice's mean degree scatters by about ±0.55, so 9–11 is too tight at the smallest 1D size. A range problem, not a regime problem.
- **Shared slices:** the seed formula overlaps whenever a slice needs 10 or more redraws. That happens often for 1D at n = 512, where only about 3% of draws are connected.

**The frame-jitter reading** came out as before and as expected. In 3D with persistent rates the within-slice tilt slope is −0.57 on grids and −0.46 on random slices; in 1D it is flat.

## What it means (C36)

- **With the wobble averaged as squares, the floor shows up in ED's causal pattern:**
  - wobble grows like about n^1.5, n^1 and n^0.5;
  - "now" tilts more with size in 1D, holds in 2D and flattens in 3D;
  - this holds on grids (matching the exact answer) and on random slices;
  - with fresh-each-tick rates, every dimension keeps a "now."
- **No pass is recorded.** The pre-registered verdict is "fix and rerun," and the pooled measure was chosen after seeing run 2.
- **Inputs:** unchanged (still 3).

## Options (Allen decides)

| | option |
|---|---|
| **(a)** | **Revise and retest on fresh seeds 13–22:** (i) E2–E4 read with the pooled measure; (ii) E1's degree range becomes 10 ± 3·√(20/N) (±1.7 at N = 64, ±0.2 at the largest sizes); (iii) random-slice seed 1000·(seed + 1) + redraw, so slices never overlap. Everything else unchanged. About 1.5 hours |
| **(b)** | Adopt the pooled measure on run 2 as a recorded revision without a retest. The degree and shared-slice issues stay |
| **(c)** | Take the grid result and take stock of road C |

**Proposal: (a).** It's the path C2a took: the telescoped check was adopted, then retested cleanly on fresh seeds.

**Allen chose (a)** (D14).

---

# Run 3: retest with the fixes (C38, C39)

*2026-09-16 (RD18). `model/c2b_run3.py`, 480 runs on fresh seeds 13–22, σ = 0.0005, 6 workers, 5,493 s. Readings E2–E4 pooled (mean of W² over seeds), E1 degree range 10 ± 3·√(20/N), non-overlapping random-slice seeds. Everything else as in note 9. Expected results and the exit rule were in the script header before running.*

## Results

**Wobble exponent β (pooled):**

| | d = 1 | d = 2 | d = 3 | range (d = 1, 2, 3) |
|---|---|---|---|---|
| **Grids, persistent** | **1.54** | **1.02** | **0.42** | 1.35–1.65, 0.85–1.15, 0.35–0.65 |
| **Random slices, persistent** | **1.68** | **0.96** | **0.54** | 1.3–1.7, 0.8–1.2, 0.3–0.7 |
| Exact answer (grids) | 1.50 | 0.99 | 0.47 | — |
| Grids, fresh each tick (median) | 0.51 | 0.11 | 0.03 | 0.35–0.65, −0.1–0.3, −0.2–0.15 |
| Random, fresh each tick (median) | 0.59 | 0.13 | 0.03 | same |

**Tilt ratio (pooled; tilt at the largest size ÷ the smallest):**

| | d = 1 | d = 2 | d = 3 |
|---|---|---|---|
| **Grids** | 3.19 (grows) | 1.05 (holds) | 0.45 (shrinks) |
| **Random slices** | 3.59 (grows) | 0.91 (holds) | 0.53 (shrinks) |

| | result | |
|---|---|---|
| **E1** | Grids exact; every random slice connected, with degree in range; largest neighbour difference 0.19; every run settled; **no shared slices** | **As expected** |
| **E2** grids | 1.54, 1.02, 0.42 | **As expected** |
| **E3** random slices | 1.68, 0.96, 0.54 | **As expected** |
| **E4** tilt | Grows, holds, shrinks, on both grids and random slices | **As expected** |
| **E5** control | Every dimension keeps a "now" | **As expected** |
| **Separation** | Gaps 0.52, 0.60 (grids); 0.72, 0.41 (random) | Yes |

**Exit: PASS.**
> **"A common now needs slice dimension ≥ 3 without a ratio in ED's causal pattern; with commitment's fewest directions and whole numbers, three: consistent, not derived."**

**Closest to an edge:** random 1D β = 1.68 (edge 1.7). Per-seed medians were reported alongside and agree: 1.55, 1.01, 0.44 (grids) and 1.70, 0.89, 0.55 (random).

**Frame jitter (reported only):** within-slice tilt slopes in 3D are −0.56 (grids) and −0.43 (random), so local frames converge with distance. In 1D the slopes are −0.05 and +0.23: no convergence. The fresh-rate controls read −0.55, −0.87, −0.93 (grids). All shapes are as expected, for the third run in a row.

## What it means (C39)

- **Inside ED's causal pattern, with clock rates that persist and a bounded pull, a synced "now" holds at large scales without a tuned ratio only when space has three or more dimensions:**
  - in 1D, "now" tilts further the bigger the region;
  - in 2D it holds a fixed tilt, set by a ratio;
  - in 3D it flattens.
- **It holds on grids and on random slices.** The grids match the exact answer.
- **With rates drawn fresh each tick, every dimension keeps a "now."** So the floor comes from persistence, which Allen decided (C2-Q5).
- **Commitment favours the fewest directions,** so three.
- **The frame jitter fades with distance only in 3D.** A single large-scale rest frame comes out of sync (C28).
- **Status:** consistent, not derived.
  - **Slices were given,** not grown (C2-Q7).
  - **Whole-number dimension is still assumed** (G-Q10).
  - **Only strong coupling was tested.**
- **Inputs:** unchanged (3).
- **Working label** (D15): **Synced Now.**

**How it got here:** three runs, recorded in full. Run 1 missed on the regime. Run 2 missed on a noisy average. Run 3 passed on fresh seeds after both were fixed.
