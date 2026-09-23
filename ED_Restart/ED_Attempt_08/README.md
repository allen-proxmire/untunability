# ED_Attempt_08

**Started 2026-09-19 (RD1). Concluded 2026-09-21 (RD19).** See [Road_E_Verdict.md](Road_E_Verdict.md), [F1_Results.md](F1_Results.md) and [Taking_Stock.md](Taking_Stock.md). Handed to [ED_Attempt_09](../ED_Attempt_09/). The eighth attempt. Allen: "a, conclude attempt 7 and open attempt 8."

**What it starts from:**
- **Attempt 7's carry-forward** (A7-ledger C105, RD56): three inputs supplied, the meanings decided through attempt 7, five walls with wall 3 restated, and reusable tools. See [Carry_Forward.md](Carry_Forward.md).
- **The cross-attempt inputs table:** [What_ED_Needs.md](../What_ED_Needs.md).

**Opening road** (meanings and expected results fixed with Allen before anything is computed):
- **Road E, resolution:** does a flat three-dimensional middle exist at slices ten times larger, where geometry can be measured — or does ED's growth run crumpled-to-branched at every size?
  - **E1:** on paper. What the compiled model must reproduce, what would count as a flat middle at the larger size, and the exit rule.
  - **E2:** the port, checked against attempt 7 by the three-tier ladder of note 2 (C5: bit-for-bit reproduction is impossible by construction).
  - **E3:** the larger runs.

| file | what it is |
|---|---|
| [Carry_Forward.md](Carry_Forward.md) | Note 1: what attempt 7 hands over — the meanings, the three inputs, the five walls, the four passes, the reusable tools and cost lessons, and the opening road |
| [E1_Resolution.md](E1_Resolution.md) | Note 2: road E part 1, on paper. The literature prior is against a flat middle and ten times the volume buys only 2.2 times the hops, so road E is reframed around whether ED's crumpled-to-branched crossing sharpens or broadens with size; bit-for-bit reproduction shown impossible and replaced with a three-tier validation ladder; expected results, exit rule and cost fixed first; E-Q1–E-Q6 |
| [E3_Model_Spec.md](E3_Model_Spec.md) | Note 3: the E3 model, specified on paper. The threshold's reading-seed wobble removed; the order parameter declared unknown, with a labelled pilot before the campaign that may stop it; the crossing width defined, strangled growth given its own outcome; cost from measured times; E3-Q1-E3-Q6 |
| [E3a_Pilot_Results.md](E3a_Pilot_Results.md) | Note 4: the pilot. Links per event is the only usable order parameter; **ED's conserved link budget and no-infinities ceiling each exclude the crumpled phase**, so E3's crossing has only one side and the campaign is withdrawn; attempt 7's wall wording corrected; options |
| [E4_Model_Spec.md](E4_Model_Spec.md) | Note 5: the E4 model, specified on paper. Does the branched reading survive at size? Grown slices judged against flat at the same size, not against 3; three sizes at one threshold; expected results and an eight-row exit rule fixed first; addendum replacing the gate, declared before the calibrations that judge it |
| [E4a_Sync_Meaning.md](E4a_Sync_Meaning.md) | Note 6: **sync means a whole slice agreeing, not a move-by-move veto** (Allen, D10). How the meaning drifted in three undecided steps; what it reclassifies; why a local veto would make slices stringy; and what it does not fix |
| [E4_Results.md](E4_Results.md) | Note 7: E4's results. Thirteen runs clean to 156,172 events; the fitting window never widened, so every fitted dimension read two hops at short range; **ED's spectral dimension runs with scale** and the fitted number was always the bottom of a dip; the pre-registered test came in at 8.45 against 11.6, so **bigger slices are closed as a route** and the wall stands |
| [Road_E_Verdict.md](Road_E_Verdict.md) | Note 8: **road E closed**, in plain language. ED's growth makes stringy compact patterns, not space, and bigger sizes are ruled out as a route; what road E found along the way; the cost; and the three roads open |
| [Road_3_One_History.md](Road_3_One_History.md) | Note 9: road 3, on paper. What a sum over histories means; where the theories stand; **Allen's decision that many pasts were possible** and his clarification that **the present does not know its own past**; two corrections Claude owed; and the gap - a classical ensemble cannot cancel, while ED's own Born rule input sits unused above the growth model |
| [F1_Whole_Slice_Sync.md](F1_Whole_Slice_Sync.md) | Note 10: road F part 1, on paper. **Sync as a whole slice agreeing** (D10), measured as Synced Now's tilt across scales; the literature's critical dimension 2 against E4's 1.64 with the veto and 2.32 without; sync as a filter rather than a driver; three outcomes fixed first; F-Q1–F-Q5 |
| [F1_Results.md](F1_Results.md) | Note 11: road F's result. The tilt reading calibrated against a ring, a square torus and a cube torus; **the veto slices fail at every size and fail identically**; the controls are not measurable and show no hidden pass; **ED's grown slices cannot hold a common now with the condition or without it**, so fixing sync's form is not enough |
| [Taking_Stock.md](Taking_Stock.md) | Note 12: **stock-take of attempt 8**, in plain language. Its question is answered - it's the rule, not the size; seven findings; the walls, with wall 3 now about the kind of rule; the cost; and the options |
| [model](model/) | The port (E2): attempt 7's slice on flat arrays with a Numba inner loop, the tier 1 and tier 2 verification against attempt 7, timing and profiling, and implementation notes written before the code ran |
| [01_Ledger](01_Ledger/) | This attempt's ledger: claims, Allen's ideas and decisions, a dated log |

**Ground rules**
- **Attempt 1's working rules apply:** `../ED_Attempt_01/00_Rules` and `../ED_Attempt_01/01_Ledger/README.md`.
- **Attempts 1–7 are closed records:** referenced, never edited. References are written A1- through A7-ledger.
- **Allen decides what ED means.** Claude proposes least-structure defaults with reasons; nothing is decided until Allen says so.
- **Every road gets its meanings and exit rule fixed with Allen before anything is computed.** Every check and model run has its expected results written first.
- **Revise and retest is the normal workflow.** Everything is recorded, including misses and changes of plan.
- **The write-ups use no prediction language.**
- **The census guard:** a result counts as a reduction only if ED's input list is shorter, with no added free parameters.
