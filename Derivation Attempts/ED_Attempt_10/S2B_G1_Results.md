# Stage B, gate G1: the history-counting program is exact on rings

*ED_Attempt_10, note 15. 2026-09-21 (RD15). Ledger: C25, C26. Code `model/sb_core.py`, `model/sb_g1.py`, `model/sb_g1_exact.py`; outputs `model/sb_g1.json`, `model/sb_g1_run1.json`, `model/sb_g1_exact.json`. Written plainly.*

## The short answer

**Passed, exactly.** On ring-shaped slices small enough to list every possible history, **the program counts every history equally, reaches all of them, and gives each the right weight.** No statistics needed: it's checked move by move.

## How it got there (three fixes, all recorded)

| | what happened | fix |
|---|---|---|
| **1** | Rings of 4 events allow no change at all — a split and a merge together touch 5 events | Rings of 6 (then 5, below) |
| **2** | **The program reached only 13 of 49 possible histories.** A child on a link can belong to either end, and a merging event can fold into either neighbour. Same slice, different history — **and no move could switch that choice** | **Added a "swap" move:** pick a recorded change and switch which end is the parent or absorber. Slices unchanged; the move is its own reverse. Then all 49 were reached |
| **3** | The statistical test I'd written ("every history within 3 error bars") was too strict for 49 histories at once. Runs showed one or two near-misses at 3.1, with the overall spread exactly as expected for an unbiased program | **Replaced with an exact test:** list every state the program can reach, and check every move against its reverse. Rings of 6 had too many states to finish; **rings of 5** (the smallest with any change) worked |

## The exact result

| check | result |
|---|---|
| **Every move exactly as likely as its reverse** | **Yes** — 0 of 37,440 moves out of balance |
| **Every possible history reached** | **Yes** — 25 of 25, none extra |
| **Each history weighted correctly** (by its symmetries) | **Yes** — exactly |
| **Replaying each tick reproduces the next slice** (in the frequency runs) | **Yes** — every check |

## A side finding on the way to G3 (C26)

The **crowded start** has to have the same number of events and links as the flat reference. It's made by rewiring the flat reference at random, then bringing the link count back exactly.

**At ED's own link density, random rewiring only crowds the slice mildly:** average distance about 11% below flat (5.2 against 5.85 at size 12). Pushing harder breaks the step that returns the link count.

**Attempt 9's strong small worlds** (distance about 60% below flat) **came with the slice losing events**, which raised the links per event. With the event and link counts held exactly, as you decided (C-Q2, B-Q1), there may be much less room to crowd.

**That's a hint, not a result.** It also means G3 — whether the readings can tell the two starts apart — may need bigger sizes.

## Next

**Gate G2** (the 3D moves, checked every step, with regular replays of every tick), then **G3**. I'll report at each.
