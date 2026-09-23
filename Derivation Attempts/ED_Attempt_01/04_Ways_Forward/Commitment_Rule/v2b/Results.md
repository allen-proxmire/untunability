# Rule version 2b: results

*Run 1, 2026-09-14 (`results_v2b_run1.txt`). Spec and predictions frozen before running: [Spec.md](Spec.md). Ledger: C278–C280, G50.*

## What was tested

**The model:** version 2, plus two additions.
- **An arrow in the phases.** Lane hops carry opposite phases set by the size of the local flow. A constant phase was also run and reported.
- **Draws that carry the mark away.** A drawn lane part drops into the committed locus's Internal channel, so its motion goes into committed matter.

**The question:** can a lasting handed flow now form from noise?

## Results

| test | prediction | result |
|---|---|---|
| **B1 code and mirror check** | Mirror to 10⁻⁹ | **Wrong:** 1.45 × 10⁻⁴. Not a bug (see below) |
| **B2 the draws no longer only mix** | Purity rises somewhere | **Right.** Purity settled at 0.057–0.12, not the fully mixed 0.007 |
| **B3 no phases: no winding** | 0 | **Right** |
| **B4 symmetric draw rates: flow dies** | \|J\| < 10⁻³ | **Right** |
| **B5 no phases: flow dies** | \|J\| < 10⁻³ | **Right** |
| **B6a–d a lasting handed flow for one sign of the feedback** | Low confidence | **Wrong.** 0 of 10 for either sign; every flow ended below 2.1 × 10⁻⁵ |
| **Reported: constant phase 0.4** | — | Also no lasting flow; winding 0 |

**The mirror mismatch (C279).**
- **The code is symmetric:** after one step the mirrored runs agree to 10⁻¹⁸.
- **The mismatch grows only when the phases follow the flow's size,** because that law has a sharp kink at zero flow, which amplifies rounding. It levels off around 10⁻⁴ to 10⁻³, below the test thresholds.

## What it means (C280)

**Even with both additions, ED's rule doesn't hold a flow.**
- **Flow-set phases never switched on:** noise-sized flows set almost no phase.
- **A constant phase didn't help either.**

**So the mechanism the toys showed (C263) doesn't appear in ED's rule with these additions, at these settings.**

**What this run can't tell apart:**
- the loop is too weak at these settings; or
- ED's rule can't do it at all.

## Gain check (G50 = a, RD48; `gain_check.py`, run 2)

**The question:** hold the phase and a small Right/Left draw-rate difference fixed, and solve exactly for the steady flow. Does ED's rule push back hard enough for the loop to amplify itself?

**Results (C281, C282).**
- **With a phase:** a single, clean steady state in all 27 settings.
  - **Response χ:** from 0.012 to 0.096 (largest at phase 0.8, Γ 0.3, every 2nd locus committed).
  - **Symmetries:** exactly odd in the rate difference and in the phase, and linear.
  - **Sign:** it flips with phase and spacing, so which feedback sign amplifies depends on the settings.
- **With no phase:** 13 steady states, every one with zero flow. The exact solve can't pick one, so those rows were junk. Three predictions (G1, G2, G4) failed on my assumption of a single steady state, not on the physics.
- **Version 2b's loop gain was 0.32,** below 1. That's why its flows died.
- **Score:** G3, G5–G8 right; G1, G2, G4 wrong.

**What it means (C283).** The door isn't shut. A hand can start from noise in this rule if all three hold:
1. **A standing phase.** A phase set by the flow is zero when there's no flow, so it can never start a hand. The arrow of time would have to be a standing phase.
2. **Draws that carry motion off** (non-unital).
3. **A steep enough rate law:** V0 < \|g\| \|χ\|, at most about 0.1 on this grid (about 0.03 at 2b's settings with g = 0.9).

Each is a free setting. A lasting hand under them would show the rule *can* do it, not that ED *predicts* it.

## Tuned dynamic test (G51 = c, RD49; `tuned_test.py`, run 1)

**Labelled as tuned.** The settings were picked from the gain check to make the loop amplify:
- **a standing phase** 0.8;
- **draws** at every 2nd locus, rate 0.3, carrying motion into Internal;
- **a steep rate law,** V0 = 0.03, with feedback g = ±0.9;
- **a ring of 24.**

**All eight frozen predictions right (C288).**

| | result |
|---|---|
| **Loop gain on this ring** | 3.0 (response 0.101, close to the big ring's 0.096) |
| **Mirror check** | 10⁻¹⁸ after one step, 10⁻¹⁷ at t = 20 |
| **g = +0.9 (amplifying)** | **All 10 runs held a lasting flow,** \|J\| ≈ 0.11. **6 went one way, 4 the other.** The draw rates were fully lopsided (0.997), and **the winding was nonzero in all 10** |
| **g = −0.9 (damping)** | All 10 died (below 5 × 10⁻⁷) |
| **Control, gentler rate law (gain 0.45)** | All 5 died (below 4 × 10⁻¹⁰) |

**Caveats.**
- **The flow was still creeping up** (0.100 at t = 200, 0.114 at t = 600), so the state may not be fully settled.
- **Only the size of the winding was recorded,** not its sign.

**What it means (C289).**
- **ED's rule can hold a handed state** that its own mirror-symmetric rules don't contain. The hand is picked by chance, and it has the winding the handedness theorem measures.
- **It needs three things together,** all set by us:
  - a standing phase (an arrow of time in the phases);
  - draws that carry motion off;
  - a rate law steeper than the loop's threshold.
- **So it shows the rule *can* be handed, not that ED *predicts* it.**
- **The draw here is the loose model** that RD50 now replaces. The result has to be re-checked with the rebuilt draw.

## Limits

- **1D, mean-field, U = 0, fixed committed loci.**
- **One set of settings** (Γ = 1, D = 3, V0 = 0.05, θ0 = 0.4, g = ±0.5).
- **The draw is still a model** (G36, D17).
