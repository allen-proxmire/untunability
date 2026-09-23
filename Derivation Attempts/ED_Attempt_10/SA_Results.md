# Stage A results: which way does counting lean?

*ED_Attempt_10, note 4. 2026-09-21 (RD4). Ledger: C8–C10, D4. Run `model/sa_count.py`, report `model/sa_report.py` → `model/sa_count.txt`: 13 slices plus the brute-force check, about 20 minutes. Expected results and exit rule in note 3 (C7), fixed before running; one revision, recorded before any result was read (below). Written plainly.*

> **Correction (note 8, C17):** these are counts of next steps. In 3D they differ from counts of how a slice came about, which weren't measured; the lean toward flat is withdrawn as a statement about histories.

## The short answer

**Mostly good news, with one catch.**

- **In 3D, the small worlds ED actually grows have far fewer ways to have happened than flat space.** Counting pushes **toward flat** — and strongly, by a factor of about e^600 to e^800 per tick at these sizes. **That push grows with the size of the slice.** It's the shape of the ingredient attempt 9 said was missing (A9 C41), and it comes from counting, with no tuned strength.
- **The catch:** the exit rule required flat to beat *every* other shape, including one artificial crumpled slice that ED's link budget doesn't allow. That one comes out level with flat. So the rule, as written, reads **"too close — build stage B small, in 2D."**
- **My expectation was wrong in 3D.** I expected counting to favour crammed shapes. For the shapes ED grows, it does the opposite.

## What was counted

For each slice, **how many different ways it could have been reached in one tick**: 10% of its events changing, each by one of ED's allowed moves (a split, a merge, a flip). Per event, then compared with flat.

## Checks (C8)

| | result | |
|---|---|---|
| **A0** | The counting matched a brute-force count **exactly** — every candidate change applied to a copy and kept only if the slice stayed valid — on flat, randomized and grown slices, 2D and 3D | **As expected** |
| **A1** | Every grown slice passed the structure and both budget checks at every tick; flat counts came out identical when repeated | **As expected** |

**One revision, recorded before any result was read:** the "flat, rewired" 3D slice couldn't be made. Paired flips need a spot where exactly three tetrahedra meet around a link, and the flat grid has none, so nothing moves and it stays identical to flat. It was replaced in the rule by attempt 8's calibration randomized slice. That slice is crumpled by single flips and **sits outside ED's link budget.** I picked it because it was the harder test for flat.

## The results (C9)

**3D** (flat has 13,824 events; "per-event difference" is against flat; negative means flat wins):

| slice | what it is | per-event difference | × size | mean distance |
|---|---|---|---|---|
| **Flat** | the flat grid | 0 | 0 | 11.5 |
| **Crumpled calibration** | single-flip randomized, off the link budget | **+0.005** | +66 | 6.0 |
| **Collapsed from flat**, seed 0 | grown as A9's F1 | **−0.052** | −598 | 4.5 |
| same, seed 1 | | **−0.054** | −626 | 4.5 |
| **Small world**, seed 0 | grown as A9's W1 | **−0.069** | −781 | 4.4 |
| same, seed 1 | | **−0.072** | −828 | 4.4 |

The seed-to-seed difference is 0.003, so the margin is 0.006. **Both grown shapes lose to flat by about ten times the margin. The crumpled calibration slice is level with flat, just inside the margin.**

**2D** (reported alongside; flat has 6,400 events):

| slice | per-event difference | × size |
|---|---|---|
| Randomized | +0.004 | +28 |
| Uniform-grown, seeds 0, 1 | +0.006, +0.005 | +37, +33 |
| Q1-grown, seeds 0, 1 | −0.0001, −0.0002 | −1, −1 |

In 2D, counting leans slightly **toward** the crammed shapes — as I'd feared for 3D.

**Exit, by the rule as written: "too close → build stage B small, in 2D."**

## What the numbers show (C10; my reading, not pre-registered)

**Why the grown small worlds lose: they're jammed.** Flat has about 40 allowed changes per event; the grown small worlds have 20 to 25.

- **Merges:** in a crammed slice, most merges fail the rule that keeps a slice from tearing (the link condition). Flat allows 14 per event; the small worlds about 3.7.
- **Splits:** crowded events sit at the 60-neighbour ceiling, which blocks splits around them.

**The unevenness itself matters much less.** Counting slightly prefers even slices, but most of the gap is the number of allowed moves.

**Why the crumpled slice ties:** its events have many neighbours but mostly stay *under* the ceiling. In 3D a split has one option per neighbour, so it gains on splits what it loses on merges. **ED's link budget forbids this shape** (A8 C22); it's in the test only because of the revision.

**Why 2D leans the other way:** attempt 7's 2D split picks a *pair* of neighbours, so its options grow with the square of the neighbour count, and crowded events win — the effect I warned about. **In 3D, ED's split picks one neighbour, and the effect goes away.** So the result depends on the move set — the split rule is part of what ED means.

**Honest limits:**
- **One tick is not whole histories.** This is the first factor of the full count. Whether the push toward flat beats the sheer number of small-world slices is what stage B would answer.
- **The flat grid isn't at ED's link density.** It has 7 links per event against ED's 6.699, so it isn't itself an allowed ED slice. The allowed-move gap (40 against 20–25) is far larger than that 4.5% difference could explain, but no flat slice at ED's density exists to check against.
- **The grown slices had shrunk** to about 83% of their start (A9 C38). Counts are per event, so that's handled, but it's recorded.

## Options (you decide)

| | option | why |
|---|---|---|
| **(a)** | **Follow the rule: build stage B small, in 2D** | As fixed before the run. But 2D is where counting leans the wrong way, because of its pair-split, so it's a poor stand-in for 3D |
| **(b)** | **Revise the rule** to compare only slices ED allows — drop the off-budget crumpled slice — then the 3D reading is **"counting leans toward flat" → stage B in 3D** | The rule's purpose was to test ED's allowed histories; the crumpled slice came in only through my revision. Recorded as a revision after the results |
| **(c)** | **First make a flat slice at ED's density** and recount | Removes the density confound before days of stage B |
| **(d)** | Pause on the split rule | 2D and 3D disagree because their splits differ; which split ED means is a meaning question |

**Proposal: (b) with (c) folded in.** Build stage B in 3D, and start by making a flat reference at ED's density. The 3D grown small worlds lose by a wide margin, and only a shape ED forbids ties.
