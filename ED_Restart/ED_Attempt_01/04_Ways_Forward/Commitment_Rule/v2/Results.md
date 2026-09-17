# Rule version 2: results

*Run 1, 2026-09-14 (`results_v2_run1.txt`). Spec and predictions frozen before running: [Spec.md](Spec.md). Ledger: C275–C277, G49.*

## What was tested

- **The model:** ED's real rule (reversible three-lane spreading) plus committed loci that draw, on one ring.
- **The feedback:** each committed locus's draw rates for the Right and Left lanes are set by the local flow at that moment (RD46).
- **The question:** can feedback at commitment make ED's transport handed?

## Results: all 10 frozen predictions right

| test | result |
|---|---|
| Code: amount, Hermitian, positive; mirror check; no draws keeps purity | Pass (mirror error 7 × 10⁻¹⁸) |
| **Purity never rises** (analysis A) | It fell in every interval in every run, from 1 to 0.0072 (fully mixed is 0.0069) |
| **Real rule with random draw losses: no winding** (analysis B) | 0 in all 90 cases |
| **Contrast: give the lanes opposite hop phases** | Winding appears in 75 of 90 cases |
| **A strong starting flow** (J = 1.85) | Gone by t = 200: 5.6 × 10⁻⁵ with feedback of either sign |
| **Noisy starts** (feedback active at first) | Every flow died out (largest 1 × 10⁻⁷) |
| **Winding at the end of every run** | 0 |

## What it means (C277)

1. **Draws of this kind drive the population toward evenness,** whatever the feedback does. Every draw mixes the population a little more, and the fully mixed state carries no flow. So no handed flow can last.
2. **The real rule's hops work the same both ways,** so draw rates, however they're set, can't make transport one-way in the theorem's sense. Changing the hop phases does unlock it (75 of 90).
3. **The arrow of commitment doesn't reach transport through draw rates** in ED's rule as written. That answers C32 for this route, and it means the public result's assumption A5 isn't delivered by the rule yet.

**What would be needed, as far as this shows:**
- **Something that breaks two-way symmetry in the phases,** such as feedback onto hop phases.
- **Draws that don't just mix,** meaning marks carried off into a cold, committed environment. That is the published recipe for one-way behaviour from dissipation: matching a coherent interaction with its dissipative counterpart (Metelmann and Clerk, C276).

Both are new choices. G49 asks whether to make them.

## Limits

- **1D, mean-field, U = 0,** and fixed committed loci.
- **One rate law** (tanh), tried with both signs.
- **Draws return the drawn part** to the same place (unital). Non-unital draws are untested.
