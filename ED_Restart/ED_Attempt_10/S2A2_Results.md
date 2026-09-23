# Recount results: with general splits, counting favours crowded slices

*ED_Attempt_10, note 10. 2026-09-21 (RD10). Ledger: C19, C20, D11. Code `model/sa2_count.py`, output `model/sa2_count.txt` and `model/sa2_count.log`. Checks, expectation and exit rule in note 9 and in the code's header, written before running; two changes to the R0 check, recorded (below). About 20 minutes. Written plainly.*

## The short answer

**Bad news for this route, and the one I expected.** Once a child can take any patch of its parent's neighbours, **crowded small worlds have far more ways to have come about than flat space** — by about e^15,000 to e^21,000 per tick at these sizes. **Verdict, by the rule: counting leans toward crowded slices.** Stage B isn't built as specified. **Next, by the rule: take stock of road S with you.**

## Checks (C19)

| | check | result |
|---|---|---|
| **R0** | Splits and merges are exact reverses | **Pass.** 10,024 sampled splits applied and undone exactly; 400 sampled merges, each reverse found among the counted splits and rebuilding the original exactly |
| **R1** | The loop count against brute force | **Pass**, 25 events, exact |
| **R2** | The estimate against exact counts | **Pass**, 12 events, all within 2.1 error bars |

**Two changes to R0, recorded:**
- **Sampling:** trying *every* split on a copy of the slice would have taken hours (a flat event alone has about 100,000). So R0 used 150 random loops per event, both sides, on 20 events per slice.
- **My test, not the counter:** the first reverse check compared against the wrong slice, and then wrongly rejected loops with shortcut links across them. Both errors were in the test. Fixed; the counter itself never changed.

## The results (C20)

**Ways to split one event:**
- **Flat event** (14 neighbours): about **100,000**.
- **Crowded event** (up to 60 neighbours): up to about **10^19**.

| slice | per-event count | difference from flat reference | mean distance |
|---|---|---|---|
| **Flat reference** (ED's density) | 1.54 | — | 11.6 |
| Flat grid | 1.48 | −0.07 | 11.5 |
| Collapsed from flat, seeds 0, 1 | 3.39, 3.36 | **+1.85, +1.82** | 4.5 |
| Small world, seeds 0, 1 | 3.00, 2.87 | **+1.46, +1.33** | 4.4 |

- **Margin:** 0.44 — twice the seed-to-seed difference (0.13) plus twice the largest estimation error (0.09). **Every grown slice is 3 to 4 margins above flat.**
- **The floor alone didn't decide it:** counting only short loops put flat ahead. Crowded events win on their long loops, and there are astronomically many of those.

**My expectation (about 75% confident): held.**

## What it means

**Counting has now been tried both ways, and it favours the crowded small worlds both times it's done consistently:**

| split | where it goes next | where it came from | consistent? |
|---|---|---|---|
| Narrow (one neighbour's share) | favours **flat** (stage A) | not counted; the general merge makes it favour **crowded** | **No** — the moves aren't each other's reverse |
| General (any patch) | favours **crowded** | favours **crowded** (the same count) | **Yes** |
| 2D (general) | favours **crowded** (stage A) | same | Yes |

**In plain terms:** crowded events have astronomically more ways to be arranged, and counting every way equally rewards exactly that. **This is the same wall as attempt 9, seen from the other side.** Small worlds win because there are more of them. Counting histories doesn't escape that under ED's moves; it counts them.

**Honest limits:**
- One tick, not whole histories. But the gap is in the thousands per slice, and the persistence argument (C15) only multiplies it.
- The crowded events' counts are estimates, with error bars up to their own size. The gap is thousands of times larger.
- This tests ED's moves as they now stand. A different kind of step between slices — like CDT's layers — isn't tested.

## What's next (by the rule)

**Take stock of road S with you, on paper.** It has now tried:
- conserved totals — none left to find (note 2);
- counting histories with ED's moves — counting favours crowded slices once the moves are consistent (this note).

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Take stock of road S on paper** — what it found, what it rules out, and what's left |
| **(b)** | Pause |

**Proposal: (a).**
