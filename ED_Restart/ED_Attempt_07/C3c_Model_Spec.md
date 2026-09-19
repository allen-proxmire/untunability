# C3c: growing a 3D slice, specified on paper

*ED_Attempt_07, note 18. 2026-09-17 (RD32). Ledger: C65–C67. **A specification only: no code, nothing run.** Implementation questions C3c-Q1–C3c-Q5 and the expected results are for Allen to confirm; running is a separate yes.*

## Accepted (C65)

**Allen chose (a) of C64** (D25: "a, spec C3c on paper"). C3b's pass stands:
> "Each bad 3D shape is flagged by one existing ED meaning, and a flat 3D slice by none."

C3c asks whether the three meanings, acting together on growth, **keep** a growing 3D slice flat.

## First, on paper: counts in a 3D slice (C66)

**A closed 3D triangulation** (V events, E links, F triangles, T tetrahedra) has F = 2T, V − E + F − T = 0, so **E = V + T**. Each tetrahedron has 6 edges, so the **mean edge valence is 6T/E.**

**Flat space:**
- **edge valence** 2π/arccos(1/3) = **5.104** (C56);
- **T/V** = 5.104 / (6 − 5.104) = **5.70**;
- **E/V = 6.70;**
- **mean degree 13.4.**

**The flat start used below** (each cube of a periodic grid cut into 6 tetrahedra along its long diagonal) has:
- degree **14**;
- E = 7V and T = 6V;
- mean edge valence 36/7 = **5.14**.

**How the pressures pull on those counts:**

| pressure | pulls toward | shape it favours if unopposed |
|---|---|---|
| **Commitment** (each link costs) | fewer links per event, so lower T/V and mean valence below 5.10 | **branched** (elongated; the large vertex-weight side of 3D DT) |
| **Quadratic curvature cost** | every edge valence near 5.10 | locally flat; large scales unknown (C53 in 2D) |
| **Sync** (reward links where ticks differ most) | more links at strained necks | against branching; unopposed, **more links everywhere strained** (toward crumpled) |

- **So the three don't just add. Commitment and sync pull against each other,** and curvature pins the local count. A flat middle, if there is one, is where they balance.
- **This is the balance C58 flagged, now as counts.**

## The model (C67)

### The slice

- **A triangulated 3-torus**, stored as its tetrahedra, with each event's link (the triangles opposite it).
- **Start:** the flat cube-grid triangulation, n³ events. **n = 16, 24:** V = **4,096** and **13,824**.
- **Budget:** each event starts with budget 1. Rates are persistent: ω = 1 + σg with **σ = 0.0005**, **K = 0.5** (C2b run 3).

### Each tick

1. **Offspring**, as C3a: c geometric with mean max(0, 1 + k(b − 1)), **k = 1**.
2. **Merges** (childless events, in random order):
   - **the move:** contract the link to a neighbour a, allowed only under the **3D link condition** Lk(v) ∩ Lk(a) = Lk(va) (Dey–Edelsbrunner);
   - **the partner:** chosen with weights e^(−ΔS);
   - **no allowed partner:** a counted forced keep;
   - **budget and rate:** the budget passes to a, which keeps its own rate and tick count.
3. **Splits** (c − 1 per event with c ≥ 2, in random order), on the newest child x:
   - **the options:** one per neighbour u of x. The new child takes the **star of u** in x's link sphere (the link triangles touching u), plus new tetrahedra joining the two children to the boundary of that star;
   - **the choice:** made with weights e^(−ΔS);
   - **inheritance:** children inherit the parent's rate and tick count, and share its budget equally.
4. **Flips** (cut and rejoin, C3-Q6): one sweep of attempts, as many as there are events.
   - **The attempt:** pick a random triangle for a 2–3 move or a random valence-3 edge for a 3–2 move, whichever the proposal draws.
   - **Acceptance:** min(1, proposal correction × e^(−ΔS)).
5. **Sync update** (C2b): φ ← φ + ω + (K/deg)·Σ tanh(φ_y − φ_x) over the current links.

### The move cost S (C3-Q7–C3-Q9)

> **S = α · E + λ · Σ over edges (valence − 5.104)² − γ · Σ over links ((φ_x − φ_y) / (σ/K))²**

**ΔS** is computed only over the links and edges a move touches.

| term | meaning | knob |
|---|---|---|
| α·E | **Commitment:** each link costs | α |
| λ·Σ(valence − 5.104)² | **Quadratic energy** in 3D | λ |
| −γ·Σ(normalized tick difference)² | **Sync:** links carrying strain are kept, and new links across strain are favoured | γ |

**Settings** (strengths are knobs, set to 1 as the unit choice, recorded):

| | setting | α | λ | γ | what it shows |
|---|---|---|---|---|---|
| **S0** | No pressure (all choices uniform, flips always accepted if valid) | 0 | 0 | 0 | What growth alone does |
| **S1** | Commitment only | 1 | 0 | 0 | Its own pull |
| **S2** | Curvature only | 0 | 1 | 0 | Its own pull |
| **S3** | Sync only | 0 | 0 | 1 | Its own pull |
| **S4** | **All three** | 1 | 1 | 1 | **The hypothesis** |
| **S5** | All three, stronger sync | 1 | 1 | 4 | Whether the balance point moves |

### Calibrations

- **FC (flat):** the cube-grid start at each size, read with no growth.
- **RC (random):** the flat start after 50 sweeps of uniform 2–3 and 3–2 flips (Metropolis-corrected to the uniform measure at fixed V). This is the standard 3D random-triangulation sampler, expected to crumple.

### Readings, at ticks T/2, 3T/4 and T

| reading | what it is |
|---|---|
| **d_H and the exponential-growth flag** | Ball-growth part of readings v2 (C3b's form) |
| **Link cost** | Mean and largest degree |
| **Curvature** | Mean and spread of edge valence; mean (valence − 5.104)² |
| **Neck strain** | The largest single-link tick difference in the exact linear steady state with fresh rates (C3b's signal), in units of the flat calibration's value at the same size |
| **Settled** | \|d_H(T) − d_H(3T/4)\| ≤ 0.15 and largest degree changing by ≤ 20% |
| **Balance** (reported) | Size relative to V at the start; forced keeps |
| **In-run sync** (reported) | Largest \|φ_x − φ_y\| over links, normalized |

### Shape classification at a size (from C3b's signals, fixed now)

| shape | test (at T, median of seeds) |
|---|---|
| **Crumpled** | Largest degree ≥ 3× the flat calibration's |
| **Hyperbolic** | Exponential-growth flag set |
| **Branched** | Neck strain ≥ 3× the flat calibration's, or d_H < 2.3 |
| **Flat 3D** | **None of the above,** and d_H in [2.5, 3.5] |
| **Unclassified** | Anything else |

**Structure checks, every tick** (exact):
- every triangle belongs to exactly two tetrahedra;
- every event's link is a 2-sphere (Euler characteristic 2 and connected);
- V − E + F − T = 0;
- no repeated tetrahedra;
- budget conserved to 10⁻⁹.

**Seeds:** 0 and 1; flip and choice randomness come from the same stream.

## Expected results, written down before any code

**All labelled low confidence except E0 and E1:** 3D growth like this hasn't been run before, here or, as far as this search found, in the literature.

| | expected | why |
|---|---|---|
| **E0** calibrations | **FC:** classified flat 3D at both sizes. **RC:** not flat 3D at both sizes | The readings must separate flat from random 3D |
| **E1** structure and balance | Every check exact; every run survives; size within ±10% of the start | The moves keep topology (C55); the budget window holds (C48) |
| **E2** S0 | Not flat 3D at the larger size (most likely crumpled) | Uniform 3D triangulations crumple |
| **E3** S1 | Branched at the larger size | Commitment alone lowers links per event (C66) |
| **E4** S3 | Not flat 3D at the larger size (most likely crumpled) | Sync alone rewards links everywhere strained (C66) |
| **E5** S4 | **Flat 3D at both sizes, settled** | The hypothesis (C56, C57, C64) |
| S2, S5 | Reported | S2: 2D suggests locally flat only; S5: where the balance moves |

## Exit rule

**First:**
- **E1 fails:** a code bug (recorded).
- **E0 fails:** a readings revision (recorded).
- **S4 or S5 unsettled at T:** "not settled in T ticks"; revise T (recorded).

**Then:**

| outcome | record |
|---|---|
| **S4 or S5 flat 3D at both sizes, and S0 not flat** | **"Commitment, quadratic energy and sync together grow a flat 3D slice at the sizes run: consistent, not derived; α, λ, γ are knobs."** Then larger sizes and a knob scan (spec) |
| **S0 flat 3D at both sizes** | "Growth alone keeps a 3D slice flat at these sizes"; the pressures aren't needed here. Take stock |
| **S4 and S5 not flat,** but each takes a named bad shape | "The three pressures don't balance at unit strengths: ⟨shapes⟩." Then a knob scan on paper, or take stock (Allen decides) |
| **Otherwise** | "A flat 3D slice isn't grown with ED's local moves at these strengths." Take stock |

**E2–E4 not as expected** are recorded as findings; the verdict follows the table.

## Honest cost plan

- **This is the heaviest model so far,** in plain Python with no compiled speed-ups available.
- **Rough guess before timing:** a few seconds per tick at 4,096 events and 10–20 s at 13,824.
- **Budget:** 6 settings × 2 sizes × 2 seeds = **24 runs**, plus 4 calibrations, on 6 workers.
- **Running order:**
  1. **Code** (`model/c3c.py`, runner, timing), with implementation notes written before any run. Code tests on small tori (n = 4, 6): every move checked against the structure checks.
  2. **Timing trial:** 10 ticks per size for S0 and S4, plus readings. **Timing only.**
  3. **Choose T:** the largest of 500, 300, 200 that fits in **about 10 hours on 6 workers.** If even T = 200 doesn't fit, record it and bring options to Allen (smaller sizes, fewer settings, or a compiled port) **before any run.**
  4. **Calibrations**, then the runs. Resumable, one file per run.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3c-Q1** | **Split choices limited to "the star of one link neighbour"** (one option per neighbour), with flips supplying the rest of the rearrangement? | **Yes** | Simple, local and always valid; flips reach all triangulations (Pachner) |
| **C3c-Q2** | **One flip sweep per tick,** Metropolis with the same cost S? | **Yes** | Cut-and-rejoin at the same pace as growth; one cost for every move |
| **C3c-Q3** | **The sync term as −γ·Σ(normalized tick difference)²** over links, rewarding links that carry strain? | **Yes, labelled** | The direct form of C3-Q7; normalized by σ/K so γ = 1 is a unit choice |
| **C3c-Q4** | **Unit strengths α = λ = γ = 1** (plus S5 with γ = 4), all recorded as knobs? | **Yes** | No basis yet for other values; S5 shows sensitivity |
| **C3c-Q5** | **Sizes 4,096 and 13,824, two seeds, T set by the timing trial within about 10 hours**, with options brought back if it doesn't fit? | **Yes** | Big enough for ball readings in 3D; cost-bounded |

## Next step

**If the defaults hold:** write the code with small-torus move tests and implementation notes, and run the timing trial. **Running needs a separate yes.**

## Guards added before results (D29)

*After a health peek at two saves (C69), before any results were read. Recorded as a revision.*

- **Densification guard:** a run stops, recorded as **"densified,"** when its tetrahedra per event exceed **20** (flat is 5.70). It's checked before each tick, so a resumed run already past the limit stops at once.
- **E1 restated:** structure exact and budget conserved, and **either** the run completes T ticks with its mean late size within ±10% of the start, **or** it stops on a recorded guard (died, ran away, densified). **A guard stop is an outcome, not a code bug.**
  - **Why:** in a dense slice, a childless event often has no partner it can merge with without pinching the space, so it's forced to keep a child. Thousands of forced keeps per tick break the budget's size control and push the event count up. That's the rule's behaviour at these strengths.
- **More recorded per run:** ticks done, events, tetrahedra, links, tetrahedra per event, mean and largest degree, and the forced-keep share.
- **In the exit rule:** a guard-stopped setting's shape is that guard's label, which counts as a named bad shape in the "don't balance" branch.
- **Unchanged:** the rules, strengths, sizes, seeds, T, readings, calibrations, classification and the order of the exit rule.
