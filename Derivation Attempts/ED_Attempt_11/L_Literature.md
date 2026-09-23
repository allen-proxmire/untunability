# Where ED's point sits on the rival theory's map: the literature check

*ED_Attempt_11, note 5. 2026-09-22 (RD5). Ledger: C7, C8, D5. Literature and exact arithmetic; nothing simulated. Written plainly.*

## What you decided (D5)

- **L-Q5:** ED conserves its forward links, as it conserves its slice links.
- **L-Q6:** at the flat value — each event passes on to itself and one step along each of its links.

**So all three of CDT's free totals are held by ED's own budgets, and ED sits at one point on CDT's map, with nothing tuned.** The literature check asked where that point is.

## The short answer

- **In ED's real case (3D slices, 4D spacetime): close to CDT's spread-out phase on one measure, not placeable on the other.** Suggestive, not settled.
- **In the simpler case (2D slices, 3D spacetime): ED's point lands inside CDT's spread-out phase, clear of the boundary.** In that case, **ED's current rules *are* the rival theory at a point where it gives spread-out spacetime — with nothing tuned.** That's the first time the project has had that, even in a simpler case.

## ED's real case: 3D slices, 4D spacetime (C7)

CDT's standard point in its spread-out phase is (κ₀, Δ) = (2.2, 0.6). From the main review, at that point:

| measure | CDT's standard spread-out point | ED's flat point |
|---|---|---|
| **(3,2)-type pieces per (4,1)-type** | **1.26** (from its volume table: total pieces are 2.26 × the (4,1)-type) | **1.00** |
| **Events per piece** | **not published as a number** that I could find | **0.044** |
| **Spatial slices' size scaling** | **3-dimensional** — distance grows like volume^(1/3) | ED's flat slices: 3-dimensional |

- **On the first measure, ED is close:** 1.00 against 1.26, the same neighbourhood. For comparison, the collapsed and disconnected phases both have this ratio *small*.
- **On the second, I can't place ED.** The only absolute value I found is about 0.15 at the edge of the disconnected phase, where the first ratio is small. That doesn't transfer to the standard point.
- **One constraint:** at CDT's standard ratio, events per piece can't exceed 0.074. ED's 0.044 is inside that range.

## The simpler case: 2D slices, 3D spacetime (C8)

Here the published answer is clean.

- **3D CDT has only two phases:** spread-out, and one where the slices come apart (decoupled). Its order parameter is τ, the share of layer pieces that are "link-below, link-above".
- **Spread-out phase:** τ is large — about 0.25 at the edge of the published plot, and larger deeper in.
- **Decoupled phase:** τ drops to nearly zero. The switch happens at one coupling value (6.64), and the spread-out phase covers the whole range below it.

**ED's point, from the same rules** (a flat 2D slice, and the flat layer "itself plus one step along each link"):

> **τ = 1/3 exactly.**

That's on the spread-out side, beyond the published curve's range and well away from the switch.

**So, in 2+1:** ED's rules — every allowed history counts once, the layer, and conserved events, slice links and forward links at their flat values — **amount to 3D CDT at a point inside its spread-out phase.**

**Honest limits:**
- **It's the simpler case, not ED's.** ED's case is 3+1, where CDT is harder (it needs its third setting in the right range).
- **τ = 1/3 is beyond the plotted range.** It's inferred to be spread-out because the curve rises steadily in that direction, and 3D CDT has no other phase there (its authors report a whole range of spread-out couplings, and later work sits at κ₀ = 1).
- **One real difference:** you decided every slice has exactly the same number of events (A10 C-Q2). In CDT, slice sizes vary, and their varying *is* the famous result — a universe that grows and shrinks like de Sitter space. With every slice fixed, that shape can't appear. See L-Q7 below.

## A question this raises (for you)

| | question | default | why |
|---|---|---|---|
| **L-Q7** | **Is only the total number of events conserved, with each slice's size free to vary** — rather than every slice exactly the same size? | **Yes (total only)** | Attempt 7's Budgeted Causality had slice sizes balancing around a value, not frozen at it. In CDT, the varying sizes are where the universe's shape shows up. **Revises A10 C-Q2** |

## What comes next (you decide)

| | option | the picture |
|---|---|---|
| **(a)** | **Run the simpler case first:** ED's 2+1 version at its own totals — the public 3D CDT program, or attempt 10's program with a layer added | **Built:** a stack of 2D sheets joined by woven layers, at ED's totals. **Read:** is spacetime spread out (sheets joined, a growing-and-shrinking shape if L-Q7 is yes), or do the sheets come apart? **Spread out** → confirmed in the simpler case, and the case for 3+1 is strong. **Apart** → the reading above was wrong. Probably a day or two |
| **(b)** | Go straight to ED's case, 3+1 | The same question in four dimensions. **Days, and much more code** |
| **(c)** | Decide L-Q7 first, then (a) | L-Q7 changes what the run can show |

**Proposal: (c) then (a).**

## Sources

- Ambjørn, Görlich, Jurkiewicz, Loll, [Nonperturbative quantum gravity (review, arXiv:1203.3591)](https://arxiv.org/abs/1203.3591): Table 2 (N₄ = 2.2625 × N(4,1) at κ₀ = 2.2, Δ = 0.6); Fig. 21 (N₀/N₄ ≈ 0.154–0.162 at the A–C transition); Fig. 40 (spatial slices d_H = 3 at κ₀ = 2.2).
- Ambjørn, Jurkiewicz, Loll, [Nonperturbative 3d Lorentzian quantum gravity (hep-th/0011276)](https://arxiv.org/abs/hep-th/0011276): the order parameter τ = N₂₂/N₃; transition at k₀ ≈ 6.64; Fig. 7.
- Ambjørn, Jurkiewicz, Loll, [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267): the counting identities.
- [The phase structure of CDT with toroidal spatial topology (arXiv:1802.10434)](https://arxiv.org/abs/1802.10434): the order-parameter pattern by phase.
- Brunekreef, van der Duin, Loll, [Simulating CDT quantum gravity (arXiv:2310.16744)](https://arxiv.org/abs/2310.16744): an open-source C++ program for 2D and 3D CDT.
- [acgetchell/causal-triangulations](https://github.com/acgetchell/causal-triangulations); [cdtea](https://github.com/JWKennington/cdtea).
