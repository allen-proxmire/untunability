# PF-d on paper: what a causal-set-like ED keeps and loses

*Fork of ED_Attempt_04 (A4-ledger D31, RD21). 2026-09-15. Fork ledger: FC1–FC5. Literature, reasoning, and one arithmetic check (`checks/causal_diamond_check.py`, expected results written first). **Nothing here is decided for attempt 4's main line.***

## What PF-d is

- **Keep:** discrete, and no rest frame.
- **Give up:** finite neighbours.

**The known example is a causal set:**
- events scattered at random, with a fixed density;
- **the only structure is order:** which event can influence which;
- every event is related to everything in its past and future;
- every event has **infinitely many nearest relations** ("links").

## What's known (FC1)

| fact | source |
|---|---|
| **Order plus number gives geometry.** The number of events in a region is its spacetime volume | Bombelli, Lee, Meyer, Sorkin (1987); Surya's review (2019) (A4 C26) |
| **The longest chain between two related events is proportional to the proper time between them,** at high density | Brightwell and Gregory (1991); Surya §4.3 |
| **Dimension can be read from order:** the fraction of related pairs depends only on the dimension (Myrheim–Meyer) | Surya §4.1 (A4 C58) |
| **Random scattering picks out no rest frame.** Every event has infinitely many links, a "characteristic non-locality" | Bombelli, Henson, Sorkin (2009); Surya §3.2 (A4 C84) |
| **Spatial shape can be recovered** from "thickened" slices of events that aren't related to each other | Major, Rideout, Surya (2007) |
| **Particles can move on it.** Summing over hop paths through a causal set gives the right propagator in 1+1 and 3+1 dimensions, a cousin of Feynman's checkerboard | Johnston (2008) |
| **Field equations become non-local,** with a non-locality scale | Benincasa and Dowker; Sorkin (2007) |
| **Randomness makes particles "swerve":** a slow drift in momentum. Relic neutrinos bound it very tightly | Kaloper and Mattingly (2006) |
| **Which growth rule gives space-like results is still open** | Surya §5; A4 C58 |
| **In 1+1 dimensions the longest chain among N random events grows like 2√N** (the longest increasing subsequence of a random permutation) | Logan and Shepp; Vershik and Kerov (1977); Baik, Deift, Johansson (1999) |

## What PF-d fits (FC2)

| attempt 4's meaning | in a causal-set-like ED | fit |
|---|---|---|
| **Time is the order of relations; space is their pattern** (D11) | Order is everything; space comes from slices of the order | **Exact** |
| **Draws, growth, commitments never stop** (A1; E-Q3) | Growth adds one event at a time, never removed | **Fits** |
| **A body commits as much as it can along its path** (R4-Q1) | **The longest chain between two events *is* the proper time.** Free fall is the longest chain of events | **Striking:** maximal aging becomes "the longest chain of commitments" |
| **Pairings as a body's ticks** (D29) | In 1+1, (pairing count)² = 4·n_R·n_L = **2 × the number of events between the two moments,** at unit density (check P1) | **Fits,** and gives pairings a meaning: **your own time squared counts what lies between.** It's frame-free because order is (P2) |
| **Light is uncommitted** (R4-Q2) | Light has no chain of events of its own between emission and absorption, so no ticks of its own | **Fits, loosely** |
| **No rest frame** (the hole) | Random scattering picks none | **Fits** (that's the point) |

## What PF-d costs (FC3)

| attempt 4's meaning | in a causal-set-like ED | cost |
|---|---|---|
| **Dimension by counting outward** (E-Q2) | Every event has infinitely many links, so counting outward fails | **E-Q2 would have to change** to dimension read from order |
| **E-C's bridge** (a pattern behaves like d-dimensional space for loops) | Knots need spatial slices, which thickened slices recover only approximately, at high density | **E-C's argument would need rewriting** on slices; hole H1 changes form |
| **A particle is a knot of commitments** (D14) | A particle's history is a chain in time. A knot would be a knotted bundle of chains across a slice | **"Knot of commitments" would need restating** |
| **Loci are born and persist** (A1) | Events don't persist; something persisting is a chain of events | **"Locus" would change meaning:** a locus becomes a chain |
| **The on/off picture:** presence, influence, blocked clocks (D1, D2; A3 C38) | No ready version. The height part of the motion rule would have to be rebuilt | **Substantial rework** |
| **Locality** | Non-local field equations and swerves, each with tight bounds | **New constraints** |
| **How space-like results grow** | Still open in causal set theory | **The same wall** as E-B (A4 C58) |

## What it means (FC5)

- **PF-d fits the motion and time side of ED remarkably well:**
  - time as order;
  - growth by draws;
  - the one rule as the longest chain;
  - pairings as counting the events in between;
  - no rest frame.
- **It costs the space side:**
  - counting outward;
  - E-C's knot bridge;
  - loci as persisting places;
  - the on/off picture.
- **Honest:** almost every fit is causal set theory's own result, said in ED words. R4's choices were already "consistent, not derived". **PF-d gives them a natural home, not a derivation.**
- **For the preferred-frame hole:** PF-d removes the rest frame, but trades it for non-locality, which has its own bounds and an unsolved growth problem.
- **Fork verdict: a comparison, no decision.** Six fits, seven costs. PF-Q1 stays with Allen.

## If PF-d were pursued (not asked now)

It would become a road, with meaning questions fixed first:
- **F-Q1:** is a locus a chain of events?
- **F-Q2:** is dimension read from order?
- **F-Q3:** is a knot of commitments a knotted bundle of chains?

It would also need an exit rule set with Allen before any model.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| FC1 | Surya, "The causal set approach to quantum gravity", *Living Rev. Relativ.* 22, 5 (2019), arXiv:1903.11544 (ar5iv: §3.2 links and non-locality, §4.1 Myrheim–Meyer, §4.3 longest chain, dynamics open); Wikipedia "Causal sets" (geodesic length proportional to proper time; volume by counting; dynamics open); Brightwell and Gregory, *Phys. Rev. Lett.* 66, 260 (1991) (listing); Major, Rideout, Surya, *J. Math. Phys.* 48, 032501 (2007) (listing); Johnston, "Particle propagators on discrete spacetime", *Class. Quantum Grav.* 25, 202001 (2008), arXiv:0806.3083 (listing); Benincasa–Dowker operators (CausalSets.jl documentation; Dowker and Glaser arXiv:1305.2588, listings); Kaloper and Mattingly, *Phys. Rev. D* 74, 106001 (2006), arXiv:astro-ph/0607485 (listing); Sorkin, "Light, links and causal sets", arXiv:0910.0673 (abstract); longest increasing subsequence results (listings) | Review via ar5iv; others via listings or abstracts |
| FC4 | `checks/causal_diamond_check.py`, run 1 | Computed |
| — | A4-ledger C26, C58, C84, C85, D11, D14, D24, D27, D29 | Attempt 4's ledger |
