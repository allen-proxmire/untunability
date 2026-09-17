# Route E-C as a shape

*ED_Attempt_04, note 12. 2026-09-15 (RD16, D24). Ledger: C68–C70. A paper argument; nothing computed. The meanings are Allen's accepted defaults E-Q1–E-Q5 (D24). The exit rule is note 10's draft, confirmed with the census guard added.*

## The method: the shape of efficiency (D23, C67)

**Three steps, in this order:**
1. **Name the quantity first,** from ED's meanings, before looking at the answer.
2. **Write the constraints** the meanings put on the thing being chosen. The constraints cut out a shape.
3. **See what's left** and where the quantity lands. Then count constraints against free parameters, so a fit would show.

**Here the thing being chosen is the dimension d of the pattern of relations.**

## The meanings used (all decided)

| | meaning | source |
|---|---|---|
| **M1** | The ball's "everything related identically" relations are sameness, not commitments. They carry no information | E-Q1 (D24) |
| **M2** | Dimension is read by **counting outward**: how many loci lie within n steps, for large n. Not by knots | E-Q2 (D24) |
| **M3** | A commitment, once made, never stops | E-Q3 (D24); A1 |
| **M4** | A particle is a closed loop of commitments that **can't be cut** and **can't pass through itself** | D14, D16 |
| **M5** | **No records are held.** What happened is reflected only in the present state | D21 |
| **M6** | "4 is never considered" means a fourth direction **leaves nothing the present keeps** | E-Q4 revised (D24) |
| **M7** | The only short-lived thing is **the uncommitted,** live until a draw | E-Q5 (D24) |

**One assumption, not a meaning** (the same one note 9 used):
- **S:** where counting outward gives d, the pattern is fine enough to behave like ordinary d-dimensional space for loops of commitments.

## Step 1: the quantity, named first

**Q(d): the number of distinct kinds of loop the present can carry,** where two loops are the same kind if one can be reshaped into the other without cutting or passing through (M4).

**Why this quantity:**
- **By M5, the present state is all there is,** so "what lasts" means "what the present keeps".
- **By M3 and M4, a loop can only be reshaped.** So what the present keeps about a particle is its kind.
- **It was named in note 11** as "lasting differences the present can carry", before this argument was written.
- **Honest caveat:** the knot facts were already known when it was named. This is a paper argument, not a blind test.

## Step 2: the constraints

| dimension | loops possible? | kinds the present can carry | fact |
|---|---|---|---|
| **1** | No closed loop fits without passing through itself | **0** | — |
| **2** | Yes | **1:** every loop reshapes into a circle | Jordan–Schoenflies (C44) |
| **3** | Yes | **infinitely many,** each permanent under reshaping | standard knot theory (C31) |
| **4 or more** | Yes | **1:** every loop reshapes into a circle | Zeeman: circles unknot when there are 3 or more extra dimensions (C68) |

**The requirement, the least that "a present that carries something" can ask:** the present carries **more than one** kind. That is, Q(d) ≥ 2.

**Two faces cut the shape:**
- **Lower face, d ≥ 3.** Below three, the present carries at most one kind. (Jordan–Schoenflies, and loops don't fit in one dimension.)
- **Upper face, d ≤ 3.** Above three, every kind relaxes into a plain circle. (Zeeman; C31.)

## Step 3: what's left

**The shape is a single point: d = 3.** In AD's words, the envelope is tight: two faces from two different theorems meet at one value.

**Where the quantity lands:** Q jumps from 1 to infinity at d = 3 and back to 1 above it. Three isn't a best compromise; **it's the only dimension where the present carries any difference of kind at all.**

**What "4 is never considered" now says exactly** (M6):
- **A region whose pattern counts as four-dimensional still has its commitments.** By M3 they never stop.
- **But every loop in it is the same kind.** So nothing distinguishable from that region survives into the present.
- **The fourth direction isn't forbidden. It just never leaves a mark the present can tell apart.**

**Census:**

| | count |
|---|---|
| Constraints on d | 2 independent faces |
| Free parameters | 0: no fitted numbers, no tuned rates |
| Inputs | 7 meanings (all decided), 1 assumption (S), 3 standard theorems |

**Nothing was fitted.** The census shows no fit. It doesn't show predictive power: there's only one unknown, and it's a whole number.

## The circularity check

- **Dimension is read by counting outward (M2),** not by knots. The knot facts are then theorems about loops in a pattern that counts as d-dimensional.
- **So it isn't circular,** but only because of assumption S. S is where the counted dimension becomes the dimension knot theory needs.

## The holes (C69)

| | hole | why it matters |
|---|---|---|
| **H1** | **Counted dimension vs. the dimension knots need.** A pattern that counts as 3 at large scales needn't be three-dimensional where particles live. Several programs find **about 2 at small scales** (C58, C59) | Knots live at small scales. If ED's pattern is about 2 there, E-C fails where it's needed. The smallest knot on a cubic grid takes 24 steps (C43), so a particle would have to span a region that already counts as 3 |
| **H2** | **It selects, it doesn't grow.** Nothing here says why the pattern grows three-dimensional across large regions rather than in patches | The emergence question itself (note 10), still open |
| **H3** | **Annihilation.** A kind can't change by reshaping, but particles annihilate. A knot and its mirror image can't untie each other without cutting (C55) | Either annihilation goes through what's uncommitted (M7), or a particle isn't only a knot. Open |
| **H4** | **One dimension everywhere.** Nothing says d has the same value everywhere | Part of H2 |

## The exit rule's verdict (C70)

**The rule** (note 10, confirmed): if the argument needs anything beyond the meanings, the E-Q answers and standard knot theory, or only restates note 9, record it as **"a reason from ED's meanings, consistent, not new physics"**; if it only works by defining dimension through knots, record it as **"circular"**. **The census guard:** free parameters must be zero, or the count must be shown.

**What it used:**
- the meanings M1–M7;
- one assumption, S;
- standard knot theory: Jordan–Schoenflies, knots in three dimensions, Zeeman.

**It isn't circular** (M2 with S). **It has zero free parameters.** **And much of it restates note 9,** with D21 added.

**Verdict: a reason from ED's meanings, consistent, not new physics.** The paper step stops here.

**What E-C adds beyond note 9:**
- **The present-state reading makes "4 is never considered" exact:** the commitments are kept, but no kind is distinguishable.
- **Three is shown as a shape:** a single point cut by two faces from two different theorems, with nothing fitted.
- **The holes are named.** H1 and H2 say where any later model would have to look: the small-scale dimension, and how a three-dimensional pattern grows.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C68 | Zeeman's unknotting theorem: piecewise-linear embeddings of an n-sphere in N-dimensional space are isotopic when N ≥ n + 3, so circles unknot in four or more dimensions (the smooth category has knotting in codimension three only for higher-dimensional spheres); as described in Zeeman talk notes (Glasgow), Manifold Atlas "Knots, i.e. embeddings of spheres" and "High codimension links", arXiv:math/0604045 | Search listings |
| — | C31, C43, C44, C55, C58, C59, C67 (this ledger) | This ledger |

**Update (D32):** ED has no infinities. In three dimensions the number of kinds of loop the present can carry is **many, as many as the loci allow,** not infinitely many (C88). It is still more than one only in three dimensions, so the shape is still the single point 3 and the verdict (C70) is unchanged.

**Update (C92):** annihilation conflicts with D14, which is carried into attempt 5 as needing revision. E-C's verdict stands as recorded, but rests on D14; whether it survives paired cut-and-rejoin (lead L1) is for attempt 5.
