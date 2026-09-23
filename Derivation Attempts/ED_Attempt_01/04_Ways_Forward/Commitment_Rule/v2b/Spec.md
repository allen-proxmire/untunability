# Rule version 2b: flow-set phases and draws that carry the mark away

*Written 2026-09-14, before any test was run. Frozen once `run_tests_v2b.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun.*

## What changes from version 2 (RD47, G49 = a)

| piece | version 2 | version 2b | ledger |
|---|---|---|---|
| **Spreading** | Real rule, reversible | Same, but each bond's lane hops carry a phase: Right-lane hops × e^(iθ_b), Left-lane hops × e^(−iθ_b) | P09, P11 |
| **Phase law** | none | θ_b = θ0 tanh(\|v_b\| / V0), with v_b the population's velocity across bond b (C277) | RD47 |
| **Draws** | A drawn part collapses onto its own channel and stays (unital: only mixes) | A drawn part in the Right or Left lane at a committed locus drops into that locus's **Internal** channel. The lane's motion is carried off, as if the mark left into a cold, committed environment (non-unital). Jump operators √γ \|x, Internal⟩⟨x, K⟩ for K = Right, Left | RD28 (model), G36, C276 |
| **Rate feedback** | γ[x, Right] = Γ(1 − g tanh(v_x/V0)), γ[x, Left] = Γ(1 + g tanh(v_x/V0)) | Same (no Internal-channel draw) | RD46 |

**Why the phases follow the flow's size, not its direction.**
- **A fixed phase θ keeps the rule mirror-symmetric.** The mirror (u → −u, Right ↔ Left) maps a Right-lane forward hop with e^(iθ) onto a Left-lane backward hop with e^(iθ).
- **It does break time-reversal symmetry** (the phases can't be removed). That's an arrow of time, which P11 allows.
- **A phase following the direction of the flow (θ ∝ v)** would send θ → −θ under the mirror and make the rule itself handed, which is against A1. So θ follows \|v\|.
- **The division of labour:**
  - **the phases** supply the arrow (breaking time reversal);
  - **the rate feedback** supplies any choice of hand (breaking the mirror);
  - **the non-unital draws** keep the population from simply mixing (C275).

**Mechanism expected (reasoning, not a derivation).**
- **With θ = 0:** the real rule's bands are time-reversal symmetric, so a lane's weight at wavenumber k equals its weight at −k. Draw rates that favour one lane then change nothing about the net flow.
- **With θ ≠ 0:** the Right lane's weight can tilt toward one direction of motion. Unequal Right/Left draw rates would then favour that direction.
- **The feedback loop:** if the flow produced has the same sign as the flow that set the rates, it can sustain itself; with the opposite sign of g it would die. Whether this happens, and which sign of g, isn't derived.

**Choices made here (can be revisited).**
- **Draw target:** drawn lane content drops into the same locus's Internal channel.
- **Phase law:** tanh, with θ0 = 0.4 (the contrast value of C275).
- **Timing:** the phases and rates used in a step are computed from the state at the start of that step, using the previous step's phases for the currents (a lag of one step, dt = 0.01).
- **Budget:** U = 0.
- **Reported variant:** a constant phase θ = θ0 (the arrow put directly in the phases) is run and reported, not judged.

## Limits (stated before running)

- **1D, mean-field, fixed committed loci, no units.**
- **The draw is still a model of** "a mark that can't be brought back" (G36). Where the carried-off motion goes isn't tracked; the environment has no state.
- **Phases and rates are test settings.** A pass would show the mechanism is possible in ED's rule with these two additions, not that ED requires them.

---

## Setup

- **Ring and rates:** L = 48, D = 3, Γ = 1, V0 = 0.05, θ0 = 0.4.
- **Evolution:** RK4, dt = 0.01, t = 300.
- **Noisy starts:** the same 10 as version 2 (seed 2468).
- **Measures:**
  - **total current:** J = Σ_b j_b;
  - **purity**, checked every 100 steps;
  - **winding of det(H_eff(φ) − E0),** where H_eff = H(θ) − (i/2) diag(draw rates) at the final state (300 twist steps, centroid plus 15 random E0).

## Tests and frozen predictions

| test | runs | prediction | confidence |
|---|---|---|---|
| **B1 (code)** | All runs | Amount conserved to 10⁻¹²; ρ Hermitian to 10⁻¹²; smallest eigenvalue ≥ −10⁻⁸. Mirror check (g = 0.5, θ0 = 0.4, noisy start 0, t = 20) to 10⁻⁹ | High |
| **B2** | All runs | Purity rises by more than 10⁻⁹ in at least one interval of at least one run (the draws are no longer only mixing) | High |
| **B3** | θ0 = 0, g = 0.5, noisy starts 0–4 | Final winding 0 in all (C275 analysis B) | High |
| **B4** | g = 0, θ0 = 0.4, noisy starts 0–4 | \|J(300)\| < 10⁻³ in all (symmetric rates: no hand) | Medium-high |
| **B5** | g = 0.5, θ0 = 0, noisy starts 0–4 | \|J(300)\| < 10⁻³ in all (no phases: no tilt) | Medium-high |
| **B6a** | g = +0.5 and g = −0.5, θ0 = 0.4, noisy starts 0–9 each | For at least one sign of g, at least 8 of 10 runs end with \|J(300)\| > 10⁻² | Low-medium |
| **B6b** | Same | For the other sign of g, all 10 runs end with \|J(300)\| < 10⁻³ | Low |
| **B6c** | The sign of g from B6a | Both directions occur: between 2 and 8 of the lasting runs have J > 0 | Medium, if B6a holds |
| **B6d** | The lasting runs from B6a | Final winding nonzero in at least half | Low-medium |
| **Reported** | Constant phase θ = 0.4, g = ±0.5, noisy starts 0–4 | J(300), purity, winding | — |

**What a pass of B6 would mean.**
- **Inside ED's rule,** with an arrow in the phases and draws that carry the mark away, a mirror-symmetric rule can settle into a lasting handed flow, with its hand set by chance.
- **Both additions are new choices,** and the mechanism is the published one (C276). So a pass would show what ED would need, not that ED predicts handedness.

**What a failure would mean.**
- **If B6a fails,** these two additions aren't enough, and the handedness line in ED's rule stops here for now. The next step would be outside review (C12), with A5's status stated.

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

**2026-09-14, after run 1 (`results_v2b_run1.txt`).** B2, B3, B4 and B5 right; B1 and B6a–B6d wrong.

**No lasting flow in any of the 40 runs.**
- **The flows:** \|J(300)\| ≤ 2.1 × 10⁻⁵, from starting values of 0.006–0.029.
- **The phases** set by the flow stayed tiny (mean θ ≤ 0.006). The reported constant-phase runs (θ = 0.4) didn't sustain a flow either.
- **Purity rose,** as B2 predicted: it ended at 0.060 with no phase, 0.057 with flow-set phases and 0.12 with a constant phase, against 0.0069 for fully mixed.
- **Winding** was 0 in every run.
- **B6b was scored as defined:** it needed B6a's sign. Both signs actually ended below 10⁻³.

**B1 failed on the mirror check** (1.45 × 10⁻⁴ at t = 20). The diagnostic `mirror_diagnostic.py` (not pre-registered) found:
- **The code is symmetric:** the one-step mirror error is 1.7 × 10⁻¹⁸.
- **The error grows only with flow-set phases,** to about 10⁻⁴ by t = 5 and up to 10⁻³ by t = 20, then levels off. With no phase or a constant phase it stays at 10⁻¹⁷.
- **The cause:** the phase law tanh(\|v\|/V0) has a kink at v = 0 with slope θ0/V0 = 8, which amplifies rounding. The size stays below the thresholds used in B4–B6.

**The exit code now checks** amount, Hermiticity and positivity, and that the recorded run-1 results reproduce: B2–B5, every \|J(300)\| < 10⁻⁴, and the mirror error 1.45 × 10⁻⁴.
