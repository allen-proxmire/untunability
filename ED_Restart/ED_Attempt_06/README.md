# ED_Attempt_06

**Started 2026-09-15 (RD1). Concluded 2026-09-16 (RD30).** See the final section of [Taking_Stock.md](Taking_Stock.md) and [Attempt_06_Plain_Language.md](Attempt_06_Plain_Language.md). The sixth attempt. Allen: "close attempt 5 and open 6."

**What it starts from:**
- **Attempt 5's carry-forward** (A5-ledger RD16): three inputs supplied, the revised meanings, and the walls. See [Carry_Forward.md](Carry_Forward.md).
- **The cross-attempt inputs table:** [What_ED_Needs.md](../What_ED_Needs.md).

**First roads** (each gets its meanings and exit rule fixed with Allen before anything is computed):
- **Road W:** waves on a direction-free random pattern. Do they travel at one speed in every direction, with no short waves slower than light? **Closed with a wall (RD4, C15):** direction-free walks on patterns with loops have many stuck states.
- **Road G:** a growth rule. Can relations grow from the One Being into a direction-free, three-dimensional pattern that stays that way? **Closed with a wall (RD9, C40):** no rule from ED's meanings found produces a smooth pattern.

| file | what it is |
|---|---|
| [Carry_Forward.md](Carry_Forward.md) | Note 1: what attempt 5 hands over, and the two proposed roads |
| [W1_Waves_Random_Pattern.md](W1_Waves_Random_Pattern.md) | Note 2: road W part 1, on paper. Long waves on a random pattern are direction-free on average; for positive-weight spreading rules every short wave is slower than light on any pattern, with or without ticks; first-order walks open; W-Q1–W-Q3 and a draft exit rule |
| [W2_Leak_And_Stuck_States.md](W2_Leak_And_Stuck_States.md) | Note 3: road W part 2, on paper. Husain–Louko's leak rests on a detector that never recoils, so in ED it becomes stuck states and unevenness; any direction-free coined walk on a pattern with loops has at least a share 1 − 2/(mean neighbours) of states that never move (checked); W-Q4, W-Q5 and a draft exit rule |
| [G1_Growth_Rule.md](G1_Growth_Rule.md) | Road W's verdict (closed with the stuck-state wall), then note 4: road G part 1, on paper. Adding never stretches distances, so adding alone can't expand; random attachment and random rewiring lose finite dimension; a rule favouring nothing ends non-space-like, so growth needs a named favoured quantity; G-Q1–G-Q4 and a draft exit rule |
| [G2_Favoured_Quantity.md](G2_Favoured_Quantity.md) | Note 5: road G part 2, on paper. Sync alone favours small worlds (its weak reading gives only a floor, d ≥ 3); maximal commitment favours a single chain; what the present can carry presupposes space; combined, the fewest directions in which rates can match is three, suggestive; G-Q5–G-Q7 and a draft exit rule |
| [G3_Rates_Can_Match.md](G3_Rates_Can_Match.md) | Note 6: road G part 3, on paper. Rates can match only if a patch's edge count (the ball-cut) outgrows the √count surplus of its random rates, so only above two dimensions, with no ratio in the floor; three is the fewest whole-number dimension (whole numbers from A5 D11's smoothness assumption); a reason for three, consistent, not derived; G-Q8–G-Q10 |
| [G4_Step_Rule.md](G4_Step_Rule.md) | Part 3's verdict (a reason for three among smooth patterns), then note 7: road G part 4, on paper. A step rule sees only local counts; ED's sync-plus-cost process heads to the floor just above two dimensions, not to a smooth three; smoothness is the missing piece; G-Q11, G-Q12 and a draft exit rule |
| [Taking_Stock.md](Taking_Stock.md) | Road G's verdict (closed with the smoothness wall), then note 8: stock-take of attempt 6. Scorecard, tally (inputs supplied still 3; two reasons for three), gains, five walls, method notes, options |
| [Attempt_06_Plain_Language.md](Attempt_06_Plain_Language.md) | The plain-language version of attempt 6 (RD11, updated RD14): roads W and G, smoothness, loops, where attempt 6 stands, honest limits |
| [S1_Smoothness.md](S1_Smoothness.md) | Note 9: smoothness, on paper. Curvature bounded below, a finite dimension ceiling and quadratic energy give smooth spaces with one whole-number dimension; ED's meanings offer readings for each; three comes out of conditions; smoothness needs short loops, against the stuck-state wall; S-Q1–S-Q3 |
| [L1_Loops.md](L1_Loops.md) | Smoothness verdict (reframed as conditions), then note 10: loops, on paper. Wave states split exactly into a moving sector built from locus values and a stuck sector; direction-free matter only touches the moving sector, so stuck states are dark and loops don't trap light (checked); L-Q1–L-Q3 |
| [M1_Model_Spec.md](M1_Model_Spec.md) | Note 11: the constrained growth model, specified on paper (no code, nothing run). Rules from ED's meanings, a no-curvature control, four scanned knobs, readings of dimension and smoothness with calibrations, expected results and an exit rule fixed first; M-Q1–M-Q5 |
| [model](model/) | The constrained growth model's code (note 11): readings, process, calibrations, timing trial, and implementation notes written before any run |
| [M1_Trial_Results.md](M1_Trial_Results.md) | Note 12: the model's first runs. Calibrations 2 of 4 as expected (readings biased at the grain and at the pattern's edge); the timing trial froze at 50 loci because sync filled every locus to its cap; a proposed readings fix; options |
| [M2_Model_Spec.md](M2_Model_Spec.md) | Note 13: the revised growth model M2, specified on paper. One change from note 11: a newborn goes inside a relation (a–b becomes a–z–b), removing the freeze and stretching distances; expected results and exit rule fixed first; M2-Q1–M2-Q3 |
| [M2_Timing_Results.md](M2_Timing_Results.md) | Note 14: M2 timing trial. No stalls; the constrained central setting grows a single ring, because the curvature floor rejects the first triangle; the control grows densely; plan about 7 hours; budget and options |
| [O1_Time_Order.md](O1_Time_Order.md) | Note 15: time order, on paper. The growth models grew space without ED's time order; causality is what separates smooth from fractal geometry; ED already has order plus count; O-Q1–O-Q3 |
| [O2_Causal_Growth_Literature.md](O2_Causal_Growth_Literature.md) | Time-order verdict, then note 16: the literature on finite-neighbour causal growth. A framework exists but no selecting rule; 2D CDT is exactly a random tree with slice dimension given; the growth wall stated as a precise open problem |
| [M2_Strong_Sync_Results.md](M2_Strong_Sync_Results.md) | Note 17: M2 results at weak and strong sync. No run reaches smooth three; ring, rough tangle or stall, or small world; a test of space-without-time |
| [checks](checks/) | Scripts behind computed claims, with recorded outputs |
| [01_Ledger](01_Ledger/) | This attempt's ledger: claims, Allen's ideas and decisions, a dated log |

**Stock taken (note 8), updated after smoothness and loops (RD14).** Both roads closed with walls; smoothness reframed as conditions a growth rule must keep; stuck states reframed as a dark sector. Attempt 6 stays open.

**Ground rules**
- **Attempt 1's working rules apply:** `../ED_Attempt_01/00_Rules` and `../ED_Attempt_01/01_Ledger/README.md`.
- **The write-ups use no prediction language.**
- **Attempts 1–5 are closed records:** referenced, never edited. References are written A1- through A5-ledger.
- **Allen decides what ED means.** Claude proposes least-structure defaults with reasons; nothing is decided until Allen says so.
- **Every road gets its meanings and its exit rule fixed with Allen before anything is computed.** Every check has its expected results written before it runs.
- **The census guard:** a result counts as a reduction only if ED's input list is shorter, with no added free parameters.
