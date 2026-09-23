# E4: does the branched reading survive at size? (specification, on paper)

*ED_Attempt_08, note 5. 2026-09-19 (RD10). Ledger: C26–C28. **A specification only: no code, nothing run.** Written after the pilot withdrew E3b (C24) and before any E4 run.*

## The question

**Every measurable slice ED has ever grown reads branched** — spectral dimension 1.29–1.47 against flat's 3 — and **every one of them was about 19 events across.** The port exists to ask the same question at **39**.

> **Does the branched reading survive when slices are twice as wide, or was it a small-size artefact?**

This replaces E3's crossing question, which the pilot showed has only one side (C23).

## The comparison is against flat *at the same size*, not against 3 (C26)

**A fact that changes how every reading in E4 must be judged.** Attempt 7's flat calibration does not read 3:

| | flat slice (FC) | randomised slice (RC) |
|---|---|---|
| **n = 20** | d_H **2.629**, d_s **3.061**, mean degree 14.00 | d_H undefined, mean degree **29.27**, small-world |
| **n = 24** | d_H **2.657**, d_s **3.05**, mean degree 14.00, radii 3–6 | d_H undefined, mean degree **29.30**, small-world |

**Ball growth underestimates the mass dimension by about 12% at these sizes**, which is exactly what the literature says it does (C2). So "flat is 3.0" is true of the geometry and false of the reading. **E4 judges every grown slice against the flat calibration at its own size**, and reports the ideal values only as context.

**The randomised calibration is also worth its own line.** RC sits at mean degree **29.3**, above the crumpled flag's 26.8 — so RC *is* crumpled, and it reaches that by ignoring the link budget, since `flip_randomize` applies flips with no budget gate. **That is C22's structural claim shown from the other side:** crumpling is reachable when the budget is switched off and unreachable when it is on.

## The runs

| | |
|---|---|
| **Sizes** | n = 24, 32, 52 (V = 13,824 / 32,768 / 140,608) |
| **Threshold** | **f = 0.45**, the tightest rung that does not strangle and the only one where d_s is measurable at n = 24. `s_max = 0.45 ×` the median flat strain over 8 reading seeds at that size (C16) |
| **Seeds** | 3 (0, 1, 2) |
| **Control** | sync off, 2 seeds at n = 32 and n = 52. **At n = 24 the control is already in hand** — tier 3's eight setting-A runs |
| **Ticks** | T = 150 |
| **Calibrations** | FC and RC at each size, plus the 8-seed threshold median |
| **Runs** | 9 main + 4 control = **13**, plus 6 calibrations |

**Cost, from measured times (C9, C25), with memory as the binding constraint:**

| | per run | runs | workers | wall |
|---|---|---|---|---|
| n = 24 | 16 min | 3 | 3 | 16 min |
| n = 32 | 28 min | 5 | 4 | 35 min |
| **n = 52** | **1.4 h + 7.7 min reading** | 5 | **2** (8.4 GB total; 755 MB a slice, ~1.5 GB more while a reading runs) | **4.6 h** |
| | | | | **about 5–6 h** |

## Expected results, written down before any code

| | expected | why |
|---|---|---|
| **E4-0** | **The gate:** at every size the flat calibration reads d_H within 0.3 of its n = 24 value of 2.657 and d_s within 0.4 of 3.05, and the randomised one reads d_H undefined with mean degree above 26 | It held at n = 20 and n = 24 |
| **E4-1** | Structure, budgets, ceiling and flip neutrality exact; all runs survive and **none is strangled** (E3-6's test) | f = 0.45 did not strangle at n = 24 |
| **E4-2** | **At n = 52 the slice readings are defined:** a mass dimension with **at least six usable radii** and a diameter of at least 20 | Flat's diameter at n = 52 is about 39, against 18 at n = 24 |
| **E4-3** | **The one that matters: d_s stays at or below 2 at all three sizes**, and does not trend upward with size | Every measurable slice so far reads 1.29–1.47 |
| **E4-4** | **C22 holds at the new sizes:** mean degree stays at or below 13.40 × (V₀/V), and max degree is pinned at the ceiling of 60, in every run | It held in ten pilot runs and eight attempt 7 runs, and it follows from the budget |
| **E4-5** | The grown spacetime's mass dimension is reported at each size, with its usable radii | Five radii at n = 52 against three at n = 24 (C25) |

## The exit rule

| outcome | record |
|---|---|
| **E4-0 fails** | The readings cannot resolve flat at that size. **The readings, not the sizes, are what need replacing**; road E closes as a failed instrument. No shape is claimed |
| **E4-1 fails on structure or a budget** | A port bug. Fix, re-verify the ladder, re-run |
| **E4-1 fails only on strangling** | "f = 0.45 strangles growth at n = ⟨size⟩", so the usable ladder narrows with size. Recorded, and the largest non-strangling f is found before anything else is said |
| **E4-2 fails** | **"Too small to measure at n = 52."** Road E closes as a failed instrument — note 2's rule, and the answer is not a larger size |
| **E4-3 holds** | **"ED's growth, with its conserved budgets and its three meanings, gives a branched slice at every size reachable here, up to 140,608 events."** Attempt 7's wall stands in its corrected form, and the shape question is settled against ED at these sizes |
| **E4-3 fails — d_s rises with size** | **"The branched reading was a small-size artefact."** The shape question reopens, and the fuller threshold scan becomes worth its cost |
| **d_s at n = 52 lands in [2.4, 3.6] with d_H within 0.3 of flat's** | **"At 140,608 events ED's growth reads three-dimensional: consistent, not derived; the density, the ceiling, the threshold and the strengths are knobs."** Then the same setting at more seeds before anything else is said |
| **E4-4 fails** | C22 is wrong or incomplete; it is withdrawn or narrowed, and said plainly |

## What this cannot settle

- **Three seeds.** Enough to see whether d_s moves with size; not enough for a distribution.
- **One threshold.** E4 asks about f = 0.45 only. A different f could behave differently, and E4 says nothing about it.
- **Not a continuum limit.** Even a flat reading at one size and one threshold would be "consistent, not derived", with every knob still put in.

## Next step

**Code it, smoke-test at n = 24, then run.** The calibrations come first, and **the gate (E4-0) is checked before any growth run starts** — if flat does not read flat at n = 52, nothing downstream means anything.

## Addendum: the gate replaced, declared before the new calibrations were run (2026-09-20, D8)

**The gate as written failed twice, once on a real defect of mine and once on itself** (C27). The second failure is the one this addendum answers: E4-0 required the randomised calibration to read "d_H undefined", which was **an artefact of n = 24 being too small to fit a dimension at all**, not a property of the readings. At n = 32 and n = 52 it does fit.

**Changing a pre-registered criterion after seeing data is how a failure gets laundered into a pass.** So the replacement is written here **before the calibrations it will judge have been run**: the single-seed values of C26 and C28 are known, the five-seed spreads that the new gate tests are not.

### What the calibrations now do

**Five seeds each, where before there was one.** Flat is a deterministic slice, so its five seeds vary the *reading* (which centres, which walks). The randomised slice varies both its randomisation seed and its reading seed. This closes the gap C28 exposed: neither calibration had a spread, so "separable" could not mean anything quantitative.

### The replacement criterion

| | test | this is |
|---|---|---|
| **E4-0a** | **Resolution.** At every size, across all five seeds, flat reads d_s within **0.4 of 3.0**, d_H is defined, and at n = 52 the fit uses **at least six usable radii**. And flat's own seed spread in d_s is **below 0.5** | **The gate.** Failing it means the readings cannot resolve geometry at that size, and road E closes as a failed instrument |
| **E4-0b** | **Discrimination.** Flat and randomised have **non-overlapping five-seed ranges** in at least one shape reading (d_H or d_s) | **Recorded, not gating** — see below |
| **E4-0c** | Which readings separate the two and which do not, at each size, with their spreads | **Recorded** |

**Why E4-0b does not gate, stated plainly and in advance.** C28 already showed the shape readings barely separating flat from crumpled at n = 52 (d_H 2.85 against 3.29, d_s 3.007 against 3.072). **E4-3 does not rest on that distinction.** It asks whether grown slices read branched — d_s near **1.3** — which is about **1.7 away from flat's 3.0**, an order of magnitude beyond any spread these calibrations have shown. A gate that blocked E4 on flat-versus-crumpled would be blocking it on a discrimination the question does not use.

**So if E4-0b fails, E4 runs and the failure is carried in every claim it produces:** *the readings cannot tell flat from crumpled at this size, and nothing E4 says about crumpling can be trusted.* That limitation is stated once here and repeated in the results.

**What would make me wrong to proceed:** if flat's own five-seed spread in d_s came out large — above 0.5 — then d_s could not distinguish 1.3 from 3.0 either, and E4-0a fails, and road E closes. That is the real test, and it has not been run yet.
