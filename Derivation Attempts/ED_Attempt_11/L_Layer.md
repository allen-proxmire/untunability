# Road L: ED's layer, written out

*ED_Attempt_11, note 4. 2026-09-22 (RD4). Ledger: C5, C6, D4. On paper, with a literature check; nothing computed except exact algebra. Written plainly.*

## What you decided (D4)

**Yes to L-Q1 through L-Q4:**
- An event reaches forward into a small patch of the next slice, and is reached from a small patch behind.
- The layer fills the gap between slices completely.
- The budget passes forward, split over all of an event's forward links.
- "Mostly one child" and the 10% limit are replaced by the layer itself.

## The layer, in pictures

**Two sheets**, slice *t* below and slice *t+1* above. Each is a 3D slice made of tetrahedra, with ED's exact event and link counts.

**Between them, a solid layer** built from 4D pieces. Every corner of every piece sits on one of the two sheets — nothing floats in between. There are four kinds of piece:

| piece | on the lower sheet | on the upper sheet | in words |
|---|---|---|---|
| **(4,1)** | a tetrahedron | one event | a floor tile with a point above it |
| **(3,2)** | a triangle | a link | a triangle below, a link above |
| **(2,3)** | a link | a triangle | the reverse |
| **(1,4)** | one event | a tetrahedron | a point below, a ceiling tile above |

**Rules of the weave:**
- **Every tetrahedron of the lower sheet** is the floor of exactly one (4,1) piece, and every tetrahedron of the upper sheet is the ceiling of exactly one (1,4) piece.
- **The pieces fit together with no gaps or overlaps**, so the layer is a proper slab of spacetime (L-Q2).
- **An event's forward patch** is the set of events above that it's linked to: a small solid ball of the upper sheet (L-Q1). Its backward patch is the same, looking down.
- **The event's budget is shared out over its forward links** (L-Q3).

**What replaces "children":** there's no single child any more. An event passes on to its whole forward patch. "Slices never split or merge" becomes "the layer between them is a proper slab."

## The counting: what ED already fixes (C5)

**The rival theory (CDT) keeps ten counts for a layered spacetime** (events, links, triangles, tetrahedra and pieces of each kind, in the slices and across the layers). **Seven exact rules tie them together, so three are free.** Their literature uses: the number of **events**, the number of **(4,1)-type pieces**, and the number of **(3,2)-type pieces**. **Each of CDT's three tuned settings weighs one of these.**

**ED already holds two of the three by its budgets:**

| total | held by | how |
|---|---|---|
| **Events** | the budget passed forward (Budgeted Causality) | directly |
| **(4,1)-type pieces** | the slice link budget | twice the number of slice tetrahedra — and ED's slice links fix the tetrahedra (A10 C2) |
| **(3,2)-type pieces** | **nothing yet** | — |

**The third is tied to one thing ED could naturally conserve — its forward links.** Solving CDT's seven rules exactly gives, per layer:

> **forward links = 2 × events + ½ × (3,2)-type pieces**

So **if ED conserves its forward links, as it conserves its slice links, all three totals are fixed.** ED would sit at **one point** on CDT's map, with **nothing tuned at all.**

**The flat value.** Take a flat slice and weave the simplest layer to a copy of itself: each tetrahedron's column cut into four pieces, one of each kind. Then (3,2)-type = (4,1)-type, and **forward links = events + slice links**:
- each event links **straight up** to its own continuation;
- plus **one diagonal link for every slice link.**

At ED's density that's **7.70 forward links per event.** In words: **an event passes on to itself and to one step along each of its links.**

## Where that point sits on CDT's map (C6; a rough reading, not settled)

CDT describes its phases by two ratios: **events per piece** and **(3,2)-type per (4,1)-type**.

- **The phases:** the spread-out phase (C) has a medium events-per-piece and a large (3,2)/(4,1). The collapsed phase (B) has both small. Phase A has many events per piece and a small (3,2)/(4,1).
- **ED's flat point:** events per piece **0.044**, and (3,2)/(4,1) = **1**.
- **A hard ceiling:** because ED's slices are at flat density (5.7 tetrahedra per event), events per piece **can't exceed 0.088** whatever the mix.
- **The comparison:** published CDT values are about 0.15 at the phase A–C boundary, and roughly 0.05 near the collapsed boundary (my reading of a plot's scale). **ED's point is at the dense end — near, but not clearly on, the collapsed side.**

**Honestly: I can't place it yet.** The published plots mostly show rescaled curves, not absolute values. **CDT's spread-out phase has spatial slices much less dense than flat** — around 3–4 tetrahedra per event, where flat is 5.7. **ED's flat-density slices may simply not match CDT's extended-phase slices.** That's either a warning or a clue.

## Questions for you (defaults proposed)

| | question | default | why |
|---|---|---|---|
| **L-Q5** | **ED conserves its forward links**, as it conserves its slice links | **Yes** | It extends the link budget to every link. It fixes CDT's last free total, so ED sits at one point with nothing tuned — *what CDT tunes, ED conserves*, all three |
| **L-Q6** | **At the flat value:** each event passes on to itself and to one step along each of its links (7.70 per event) | **Yes, labelled** | The same reasoning that set the slice links at their flat value. But see the rough reading above — this point may sit near CDT's collapsed side |

## What comes next (after your answers)

**First, find ED's point on CDT's map** — before building anything. Two ways:
1. **Literature, first:** look for published absolute values of CDT's two ratios in each phase, and see where ED's (0.044, 1) falls. Cheap.
2. **If that doesn't settle it:** run an existing CDT program, or build ED's layer into attempt 10's program, at ED's fixed totals, and look at the spacetime. **Days.**

**The picture for step 2**, as the ground rule asks:
- **What's built:** a whole ED spacetime — sheets joined by woven layers, all three totals held at ED's values.
- **What's read:** is time extended (a spread-out universe), collapsed onto one sheet (phase B), or are the sheets disconnected from each other (phase A)?
- **Spread-out** → ED's own conserved values land in the right place, with nothing tuned — **the result the project has been after.**
- **Collapsed or disconnected** → ED's flat values put it in the wrong phase; the next question is whether ED's slices really should be at flat density.

## Sources

- Ambjørn, Jurkiewicz, Loll, [Dynamically triangulating Lorentzian quantum gravity (hep-th/0105267)](https://arxiv.org/abs/hep-th/0105267), sec. 3.2: the ten counts and seven rules in 3+1.
- [Second- and first-order phase transitions in CDT (arXiv:1205.1229)](https://arxiv.org/abs/1205.1229): events per piece near 0.15–0.16 at the A–C boundary; the B–C order parameter.
- [The phase structure of CDT with toroidal spatial topology (arXiv:1802.10434)](https://arxiv.org/abs/1802.10434): the two ratios and their pattern across phases (Table 1).
- [Exploring the new phase transition of CDT (arXiv:1510.08672)](https://arxiv.org/abs/1510.08672).
