# ED bootstrap, part 3: the draw and budget rules (on paper)

*ED_Attempt_03, note 4. 2026-09-15 (RD4). Ledger: C20–C25. Paper and literature only; no code was run for this note.*

## The question

Note 3 found that ED's coin rules are all equalities, so they have no corners. **ED's inequality-type rules live in the draw and budget sector.** If ED has its own "Ising kink", a special edge point that fixes a number, this is where it would be.

## ED's inequality-type rules, as they stand (C22)

| rule | the inequality | source | status now | an edge with a number? |
|---|---|---|---|---|
| **Budget cap** | Used budget can't exceed the locus budget: U ≤ B = 1 | A1 RD14 | **Active.** Reached only near black-hole conditions (A1 C104) | **Yes:** see below |
| **Rate never below zero** | Tick rate (B − U)/B ≥ 0 | A1 RD14, RD35 | **Removed.** Replaced by e^(−U), which never reaches zero: "a full budget becomes a limit rather than a wall" (A1 RD36) | Its wall is gone |
| **Too-thin draw** | Draw when a pattern's share drops below b_min | A1 RD19 | **Retired** (A1 RD26) | Gone |
| **Record threshold** | A draw once R\* = 3 near-perfect marks exist | A1 RD50 | **A stand-in.** Its meaning is "out of reach of every future path", a horizon whose size is an input (A3 C13) | Stand-in number |
| **Speed limit** | (ticking share)² + (speed/c)² = 1, so speed ≤ c | A1 RD17 | Chosen to match muon clocks | Light sits at the edge (speed c, no ticking). That's standard relativity |
| **Births never negative** | Dark energy = max(fluctuation, 0) | A1 RD20, RD38, C213, C219 | **Live,** awaiting a distance-data test (A1 G41) | **Yes:** see below |
| **Whole-unit outcomes** | Outcomes come in counts | A1 RD25 | Active | A count, not an edge |
| **Probabilities ≤ 1** | Draw probability Γ(1 + g) ≤ 1 | A2 C63 | Validity limit of the model | Modelling |

**How the list sorts:**
- **Removed or retired:** the rate wall and the too-thin draw.
- **Stand-ins or matched to measurement:** the record threshold and the speed limit.
- **Validity limits and counts:** probabilities ≤ 1 and whole-unit outcomes.
- **Two live edges that carry a number:** the budget cap and never-negative dark energy.

**None of these edges cross each other to make a corner** the way bootstrap boundaries do. They're separate one-dimensional limits.

## Edge 1: the budget cap (C23)

**What it does.** Near a very dense mass the used budget reaches the cap, U = 1. Under the rate law ED adopted (A1 RD36), clocks there slow by **e^(−1) ≈ 0.37** and motion between loci by **e^(−2)**. There's no horizon: nothing freezes completely.

**Why its number is physical now, not a convention.**
- **When the cap was set** (A1 RD14), "B = 1, only fractions matter", so the 1 was a unit choice.
- **Later, U was tied to gravity:** U ≈ GM/(rc²) in weak fields (A1 C104), with the rate law and weights chosen to match light bending, Mercury and more (A1 RD35–RD37).
- **Once U is measured in gravity's units, the cap's value means something.** Saturation happens where GM/(rc²) reaches 1, with a finite slowing there.

**So the cap is one of two things:**
- **(i) a hidden free number,** if ED's full budget B isn't really fixed at 1; or
- **(ii) a specific ED rule:** gravity saturates at a set point with a finite slowing and **no horizon.** That would be a strong-field departure from general relativity.

**What's known about rules like this (C20, C21):**
- **The rate law e^(−U) is the "exponential metric".** Written that way, it has no event horizons, and light aimed straight out can always escape (Yilmaz; Papapetrou's exponential spacetime is horizon-free).
- **Objects without horizons are what black-hole images and gravitational-wave "echoes" after mergers are used to test.**
- **This pass found no published constraint aimed specifically at the exponential metric.** Checking that properly would need its own literature step.

**Honest limits:**
- **Strong-field numbers are uncertain.** ED's gravity weights were matched only at the orders tested, so "U = 1 means GM/(rc²) = 1" is a weak-field reading pushed to strong fields.
- **Attempt 1 said gravity was unlikely to be where ED says something new** (A1 RD37).

## Edge 2: dark energy that's never negative (C24)

**What it does.** In ED, dark energy is new loci being born, and loci persist, so the birth-driven dark energy can't go below zero. The live form **clips** a fluctuating value at zero (A1 RD38, C219). That clip is an edge.

**Where its size comes from.** The fluctuation size, about 1 over the square root of spacetime volume, is **borrowed from causal set theory** (Sorkin's "everpresent Λ"; A1 C209, C210). That's a **counting** mechanism, and it gets Λ's order of magnitude from counting: Sorkin's estimate is 1.4 × 10⁻¹²² against the 2.9 × 10⁻¹²² needed (A1 C211).

**So it's a real specificity mechanism, but not ED's own.** ED adds only the one-sided clip. The clipped form still needs its data test (A1 G41), and in toy runs most today-like universes have dark energy changing more than current data probably allow (A1 C219).

## What the draw and budget bootstrap finds (C25)

- **ED's inequality sector has edges, but no corner that comes from ED's own principles with no inputs.** Each edge is:
  - **removed** (the rate wall, the too-thin draw);
  - **a stand-in** (three marks);
  - **matched to measurement** (the speed split, the rate law);
  - **borrowed** (everpresent Λ); or
  - **a units choice that became physical** (the budget cap).
- **The most ED-specific edge is the budget cap.** Its number is either a hidden free number, or a finite, horizon-free strong-field rule. That's a claim about black holes that ED's matching never tested.
- **A pattern across attempt 3 so far:**
  - **The specific numbers found inside ED** (1/3, 4/9, 120°) are known mathematics of its coin.
  - **The specific numbers in its draw and budget sector** come from inputs, stand-ins, matching or borrowing.
  - **ED's own principles haven't yet produced an edge that fixes a physics number.**

**Reading that honestly.** This doesn't show ED *can't* have a source of specificity. It shows that the places where one could sit are currently filled by choices. The one exception worth a real look is the budget cap, because it's both ED's own rule and quietly physical.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(h)** | **Decide what the budget cap means:** is "a locus can be full" part of ED's meaning (so B = 1 is a real rule), or a convenience (so B is a free number)? | Allen's call. If it's meaning, ED has one edge that fixes a strong-field number, and it's worth a proper literature check against black-hole images and merger signals |
| **(i)** | **The dark energy clip's data test** (A1 G41): today-like clipped runs against supernova and BAO distances | The live edge, but its size is borrowed |
| **(j)** | **Consolidate attempt 3:** a short write-up of the specificity search so far (map, coin shape, draw and budget edges) | A clean stopping point; the pattern is clear |

**Proposal: (h).** It's a quick meaning question, and it decides whether ED's one own edge is a free number or a real claim.

**Update:** Allen decided a full locus is part of ED's meaning (D2). What that means for black holes: [Full_Locus_Strong_Field.md](Full_Locus_Strong_Field.md) (note 5).

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C20 | Yilmaz exponential metric g = e^(−2u): no singularities and no event horizons, radially directed photons always escape, as described in arXiv:1606.01417 ("MECO in an exponential metric") and arXiv:2009.08655 ("Triple path to the exponential metric"); Papapetrou's (1954) exponential spacetime is horizon-free, as described in search listings on exponential wormhole spacetimes | Search listings; original papers not read |
| C21 | Horizonless compact objects and tests: Cardoso, Franzin, Pani, "Is the gravitational-wave ringdown a probe of the event horizon?", *Phys. Rev. Lett.* 116, 171101 (2016); echoes, arXiv:1709.01525; strong-field metric tests with the Event Horizon Telescope, arXiv:1908.11794 | Search listings |
| — | Attempt 1's own record: RD14, RD17, RD19, RD20, RD25, RD26, RD35–RD38, RD50; C104, C117, C209–C213, C219 | Read directly |
