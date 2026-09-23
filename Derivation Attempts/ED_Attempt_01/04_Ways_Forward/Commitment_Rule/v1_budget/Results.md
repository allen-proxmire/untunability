# The budget slows spreading: results

*Run 2026-09-13. First run: `results_budget_run1.txt`. Second run, with the follow-up tests added after the first: `results_budget_run2.txt`. Spec and frozen predictions: [Spec.md](Spec.md). Ledger: C192–C194.*

## Summary

| test | what it checks | result | predicted |
|---|---|---|---|
| **H1–H4** | The slowed generator is Hermitian, reduces to the unslowed one where U = 0, conserves the amount, and has no left–right preference | **Pass** (errors ≤ 1.4 × 10⁻¹⁴) | Pass |
| **S1** | Uniform slowing is exactly the same as running slower | **Pass** (1.3 × 10⁻¹⁴) | Pass |
| **F0** | No mass, no drift | **Pass** | Pass |
| **F1** | A pattern with positive commitment moves toward the mass | **Pass** (+0.0021) | Pass |
| **F2** | A pattern with negative commitment moves away | **Fail: it also moved toward the mass** (+0.0075) | Pass: **wrong prediction** |
| **F3** | The drift doubles when the budget doubles | **Pass** (ratio 2.03) | Pass |
| **F4** | The rest-term potential alone | **Moved away** (−0.0028) | Toward: **wrong** |
| **K1** *(follow-up)* | Slowing spreading only (m = 0) | **+0.0048, toward** | +0.0049, toward: right |
| **E1** *(follow-up)* | Massive-like start, potential only | **+0.063, toward** | Toward: right |
| **E2** *(follow-up)* | Massive-like start, slowed, m = +4 | **+0.079, toward**, more than E1 | Toward and more: right |
| **E3** *(follow-up)* | Massive-like start, slowed, m = −4 | **−0.048, away** | Not predicted |

## What it means, in plain words

**Slowing everything at a place has two separate effects.**

1. **Patterns linger where things are slow.**
   - Spreading is slower near the mass, so a pattern's bandwidth builds up there. Its centre moves toward the mass whatever the sign of its commitment (K1).
   - It's like light bending toward glass, where it travels slower.
2. **Slowing the rest term acts like gravity's pull.**
   - For a **massive-like pattern** it pulls toward the mass when commitment is positive (E1, E2) and pushes away when negative (E3). This is **Newtonian gravity's direction**, and it depends on commitment amounts being positive (D7).
   - The effect is **about 30 times stronger** than the lingering effect.

**Why my F2 and F4 predictions were wrong.**
- I reasoned from the pull alone.
- The starting pattern (all in the Internal lane) turned out to be mostly **light-like**. Light-like patterns respond mainly to lingering, and the pull acts on them backwards.
- A pattern started in the massive-like lane combination behaves the way I expected.

**What it's worth.** This is how gravitational time dilation acts on energy in standard physics, so it's a requirement met, not evidence for ED.

## The problem it exposes: light bends only half as much (G37)

- **"The budget slows everything at a place by one factor"** (RD16) is a *time-only* effect. Measured light bending needs a *space* effect of the same size as well (C195, C196).
- **Time-only slowing gives half** of the observed bending of starlight by the Sun, the value Soldner and Einstein (1911) found.
- **The Cassini spacecraft measured the full value** to about 1 part in 100,000.
- **So RD16, as the whole story, is ruled out.** See [../../Budget_Spreading.md](../../Budget_Spreading.md).

## RD35: ticking slows by s, moving between loci by s² (run 3, 2026-09-14)

*Output: `results_budget_run3.txt`. Predictions were written in Spec.md before running. Ledger: C199.*

| test | result | predicted |
|---|---|---|
| **M1** construction checks | **Pass** (asymmetry 0, U = 0 exact, amount 2.2 × 10⁻¹⁶, mirror 1.1 × 10⁻¹⁴) | Pass |
| **M2** hops only, uniform U = 0.3: slowed at t equals unslowed at 0.49 t | **Pass** (1.8 × 10⁻¹⁵) | Pass |
| **M3** lingering only (Internal start, no rest term) | **−0.0020, slightly away** | Toward, 1.5–2.5 × K1: **wrong** |
| **M4** massive-like, positive commitment | **+0.078, toward: 0.99 × E2** | Within 15% of E2: right |
| **M5** massive-like, negative commitment | **−0.048, away** | Away: right |

**In plain words:**
- **Moving now slows exactly twice as much as ticking (M2).** Light-like patterns cross a region of used budget at about s² of their normal speed. That is an effective refractive index of about 1 + 2U, the measured value.
- **Falling is unchanged (M4, M5).** It comes from the slowed rest term, which RD35 doesn't touch.
- **My M3 prediction was wrong.** I assumed the 1D "lingering" drift would double. But with no rest term, the lane mixing (still slowed by s) acts like a potential with both signs, and it isn't separate from lingering. A pattern's centre drifting in 1D turns out to be a poor stand-in for light bending, which needs 2D. The bending factor follows from M2 directly.

## Limits

- **1D only.** Bending itself can't happen here, which is why the light-bending point is argued, not simulated.
- **No units:** only direction and proportion are tested.
- **Fixed test profile for U, not the q = 1 steady state.**
- **The continuous-time generator stands in** for version 0's discrete step.
