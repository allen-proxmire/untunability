# E1: resolution — what a bigger model could settle, on paper

*ED_Attempt_08, note 2. 2026-09-19 (RD2). Ledger: C2–C6. **Reasoning, literature and arithmetic only: no code, nothing run.** Questions E-Q1–E-Q6 and the expected results are for Allen to confirm; building the port is a separate yes, and running it is another.*

## Where road E starts

**Road C ended on one question it could not answer** (A7 C103): ED's growth runs from crumpled to branched, and at the sizes reachable there was no flat three-dimensional middle between them. Every slice was at most 24 events across, and most slice readings came back "too small to measure."

**Road E asks whether size is the reason.**

## 1. What the literature says about size (C2)

**Two findings, both bearing directly on this.**

**Finite-size effects in three-dimensional dynamical triangulations are large, and they run the wrong way for us.** The crumpled phase is dominated by triangulations with singular vertices — vertices whose local volume grows in proportion to the whole manifold — and **that singular structure only takes over above a certain volume.** Degenerate triangulations were introduced precisely because they cut these effects by about two orders of magnitude. The crumpled-to-branched transition itself is **strongly first order**.

**Dimension readings are resolution-hungry and biased low.** Hausdorff dimension is extracted from how volume grows with geodesic distance, and the radius grows so slowly with volume that much larger volumes are needed for a reliable value; measurements tend to **underestimate**. Even at 32,000 simplices in two dimensions the fits are difficult.

**What this means for ED, stated plainly:**
- **The prior is against finding a flat middle.** In the nearest studied system, going bigger **sharpens** the crumpled/branched split rather than opening something between. Road E should not be sold as a search for a flat middle.
- **ED's slices are not small in simplex count.** At 13,824 events a slice carries about **79,000 tetrahedra** — the upper end of the sizes at which 3D dynamical triangulations were studied. **What is small is the linear extent**, and that is exactly what dimension readings need.

**So the resolution problem is real but specific:** not too few simplices for the physics, too few **hops** for the readings.

## 2. What ten times larger actually buys (C3, arithmetic)

**The flat cube-grid slice** at side n has V = n³ events, about 6V tetrahedra, and a diameter of about 0.75n hops.

| side n | events | tetrahedra | flat diameter | vs attempt 7's largest |
|---|---|---|---|---|
| 20 | 8,000 | 48,000 | 15 | 0.58× |
| **24** | **13,824** | **83,000** | **18** | **attempt 7's largest** |
| 32 | 32,768 | 197,000 | 24 | 2.4× volume |
| 40 | 64,000 | 384,000 | 30 | 4.6× |
| **52** | **140,608** | **844,000** | **39** | **10.2× volume** |

**Ten times the volume buys 2.2 times the hops.** That is the whole gain, and it is worth being blunt about it: radius goes as volume^(1/3), so the readings improve slowly. Going from 18 hops to 39 turns a fit with two or three usable radii into one with perhaps six to nine — the difference between "undefined" and "a number with an error bar," and no more than that.

**A hundred times the volume would buy 4.6 times the hops.** That is what would settle a dimension properly, and it is out of reach.

## 3. So the question has to change (C4)

**"Is there a flat middle?" is the wrong question to spend a port on.** The literature's answer is probably no, and ten times the size cannot answer it decisively either way.

**The question worth the compute is the character of ED's crossing:**

> **As slices grow, does ED's crumpled-to-branched crossing sharpen (first order, as in dynamical triangulations) or broaden (continuous)?**

**Why this one is worth asking:**
- **It is answerable at reachable sizes.** Finite-size scaling needs several sizes and a sharp order parameter, not a resolved dimension. Mean links per event, the branched flag (spectral dimension below 2) and diameter over volume^(1/3) are all measurable at 13,824 events today — the threshold scan already produced them.
- **It is the one place ED's structural difference could show.** Dynamical triangulations reach the crossing by **tuning** a coupling. ED reaches it by **conserving** a budget, and the knob being turned is sync's threshold, which ED argued for on its own grounds. If a conserved system has a continuous transition where a tuned one has a first-order jump, **that is a real difference**, and a continuous transition is what a continuum limit needs.
- **"Is there a flat middle?" is a special case of it** — a flat middle is what a continuous transition could open up — so nothing is given away.

**Census note, before anything is built:** **road E cannot reduce ED's input count.** It settles whether wall 3 stands, and it can produce one genuinely new statement about ED's balance. **Inputs supplied stay at 3 either way.**

## 4. A correction to the carry-forward: "reproduce exactly" is not available (C5)

**Note 1 said the port should reproduce attempt 7's runs "on identical seeds." That cannot be done, and the reason matters.**

The model chooses moves by drawing from Python sets whose **iteration order depends on insertion and deletion history**, not on the seed. This is the same fact I got wrong once already in attempt 7, when I claimed a resumed run follows an identical random path and had to correct it. **A rewrite onto arrays changes that order, so the random path diverges from the first differing draw — by construction, not by error.**

**What can be demanded instead, a ladder of three:**

| tier | what is compared | standard |
|---|---|---|
| **1. Predicates and costs** | For the same state and the same proposed move: the link condition, the budget gate, the ceiling gate, the sync gate, `n3_after_exact`, and the cost change ΔS | **Exact.** Integers bitwise; floats to 1×10⁻¹² |
| **2. Scripted move sequences** | A fixed list of moves applied to the same starting complex, in both codes | **Exact.** Identical V, E, T, sorted degree sequence, and `check()` passing in both |
| **3. Whole runs** | The port at n = 24, **eight seeds**, against attempt 7's two seeds per setting | **Statistical.** Attempt 7's values fall inside the port's seed-to-seed spread, for links per event, diameter, spacetime d_H and the refusal counts |

**Tier 3 needs more seeds than attempt 7 had** — two values cannot define a spread — so the port's first job is to supply them. That is a cost, and it is counted below.

## 5. Expected results, written down before any code

**For E2, the port:** tiers 1, 2 and 3 above, all three. **Any tier-1 or tier-2 disagreement is a port bug, full stop** — no run is planned until they pass.

**For E3, the runs**, at four sizes (n = 24, 32, 40, 52), setting B, with sync's threshold scanned:

| | expected | why |
|---|---|---|
| **E3-0** | The calibration gate passes at every size: flat reads flat, randomized doesn't | It passed at both sizes in attempt 7 |
| **E3-1** | Structure, budgets, ceiling and flip neutrality exact at every size; event counts within ±10% of the start except at the tightest threshold | Held in C3f and C3g |
| **E3-2** | **At n = 52 the slice readings are defined** for every threshold that isn't strangling growth: a mass dimension with **at least six usable radii**, and a diameter of at least 20 | 39 hops against 18 |
| **E3-3** | **The crossing sharpens.** The range of threshold over which links per event moves from crumpled to branched **shrinks** as volume grows, roughly as a power of volume | The first-order prior, from the literature |
| **E3-4** | **No threshold gives a flat middle:** no setting reads slice d_H in [2.6, 3.4] with d_s in [2.4, 3.6] at the two largest sizes | The same prior; this is the statement road C could not make |
| **E3-5** | Spacetime d_H stays above 4.7 at every threshold | Attempt 7 read 5.4–6.4 |

**The numbers a flat slice must hit, fixed now:** mass dimension **3.0**, spectral dimension **3.0**, links per event **6.70**, mean degree **13.4**, diameter **0.75n**, and for the grown spacetime **4.0**. **Branched** is spectral dimension at or below 2 (attempt 7 measured 1.35 and 1.59). **Crumpled** is links per event at or above 13.4, or a diameter that stops growing with size.

## 6. The exit rule

**Fixed before anything is built.**

| outcome | record |
|---|---|
| **Tier 1 or 2 fails** | A port bug. Fix and re-verify; no run |
| **Tier 3 fails** | The port is a different model. **Say so plainly**, name the difference, and do not use it to reinterpret attempt 7 |
| **E3-3 holds and E3-4 holds** | **"ED's growth has a first-order-like crumpled-to-branched crossing with no smooth middle, up to slices of 140,608 events."** Wall 3 stands, ten times more firmly than road C left it. Road E closes; ED's growth rule is then a known dead end and the meanings, not the model, are what need revisiting |
| **E3-3 fails — the crossing broadens** | **"ED's conserved balance gives a continuous crumpled-to-branched crossing where the tuned version gives a first-order one."** That is a difference from dynamical triangulations, a continuum limit becomes a live question, and road E continues into measuring the exponents |
| **E3-4 fails — a flat middle appears** | **"At slices of N events, ED's growth with sync's threshold at s reads three-dimensional: consistent, not derived; the density, the ceiling, the threshold and the strengths are knobs."** Then the same setting at the next size up, before anything else is said |
| **E3-2 fails — still unmeasurable at n = 52** | **"Too small to measure, again."** Road E closes as a failed instrument, and the record says the readings, not the sizes, are what need replacing |

**The last row matters.** Attempt 7 spent two of three runs on bookkeeping. **If the port cannot measure at ten times the size, the answer is not twenty times the size.**

## 7. What the port is, and what it costs (C6)

**The port:** `c3c`–`c3f` rewritten onto flat integer arrays — tetrahedra as 4 vertices plus 4 face-neighbours, edges and degrees as arrays, the random-choice sets as index-swap pools — with the inner loop compiled by **Numba**. About **1,500 lines** of attempt 7 model code, of which `c3c.py` (471 lines, the rotation system and the topology-safe moves) is the hard part.

**Memory stops being the constraint:** at n = 52 the tetrahedron table is 844,000 × 8 four-byte integers, about **27 MB**. Attempt 7's Python objects were what exhausted 15 GB.

**Time, as things stand today** (28.6 s per tick at n = 24, measured):

| side n | seconds per tick, Python | one 150-tick run |
|---|---|---|
| 24 | 28.6 | 1.2 h |
| 32 | 68 | 2.8 h |
| 40 | 132 | 5.5 h |
| **52** | **291** | **12.1 h** |

**A campaign of roughly 56 runs is about 190 hours of Python — 65 hours on three workers. That is why the port exists.** At a 30× speedup the same campaign is about **6 hours single process**, and the n = 52 runs go from 12 hours to 24 minutes each.

**The 30× is an assumption, not a measurement.** Following attempt 7's own lesson — time every reading before planning a run — **E2 ends with a measured per-tick time at n = 52, and E3 is only planned after that number exists.** If the speedup comes in under about 8×, the campaign is cut to three sizes and that is recorded before any run.

## 8. Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **E-Q1** | **Reframe road E around the crossing's character** — does it sharpen or broaden with size — with "is there a flat middle" kept as a special case? | **Yes** | It is answerable at reachable sizes, and it is where ED's conserve-don't-tune difference could actually show |
| **E-Q2** | **Accept the three-tier validation ladder,** given that bit-for-bit reproduction is impossible by construction? | **Yes** | Tiers 1 and 2 are exact where exactness is available; tier 3 is honest about the rest |
| **E-Q3** | **Four sizes, n = 24, 32, 40, 52,** with sync's threshold as the scanned knob and setting B as the line? | **Yes** | Four points is the fewest that can show a width shrinking as a power of volume |
| **E-Q4** | **Keep T = 150 ticks at every size,** with one check at T = 300 at n = 24 to see whether the outcome is tick-limited? | **Yes, and record T as a knob** | A bigger slice may need longer to settle; the check costs about an hour and would otherwise be a hole in the result |
| **E-Q5** | **Numba on arrays**, rather than C or C++? | **Yes** | It stays in one language, the readings and runner carry over unchanged, and it is the fastest route to a measured per-tick time |
| **E-Q6** | **The ceiling (60), the conserved density (6.699) and the other knobs unchanged from C3f/C3g?** | **Yes** | The port must be the same model; changing a knob and the implementation at once would confound the comparison |

## Questions this note does not settle

- **Whether a continuous crossing, if found, means a continuum limit exists.** That needs exponents and a scaling function, which is road E's second half at best.
- **What replaces the growth rule if wall 3 stands.** That is a meanings question, not a model question, and it belongs on paper with Allen.

## Next step

**If the defaults hold:** the port (E2), tier 1 and tier 2 verification, then the measured per-tick time at n = 52. **The runs need a separate yes.**

## Sources

- [Phase Structure of Dynamical Triangulation Models in Three Dimensions](https://arxiv.org/pdf/hep-lat/9712011)
- [Three-Dimensional Simplicial Gravity and Degenerate Triangulations](https://arxiv.org/pdf/hep-lat/9807026)
- [Simulating Four-Dimensional Simplicial Gravity using Degenerate Triangulations](https://arxiv.org/pdf/hep-lat/9810049)
- [Recent results in Euclidean dynamical triangulations](https://arxiv.org/pdf/1701.06829)
- [On the Nature of Spatial Universes in 3D Lorentzian Quantum Gravity](https://arxiv.org/pdf/2208.12718)
- [Zooming in on the Universe: In Search of Quantum Spacetime](https://arxiv.org/pdf/2311.06910)
