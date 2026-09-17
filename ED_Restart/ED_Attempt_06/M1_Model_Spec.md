# The constrained growth model: specification (on paper)

*ED_Attempt_06, note 11. 2026-09-15 (RD15). Ledger: C56–C60. **A specification only: no code written, nothing run.** Meaning questions M-Q1–M-Q5, the knob ranges, the expected results and the exit rule are for Allen to confirm. **Running is a separate yes.***

## What the model is for, and what it isn't

**It tests two on-paper claims:**
1. **Road G's process, with nothing constraining it, heads to just above two dimensions** (C36).
2. **The same process, kept inside the smoothness conditions** (sync as contraction, a dimension ceiling, many short loops: C47, C54), grows a smooth three-dimensional pattern **that stays that way.**

**It also measures two open numbers:**
- how much of a wave leaks into the dark sector when relations rewire (C52);
- the stuck share.

**What it isn't:**
- **not a derivation.** A model result is recorded as a model result, with its knobs counted by the census guard;
- **not a search for settings that give 3.** Every range and threshold below is fixed before any code exists.

**Attempt 4's bar applies** (A4 C59): no known programme grows three dimensions as a resting state with nothing put in. **Not meeting it is a likely outcome,** and it's written into the expected results.

## The model: CGP (constrained growth process)

### State

- **A pattern:** loci and relations (an undirected simple graph), always connected.
- **Each locus has a clock:** a phase θ and its own natural rate ω, drawn once at birth from a normal distribution with spread σ (G-Q9: rates differ a little at random).

### One tick, in order

| step | rule | ED meaning behind it |
|---|---|---|
| **1. Clocks** | Every locus: θ ← θ + ω + (K/k_max)·Σ over neighbours sin(θ_neighbour − θ). A single relation pulls by at most K/k_max per tick | Clocks want to sync (A4 D20); bounded pull per relation (G-Q8) |
| **2. Rates** | Each locus's effective rate Ω is its phase advance over the last W ticks divided by W. A locus is **out of step** if \|Ω − (mean Ω of its neighbours)\| > τ | "Rates can match" (G-Q6) |
| **3. Birth** (every B ticks) | A new locus is born with its own ω and linked to **both ends of a randomly chosen relation** (a triangle), if both have room | Growth adds loci locally (G-Q3); births happen everywhere, not at an edge (C17) |
| **4. Sync pull** | Pick one out-of-step locus with room. Propose a relation to a random locus exactly **two hops** away with room (closing a triangle). Accept with probability e^(−c), subject to the constraints | Sync pulls relations in where rates fail (G-Q11); each relation costs commitment (G-Q11); local (G-Q3) |
| **5. Rewire** | Pick a random relation a–b and a random relation c–d with c within two hops of a and d within two hops of b. Propose cutting both and rejoining **a–c and b–d**. Accept only if total rate mismatch (Σ\|Ω_i − Ω_j\| over the two relations) goes **down**, subject to the constraints | Cut and rejoin only in pairs (G-Q2, A5 D10); local (G-Q3); sync favoured (G-Q6) |

### Constraints (checked before any move is accepted)

| constraint | rule | ED meaning |
|---|---|---|
| **Neighbour cap** | No locus exceeds k_max relations | No infinities (A4 D32, S-Q3) |
| **Curvature floor** | After the move, every relation touching a changed locus has curvature κ ≥ κ_min. Curvature is Ollivier's, with the lazy random walk (half the mass stays put), computed exactly by optimal transport on the local neighbourhood | Sync as contraction, never beaten by spreading apart (S-Q1) |
| **Connected** | The pattern stays connected (checked exactly) | One pattern |
| **Simple** | No self-relations, no doubled relations | — |

**Quadratic energy (S-Q2)** holds automatically: the pattern's random walk has a quadratic energy on any graph. It is recorded, not enforced.

**The control** is the same model with **no curvature floor** (κ_min = −∞). That's C36's process.

## Knobs

**Fixed choices** (labelled model choices, not scanned):

| knob | value | why |
|---|---|---|
| σ (rate spread) | 0.05 rad per tick | Sets the unit; only K/σ and τ/σ matter |
| W (rate window) | 50 ticks | Several coupling times at the weakest scanned coupling |
| τ (out-of-step threshold) | 0.2 σ | A clear mismatch, well above window noise |
| B (birth interval) | 10 ticks | Slow enough that clocks respond between births |
| Laziness of the curvature walk | ½ | Ollivier's standard choice |
| Seed pattern | one triangle (3 loci) | The smallest pattern a birth can grow from; the One Being is nothing (A5 D3), so the start carries no structure |

**Scanned knobs** (the result must hold across these, not in a corner):

| knob | values | why these |
|---|---|---|
| K/σ (sync strength) | 1, 3, 10, 30 | ED doesn't supply it (C33); from weak to strong |
| c (relation cost) | 0.5, 1, 2 | ED doesn't supply it |
| k_max (neighbour cap) | 8, 12, 16 | ED doesn't supply it |
| κ_min (curvature floor) | −0.2, −0.1, 0 | "Nearly nonnegative at the grain" (C45) |

**The full scan is 4 × 3 × 3 × 3 = 108 settings.**

**Central setting:** K/σ = 10, c = 1, k_max = 12, κ_min = −0.1.

## Sizes, seeds, stopping

- **Growth stops at N_final loci:**
  - the **central setting** runs at N_final = 1,000, 4,000 and 16,000, with 5 seeds each;
  - the **full scan** runs at N_final = 4,000, with 3 seeds each;
  - the **control** repeats the same runs with no curvature floor.
- **Then a resting phase:** no more births; steps 1, 2, 4 and 5 continue for 20 × (number of relations) rewire attempts.
- **Readings are taken at 5 checkpoints:** 0%, 25%, 50%, 75% and 100% of the resting phase.
- **"At rest" means** the readings at all 5 checkpoints meet the criteria, with a spread of at most 0.2 in each dimension reading.

## Readings (fixed before any run)

| | reading | procedure |
|---|---|---|
| **R1** | **Mass dimension d_H** (counting outward) | From 200 random centres, count loci within r hops, V(r). Fit the slope of log V against log r for r from 2 up to the largest r with mean V(r) ≤ N/10. **Small-world flag:** raised if that largest r is below 5, or if log V fits a straight line in r better than in log r |
| **R2** | **Ball-cut exponent β** | For the same balls, count relations crossing the edge, C(r). β is the slope of log C against log V. A space-like pattern has β ≈ 1 − 1/d_H |
| **R3** | **Spectral dimension d_s** | Lazy random walk (½ stays) from 200 starts, computed exactly by sparse matrix powers. Return probability p(t) is fitted as p ∝ t^(−d_s/2) for t from 10 up to where p reaches 10/N |
| **R4** | **Walk dimension d_w** (the smoothness test) | Same walks: mean squared hop distance ⟨r²⟩(t) is fitted as ∝ t^(2/d_w) over the same window. **Smooth means d_w ≈ 2;** fractal means d_w > 2 |
| **R5** | **Consistency** | \|d_s − 2 d_H/d_w\| (Alexander–Orbach relation) |
| **R6** | **Sameness everywhere** | Coefficient of variation of V(r) across centres at the middle radius |
| **R7** | **Sync** | Fraction of loci whose Ω is within τ of the largest cluster of matching rates |
| **R8** | **Curvature** | Mean and 5th percentile of κ over all relations |
| **R9** | **Dark sector** | Stuck share from the algebra, 1 − 2/(mean neighbours) + 1/(2·relations). **Leakage** (at N_final = 1,000 only): for 200 accepted rewires, take 20 random unit states in the moving sector before the rewire and measure the squared size of their part outside the new moving sector (sparse least squares) |

**Calibrations** (run first, through the same reading code):

| pattern | size |
|---|---|
| **3D random geometric graph,** periodic box, mean neighbours 12 | 16,000 |
| **3D cubic grid,** periodic | 25³ = 15,625 |
| **2D random geometric graph,** periodic, mean neighbours 8 | 16,000 |
| **Random 12-regular graph** (small world) | 16,000 |

## Expected results, written down before the first run

| | expected | on what grounds |
|---|---|---|
| **E0** (calibrations) | 3D random graph and 3D grid: d_H and d_s in [2.6, 3.4], d_w in [1.8, 2.2], β in [0.55, 0.78]. 2D random graph: d_H and d_s in [1.7, 2.3], d_w in [1.8, 2.2]. Random regular graph: small-world flag raised | Known geometry; tests the reading code |
| **E1** (stuck share) | Equals 1 − 2/(mean neighbours) + 1/(2·relations) exactly, at every checkpoint | Algebra (C49, C50) |
| **E2** (leakage) | Mean leakage per rewire between 10⁻⁴ and 10⁻² at N_final = 1,000 | A rewire changes a handful of arcs out of about 2N moving states, so roughly (a few)/(2N) |
| **E3** (control, no curvature floor) | In at least half of the settings: at rest, **either the small-world flag is raised, or d_H is in [2.0, 2.7] with d_w > 2.2** | C36's scaling argument (heads to the floor, uneven) |
| **E4** (constrained, against control) | In at least half of the settings: **d_w closer to 2 than in the matching control setting** | The curvature floor excludes fractal roughness (C43, C45) |
| **E5** (constrained, the bar) | **Fails the "smooth three at rest" criteria (below) in at least half of the scanned settings** | Attempt 4's bar (A4 C59): no known programme does this |
| **E6** (sync) | At K/σ = 30, R7 ≥ 0.9 at rest in both constrained and control runs | Strong coupling above the entrainment threshold in three or more dimensions (C28) |

## Exit rule (fixed before any run; no rule, range or threshold changes afterwards)

**"Smooth three at rest"** means, at all 5 resting checkpoints:
- d_H and d_s both in [2.6, 3.4];
- d_w in [1.8, 2.2];
- R5 ≤ 0.3;
- β in [0.55, 0.78];
- no small-world flag;
- a spread of at most 0.2 in each dimension reading.

| | outcome | recorded as |
|---|---|---|
| **X0** | **Any calibration misses E0** | The reading code is broken: **no process result counts.** The harness error is recorded, the readings are fixed, and the calibrations are rerun. Process rules and ranges don't change |
| **X1** | **Smooth three at rest** at all three sizes in the central setting (with N_final = 16,000 inside the ranges) **and** in at least 75% of the 108 settings | "**Model result:** the constrained process grows a smooth, direction-free, three-dimensional pattern that stays that way, conditional on M-Q1–M-Q5; not a derivation; four scanned knobs and six fixed choices counted by the census guard" |
| **X2** | Smooth three at rest in 25–75% of settings | "**Three in a region of the knobs;** the region is recorded, and counts as tuning" |
| **X3** | Smooth three at some checkpoints but not all | "**Three at a moment, not at rest**" |
| **X4** | Otherwise | "**The smoothness conditions, as read, don't make this process grow a smooth three;** wall 3 stands as conditions without a working rule" |
| **X5** | Control against E3 | "C36's scaling argument **supported / not supported** by the model," recorded separately |
| **X6** | Leakage against E2, sync against E6 | Recorded as measured |

**Any follow-up after a run is labelled as not pre-registered.**

## What running would need (not done)

- **Allen's yes.**
- **Code in `ED_Attempt_06/model/`.** Every run saves its settings, seed, checkpoint readings and exit status.
- **Order:**
  1. a timing trial at N_final = 1,000 in the central setting with readings off (timing only, no readings recorded);
  2. the calibrations (E0);
  3. the process runs.
- **If the timing trial shows the full plan can't finish,** the sizes are reduced by a rule fixed now: the largest size halves until it fits. The scan stays at 4,000. The change is recorded before any process reading is taken.

## Census note

Four scanned knobs (K/σ, c, k_max, κ_min) and six fixed choices (σ, W, τ, B, the laziness, the seed). Even the best outcome (X1) adds these as model inputs. **The model can move wall 3 from "no rule" to "a rule with knobs"; it can't shorten ED's input list.**

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **M-Q1** | **Is a new locus born onto an existing relation,** linked to both its ends? | **Yes** | The most local birth; happens everywhere the pattern is, not at an edge |
| **M-Q2** | **Does sync pull in a relation to a locus two hops away** (closing a triangle)? | **Yes** | The shortest new link that isn't already there; it builds the short loops smoothness needs |
| **M-Q3** | **Is a rewire accepted only if it reduces rate mismatch?** | **Yes** | Sync is what's favoured (G-Q6, G-Q7) |
| **M-Q4** | **Is commitment's cost an acceptance chance e^(−c) per new relation,** with c scanned? | **Yes, labelled** | The simplest cost; ED doesn't fix c |
| **M-Q5** | **Are ED's clocks stood in for by phase oscillators with bounded pull** (the Kuramoto form)? | **Yes, labelled stand-in** | The standard model behind the floor result (C28); bounded per relation (G-Q8) |

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide M-Q1–M-Q5** and confirm the knobs, readings, expected results and exit rule | Fixes the model before any code |
| **(b)** | **Then, if you say run:** timing trial, calibrations, runs, in that order | The test itself |
| **(c)** | **Revise the specification** before confirming | If any rule or range looks wrong to you |
| **(d)** | **Conclude attempt 6 without running** | If the model belongs in attempt 7 |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C56 | Lin, Lu, Yau, "Ricci curvature of graphs", *Tohoku Math. J.* 63, 605 (2011) (listing); Ollivier, arXiv:math/0701886 (A6 C42); Alexander and Orbach, *J. Physique Lett.* 43, 625 (1982), and the Einstein relation d_s = 2d_f/d_w (listings); Hong, Park, Choi, *PRE* 72, 036217 (A6 C21, C28) | 2026-09-15 |
| — | A4-ledger C59, D20, D32; A5-ledger D3, D10; A6 C17, C28, C33, C36, C43–C54 | Earlier ledgers |
