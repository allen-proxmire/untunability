# ED_Attempt_10

**Started 2026-09-21 (RD1). Concluded 2026-09-22 (RD22).** See [Taking_Stock.md](Taking_Stock.md). Handed to [ED_Attempt_11](../ED_Attempt_11/). The tenth attempt. Allen: "a, conclude attempt 9 and open attempt 10."

**What it starts from:**
- **Attempt 9's carry-forward** (A9-ledger C42, C43, RD14): the answer that ED's growth is missing one ingredient — a strong, size-scaling preference for extended shape — the meanings through attempt 9, the inputs, the walls and the tools. See [Carry_Forward.md](Carry_Forward.md).
- **The cross-attempt inputs table:** [What_ED_Needs.md](../What_ED_Needs.md).

**Opening road** (meanings and expected results fixed with Allen before anything is computed):
- **Road S, what sets the shape?**
  - **S1:** on paper — is there something ED conserves that would prefer extended space by itself, the way the budget sets size?
  - **S2:** the test — tune a strength in a proper weighing over whole histories, and see whether any strength gives three-dimensional space.

| file | what it is |
|---|---|
| [Carry_Forward.md](Carry_Forward.md) | Note 1: what attempt 9 hands over, in plain language |
| [S1_What_ED_Conserves.md](S1_What_ED_Conserves.md) | Note 2: **S1 on paper.** No new conserved total exists; the rival theory's extended space comes from counting histories, not a preference; proposal and questions |
| [S2_Counting_Test_Spec.md](S2_Counting_Test_Spec.md) | Note 3: **the counting test, on paper.** A warning that counting may favour crowded shapes; a cheap check of which way it leans (stage A) before the full test (stage B); questions |
| [SA_Results.md](SA_Results.md) | Note 4: **stage A results.** In 3D the small worlds ED grows have far fewer ways to have happened than flat: counting pushes toward flat. One forbidden crumpled shape ties, so the rule reads 'too close'; options |
| [Flat_Reference.md](Flat_Reference.md) | Note 5: **the flat reference, first try.** Rewiring the grid to ED's density roughens it, so it failed the check; building it by adding events instead is proposed |
| [Flat_Reference_Results.md](Flat_Reference_Results.md) | Note 6: **counting leans toward flat.** A flat slice at ED's exact density has far more one-tick histories than the small worlds ED grows; next, stage B in 3D |
| [S2B_Spec.md](S2B_Spec.md) | Note 7: **stage B on paper.** Why counting whole histories might win, the program, its checks, the pass rule, the cost, and three questions |
| [Stage_A_Correction.md](Stage_A_Correction.md) | Note 8: **a mistake in stage A.** In 3D, ED's split and merge aren't each other's reverse, so counting where a slice came from differs from where it goes; the verdict is withdrawn; a question |
| [S2A2_Recount_Spec.md](S2A2_Recount_Spec.md) | Note 9: **the recount with general splits, on paper.** How the ways to split are counted, the checks, the expectation and what follows |
| [S2A2_Results.md](S2A2_Results.md) | Note 10: **recount results.** With general splits, crowded small worlds have far more ways to have come about than flat space; counting favours them. Road S goes to stock-taking |
| [Road_S_Verdict.md](Road_S_Verdict.md) | Note 11: **road S stock-taken**, in plain language. What it tried, the wall restated (what ED allows in one tick decides it), what is left, and the options |
| [S2A3_Narrow_Results.md](S2A3_Narrow_Results.md) | Note 12: **narrow both ways: counting leans toward flat.** With consistent narrow moves, flat has more ways to have come about than crowded slices; adopting it is your call |
| [N1_Growth_Results.md](N1_Growth_Results.md) | Note 13: **growing forward with narrow moves.** The collapse is about seven times slower but not stopped; stage B (counting) is still the test |
| [S2B_Narrow_Plan.md](S2B_Narrow_Plan.md) | Note 14: **stage B's plan for narrow moves.** Balanced bundles, the two starts, the three gates; the pass rule unchanged |
| [S2B_G1_Results.md](S2B_G1_Results.md) | Note 15: **stage B's first gate passed exactly** on ring slices, after three recorded fixes; a side finding about crowding at ED's density |
| [S2B_G2_G3_Results.md](S2B_G2_G3_Results.md) | Note 16: **the 3D program works (G2); the crowded start isn't crowded enough (G3).** At ED's exact counts, random rewiring leaves a slice nearly flat; options |
| [S2B_Run_Results.md](S2B_Run_Results.md) | Note 17: **stage B results, inconclusive.** Each start stayed exactly where it began; the history moves too slowly for the answer to show; a short-loop diagnostic proposed |
| [S2B_Short_Loop_Results.md](S2B_Short_Loop_Results.md) | Note 18: **short loops frozen too, and why.** Changes are short-lived; the history's shape barely moves; a whole-history move proposed |
| [S2B_Global_Results.md](S2B_Global_Results.md) | Note 19: **the whole-history move: still frozen.** Exact, but blocked by short-lived changes in every tick; take stock proposed |
| [Taking_Stock.md](Taking_Stock.md) | Note 20: **road S and attempt 10 stock-taken**, in plain language. What it found, what you decided, the wall restated, what stands and what is open, options |
| [model](model/) | Stage A code: `sa_count.py`, `sa_report.py`, results in `sa_count.txt` |
| [01_Ledger](01_Ledger/) | This attempt's ledger: claims, Allen's ideas and decisions, a dated log |

**Ground rules**
- **Attempt 1's working rules apply:** `../ED_Attempt_01/00_Rules` and `../ED_Attempt_01/01_Ledger/README.md`.
- **Attempts 1–9 are closed records:** referenced, never edited. References are written A1- through A9-ledger.
- **Allen decides what ED means.** Claude proposes least-structure defaults with reasons; nothing is decided until Allen says so.
- **Every road gets its meanings and exit rule fixed with Allen before anything is computed.** Every check and model run has its expected results written first.
- **Revise and retest is the normal workflow.** Everything is recorded, including misses and changes of plan.
- **The write-ups use no prediction language.**
- **The census guard:** a result counts as a reduction only if ED's input list is shorter, with no added free parameters.
- **Plain language first.** Allen reads the notes; the technical detail lives in the ledger.
