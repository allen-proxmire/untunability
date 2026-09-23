# Locus birth: what makes a new locus, how often, and how it attaches

*2026-09-13. Gaps G29b and G30, and G36 revisited. Ledger: C131–C146. Follows [Space_As_Record.md](Space_As_Record.md) and [Commitment_Rule/Interaction.md](Commitment_Rule/Interaction.md).*

## Why it matters now

- **RD21:** Allen decided that loci are still being born today.
- **C91:** with q = 1, used budget piles up forever on a closed graph unless something balances it.
- **G36:** draws are exactly "can't be brought back" only if the region anyone can reach keeps growing.

---

## 1. What locus birth does for the budget

**New check** (`checks/budget_growth.py`, C131). The predictions were frozen before running, and all passed. The setup is a closed 3D space with one mass and q = 1, run for 600 steps.

| space | budget at the mass, every 100 steps | settles? |
|---|---|---|
| **Fixed size** (side 15) | 0.1452 → 0.1485 → 0.1515 → 0.1545 → 0.1574 → 0.1604 | **No.** It keeps rising by exactly the amount predicted |
| **Growing** (side 15 → 135, new loci born with budget 0) | 0.1450 → 0.1470 → 0.1478 → 0.1483 → 0.1487 → 0.1489 | **Yes.** It approaches the infinite-space value 0.1516 |

**In plain words:**
- **Birth never removes budget.** The total used is exactly (mass × steps), with or without births. Birth only *dilutes* it, by spreading the same total over more loci.
- **Growth outruns the pile-up if space grows faster than the budget spreads.** The budget near a mass then looks as if space were infinite, and it settles.

**Honest surprise: C91 isn't urgent for the real universe** (C136). The estimate below assumes steps near the Planck length, which RD15 leaves open. The observable universe then holds roughly 10¹⁸⁴ loci, and its age is about 10⁶¹ steps.
- **How far the budget has spread since the start:** about 10³⁰ steps. The universe is about 10⁶¹ steps across.
- **How much the budget has piled up everywhere:** about 10⁻¹²⁴ of a mass's own effect.

**A closed universe that stopped making loci would only notice the pile-up after about 10¹²³ steps.** So C91 is real in principle, locus birth solves it in principle, and nothing observable depends on it.

## 2. What observations say about space growing

| fact | what it means for ED | ledger |
|---|---|---|
| **Bound systems don't take part in cosmic expansion.** For planets, galaxies and clusters the effect is insignificant | Births must not make atoms, planets or galaxies grow. A birth chance as tiny as the cosmic expansion rate (about 10⁻⁶¹ per Planck step) is harmless, for the same reason it is in general relativity: binding acts far faster | C133 |
| **"Space is being created" is one reading of expansion, not a fact forced by data.** Redshift can equally be read as accumulated Doppler shifts | RD21 is a choice ED makes for its own reasons (C131, G36), not something observations demand | C134, C146 |
| **Expansion is accelerating.** Planck 2018 gives a matter fraction of 0.315, so dark energy is about 0.685 in a flat universe | Something drives acceleration. Loci born at a steady chance *per existing locus* would give exponential growth, which behaves like a cosmological constant | C140 |
| **A repulsive cosmological constant gives each observer an event horizon,** a finite region beyond which nothing can ever be seen, and that horizon has an entropy | This is the problem for exact draws, section 4 | C141 |
| **Newest data hint that dark energy changes over time.** DESI 2025 prefers it over a constant at 3.1σ, or 2.8–4.2σ with supernovae. That is a hint, not yet a discovery | A birth rate that isn't constant is not ruled out, and might even be favoured | C139 |
| **Everpresent Λ** (causal sets: the growing count of spacetime elements makes Λ fluctuate at about the size of the matter density) has been tested against supernova and CMB data. Some runs fit supernovae better than the standard model | The closest published relative of "births set Λ" | C71, C138 |
| **The budget is tiny almost everywhere** (C104) | A birth rate weighted by budget left would look exactly like a uniform rate, except near neutron stars and black holes | C144 |

## 3. The hard part: attaching a new locus without ruining space

- **Most random ways of building a discrete space don't look like space at all.** Among orderings of N elements, the overwhelming majority are flat three-layer structures (Kleitman–Rothschild orders), numbering about 2^(N²/4). Causal set theory has to suppress them. Recent work shows most are strongly suppressed by the gravitational action, but the continuum is not yet shown to emerge (C135).
- **Growing networks can end up as smooth manifolds or as tangled "small-world" webs,** depending on the attachment rule (Bianconi and Rahmede, C137).

**So the attachment rule (G30) decides whether ED's space stays 3D and smooth** (C145). ED has no attachment rule yet. Whatever is chosen must pass a dimension check before anything is built on it.

## 4. The horizon problem for exact draws (G36 revisited)

The chain of reasoning (C143):
1. The observed universe has a repulsive dark energy (C140), which gives a finite event horizon (C141).
2. **If** the number of distinguishable states within reach obeys the covariant entropy bound, S ≤ A/4 (C142),
3. **then** the reachable region is effectively finite,
4. **and** Bousso and Susskind's result (C120) says outcomes are then never *exactly* definite.

**So "can't be brought back" would hold in practice, but not exactly.**

**ED keeps exact draws only if one of these holds:**
- the entropy bound doesn't apply to ED's loci, **or**
- dark energy evolves in a way that avoids a permanent horizon. DESI hints at evolution (C139), but that isn't established, and evolution alone doesn't guarantee no horizon.

This is Claude's argument, built from the cited pieces. It is not a published result about ED.

---

## Options

### G29b: what makes a new locus?

| | option | verdict |
|---|---|---|
| **(i)** | **Commitments make loci.** Every draw leaves a new locus behind (closest to "space is the record of events", D8) | **Open.** No new number, because the rate comes from draws. But births would concentrate where matter commits, and expansion would follow the history of commitment activity. That is testable in principle, and must not make bound systems grow (C133). Needs units to check |
| **(ii)** | **A locus birth is itself the most basic event:** at every locus, the same tiny chance per step, independent of matter | **Least structure.** Same rule everywhere, gives exponential growth like a cosmological constant, and no preferred place. **Cost:** one free number, the birth chance, which plays the role of the cosmological constant. The rule's free-number count goes from 0 to 1 (C102), and ED inherits the "why is it so small?" question |
| **(iii)** | **Birth weighted by budget left** | Looks the same as (ii) everywhere except near neutron stars and black holes (C144). Nothing gained for cosmology |
| **(iv)** | **No births after the early universe** (would reverse RD21) | C91 would be harmless in practice (C136), and expansion can be read as motion (C134). **But** the graph would be finite, so exact draws (G36) fail in principle |

**Proposal: (ii), with (i) as the serious alternative.** (ii) is the least structure and fits the data qualitatively. (i) is closer to your founding picture and adds no number, but it needs units before it can be checked.

### G30: how does a new locus attach?

| | option | verdict |
|---|---|---|
| **(A)** | **Local splitting:** a random locus splits in two, and the pair shares its old connections | **Proposal.** It keeps things local, and births at random places in random order avoid a preferred frame (C76). **Must pass a frozen dimension check:** does random local splitting keep a 3D graph 3D and smooth? |
| **(B)** | **Attach anywhere at random** | **Ruled out.** It connects distant places, so space stops being local (the small-world webs in C137) |
| **(C)** | **Causal-set growth:** a new element is placed "after" a random set of earlier ones | **Known program** (C69, C132). Whether it gives smooth space is unsettled (C135), and it describes spacetime order rather than a spatial graph |

### G36 revisited: exact or practical?

| | option | cost |
|---|---|---|
| **(a)** | **Draws are "can't be brought back" in practice,** as in standard physics | D1's "can't be taken back" becomes a statement about practice, not principle |
| **(b)** | **Keep draws exact** | ED must say the entropy bound doesn't apply to loci, or rely on dark energy avoiding a horizon |

**Proposal: keep (b) as the aim for now, since D1 is a core commitment, and log the tension (C143) as a known risk.** Revisit if dark energy turns out constant *and* ED's loci turn out to obey an entropy bound.

---

## Questions for Allen

1. **G29b:** (ii) same small birth chance everywhere, with one new number? Or (i) commitments make loci?
2. **G30:** local splitting (A), checked first by a frozen dimension test?
3. **G36:** keep exact draws as the aim, with the horizon tension logged? Or accept "in practice"?

## Sources checked

| ledger | source | how it was checked |
|---|---|---|
| C132 | Martin, O'Connor, Rideout, Sorkin, *Phys. Rev. D* 63, 084026 (2001), arXiv:gr-qc/0009063 | Abstract |
| C133 | Cooperstock, Faraoni, Vollick, *ApJ* 503, 61 (1998), arXiv:astro-ph/9803097 | Abstract |
| C134 | Bunn and Hogg, *Am. J. Phys.* 77, 688 (2009), arXiv:0808.1081 | Abstract |
| C135 | Kleitman and Rothschild, *Trans. AMS* 205, 205 (1975) | Bibliographic details only |
| C135 | KR-order facts | Search listings of the causal set literature |
| C135 | Loomis and Carlip, *Class. Quantum Grav.* 35, 024002 (2018), arXiv:1709.00064 | Abstract |
| C135 | Carlip, "Causal sets and an emerging continuum" (2024), arXiv:2405.14059 | Abstract |
| C137 | Bianconi and Rahmede, *Phys. Rev. E* 93, 032315 (2016), arXiv:1511.04539 | Abstract |
| C138 | Das, Nasiri, Yazdi, *JCAP* 10 (2024) 076, arXiv:2307.13743 | Search listing only |
| C139 | DESI Collaboration, DR2 Results II, *Phys. Rev. D* 112, 083515 (2025), arXiv:2503.14738 | Abstract |
| C140 | Planck Collaboration, 2018 results VI, *A&A* 641, A6 (2020), arXiv:1807.06209 | Abstract; the dark energy fraction is inferred |
| C141 | Gibbons and Hawking, *Phys. Rev. D* 15, 2738 (1977) | Abstract from a search listing |
| C142 | Bousso, *JHEP* 9907:004 (1999), arXiv:hep-th/9905177 | Abstract |

---

## Decided (2026-09-13)

- **G29b = (ii) (RD29).** At every locus there is the same tiny chance per step of a birth, independent of matter. A birth is itself the most basic event. **The rule now has one free number:** the birth chance, which plays the role of the cosmological constant (C155).
- **G36 = keep exact draws as the aim (RD31).** The horizon and entropy-bound tension (C143) is logged as a known risk.
- **G30 = local splitting, provisionally (RD30).** Allen wasn't sure. The check below supports his doubt, so G30 is reopened.

## Local splitting, checked (C147–C149, C154)

**The check** (`checks/split_dimension.py`, predictions frozen before running):
- Start from a 3D lattice of 4,096 loci.
- Grow it to 32,768 by random local splits.
- Compare with a plain 3D lattice of the same size.

"The pair shares its old connections" can be read three ways, so all three were tried.

| rule | links per locus | how far apart loci are | how a random walker experiences it (d_s) | how count grows with size (D_g) | what space became |
|---|---|---|---|---|---|
| **Plain 3D lattice** (control) | 6 | 24.0 | 3.05 | 3.00 | 3D |
| **S1: new locus takes half the links** | 2.5, heading to 2 | 23.0 | **1.98** | 3.21 | **Stringy.** Big like 3D, but a walker feels about 2D, and it thins toward chains as births continue |
| **S2: as S1, plus two extra links** | 6 | **13.6** | 2.88 | **16.6** | **Crumpled.** New loci crowd in instead of making space bigger |
| **S3: new locus copies all links** | **62** | **12.0** | 2.51 | no growth | **A clump.** Space doesn't get bigger at all |

**Four of my frozen predictions were wrong.**
- **One was my arithmetic:** the exact control distance is 24.0007, not 24.
- **Three were real misjudgements:**
  - I expected S1 to stretch distances; it didn't.
  - I expected S2 to stay close to 3D; it crumpled.
  - I expected S3 to form hubs; it didn't, at this size.

**In plain words:** none of the three ways of splitting keeps space 3D. They make space stringy, crumpled, or a clump.

**This matches the literature.**
- **Growing simplicial spaces** in more than 2 dimensions become scale-free webs with hubs (C150).
- **Random triangle-splitting** gives small-world webs (C151).
- **Copy-the-links growth** is the classic way biology models protein networks, which are far from geometric (C152).
- **Where 3D (or 4D) is recovered,** it takes a global ingredient:
  - **Causal dynamical triangulations** get four dimensions at large scales from a built-in time layering plus the gravitational action (C153).
  - **Causal sets** need the action to suppress non-geometric structures (C135).

**Limits of this check:**
- only three rules;
- one growth factor (×8);
- one size;
- one random seed.

It shows these rules fail. It doesn't show every local rule fails.

## G30 reopened: options

| | option | what it costs |
|---|---|---|
| **(A′) Keep looking for a purely local birth rule** that keeps 3D, testing each candidate with this same check | Might not exist; nothing in the literature so far suggests an easy one |
| **(B) Births guided by a global preference for 3D,** in the style of an action, as in causal dynamical triangulations and causal sets | Adds real structure, probably with a coupling number. ED moves closer to those programs |
| **(C) Let connections move:** births are local, but links can rewire over time and settle into 3D, as in quantum graphity's low-energy phase (C74) | Adds a rewiring rule. Geometry then comes from dynamics, not from the birth rule |
| **(D) Loci are born, but geometry isn't a graph of neighbours at all.** "Near" comes from the order of events, as in causal sets | Moves ED onto causal set theory's ground, including its entropy problem |

**No option here is least structure in the usual sense.** This is the open problem every discrete-spacetime program faces: getting smooth 3D space out of discrete growth. It is a real frontier, not a gap only ED has.

*Continued in [Geometry_B_vs_C.md](Geometry_B_vs_C.md): horizon births, Allen's 3D ideas, and (B) and (C) in plain words.*
