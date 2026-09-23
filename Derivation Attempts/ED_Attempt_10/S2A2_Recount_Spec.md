# The recount with general splits, on paper

*ED_Attempt_10, note 9. 2026-09-21 (RD9). Ledger: C18, D10. Specification only; nothing built or run. Written plainly; technical detail in the box at the end.*

## What you decided (D10)

**Choice (ii): general both ways.**
- **Split:** a child can take any group of its parent's neighbours that forms one connected patch. This is attempt 7's original wording (C3-Q6, "vertex splits"). It replaces the narrow "one neighbour's share" simplification (A7 C3c-Q1).
- **Merge:** any childless event can fold into a neighbour without tearing the slice, as before.
- **Flips:** as before.

**Now every move's reverse is also a move**, so the count of ways a slice *came about* equals the count of ways it *goes on*. One count covers both directions.

## What the recount asks

The same question as stage A, with the general split: **per event, does a flat slice or a crowded small world have more ways to have come about in one tick?**

## The hard part

The number of ways to split an event is **the number of ways to draw a closed loop through its neighbours**, dividing them into two patches, times two for which side the child takes.
- **Flat event** (about 14 neighbours): countable exactly, loop by loop.
- **Crowded event** (up to 60 neighbours): far too many loops to list. **Estimated** by sampling random partial loops — a standard method (Knuth's estimator) whose average is exactly right, with a stated error bar.
- **A shortcut that may decide it without estimating:** counting only the short loops gives a *floor* for crowded events. If the floor alone already puts the crowded slices ahead of flat, the answer is settled.

## The slices

The same 3D slices as stage A: **the flat reference at ED's density** (note 6), the flat grid, two collapsed-from-flat slices and two small-world slices (regrown exactly as before). 2D isn't redone — its moves were already each other's reverse, and it leaned crowded.

## Checks and expected results, fixed now

| | check | pass |
|---|---|---|
| **R0** | **Split and merge are exact reverses:** on small slices, every counted split, applied, gives a valid slice; merging the child back restores the original exactly; every allowed merge's reverse is among the counted splits | Exact |
| **R1** | **The loop count is right:** on small neighbour-patches, the loop count matches a brute-force count of every patch of triangles that forms a disc | Exact |
| **R2** | **The estimator is right:** on events whose loops can also be counted exactly, the estimate agrees within its error bar | Within 3 error bars |

**My expectation** (about 75% confident): **the crowded slices come out far ahead.** Crowded events have vastly more ways to split, and counting rewards that. If so, counting under choice (ii) leans the wrong way.

## What happens next, fixed now

Margin, as before: twice the seed-to-seed difference, **plus** twice the estimate's error per event.

| if | then |
|---|---|
| R0, R1 or R2 fails | A code problem; fix it and rerun, recorded |
| **Every grown slice is above the flat reference** by more than the margin (the floor may be enough) | **Record: "with general splits, counting leans toward crowded slices at one tick."** Stage B isn't built as specified. **Take stock of road S on paper with you** — counting has now been tried both ways |
| **The flat reference is above every grown slice** by more than the margin | **"Counting leans toward flat at one tick"** → build stage B with general splits |
| Otherwise | Too close → take stock with you |

## Cost

- **Code:** a few hours. It needs a fast loop counter and a new split move in the 3D model.
- **Runs:** under an hour, including regrowing the four grown slices.

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Run the recount as specified** |
| **(b)** | Talk through the expectation first |

**Proposal: (a).**

---

### Technical box

- **General vertex split** of x: choose a simple cycle C of length ≥ 3 in the link sphere Lk(x), and one of the two discs D it bounds.
  - The new child y takes the star tetrahedra whose link triangles lie in D, with x replaced by y.
  - New tetrahedra (x, y, p, q) are added for each edge pq of C.
  - Then Lk(xy) = C, y has degree |V(D)| + 1, x has degree |V(D′)| + 1, and each vertex of C gains one neighbour.
- **Validity:**
  - The ceiling (60) must hold for x, y and C.
  - The merge of y back into x satisfies the link condition by construction: a chord of C lies in only one disc.
  - Each (C, D) pair is one option; so a_split(x) = 2 × #cycles, minus the options the ceiling rules out.
- **Exact cycle count:** depth-first search with 64-bit masks (compiled), counting each cycle once (lowest vertex first, one direction), for degree ≤ 24.
  - **Floor:** cycles of length ≤ 8, counted exactly, for every vertex.
  - **Estimate:** Knuth's random-probe estimator (Knuth 1975) of the size of the cycle-search tree, for degree > 24. Each probe follows one random path, weighting by the product of branching factors; 20,000 probes per vertex; the error comes from the probe variance.
- **Per-slice count:** s = ln e_m(a) / V with m = round(0.1 V), as in stage A, where a_v = splits + merges + apportioned flip sites.
  - ln a_v enters through the e_m recursion.
  - Estimation error is carried to s by the delta method, with a conservative bound.
- **R0:** n = 6 slices (flat, and grown 30 ticks at q = 1): for every vertex, apply each counted split to a copy, run the structure check, merge back and compare exactly. For every allowed merge, confirm its reverse (C = Lk(va), D = the triangles of Lk(v)) is in the list.
- **R1:** for vertices of degree ≤ 10, enumerate all subsets of link triangles and keep those that form a disc with a simple boundary. This must equal 2 × #cycles, less the whole-sphere complement cases handled consistently.
- **R2:** at degree 18–24, compare the estimate with the exact count.
- **Literature:** D. E. Knuth, "Estimating the efficiency of backtrack programs", *Math. Comp.* 29 (1975) 121–136.
