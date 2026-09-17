# C1 results: the causal half checked

*ED_Attempt_07, note 4. 2026-09-16 (RD5). Ledger: C8. Run `model/c1_run.py`, 25 minutes; outputs `model/c1_run1.txt`, `.json`, `.log`.*

## Verdict

> **PASS. C1: ED's causal growth with no splitting reproduces 2D CDT: the causal half checked.**

**Every expected result, written before the run, was met.**

## Results

| | expected | result | |
|---|---|---|---|
| **F0 flat strip** (calibration, 40,000 events) | d_H and d_s in [1.7, 2.3], d_w in [1.8, 2.2] | d_H 1.90, d_s 1.88, **d_w 2.07** | As expected |
| **E1 structure** | exact in every run | **exact in all 10**: one circle per slice, links only one slice forward, forward-link counts adding up, parent links one tree | As expected |
| **E2 slice length** (1,000 seeds) | slope in [1.8, 2.2] | **slope 2.05**; mean length 102.6, 203.2, 413.9 at t = 50, 100, 199 (theory 101, 201, 399) | As expected |
| **E3 mass dimension** (median of 10) | [1.7, 2.3] | **2.17** (range 2.11–2.20) | As expected |
| **E4 walk-return dimension** (median of 10) | ≤ 2.3 | **1.89** (range 1.74–1.95) | As expected |
| **E5 walk dimension** (median, reported) | ≥ 1.8 | **2.41** (range 2.38–2.65) | As expected |

**Sizes:** the ten trees had 15,819 to 65,546 events.

## What it means

- **ED's time order plus "space doesn't split" gives honest two-dimensional geometry,** exactly as 2D causal dynamical triangulations do.
  - Space grows as one circle at the rate the tree theory gives.
  - The pattern reads as two-dimensional.
  - Its walk-return dimension sits just under 2, as the literature says.
- **The causal machinery works in ED's terms,** and the readings handle this kind of pattern. That's what C1 was for.
- **Walk dimension is about 2.4,** above the flat strip's 2.07. That fits a walk-return dimension slightly under 2 with mass dimension about 2.2. It's recorded, not scored.
- **Put in, as planned:**
  - slice dimension (a circle, by design);
  - the critical balance (offspring averaging exactly 1).
- **This is a machinery check, not new physics.** Inputs supplied are unchanged (still 3).

## Next

**C2.** Two questions, on paper first:
1. **The balance:** what, in ED, keeps space from growing or shrinking on average? C1 put this in. The candidate from attempt 6 is commitment's cost against sync's pull.
2. **Slice dimension:** with nothing built in, do sync and commitment make slices settle at three dimensions instead of a given circle?
