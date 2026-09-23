# Road R5, part 3: why knots of commitments need three dimensions

*ED_Attempt_04, note 9. 2026-09-15 (RD9, D14–D16). **K2′ confirmed (D16).** Ledger: C43–C49. A paper argument; nothing computed. The exit rule drafted in note 7 applies.*

## Allen's decision (D14)

> "yes, a particle is a knot of commitments that can't be cut"

## The meanings the argument uses

| | meaning | source |
|---|---|---|
| **K1** | A particle is a **closed, knotted loop of commitments** | D14 |
| **K2** | **No commitment in the loop can be cut,** by what a commitment is | D14 |
| **K2′** | **The loop can't pass through itself.** In knot theory, passing one strand through another is equivalent to cutting and rejoining, so "can't be cut" has to include this | **Confirmed by Allen (D16)** |
| **S** | Space is the emergent pattern of relations (D11), with some number of dimensions *d*, and fine enough that a loop of commitments behaves like a curve | Assumption |

## The knot facts it uses (C31, C43, C44)

| dimensions | fact | source |
|---|---|---|
| **2** | **No knots.** Every non-crossing loop in a plane can be reshaped into a circle (Jordan–Schoenflies) | C44 |
| **3** | **Knots exist and keep their type.** A trefoil can't be turned into a plain loop, or into a figure-eight, without cutting or passing through itself. There are infinitely many distinct types | standard knot theory |
| **4 or more** | **Every knotted loop can be untied** without cutting or passing through itself; there's enough room to slip strands around each other | C31 |
| **On a grid** | **Knots exist on discrete grids too.** On a cubic grid the smallest knot takes 24 steps, and it's a trefoil. The figure-eight takes 30, the five-pointed star knot 34 | C43 |

## The argument (C45)

1. **By K2 and K2′,** a particle can only change by **reshaping**: no commitment is cut, and no strand passes through another.
2. **By K2, the loop's commitments are never removed.** So a loop of commitments lasts **in any number of dimensions**. Existence doesn't depend on dimension.
3. **What does depend on dimension is the particle's kind,** meaning its knot type:
   - **in 2 dimensions,** every loop can be reshaped into a plain loop, so **there's only one kind**;
   - **in 3 dimensions,** there are **infinitely many kinds** (trefoil, figure-eight, …), and **each is permanent**, because reshaping can't change it;
   - **in 4 or more dimensions,** every loop can be reshaped into a plain loop, so **kinds don't last**. Effectively there's one kind again.
4. **So only in three dimensions do K1 and K2 give many distinct kinds of particle, each kind permanent.**

**In Allen's words, "3 is stable".** Three is the only dimension where a particle's kind is protected by its own shape. And "4 is never considered" fits too: in four dimensions, knotted particles can't keep their kind, so a world of lasting kinds never "sees" four.

## What it doesn't show (C46)

- **It doesn't show that space *grows* three-dimensional.** It shows that *if* particles are uncuttable knots, lasting kinds of particle exist only in three dimensions. That's a selection ("a world of lasting particles must be 3D"), not a derivation of how relations become 3D space. The hard emergence step, the one causal dynamical triangulations struggles with, is untouched.
- **It doesn't say which knot is which particle.** Pairing knot types with particles is Kelvin's trap, and nothing here licenses it.
- **It doesn't give spin, charge or mass.** Finkelstein–Rubinstein says tethered objects in 3D *can* be fermions (C29). That's compatible, but not derived here.
- **In 4 dimensions, untying is *possible*, not forced.** A knotted loop there could still last a while if something holds it. The argument only says topology alone doesn't protect it.
- **Discreteness is assumed away.** Knots exist on grids (C43), but that ED's emergent space is fine enough, and that ED's allowed moves match smooth reshaping, is assumed, not shown. One suggestive side note: on a cubic grid, the smallest knotted particle would need at least 24 loci. That's an association, not physics.

**K2′ is confirmed (D16).** It sits alongside D1 without conflict: D1 says a body's own presence doesn't block its own processes (clocks), and K2′ says a knot's own strands can't pass through each other (shape).

## The exit rule's verdict (C49)

**The rule (note 7):** if the argument needs anything beyond the two meanings plus standard knot theory, or only restates the knot theorem with ED labels, record it as **"a reason from ED's meanings, consistent, not new physics".**

**What it used:**
- **the two meanings** (K1, K2);
- **one reading of them** (K2′);
- **standard knot theory;**
- **one assumption** (space fine enough to behave like a continuum).

**Verdict: a reason from ED's meanings, consistent, not new physics.**

Under D12 that's the expected kind of outcome: **ED gives a reason why three dimensions, from what a particle and a commitment are, without changing any experiment.**

## Allen's pictures (D15)

### "If you define a force as carried by a particle, gravity isn't a force" (C48)

- **Physics agrees with the split.** Electromagnetism, the weak force and the strong force are carried by particles: the photon, the W and Z, the gluons. Gravity's carrier (the "graviton") has never been observed, and general relativity treats gravity as geometry, not a carried force.
- **ED's picture already makes this split:** gravity is *influence*, not presence (D2). So in ED's own terms there are **exactly three carried forces**. That's a consistency.
- **What stays open:** tying those three to three dimensions still needs a rule for why each carried force would need its own independent direction.

### The 45° cones (C47)

**Made precise in the simplest way:** put a cone of 45° half-angle, the speed-of-light slope, around each space axis, and ask whether the cones overlap and whether they fill all directions.
- **They never overlap, in any number of dimensions.** Being inside two cones would need more than half of a direction's "length squared" along two axes at once, which is impossible.
- **They fill all directions only in 2 dimensions.**
  - **In 2D,** the four 45° wedges tile the plane exactly.
  - **In 3D,** the diagonal direction (equal parts x, y and z) sits about 54.7° from every axis, outside all three cones.
- **Cones wide enough to fill 3D (54.7°) overlap; cones narrow enough not to overlap (45°) leave gaps.** So "fill without overlap" happens only in two dimensions.

**Honest reading:** as a picture in ordinary space, the cones pick **2**, not 3. **But Allen described a spacetime graph,** with a time axis and light cones at 45°. That's a different picture, and it isn't pinned down enough to test: which axis does each force's cone go around? **Worth sketching before deciding it's gunk.**

**Update (D17, D18):** sketched in [Cone_Sketch.html](Cone_Sketch.html). In Allen's corner picture, round cones leave gaps (at best about 79% covered), while square pyramids tile exactly with 45° walls, but do so in every dimension (C50, C51). Allen's point that rotation does not: d(d−1)/2 ways to rotate match d axes only in three dimensions (C52).

**Update (RD12):** using knots to select three dimensions is published: in 'Knotty inflation' (2017), knotted flux tubes drive inflation only in three space dimensions (C54). The facts that pick three are grouped by root, with what differs in ED and the annihilation poke, in [Attempt_04_Plain_Language.md](Attempt_04_Plain_Language.md) Part 6 (C55).

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Confirm K2′:** a knot's strands can't pass through each other (part of "can't be cut") | The argument rests on it |
| **(b)** | **Describe the spacetime cone picture** (which axis each force's cone sits on, and what "fill" means), so it can be made precise | The spatial version picks 2; the spacetime version is untested |
| **(c)** | **Consolidate attempt 4:** a plain-language write-up of the picture, roads R1, R2 and R5, and the knot argument | A natural point to take stock |

**Proposal: (a),** then **(c).** (b) is welcome whenever the picture is clearer.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C43 | Diao, "Minimal knotted polygons on the cubic lattice", *J. Knot Theory Ramifications* (1993): the minimum is 24 steps, trefoil only; figure-eight 30 and 5₁ 34; counts of minimal trefoils, as described in "The number of smallest knots on the cubic lattice" (*J. Stat. Phys.*), arXiv:1411.1845, UBC "Minimal knotted polygons in cubic lattices" | Search listings |
| C44 | Jordan–Schoenflies theorem: a simple closed curve in the plane can be mapped onto a circle by a homeomorphism of the plane, as described in Cairns, "An elementary proof of the Jordan–Schoenflies theorem" (*Proc. AMS*, 1951), Wikipedia "Schoenflies problem" | Search listings |
| — | C29, C31 (earlier notes) | This ledger |
