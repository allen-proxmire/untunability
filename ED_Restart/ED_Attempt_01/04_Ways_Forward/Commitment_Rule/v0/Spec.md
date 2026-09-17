# Rule version 0: test spec

*Written 2026-09-13, before any test was run. Frozen once `run_tests_v0.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun.*

## What version 0 is

A runnable version of the commitment rule on a 1D ring of loci, built from decisions RD1–RD21 (worksheet and ledger). It lives in `rule_v0.py`.

| piece | implementation | ledger |
|---|---|---|
| Loci and channels | Ring of L loci; channels Internal, Left, Right | RD13 |
| Amplitudes | Complex a[u, K]; bandwidth = \|a\|² | RD13 |
| Spreading between ticks | One substrate step = coin, then shift. Content in Right moves one locus right, Left one locus left, Internal stays. Linear, conserving, connection phase 0 | RD13 |
| The coin | **Grover coin** (2/3)J − I: no free number, and it treats all three channels symmetrically, so it passes the mirror check automatically. **A new choice by least structure; Allen can veto (V0-D1)** | — |
| Draw | Pick (locus, channel) with probability ∝ bandwidth; every other option goes to zero; the drawn content keeps its phase; spreading restarts from there | RD3, RD9, RD11, RD13 |
| Lone-particle draw trigger | A pattern draws when its largest per-locus share falls below b_min | RD19 |
| Budget | U_{t+1}(u) = min(1, M(u) + q × average of U_t over the two neighbours); local rate factor s(u) = 1 − U(u) | RD14, RD16 |
| Clock ticks | Per step, a pattern gains ω × (bandwidth-weighted average of s) clock ticks; clock ticks don't zero anything | RD18 |
| Entangled pattern | One amplitude over pairs (part A's locus and channel, part B's locus and channel), with the parts on two separate rings | RD5, D5 |

## Limitations of version 0 (stated before running)

- **V0-L1. The budget slows clock ticks and draw probabilities, but not spreading.** RD16 says every process slows. Slowing a unitary spreading step locus by locus needs a different construction, left for version 1.
- **V0-L2. Masses are fixed test inputs,** not chains that move.
- **V0-L3. No P12 feedback.**
- **V0-L4. One dimension, no units.** Tests T3, T5, T6 and T9 can't be run here.
- **V0-L5. No motion-dependent clock slowing** (RD17), so T8 is not tested here. Its requirement is recorded in C63.
- **V0-L6. No locus birth** (RD21). The ring is a patch of already-born loci.
- **Known property of the coin.** Three-state Grover walks keep part of their weight trapped near the starting point for most initial states (Inui, Konno and Segawa, 2005; C77). A lone pattern may therefore never get "too thin" for small b_min.

---

## Tests and frozen predictions

### Test A: mirror check (T2)
**Setup.** A random complex initial pattern on a ring of 40 loci and a random mass profile. Run 50 spreading steps and 50 budget steps from the original, and separately from its mirror image (locus u → −u, Left ↔ Right).

**Pass if** every one of these matches its mirror image to within 10⁻¹² in the largest entry:
1. the spread pattern;
2. the budget field;
3. the draw probabilities;
4. the step at which the pattern first becomes too thin.

### Test B: budget profile around a mass (C54, and T1's direction)
**Setup.** A ring of 201 loci, mass 0.1 at locus 0, q ∈ {0.5, 0.9}, budget iterated to steady state.

**Pass if:**
1. **The falloff matches.** For loci 1 to 20, U(x+1)/U(x) equals ρ, the root below 1 of q(ρ + 1/ρ)/2 = 1, to within a relative error of 10⁻⁶.
2. **It is symmetric:** U(x) = U(−x) to 10⁻¹².
3. **The rate is lowest at the mass:** s(0) < s(100). This is true by construction, and is included only as a sanity check.

### Test C: interference before a lone draw (T4, qualitative)
**Setup.** A ring of 401 loci. A lone pattern starts at the centre locus, in the Internal channel. For each b_min ∈ {0.5, 0.3, 0.15, 0.08, 0.04}, spread until the pattern is first too thin, or give up after 200 steps. At that step, compare the coherent pattern's per-locus shares with a fully decohered walk (the same step probabilities, but with no interference), using total variation distance (TV).

**Pass if:**
1. **No interference after one step.** If the draw fires at step 1, TV < 10⁻¹².
2. **Interference once it has spread.** If the draw fires at step 2 or later, TV > 10⁻⁶.
3. **More spreading, more interference.** Among the b_min values whose draw fires, TV does not decrease as b_min gets smaller.
4. **Recorded, not judged.** Any b_min whose draw never fires within 200 steps is recorded as an observation (see the coin's known trapping, C77).

### Test D: no signalling with an entangled pattern (T7)
**Setup.** Two rings of 16 loci, part A (Alice) and part B (Bob). The initial state is

  ∝ |A at 0⟩|B at 0⟩ + |A at 1⟩ (|B at 0⟩ + |B at 1⟩)/√2,

all in the Internal channel. It is chosen so that Bob's part on its own still carries coherence between loci 0 and 1.

- **Alice's choice.**
  - **(0) Idle:** her part does nothing.
  - **(1) Spread:** her part spreads until it is first too thin (b_min = 0.2), which fires the draw.
- **Then Bob's part spreads for 3 steps, and Bob's average per-locus distribution is computed exactly,** averaging over every possible draw outcome with its probability.
- **This is done under three rules:**
  - **Baseline:** no draw ever happens.
  - **Joint draw:** RD5 read literally. One draw picks A's *and* B's locus and channel together.
  - **Local draw:** the draw picks only the triggering part's locus and channel. Bob's part keeps whatever conditional pattern goes with that outcome.

**Pass if** Bob's average distribution is the same for Alice idle and Alice spread, to 10⁻¹², **and** Bob's part never becomes too thin itself during his 3 steps (checked, not assumed).

### Claude's predictions (2026-09-13, before running)

| test | prediction | confidence |
|---|---|---|
| A | Passes all four | High: everything in the rule treats Left and Right alike |
| B | Passes all three | High: C54 is a short proof |
| C | Parts 1–3 pass. For the smallest b_min values the draw may never fire, because of the coin's known trapping | Medium on part 3; the trapping outcome is a genuine unknown |
| D, baseline | Passes | High: a local choice by Alice can't change Bob's part without a draw |
| D, joint draw | **Fails.** Alice's choice changes Bob's average distribution | Medium-high: a draw that fixes Bob's locus destroys the coherence Bob's part carries, and Alice controls whether it happens |
| D, local draw | Passes | High: averaged over Alice's outcomes, Bob's part is unchanged |

**If the joint draw fails as predicted,** that is a real finding: RD5 read literally would allow a signal faster than light. The fix to decide would be G31, whether an entangled pattern's draw fixes only the part that interacts. Nonlinear modifications of quantum mechanics are known to open this kind of loophole (Gisin, 1990; C78).

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

**2026-09-13, after the first run: test B1's numerical method.**

- **What happened.** B1 failed for q = 0.5, with a maximum relative error of 2.3 × 10⁻⁵ against the 10⁻⁶ criterion. It passed for q = 0.9.
- **Diagnosis.**
  - The rule's iterated budget agrees with an exact linear solve of the same steady-state equation to 4.5 × 10⁻¹⁶, and the cap at 1 is never reached.
  - With the exact solve, the ratio error is 6.2 × 10⁻¹⁶.
  - The failure came from dividing numbers near 10⁻¹³ (at x = 20, U ≈ 4.2 × 10⁻¹³), where rounding in the iteration dominates. It is a flaw in the test's method, not in the rule or the prediction.
- **Change.**
  - **B0 (new):** the rule's iterated budget must match the exact linear solve to 10⁻¹², which tests the rule's code.
  - **B1:** the falloff ratios are taken from the exact solve, with the same 10⁻⁶ criterion.
  - Nothing else changes. All tests are rerun.

**2026-09-13: RD22 adopted (G31).**
- **The change.** The rule's entangled draw is now the local draw: it fixes only the part that interacts. `rule_v0.py` gains `draw_entangled` for this.
- **Test D2 is unchanged.** It now documents the *rejected* option, and is still expected to fail no-signalling. Test D3 checks the adopted rule.
- **No existing test logic or criterion changed.** All tests are rerun.
- **New test D4** checks the rule's own draw function. Sampled 20,000 times, `draw_entangled` must reproduce the exact local-draw average of Bob's distribution to within 0.02. This is a code check, and the criterion was set before it was first run.
