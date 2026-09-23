# E3a: the pilot, and what it did to the question

*ED_Attempt_08, note 4. 2026-09-19 (RD9). Ledger: C21–C24. Run `model/e3_pilot.py`: ten runs at n = 24, one seed, T = 150, 0.79 h on four workers. **The pilot was exploratory and labelled (C17); its numbers are not results.** The two arithmetic findings in sections 3 and 4 are not exploratory — they follow from ED's own rules and the recorded run values.*

## What the pilot ran

Nine values of the sync control **f**, plus the no-sync control, at n = 24. Threshold **s_max = f × 7.3232**, the median flat strain over eight reading seeds (C16, C20).

| f | s_max | status | events / start | links per event | mean degree | max degree | R | d_s | spacetime d_H | sync refusals/tick |
|---|---|---|---|---|---|---|---|---|---|---|
| **control** | — | survived | 1.008 | **5.141** | 10.28 | **60** | 0.58 | — | 6.45 | 0 |
| 2.00 | 14.65 | survived | 1.027 | 5.123 | 10.25 | **60** | 0.54 | — | 6.27 | 572 |
| 1.50 | 10.98 | survived | 1.024 | 5.103 | 10.21 | **60** | 0.83 | — | 6.44 | 1,213 |
| 1.20 | 8.79 | survived | 1.049 | 5.096 | 10.19 | **60** | 0.82 | — | 6.52 | 1,767 |
| 0.90 | 6.59 | survived | 1.045 | 5.076 | 10.15 | **60** | 0.78 | — | 6.15 | 3,058 |
| 0.70 | 5.13 | survived | 1.074 | 5.066 | 10.13 | **60** | 0.77 | — | 5.89 | 4,595 |
| 0.55 | 4.03 | survived | 1.096 | 5.042 | 10.08 | **60** | 0.81 | — | 6.03 | 6,347 |
| 0.45 | 3.30 | survived | 1.125 | **5.017** | 10.03 | **60** | 0.76 | **1.39** | 5.86 | 8,184 |
| 0.30 | 2.20 | **strangled** | 1.339 | 4.966 | 9.93 | **60** | 0.79 | **1.29** | 5.57 | 18,881 |
| 0.22 | 1.61 | **strangled** | 1.316 | 5.090 | 10.18 | **60** | 0.61 | **1.47** | 5.64 | 49,151 |

*Flat: links per event 6.70, mean degree 13.40, R = 0.75. Crumpled flag: mean degree ≥ 26.8. Branched flag: d_s ≤ 2.*

## 1. The order parameter: links per event (C21)

**Of the five candidates, one is usable.**

| candidate | verdict |
|---|---|
| **Links per event** | **Monotone** from the control to f = 0.45: 5.141 → 5.017. The move is 0.124 against a seed-to-seed standard deviation of 0.013 known from tier 3 — **a signal about ten times the noise** |
| **Stringiness R = diameter / V^(1/3)** | **Unusable.** Diameter is an integer, and tier 3 measured it scattering 14–22 across seeds at fixed settings; that scatter alone spans R = 0.58 to 0.92, which is wider than the whole range R covers across the ladder. The favourite going in, and the pilot killed it |
| **Spectral dimension d_s** | **Exists only on one side.** Undefined for f ≥ 0.55 — the slices are too small to measure — and 1.29–1.47 where it is defined. A phase flag, not an order parameter |
| **Spacetime mass dimension** | Falls 6.45 → 5.86, but not monotonically (6.27, then 6.44, then 6.52), on a seed spread of 0.157. Usable as a check, too noisy to be the order parameter |
| **Events vs start** | Monotone, 1.008 → 1.125, but it measures growth, not shape |

**Both pre-registered ladder checks pass:** E3-7 (loosest to tightest exceeds three times the seed spread) — 0.124 against 0.039, passes. E3-8 (the control sits with the loosest f) — 5.141 against 5.123, about 1.4 standard deviations, passes.

**And both checks missed the real problem**, which is the next two sections. That is worth saying plainly: the checks I wrote tested the ladder's *magnitude*, and the thing wrong with it is its *location*.

## 2. Strangling starts between f = 0.45 and f = 0.30

At f = 0.30 the event count is 34% above the start; at f = 0.22, splits are abandoned **548 times per tick**. Both are recorded as strangled and given no shape (E3-6). **The usable ladder is f ≥ 0.45.**

## 3. ED has no crumpled phase — the budget forbids it (C22)

**Every run's mean degree is about 10.2, against flat's 13.40 and the crumpled flag's 26.8.** Not one run is crumpled, and this is not an accident of the settings. It follows from ED's own rule:

> Links are conserved: **E ≤ BL = 6.699 × V₀**. So **mean degree = 2E/V ≤ 13.40 × (V₀/V)**.

**With the slice holding its size, mean degree cannot exceed the flat value.** Reaching the crumpled flag would need the slice to fall to **half** its starting size — and the runs grow, not shrink.

**The unpressured runs prove the cap is real, not slack.** Attempt 7's settings C and D, with no commitment or curvature, sit at mean degree **14.3 with 98–100% of the link budget spent**. They are pressed flat against the budget and can go no further. The pressured runs use only 77–84% of it.

**And the ceiling blocks the mechanism separately.** **Max degree is exactly 60 — the ceiling — in every run in this pilot and in every attempt 7 run at n = 24.** Dynamical triangulations' crumpled phase is built on *singular vertices*, whose local volume grows in proportion to the whole manifold (C2). **ED's "no infinities" bound caps any vertex at 60 neighbours, so singular vertices are forbidden outright.**

**So ED's two bounded quantities — the conserved link budget and the no-infinities ceiling — each independently exclude the crumpled phase.**

## 4. Which means E3's question was the wrong one (C23)

**E3 asked whether ED's crumpled-to-branched crossing sharpens or broadens with size.** The pilot says **there is no such crossing in ED's growth**, because one of its two phases does not exist. The ladder runs from *too small to measure* to *branched*, and then to *strangled*.

**This also corrects the wording of attempt 7's wall (A7 C103),** which said ED's rules "move the pattern along a line from crumpled to branched." By ED's own crumpled flag, **no growth run was ever crumpled.** Attempt 7's crumpled observations came from two places, neither of them a budgeted growth run: C3c's density runaway, which happened *before* the link budget existed, and C3b's stand-in slices, which were built crumpled by hand as a test of the readings.

**The finding underneath is stronger than the question it replaces.** In dynamical triangulations the crumpled and branched phases meet at a first-order transition, and that transition is the obstacle to a continuum limit (C2). **ED's conserved budget and its finite-neighbour bound remove one of the two phases by construction.** That is what "what CDT tunes, ED conserves" cashes out to here — and it is the first time that slogan has had a concrete structural consequence rather than a numerical one.

**What it does not say:** it does not say ED has a continuum limit, or that the remaining side is flat. Every measurable slice in this pilot reads **branched** (d_s 1.29–1.47, flat is 3). The wall of attempt 7 stands; only its description changes.

## 5. So E3b as specified should not run (C24)

**The campaign was 15 hours to measure the width of a crossing.** There is no crossing to measure. Running it would produce a width for a drift within one phase, and a finite-size scaling of that number would mean nothing.

**Invoking note 3's rule (E3-Q6) in its spirit if not its letter:** the rule let the pilot stop the campaign if nothing moved monotonically. Something does move monotonically — links per event — but the premise the campaign rests on fails. The pilot cost **47 minutes and saved 15 hours**, which is what it was for.

## Options (Allen decides)

| | option | cost | what it settles |
|---|---|---|---|
| **(a)** | **Record the finding and re-pose road E** around what is actually there: ED has no crumpled phase, and the measurable side is branched. The new question is whether the branched reading survives at n = 52, where slices are 39 across instead of 19 | About 6 h: three sizes, setting B at one or two values of f, three seeds | Whether "branched" is the real answer or a small-size artefact |
| **(b)** | **Test the structural claim directly** by raising the ceiling and the link budget and seeing whether crumpled appears | A few hours, and it is a **meanings question** — changing ED's no-infinities bound is Allen's call, not a knob-turn | Whether the budget and ceiling are what exclude crumpling, or something else is |
| **(c)** | **Run E3b anyway** as specified | 15 h | A width for a drift; I do not recommend it |
| **(d)** | **Stop and take stock of road E** on paper before any more compute | — | — |

**Proposal: (a).** The branched reading is the one thing every measurable run agrees on, and it has only ever been measured on slices 19 events across. The port exists precisely to ask it at 39.

## Sources

- [Phase Structure of Dynamical Triangulation Models in Three Dimensions](https://arxiv.org/pdf/hep-lat/9712011)
- [Three-Dimensional Simplicial Gravity and Degenerate Triangulations](https://arxiv.org/pdf/hep-lat/9807026)
