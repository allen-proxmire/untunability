# Implementation notes (written before any run)

*ED_Attempt_06, model folder. 2026-09-15 (RD16). These are the choices note 11 (`M1_Model_Spec.md`) didn't fix. They were written **before the timing trial or any calibration ran.** Nothing here changes a rule, range, threshold or expected result in note 11.*

## Environment

- **Software:** Python 3.12.10, numpy 2.4.4, scipy 1.17.1. networkx, POT and numba are not installed.
- **No packages were downloaded.**
- **Hardware:** 8 logical cores (Intel family 6 model 142).

## Readings (`readings.py`)

| choice | what was chosen |
|---|---|
| **Centres and starts** | 200, sampled without replacement with a fixed seed. R1–R4 use the same set |
| **Distances** | Exact hop distances by unweighted shortest paths (scipy) |
| **R1 fit** | Least squares of log V̄(r) on log r, for integer r from 2 to r_max (the largest r with mean V ≤ N/10). Needs r_max ≥ 3; otherwise d_H is undefined and the small-world flag is raised |
| **Small-world flag** | Raised if r_max < 5, **or** if R² of log V̄ against r is higher than R² of log V̄ against log r over the same radii |
| **R2** | A relation crosses the ball of radius r when its ends are at distances r and r + 1 from the centre. β is the least-squares slope of log C̄(r) against log V̄(r) over the R1 radii |
| **R6** | Coefficient of variation of V(r) across centres at r = round((2 + r_max)/2) |
| **R3/R4 walk** | Lazy walk (½ stays, ½ spread evenly over neighbours), iterated exactly by sparse matrix–vector products on all 200 starts at once. p(t) is the mean return probability; ⟨r²⟩(t) is the mean over starts of Σ_y P_t(y) d(start, y)² |
| **Walk window** | Starts at t = 10 and ends at the first t ≥ 10 with p(t) ≤ 10/N. **Cap: t = 20,000.** If the cap is hit, `t_capped` is recorded and the window ends at the cap |
| **Walk fits** | Least squares on 30 log-spaced integer times in the window (duplicates removed). d_s = −2 × slope(log p, log t); d_w = 2 / slope(log ⟨r²⟩, log t) |
| **R5** | \|d_s − 2 d_H / d_w\| |
| **R9 stuck share** | 1 − 2/(mean neighbours) + 1/(2·relations) |

## Calibration patterns (`calibrate.py`)

| pattern | construction |
|---|---|
| **3D periodic random geometric graph** | 16,000 uniform points in the unit cube with periodic boundaries. Reach r from N·(4/3)πr³ = 12. Largest connected component kept (size recorded) |
| **2D periodic random geometric graph** | 16,000 points in the unit square, periodic. Reach from N·πr² = 8. Largest component kept |
| **3D periodic cubic grid** | 25 × 25 × 25, six neighbours |
| **Random 12-regular graph** | 16,000 loci. Stubs are paired at random; self-relations and doubled relations are removed by random double-edge switches with good relations until none remain. networkx isn't available, and this is the standard switching repair |

- **Seeds:** construction seed 1; centre seed 2.
- **Output:** `calibration_run1.txt` (readings and the E0 verdict per pattern) and `calibration_run1.json`.

## The process (`cgp.py`)

| choice | what was chosen |
|---|---|
| **Phases** | Unwrapped (not reduced mod 2π). Birth phase uniform on [0, 2π). Birth rate ω ~ Normal(0, σ) |
| **Effective rate Ω** | Loci aged at least W ticks: (θ_now − θ W ticks ago)/W from a ring buffer. Loci younger than W: (θ_now − θ_birth)/age, with age ≥ 1 (Ω = 0 at age 0) |
| **Out of step** | \|Ω − mean neighbour Ω\| > τ, age ≥ W, room (degree < k_max), and at least one neighbour |
| **Tick order** | clocks → rates → birth (on ticks where t mod B = 0, while loci < N_final) → sync pull → rewire |
| **Birth** | A relation is chosen uniformly. If either end is full, that birth attempt fails (no retry that tick). **Stall guard:** 10,000 consecutive failed birth attempts ends the run as "stalled" (a result, recorded) |
| **Sync pull** | One locus chosen uniformly among out-of-step loci with room. Its target is chosen uniformly among loci at hop distance exactly 2 with room. The e^(−c) draw is made first |
| **Rewire** | A relation chosen uniformly and oriented at random as a–b. The candidate is chosen uniformly among ordered pairs (c, d) with c–d a relation, c within 2 hops of a, d within 2 hops of b, and {c, d} disjoint from {a, b}. A rewire attempt with no candidate still counts as an attempt |
| **Rewire conditions** | a not already linked to c and b not already linked to d; mismatch strictly decreases; curvature floor; connectivity |
| **Connectivity** | After a rewire, the pattern is connected exactly when a can still reach b, c and d. Checked by breadth-first search from a, stopping early when all three are found |
| **Curvature** | Ollivier with laziness ½ on each relation touching a changed locus (birth: z, a, b; pull: x, y; rewire: a, b, c, d). Common mass is cancelled first (exact for W1). Distances between the two supports are 1, 2 (a common neighbour) or 3. **W1 is solved exactly by linear programming (scipy HiGHS).** Checked only when κ_min > −∞ |
| **Curvature screens** | Added before any run, for speed; every decision stays exact. **Reject** at once if 1 − (mass to move) < κ_min: every cost is at least 1, so κ can't be higher. **Accept** that relation if 1 − (cost of a greedy plan, cheapest pairs first) ≥ κ_min: a feasible plan bounds W1 from above. **Only when neither decides** does the exact linear program run. (The curvature timer includes the screens; the exact-LP count is recorded separately.) |
| **Check order** | Cheap conditions first, then curvature, then connectivity. A move is kept only if every condition holds, so the order doesn't change outcomes |
| **Harness smoke test** | Before the timing trial, a tiny run checks the code executes: the process at N_final = 40, the screens bracketing the exact curvature on random relations, and the readings on a 6³ grid. **Its numbers are not results and aren't recorded as readings** |
| **Resting phase** | Starts when loci = N_final. Runs until rewire attempts during rest reach 20 × (relations at the start of rest) |

## Readings v2 (`readings_v2.py`, `calibrate_v2.py`), written before calibration run 2

*Allen D14 ("do a then c"), carrying out the fix proposed in note 12 (C65) after calibration run 1 (C61) and its diagnostic (C62). v1 files and their outputs are kept unchanged.*

**What changed:**
- **Mass dimension, ball-cut, the small-world comparison and R6** use radii r_lo = max(2, ⌈r_max/2⌉) to r_max. At least 3 radii are needed; otherwise the reading is undefined and the flag raised.
- **Walk-return and walk dimension** use times from the first t with √⟨r²⟩ ≥ r_lo to the first t with √⟨r²⟩ ≥ r_max. 30 log-spaced points; at least 5 ticks long, or the reading is undefined. Cap unchanged.

**Unchanged:** everything else, including the E0 ranges.

**Held-out calibrations** (not used in choosing the fix):
- a 3D periodic random geometric graph, mean degree 8, construction seed 11;
- a 2D periodic square grid, 126 × 126.

**Run order:** the first four patterns keep run 1's seeds and order. Centre sampling uses seed 2 in the same order, then the held-out patterns.

**Recorded before the run:** the 3D random pattern's walk dimension may sit at the 2.2 edge.

## M2 (`m2.py`, `m2_timing_trial.py`), written before any M2 run

*Allen D15 ("defaults are fine, run the M2 timing trial"). M2-Q1–M2-Q3 accepted; note 13 confirmed.*

**Code.** `M2` subclasses `CGP` and replaces only `_birth`.

**Birth steps:**
1. Choose a relation a–b uniformly and remove it.
2. Create z, with its rate and phase drawn as in CGP.
3. Add a–z and z–b.
4. Check the curvature floor on every relation touching z, a or b.
5. If the check fails, remove a–z and z–b, discard z and restore a–b. This counts as a failed birth.

**Unchanged from CGP:**
- the stall guard (10,000 consecutive failed births);
- connectivity, which a–z–b preserves, so it isn't checked;
- every other rule and choice.

**Timing trial:**
- **Settings:** central (K/σ = 10, c = 1, k_max = 12), N_final = 1,000, seed 0, readings off.
- **Two runs:** constrained (κ_min = −0.1) and control (no floor), each as its own process, run at the same time.
- **Plan estimates:** reported only for a run that reaches N_final and finishes its resting phase. A stalled run gets none (the lesson from C63). Estimates use the same scaling as CGP's trial: clock and connectivity by (N/1,000)², moves by N/1,000. Each run is timed on its own, rather than taking the control as the constrained run minus curvature.
- **Reading and budget:** choosing a budget and applying the halving rule is Allen's call after the trial.

**Harness smoke test** (not a result): M2 at N_final = 40, with and without the floor, checking that it runs and that births keep the pattern connected.

## M2 runs (`readings_timing.py`, `run_m2.py`, `run_m2_plan.py`, `m2_analyze.py`), written before any M2 process reading

*Allen D16 ("(a), 24 hour budget, run M2"). Everything below was fixed before the first M2 process reading.*

### Budget and sizes
- **Budget:** 24 wall-clock hours on 8 cores (Allen).
- **Readings timing first:** the M2 timing trial left readings out. `readings_timing.py` times one checkpoint's readings on stand-in patterns (a ring; a 3D random pattern with mean degree 9) at 1,000, 4,000 and 16,000 loci. Timing only; the values aren't results.
- **Plan estimate:** process time from C71/C72, plus 5 checkpoints of readings per run.
  - Constrained floors −0.1 and 0 are costed as rings (C73 arithmetic).
  - Floor −0.2 and all controls are costed as dense.
- **Halving rule (note 11):** largest size 16,000 → 8,000 → 4,000 until the estimate is within 24 hours. The chosen size is recorded before launching.

### Jobs
| group | runs |
|---|---|
| **Central constrained** (K/σ 10, c 1, k_max 12, floor −0.1) | sizes {largest, 4,000, 1,000} × seeds 0–4 |
| **Central control** | the same, no floor |
| **Scan constrained** | 108 settings × seeds 0–2 at 4,000 |
| **Scan control** | the 36 distinct (K/σ, c, k_max) settings × seeds 0–2 at 4,000 |

- **Why the control has only 36 settings:** the floor isn't checked when it's absent and draws no random numbers, so a control run is identical for all three floor values. Each of the 108 comparisons uses the matching control.
- **Duplicates skipped:** central 4,000 seeds 0–2 are the same jobs as the scan's.
- **Workers:** 8 processes; math libraries set to one thread each. Longest jobs first.
- **Resume and safety:** saved results are skipped on restart, and results are written atomically.

### Readings per checkpoint
| reading | how |
|---|---|
| **R1–R6, R9 stuck share** | `readings_v2.all_readings`. Centre seed 30,000 + 10·seed + checkpoint |
| **R7 sync** | Largest share of loci whose Ω fit in a window of width 2τ |
| **R8 curvature** | **Departure from note 11, for time:** exact curvature on a random sample of 1,000 relations, or all if fewer, rather than all relations. Sample seed 40,000 + 10·seed + checkpoint. R8 isn't part of the exit criteria |
| **R10 expansion** | 200 random pairs of distinct loci (seed 20,000 + seed). During growth, drawn when loci first reach 25% of N_final, with mean hop distance recorded at 25, 50, 75 and 100%. At rest, a fresh 200 pairs drawn at the start of rest, distance recorded at each checkpoint |

**R9 leakage** (central N_final = 1,000 runs, both kinds):
- **When:** during rest, at the first 200 accepted rewires.
- **What:** for 20 random unit states in the old moving sector {d\*f, S d\*g}, the squared part outside the new moving sector.
- **How:** computed on the union of old and new arcs, so amplitude on cut arcs counts as outside. Solved by sparse least squares (lsqr, tolerance 10⁻¹²). Probe seed 10,000 + seed.
- **The probe draws its own random numbers,** so it doesn't change the process.

### Scoring (for spec gaps; fixed before any reading)
| item | rule |
|---|---|
| **A run is "smooth three at rest"** | Note 11's criteria at all 5 checkpoints, and a spread ≤ 0.2 in each of d_H, d_s, d_w. A stalled run fails |
| **A setting passes** | A majority of its seeds pass: 2 of 3 in the scan, 3 of 5 for the central setting at each size |
| **X1** | Central passes at all three sizes **and** at least 75% of the 108 settings pass |
| **X2** | 25% ≤ fraction < 75% |
| **X3** | Fraction < 25% **and** at least 25% of settings have a majority of seeds meeting the per-checkpoint criteria at one or more checkpoints |
| **X4** | Otherwise |
| **E2** | Mean over all probes, pooled over both kinds, in [10⁻⁴, 10⁻²]. Each kind also reported |
| **E3** | Per setting, majority of control seeds with the condition at all 5 checkpoints; at least half of settings |
| **E4** | Per setting, mean \|d_w − 2\| over seeds and checkpoints (undefined values skipped; none at all counts as infinite) smaller for constrained than control; at least half of settings |
| **E5** | At least half of settings not passing |
| **E6** | Every K/σ = 30 setting, both kinds, with a majority of seeds at R7 ≥ 0.9 at all checkpoints |
| **E7** | Constrained settings with a majority of stalled seeds fewer than half; no control run stalled |
| **E8** | Majority of seeds with distance at 100% greater than at 25%, in at least half of settings, for each kind |

**Scoring code:** `m2_analyze.py`, output `m2_verdict.txt`.

**Completeness guard:** added after the scoring crash check, before any M2 process reading. The script gives no expected-result verdicts and no exit verdict unless every planned job has a saved result. Otherwise it writes only "INCOMPLETE" with the count of missing jobs. (The crash check showed missing runs would otherwise count as "not stalled".)

**Harness smoke test** (not a result): the runner at tiny size before launch.

## Reduced M2 plan (`run_m2_plan_reduced.py`, `m2_analyze_reduced.py`), written before it ran

*Allen D17 ("do b"), after the full plan was stopped for cost (C75: measured 5.3 times the estimate, projecting 50–76 wall-clock hours against a 24-hour budget).*

**This is a scope change made after readings existed.** It is not a rule change: every per-run criterion, the majority-of-seeds rule and the forms of E1–E8 stay exactly as fixed before any M2 reading.

| | kept | dropped |
|---|---|---|
| **Scan** | Floor −0.2 only: 36 settings × 3 seeds at 4,000 | Floors −0.1 and 0 (216 jobs) |
| **Control** | 36 settings × 3 seeds at 4,000 | — |
| **Central** | 1,000 and 4,000, seeds 0–4, constrained and control | Every 16,000-locus job |

**Why these:** the dropped constrained settings are rings by C73's arithmetic and by the three measured runs (C71, C75, mean degree 2.00). The floor −0.2 scan is the one open question: whether a looser floor leaves the ring.

**Consequence for the verdict, stated before running:**
- **Note 13's X1 cannot be reached,** because it needs the central setting at rest at all three sizes. It is reported as unreachable, not as failed.
- The reduced verdicts are labelled **R-X1 to R-X4** and speak only about the floor −0.2 region at 1,000 and 4,000 loci.
- The floors −0.1 and 0 are recorded as rings from existing evidence, not scored.

**Unchanged:** readings v2, the checkpoint readings, the completeness guard, and the resume behaviour (the three saved runs count).

**Cost guard:** if the first floor −0.2 jobs turn out to be rings too (so about 1.3 core-hours each), the plan runs to roughly 23 hours and I report back rather than push past the budget.

## Timing trial (`timing_trial.py`)

- **Setting:** central (K/σ = 10, c = 1, k_max = 12, κ_min = −0.1), N_final = 1,000, seed 0. **Readings off.**
- **Records:** wall time for growth and rest, time in clock updates, curvature linear programs and connectivity searches, and move counts.

**Estimating the full plan's time:**
- **Clock time** is scaled by (N/1,000)², since ticks grow with N and each tick's update grows with the number of relations.
- **Move time** (including curvature) is scaled by N/1,000.
- **Connectivity time** is scaled by (N/1,000)².
- **The control's time** is taken as the constrained time minus its curvature time.
- **The plan:** central setting at 1,000, 4,000 and 16,000 with 5 seeds; the scan at 4,000 with 3 seeds across 108 settings; the control mirroring both. It's summed and divided by 8 cores for a wall-clock figure.

**"Fits" wasn't defined in note 11.**
- The trial reports the estimate, and what the halving rule would give under **24, 72 and 168 hours** on 8 cores.
- **Choosing the budget is Allen's call before any process run.** No process readings are taken until then.
- The scan-at-4,000 cost is reported separately: the halving rule can't reduce it.
