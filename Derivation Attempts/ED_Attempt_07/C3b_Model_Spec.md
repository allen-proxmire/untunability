# C3b: the static check, specified on paper

*ED_Attempt_07, note 16. 2026-09-17 (RD28). Ledger: C60, C61. **A specification only: no code, nothing run.** Implementation questions C3b-Q1–C3b-Q4 and the expected results are for Allen to confirm; running is a separate yes.*

## Accepted in note 15 (C60)

**Allen accepted C3-Q6–C3-Q10 and the draft exit rule** (D22: "defaults are fine, spec C3b"). So:
- **3D moves:** link-condition merges, splits, and 2–3 and 3–2 flips as cut-and-rejoin (with the "in pairs" flag).
- **Sync:** favours moves that shrink tick differences across links. A labelled reading.
- **Commitment:** penalizes neighbour count.
- **3D curvature cost:** quadratic in (edge valence − 5.10). A labelled reading.
- **First step:** a cheap static check on stand-in slices before any 3D growth code.

## The question C3b answers

> **Does each ED meaning flag its own bad 3D shape, and does no meaning flag a flat 3D slice?**

| meaning | its bad shape | the signal |
|---|---|---|
| **Sync** | Branched (thin necks) | The largest tick difference across a single link grows with size |
| **Commitment** | Crumpled | Links per event grow with size |
| **Quadratic energy** (curvature) | Hyperbolic | Volume grows exponentially with distance |

## The model (C61)

### Stand-in slices

**Five kinds.** Only the flat grid is exact; the others are graphs with each shape's defining feature. Three sizes each, N ≈ 1,000, 8,000, 27,000.

| | stand-in | construction | sizes N |
|---|---|---|---|
| **F** | **Flat 3D grid** | Periodic cubic grid n³, 6 neighbours | n = 10, 20, 30: 1,000, 8,000, 27,000 |
| **FR** | **Flat, random** | N points uniform in the unit 3-torus, linked within the radius for mean degree 14; must be connected (redraws counted) | 1,000, 8,000, 27,000 |
| **B** | **Branched** | Blocks of 4 × 4 × 4 grid events (open edges), joined in a uniform random tree (Prüfer sequence). Each tree edge is **one link** between a random event of each block, which is the thin neck | 16, 128, 432 blocks: 1,024, 8,192, 27,648 |
| **H** | **Hyperbolic** (bounded degree, exponential growth) | Random 6-regular graph, simple and connected (redraws counted) | 1,000, 8,000, 27,000 |
| **Cr** | **Crumpled** (degrees grow with size) | Random graph with mean degree √N (about 32, 89, 164), connected | 1,000, 8,000, 27,000 |

**Seeds:** construction seeds 0, 1, 2 (the grid is the same for every seed); rate seeds 100 + seed.

### Signals

**Sync** (C3-Q7):
- **Rates:** each event gets a persistent random rate ω, and each link pulls as in C2b.
- **Steady state:** in the linear regime it solves K·(D − A)·φ = deg ∘ (ω − Ω), where Ω is the degree-weighted mean rate.
- **How it's computed:** directly, with a sparse linear solve and σ/K = 1. The ratios below don't depend on σ/K.
- **Link tick difference:** the largest |φ_x − φ_y| over all links.
- **Neck tilt ratio:** the pooled largest link difference (root-mean-square over seeds) at the largest size, divided by the same at the smallest size.
- **Also reported:**
  - for B, the share of seeds whose largest difference sits on a neck link;
  - the pooled wobble W and its exponent.
- **What it means:** tanh pull locks only while link differences stay below about 1 in units of K. So a difference that grows with size means some region can't stay synced once the slice is large enough.

**Commitment** (C3-Q8):
- **Degree ratio:** mean degree at the largest size ÷ mean degree at the smallest.
- **Also reported:** the largest degree.

**Curvature proxy** (C3-Q9, recorded as a proxy):
- **Why a proxy:** only F is a triangulation, so edge valence isn't defined for the other stand-ins.
- **What's used instead:** for bounded degree, negative curvature everywhere shows up as exponential volume growth.
- **The reading:** readings v2's exponential-growth flag at the largest size, where `small_world` is true when balls grow faster than a power law or the usable radius is under 5.
- **Also reported:** mass dimension d_H where defined.

### What C3b doesn't test

- growth;
- whether the three pressures balance;
- edge valence on real triangulations;
- the nonlinear unlocking itself (only its linear precursor).

## Expected results, written down before any code

| | expected | why |
|---|---|---|
| **E1** construction | Every stand-in connected. F degree exactly 6; FR mean degree in [13, 15]; B has exactly one link per tree edge; H exactly 6-regular and simple; Cr mean degree within ±10% of √N | Harness |
| **E2** sync | Neck tilt ratio **≥ 3 for B**, and **≤ 1.5 for F, FR, H and Cr** | Branch surplus about √n against a single-link neck (C57): about √27 ≈ 5 over this range. In the other stand-ins a local link difference shouldn't grow beyond slowly (extremes of many local values) |
| **E3** commitment | Degree ratio **≥ 3 for Cr**, and **≤ 1.2 for F, FR, B and H** | √N grows about 5× over the sizes; the others have fixed local degree |
| **E4** curvature proxy | At the largest size, exponential-growth flag **true for H**, **false for F, FR and B**. Cr is reported (a flag there is allowed) | Random regular graphs grow exponentially; flat and branched grow like powers |

**Extra flags on other bad shapes are allowed and reported.** A shape ruled out twice is fine. Examples: sync flagging crumpled, or the growth flag catching crumpled.

## Exit rule (note 15's, made exact)

| outcome | record |
|---|---|
| **E1 fails** | A code or construction bug, fixed and rerun (recorded) |
| **E2, E3, E4 all as expected** | **"Each bad 3D shape is flagged by one existing ED meaning, and a flat 3D slice by none: consistent, not derived."** Then spec 3D growth (C3c) |
| **A meaning misses its shape** | "⟨meaning⟩ doesn't flag ⟨shape⟩." Take stock of road C3 |
| **A meaning flags F or FR** | "⟨meaning⟩ flags a flat 3D slice." Take stock of road C3 |

**Revise and retest is allowed and recorded.**

## Running order

1. **Code** (`model/c3b.py`, runner, timing) with implementation notes written before any run.
2. **Timing trial:** one seed of each stand-in at each size. **Timing only.**
3. **Run:** 5 kinds × 3 sizes × 3 seeds = 45 jobs. Resumable, one result file per job.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3b-Q1** | **The five stand-ins as specified** (flat grid; flat random, degree 14; blocks of 4³ in a random tree with single-link necks; random 6-regular; random graph with mean degree √N)? | **Yes** | Each carries its shape's defining feature, with the smallest construction that does |
| **C3b-Q2** | **Sync signal from the exact linear steady state of C2b's update** (a sparse solve, σ/K = 1), read as the largest single-link tick difference? | **Yes** | Exact and fast; the ratio is independent of σ/K; the linear difference is the precursor of unlocking |
| **C3b-Q3** | **Curvature proxy:** readings v2's exponential-growth flag, since the stand-ins aren't triangulations? | **Yes, recorded as a proxy** | For bounded degree, negative curvature everywhere means exponential growth |
| **C3b-Q4** | **Extra flags on other bad shapes allowed;** only a missed own shape or a flag on flat counts against? | **Yes** | The claim is "each shape has a meaning against it, flat has none," not "exactly one" |

## Next step

**If the defaults hold:** write the code and implementation notes, and run the timing trial. **Running needs a separate yes.**
