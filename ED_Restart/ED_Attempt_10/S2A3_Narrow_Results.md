# Narrow both ways: counting leans toward flat

*ED_Attempt_10, note 12. 2026-09-21 (RD12). Ledger: C22, D13. Code `model/sa3_count.py`, output `model/sa3_count.txt`. Checks, expectation and exit rule in the code's header, written before running; one fix to the merge test, caught by the first check (below). About 20 minutes. Written plainly.*

## The short answer

**Good news, and this time the moves are consistent.**

With **narrow moves both ways** — a child appears only on a link, and only such an event can merge back — **flat space has more ways to have come about in one tick than every crowded small world**, by 3 to 6.5 margins. The count is exact, with no estimates.

## What was tested

**Choice (i)**, which I'd set aside as "probably too rigid" without checking:
- **Split:** narrow, as before — a new child appears on a link between two events.
- **Merge:** narrow — an event can merge back only if it sits "on a link" in exactly that shape, so the merge is the exact reverse of a split.
- **Flips:** as before.

**Every move's reverse is a move**, so "ways to come about" and "ways to go on" are the same count.

## Checks

**N0 — splits and merges are exact reverses:**
- 204 merges undone exactly by a split; 1,655 splits each undone by a counted merge, on flat and grown slices.
- **Caught on the first try:** 30 merges didn't undo. My test let through events that touched the right neighbours but weren't wrapped round them in the right shape. **Fixed, and the check then passed exactly.**

## The results (C22)

| slice | per-event count | difference from flat reference | events able to merge | mean distance |
|---|---|---|---|---|
| **Flat reference** (ED's density) | 0.6493 | — | **15%** | 11.6 |
| Flat grid | 0.6504 | +0.001 | **0%** | 11.5 |
| Collapsed from flat, seeds 0, 1 | 0.6259, 0.6234 | **−0.023, −0.026** | 13–14% | 4.5 |
| Small world, seeds 0, 1 | 0.6064, 0.6028 | **−0.043, −0.047** | 14% | 4.4 |

- **Margin:** 0.007 (twice the seed-to-seed difference). **Every grown slice is below flat by 3.3 to 6.5 margins** — about e^270 to e^530 fewer ways per tick at these sizes.
- **Verdict, by the rule:** "narrow both ways: counting leans toward flat at one tick."
- **My expectation (about 65%): held.**

**Why flat wins:**
- **Crowded slices are jammed.** Their events average 17–21 allowed changes; flat's average 26.
- **Unevenness costs a little too.** With the total fixed, counting prefers events with even numbers of options.

## Is it "too rigid"?

**Not the way I feared.**
- The plain flat grid can't merge anywhere (0%). **But the flat reference at ED's density can merge at 15% of its events** — the ones sitting on links.
- The crowded slices sit at 13–14%.

So narrow moves don't freeze flat space any more than they freeze crowded space.

## What it means

Across road S, **one thing decides the outcome: what ED allows in one tick.**

| moves | consistent? | counting favours |
|---|---|---|
| Narrow split, general merge | no | can't be used |
| **General both ways** | yes | **crowded** (note 10) |
| **Narrow both ways** | yes | **flat** (this note) |

**Narrow both ways is the first ED-own, consistent rule under which counting pushes toward flat** — strongly, growing with size, and with no tuned strength.

**Not yet shown:**
- **One tick isn't whole histories.** Stage B would test that.
- **Forward growth with narrow moves hasn't been run.** Attempt 9's growth used general merges.

## Your decision

**Adopting narrow both ways would revise D10** (you chose general both ways on my proposal). It's your call what ED means. In plain terms: **a new event always appears between two existing ones, and an event can only disappear by stepping back out from between two.**

## Options (you decide)

| | option | why |
|---|---|---|
| **(a)** | **Adopt narrow both ways, then a quick forward-growth check** (as attempt 9's H4: flat start and small-world start, narrow moves, about 30 minutes), **then stage B** with narrow moves | The quick check shows whether the rule alone keeps or finds flat before days of stage B |
| **(b)** | Adopt it and go straight to stage B | Skips the cheap check |
| **(c)** | Keep general both ways and go to the layered step (road L) | If narrow doesn't feel like ED |

**Proposal: (a).**
