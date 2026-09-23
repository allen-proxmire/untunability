# H3 S0: the floor has no teeth, and selection doesn't accumulate — because ED rewrites most of each slice every tick

*ED_Attempt_09, note 8. 2026-09-21 (RD10). Ledger: C30–C33. Run `model/h3_s0.py`, 32 minutes at n = 24. Pass marks fixed before running (C29). Written plainly.*

## S0-a: the floor (C30)

**The floor** — rates can match across the pattern — passes a slice if no connection needs more than twice the strain flat space needs.

| slice | strain | average distance | floor (≤ 14.65) |
|---|---|---|---|
| flat | 7.30 | **11.49** | pass |
| small world (conditions only) | 9.73 | 4.58 | pass |
| **stringy (attempt 8's costs on)** | **12.71** | 5.57 | **pass — should have failed** |

**By the rule fixed beforehand, the floor is still toothless.** The strains are in the right order, but close together: stringy needs only 1.74× flat's strain. A line separating stringy from small-world would have to sit between 9.7 and 12.7 — a finely set clock-rate spread. **That number was not chosen after seeing these results; it's Allen's call.**

**And a second finding:** the stringy slices are compact too — average distance 5.6 against flat's 11.5. Attempt 8's costs made slices stringy up close but no less crammed overall. **So "fewest directions", measured as average distance, would prefer stringy over small-world**, and the floor can't stop it.

## S0-b: does picking the best move the shape? (C31)

From the same small-world slice, 30 more ticks two ways: plainly, and **best of 8** — each tick, grow eight possible next slices and keep the one with the largest average distance that passes the floor.

| | first 5 ticks | last 5 ticks | trend |
|---|---|---|---|
| plain | 4.49 | 4.46 | — |
| **best of 8** | **4.55** | **4.56** | **zero per tick** |
| *flat* | *11.49* | | |

**By the letter of the rule fixed beforehand, it passed** — best-of-8 ended 0.165 above plain, above the 0.135 bar. **In substance it did nothing.** Best-of-8 sits a constant 0.07 above plain from the first tick to the last, with **no accumulation at all**. It never moves toward flat's 11.5. The rule compared end points, and a one-tick selection bump satisfies that; **the rule was poorly designed, and that is recorded rather than used.**

## Why nothing accumulates (C32)

**Each tick, about 58% of the slice is rewired** — measured on attempt 8's runs: 8,079 merges a tick among about 13,900 events. Half of all events have no children, by the offspring rule, and are merged away; the splits refill them.

**So whatever the selection achieves on one tick, the next tick largely erases.** The slice's shape has a memory of only a few ticks. **Weighting whole histories runs into the same wall**: the final slice's shape depends on its last few ticks, and those scramble the wiring. To move the shape, the weight would have to push hard on *every* tick — which is a strong, tuned, per-tick bias again.

## Where the turnover comes from (C33)

**The rewiring rate is set by how spread out the number of children is**, not by the average. ED's meaning is **"an average of one child"** — that's the balance, Budgeted Causality. **The particular spread** — half of events having none, some having several — **came from causal dynamical triangulations' known answer** in attempt 7's C1, where it was used to *check* the causal machinery against CDT.

**It was never decided as ED's meaning.** Same pattern as sync and the costs: a modelling choice nobody chose as the meaning.

**If most events had exactly one child**, the slice would change slowly, shape could build up over many ticks, and weighting — or even a gentle preference — would have something to work on.

> **Claude's reading, labelled:** the obstacle may not be the weighting at all, but that ED's growth churns most of every slice every tick. That churn comes from a choice of spread borrowed from CDT to test the machinery, not from ED's meanings.

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Decide what ED means by the spread of children.** If "average one, but mostly exactly one" is right, the slice keeps its shape across ticks — then rerun the conditions-only growth and see whether the shortcuts persist | The churn is the thing that erases every attempt to shape the slice. Cheap to test once decided |
| **(b)** | **Set the floor's clock-rate spread between 9.7 and 12.7 and build rewind-and-regrow anyway** | Tests H3 as specified, but S0-b says it's unlikely to accumulate while the churn remains |
| **(c)** | **Rethink "fewest directions"** so it doesn't rank stringy above small-world | Needed eventually if weighting is pursued |
| **(d)** | **Take stock of road H** before more compute | H1, H2 and H3 have each found something; a pause to see them together |

**Proposal: (a).** It's a meanings question, it's cheap, and the churn appears to sit underneath every failure since attempt 7.
