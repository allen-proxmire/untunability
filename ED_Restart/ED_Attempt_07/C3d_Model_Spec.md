# C3d: growing a 3D slice with the link balance (specification, on paper)

*ED_Attempt_07, note 21. 2026-09-18 (RD37). Ledger: C75, C76. **A specification only: no code, nothing run.** Implementation questions C3d-Q1–C3d-Q5 and the expected results are for Allen to confirm; running is a separate yes.*

## Accepted (C75)

**Allen accepted C4-Q1–C4-Q5 and note 20's exit rule** (D31). So:
- **holding a link uses up an event's commitment budget** (labelled reading);
- **that budget is conserved,** so the slice's total link count is pinned, not tuned;
- **there's a hard ceiling** on links per event, with its value a knob;
- **the budget is set at the flat value,** recorded plainly as density put in;
- **two budgets:** one for children (C2a's reading B), one for links.

## The model (C76)

**C3c's model** (note 18 and its D29 revision) with four changes.

### 1. The link budget

- **Total:** B_L = round(6.699 × V₀) links, the flat-space value (C66), set from the starting event count.
- **A pool:** free budget = B_L − (current links). A move that would add more links than the pool holds is **not allowed**; a move that removes links returns them.
- **The start already sits at it:** the cube-grid start has E = 7V, slightly above flat's 6.699V, so the first few ticks trade the difference away. That's recorded.
- **Conservation is exact by construction,** and the runner checks it every tick.

### 2. The ceiling (no infinities)

- **No event may hold more than 30 links** (about 2.2× the flat mean of 13.4). A move that would exceed it is not allowed.
- **The value is a knob;** "finite" is the decided meaning (A4 D32).

### 3. Readings repaired

- **Sizes:** V = **8,000** (n = 20) and **13,824** (n = 24). C3c's flat calibration failed at 4,096 and passed at 13,824.
- **Calibrations run first, as a gate.** If the flat calibration doesn't read flat 3D at both sizes, **the run stops there** and the fix is a recorded readings revision, before any growth runs.
- **The walk reading comes back:** the spectral dimension (dropped in C3b and C3c for speed on tree-like graphs) is affordable now that density is pinned, and it does not need wide balls.
- **Also reported:** the slice's diameter and mean distance, so a "too small across" case is visible.

### 4. Settings and sizes

| | setting | α | λ | γ |
|---|---|---|---|---|
| **S0** | No pressure | 0 | 0 | 0 |
| **S1** | Commitment only | 1 | 0 | 0 |
| **S2** | Curvature only | 0 | 1 | 0 |
| **S3** | Sync only | 0 | 0 | 1 |
| **S4** | **All three** | 1 | 1 | 1 |

- **T = 200 ticks** (C3c's heavy runs showed the cost; see the plan below).
- **Seeds 0 and 1**, two sizes, five settings: **20 growth runs** plus 4 calibrations.
- **Guards kept:** died, ran away, densified (tetrahedra per event over 20), each a recorded outcome, plus the new link-budget and ceiling limits, which are refusals rather than stops.

### Readings, at ticks T/2, 3T/4 and T

| reading | what it is |
|---|---|
| **d_H** | Ball growth, as before |
| **d_s** | Spectral dimension from the walk (restored) |
| **Exponential-growth flag** | As before |
| **Diameter and mean distance** | New, reported |
| **Links per event, tetrahedra per event, mean and largest degree** | As before |
| **Valence** | Mean, spread, mean (valence − 5.104)² |
| **Neck strain** | C3b's signal, in units of the flat calibration at the same size |
| **Refusals** | Moves blocked by the link budget and by the ceiling, per tick |
| **Balance** | Event count against the start; forced keeps |

### Shape classification at a size (median of seeds; booleans need both seeds)

| shape | test at T |
|---|---|
| **Crumpled** | Largest degree ≥ 3× the flat calibration's, **or** tetrahedra per event ≥ 2× flat's 5.70 |
| **Hyperbolic** | Exponential-growth flag set |
| **Branched** | Neck strain ≥ 3× the flat calibration's, or d_H < 2.3, or d_s < 2.0 |
| **Flat 3D** | **None of the above,** d_H in [2.5, 3.5] **and** d_s in [2.3, 3.7] |
| **Unclassified** | Anything else |

## Expected results, written down before any code

**Low confidence except E0 and E1**, as in C3c.

| | expected | why |
|---|---|---|
| **E0** calibrations | The flat start reads **flat 3D** at both sizes; the randomized one doesn't | The gate. C3c failed here at 4,096 |
| **E1** structure, budgets, limits | Every structure check exact; both budgets conserved; no event over the ceiling; links exactly at B_L or below with the shortfall only from refusals; event count within ±10% of the start | The moves are exact (C3c E1 passed); the link budget is conserved by construction |
| **E2** S0 | **Not flat 3D** at the larger size | With density pinned it can't densify, so entropy should push it to a rough or branched shape instead |
| **E3** S4 | **Flat 3D at both sizes, settled** | The hypothesis: with density fixed, the three pressures pick the shape |
| **E4** settling | Every setting settled at both sizes | T = 200 with pinned density |
| S1, S2, S3 | Reported | Their own pulls at fixed density |

## Exit rule

**First:**
- **E0 fails:** stop before the growth runs; readings revision (recorded).
- **E1 fails on structure or a budget:** a code bug (recorded).
- **A setting is unsettled at a size it decides:** "not settled in T ticks" (recorded).

**Then:**

| outcome | record |
|---|---|
| **S4 flat 3D at both sizes, and S0 not flat** | **"With the link balance and the ceiling, ED's meanings grow a flat 3D slice at the sizes run: consistent, not derived; the density, the ceiling and the three strengths are knobs."** Then larger sizes and a strength scan |
| **S0 flat 3D at both sizes** | "At pinned density, growth alone keeps a 3D slice flat"; the pressures aren't needed here. Take stock |
| **Density holds but no setting reads flat 3D** | "The link balance fixes density but not shape: ⟨shapes per setting⟩." Take stock of road C |
| **Anything else** | Recorded as it reads, then take stock |

## Cost plan

- **Per tick, from C3c's measurements at pinned-density settings:** about 14 s at 8,000 events and 24 s at 13,824, on 3 workers.
- **Per run at T = 200:** about 47 min and 80 min.
- **Total:** 20 runs plus calibrations, about **7 hours on 3 workers.**
- **Workers:** 3, with saves every 10 ticks, as C3c ended up running.
- **If the timing trial shows more than about 10 hours,** T drops to 150 and that's recorded before any run.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3d-Q1** | **Link budget as a pool:** moves that would add more links than are free are refused, and refusals are counted? | **Yes** | The simplest exact form of conservation |
| **C3d-Q2** | **Ceiling at 30 links per event** (about 2.2× the flat mean)? | **Yes, a knob** | Loose enough not to shape the flat case, tight enough to stop the extremes C3c saw |
| **C3d-Q3** | **Calibrations as a gate:** if the flat calibration doesn't read flat at both sizes, stop before the growth runs? | **Yes** | C3c spent a day before that failure showed up |
| **C3d-Q4** | **Restore the spectral dimension** and add diameter and mean distance? | **Yes** | The measurement half of C3c's failure |
| **C3d-Q5** | **Five settings, two sizes, two seeds, T = 200** | **Yes** | Cost-bounded; S5 dropped, since the stronger-sync case can come back in a strength scan if S4 passes |

## Next step

**If the defaults hold:** write the code and implementation notes, run the timing trial, then the calibration gate. **Running the growth runs needs a separate yes.**
