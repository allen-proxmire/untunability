# A flat reference at ED's link density: first try

*ED_Attempt_10, note 5. 2026-09-21 (RD5). Ledger: C11, C12, D5. Code `model/sa_flatref.py`; pilots in `model/sa_flatref_pilot.txt`. Expected results and exit rule in the code's header, written before running. Written plainly.*

## What you decided (D5)

Option (b) with (c) folded in: **compare only slices ED allows**, and **first make a flat reference at ED's link density** (6.699 links per event; the flat grid has 7).

## What I tried, and what happened (C11)

**The plan:** start from the flat grid and rewire it with flips, nudged toward fewer links, stopping the moment it reaches ED's link count. The aim was to disturb it as little as possible.

**The rule, fixed first:** the result counts as a flat reference only if it stays extended — its average distance within 5% of the grid's 11.49. If not, stop and report.

| nudge strength | reached ED's link count? | flips needed | average distance |
|---|---|---|---|
| 2 | no — links went *up* | — | 6.1 |
| 4 | yes | 271,000 | 8.5 (−26%) |
| 6 | yes | 225,000 | 9.0 (−22%) |
| 8 | yes | 218,000 | 9.0 (−21%) |
| 12 | no (ran out of attempts) | — | 9.7 |

**Every version that reached ED's density shrank by about a fifth.** Getting there by rewiring alone takes about 16 flips per event, and that much rewiring roughens the slice. **By the rule, none is a flat reference. So I stopped, and counted nothing on them.**

## A better way to build it (C12, proposal)

**Add events instead of rewiring.** Put a new event in the middle of some links of the flat grid, spread evenly. Splitting one of the grid's shorter links adds one event and five links, and five is below 6.699, so each split lowers the links-per-event. About 2,450 splits bring the grid to exactly ED's density, at about 16,270 events.

- **It's flat by construction:** putting a point in the middle of a link never creates a shortcut, so no distance can shrink. It's the same flat space, drawn with more points.
- **It's an allowed ED slice:** splits are ED's own move, and the result sits exactly at ED's link density.

**Revised rule, if you agree:**
- **Build check:** the structure check is clean, and links per event equals ED's 6.699 exactly.
- **Extended check:** no distance between two of the grid's own events has shrunk. This replaces the "within 5%" test, which assumed the number of events stays fixed.
- **Then the verdict:**
  - If the reference beats every grown slice by more than the stage A margin, **counting leans toward flat** — spec stage B in 3D.
  - If a grown slice beats it by that margin, **counting leans toward small worlds.**
  - Otherwise, take stock with you.

## A side finding (reported, not a test)

**The flat grid can't reach ED's link density by rewiring without getting rougher.** ED's grown slices got there another way: by losing events. They shrank to about 83% of their starting size (A9 C38). It hints that, at fixed size, ED's density sits nearer to rough slices than to smooth ones. That's only a hint.

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Build the reference by adding events, with the revised rule, and count it** (minutes) |
| **(b)** | Accept the rewired version anyway (distance −21%) as the reference |
| **(c)** | Stop here and take stock |

**Proposal: (a).**
