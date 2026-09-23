# Growing forward with narrow moves: slower collapse, not stopped

*ED_Attempt_10, note 13. 2026-09-21 (RD13). Ledger: C23, D14. Code `model/p10.py` (attempt 9's growth tick with a narrow-merge switch), `model/n1_grow.py`, output `model/n1_grow.txt`. Expected results in the code's header, written before running; one revision after the first run, recorded before the rerun (below). About 45 minutes in all. Written plainly.*

## The short answer

**Mixed.**
- **Narrow moves slow the collapse a lot** — but growing forward, flat space still drifts toward a small world.
- **A small world still doesn't come back.**

**None of this tests counting.** Growing forward one step at a time doesn't weigh histories. **The real test is still stage B.**

## What was run

Attempt 9's growth (mostly one child, rewiring flips on, no costs) with **one change: narrow merges** — an event can only disappear by stepping back out from between two.

**Pre-run check:** with the change switched off, the new code reproduces attempt 9 exactly. The fast merge test agrees with the checked slow one on all 2,456 cases.

## The results (C23)

**Average distance between points**, every 10 ticks of 150:

| run | start | tick 0 | 20 | 50 | 100 | 150 | size at end |
|---|---|---|---|---|---|---|---|
| **N1, N2** | flat grid | 11.49 | 11.49 | 11.49 | 11.49 | **11.49** | 100% |
| **NF1** | flat reference | 11.59 | 9.64 | 8.61 | 7.20 | **6.51** | 93% |
| **NF2** | flat reference | 11.59 | 9.63 | 8.65 | 7.24 | **6.48** | 93% |
| **NW** | small world | 4.43 | 4.42 | 4.39 | 4.43 | **4.43** | 90% |
| *A9 H4, general merges* | *flat grid* | *11.49* | *5.82* | *5.13* | *4.73* | *4.55* | |

**The spacetime reading** (flat is 3.61): flat-grid runs 3.61; flat-reference runs 4.41; small world 5.26.

**All structure and budget checks were exact in every run.**

## What it shows

**1. The flat-grid runs stayed flat because nothing happened.**
- None of the grid's events can merge (none sits "on a link").
- It's over ED's link budget, so every split was refused — about 5,200 a tick.
- It has no spots for a paired flip.

So it was frozen — **the trap attempt 9 warned about.** My mistake: I reused attempt 9's grid start.

**Revision, recorded before the rerun:** added two runs starting from **the flat reference at ED's density**, which can actually change.

**2. From the flat reference, the collapse is about seven times slower, but it keeps going.**
- Attempt 9 fell from 11.5 to about 6 in **20 ticks**. Here it takes **150 ticks** to reach 6.5, and it's still falling.
- Growing forward, random rewiring still drifts toward the far more numerous crowded shapes.

**3. The small world stays a small world** — as expected, since growing forward has no counting in it.

**Against the expectations:**

| | expectation | result |
|---|---|---|
| **G1** | Structure and budgets exact | **As expected** |
| **G2** | Flat starts stay at 8 or more | **Not as expected** from the flat reference (6.5); met only by the frozen grid, which doesn't count |
| **G3** | The small world doesn't return | **As expected** |

The outcome falls **between** the pre-written readings ("stays within 10%" and "falls below 6"). **Recorded as "slower collapse, not settled."**

## What it means for stage B

**This was always only a hint; stage B is the test.** Growing forward weighs each slice by its options *once*. Counting whole histories weighs them **at every tick a slice lasts** (C15). With narrow moves, flat has the advantage at every tick (C22) — so counting has something to multiply, which forward growth doesn't use.

**Stage B's plan (note 7) needs updating for narrow moves:**
- **Paired moves stay exactly balanced:** a narrow split of a link with *k* tetrahedra around it paired with a narrow merge of the same *k* keeps the event and link counts exact.
- **The flat start is the flat reference at ED's density,** not the grid.
- Everything else as written.

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Update stage B's plan on paper for narrow moves,** then build it gate by gate |
| **(b)** | Take stock first |

**Proposal: (a).**
