# The edge of the record, and the first rewiring test

*2026-09-13. G29b (open again) and G30 = (C) (RD32). Ledger: D12, C169–C178. Follows [Geometry_B_vs_C.md](Geometry_B_vs_C.md).*

## 1. What Allen meant by "the horizon"

**Allen (D12):**
- **"The horizon" means the current edge of what's committed,** not an observer's cosmic horizon.
- **Loci at that edge have a slightly different environment** from the rest.
- **Committed loci don't create other loci.** That is his issue with births spread evenly, "but maybe they are".
- **An object wouldn't get bigger anyway,** because it occupies the same number of loci.

### Two ways to read "the edge of what's committed" (C173)

| reading | picture | what observations say |
|---|---|---|
| **(a) An edge in space** | The record is a region with a border. New loci are born at the border, and the inside doesn't breed | **Heavily constrained.** It gives the universe a centre and an edge. Tests show we are not near any centre out to billions of light-years (C170), and expansion is the same in every direction (odds 121,000:1 against anything else, C171). The edge would have to lie far beyond what we can see. Expansion inside would have to be plain motion (C134), which leaves the observed acceleration with no local cause (C140) |
| **(b) An edge in time** | The edge of the record is **the present**. New loci are born next to the newest, not-yet-settled part of the record, never by old committed loci. Since "now" is everywhere, births happen everywhere in space | **Fits.** Space stays uniform. It is how causal set growth describes the passage of time: new spacetime atoms added at the growing edge (C69, C169), and like Ellis's growing block universe (C70) |

**My reading: (b) keeps your point and fits the data.** Old committed loci don't create loci; the frontier does. The frontier is the present, and the present is everywhere.

**"A slightly different environment" then has a natural meaning under (C):** the newest loci are the ones whose links haven't settled yet.

### Your object point (C174)
If an object's size in loci is set by its own pattern, a locus born inside it wouldn't make it bigger. The object would re-settle over the same number of loci and the extra locus would end up outside it. This is how bound systems keep their size in general relativity (C133). **It's a plausibility argument, not yet shown in ED's rule.** It does mean even births don't have to grow objects.

### G29b is open again (C175)

| option | what it says |
|---|---|
| **(ii)** Same chance everywhere (RD29, now under review) | Old and new loci breed alike |
| **(vi)** Births at the edge in time | New loci are born where links are still unsettled. This ties birth to option (C). The birth rate relative to how fast links settle is probably a number |
| **(a)** Births at an edge in space | Heavily constrained by the data above |

---

## 2. The first rewiring test (option C)

**Setup** (`checks/rewire_dimension.py`, predictions frozen before running):
- **Start:** 3,375 loci with 10,125 links placed at random, so 6 per locus on average. This is a "small world" with no geometry.
- **Each move:** a locus drops a link and grabs a locus two steps away, if that improves its local preference, or occasionally even if it doesn't.
- **Cooling:** the occasional "even if not" fades over 60 rounds, like cooling.
- **Comparison:** a plain 3D lattice of the same size.

**Two local preferences:**
- **R1 "favour squares":** about 6 links, and as many square loops as possible.
- **R2 "squares like a lattice":** about 6 links, and about 12 square loops through each locus. That is what a 3D grid locus has.

| | pieces | share in the biggest piece | how far apart loci are | how a random walk feels it (d_s) | squares per locus | perfect grid-like loci |
|---|---|---|---|---|---|---|
| **3D lattice** | 1 | 100% | 11.2 | 3.05 | 12 | 100% |
| **Random start** | 7 | 99.8% | 4.7 | 4.42 | 0.2 | 0% |
| **R1 favour squares** | **417** | **0.6%** | 2.2 | — | **78** | 0% |
| **R2 squares like a lattice** | 7 | 99.8% | **7.3** | **3.37** | **11.8** | **0.3%** |

### What it means

- **R1 shattered,** as predicted. Asking for "as many squares as possible" makes tiny, dense clumps stuffed with squares, 417 separate pieces (C176).
- **R2 came closest to 3D of any rule tried so far** (C177):
  - It stays connected.
  - Every locus ends up with about 6 links and 12 squares.
  - Almost no locus is a perfect grid locus: **glass, not crystal**, which is what we wanted.
  - **A random walker feels about 3.4 dimensions,** near the lattice's 3.05.
  - **But distances are still 35% too short** (7.3 against 11.2). Some long shortcuts from the random start survive, so it's still partly a small world.
- **My low-confidence prediction that R2 would come out 3D was wrong,** on distance only.

**One crash to record.** The first attempt stopped inside the measuring code before printing anything, because R1's biggest piece was smaller than the sample size. I fixed the code; the predictions weren't touched.

### Honest limits (C178)
- **One size, one seed, one cooling schedule.** Only about 5% of proposed moves were accepted, so R2 may simply be stuck.
- **R2's preference copies a 3D lattice's local counts** (6 links, 12 squares). That builds in a lot. It is a strong choice, not least structure.

### The lesson
- **The preference decides everything.** R1 and R2 differ by one term and end up as clumps versus near-3D glass.
- **Option (C) already does better than local splitting** (C147–C149).
- **Starting from a random tangle may be the real obstacle.** Long shortcuts are hard to undo.

That points somewhere interesting. **If space grows from a small seed, with births at the unsettled edge and local rewiring, long shortcuts never form in the first place.** That is your edge-of-the-record picture and your "first difference was the first locus" (D8), put together.

---

## Questions for Allen

1. **The edge:** is (b), the edge in time ("the frontier is now, and now is everywhere"), what you meant? Or did you mean an edge in space?
2. **The preference:** R2 works by copying a grid's local counts (6 links, 12 squares). Is that acceptable as a starting point, or should the preference mean something in ED terms?
3. **Next test:** grow from a small seed, with births where links are unsettled plus local rewiring, and see whether it comes out 3D and glass-like?

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C169 | Dowker, "The birth of spacetime atoms as the passage of time", *Ann. N. Y. Acad. Sci.* (2014), arXiv:1405.3492 | Abstract |
| C170 | Zhang and Stebbins, *PRL* 107, 041301 (2011), arXiv:1009.3967 | Abstract |
| C171 | Saadeh et al., "How isotropic is the Universe?", *PRL* 117, 131302 (2016), arXiv:1605.07178 | Abstract |
| C172 | Kardar, Parisi, Zhang, *PRL* 56, 889 (1986) | Search listing |
