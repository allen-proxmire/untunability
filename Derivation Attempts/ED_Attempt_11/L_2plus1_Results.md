# The 2+1 test: results

*ED_Attempt_11, note 7. 2026-09-22 (RD8). Ledger: C10–C12. Code `model/st3.py`, `model/st3_run.py`; output `model/st3_run.txt`, `model/st3_runs/`. Expectations and outcomes in note 6, fixed before any code; revisions recorded before the run they affected. Written plainly.*

## The short answer

**Not settled — the two starts ended in different places.**
- **The flat start stayed spread out.**
- **The crowded start stayed crowded, and slowly got *more* crowded.**

By the rule: **"the starts disagree: not settled — take stock of the program."** It doesn't show that ED's rules give spread-out space in 2+1, and it doesn't show they don't. **But the direction of drift leans the wrong way, and there's a reason to question what we were reading** (below).

## How it went

1. **Built and independently reviewed.** A separate agent checked the program's moves and counting balance and found no errors. It caught three smaller problems, all fixed. (C10)
2. **Calibration passed at sizes 28 and 40**, after the planned sizes proved too small to read (recorded). (C10)
3. **First run invalid — my error.** The automatic tuning that holds the totals overshot: flat runs froze, crowded runs slid off ED's totals. Fixed by dropping the tuning; rerun. (C11)
4. **Second run: clean.** No check failures; totals within about 1% of ED's values throughout. (C12)

## The results (C12)

| run | distance across a sheet, start → end | spacetime reading, start → end | sheet sizes | changes accepted |
|---|---|---|---|---|
| Size 28, flat | 10.88 → 10.02 | 2.66 → 2.75 | 784–790 (hardly vary) | 2% |
| Size 28, crowded | 7.63 → 7.10 | 3.21 → too small to read | 727–917 | 9% |
| Size 40, flat | 15.55 → 14.22 | 2.74 → 2.81 | 1600–1607 (hardly vary) | 2% |
| Size 40, crowded | 8.00 → 7.69 | 3.52 → 3.82 | 1497–1678 | 9% |

**How sheet distance grows with size:**

| | growth rate |
|---|---|
| Flat start | **0.49** (a flat surface is 0.5) |
| Crowded start | **0.11** |

**Against the expectations:**

| | expectation | result |
|---|---|---|
| **P0** | Every step valid | **As expected** |
| **P1** | Calibration separates flat from crowded | **As expected** (after the size revision) |
| **P2** | Spread-out from both starts | **Not as expected** — only from the flat start |
| **P3** | The two starts agree | **Not as expected** |

## What it shows (my reading, labelled)

1. **The flat start barely moves at large scale.** Its sheets stay almost exactly the same size, and its distances settle after the first 50 passes and then don't change. **That may be the "nothing moved" trap again,** not a sign that flat is preferred.
2. **The crowded start moves about four times more, and drifts *away* from flat.** If the program is right and given time, that drift is the stronger signal — **and it points toward crowded.**
3. **A reason to doubt what we read.** In the rival theory's own spread-out phase, the spatial sheets are **not** smooth, flat surfaces: they're crumpled and fractal at small scales. The spread-out property is the **whole universe's shape at large scales** — how its size grows and shrinks over time — and that needs far bigger spacetimes than ours to see. **So "the crowded start stays crowded" may be exactly what the rival theory's spread-out phase looks like at these sizes.** If so, we've been testing for the wrong thing: smooth sheets rather than a large-scale shape.

**These readings can't tell 2 and 3 apart.** That needs the program run where the answer is already known.

## Options (you decide)

| | option | what it tells us |
|---|---|---|
| **(a)** | **Check the program against the rival theory's published numbers.** Run it as plain 3D CDT at couplings where they've published results (e.g. the (2,2)-share at a given coupling, and the universe's size-over-time shape), with our readings alongside. **About 2–3 hours** | **Whether the program is right, and what the rival theory's own spread-out phase looks like in our readings.** If its sheets read "crowded" too, our target was wrong, not ED |
| **(b)** | **Run the crowded start longer**, to see where its drift ends | Whether the drift toward crowded keeps going |
| **(c)** | Take stock of road L now | The 2+1 question is open |

**Proposal: (a).** It's the attempt 10 lesson from your primes work — show the instrument can see the known answer before trusting what it says about the unknown one.
