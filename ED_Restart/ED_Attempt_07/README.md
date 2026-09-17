# ED_Attempt_07

**Started 2026-09-16 (RD1).** The seventh attempt. Allen: "open attempt 7. lets do it, im excited."

**What it starts from:**
- **Attempt 6's carry-forward** (A6-ledger C90, RD30): three inputs supplied, the meanings decided through attempt 6, five walls, reusable tools. See [Carry_Forward.md](Carry_Forward.md).
- **The cross-attempt inputs table:** [What_ED_Needs.md](../What_ED_Needs.md).

**Opening road** (meanings and expected results fixed with Allen before anything is computed):
- **Road C, causal growth:** can a finite-neighbour causal growth rule, where space doesn't split or merge, grow a smooth pattern whose slices sync and commitment make three-dimensional?
  - **C1:** the causal half, checked against 2D CDT's known answer.
  - **C2:** slice dimension from sync and commitment.

| file | what it is |
|---|---|
| [Carry_Forward.md](Carry_Forward.md) | Note 1: what attempt 6 hands over, and road C |
| [C1_Causal_Half.md](C1_Causal_Half.md) | Note 2: road C1, on paper. ED's causal growth with slices given as circles and no splitting, checked against 2D CDT's known answer (slice length 1 + 2t, dimension 2); criticality named as put in; C1-Q1–C1-Q4 |
| [C1_Model_Spec.md](C1_Model_Spec.md) | Note 3: the C1 model, specified on paper (no code). Kesten-tree build with cyclic order, 1,000 seeds for slice length, 10 seeds with calibrated readings, a flat-strip calibration, expected results and exit rule fixed first |
| [C1_Results.md](C1_Results.md) | Note 4: C1 results. PASS: ED's causal growth with no splitting reproduces 2D CDT (slice-length slope 2.05, dimension 2.17, walk-return 1.89, structure exact) |
| [C2_Balance.md](C2_Balance.md) | Note 5: road C2 part 1, the balance, on paper. Offspring averaging exactly 1 is a condition for smooth geometry (below dies, above is hyperbolic); the universe is balanced to 1 part in 10⁶¹; ED's budget as a local feedback toward the balance; C2-Q1–C2-Q4 |
| [C2a_Model_Spec.md](C2a_Model_Spec.md) | Note 6: the C2a model, specified on paper. The naive budget reading pushes away from the balance; budget passed forward and conserved pulls toward it (stable for 0 < k < 2); expected results and exit rule fixed first; C2a-Q1–C2a-Q3 |
| [C2a_Results.md](C2a_Results.md) | Note 7: C2a results. Budget passed forward holds slices at L* in every seed and the geometry stays 2D; the pre-registered offspring check missed on a biased average; the telescoped measure (Allen's prime-triangle point) gives 1.000; adopted, and a fresh-seed retest PASSED |
| [C2_Slice_Dimension.md](C2_Slice_Dimension.md) | Note 8: road C2 part 2, slice dimension, on paper. C2a's balance recorded as self-organizing (Allen's (a)); with time order, sync keeps 'now' space-like, which without a ratio needs slices of dimension 3 or more; commitment's fewest gives three; C2-Q5–C2-Q7 |
| [C2b_Model_Spec.md](C2b_Model_Spec.md) | Note 9: the C2b model, specified on paper. Slices given as 1-, 2-, 3-dimensional grids and random slices, persistent random clock rates with bounded pull; the wobble of 'now' against size; fresh-each-tick control; expected results and exit rule fixed first; C2b-Q1–C2b-Q3 |
| [C2b_Results.md](C2b_Results.md) | Note 10: C2b run 1. Grids show the floor as calculated (wobble exponents 1.40, 0.95, 0.52); fresh-each-tick rates keep a 'now' in every dimension; frame jitter fades in 3D; but two 1D random-slice runs left the linear regime, so the pre-registered exit is 'fix and rerun'; run 2 (σ = 0.0005, 10 seeds) clean in regime but missed at range edges on a noisy statistic; averaged as squares, every range is met; run 3 on fresh seeds PASSED: a synced 'now' needs 3+ dimensions without a ratio in ED's causal pattern |
| [Taking_Stock.md](Taking_Stock.md) | Note 11: stock-take of road C and attempt 7. Three model passes (C1; C2a Budgeted Causality; C2b Synced Now), what's still put in, the walls, an honest assessment, options |
| [Attempt_07_Plain_Language.md](Attempt_07_Plain_Language.md) | The plain-language version of attempt 7 so far (in progress): C1, Budgeted Causality, Synced Now, where it stands, honest limits |
| [C3_Growing_A_Slice.md](C3_Growing_A_Slice.md) | Note 12: road C3, growing a slice of more than one dimension, on paper. Surface moves without splitting; size by budget, shape open; quadratic curvature cost; in 3D commitment and sync rule out random geometry's two bad phases (a lead); C3-Q1–C3-Q5 |
| [C3a_Model_Spec.md](C3a_Model_Spec.md) | Note 13: the C3a model, specified on paper. A torus slice grown from a flat grid by C2a's budget with splits and link-condition collapses; uniform vs quadratic curvature cost; calibrations flat and flip-randomized; expected results and exit rule fixed first; C3a-Q1–C3a-Q4 |
| [C3a_Results.md](C3a_Results.md) | Note 14: C3a results. Uniform growth makes a random surface; the quadratic curvature cost flattens locally but surfaces still roughen with size; the random calibration failed at the smallest size, so the pre-registered exit is 'readings or sizes revision'; read at calibrated sizes (Allen's (a)): a flat 2D slice isn't reached |
| [C3_3D.md](C3_3D.md) | Note 15: road C3 part 2, a 3D slice, on paper. Three bad shapes (crumpled, hyperbolic, branched), each broken by one ED meaning (commitment, quadratic energy, sync); sync acts at large scales through thin necks; limits; C3-Q6–C3-Q10 and a cheap static check first |
| [C3b_Model_Spec.md](C3b_Model_Spec.md) | Note 16: the C3b static check, specified on paper. Five stand-in 3D slices (flat, flat random, branched, hyperbolic, crumpled); does sync flag branching, commitment crumpling, curvature (proxy) hyperbolic, and nothing flag flat? Expected results and exit rule fixed first; C3b-Q1–C3b-Q4 |
| [C3b_Results.md](C3b_Results.md) | Note 17: C3b results. PASS: sync strain grows only on branched slices (always at a neck), link cost only on crumpled, exponential growth on hyperbolic (and crumpled); a flat 3D slice trips nothing. Consistent, not derived; options |
| [C3c_Model_Spec.md](C3c_Model_Spec.md) | Note 18: the C3c model, specified on paper. Growing a 3D slice (3-torus) with commitment, quadratic energy and sync in the move cost; six settings from none to all three; calibrations and shape classification from C3b's signals; expected results, exit rule and a cost plan fixed first; C3c-Q1–C3c-Q5 |
| [checks](checks/) | Scripts behind computed claims, with recorded outputs |
| [model](model/) | Model code for road C (C1): tree build, runs, timing, readings copied from A6, implementation notes written before any run |
| [01_Ledger](01_Ledger/) | This attempt's ledger: claims, Allen's ideas and decisions, a dated log |

**Ground rules**
- **Attempt 1's working rules apply:** `../ED_Attempt_01/00_Rules` and `../ED_Attempt_01/01_Ledger/README.md`.
- **Attempts 1–6 are closed records:** referenced, never edited. References are written A1- through A6-ledger.
- **Allen decides what ED means.** Claude proposes least-structure defaults with reasons; nothing is decided until Allen says so.
- **Every road gets its meanings and exit rule fixed with Allen before anything is computed.** Every check and model run has its expected results written first.
- **Revise and retest is the normal workflow.** Everything is recorded, including misses and changes of plan.
- **The write-ups use no prediction language.**
- **The census guard:** a result counts as a reduction only if ED's input list is shorter, with no added free parameters.
