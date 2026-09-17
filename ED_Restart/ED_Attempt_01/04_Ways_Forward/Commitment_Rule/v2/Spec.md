# Rule version 2: spreading and draws together, with feedback at commitment

*Written 2026-09-14, before any test was run. Frozen once `run_tests_v2.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun.*

## What version 2 is (RD46, G48 = c)

| piece | version 2 | ledger |
|---|---|---|
| **Spreading** | The real rule's generator from v1_budget: three lanes (Internal, Left, Right), Grover lane mixing, the budget slowing with rate e^(−U) (RD36). Reversible (Hermitian) | RD13, RD35, RD36, V0-D1 |
| **One ring** | Spreading and draws happen on the same ring of loci (lifts V1-L3's separate marker ring) | V1-L3 |
| **Committed loci** | Every D-th locus stands for committed matter. A part in channel K at a committed locus x is drawn at rate γ[x, K] and collapses onto that single channel | P11, RD28 (detector model) |
| **A population** | Many identical patterns, described by their one-pattern density matrix ρ. Averaged over draws: dρ/dt = −i[H, ρ] + Σ_a γ_a (P_a ρ P_a − ½{P_a, ρ}), P_a = \|a⟩⟨a\| | standard averaging of draws |
| **Feedback at commitment** | The draw rates at x are set by the population's local velocity v_x at that moment: γ[x, Right] = Γ(1 − g tanh(v_x/V0)), γ[x, Left] = Γ(1 + g tanh(v_x/V0)), γ[x, Internal] = Γ | RD46, A7 |

**The local velocity.**
- **Current:** the amount per unit time crossing bond (u, u+1) is j_u = Σ 2 Im(H_ba ρ_ab), summed over channels a at u and b at u+1.
- **Velocity:** v_x = ½(j_{x−1} + j_x) / n_x, with n_x the amount at x.
- **No memory:** it uses the present state only (D1, C33).

**Mirror symmetry.**
- **The mirror** (locus u → −u, Left ↔ Right) sends v_x → −v_{−x} and swaps the Left and Right rates.
- **The committed loci** are mirror-symmetric when D divides L.

**Choices made here (can be revisited).**
- **The rate law:** the tanh form and its sign (the lane moving with the flow is drawn less). The opposite sign is also run.
- **Mean-field:** feedback responds to the population's flow, not to a single pattern's own flow. A single pattern responding to itself would make draws nonlinear.
- **Budget:** U = 0 in the tests. Uniform U only rescales time (C193); the budget code path is kept.

## Analysis written before running

**A. Draws that collapse onto single channels can only lower purity, with or without feedback.**
- Purity is tr ρ², roughly how unmixed the population is.
- **Derivation:** d(tr ρ²)/dt = 2 Σ_a γ_a (ρ_aa² − (ρ²)_aa) = −2 Σ_a γ_a Σ_{b≠a} \|ρ_ab\|² ≤ 0, for any rates ≥ 0, including rates that depend on ρ.
- **Consequence:** the draws push the population toward the fully mixed, even state, which carries no current. No lasting handed flow is expected unless a state exists that the draws can't touch.

**B. The real rule's hops are reciprocal, so losses at draw sites can't give winding.**
- **Real gauge:** with ψ_{u,Right} → i^(−u) ψ and ψ_{u,Left} → i^(u) ψ, every hop becomes real, and the lane mixing becomes real with signs (−1)^u. The generator is then real symmetric, with a flux of π per lane plaquette.
- **The no-draw generator** H_eff = H − (i/2) diag(γ) is then complex symmetric (H_eff^T = H_eff).
- **Winding is forced to zero:** with the twist φ at one bond, det(H_eff(φ) − E) = det(H_eff(−φ) − E), so the winding about any point E is zero, for any loss pattern.
- **What would change it:** giving the Right and Left lanes different hop phases (e^(+iθ) and e^(−iθ)) changes the flux away from π, and then winding is no longer forced to zero.
- **In ED terms:** feedback that only changes how often draws happen can't make transport one-way in the theorem's sense. The arrow would have to reach the phases, which is option (a) and C32.

## Limits (stated before running)

- **1D, no units, U = 0.** The committed loci are fixed and don't move or respond except through their rates.
- **The draw model stands in for** "a mark that can't be brought back" (G36).
- **Draws here return the drawn part to the population at the same locus.** Marks carried away into a cold environment (non-unital draws) are not modelled.
- **Mean-field only.** Single-pattern trajectories aren't simulated.

---

## Setup

- **Ring and loci:** L = 48, D = 3 (16 committed loci). Γ = 1, V0 = 0.05, g = 0.5 unless stated.
- **Evolution:** RK4, dt = 0.01, rates held fixed within a step.
- **Starts:**
  - **current start:** all in the Right lane, ψ_{u,Right} = e^(iku)/√L, k = 2π·3/48;
  - **mirror current start:** its mirror image;
  - **noisy starts:** 10 of them, ψ ∝ 1 + 0.1 ξ in all channels, with ξ complex unit Gaussian (seed 2468).
- **Winding:** of det(H_eff(φ) − E0) as the twist φ at bond (L−1, 0) goes once around (600 steps). E0 is the centroid plus 30 random points in the spectrum's bounding box; points within 10⁻³ of an eigenvalue are skipped. The largest \|winding\| is reported.

## Tests and frozen predictions

| test | what | prediction | confidence |
|---|---|---|---|
| **V2-P1 (code)** | Every run | Amount conserved to 10⁻¹²; ρ Hermitian to 10⁻¹²; smallest eigenvalue of ρ ≥ −10⁻⁸ at the end | High |
| **V2-P2 (code)** | Mirror check: a noisy start and its mirror image, g = 0.5, t = 20 | Mirror of one end matches the other to 10⁻⁹ | High |
| **V2-P3 (analysis A)** | All runs with draws, checked every 100 steps | Purity never rises by more than 10⁻¹² | High |
| **V2-P4 (code)** | No draws (Γ = 0), noisy start, t = 50 | Purity constant to 10⁻⁹ | High |
| **V2-P5 (analysis B)** | Real rule, L = 12, 13, 16, 30 random loss patterns each (every channel's rate uniform in [0, 2]) | All windings 0 | High |
| **V2-P6 (contrast)** | As P5 but Right-lane hops × e^(0.4i), Left-lane hops × e^(−0.4i) | At least one nonzero winding among the 90 | Medium |
| **V2-P7** | Current start, g = 0.5, t = 200 | \|J(200)\| < 0.01 \|J(0)\|, with J the total current | Medium-high (a dark state could hold current) |
| **V2-P8** | Current start, g = −0.5 | Same as P7 | Medium-high |
| **V2-P9** | Noisy starts, g = 0.5, t = 200 | Largest \|J(200)\| < 10⁻³ | Medium-high |
| **V2-P10 (analysis B)** | P7–P9 runs | Winding of H_eff at the final rates is 0 | High |
| **Reported** | All runs | J(0), purity at t = 0 and t = 200, spread of the Right/Left rates at t = 0 and t = 200 | — |

**What a pass would mean.**
- **Feedback at commitment, in its simplest form, can't make ED handed.** Draws of this kind drive the population toward evenness, and the real rule's reciprocity blocks winding.
- **It would sharpen C32:** the arrow of commitment doesn't reach transport through draw rates alone.
- **It would say where to look instead:**
  - draws that carry marks away into a cold environment (non-unital);
  - feedback on phases, which combines (a) with (c).

**What a failure would mean.**
- **If P7–P9 fail,** some state holds a current against the draws, which is worth understanding.
- **If P5 fails,** the reciprocity analysis is wrong.

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

**2026-09-14, after run 1 (`results_v2_run1.txt`).** All ten predictions were right.
- **Current start:** J fell from 1.848 to 5.6 × 10⁻⁵ with g = +0.5, and to 5.3 × 10⁻⁵ with g = −0.5.
- **Noisy starts:** the largest \|J(200)\| was 1.0 × 10⁻⁷.
- **Purity:** fell in every interval, from 1 to 0.0072, near the fully mixed value 1/144 ≈ 0.0069.
- **Winding:** the real rule with random losses gave 0 in all 90 cases. With lane phases 0.4 it was nonzero in 75 of 90. The final-rate winding was 0 in every dynamic run.

**A reporting note.** "R/L rate spread" is the max − min of the Right-lane rate across committed loci.
- For the current start it is 0 because the flow is uniform; the rates were Γ(1 ∓ g tanh(v/V0)) everywhere.
- For noisy starts it was 0.91–1.00 at t = 0, so the feedback was active, and 0 at t = 200.

**The exit code now checks** V2-P1, P2 and P4, and that the recorded run-1 results reproduce. Nothing else changed.
