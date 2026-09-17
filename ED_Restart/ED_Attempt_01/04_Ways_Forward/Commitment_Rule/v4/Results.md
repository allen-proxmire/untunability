# Rule version 4: results

*Run 1, 2026-09-14 (`results_v4_run1.txt`). Spec and predictions frozen before running: [Spec.md](Spec.md). Ledger: RD51, C293, C294, G54.*

## What was tested

The tuned hand (C288), with the rebuilt draw:
- **The meeting:** a transfer meeting at a committed locus moves part of a Right- or Left-lane pattern into the Internal channel.
- **The record:** committed matter records, in 3 copies, that the transfer happened.
- **The draw:** fixes only that record.

## Results: all nine frozen predictions right

| test | result |
|---|---|
| **Code checks** | Pass (mirror 10⁻¹⁷) |
| **Tracking every record and drawing each one = version 2b's simple jumps** | Agree to 10⁻¹⁶ |
| **Keeping records coherent, with no draws = the same** | Agree to 10⁻¹⁶ |
| **Amplifying feedback** | **10 of 10 runs hold a hand** (flow 0.114). **Same direction as the tuned test in every run.** Winding nonzero in all |
| **Damping feedback and the gentler control** | All die |

## What it means (C294)

1. **The hand survives the rebuilt draw.** Version 2b's jumps were the rebuilt draw in disguise, once the meeting is a transfer.
2. **The hand doesn't depend on draws being final.** It depends on meetings carrying motion into committed matter. Finality matters for erasure (C291), not for how a population behaves.
3. **It still rests on three choices of ours:** a standing phase, transfer meetings, and a steep response.
4. **So the handedness line has reached its honest end point.** ED's rule *can* hold a chance-chosen hand with the theorem's winding, but it doesn't yet say why. The next real step is making ED *fix* one of those choices, most naturally the standing phase (G54).
