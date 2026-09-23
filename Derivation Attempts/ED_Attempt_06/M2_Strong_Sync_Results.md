# M2 results: weak and strong sync

*ED_Attempt_06, note 17. 2026-09-16 (RD29). Ledger: C89. A labelled partial result (D20), not note 13's full verdict. All M2 runs saved in `model/m2_runs/`.*

## What was run

**M2** (note 13): newborns go inside links; sync pulls links in; paired rewiring; a neighbour cap; a curvature floor. **No time order**, so space can branch freely.

**What the saved results cover:**

| group | runs | notes |
|---|---|---|
| **Central setting, floor −0.1** (K/σ 10) | 10 (1,000 and 4,000 loci) | Full |
| **Floor −0.2, weak sync** (K/σ 1) | 13 | Partial: 4 settings |
| **Floor −0.2, strong sync** (K/σ 30) | 27 | Full: 9 settings × 3 seeds |
| **Control, no floor** | 30 weak-sync-side, 27 strong sync | — |

## Results

**No run, at any sync strength, reaches "smooth three" at any checkpoint.**

| | what grows | mass dim | walk-return dim | walk dim |
|---|---|---|---|---|
| **Floor −0.1** | A single ring | 1.0 | 1.0 | 2.0 |
| **Floor −0.2, weak sync** | Dense (7.4 links each), rough | 1.5 | 0.9 | 2.7 |
| **Floor −0.2, strong sync** | Less dense (5.3), rough | 1.6 | 1.1 | 2.7 |
| **Control (no floor)** | Small world, no finite dimension | — | — | — |

### Strong sync, setting by setting (floor −0.2, 4,000 loci, 3 seeds each)

| link cost c | cap | links each | mass dim | walk dim | stalled |
|---|---|---|---|---|---|
| 0.5 | 8 | 5.5 | 1.68 | 2.66 | 0/3 |
| 0.5 | 12 | 6.9 | — | — | **3/3** |
| 0.5 | 16 | 7.8 | — | — | **3/3** |
| 1 | 8 | 4.9 | 1.43 | 2.79 | 0/3 |
| 1 | 12 | 6.0 | 1.22 | 2.50 | 2/3 |
| 1 | 16 | 6.7 | 1.20 | 2.37 | 2/3 |
| 2 | 8 | 3.5 | 1.55 | 2.80 | 0/3 |
| 2 | 12 | 3.2 | 1.67 | 2.84 | 0/3 |
| 2 | 16 | 3.2 | 1.95 | 2.77 | 0/3 |

**Stalls:** **4 of 9 strong-sync settings stalled** (a majority of seeds). The curvature floor blocked 10,000 births in a row. Cheap links plus high caps stall most. That's also why several strong-sync jobs finished fast: they stopped early.

## What it means

- **Stronger sync doesn't rescue M2.** Where it grows, the pattern is rough and about 1.2–2-dimensional (walk dimension about 2.4–2.8, fractal-like). Where links are cheap and caps high, growth stalls.
- **Across both sync strengths, three conditions give three results:**
  - a tight floor gives a ring;
  - a loose floor gives a rough, low-dimensional tangle, or a stall;
  - no floor gives a small world.
- **This fits notes 15 and 16:** M2 grows space without time order, and without causality (no branching of space) the known outcomes are exactly rough, crumpled or stuck geometries.
- **So M2's result is a test of space-without-time, and it comes out as expected.** It doesn't count against ED's picture that includes time order, which hasn't been modelled yet.
- **Inputs supplied:** still 3.

## Next

**Take stock and conclude attempt 6.** The model that adds time order (no branching of space, slice dimension from sync and commitment) is the natural opening road for attempt 7.
