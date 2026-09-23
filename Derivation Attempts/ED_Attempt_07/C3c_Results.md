# C3c results: growing a 3D slice

*ED_Attempt_07, note 19. 2026-09-17 (RD35). Ledger: C70, C71. Run `model/c3c_run.py` with the D29 guards; 28 jobs, 8.1 h in the last session after two restarts (3 workers). Expected results, shape rules and exit rule fixed in note 18 and its D29 revision, before any results.*

## Run 1, as pre-registered (C70)

**Calibrations:**

| | flat start (FC) | randomized (RC) |
|---|---|---|
| **4,096 events** | **flagged hyperbolic** ✗ (d_H 2.50, largest degree 14, growth flag set) | crumpled + hyperbolic |
| **13,824 events** | **flat 3D** ✓ (d_H 2.66, largest degree 14, no flag) | crumpled + hyperbolic (d_H undefined, largest degree 60) |

**The flat slice at 4,096 was mis-flagged,** because its balls hit the reading's limit before three radii fit. That's what fails E0.

**Growth settings** (both sizes, 2 seeds each):

| setting | outcome | how it got there |
|---|---|---|
| **S0** no pressure | **densified** at both sizes | Guard hit at ticks 137–144; 20 tetrahedra per event (flat 5.7); mean degree 42–43 |
| **S1** commitment only | ran all 500 ticks; read **crumpled + hyperbolic** | Mean degree 13.8 (4,096) and 16.0 (13,824), close to flat's 13.4, but largest degree 224 and 406; d_H undefined |
| **S2** curvature only | ran all 500 ticks; read **crumpled + hyperbolic** | Mean degree 11.0; valence spread 1.06, the tightest of any setting; largest degree 94 and 154; d_H undefined |
| **S3** sync only | **densified** at both sizes | Guard hit after **5 ticks**: sync alone adds links fastest |
| **S4** all three | **densified** at both sizes | Guard hit at ticks 128–200; at 13,824, 32–34 tetrahedra per event, mean degree 65–69 |
| **S5** stronger sync | **densified** at both sizes | Guard hit at ticks 60–150; at 13,824, 37 tetrahedra per event, mean degree 77 |

| | result | |
|---|---|---|
| **E0** calibrations | Flat reads flat at 13,824, but is flagged hyperbolic at 4,096 | **Not as expected** |
| **E1** structure, budget, guards | Every structure check exact in every tick of every run; budget conserved; every stop is a recorded guard | **As expected** |
| **E2** S0 not flat at the larger size | Densified | **As expected** |
| **E3** S1 branched at the larger size | Read crumpled, not branched | **Not as expected** |
| **E4** S3 not flat at the larger size | Densified | **As expected** |
| **E5** S4 flat at both sizes | Densified at both | **Not as expected** |

**Exit, by the rule as written: "E0 failed: readings revision (recorded)."**

**No setting produced a flat 3D slice,** and none of the runs that finished could even be measured for dimension: their slices became too small across for the ball reading.

## What went wrong, and it isn't the code (C71)

**The code is sound as far as it can be checked:**
- every structure check exact, every tick, in every run;
- budget conserved to 10⁻⁹;
- the incremental cost matches a full recomputation to 5 × 10⁻¹³;
- the guards did their job, turning runaways into recorded outcomes.

**Two real problems, both about the model, not the machinery:**

**1. Nothing controls the number of tetrahedra.**
- **The budget balances events** (C2a), and it did: every run held its event count within about 1–19% of the start.
- **But links and tetrahedra have no balance.** Tetrahedra per event went from 5.7 at the start to 20 or more, even with **no pressure at all** (S0).
- **That's the known behaviour of random 3D triangulations:** with nothing weighting the tetrahedron count, the count runs away, because there are far more dense triangulations than sparse ones. In CDT and dynamical triangulations this is exactly what the cosmological-constant coupling per building block controls.
- **Commitment is ED's version of that weight,** and at strength 1 it holds the *mean* (S1's mean degree 13.8 against flat's 13.4) but not the extremes (largest degree 224).
- **Sync alone is the worst,** as the counting on paper said it would be (C66): it rewards links, and it hit the limit in 5 ticks.

**2. The readings can't measure these slices.**
- **Dense slices are small across.** A few hops reach everything, so fewer than three ball radii fit under the reading's limit, and the mass dimension comes out undefined.
- **It also mis-flagged the flat calibration** at 4,096 events, which is what fails E0.
- **So "crumpled + hyperbolic" for S1 and S2 is partly the reading's limits,** not a clean measurement.

**What this says about road C3:** the piece ED is missing in 3D isn't only smoothness. **It's a second balance.** C2a balanced how many events there are; nothing yet balances how many links and tetrahedra hold them together. Commitment is the natural candidate from ED's meanings, but at unit strength it isn't enough, and its strength is a knob.

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **On paper first: the link balance.** What ED's meanings say about what fixes the number of links per event, the way the budget fixes the number of events. Then spec C3d with that balance and repaired readings | Cheap, and it's the piece the run identified |
| **(b)** | **Repair the readings and rerun as is** (larger slices, or a reading that doesn't need wide balls) | Fixes E0, but the densification would still be there |
| **(c)** | **Take stock of road C3 and attempt 7** | 2D not reached, 3D static check passed, 3D growth blocked on a missing balance |

**Proposal: (a), then (c) if the paper work doesn't open a way.**
