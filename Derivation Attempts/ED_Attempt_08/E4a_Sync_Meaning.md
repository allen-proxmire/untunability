# Sync means a whole slice agreeing, not a move-by-move veto

*ED_Attempt_08, note 6. 2026-09-20 (RD12). Ledger: C32, C33. Allen's decision (D10), **recorded before the n = 52 scale curve finished**, so it cannot be read as a response to that result. Reasoning and existing run values only; nothing new computed.*

## The decision

> **Allen: "sync was always about a whole slice agreeing, not one move — is what my instinct is."**

## How the meaning drifted, in three steps and no decisions

| | what sync was | where |
|---|---|---|
| **Attempt 6** | "Clocks want to sync" means rates **can match** across a region | A6 D6, D7 |
| **Synced Now (A7 C2b)** | The **wobble across a region of size L** shrinks relative to how fast influence travels, so a common "now" survives for d ≥ 3 | A7 C2b |
| **A7 C3e** | A **sum over links** of squared clock difference, added to the cost | A7 C3e |
| **A7 C3f (D39–D41)** | **Refuse any move that would create one link carrying strain above a threshold** | A7 D39, D41 |

**Each step had a good modelling reason** — a cost function needs local terms; a condition has to be checkable move by move. **None of them was a decision about what sync means.**

## Why the last two are a different claim, not a simplification

**Synced Now's statement is about an aggregate over a region:** the differences between many clocks do not accumulate coherently as the region grows. That is **compatible with neighbouring clocks disagreeing substantially** — what matters is that the disagreement does not build with distance.

**The per-move veto says something strictly stronger:** no single pair may disagree by more than s_max. **It forbids local roughness that Synced Now never forbade.**

## What this reclassifies

**Every three-dimensional growth run in attempts 7 and 8 — C3e, C3f, C3g, the threshold scan, the E3 pilot and E4 — tested a local veto, not sync as ED means it.**

**Those runs are not discarded.** They are valid tests of a local veto, and the local veto turns out to have a mechanism of its own (below). What changes is what they are evidence *about*.

## Why a local veto would make slices stringy (C33)

**If a move is refused whenever it would create a link whose two clocks disagree, growth can only go where clocks already agree.** The pattern then follows narrow corridors of agreement — and corridors are filaments.

**The E4 runs fit this**, at n = 52 with 140,608 events:

| | spectral dimension |
|---|---|
| **Condition on** (three seeds) | **1.635, 1.646, 1.685** |
| **Condition off** (two seeds) | **2.319, 2.320** |

**Switching the condition off moves the slice toward three dimensions, not away** — and 2.32 is the most space-like number this project has produced, identical to three figures across seeds. That is the opposite of what sync was introduced to do.

## What this does not fix

**Removing the veto does not rescue the growth rule.** The controls read **2.32, not 3**, with commitment and curvature still acting. **Sync's form is part of the wall, not all of it.** The local costs remain, and they still lose to entropy — which is attempt 7's own C3a lesson, that local costs do not act at large scales, now confirmed a second time in 3D.

## Claude's reading, offered and labelled as such

**In Synced Now, sync was a diagnostic:** given a slice of dimension d, can a common "now" survive? The answer was yes for d ≥ 3.

**In the growth model it became a driver:** a rule that decides which move to make.

**That is a change of job, and it was never decided.** A test of whether a finished slice can support a common "now" is not obviously a rule for choosing the next move. If that reading is right, sync does not belong in the move loop at all — it belongs where it started, as a condition on whole slices.

**This is a proposal, not a decision.** Allen has decided what sync *means*; what follows for the model is a separate question and still open.

## What this opens

- **Sync acting on whole slices** — item 4 of attempt 7's carry-forward, never opened, and now the natural next road.
- **What a whole-slice sync would even look like in growth:** a condition on a tick rather than a move; a coarse-grained clock field agreeing patch by patch while links stay rough; or sync as a filter applied after a slice is grown rather than during.
- **Whether the local costs need the same examination.** Commitment as α·E and curvature as a sum over edges are local sums too, and they arrived the same way.
