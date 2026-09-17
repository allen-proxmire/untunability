# Putting feedback into ED's real rule (G47 = c, RD45)

*2026-09-14. Ledger: RD45, C269–C271, G48. Background: A5, A7, C4, C32, C33, C34, C263, C268.*

## 1. What the real rule is now

**ED's real rule** is version 1 plus the budget (`Commitment_Rule/v1_budget/rule_budget.py`):
- **Spreading** is a local three-lane generator: Right hops right, Left hops left, and the lanes mix at each locus.
- **The budget slows everything** at a place: ticking by e^(−U), moving by e^(−2U) (RD35–RD37). This is what gave GR's light bending, Mercury and Nordtvedt.
- **Draws happen only** where a mark can't be brought back (RD26–RD28).
- **There is no feedback law (A7).** The state doesn't change how the pattern itself moves, except through the budget, which is a slowing, not a direction.

## 2. What I found before designing anything (C269)

**The real rule's spreading is reversible.** Its generator is Hermitian, so the amount is conserved, and forward and backward hops mirror each other in time.

**The consequence is a theorem already in the ledger.** Hermitian transport has zero winding (C4). So:

> **Any feedback that keeps spreading reversible cannot produce the handedness the theorem measures,** however it's designed.

**This isn't new, but it's now concrete.** The public handedness result assumed the arrow (P11) reaches transport (A5). Under D1 and P11, irreversibility lives in the commitment step, not in spreading, and whether transport between commitments comes out one-way is still open (C32). The toys (C248, C263) put the arrow straight into the hops. The real rule doesn't.

## 3. The options (G48)

| | where feedback enters | what it can give | cost |
|---|---|---|---|
| **(a)** | **A phase on each hop, set by the local current** (P09 phases). Spreading stays reversible | A pattern that moves one way by itself: handedness as a **direction of motion**. Winding stays zero (C4). Published home: chiral solitons in current-coupled Schrödinger models (C270) | Cheapest. Keeps all gravity results. Not the theorem's handedness |
| **(b)** | **Hop strengths set by the local current, as in the toys.** Spreading becomes one-way | The theorem's handedness (winding), as in C248 and C263 | Spreading stops conserving the amount, so the gravity construction (C192–C203) has to be redone. And it puts the arrow where ED says it doesn't live (D1, C32) |
| **(c)** | **At commitment.** Spreading stays reversible; each draw, which is irreversible, sets the imbalance of the hops that follow from the local current at that moment | The theorem's handedness is possible, with the arrow entering exactly where P11 and D1 put it. It directly answers C32 | Needs draws and spreading in one model (version 2, V1-L3). Feedback acts only where draws happen, so **a lone pattern never gets it** |
| **(d)** | **P12's own steering, a = −∇Σ** | A push down a gradient. No direction of its own | The budget already does this (it's gravity). Set aside for handedness |

**About (c)'s cost.** Because draws happen only where a mark can't be brought back (RD28), handedness under (c) could only arise where patterns meet committed matter often: a dense, busy region. That fits your seed-crystal picture of an early, saturated universe (D15). But it means (c) can't be tested on one pattern alone.

## 4. Recommendation

**(c).** It's the only option that:
- puts the arrow where ED says it lives;
- keeps the gravity results;
- turns the long-open C32 into a computation.

**Plan if chosen.** Build version 2 minimally: one ring, three lanes, budget-slowed reversible spreading, and many committed "detector" loci that draw. Each draw sets the next hops' imbalance from the local current. Then ask, with frozen predictions, whether a handed state forms and whether it has nonzero winding.

**Fallback (a).** Cheap and clean, but it can only give direction of motion, not the theorem's handedness.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C270 | Aglietti, Griguolo, Jackiw, Pi, Seminara, "Anyons and chiral solitons on a line", *PRL* 77, 4406 (1996) | Abstract via search listing |
| C270 | Harikumar, Kumar, Sivakumar, "Chiral solitons in a current coupled Schrödinger equation with self interaction", *PRD* 58, 107703 (1998), arXiv:cond-mat/9808239 | Abstract read |
| C270 | Clark et al., "Observation of density-dependent gauge fields in a Bose–Einstein condensate…", *PRL* 121, 030402 (2018) | Abstract via search listing |
| C270 | Görg et al., "Realization of density-dependent Peierls phases…", *Nature Physics* (2019) | Title via search listing |

## 5. Result of (c): version 2 (2026-09-14)

**All ten frozen predictions right** ([Commitment_Rule/v2/Results.md](Commitment_Rule/v2/Results.md), C275).
- **Flow dies:** draw-rate feedback, of either sign, can't keep a flow going. The draws only mix.
- **No winding:** the real rule's two-way hops block it for any draw rates.
- **Phases unlock it:** giving the lanes opposite hop phases makes winding possible.

**Next (G49).** Proposal: version 2b, with flow-set lane phases plus draws that carry marks into a cold environment.

## 6. Result of version 2b (2026-09-14)

**No lasting flow in any run** ([Commitment_Rule/v2b/Results.md](Commitment_Rule/v2b/Results.md), C278). That held with phases following the flow's size, with a constant phase, and with draws that carry motion into committed matter.

**Next (G50).** Proposal: a short gain check, then work out the draw itself (G36), with outside review of the handedness theorem alongside.

## 7. Gain check (2026-09-14)

**The door isn't shut** (C281–C283). A hand can start from noise in version 2b's rule, but only with three things together:
- **a standing phase,** since a flow-set phase can't start one;
- **draws that carry motion off;**
- **a rate law steep enough** (V0 below about 0.1).

All three are free settings. **Next (G51):** proposal (c), a labelled tuned dynamic test alongside starting work on the draw (G36).

## 8. Tuned test (2026-09-14)

**At settings labelled as tuned, ED's rule held a lasting hand** (C288, C289).
- **All 10 runs** with the amplifying sign kept a flow, 6 one way and 4 the other.
- **The winding** was nonzero in every run.
- **The damping sign and a gentler rate law** both died.

**What it needs.** A standing phase, draws that carry motion off, and a steep rate law, all choices of ours. So it shows ED *can* be handed, not that it *must* be.

**Next.** Re-check on the rebuilt draw (RD50).
