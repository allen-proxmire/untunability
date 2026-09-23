# Taking stock of road S and attempt 10, in plain language

*ED_Attempt_10, note 20. 2026-09-22 (RD21). Ledger: C33, D19. Reasoning only; nothing computed. Updates the interim stock-take (note 11).*

## What attempt 10 asked

Attempt 9 ended with one missing ingredient: **something that prefers spread-out space strongly, and more so as the slice grows.** Attempt 10 asked: **where could ED get it?**

## What it found, one line each

1. **Nothing is left for ED to conserve.** A 3D slice has two free totals, and ED already conserves both at the flat values. *What CDT tunes, ED conserves* now covers both. (note 2)
2. **The rival theory (CDT) gets spread-out space by counting histories, not by a preference.** (note 2)
3. **Counting one tick gives exactly the kind of push attempt 9 wanted** — strong, growing with size, nothing tuned. **But which way it pushes depends entirely on what ED allows in one tick:**
   - **General moves both ways** (any split, any merge): counting favours **crowded** space, by a huge margin. (note 10)
   - **Narrow moves both ways** (a new event appears on a link, and leaves by stepping back out): counting favours **flat** space. (note 12) **You adopted these** (D14).
4. **Growing forward with narrow moves, flat space still drifts toward a small world — but about seven times slower** than attempt 9. (note 13)
5. **Crowded slices with ED's exact counts do exist** (note 16, after my first attempt at one was too weak).
6. **Counting whole histories: the tools work, but the histories don't move.** (notes 14–19)
   - The history-counting program is exact on rings, clean in 3D, and can tell flat from crowded.
   - **But in every run, flat histories stayed flat and crowded stayed crowded.** Counting fills every tick with short-lived back-and-forth changes, while the large-scale shape barely moves. Nothing I tried got a whole history to move.
7. **So under ED's rules, a slice's large-scale shape is extremely persistent.** Whatever shape a history has, it keeps for a very long time.

## What you decided

| | decision |
|---|---|
| **The rule** | A list of what's allowed; **every allowed history counts once** (D3) |
| **Links** | Only within a slice or to the next (D3) |
| **A history** | The spacetime itself — events, links, parents (D4) |
| **Counts** | Every slice has exactly the same number of events and links (D4, D8) |
| **Each tick** | At most 10% of events change; changes at separate places (D4, D8) |
| **Moves** | **Narrow both ways** (D14, replacing D10) |

**Flagged, not decided:** whether a single flip may ride in a link-balanced bundle (I read your link count as covering what pairing was for; D15).

## The wall, as it now stands

> **What ED allows in one tick decides which way counting pushes. With narrow moves it pushes toward flat, one tick at a time. Whether that wins over whole histories is still unknown, because under ED's rules the large-scale shape of a history hardly moves at all.**

**One reading worth keeping, not claiming:** if shape is that persistent, **the shape of space may be set mostly by where history starts, and then carried forward** — like commitment, passed on. That's close to your S1 hope (something carried forward sets shape), **but it's persistence, not a law:** growing forward, flat space still drifts, just slowly.

## What stands

- **Budgeted Causality**, now covering both slice totals.
- **Synced Now.**
- **ED can't crumple.**
- **Inputs supplied: still 3.** Nothing derived.

## What's open

- **Which shape whole-history counting prefers**, with narrow moves.
- **Road L:** a layered step between slices, like CDT's — the one known route that works by counting alone (in 3D).
- **The flip-pairing reading** (D15).
- **Amplitudes, roads R, I, D** — carried, untouched.

## What it cost

| | |
|---|---|
| **Compute** | about 12–15 hours |
| **Ledger** | 32 claims, 18 of your decisions, 20 recorded steps, 19 notes |
| **Claude's slips** | **One serious error:** claiming ED's 3D moves were each other's reverse, which inflated stage A's first verdict (C17). **Wrong expectations**, recorded each time: crowded would win at one tick in 3D; flat would stay above 8 growing forward; short loops would move. **Weak designs caught by their own checks:** a start that couldn't move (twice), a crowded start too weak, a statistical test too strict, a ring too small to change. **Smaller ones:** a capacity overflow, a reference one link off, two test-code mistakes, a first program too slow. **One judgment call:** dismissing narrow moves as "too rigid" without checking — they turned out to be the ones that favour flat |

## Options (you decide)

| | option | why |
|---|---|---|
| **(a)** | **Conclude attempt 10 and open attempt 11 on "what can happen in one tick?"** — the move set as ED's central meaning, with road L (a layered step) as the opening road | Attempt 10's question is answered as far as these tools can go: the move set decides the push, and narrow moves push toward flat. The next question is the step between slices itself |
| **(b)** | Stay in attempt 10 and keep trying to move whole histories | Open-ended; several approaches already stuck |
| **(c)** | Conclude attempt 10 and pause | Nothing in the record needs finishing |

**Proposal: (a).**
