# C2a results: the balance from ED's budget

*ED_Attempt_07, note 7. 2026-09-16 (RD9). Ledger: C16–C18. Run `model/c2a_run.py`, 17 minutes; follow-up `model/c2a_telescoped_diagnostic.py`.*

## Run 1, as pre-registered (C16)

| | expected | result | |
|---|---|---|---|
| **E1** structure and budget | exact / conserved in every run | exact; budget conserved in every run | **As expected** |
| **E2** reading B balance (k = 0.5, 1, 1.5; L\* = 100, 200) | ≥ 19/20 survive; median mean offspring in [0.98, 1.02]; median slice length within ±10% of L\* | **all 20/20 survived** in every setting; **slice lengths 99.8–105.6% of L\*;** mean offspring **1.009–1.116**, over 1.02 in three of the six settings | **Not as expected** (offspring measure only) |
| **E3** reading B, k = 2.5 | fails E2 in a majority | slices hover about **40% above L\*** in every seed (no runaway, no extinction) | **As expected** |
| **E4** reading A | majority die or run away | **all 40 seeds ran away** | **As expected** |
| **E5** geometry (k = 0.5, 1, 1.5) | d_H in [1.7, 2.3], d_s ≤ 2.3 | medians **d_H 2.11, d_s 2.00, d_w 2.20;** structure exact | **As expected** |

**Exit, by the rule as written: "Balance put in (E2 not met)."** That verdict stands as the pre-registered outcome.

## Why E2 missed: Allen's prime-triangle point (C17)

- **E2's offspring measure was the average of each slice's growth ratio,** L_{t+1}/L_t. Averages of ratios are biased upward by random swings: a step up 10% then down 10% leaves you 1% lower (1.1 × 0.9 = 0.99), while the two ratios average exactly 1.
- **Allen connected this to his Prime-Triangle angle** (`Primes/2_One_Wheel_Many_Shadows/PG_Angle_Wobble.md`):
  - the angle is, to first order, 45° − (90/π)·ln(p_{n+1}/p_n), **a log-ratio of consecutive terms;**
  - its changes **telescope,** summing to (last − first), so the ups and downs cancel at any window length, and the leftover depends only on where you stop.
- **The same coordinates fix C2a.** Measure growth as a log-ratio and it telescopes: the average offspring becomes exp[(ln L_last − ln L_first) / steps], equivalent here to total next-slice events over total current-slice events.

**Follow-up diagnostic (not pre-registered), same settings and seeds:**

| reading B | average of ratios (E2 as run) | **telescoped** | ratio of sums |
|---|---|---|---|
| k = 0.5, L\* = 100 | 1.0174 | **0.9993** | 0.9993 |
| k = 0.5, L\* = 200 | 1.0089 | **0.9999** | 0.9999 |
| k = 1, L\* = 100 | 1.0395 | **0.9999** | 0.9999 |
| k = 1, L\* = 200 | 1.0196 | **1.0001** | 1.0001 |
| k = 1.5, L\* = 100 | 1.1157 | **1.0003** | 1.0003 |
| k = 1.5, L\* = 200 | 1.0593 | **1.0002** | 1.0001 |
| k = 2.5, L\* = 100 | 1.3825 | 0.9991 | 0.9991 |
| k = 2.5, L\* = 200 | 1.1708 | 1.0010 | 1.0009 |

**Measured without the ratio bias, the offspring average is 1 to within 0.001 in every setting.** The miss came from the statistic, not the balance.

At k = 2.5 the telescoped average is also about 1, but slices sit 40% above L\*. So k = 2.5 still fails on slice size, as E3 expected: it settles at the wrong size rather than running away.

## What it means (C18)

- **Reading B holds the balance:**
  - every seed survived;
  - slice size stays at L\* (within 6% for k up to 1.5);
  - the telescoped offspring average is 1.000;
  - the geometry still reads as two-dimensional (d_H 2.11, d_s 2.00).
- **No one tuned the average to 1;** it comes out of budget passed forward and conserved.
- **The naive reading ran away every time,** confirming the sign check.
- **The pre-registered verdict is "balance put in,"** because the offspring check used a biased average. **With the telescoped measure, every E2 condition is met.**
- **Adopting the telescoped measure is a revise-and-retest decision for Allen.** If adopted, the recorded result becomes:
  > "The balance self-organizes from ED's budget passed forward and conserved: consistent, not derived; k and L\* are knobs; space settles as a fixed-size tube, and growth would need budget creation (the cosmic excess, inherited)."
- **Inputs:** unchanged (still 3).

## Options (Allen decides)

| | option |
|---|---|
| **(a)** | **Adopt the telescoped offspring measure** as E2's check (recorded as revise-and-retest, with Allen's prime-triangle reason) and record the balance as self-organizing. Then C2 part 2: slice dimension |
| **(b)** | **Keep "balance put in"** and go on to slice dimension with the balance as an input |

## Allen's decision and the fresh-seed retest (C19, C31)

**Allen chose (a)** (D9): the telescoped measure is now E2's check. The retest ran on **fresh seeds** (balance seeds 20–39, geometry seeds 103–105) with the same rule, settings and exit rule. Expected results were written in `model/c2a_run2.py` before running (D10).

| | result | |
|---|---|---|
| **E1** | Structure exact; budget conserved in every run | **As expected** |
| **E2** reading B, k = 0.5, 1, 1.5 | All 20/20 survived in every setting; **telescoped offspring 0.9998–1.0006;** slice lengths 98.5–105.0% of L\* | **As expected** |
| **E3** k = 2.5 | Slices about 39–40% above L\* (2 of 20 died at L\* = 100) | **As expected** |
| **E4** reading A | 40 of 40 ran away | **As expected** |
| **E5** geometry | Structure exact; medians **d_H 2.105, d_s 1.987, d_w 2.199** | **As expected** |

**Exit: PASS, revised check confirmed on fresh seeds.** Recorded:
> **"The balance self-organizes from ED's budget passed forward and conserved: consistent, not derived; k and L\* are knobs; space settles as a fixed-size tube, and growth would need budget creation (the cosmic excess, inherited)."**
