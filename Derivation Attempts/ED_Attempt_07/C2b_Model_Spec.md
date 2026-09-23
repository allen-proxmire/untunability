# C2b: the model, specified on paper

*ED_Attempt_07, note 9. 2026-09-16 (RD11). Ledger: C26, C27. A specification only: no code, nothing run. **C2b-Q1–C2b-Q3 are for Allen; expected results and the exit rule are fixed here, before any code.***

## Accepted (C26)

**Allen accepted C2-Q5–C2-Q7 and note 8's exit rule** (D10: "defaults are fine, spec C2b and run the C2a retest"). So:
- **C2-Q5:** clock-rate differences persist along a worldline.
- **C2-Q6:** in a time-ordered pattern, sync means a common "now" holds. Tick counts across space never differ by as much as the hop distance at large scales.
- **C2-Q7:** the floor is checked first with slices given as 1-, 2- and 3-dimensional.

## The question C2b answers

**In ED's causal pattern, with slices given, does the wobble of "now" grow like L^1.5, L^1 and L^0.5 for slices of dimension 1, 2 and 3?** Equivalently, does its tilt grow, hold or shrink? And does that hold on **random** slices, not just grids?

## The model (C27)

### The pattern

**Slices:** every slice is the same given d-dimensional slice S, with N events. This is C2a's fixed-size tube with the offspring randomness switched off: each event has one successor, which is the balanced fixed point of reading B. Two kinds of slice:

| | slice | sizes (side n, N = n^d) |
|---|---|---|
| **G (grid)** | d-dimensional periodic grid, 2d neighbours. The calibration | d = 1: n = 64, 128, 256, 512; d = 2: n = 16, 32, 64, 128; d = 3: n = 8, 16, 24, 32 |
| **R (random)** | N points uniform in the d-dimensional unit torus, linked within a radius set for **mean degree 10**. Must be connected; a disconnected draw is redrawn from the next sub-seed, with redraws counted. ED's pattern is random (A5 D10) | Same N as G |

**Causal links:** event x in slice t+1 has past links to x and to each slice neighbour y of x in slice t. There's no global clock: each event's tick count is computed only from its past events.

### Tick counts

**Each place has a rate** ω(x) = 1 + σ·g(x), with g standard normal, drawn once and kept (C2-Q5). **σ = 0.002.**

**The tick count is carried forward:**

> φ(x, t+1) = φ(x, t) + ω(x) + (K / deg x) · Σ over neighbours y of tanh( φ(y, t) − φ(x, t) )

- **K = 0.5.**
- **Each link's pull is bounded** (tanh never exceeds 1, G-Q8), and linear for small differences.
- **Start:** φ = 0 everywhere.
- **In code, ψ = φ − t is stored** (the same differences, better precision).

**Why these numbers:**
- **K < 1** keeps the one-tick update stable.
- **σ/K is small**, so neighbour differences stay well inside tanh's linear range: about 0.1 at the largest 1D grid, by the steady-state random-walk estimate. That's the strong-coupling regime note 8's calculation covers.
- **Weak coupling is not tested.**

**Run length:** T = ⌈3 · ln(1000) · 2d · n² / (4π² K)⌉ ticks. That's three times the time for the slowest grid mode to relax by a factor of 1,000. Random slices with mean degree 10 relax at least about as fast.

### The control (C2-Q5's "no" branch)

**The same runs with a fresh rate every tick:** ω_t(x) = 1 + σ·g_t(x).
- **Wobble** is the time average of W² over the last third of the run, sampled 300 times.
- **Expected:** W² ∝ n^(2−d), so every dimension keeps a "now." This shows persistence is what makes the floor.

### Readings

| reading | definition |
|---|---|
| **Wobble W(n)** | RMS over the slice of φ(x, T) − mean φ(T) (for the control, √ of the time-averaged W²) |
| **Wobble exponent β** | Least-squares slope of ln W against ln n over the four sizes, per seed; **median over 3 seeds** |
| **Tilt** | W(n)/n. **Tilt ratio** = tilt at the largest n ÷ tilt at the smallest n (median over seeds) |
| **Linear regime** | Largest neighbour difference \|φ(y) − φ(x)\| at T |
| **Settled** | Spread (standard deviation over sites) of the rate over the last tenth of the run, [φ(T) − φ(0.9T)]/(0.1T), and the change in W between 2T/3 and T |

**Seeds:**
- rates and fresh noise: seeds 0, 1, 2;
- random slices: seed 1000 + 10·seed + redraw count.

### What C2b doesn't test

- slices growing or branching (they're given; C2-Q7);
- weak coupling;
- whole-number dimension;
- any rule that picks the dimension.

## Expected results, written down before any code

| | expected | why |
|---|---|---|
| **E1** structure and regime | Every random slice connected, with mean degree in [9, 11]; grids exact. Every persistent run: largest neighbour difference < 0.3, rate spread < 0.01·σ, and W changes by < 2% between 2T/3 and T | Checks the harness and that the runs are in the regime the calculation covers |
| **E2** grids, persistent | Median β in **[1.35, 1.65]** (d = 1), **[0.85, 1.15]** (d = 2), **[0.35, 0.65]** (d = 3) | W ∝ n^((4−d)/2) (note 8, C22; Hong–Park–Choi's linear regime) |
| **E3** random slices, persistent | Median β in **[1.3, 1.7]**, **[0.8, 1.2]**, **[0.3, 0.7]** | Same exponents if the random slice has the dimension of its torus; wider for randomness and small sizes |
| **E4** tilt, persistent (G and R) | Tilt ratio **> 1.5** (d = 1), **in [0.8, 1.25]** (d = 2), **< 0.67** (d = 3) | Tilt ∝ n^((2−d)/2): 8^0.5 ≈ 2.8, 1, 4^(−0.5) = 0.5 |
| **E5** control, fresh each tick (G and R) | Median β in [0.35, 0.65] (d = 1), [−0.1, 0.3] (d = 2), [−0.2, 0.15] (d = 3); tilt ratio < 0.67 in every d | W² ∝ n^(2−d): logarithmic at d = 2, bounded at d = 3. Every dimension keeps a "now" |

## Exit rule (note 8's, made exact)

| outcome | record |
|---|---|
| **E1–E4 as expected** | **"A common now needs slice dimension ≥ 3 without a ratio in ED's causal pattern; with commitment's fewest directions and whole numbers, three: consistent, not derived."** Road C then takes stock, or goes on to the growth rule for d-dimensional slices (Allen decides) |
| **E2 met, E3 not** | "The floor is seen on grids but not on ED's random slices." Take stock of road C |
| **E2 not met** | A calibration or regime problem: check linearity and settling, then revise and retest (recorded), as with A6's readings |
| **Exponents don't separate** (β1 − β2 < 0.3 or β2 − β3 < 0.3, in both G and R) | "The floor isn't seen in ED's causal pattern." Take stock of road C |
| **E5 not as expected** | A finding about the control, recorded; **not blocking** |
| **E1 fails** | A code bug, fixed and rerun (recorded) |

## Running order

1. **Code, with implementation notes written before any run.**
2. **Timing trial** on the largest size of each d, for G and R, both noise types: timing only, no readings kept.
3. **Run.** 3 dimensions × 4 sizes × 2 slice kinds × 2 noise types × 3 seeds = **144 runs**. Minutes to about an hour by rough estimate; the timing trial sets it.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C2b-Q1** | **Is each link's pull (K/deg)·tanh(difference):** bounded, and linear for small differences? | **Yes** | Bounded pull (G-Q8), the simplest smooth bounded form; neighbours count equally (A6 D4) |
| **C2b-Q2** | **Run both grids (calibration) and random slices (mean degree 10)?** | **Yes** | Grids check the harness against the known answer; ED's pattern is random |
| **C2b-Q3** | **Include the fresh-each-tick control?** | **Yes** | It shows the floor comes from persistence, the thing C2-Q5 decided |

## Added before code: the frame-jitter reading (D11)

*Allen accepted C2b-Q1–C2b-Q3 and asked for the tilt reading (D11), before any code. It is **reported only, outside the exit rule** (C28).*

**Reading, within one slice:**
- **G(r)** is the RMS of φ(x) − φ(y) over pairs at hop distance r.
- **Tilt(r) = G(r)/r** is the spread of local frame speeds at scale r, in units of one hop per tick.
- **Which pairs:**
  - **grids:** every site paired with its offset of r along each axis, for r = 1, 2, 4, … ≤ n/2;
  - **random slices:** hop distances from 20 source events (rng seed 5000 + seed), at r = 1, 2, 4, … with at least 100 pairs.
- **When:** persistent runs at T; controls averaged (G²) over the same 300 samples.
- **Summary:** slope of ln tilt(r) against ln r, for r ≤ n/4 (grids) or the matching hop range (random), at the largest size.

**Expected shapes (from note 8's calculation; reported, not pass or fail):**

| | persistent rates | fresh each tick |
|---|---|---|
| **d = 1** | G ∝ r√n, so tilt is **flat in r**, set by the whole slice | G ∝ √r, tilt ∝ r^(−0.5) |
| **d = 2** | G ∝ r·√ln(n/r), so tilt **falls slowly** (logarithmically) | G ∝ √ln r, tilt ≈ r^(−1) |
| **d = 3** | G ∝ √r, tilt ∝ **r^(−0.5):** the frame jitter fades with distance | G bounded, tilt ∝ r^(−1) |

## Next step

**Write the code and implementation notes, run the timing trial, then run** (Allen says run).
