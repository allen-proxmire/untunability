# A mistake in stage A, found before building stage B

*ED_Attempt_10, note 8. 2026-09-21 (RD8). Ledger: C17, D8, D9-question. Reasoning, checked against the code; nothing run. Written plainly.*

## Your decision (D8)

B-Q1, B-Q2 and B-Q3: **yes to all three.**

## The mistake (C17)

**Stage A counted how many ways a slice can *change next*. Your meaning is how many ways it could have *come about*** — "a present is weighed by how many histories could have led to it." I said the two counts were the same, because every move is undone by another move of the same kind. **That's true in 2D but not in 3D.** I didn't check the 3D code closely enough.

**Why they differ in 3D:**

- **ED's 3D split is a narrow one** (attempt 7, C3c-Q1, which you agreed to): a new child can only appear *on a link* between two events, taking a thin slice of neighbours. There's **one way to do it per neighbour** — about 13 per event.
- **ED's 3D merge is a general one:** any childless event can fold into a neighbour, however its neighbours are arranged, as long as the slice doesn't tear.
- So **undoing a merge is a *general* split** — cutting an event's surrounding neighbours into two groups any way you like. That isn't ED's narrow split. **The two moves aren't each other's reverse.**

**Why it matters:** the number of ways an event could have *absorbed* a neighbour grows enormously with how many neighbours it has — roughly exponentially.
- A flat event with 14 neighbours: hundreds or thousands of ways.
- A crowded event with 60 neighbours: an astronomically larger number.

**So counting where a slice came from probably favours crowded slices strongly** — the opposite of what stage A found by counting where it goes next. When whole histories are counted, both directions matter, so **stage A's verdict only covers half the count.**

**A pointer that fits:** in 2D, the split and merge *are* each other's reverse (a 2D split cuts a ring of neighbours any way you like). And **in 2D, stage A leaned toward the crowded slices.** 3D leaned flat only because its split is narrow.

## What still stands

- Stage A's numbers are correct **as counts of next steps.** The brute-force check was exact.
- The flat reference and its comparison stand, **as next-step counts.**
- **The verdict "counting leans toward flat" does not stand as a statement about histories.** It's withdrawn until the other half is counted.

## The question this raises (for you)

**Counting histories needs every move to have its reverse among ED's moves.** Otherwise a history can come about in ways it can't go on in, and the program in stage B can't balance its counts. There are three ways to make ED's moves consistent:

| | choice | what it means | consequence |
|---|---|---|---|
| **(i)** | **Narrow both ways** | A child appears only on a link (as now), **and an event can only merge if it sits "on a link"** — the exact reverse | Stage A stands. But the grid's original events could never disappear; slices change only through flips and short-lived extra children. Probably too rigid |
| **(ii)** | **General both ways** | A child can take **any** group of its parent's neighbours (as attempt 7 first worded it, C3-Q6: "vertex splits"), and any childless event can merge (as now) | Matches attempt 7's original meaning. **Stage A must be redone**; the 2D result hints it may lean crowded |
| **(iii)** | **Keep both as they are**, and count the past and future separately | The narrow split and general merge stay | Stage B can't be built as specified; the counting would need a different design |

**My proposal: (ii)**, with a recount first. It's attempt 7's original wording, it treats splitting and merging alike, and it's the least special. The recount comes before any stage B code, because if it leans crowded, stage B isn't worth building as specified.

**What the recount needs:** counting the ways to cut an event's neighbours into two groups. For a flat event (14 neighbours) it can be counted exactly. For crowded events (up to 60) it can't be listed one by one, so it would be estimated. Its method and expected results go on paper first.

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Choose (ii), and spec the recount on paper** (general split both ways) |
| **(b)** | Choose (i) and build stage B with the narrow moves |
| **(c)** | Talk it through first |

**Proposal: (a).**
