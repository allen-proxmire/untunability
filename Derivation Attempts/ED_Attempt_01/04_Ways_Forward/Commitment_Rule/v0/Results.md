# Rule version 0: results

*Run 2026-09-13. Full output: `results_v0_run2.txt`. After RD22: `results_v0_run3.txt`, where new test D4 confirms the rule's own entangled draw function matches the exact local-draw average (difference 0.0006 over 20,000 samples). Spec and frozen predictions: [Spec.md](Spec.md). Ledger: C79–C82, G31.*

## Summary

| test | what it checks | result | predicted |
|---|---|---|---|
| **A** | The rule has no built-in left–right preference (T2) | **Pass.** Every quantity matches its mirror image, errors ≤ 2.1 × 10⁻¹⁵ | Pass |
| **B** | The budget falls off around a mass exactly as C54 proves, symmetrically, with slower ticks at the mass | **Pass**, after one change to the test's numerical method (below) | Pass |
| **C** | A lone pattern interferes before its draw (T4, qualitatively) | **Pass**, plus one observation | Pass, with the observation flagged as possible |
| **D, baseline** | Without draws, Alice can't signal Bob | **Pass** (difference 1.1 × 10⁻¹⁶) | Pass |
| **D, joint draw** | RD5 read literally: one draw fixes both entangled parts | **Fails no-signalling.** Alice's choice changes Bob's statistics by up to 0.077 | **Fail** |
| **D, local draw** | The draw fixes only the part that interacts | **Pass** (difference 5.6 × 10⁻¹⁷) | Pass |

Every prediction written before the run came out as predicted.

---

## Findings, in plain words

### 1. RD5 as worded would allow faster-than-light signalling (C81)
RD5 says an entangled pattern "resolves as two chains in a single draw," and G16 says that happens at the first interaction of *any* part.

Read literally, when Alice's part interacts, one draw fixes where *Bob's* part is too. Alice controls whether that happens: spreading her part makes it too thin and triggers the draw. Pinning Bob's part down destroys the spread-out coherence his part carried, which Bob can see in his own later statistics. So Alice could send Bob a signal, instantly, across any distance. Experiments and relativity don't allow that (C52).

**The version that passes:** the draw fixes only the part that interacts. Bob's part keeps its conditional pattern, and becomes definite through correlation when *it* interacts. Averaged over Alice's outcomes, nothing about Bob changes, to 10⁻¹⁷.

**This is how physics already handles it.** In standard quantum mechanics a measurement acts on the measured particle only, and collapse models localize one particle at a time. Nonlinear changes to quantum mechanics are known to open exactly this kind of signalling loophole (C78). The correlations between the two chains are still there, and still come out right. What changes is only *which part the draw acts on*.

**Decided 2026-09-13 (RD22):** an entangled pattern's draw fixes only the part that interacts. The other parts become definite through correlation when they interact. The joint draw is kept in the code only as the rejected option, for comparison.

### 2. A lone pattern interferes before its draw, more the further it spreads (C80)

| b_min (how thin before a draw) | draw happens at step | interference (difference from a no-interference walk) |
|---|---|---|
| 0.50 | 1 | 0.00 |
| 0.30 | 4 | 0.34 |
| 0.15 | 8 | 0.40 |
| 0.08 | 34 | 0.59 |
| 0.04 | **never** (within 200 steps) | — |

That is what T4 needs: interference builds while the pattern spreads, and the draw fires once it is too thin.

### 3. Observation: with this coin, some lone patterns never get thin enough to draw (C80, C77)
At b_min = 0.04 the pattern's largest share stayed at 0.128 for all 200 steps. That is the known trapping of three-state walks: part of the pattern stays near where it started. So with the Grover coin (V0-D1), any "too thin" limit below about 0.13 means a lone particle *never* draws by thinness.

This matters because the coin was a least-structure choice, not a decision about what ED means. Before RD19's limit is tied to anything physical, it's worth knowing whether trapping belongs to ED or only to this coin. This goes on the list for Allen (V0-D1).

### 4. The budget behaves exactly as calculated (C82)
Around a lone mass, the used budget falls off by the predicted factor per step: 0.268 per step for q = 0.5, 0.627 for q = 0.9, matching C54 to 10⁻¹⁶. It is symmetric, and ticks are slower at the mass. On the ring the falloff is exponential. The 1/r of gravity needs 3D.

---

## One change after freezing (recorded in Spec.md)

B1 failed on the first run for q = 0.5, with a relative error of 2.3 × 10⁻⁵ against 10⁻⁶. The diagnosis: the rule's budget matches the exact steady state to 4.5 × 10⁻¹⁶, and the test was dividing numbers near 10⁻¹³, where rounding dominates. So the flaw was in the test, not the rule. The test was changed to compare the rule against the exact solution (new B0) and to take the ratios from the exact solution. All tests were rerun. The first run's output is summarized in the ledger log.

## What version 0 does not show

- **Nothing about real numbers.** One dimension, no units: no clock-effect size (T3), no collapse bounds (T5), no preferred-frame test (T6), no 54 cm atom test (T9).
- **Spreading isn't slowed by the budget yet** (V0-L1).
- **No motion-dependent clock slowing, so no muon test** (T8).
- **No P12 feedback, no locus birth.**
- **Tests A, B and the D baseline are checks of the code against its own maths** (Rule 6, kind 1). Tests C and D are logic checks of the rule (does it do what the decisions say, and does it break no-signalling?). None of this is evidence about nature.
