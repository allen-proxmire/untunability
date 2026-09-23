# E3: the crossing's character (specification, on paper)

*ED_Attempt_08, note 3. 2026-09-19 (RD8). Ledger: C16–C19. **A specification only: no code, nothing run.** Questions E3-Q1–E3-Q6 and the expected results are for Allen to confirm; running the pilot is a separate yes, and running the campaign is another.*

## What E3 asks

**Note 2's question (C4), unchanged:**

> **As slices grow, does ED's crumpled-to-branched crossing sharpen (first order, as in dynamical triangulations) or broaden (continuous)?**

The knob turned is **sync's threshold**. The port (C7, C8, C15) is what makes it affordable.

## What is already settled, and what E3 inherits

| | |
|---|---|
| **The port is attempt 7's model** | All three tiers pass (C15); eight seeds against eight, U p-values 0.645–0.878 |
| **Speed** | 7.2× measured; one 150-tick run is 15.5 min at n = 24, 26 min at n = 32, **2.0 h at n = 52** (C9) |
| **Three sizes, not four** | The pre-registered consequence of the speedup landing under 8× (C6, C9). **n = 24, 32, 52** — still a 10× span in volume |
| **Expected results and the exit rule** | Fixed in note 2 (C6). E3-3's *definition of width* is the one thing this note adds, and the pilot is what sets it |

## 1. The control parameter has a 10% wobble that has to go first (C16)

**Attempt 7 set the threshold as `s_max = 1.5 × (the flat calibration's largest link strain)`.** That calibration draws random rates, so **its value depends on a reading seed**: at n = 24 the flat slice's neck strain is **6.657 at reading seed 1 and 7.304 at reading seed 0** — a 10% spread in what is supposed to be a fixed property of flat space.

**That wobble already did damage once.** It is exactly what made tier 3 fail (C13): two codes at the "same" threshold were 9.7% apart.

**Proposed fix, and it is a change from attempt 7:** the threshold becomes

> **s_max(f, n) = f × median over 8 reading seeds of the flat slice's largest link strain at n**

with **f** the scanned control. This costs eight sparse solves per size, once. It removes an arbitrary 10% from the control parameter, which matters doubly here because **the whole measurement is the width of a crossing in f** — a 10% jitter in the abscissa would swamp the thing being measured.

**Consequence, recorded plainly:** E3's f = 1.5 is not exactly attempt 7's threshold. Nothing is being compared to attempt 7 in E3, so this costs nothing, but it must not be quietly conflated later.

## 2. Which quantity is the order parameter is not yet known (C17)

**Being honest about the state of knowledge.** Attempt 7's threshold scan (A7 C101) was one seed, one size, four thresholds, and it did not record several quantities. What it showed at n = 24:

| f (roughly) | events vs start | diameter (flat 18) | slice d_H | slice d_s | spacetime d_H | refusals/tick |
|---|---|---|---|---|---|---|
| **≈1.5** | 1.01 | 15.0 | — | — | 6.33 | 1,403 |
| **≈0.9** | 1.06 | **25.0** | — | — | 6.35 | 3,993 |
| **≈0.45** | 1.17 | 23.0 | 4.80 | **1.35** | 5.57 | 9,902 |
| **≈0.22** | **1.30** | 16.0 | 4.39 | **1.59** | 5.39 | **54,702** |

**Two things are clear from it, and one is not.** Clear: the pattern does move with f, and at tight f it reads branched. Clear: **the tightest setting strangles growth** (719 splits abandoned per tick) — that is a *third* outcome, not the branched phase, and E3 must label it as such. **Not clear: which quantity moves monotonically across the crossing.** Diameter does not — it rises then falls, because strangling sets in.

**So E3 runs in two parts, and only the second is pre-registered:**

- **E3a, the pilot** — exploratory, labelled as such: **n = 24, one seed, nine values of f**, everything recorded. Its job is to find where the crossing sits and which quantity moves cleanly through it. **Nothing in the pilot is a result.**
- **E3b, the campaign** — the order parameter, the crossing's location and the ladder spacing are **fixed from the pilot and written down as a decision before any campaign run starts**, along with the expected results already fixed in C6.

**This is the "measure before you tighten" lesson from attempt 7, applied before spending the compute rather than after.**

### The candidates the pilot judges

| candidate | flat | crumpled | branched | cost |
|---|---|---|---|---|
| **Stringiness R = diameter / V^(1/3)** | **0.75** | falls toward 0 with size | grows with size | free |
| **Links per event** | 6.70 | rises (13.4 = the crumpled flag) | falls | free |
| **Spectral dimension d_s** | 3.0 | above 3 | **at or below 2** | slow; undefined at small sizes |
| **Spacetime mass dimension** | 4.0 | above | below | moderate |
| **Events vs start** | 1.0 | — | rises | free |

**R is the favourite going in** — it is free, it is size-aware, and all three phases have known values — but the pilot decides, not this note.

## 3. Defining "sharpens or broadens" (C18)

Once the order parameter **X(f)** is chosen, the **crossing width W** is the range of f over which X moves through the middle of its range:

> **W = f(X = X_hi − 0.75ΔX) − f(X = X_hi − 0.25ΔX)**, by linear interpolation on the ladder, where ΔX = X_hi − X_lo across the ladder.

| outcome | what is recorded |
|---|---|
| **W shrinks as a power of volume**, W ∝ V^(−a) with a > 0 beyond its error bars | **The crossing sharpens.** First-order-like, as in dynamical triangulations |
| **W does not shrink**, or shrinks with a consistent with 0 | **The crossing broadens or holds.** Continuous is live, and road E continues into exponents |
| **W cannot be measured at the largest size** | "Not resolved at these sizes," with what it would need |

**Also recorded at every point, because a first-order crossing shows them and a continuous one does not:** the **seed-to-seed spread of X** at each f (it peaks at the crossing and, for first order, becomes **double-peaked**), and whether any single run's X sits far from the others.

**Three seeds cannot see a double peak.** That is a stated limitation of this design, not a claim it avoids.

## 4. The runs

| | pilot (E3a) | campaign (E3b) |
|---|---|---|
| **Sizes** | n = 24 | n = 24, 32, 52 |
| **f** | 2.0, 1.5, 1.2, 0.9, 0.7, 0.55, 0.45, 0.3, 0.22 (nine) | six, bracketing the crossing found by the pilot |
| **Seeds** | 1 | 4 at n = 24 and 32, **3 at n = 52** |
| **Ticks** | 150 | 150, plus **one T = 300 check at n = 24** (E-Q4) |
| **Control** | setting A (sync off) is the f → ∞ rung | the same, one per size per seed |
| **Runs** | 9 | 24 + 24 + 18 = **66**, plus 3 calibrations and 11 controls |

**Cost, from measured per-tick times (C9), not from an assumption:**

| | per run | runs | total |
|---|---|---|---|
| **Pilot** | 15.5 min | 9 | **2.3 h** → about 35 min on 4 workers |
| **n = 24** | 15.5 min | 28 | 7.2 h |
| **n = 32** | 26 min | 28 | 12.1 h |
| **n = 52** | 2.0 h | 21 | 42 h |
| **Campaign total** | | | **61 h single process → about 15 h on 4 workers** |

**Plus spacetime readings at n = 52:** about 1.5 million events per run against 292,000 at n = 24, where ball growth took 16 s. **This is not yet measured and is the one soft number in the plan.** The pilot does not touch it, so **E3b is not planned until a single n = 52 spacetime reading has been timed** — the same rule that governed E2.

## 5. Expected results and the exit rule

**Unchanged from note 2's C6** (E3-0 to E3-5 and its six-row exit rule), with three additions:

| | added | why |
|---|---|---|
| **E3-6** | **Growth strangled is its own outcome:** a run with more than 10 abandoned splits per tick, or an event count more than 20% above the start, is recorded as *strangled* and is not given a shape | The tightest setting in attempt 7's scan did exactly this, and calling it "branched" would be wrong |
| **E3-7** | **The pilot's ladder brackets the crossing:** X at the loosest f and X at the tightest differ by more than three times the seed-to-seed spread at n = 24 | If the ladder does not span the crossing, the campaign is pointless and must be re-laddered first |
| **E3-8** | **The control (sync off) sits at the loose end**, within the spread of the loosest f | A control that does not agree with the loose limit means f is not the only thing acting |

**And one rule about the pilot, fixed now:** **if the pilot shows no quantity moving monotonically across the crossing, E3b does not run.** That result is recorded as "ED's crossing has no order parameter this design can see," and road E returns to Allen. **The pilot is allowed to stop the campaign.**

## 6. Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **E3-Q1** | **Threshold as f × the median flat strain over 8 reading seeds**, dropping attempt 7's single-seed value? | **Yes** | A 10% jitter in the abscissa would swamp a width measurement; it already caused C13 |
| **E3-Q2** | **A pilot first,** exploratory and labelled, with the order parameter and ladder fixed from it before any campaign run? | **Yes** | Which quantity moves is genuinely not known; guessing it costs 15 hours |
| **E3-Q3** | **The crossing width W as the quarter-to-three-quarter range**, with the seed spread reported at every point? | **Yes** | It is the least-structure definition that does not assume a functional form |
| **E3-Q4** | **Three sizes (24, 32, 52), four seeds at the first two and three at the largest?** | **Yes** | The pre-registered consequence of C9; three seeds at n = 52 is the cost ceiling, and its limitation is stated |
| **E3-Q5** | **Strangled growth as its own outcome, given no shape?** | **Yes** | Attempt 7's scan produced it and it is not a phase |
| **E3-Q6** | **The pilot may stop the campaign** if nothing moves monotonically? | **Yes** | The alternative is spending 15 hours to learn what 35 minutes would have said |

## What this note does not settle

- **Whether a continuous crossing, if found, means a continuum limit exists.** That needs exponents and a scaling function, and it is road E's second half at best.
- **Whether three seeds at n = 52 can see a double peak.** They cannot. If the width measurement points to first order, the double-peak check needs more seeds, and that is a separate cost.

## Next step

**If the defaults hold:** time one n = 52 spacetime reading, then run the pilot (about 35 minutes on 4 workers). **The campaign needs a separate yes, after the pilot's ladder and order parameter are written down.**

## Addendum: the wobble is 23%, not 10% (measured 2026-09-19, before any pilot run finished)

**Section 1 put the reading-seed spread at 10%, from the two seeds that happened to be known.** Measured properly over the eight seeds the new definition uses, at n = 24:

| | |
|---|---|
| **Values** | 7.304, 6.657, 7.051, 7.343, 7.404, 6.808, 7.556, **8.162** |
| **Range** | **6.657 – 8.162, a 23% spread** |
| **Median (the threshold's base)** | **7.3232** |

**This makes C16's change more necessary, not less.** A single reading seed lands anywhere in a 23% band, and **the crossing width E3 is trying to measure may well be narrower than that band**. Had E3 kept attempt 7's single-seed threshold, the abscissa's own jitter could have exceeded the signal.

**Recorded as a correction to the figure quoted in section 1**, made before any pilot run finished and before any pilot value was seen. The design it justifies is unchanged.
