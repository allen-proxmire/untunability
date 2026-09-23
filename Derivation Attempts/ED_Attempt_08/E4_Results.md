# E4 results: the branched reading survives, and bigger slices are ruled out as a route

*ED_Attempt_08, note 7. 2026-09-20 (RD13). Ledger: C34–C37. Runs `model/e4_run.py` (13 growth runs, 30 calibrations, about 6 h) and `model/e4_dscurve.py` (three scale curves, about 5 h). The scale curves are a **diagnostic, not pre-registered**, added after the fitting windows were found to sit in one place at every size; the prediction they were judged against **was** written down before they ran.*

## The question

**Every measurable slice ED had grown read branched — and every one was about 19 events across.** E4 asked whether that survives at 39.

## 1. The runs (C34)

Thirteen growth runs at f = 0.45, three sizes, three seeds, plus no-sync controls. **All survived. Structure, the event budget, the link budget, the ceiling and flip neutrality were exact at every tick of every run, including at 156,172 events.**

| | sync on (3 seeds) | | sync off (2 seeds) |
|---|---|---|---|
| | **d_s** | d_H | **d_s** |
| **n = 24** | 1.393 – 1.422 | 4.74 – 4.76 | — (tier 3's eight runs) |
| **n = 32** | 1.392 – 1.498 | 4.97 – 5.08 | **1.728 – 1.784** |
| **n = 52** | 1.635 – 1.685 | 6.01 – 6.21 | **2.318 – 2.319** |

*Flat at the same sizes: d_s 3.050, 3.024, 3.007; d_H 2.657, 2.740, 2.850.*

**E4-4 held everywhere:** mean degree 9.98 – 10.31 against the budget's bound of 11.73 – 13.44, and max degree pinned at the ceiling of 60, in all thirteen runs. **C22 stands at ten times the size.**

## 2. The fitting window never widened, and that changed the question (C35)

| | flat | grown |
|---|---|---|
| n = 24 | radii **3 – 6** | radii **2 – 4** |
| n = 32 | radii **4 – 8** | radii **2 – 4** |
| n = 52 | radii **7 – 14** | radii **3 – 5** |

**Flat's measurement window grows with size. The grown slices' does not.** So every spectral dimension in the table above describes a **two-hop span at short range** — and the apparent upward drift with size, 1.41 → 1.44 → 1.66, is the window sliding, not the geometry changing.

**This was Claude's error of interpretation, and it was reported to Allen as a finding before it was checked.** The fitting windows should have been looked at before any verdict was offered. They were not.

## 3. ED's spectral dimension runs with scale (C36)

Each slice was **re-grown exactly** — the port's generator is seeded, and all three re-grown slices matched their runs to the event and the link — and then measured at every distance instead of one window.

| walk radius | n = 24 | n = 32 | n = 52 |
|---|---|---|---|
| ~1.4 | 2.38 | 2.39 | 2.35 |
| ~2.8 | **1.36** | **1.43** | **1.48** |
| ~4.3 | 1.80 | 1.66 | 1.82 |
| ~5.6 | 2.60 | 2.06 | 2.30 |
| ~6.9 | 3.65 | 3.60 | 3.08 |
| **peak** | **3.88** | **4.00** | **4.94** |
| **walk's reach** | **6.68** | **7.37** | **8.45** |

**The single fitted number was always the bottom of the dip.** The run at n = 52 fitted 1.685 over radii 3–5; the curve's minimum is 1.48 at radius 2.8.

**The flat slice's curve is nearly constant at 3.0–3.3 across the same radii**, then collapses at saturation. So the dip is a real feature of grown slices, not an artefact of the method.

## 4. What settles it, against a prediction made first (C37)

**Written down before the n = 52 curve ran:** the walk's reach should come in near **11.6** if the slices are three-dimensional at large scales, or near **8.5** if the rise is a finite-size effect.

> **It came in at 8.45.**

**Ten times the volume bought 26% more reach.** Fitting all three sizes:

| | reach grows as |
|---|---|
| **ED's grown slices** | **V^0.101** — an effective dimension of **9.9** |
| **Flat slices** | **V^0.333** — exactly three, measured the same way |

**And the peak is rising, not converging:** 3.88 → 4.00 → **4.94**. Real three-dimensional behaviour would settle near 3. Overshooting further at each size is the signature of a walk reaching equilibrium, not of a dimension.

### The part that makes this final

**The walk saturates before the spectral dimension can settle, and a bigger slice cannot fix it.** At V^0.101, **doubling the reach takes about 943 times the volume.** An n = 52 run takes 1.4 hours; 943× of that is not a compute problem, it is a wall.

> **Road E's question is answered, and the route it was built on is closed. Bigger slices cannot settle the shape of ED's grown space — not with more time, not with a faster model. The obstruction is that the geometry is too compact for the measurement to converge.**

## 5. What E4 records

| | |
|---|---|
| **E4-0** gate | **Passed** at all three sizes (C30) |
| **E4-1** structure and budgets | **Passed**, exact in all thirteen runs |
| **E4-2** readings defined at n = 52 | **Passed** — but over radii 3–5, not the six-radius span flat gets |
| **E4-3** d_s stays ≤ 2 and does not trend upward | **Held in substance**: every grown slice reads 1.39–1.69 with sync and 1.73–2.32 without, against flat's 3.01. The apparent upward trend is the window sliding (C35), not the geometry |
| **E4-4** the budget's cap on mean degree | **Passed** at ten times the size |
| **E4-5** the grown spacetime | **Reduced to one seed for memory** (C31), and the reading over 3.26 million events needs 6.5 GB of an 8.4 GB machine |

**By the exit rule fixed in note 5:** *ED's growth, with its conserved budgets and its three meanings, gives a branched slice at every size reachable here, up to 156,172 events. Attempt 7's wall stands in its corrected form.*

## 6. Two things that are not the wall

**The controls are the most space-like numbers this project has produced.** With the sync condition off, d_s reads **2.318 and 2.319** at n = 52 — identical to three figures, and a long way above the 1.64–1.69 with it on. **Switching sync off moves the slice toward three dimensions.** Read with note 6's decision (D10, C32), the runs with it on were testing a **local veto**, not sync — and the veto is pushing the geometry away from space.

**And 2.32 is still not 3.** Commitment and curvature are still acting in the controls, still local, still losing to entropy. **Sync's form is part of the wall, not all of it.**

## 7. What this closes and what it opens

**Closed:** bigger slices, as a route. Road E was built on the hope that resolution was the obstacle. It was not, and the reason is now measured rather than guessed.

**Open, and sharper than before:**
1. **Sync acting on whole slices**, as Allen has now decided it means — item 4 of attempt 7's carry-forward, never opened, and the first road that tests ED's own meaning rather than a modelling convenience.
2. **The local costs.** Commitment as α·E and curvature as an edge sum arrived the same way sync did, and they are what remains when the veto is removed.
3. **Whether a single grown history can give smooth geometry at all** — the question under all of it, and a meanings question for Allen.

## Honest limits

- **One threshold.** E4 tested f = 0.45 only.
- **Three seeds**, and one scale curve per size on one seed.
- **The scale curves are a diagnostic**, added mid-road; the prediction they were judged against was fixed first, the curves themselves were not pre-registered.
- **Nothing here is derived.** Inputs supplied: still 3.
