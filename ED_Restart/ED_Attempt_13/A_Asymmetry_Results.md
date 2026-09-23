# The asymmetry, explained — and it is duller than it looked

*ED_Attempt_13, note 12. 2026-09-23 (RD12). Ledger: C14, C15. Code `model/a_asym.py`, `model/m_mech.py`; outputs `a_asym.txt`, `m_mech.txt`. All rules fixed in the files before they ran. Written plainly.*

## What was being chased

C11 said: **ED's growth carries a line perfectly and degrades a cubic grid**, and I added the striking sentence that ED's growth is hardest on exactly the shape the project wants. Two tests were built to kill that sentence if it deserved killing. It did, though not for the reason I guessed.

## First: my explanation was wrong

**The guess:** three dimensions has a weaker signature to begin with — the gap above its lowest modes is about 2, against about 4 for a ring — so any blurring destroys it sooner.

**Test:** blur clean shapes with local rewiring and see which loses its reading first.

| shape | survives local re-pointing of… |
|---|---|
| flat torus | **100% of its relations** — still reads exactly 2.0 |
| cubic torus | **100%** — still reads exactly 3.0 |
| ring | **fails at 5%** |

**Exactly backwards.** Three dimensions is the *robust* one; the ring's signature depends on its loop staying intact and breaks almost immediately. Yet under ED's growth the ring survives 16 of 16 and the cubic torus fails 7 of 8.

*(The first version of this test used long-range rewiring and destroyed every shape at 2%, telling us nothing. Recorded, and replaced with local rewiring, which is what ED's growth actually does.)*

**And thickness isn't the cause either:** a clean cubic torus reads exactly 3.0 at 6, 12, 25 and 50 relations per event; a clean ring reads exactly 1.0.

## Second: the mechanism test, and what it actually found

**The hypothesis:** when a parent has two children, its neighbourhood is split between them **at random**, and that decoheres the three directions a little each generation. A ring wouldn't care — a loop split any way is still a loop.

**Test:** the same growth, one line different — children paired **by index** so a neighbourhood passes on consistently. Read every third generation.

| arm | generation 0 | 3 | 6 | 9 | 12 | 15 |
|---|---|---|---|---|---|---|
| **random** (gap) | 2.00 | 1.77–1.82 | 1.68–1.76 | 1.63–1.73 | 1.08–1.73 | 1.56–1.68 |
| **coherent** (gap) | 2.00 | 1.78 | 1.62–1.73 | 1.55–1.66 | 1.53–1.58 | 1.51–1.56 |

**M2 fails. Coherent pairing does not rescue three dimensions** — it loses the reading in all three seeds, and if anything slightly sooner. **M1 fails too:** one random seed kept 3.0 the whole way.

**So random splitting is not the cause.**

## What the numbers actually say

**Both arms show the same thing: the gap decays smoothly with growth**, from 2.00 at the start to about 1.55 after fifteen generations. The group of six modes is still there — what widens is the spread *within* it. **The reading doesn't collapse; it blurs.**

And the ring does the same: its gap drifts from 4.00 down to 3.4–3.9 over comparable growth. **In relative terms the two decay at similar rates** — about 20% for the cubic torus, about 15% for the ring.

**The difference is the starting margin and where my bar sits.** The ring starts at 4.0 and never comes near the threshold. The cubic torus starts at 2.0 and crosses it. **My pass/fail rule turned a smooth, common decay into a dramatic-looking asymmetry.**

## The honest statement

> **ED's growth gradually blurs directional structure — at a similar relative rate whatever the dimension. A one-dimensional signature starts with twice the margin and survives; a three-dimensional one starts with half and does not.**

**C11's sentence is withdrawn.** ED's growth is not hostile to three dimensions specifically. It is corrosive to *all* directional structure, and three simply has less room before a threshold I chose.

## What survives all of this

- **Nothing creates a dimension.** 16 runs from a random web, two sizes, no structure at all. Untouched by any of this.
- **ED's growth degrades directional structure as it grows.** New, measured in two arms and three seeds, and stated as a constraint rather than a mechanism — which is what D3 asks for.
- **ED's own instrument works**, and a clean lattice reads its dimension exactly at every thickness, which is the calibration that made all of this legible.

## What I got wrong today, in order

1. Claimed the thick regime preserves a dimension exactly — **withdrawn**, it was three seeds counted nine ways.
2. Claimed ED's growth is hardest on the shape the project wants — **withdrawn**, it is hardest on everything, and three has less margin.
3. Guessed the cause was random splitting of neighbourhoods — **wrong**, coherent splitting does the same.

All three were caught by tests written to catch them, and the negative result at the centre — *nothing creates a dimension* — is the one that has survived every attempt to break it.
