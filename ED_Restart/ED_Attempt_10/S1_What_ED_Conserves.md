# S1: is there something ED conserves that sets the shape?

*ED_Attempt_10, note 2. 2026-09-21 (RD2). Ledger: C2–C5. On paper plus a literature check; nothing computed. Written plainly.*

## The short answer

**No — but looking for one turned up something better.**

- **There's nothing left for ED to conserve.** ED already conserves every total a 3D slice has, and they're already set to the flat values. Totals can't tell spread-out space from a crammed small world: both have the same totals.
- **The rival theory (CDT) doesn't get its extended space from a preference either. It gets it from *counting*:** every allowed history counts once, and a slice's shape is weighed by how many ways it can join onto the slices before and after it. In its 3D version, that counting alone gives extended space across a whole range of settings, with no tuning of shape.
- **That's your idea already.** You said: *"to the present, any set of events that led to the present is possible."* And you decided ED weighs whole histories (A9 D9). **ED has never been run that way.** Attempt 9 weighed histories with a *preference* ("fewest directions") and picked the best — which isn't counting.

**Mixed, leaning good.** Route (ii) as I first put it is closed. But the missing ingredient may not be a preference at all. It may be the difference between *stepping forward* and *counting histories*, and that difference comes from ED's own meanings.

## 1. ED's totals are used up (C2)

A closed 3D slice made of tetrahedra has four totals: events, links, triangles and tetrahedra. Two rules of geometry tie them together, so **only two are free.** ED already conserves both:

| total | conserved by | set to |
|---|---|---|
| events | the budget passed forward (Budgeted Causality) | the starting size |
| links | the link budget | 6.699 per event — the flat value (A7 C66, C74) |

Those two fix the rest: 5.699 tetrahedra per event, and **exactly 5.104 tetrahedra around each link on average — the value for flat space.** So ED already holds its average curvature at flat by conservation, which is what CDT tunes a setting to do. *What CDT tunes, ED conserves* — for both of a slice's settings, not just size. Attempt 7 already saw this (C74). The new point is that **there's no third total to find.**

**Why totals can't set shape:** a total is a sum of local pieces. A crammed small world and a flat space can have exactly the same number of events, links and tetrahedra. The difference is in how the pieces are *arranged* at large scale, and no total sees that.

## 2. What the literature says (C3)

| finding | source |
|---|---|
| **Fixing the totals isn't enough.** In the older, non-causal version (Euclidean dynamical triangulations), holding average curvature fixed leaves only two kinds of space: crumpled (everything close to everything) or branched (thin tree-like). No extended phase | [Curvature and scaling in 4D dynamical triangulation](https://arxiv.org/abs/hep-lat/9407014); [Remarks on the quantum gravity interpretation of 4D dynamical triangulation](https://arxiv.org/abs/hep-lat/9608082) |
| **Causality changes the counting, not the preference.** In CDT, links join only events in the same slice or the next one, a slice never splits off "baby universes", and **the extreme crumpled and branched shapes can't even be built** | Ambjørn, Jurkiewicz, Loll, [Dynamically triangulating Lorentzian quantum gravity](https://arxiv.org/abs/hep-th/0105267), sec. 8 |
| **In 3D, counting gives extended space across a whole range.** "A whole range of the gravitational coupling" gives non-degenerate 3D spacetime, and the authors argue that coupling needs no tuning; one later study puts the edge of that range at about 3.3 and works at 1 | [Nonperturbative 3d Lorentzian quantum gravity](https://arxiv.org/abs/hep-th/0011276); Cooperman et al., [Scaling analyses of the spectral dimension in 3D CDT](https://arxiv.org/abs/1711.02685) |
| **In 4D it's harder.** A second balance (between two kinds of building block) has to sit away from a collapsed phase; at small values of it, spacetime collapses | [Studies of Critical Phenomena in CDT on a Torus](https://arxiv.org/abs/2303.13120); [CDT: Gateway to Nonperturbative Quantum Gravity](https://arxiv.org/abs/2401.09399) |
| **A graph-only cousin** (Trugenberger's combinatorial quantum gravity) gets geometry from a curvature weight with a tuned coupling — a preference, not counting | Kelly, Trugenberger, Biancalana, [Self-Assembly of Geometric Space from Random Graphs](https://arxiv.org/abs/1901.09870) |

## 3. Why ED hits the wall (C4, Claude's reading)

**ED's slices change by moves made inside each slice** — splits, collapses, paired flips — with nothing from the slices before or after weighing in. **That makes each slice the older, non-causal kind of ensemble at fixed curvature, which the literature says has no extended phase.** ED's neighbour ceiling rules out the crumpled extreme, so ED lands in between: the small world attempts 8 and 9 kept finding.

In CDT a slice never changes by itself. It changes only as part of the layer that joins it to the next slice, and **how many ways that layer can be filled is what weighs its shape.** That's where extended space comes from.

## 4. What this suggests (C5)

**Change what ED's rule is, not what it prefers:**

> **ED's rule is a list of what's allowed** — the budgets, the ceiling, no splitting or merging, links only within a slice or to the next one, mostly one child. **Every allowed history counts once.** A present is weighed by how many histories could have led to it.

- **No preference and no strength to tune.** Every setting is either conserved or already a labelled ED setting, so the census guard is satisfied.
- **The moves stop being physics.** Splits, collapses and flips become the tool for visiting histories, not ED's rule for the next step. Any set of moves that reaches every allowed history gives the same count.
- **This fits what you said:** once something has happened it's fixed, but many things could have happened, and the present doesn't know which.

**Honest limits:**
- The match between ED's settings and CDT's is my reading.
- In 4D, plain counting may sit on the collapsed side unless the second balance falls right. ED fixes its version of that balance through "mostly one child", but nobody knows where that lands.
- It's untested.

## Questions for you (defaults proposed; nothing decided until you say)

| | question | default | why |
|---|---|---|---|
| **S1-Q1** | **Is ED's rule a list of what's allowed, with every allowed history counting once** — rather than a recipe for the next step? | **Yes** | Your "any set of events that led to the present is possible" and A9 D9; it's the least structure (no preference, no strength) |
| **S1-Q2** | **Do links join only events in the same slice or the next one?** | **Yes** | ED already works this way; it's the causal condition that removes the extreme shapes in CDT |

## What would test it (S2, reshaped)

**Not "tune a strength" but "count histories":** a sampler that visits whole ED histories, each allowed one equally often, with ED's conserved totals held fixed. Then read the spacetime with the calibrated readings.

- **First with 2D slices** (a 3D spacetime), where CDT's answer is known — extended — as the calibration.
- **Then 3D slices.**
- **Cost:** days to build. Expected results and exit rule fixed with you on paper first.

## Options (you decide)

| | option | why |
|---|---|---|
| **(a)** | **Decide S1-Q1 and S1-Q2, then spec the counting test on paper** | The direct test of whether ED's own meanings supply the missing ingredient |
| **(b)** | Keep the old S2 (tune a strength) | Answers "does any strength work?", but adds a tuned setting |
| **(c)** | Pause and think about S1-Q1 | It changes what ED's rule *is*; worth sitting with |

**Proposal: (a).**
