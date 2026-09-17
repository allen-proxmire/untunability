# The C1 model: specification (on paper)

*ED_Attempt_07, note 3. 2026-09-16 (RD3). Ledger: C6–C7. **A specification only: no code written, nothing run.** The rule, expected results and exit rule were fixed in note 2 and accepted (D3). This note fixes the build, sizes, readings and running order. **Running is a separate yes.***

## Accepted in note 2 (C6)

**Allen accepted C1-Q1–C1-Q4 and the exit rule** (D3):
- slices are given as circles;
- forward links go to a run of consecutive next-slice events, neighbours sharing exactly one;
- offspring average exactly 1, with a surviving spine;
- no fixed cap on links.

## The build

**Growth, slice by slice** (Kesten's tree with cyclic order):

| step | rule |
|---|---|
| **Slice 0** | One event (the root, on the spine) |
| **Offspring** | Each ordinary event: c children with chance (1/2)^(c+1), so c = 0, 1, 2, … average 1. The spine event: c children with chance c·(1/2)^(c+1) (size-biased, c ≥ 1); one of its children, picked uniformly, carries the spine |
| **Order within a slice** | Children appear in slice t+1 in the order of their parents around slice t, and in birth order within a parent. **So slice t+1 is one circle, in the same cyclic order** |
| **Links within a slice** | Each event links to its two neighbours around the circle. A slice of 2 events has one link; a slice of 1 has none |
| **Forward links** | The event at position i of slice t, whose children start at position s_i in slice t+1, links forward to positions s_i, s_i+1, …, s_i+c_i (c_i + 1 events, cyclic). Neighbouring events share exactly one |

**The spacetime pattern for readings:** all events, with all in-slice and forward links, taken as undirected, with duplicate links in very small slices merged.

## Sizes and seeds

| part | what | size |
|---|---|---|
| **Slice-length check** | Tree only, no readings | **1,000 seeds**, 200 slices each |
| **Readings** | Full spacetime pattern | **10 seeds** (0–9), 200 slices each: about 40,000 events on average, varying a lot by seed |
| **Flat calibration** | Every event exactly one child: slices stay the same length, a regular triangulated strip | 200 events per slice × 200 slices = 40,000 events |

**Why so many seeds for slice length:** each run's slice length spreads widely. For this tree its standard deviation at time t is about 1.4·t. The mean over 1,000 runs pins the slope to about ±0.1, enough to test [1.8, 2.2].

## Readings (fixed before code)

| | reading | procedure |
|---|---|---|
| **S1** | Slice length | Mean L_t over the 1,000 tree-only seeds; least-squares slope of mean L_t against t for t = 10…200 |
| **S2** | Structure (every run) | For each slice with 3 or more events: its in-slice links form exactly one cycle. Every forward link joins slice t to slice t+1. **Forward links out of slice t (counted before merging duplicates) = L_{t+1} + L_t.** Parent links number (events − 1) and connect everything: one tree |
| **R1–R5** | Dimensions | **A6 readings v2, copied unchanged** (A6 C70: 6 of 6 calibrations): mass dimension d_H, ball-cut β, walk-return d_s, walk dimension d_w, consistency R5 |

## Expected results, written down before any code

| | expected | grounds |
|---|---|---|
| **F0** (flat calibration) | d_H and d_s in [1.7, 2.3], d_w in [1.8, 2.2] | A regular 2D strip; A6's 2D calibration class |
| **E1** (structure) | Exact in every run, every slice | By construction (C3) |
| **E2** (slice length) | Slope in [1.8, 2.2] | 1 + 2t (C4) |
| **E3** (mass dimension) | Median over the 10 seeds in [1.7, 2.3] | Exactly 2 (C2) |
| **E4** (walk-return dimension) | Median over the 10 seeds ≤ 2.3 | At most 2 (C2) |
| **E5** (walk dimension) | Reported; median ≥ 1.8 | 2·d_H/d_s (C4) |

## Exit rule (from note 2, confirmed D3)

| | outcome | recorded as |
|---|---|---|
| **Pass** | E1 exact, E2, E3, E4 met (F0 met) | "**C1: ED's causal growth with no splitting reproduces 2D CDT: the causal half checked.**" Go to C2 |
| **E1 fails** | Code bug | Fix it (recorded), rerun |
| **F0 fails** | Readings don't suit this pattern type | Fix the readings for it (recorded), rerun the calibration, then the tree |
| **F0 passes, E2–E4 miss** | — | "**C1 not reproduced.**" Look at why (for example, edge effects of a growing cone); record it |
| **The growth rule** | — | **Not changed after seeing results** |

## Running order (when Allen says run)

1. **Timing first:** readings on the flat strip and on one tree seed, timing only. Then a plan estimate from those numbers, **including every reading.**
2. **Flat calibration** (F0).
3. **Tree-only slice-length runs** (E2).
4. **Ten tree seeds with readings** (E1, E3–E5).

**Estimate:** minutes to perhaps an hour. It runs in `ED_Attempt_07/model/`, with each run saving its own result.

## Implementation choices (recorded now, before code)

- **Readings:** `readings.py` and `readings_v2.py` are copied from `ED_Attempt_06/model/` unchanged, with file hashes recorded.
- **Seeds:**
  - tree seed s draws offspring from its own random stream;
  - reading centres use seed 1,000 + s;
  - the flat strip uses centre seed 999.
- **Spine child choice:** uniform among the spine event's children.
- **Duplicates:** merged for readings; the structure count (S2) is taken before merging.

## Next step

**Say run,** and I'll write the code and IMPLEMENTATION_NOTES, time the readings, then run the calibration, the slice-length check and the ten seeds, in that order.
