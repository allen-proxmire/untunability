# Does gravity's own energy gravitate? The Nordtvedt check

*2026-09-14. Ledger: C206–C208. Follows [Budget_Spreading.md](Budget_Spreading.md).*

## The question

**A planet is held together by its own gravity, and that binding energy counts toward its mass.**
- **In general relativity, all energy pulls and is pulled the same way,** including gravity's own binding energy, the energy of motion, pressure and the internal energy of atoms.
- **If some kind of energy didn't pull (or wasn't pulled) the same way, the Earth and the Moon would fall toward the Sun slightly differently.** The Earth has much more gravitational binding energy for its size (4.6 × 10⁻¹⁰ of its mass, against 0.2 × 10⁻¹⁰ for the Moon).
- **That difference would make the Earth–Moon distance wobble** in step with the Sun, by 13.1 × η_N metres, where η_N measures the violation (C206).
- **Lunar laser ranging times light pulses bounced off mirrors left on the Moon,** to millimetres. It gives |η_N| = (4.4 ± 4.5) × 10⁻⁴: no wobble, down to about a centimetre (C206).

## What ED's budget counts, and what that implies (C207)

**ED's budget is linear:** U just adds up contributions from wherever mass is committed. It doesn't feed back on itself. Using the standard post-Newtonian bookkeeping, I worked out what that implies under two readings of "what the budget counts" (`checks/pn_sourcing.py`, predictions frozen before running, all as predicted):

| reading | Nordtvedt η_N | Earth–Moon wobble | other tests |
|---|---|---|---|
| **A. Only rest mass counts** (RD14 as written) | **3.3** | **about 44 m** | **Fails** Newton's third law for different materials (lunar test, 4 × 10⁻¹²) and the binary pulsar test |
| **B. All commitment counts** (rest, internal energy, motion, gravitational binding), still linear. Closer to "mass is concentrated commitment" (D7) | **2.8** | **about 37 m** | Passes the materials test; **fails** the binary pulsar test (ζ₂) and a combined bound (ζ₁) |
| **What GR needs** | 0 | none | Passes |

**Measured: less than about a centimetre.**

**In plain words:** a budget that simply adds things up, whatever it counts, **gets the Earth and Moon wrong by a factor of thousands.** It also fails other tests (the binary pulsar, and Newton's third law between materials) by even more.

**Why simple counting can't work.** In general relativity, gravity's own energy and the motion of the sources pull *more* than simple counting gives. The post-Newtonian "weights" GR needs are 4 for motion (counting gives 1), **+4** for gravitational energy (counting gives −1, because binding energy is negative), 2 for internal energy (counting gives 2) and 6 for pressure (counting gives 0). **Those weights come from gravity feeding back on itself,** which a linear budget doesn't do.

**Honest limits:**
- This maps ED's effective gravity onto the standard framework as if it fitted there, and assumes ED has no preferred-frame or velocity-dependent terms.
- The weights under A and B are my reading of what "counting" means.
- It shows the size of the mismatch clearly. It is not a derivation of ED's full gravity.

---

## G39: what now?

| | option | what it means | verdict |
|---|---|---|---|
| **(a)** | **The budget counts all commitment and its own use, feeding back on itself,** with the weights GR needs | "Used budget uses budget", so gravity gravitates | **Passes these tests.** But the weights are chosen to match GR. At this order ED's gravity then *is* general relativity, in budget language |
| **(b)** | **Keep the linear budget** | Simple counting | **Ruled out** by lunar laser ranging (by about 10⁴), the binary pulsar and the lunar materials test |
| **(c)** | **Look for an ED reason for GR's weights** | Derive the feedback from ED's own pieces (positive commitment, the Pythagorean split, the exponential rate) | Worth trying, but likely hard. It is the same kind of problem as G26 |

**Proposal: (a), stated plainly as "ED's gravity is GR in ED's words",** with (c) kept as open research.

**What this means for the whole programme.** Every gravity fix so far has matched a measurement rather than predicting one: light bending (RD35), Mercury (RD36), and now this. The pattern is clear. **ED's gravity side, done honestly, converges on general relativity.** That isn't a failure; GR is extremely well tested. But **it means gravity is unlikely to be where ED says something new.**

The places left where ED could differ are:
- **locus birth and dark energy** (a birth rate that changes over time);
- **exact draws** (a point of principle about horizons and entropy bounds);
- **the commitment rule's own structure,** if a version of it ever predicts something standard quantum physics doesn't.

## Questions for Allen

1. **G39:** adopt (a), "the budget feeds back on itself so that gravity matches GR", and say openly that ED's gravity is GR in ED language?
2. **Where next?** Given that gravity is converging on GR, should the effort move to locus birth and dark energy, which is the most promising place for ED to say something new?

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C206 | Will, "The confrontation between general relativity and experiment", *Living Rev. Relativ.* 17, 4 (2014), arXiv:1403.7377 | Paper text read: PPN metric terms; Nordtvedt formula (Eq. 66) and Earth–Moon wobble (Eq. 67); LLR bound; Table 4; Bartlett–van Buren (Eq. 72); Kreuzer |
| C206 | Williams, Turyshev, Boggs, *Phys. Rev. Lett.* 93, 261101 (2004), arXiv:gr-qc/0411113 | Via Will; not read directly |
| C206 | Bartlett and van Buren, *Phys. Rev. Lett.* 57, 21 (1986) | Via Will; not read directly |
