# The boundary class: a literature map

*ED_Attempt_03, note 2. 2026-09-15 (RD2). Ledger: C7–C13, D1. A literature map with labelled reasoning; no model.*

## Allen's frame for this note (D1)

> "the attractor is the shape, like in Taos exponent database"

**Read as:** specific values aren't mainly *pulled in* by a flow. They're fixed by **the shape of what's allowed**, and they sit at its special boundary points: edges, corners, kinks. That's how the best-known exponents sit on the edge of the region in Tao's database (A2 note 1, X5D).

**This note tests that frame against the known boundary-type mechanisms.**

## The map

| mechanism | what it constrains | how a specific number comes out | status | ledger |
|---|---|---|---|---|
| **Consistency carves a region; real theories sit at its corners** (the conformal bootstrap) | Which combinations of a theory's numbers are mathematically consistent (symmetry plus positive probabilities) | The allowed region's edge has a **kink**, and the **3D Ising model sits right at it**. Its critical exponents come out precisely from sitting there | Established; precise numbers followed | C7 |
| **The vacuum sits at an edge** (near-criticality) | Whether our vacuum is stable, metastable or unstable | The measured Higgs and top masses put the Standard Model **near the stability boundary**. Froggatt–Nielsen *assumed* balanced vacua and got masses (A3 C2) | Near-criticality is measured; *why* it's there is open | C2 |
| **Dynamics drives parameters onto the edge** (self-organised localisation) | Parameters that depend on a field fluctuating during inflation | **Phase transitions act as attractors**, so parameters end up piled near the critical value and the universe sits at the edge of a transition. Proposed for Higgs near-criticality, the Higgs mass and the small cosmological constant | Proposed (2021) | C11 |
| **Horizons bound what fits inside** (holography) | How much information or energy a region can hold | The **de Sitter horizon's entropy** is its area in Planck units, which is 1/Λ, about 3 × 10¹²². Cohen, Kaplan and Nelson link a theory's shortest and longest length scales through black-hole limits, which **ties vacuum energy to the horizon size** | Entropy formula established; the link to Λ's size is a proposal | C8, C9 |
| **Consistency with gravity draws a border** (the swampland) | Which low-energy theories can come from a consistent quantum gravity | Conjectured edges, for example **the weak gravity conjecture**: some particle must have charge-to-mass ratio above an extremal black hole's. That gives inequalities, not exact values | Conjectures, actively tested | C10 |

## What the map says about "the attractor is the shape" (C12)

**Allen's frame fits the literature well.** It describes two known routes to specific numbers:

1. **The shape does the fixing.**
   - **The rule:** consistency conditions carve out an allowed region, and the real theory sits at a special point of its edge.
   - **Example:** the 3D Ising model at the bootstrap's kink is the cleanest case in physics.
   - **Tao's database works the same way:** the best exponents are corners of the allowed region.
2. **Dynamics drives things onto the edge.**
   - **The rule:** the attractor isn't a point inside the region; it *is* the region's edge.
   - **Example:** self-organised localisation, where phase transitions pull parameters to criticality.

**In Allen's relation–gradient–boundary terms:** the gradient ends *on* the boundary. The two classes aren't separate after all. Specificity comes from a flow whose resting place is an edge, or from consistency alone putting the theory on the edge.

**What a shape-type mechanism gives, and what it doesn't:**
- **Gives:** exact values, if the theory sits at a corner or kink.
- **Gives:** inequalities, if it only sits somewhere on a smooth edge. The weak gravity conjecture is like that.
- **Doesn't give:** anything, if nothing puts the theory on the edge.

## What it means for ED (C13)

**First, a necessary correction.** ED's "capacity of about 10¹²²" (A1 rebuilt draw) is the de Sitter horizon entropy, which is the cosmological constant written as 1/Λ. **ED took that number from observation, so it can't explain Λ.** Treating it as a source would be circular. The horizon may still *constrain* things, but its size can't be an output.

**Second, ED already has one shape-type result.** In attempt 2, the **fair coin turned out to be unique**: among all three-channel coins, only one (up to relabelling and phases) has all outcomes equally likely (Haagerup's classification). That's a theory sitting at a special point of an allowed region: an extreme, "maximally unbiased" corner of the space of coins. It's ED's closest thing to the Ising kink.

**So the natural next question inside ED:** if you write down the space of rules ED allows, do its own constraints push the actual rule onto special corners of that space? And do any of those corners fix numbers?

ED's own constraints include:
- mirror symmetry;
- conserving the total amount;
- no signalling;
- draws that fix only records;
- fair odds.

**Call it an ED bootstrap.** It's Allen's "the attractor is the shape", applied to ED itself.

**Cautions to keep in front:**
- **A corner is only a finding** if ED's constraints put the rule there *before* we look at what numbers come out.
- **Look-elsewhere applies:** with enough ways to carve a space, some corner will match something.
- **Constraints must be ED's own,** from its ledgers, not added to produce a corner.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(d)** | **ED bootstrap, part 1 (paper only):** list ED's constraints from the A1 and A2 ledgers, define the space of rules they act on (coins first), and map which rules they allow and where its corners are, with expected results written before any computation | Allen's shape frame, applied where ED already showed one corner (the fair coin) |
| **(b)** | **What ED's horizon constrains,** with its size taken as an input (not an output) | Still a real boundary ingredient, but its number is circular |
| **(c)** | **Counting in ED:** what ED forces to be whole-numbered | The relation-class route |

**Proposal: (d).**

**Update:** (d) part 1 is done ([ED_Bootstrap_Coins.md](ED_Bootstrap_Coins.md), note 3). **Correction:** the list above names "fair odds" as one of ED's own constraints. It isn't: it's attempt 2's working default (A2 D7). Note 3 separates ED's own constraints from the choices.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C7 | El-Showk, Paulos, Poland, Rychkov, Simmons-Duffin, Vichi, "Solving the 3D Ising model with the conformal bootstrap", *Phys. Rev. D* 86, 025022 (2012), arXiv:1203.6064; follow-up II (2014, c-minimization) | Abstract via search listing |
| C8 | Cohen, Kaplan, Nelson, "Effective field theory, black holes, and the cosmological constant", *Phys. Rev. Lett.* 82, 4971 (1999), arXiv:hep-th/9803132 | Abstract via search listing |
| C9 | Gibbons–Hawking entropy of de Sitter space (S = area/4 ∝ 1/Λ), as stated in arXiv:2510.24502; cosmic event horizon entropy about 3 × 10¹²² (arXiv:2412.11282, "A new census of the universe's entropy"); Bousso's D-bound, as stated in arXiv:1706.04434 | Search listings; original papers not read |
| C10 | Palti, "The swampland: introduction and review", *Fortschr. Phys.* (2019); Arkani-Hamed, Motl, Nicolis, Vafa, "The string landscape, black holes and gravity as the weakest force" (2007) | Search listings |
| C11 | Giudice, McCullough, You, "Self-organised localisation", arXiv:2105.08617 (2021) | Abstract via search listing |
