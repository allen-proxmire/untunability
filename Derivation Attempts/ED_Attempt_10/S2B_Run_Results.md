# Stage B results: each start stayed exactly where it began

*ED_Attempt_10, note 17. 2026-09-22 (RD18). Ledger: C30. Code `model/sb_run.py` (rules in its header, fixed before running), output `model/sb_run.txt`, `model/sb_runs/`. Four runs, several hours. Written plainly.*

## The short answer

**Inconclusive.**
- **The flat histories stayed flat. The crowded histories stayed crowded.** Neither moved at all at large scale, from start to finish.
- **By the rule: "the starts disagree — not settled, or the program doesn't reach every history."**
- **So this doesn't tell us which one counting prefers.** It tells us the program can't move a whole history far enough, in the time we have, for the answer to show.

## The results

| run | average distance, start → end | spacetime reading (flat is 3.56) |
|---|---|---|
| size 12, flat | 5.85 → **5.82** | — |
| size 12, crowded | 3.63 → **3.63** | — |
| size 16, flat | 7.76 → **7.72** | **3.59** |
| size 16, crowded | 4.05 → **4.04** | **4.89** |

- **Distance growth with size:** flat runs 0.328 (flat is 0.327); crowded runs 0.126 (small worlds about 0.12–0.15).
- **Checks:** none failed — structure, both counts and every replay were exact throughout.
- **Activity:** 20% of proposed changes were accepted from flat, 7–8% from crowded.
- **"Settled"** by the rule's test — but trivially: **nothing changed to settle.**

## Why nothing moved (my reading)

**The slices are tied to each other round the loop.** Each slice can differ from its neighbours by at most 10% of its events (your "mostly one child"), and the 32 slices close into a loop. To reshape the history, every slice has to move together, a little at a time, while each stays within 10% of its neighbours. **The program changes one slice at a time, so the history's overall shape moves extremely slowly** — like dragging a long chain one link at a time.

**Growing forward (note 13) wasn't tied like this:** each tick's changes simply added up, so flat drifted within tens of ticks.

**So "nothing moved" can mean either:**
1. **The program is too slow to reach the answer** — the likely reading; or
2. **Counting really does hold each start in place** — which would itself be strange, since counting has one preferred answer, not two.

**These runs can't tell them apart.**

## What this means for road S

- The tools are sound: exact on rings (G1), clean in 3D (G2), able to tell flat from crowded (G3).
- **The question stage B asked is still open.** One-tick counting under narrow moves favours flat (note 12); whether whole-history counting does is unanswered.

## Options (you decide)

| | option | what it tells us |
|---|---|---|
| **(a)** | **A quick diagnostic with short loops** — 4 slices instead of 32, size 12, both starts, about an hour. With a short loop, the whole history can move much faster | **If the two starts meet with short loops, the long runs were just too slow** — and where they meet is the first real answer, at short loops |
| **(b)** | Longer runs, as the rule says | Probably pointless: nothing moved at all in 200–300 passes |
| **(c)** | Take stock of stage B and road S now | The tools work; the question is open |

**Proposal: (a).**
