# The budget slows spreading: test spec

*Written 2026-09-13, before any test was run. Frozen once `run_tests_budget.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun.*

## What this adds

**The gap.** RD16 says the budget slows *every* process at a place, spreading included. Version 0 slowed clock ticks but not spreading (V0-L1), because slowing a spreading step locus by locus while keeping it unitary needs a different construction.

**The construction** (`rule_budget.py`, on a 1D ring test bed of loci, each with channels Internal, Left and Right):

| piece | implementation | ledger |
|---|---|---|
| **Spreading generator H** | Local and Hermitian. Right-lane content hops right (term +i(T − T†)), Left-lane content hops left (−i(T − T†)), Internal stays. At every locus the lanes mix through the Grover matrix G = (2/3)J − I (Hermitian; the continuous-time counterpart of V0-D1). Mirror-symmetric | RD13, V0-D1 |
| **Rest term** | + m at every locus and channel. "Mass is concentrated commitment": a pattern's commitment amount is positive. m = 4 is larger than the largest spreading energy (at most 3), so every energy is positive | D7, RD17 |
| **Slowing** | H_s = √S (H + m) √S, with S the diagonal of s(u) = 1 − U(u) at every locus. Hermitian, so evolution stays unitary. It equals H + m where U = 0, and everything at a place slows by the same factor | RD14, RD16 |
| **Evolution** | ψ(t) = exp(−i H_s t) ψ(0), exact, by diagonalising H_s | — |

**Choices made here (can be revisited):**
- **The continuous-time generator** stands in for version 0's discrete coin-and-shift step. Slowing a discrete step locus by locus has no clean unitary form, and the three lanes keep their roles.
- **The symmetric placement √S · · · √S.** It is the least structure that stays Hermitian.
- **The value m = 4.** It only has to exceed the spreading energies.
- **The budget profile U(x) = U₀ a / √(d² + a²),** with d the distance around the ring to the mass and a = 5. It is a smooth test profile, not the q = 1 steady state.

## Limits (stated before running)

- **Only 1D.** In 1D a pattern can speed up or slow down but can't bend. Light bending needs 2D or 3D and is handled analytically in the note.
- **No units.** Only the sign of the effect, and whether it grows in proportion, are tested.
- **Draws, meetings and budget dynamics are left out.** U is fixed, and this is spreading only.

---

## Tests and frozen predictions

**Ring:** 400 loci.

**Starting pattern** (tests F): a real Gaussian of width 6 in the Internal channel, centred at locus 120, with no momentum. It is mirror-symmetric about its centre.

**Mass** (tests F): at locus 200.

### Test H: the construction (code checks)
- **H1.** H_s is Hermitian to 10⁻¹². Every energy of H + m is positive.
- **H2.** With U = 0, H_s equals H + m exactly.
- **H3.** The total amount is conserved to 10⁻¹² after evolving to t = 40.
- **H4 (mirror, T2).** A random pattern with a random U profile, evolved to t = 25, matches the mirror image (locus u → −u, Left ↔ Right) of the mirrored pattern evolved with the mirrored U, to 10⁻¹⁰.

### Test S: slowing is exact where the budget is uniform (RD16)
- **S1.** With uniform U = 0.3, the pattern at time t equals the unslowed pattern at time 0.7 t, to 10⁻¹⁰ (t = 30).

### Test F: does a pattern fall toward the mass?
The centre ⟨x⟩ of the pattern's bandwidth is measured at t = 40. Its change from t = 0 is Δ, and positive means toward the mass.
- **F0 (baseline).** With U₀ = 0, Δ = 0 to 10⁻¹⁰, by symmetry.
- **F1 (falls).** With U₀ = 0.01 and m = +4, Δ > 0.
- **F2 (sign of commitment).** With U₀ = 0.01 and m = −4, so every energy is negative, Δ < 0: it moves away.
- **F3 (proportional).** Δ at U₀ = 0.02 is between 1.8 and 2.2 times Δ at U₀ = 0.01.
- **F4 (reported, not judged).** The same run with only the potential −m U(x) added and hopping left unslowed. How Δ compares shows how much of the fall comes from slowing the rest term, and how much from slowing spreading.

### Claude's predictions (2026-09-13, before running)

| test | prediction | confidence |
|---|---|---|
| H1–H4 | Pass | High: by construction |
| S1 | Pass | High: with uniform s, H_s = s(H + m) |
| F0 | Pass | High: mirror symmetry about the start |
| F1 | Pass: it falls toward the mass | High: √S m √S = m(1 − U) acts as a potential −mU, which pulls a positive-amount pattern toward larger U |
| F2 | Pass: it moves away | High: same reason, opposite sign |
| F3 | Pass | Medium-high: weak-field linear response |
| F4 | Same direction as F1, with a size within a factor of 2 | Medium |

**What a pass would mean.** It would mean slowing everything at a place (RD16) makes positive-amount patterns fall, which is Newtonian-style gravity's direction. **It would not be evidence for ED:** this is how gravitational time dilation acts on energy in standard physics, and a potential −mU is the Newtonian limit. The sign depends on commitment amounts being positive (D7).

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

**2026-09-13, after the first run (`results_budget_run1.txt`).** H1–H4, S1, F0, F1 and F3 passed. **F2 failed:** with m = −4 the pattern still moved toward the mass (+0.0075), and by more than with m = +4 (+0.0021). **F4 went the opposite way from F1** (−0.0028), against my prediction.

**The numbers split into two parts:**
- **Slowing the hops** gives about +0.0049 toward the mass, whatever the sign of m.
- **The rest-term potential** gives about −0.0007 × m.

The sum gives +0.0021 for m = +4 and about +0.0077 for m = −4; the measured values were +0.0021 and +0.0075. My F2 prediction reasoned from the potential alone and was wrong.

**A likely reason the potential pushes away.** A start purely in the Internal lane sits mostly in bands that behave light-like near zero momentum. The lane combination (1, 1, 1)/√3, which has G = +1, should behave like a massive band.

**Added follow-up test K/E.** Its predictions were written here before it was run. Nothing earlier was changed, and everything is rerun.

- **K1.** Internal start, slowed, **m = 0** (spreading slowed, no rest term). Predicted: moves toward the mass by +0.0049, within 20%.
- **E1.** Start in the (1, 1, 1)/√3 lane combination, same Gaussian. Potential only, m = +4. Predicted: toward the mass (Δ > 0).
- **E2.** Same start, slowed, m = +4. Predicted: toward the mass, by more than E1.
- **E3.** Same start, slowed, m = −4. Reported only; the direction is not predicted.

These are exploratory and reported, not code checks.

**2026-09-14: RD35 adopted (G37 = option a). New tests M, predictions written before running.**

**The rule.**
- **Ticking and internal change at a locus slow by s:** the rest term and lane mixing, placed as √S · · · √S.
- **Moving between loci slows by s²:** each hop between u and v is weighted by s(u) s(v).

Function `slowed_rd35`. Light-like patterns then cross a region with used budget U at a speed of about s², which means an effective refractive index of about 1 + 2U, the measured value (C197). Nothing earlier is changed; the RD16 tests stay as the record.

- **M1 (code).** The RD35 generator is Hermitian, equals H + m where U = 0, conserves the amount (10⁻¹²), and passes the mirror check (10⁻¹⁰).
- **M2 (code).** Hops only (no lane mixing, m = 0), uniform U = 0.3: the pattern at t equals the unslowed pattern at s² t = 0.49 t, to 10⁻¹⁰.
- **M3.** Internal start, m = 0, U₀ = 0.01 (lingering only). Predicted: drift toward the mass, between 1.5 and 2.5 times K1 (+0.0048), because moving now slows about twice as much.
- **M4.** Massive-like start, m = +4, U₀ = 0.01. Predicted: drift toward the mass, within 15% of E2 (+0.079), because the pull comes from the rest term, which is unchanged.
- **M5.** Massive-like start, m = −4. Predicted: moves away (Δ < 0).

**2026-09-14: RD36 adopted (G38 = option a). New tests N, predictions written before running.**

**The rule.** The rate becomes s = e^(−U): ticking slows by e^(−U), moving between loci by e^(−2U). Function `slowed_rd36`. In weak fields it differs from RD35 only at order U².

- **N1 (code).** The RD36 generator is Hermitian, equals H + m where U = 0, conserves the amount (10⁻¹²), and passes the mirror check (10⁻¹⁰).
- **N2 (code).** Hops only, uniform U = 0.3: the pattern at t equals the unslowed pattern at e^(−0.6) t, to 10⁻¹⁰.
- **N3.** Massive-like start, m = +4, U₀ = 0.01. Predicted: drift within 2% of M4 (+0.0783), since the difference is order U².
