# The flat reference at ED's density: counting leans toward flat

*ED_Attempt_10, note 6. 2026-09-21 (RD6). Ledger: C13, C14, D6. Code `model/sa_flatref2.py`, output `model/sa_flatref2.txt` (the first build's output kept as `model/sa_flatref2_miss.txt`). Checks and verdict in the code's header, written before running. Written plainly.*

> **Correction (note 8, C17):** the verdict below is about next steps only; the count of how a slice came about wasn't measured and probably favours crowded slices. Withdrawn as a statement about histories.

## The short answer

**Good news.** With a flat slice that ED actually allows — exactly at ED's link density — flat space still has far more ways to have happened in one tick than the small worlds ED's growth makes. **By the rule, counting leans toward flat.** Next step: plan stage B, the whole-history counting test, in 3D on paper.

## What was built

The flat grid, with **2,456 links split** — new events put in the middle of existing links, spread evenly. That brought it to **16,280 events at exactly ED's 6.699 links per event.**

| check | result | |
|---|---|---|
| **Structure** | clean | ✓ |
| **Exactly at ED's link density** | 109,054 links = target | ✓ (second build, below) |
| **Still flat** | no distance between two of the grid's own events got shorter; average distance 11.59 (grid 11.49) | ✓ |

**A miss, recorded:** the first build overshot by **one link** (109,028 against 109,027) and failed the density check. Splitting a short link always adds 5 links, and no number of those lands exactly on the target. **Fix:** three splits of longer links (+7 each) first; then it lands exactly. The first build's count had already printed (0.68888). The fixed build's count differs from it by 0.0001.

## The count (C14)

Per event, against the new flat reference (0.68874). The old grid read 0.69348.

| grown slice | difference | in margins |
|---|---|---|
| Collapsed from flat, seed 0 | −0.047 | 8 |
| Collapsed from flat, seed 1 | −0.049 | 8.5 |
| Small world, seed 0 | −0.064 | 11 |
| Small world, seed 1 | −0.067 | 11.5 |

Margin (twice the seed-to-seed difference): 0.006. **Every grown small world is far below flat. Verdict: "counting leans toward flat at one tick."**

**My expectation** (below the grid, above every grown slice) **held.** At ED's density, flat has about 38 allowed changes per event; the small worlds have 20–25.

## What it means

- **At one tick, counting gives exactly the kind of push attempt 9 said was missing:** strong, growing with the size of the slice, and with no strength tuned by hand. At these sizes, a small-world slice has about e^550 to e^770 fewer ways to have happened in one tick than a flat one.
- **Why:** crammed slices are jammed. Most merges there would tear the slice, so ED forbids them, and crowded events at the neighbour ceiling block the splits around them.
- **Not yet shown:** that the push wins over whole histories. There are vastly more small-world slices than flat ones, so the push has to beat their sheer number. **That's stage B.**

## Next (you decide)

| | option |
|---|---|
| **(a)** | **Spec stage B in 3D on paper**: count whole ED histories, with calibrations first, pass rules fixed before any code, and an honest cost (likely days to build) |
| **(b)** | Take stock of stage A first |

**Proposal: (a).**
