# Rule version 1: test spec

*Written 2026-09-13, before any test was run. Frozen once `run_tests_v1.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun.*

## What version 1 is

Version 0 plus the decisions made since. The code is in `rule_v1.py`, which reuses version 0's spreading, mirror, budget and local draw.

| piece | version 1 | ledger |
|---|---|---|
| Spontaneous draws | **None.** The "too thin" trigger is gone | RD26 |
| Two patterns meeting | **Hinge.** `meet` is a linear step on two parts that conserves the amount. It never draws | RD27 |
| When a draw happens | **Only where a mark can't be brought back.** Version 1 models this with a detector: a part that reaches a detector is always drawn | RD28 (model), G36 (open) |
| What a draw fixes | Only the part that is drawn. The other part keeps its conditional pattern | RD22 |
| Spreading, coin, mirror, budget, clock ticks | Unchanged from version 0 | RD13, RD14, RD16, RD18, V0-D1 |

**Two ideas used in the tests:**
- **The marker** is a second part, on its own ring, that records a meeting.
- **A mark** is a change to the marker that depends on where the system was. How well the mark tells the paths apart is D = √(1 − |overlap|²), where the overlap is between the marker's two possible patterns (Englert, C110).

## Limitations of version 1 (stated before running)

- **V1-L1. The detector stands in for "a mark that can't be brought back".** The general meaning is open (G36).
- **V1-L2. Which interaction happens at a meeting is a test input,** here swapping Left and Right lanes, or one spreading step. The rule says only that meetings are linear, conserve the amount and never draw. This is like version 0 taking masses as inputs.
- **V1-L3. The marker lives on its own ring.** A meeting is the step "where the system is at locus x, change the marker". It is not yet two patterns arriving at the same locus of one graph. That is left for version 2.
- **V1-L4. Carried over from version 0:**
  - the budget doesn't slow spreading (V0-L1);
  - fixed masses;
  - no P12;
  - 1D and no units;
  - no motion-dependent clock ticks;
  - no locus birth;
  - the Grover coin (V0-D1).

**What these tests can and can't show.** They check that version 1 reproduces known quantum results for marks, erasers and reversible hinging. **Passing is a requirement met, not evidence for ED (Rule 4).** A failure would be a real finding.

---

## Setup shared by tests E, F and G

- **The system ring:** 31 loci. The system starts on two paths, locus 13 and locus 17, in the Internal channel, with amplitudes 1/√2 and e^{iφ}/√2.
- **The marker ring:** 8 loci.
- **Order of events:**
  1. The meeting happens at locus 13, on path 1 only.
  2. Anything else the test specifies: marker steps, a detector, a second meeting.
  3. The system spreads for 8 steps and lands on the screen.
- **The screen:** the system's share at each locus, for φ = 0, π/2 and π. It has the form a + Re(c e^{iφ}), so the visibility at each locus is V = |c|/a, wherever a > 10⁻⁹.
- **V0** is the visibility with no meeting at all.
- **Marker patterns:**
  - m_θ = cos θ at (locus 0, Internal) + sin θ at (locus 0, Left). Swapping lanes gives an overlap of cos²θ.
  - Two random marker patterns, with one spreading step as the interaction.

---

## Tests and frozen predictions

### Test U1: meetings conserve the amount (code)
Random system and marker patterns; interactions: lane swap and a spreading step; meeting loci 0, 5 and 30.

**Pass if** the total amount changes by less than 10⁻¹².

### Test L1: no spontaneous draws (code, RD26)
A lone pattern runs through 200 spreading events with the rule's event runner.

**Pass if** there are 0 draws and the pattern equals 200 plain version 0 spreading steps, to 10⁻¹².

### Test M: mirror check (code, T2)
Random system and marker; a lane-swap meeting at locus 9; 5 steps of each part; then a spreading-step meeting at locus 9. Separately, the same from the mirror images, with the meeting at the mirrored locus.

**Pass if:**
- **M1:** the final joint patterns match their mirror images to 10⁻¹².
- **M2:** the system's screen, averaged over detector outcomes on the marker, matches its mirror image to 10⁻¹².

### Test E: a partial mark gives partial fringes (Chapman C109, Englert C110; RD27)
**Cases:**
- m_θ for θ = 0, π/8, π/4, 3π/8, π/2, with the lane-swap meeting;
- the two random markers, with the spreading-step meeting.

**Pass if:**
- **E1:** V = |overlap| × V0 at every locus, to 10⁻¹⁰.
- **E2:** D² + V² ≤ 1 + 10⁻¹² at every locus, in every case.
- **E3:** a detector drawing the marker right after the meeting leaves the system's average screen unchanged, to 10⁻¹² (no signalling).
- **E4 (code):** the rule's sampled draw, over 20,000 samples (θ = π/4, φ = 0), reproduces the exact average screen to within 0.02.

### Test F: eraser (C111; RD22, D1)
m_θ with θ = π/2, so the two marks are fully distinguishing. After the lane-swap meeting, the marker spreads 3 steps, then a detector draws it.

**Pass if:**
- **F0 (code):** the list of detector outcomes and their probabilities is the same for all three φ, to 10⁻¹².
- **F1:** the system's average screen shows no fringes: V < 10⁻¹² at every locus.
- **F2:** sorted by detector outcome, at least one outcome with probability above 0.01 shows fringes with a largest V above 0.5 × (largest V0).
- **F3:** the probability-weighted sum of the sorted screens equals the screen with no detector at all, to 10⁻¹². Sorting brings fringes back; nothing is undone.

### Test G: meetings without a mark, and marks that can or can't be brought back (C107; RD27, RD28)
- **G1.** A random marker meets both paths with the same spreading step, so the meeting leaves no distinguishing mark.
  - **Pass if** V = V0 at every locus, to 10⁻¹⁰, both without and with a detector drawing the marker.
- **G2. Brought back before a draw.** The θ = π/2 marker meets path 1 with a lane swap (a full mark), then meets it again with a lane swap, which undoes it. No detector.
  - **Pass if** V = V0 at every locus, to 10⁻¹².
- **G3. Can't be brought back after a draw.** The same, but a detector draws the marker between the two meetings.
  - **Pass if** the average V < 10⁻¹² at every locus.

### Claude's predictions (2026-09-13, before running)

| test | prediction | confidence |
|---|---|---|
| U1, L1, M1, M2 | Pass | High. The meeting applies a conserving step to separate branches, nothing in version 1 draws on its own, and both interactions treat Left and Right alike |
| E1 | Pass | High. For a marker in a definite pattern, the fringe term is multiplied by the overlap; that is the standard result |
| E2 | Pass | High. It follows from E1 and V0 ≤ 1 |
| E3 | Pass | High. It is the same reason version 0's local draw passed no-signalling |
| E4, F0 | Pass | High |
| F1 | Pass | High. Orthogonal marks remove the fringe term entirely |
| F2 | Pass | **Medium.** It depends on how much the marker's Left and Right contributions overlap after 3 steps with the Grover coin |
| F3 | Pass | High |
| G1, G2 | Pass | High |
| G3 | Pass | High. After the draw, each outcome leaves the system on one path only, so a second meeting has no coherence to restore |

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

*(none yet)*
