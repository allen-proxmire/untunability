# Rule version 4: the tuned hand on the rebuilt draw

*Written 2026-09-14, before any test was run. Frozen once `run_tests_v4.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun. RD51; follows C288 (tuned test) and C291 (rebuilt draw).*

## What version 4 is

**The idea.** In the rebuilt draw (RD50), a draw fixes only a record; carrying motion off is part of what a meeting does. So version 4 puts the tuned test's "draws carry motion off" where it belongs:
- **A transfer meeting.** Where a pattern is in the Right or Left lane at a committed locus x, part of it moves into x's Internal channel.
- **The record.** Committed matter records that the transfer happened, in R identical fragments.
- **The draw (rebuilt rule).** Once R ≥ R* = 3, the record is fixed: transferred or not. Nothing else is fixed.

**Per step of length dt.**
- **Spreading:** exp(−iH dt), with the tuned test's standing phase.
- **Meetings:** a transfer meeting at each committed lane channel, with transfer probability p = γ dt.
- **Rates:** γ comes from version 2b's flow feedback (population velocity at that moment).

**Two descriptions of the same thing.**
- **Explicit:** the pattern plus its records, with draws branching. For small rings only. The R fragments of one record are always all unmarked or all marked, so they're stored as one two-level record carrying its count R (exact for this meeting type).
- **Population:** the one-pattern density matrix, spread by exp(−iH dt), then the map K0 = 1 − (1 − √(1 − p)) P_a and K1 = √p \|x, Internal⟩⟨x, K\| for each committed lane channel a = (x, K).

## Analysis before running

**A. The two descriptions agree exactly, step by step.** For one channel, the meeting and the draw give:
- the record "transferred", with probability p times the amount at a, and the pattern moved to Internal;
- the record "not", with the amount at a scaled by √(1 − p).

Averaged, that is exactly K0 and K1. Channels at different loci, and the two lanes at one locus, don't interfere, because each meeting touches only its own lane component and a fresh record.

**B. Finality doesn't change the population's behaviour.** With R < R* there is no draw, and the records stay coherent. Tracing them out gives the same density matrix as drawing them. Finality matters only for erasure (C291, D8b), not for the averaged dynamics.

**C. So the tuned hand should carry over.** The population map is the discrete-time form of version 2b's jumps with rate γ. Differences are expected only at order γ dt (about 1%).

## Limits (stated before running)

- **The transfer meeting is a choice** of meeting interaction (V1-L2), as in the tuned test.
- **Feedback and settings are the tuned ones** and stay labelled as tuned.
- **Mean-field feedback.** The rates follow the population's flow, not each pattern's.
- **1D, U = 0, fixed committed loci.**

---

## Setup

**Equivalence tests:**
- ring L = 4, every 2nd locus committed, standing phase 0.8, dt = 0.02, 3 steps;
- fixed transfer probabilities 0.20, 0.35, 0.10, 0.25 on the four committed lane channels;
- a random start (seed 404).

**Tuned tests (same settings and starts as C288):**
- L = 24, D = 2, Γ = 0.3, phase 0.8 (standing), V0 = 0.03, g = ±0.9;
- dt = 0.02, t = 600;
- 10 noisy starts (seed 1357);
- control V0 = 0.2.

## Tests and frozen predictions

| test | what | prediction | confidence |
|---|---|---|---|
| **V4-1a (code)** | The population map on a random density matrix | Trace kept to 10⁻¹², Hermitian, smallest eigenvalue ≥ −10⁻¹² | High |
| **V4-1b (code)** | Mirror check: population, g = +0.9, one step | Below 10⁻¹⁵ (t = 20 reported) | High |
| **V4-2 (analysis A)** | Explicit with R = 3 (draws) vs population map | Density matrices agree to 10⁻¹² | High |
| **V4-3 (analysis B)** | Explicit with R = 2 (no draws, records coherent) vs population map | Agree to 10⁻¹² | High |
| **V4-4** | Tuned, g = +0.9 | At least 8 of 10 runs keep \|J(600)\| > 10⁻³ | High |
| **V4-5** | Those lasting runs | \|J(600)\| between 0.10 and 0.13 | Medium-high |
| **V4-6** | Direction run by run vs the tuned test (−, −, +, +, −, −, +, +, +, +) | Agrees in at least 8 of 10 | Medium (early flows are small, so a step-size difference could flip a run) |
| **V4-7** | Lasting runs | Winding nonzero in at least half | High |
| **V4-8** | g = −0.9 (10 starts) and control V0 = 0.2 (5 starts) | All \|J(600)\| < 10⁻⁴ | High |

**What a pass would mean.**
- **The tuned hand survives the rebuilt draw,** with motion carried off by the meeting.
- **It doesn't depend on draws being final,** only on marks carrying motion into committed matter.
- **The hand still rests on the same three choices of ours** (standing phase, transfer meetings, steep response).

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

**2026-09-14, after run 1 (`results_v4_run1.txt`).** All nine predictions right.
- **Code:** map error 10⁻¹⁸; mirror 6 × 10⁻¹⁷ after one step, 1.7 × 10⁻¹⁴ at t = 20.
- **Explicit vs population:** agree to 2.8 × 10⁻¹⁶ with draws, 1.3 × 10⁻¹⁶ without.
- **g = +0.9:** 10 of 10 lasting, every \|J(600)\| = 0.114, same direction as the tuned test in 10 of 10, winding nonzero in 10 of 10.
- **g = −0.9 and control:** died (largest 4.5 × 10⁻⁷).

The exit code now also requires all nine verdicts to reproduce.
