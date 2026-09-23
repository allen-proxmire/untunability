# Rule version 1: results

*Run 2026-09-13. Full output: `results_v1_run1.txt`. Spec and frozen predictions: [Spec.md](Spec.md). Ledger: C126–C130.*

## Summary

| test | what it checks | result | predicted |
|---|---|---|---|
| **U1** | Meetings conserve the amount | **Pass** (change 0) | Pass |
| **L1** | No spontaneous draws: a lone pattern never draws (RD26) | **Pass** (0 draws in 200 steps) | Pass |
| **M1, M2** | No left–right preference, including through meetings and a detector (T2) | **Pass** (errors ≤ 2.2 × 10⁻¹⁷) | Pass |
| **E1** | A partial mark gives partial fringes: V = \|overlap\| × V0 | **Pass** (error ≤ 3.3 × 10⁻¹⁶) | Pass |
| **E2** | Englert's D² + V² ≤ 1 | **Pass.** It reaches 1 only for the full mark | Pass |
| **E3** | A detector drawing the marker doesn't change the system's statistics (no signalling) | **Pass** (≤ 5.6 × 10⁻¹⁷) | Pass |
| **E4** | The rule's sampled draw matches the exact average | **Pass** (0.0004 over 20,000 samples) | Pass |
| **F0–F3** | Eraser: no fringes overall, fringes return when sorted, sorted screens add back up | **Pass**. Best sorted V 0.945, equal to the unmarked best | Pass (F2 medium confidence) |
| **G1** | A meeting that marks both paths alike removes nothing | **Pass** | Pass |
| **G2** | A mark undone before any draw: fringes come back exactly | **Pass** | Pass |
| **G3** | "Undoing" after a draw: no fringes | **Pass** | Pass |

**Every prediction written before the run came out as predicted. No changes were made after freezing.**

---

## Findings, in plain words

### 1. Partial marks give partial fringes, exactly as experiments show (C127)
The marker was set to tell the two paths apart by different amounts, from not at all to completely.

| how well the mark tells the paths apart (D) | 0 | 0.52 | 0.87 | 0.99 | 1 |
|---|---|---|---|---|---|
| **fringe visibility (V)** | 0.945 | 0.807 | 0.473 | 0.139 | 0 |

The fringes fade smoothly as the mark gets clearer, following Englert's rule. It was not programmed in; it comes out of "meetings hinge" plus the local draw.

**A detector drawing the marker changes nothing about the system's own statistics.** The draw happening elsewhere is invisible from here, as Fact 3 in [Interaction.md](../Interaction.md) said.

### 2. The eraser works, and nothing is undone (C128)
- **With a full mark, the system shows no fringes at all.**
- **Sorted by where the marker was drawn, some groups show full-strength fringes.**
- **Adding the sorted groups back together gives exactly the no-fringe screen.**

So "erasing" is sorting records after the draws. No commitment is taken back (D1).

### 3. "Can't be brought back" in miniature (C129)
- **Before any draw, a mark can be undone.** Repeating the lane swap removes the mark, and the fringes come back exactly. This is the entangle-then-disentangle seen with colliding atoms (C107).
- **After a draw, the same undo step brings nothing back.** Once the marker has been drawn, the system is on one path in each outcome, and there is no coherence left to restore.

That is RD28 on a small scale: the draw is what makes a mark permanent.

### 4. The honest bottom line (C130)
Version 1 reproduces standard quantum physics for marks, erasers and reversible hinging, with no free numbers.

- **That is a requirement met, not evidence for ED (Rule 4).**
- **For measurement, ED currently says nothing standard physics doesn't.**
- **G3 is close to automatic:** once the detector draws, the result follows. The detector itself is a model of "can't be brought back", not a derivation of it (G36).

## Limits (from the spec)

- **V1-L1:** the detector stands in for "can't be brought back" (G36).
- **V1-L2:** which interaction happens at a meeting is a test input.
- **V1-L3:** the marker lives on its own ring. A meeting is not yet two patterns arriving at the same locus of one graph.
- **V1-L4:** everything carried over from version 0, including that the budget doesn't yet slow spreading.
