# Road L: what is one tick? On paper

*ED_Attempt_11, note 3. 2026-09-22 (RD3). Ledger: C3, C4, D3. On paper, with a literature check; nothing computed. Written plainly.*

## Your instinct (D3)

> "neighbourhood, like CDT, i think."

**When an event passes on, it reaches forward into a neighbourhood** of the next slice, not to a single successor.

## The picture

**Now (attempts 7–10), a relay race.** Each event hands its baton to mostly one successor, standing in the same spot. Two slices in a row are nearly the same slice with a few changes. Nothing between them has any shape of its own.

**Road L, a woven layer.** Two sheets of events, one above the other. Between them, a layer of links running up and across:
- **Each event on the lower sheet reaches up to a small patch** of the upper sheet — its forward neighbourhood.
- **Each event on the upper sheet is reached from a small patch** below.
- **The links fill the gap completely** — no holes, no overlaps — so the layer is itself a solid piece of spacetime.

**Why the layer matters:** there are many ways to weave a layer between two given sheets. **The number of ways depends on the sheets' shapes.** Counting histories, each sheet is weighed by how many ways it can be woven to the sheets before and after it. **In the rival theory (CDT), that weighing is what makes spread-out sheets win** — in its 3D version, with nothing tuned.

## How the rival theory builds the layer

(From the literature; sources below.)

| piece | in a 3+1 spacetime (ED's case) |
|---|---|
| **The building blocks** | 4D pieces of two kinds: **(4,1)** — a tetrahedron on one sheet plus one event on the other; **(3,2)** — a triangle on one sheet plus a link on the other |
| **The weighing of a sheet** | the number of ways to fill the layer between it and the next sheet — the **transfer matrix** |
| **What had to be tuned** | two settings: one for size (ED's budget already holds it), one for average curvature (**ED's link budget already holds it**, A10 C2), and **in 4D, a third, Δ — the balance between the two kinds of building block** |

**A possible connection** (reading, not claimed): attempt 10 found no slice total left for ED to conserve. **A layer brings new totals — how many of each kind of building block.** CDT's third setting, Δ, weighs exactly that mix. **If ED conserves the mix, as it conserves the budget, "what CDT tunes, ED conserves" could cover the third setting too.** That would be route (ii) from attempt 9 — something conserved that sets shape — reached through the layer. Untested.

## Questions for you (defaults proposed; nothing decided until you say)

| | question | default | why |
|---|---|---|---|
| **L-Q1** | **An event's forward links reach a small connected patch of the next slice, and each event is reached from a small patch behind** | **Yes** | Your "neighbourhood"; the CDT layer |
| **L-Q2** | **The forward links, with the links in both slices, fill the gap completely** — the layer is a proper piece of spacetime, no holes or overlaps | **Yes** | It's what makes "the number of ways to fill the layer" well-defined; it replaces "slices never split or merge" |
| **L-Q3** | **The budget passes forward along all an event's forward links** (split among them, as attempt 7 first wrote it: "each event splits its budget over its forward links") | **Yes** | Keeps Budgeted Causality; it's ED's own earlier wording |
| **L-Q4** | **"Mostly one child" and the 10% limit are replaced by the layer itself** — how different two slices can be is set by what a layer can join, not by a cap | **Yes** | Least structure: CDT needs no cap. And the cap is what froze attempt 10's histories |
| **L-Q5** | **Is the mix of building blocks conserved,** like the budget? | **Open — not proposed yet** | Needs the counting on paper first: which total, at what value, and whether ED has a natural one |

**L-Q4 revises D11 from attempt 9 and C-Q3 from attempt 10.** Yours to decide.

## What would come next (after your answers)

**On paper first:** write down ED's layer — which building blocks, which moves change a layer — and **count, for a small example, how many ways a flat sheet and a crammed sheet can each be woven to a copy of themselves.** That's the layer version of attempt 10's one-tick count. The tools from attempt 10 (the history-counting program, the flat and crowded starts) can be reused.

**The picture for that first test**, as the new ground rule asks:
- **What's built:** two identical sheets, one flat and one crammed, each with a layer woven to a copy of itself.
- **What's counted:** the number of ways to weave that layer, per event.
- **Flat wins** if a flat sheet has more ways → the layer favours spread-out space, and the whole-history test comes next.
- **Crammed wins** → the layer doesn't rescue ED on its own, and L-Q5 (a conserved mix) becomes the question.
- **Even** → the mix of building blocks decides it; L-Q5 again.

## Sources

- [The transfer matrix in four-dimensional CDT (arXiv:1302.1093)](https://arxiv.org/abs/1302.1093) — the layer ("sandwich") count as the transfer matrix.
- [Phase structure of CDT in 4D (arXiv:1704.00577)](https://arxiv.org/pdf/1704.00577) — the (4,1) and (3,2) pieces, and Δ weighing their mix.
- [CDT in Four Dimensions (arXiv:1111.6938)](https://arxiv.org/abs/1111.6938).
- [(2+1)-dimensional quantum gravity as the continuum limit of CDT (arXiv:0704.3214)](https://arxiv.org/abs/0704.3214).
- Carried from attempt 10: [Ambjørn, Jurkiewicz, Loll, hep-th/0105267](https://arxiv.org/abs/hep-th/0105267); [hep-th/0011276](https://arxiv.org/abs/hep-th/0011276).
