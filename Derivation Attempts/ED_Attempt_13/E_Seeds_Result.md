# G2 settled: the line keeps something. The grid and the web don't keep anything from each other.

*ED_Attempt_13, note 7. 2026-09-23 (RD7). Ledger: C7. Code `model/g_seeds.py`, output `model/g_seeds.txt`, data `model/e_runs/seeds.json`. The rule G2a was fixed in the file before it ran. Written plainly.*

## The result

Ten seeds per start, same model, same settings, nothing else changed:

| start | reading | 95% interval | small world in | relations/event |
|---|---|---|---|---|
| **ring** | **4.10** | [3.94, 4.26] | **9 of 10** | 3.41 |
| **3D grid** | **4.58** | [4.48, 4.68] | 4 of 10 | 3.22 |
| **web** | **4.63** | [4.53, 4.73] | **2 of 10** | 3.18 |

Every run gave a reading — none were dropped, which matters, because silently excluding the runs that fail to produce a number would have biased this.

**G2a passes.** The ring's interval sits clearly below the 3D grid's, and below the web's. **With gradients, where a pattern starts still shows in where it ends.**

**But the 3D grid and the web are not distinguishable from each other** — a gap of 0.05 with overlapping intervals.

## What this does to attempt 12's convergence finding

**A12 C11 and C12 said every start converges on one end state. That is now half right, and the half that's wrong is specific.**

- **The line does not join them.** It stays measurably lower, at 4.10 against 4.58 and 4.63, and it stays a small world in 9 runs of 10 where the web does in only 2.
- **The 3D grid and the random web do converge**, on each other, and completely.

So the honest statement is: **ED's rules erase the difference between a lattice and a random web, but they do not erase the difference between a line and either of them.** A one-dimensional start keeps something that survives four-fold growth.

With noise rates, all three agreed to within 0.1 — the line's difference only appears once gradients are in.

## What it does not show

**None of these are dimensions.** 4.10, 4.58 and 4.63 with small-world flags set in most runs are readings from an instrument telling us there is no stable dimension to read. The starts are distinguishable *from each other*; none of them is three-dimensional, and the 3D-grid start is no more three-dimensional than the random web it converges with.

**And by paper 11's account (C6), that is expected in this regime** — all of these runs sit at about 3.2 relations per event, the thinnest participation the rules allow, which is exactly where ED says dimensionality is not defined.

## Recorded

- **G2 is established** and C5's caution is discharged.
- **A12 C11 and C12 are revised:** convergence holds between a lattice and a web; it does not hold for a line.
- The small-world flag separates the starts too, in the same order (ring 9/10, grid 4/10, web 2/10), which is a second reading pointing the same way and was not part of the pre-registered rule.
