# Allen's ideas and decisions (ED_Attempt_10)

## Definitions and ideas (D)

| ID | idea (Allen's words where possible) | date | related |
|---|---|---|---|
| D1 | Attempt 10 opened on what sets the shape. Allen: 'a, conclude attempt 9 and open attempt 10.' | 2026-09-21 | A9-ledger D14, RD14 |
| D2 | Start S1 on paper. Allen: 'go ahead with S1'. | 2026-09-21 | C2-C5 |
| D3 | S1-Q1 yes: ED's rule is a list of what is allowed and every allowed history counts once; S1-Q2 yes: links join only events in the same slice or the next. Spec the counting test on paper. Allen: 'yes to both, spec the counting test on paper'. | 2026-09-21 | C5-C7 |
| D4 | C-Q1 yes: one history is the spacetime (events, links, parents), order within a tick not distinct; C-Q2 yes: every slice exactly V events; C-Q3 yes: mostly one child as at most 10% of events changed per tick, all change types counted; C-Q4 yes: stage B time periodic, technical. Run stage A. Allen: 'yes to all four, run stage A'. | 2026-09-21 | C7-C10 |
| D5 | Option (b) with (c) folded in: revise stage A's rule to compare only slices ED allows (the off-budget crumpled FRc dropped; revision made after results, recorded), and first make a flat reference at ED's link density. Allen: 'b with c folded in, make the flat reference first'. | 2026-09-21 | C10-C12 |
| D6 | Build the flat reference by adding events (C12's edge-split construction with the revised checks) and count it. Allen: 'a, build it by adding events and count it'. | 2026-09-21 | C12-C14 |
| D7 | Spec stage B in 3D on paper. Allen: 'a, spec stage B in 3D on paper'. | 2026-09-21 | C15, C16 |
| D8 | B-Q1 yes: every slice has exactly ED's link count; B-Q2 yes: changes in one tick at separate places; B-Q3 yes: the ring stage checks the program against an exact count, not CDT. Allen chose option (a), then 'Yes to all three' when asked. | 2026-09-21 | C16 |
| D9 | Open question put to Allen (C17): which 3D split/merge pair ED means for counting histories - (i) narrow both ways (edge split, merge only of edge-shaped events), (ii) general both ways (vertex split along any separating cycle, A7 C3-Q6's wording, and link-condition merge) [proposed, with a recount first], (iii) as implemented, past and future counted separately. Not decided. | 2026-09-21 | C17 |
| D10 | D9 answered, choice (ii): general both ways - a split gives the child any connected patch of its parent's neighbours (vertex split along a separating cycle, A7 C3-Q6's wording, replacing A7 C3c-Q1's one-neighbour narrowing), merges as before (link condition); spec the recount on paper. Allen: 'a, choose (ii) and spec the recount on paper'. | 2026-09-21 | C17, C18 |
| D11 | Run the recount as specified. Allen: '(a)'. | 2026-09-21 | C19, C20 |
| D12 | Take stock of road S on paper. Allen: 'a, take stock of road S on paper'. | 2026-09-21 | C21 |
| D13 | Allen, mid-turn after the road S stock-take: 'whats the answer mate. i feel like you see it. can we just do what will make it work, lol?' Taken as go-ahead for the stock-take's proposed option (a), the recount under choice (i), as a test; D10 not revised. | 2026-09-21 | C22 |
| D14 | ED's 3D moves are narrow both ways: a new event appears only on a link between two existing ones (edge split), and an event can disappear only by stepping back out from between two (merge only when it is the exact reverse of an edge split); flips as before. Revises D10. Then run the forward-growth check. Allen: 'a, adopt narrow both ways and run the check'. | 2026-09-21 | C22, C23 |
| D15 | Update stage B's plan for narrow moves and build it. Allen: 'a, update the plan and build it'. Flagged reading (C24), not decided by Allen: a single flip may ride in a link-balanced bundle. | 2026-09-21 | C24 |
| D16 | Build a strongly crowded start at exact counts (note 16 option (a)), then run stage B. Allen: 'a, build the crowded start then run it'. | 2026-09-21 | C29 |
| D17 | Run the short-loop diagnostic (note 17 option (a)). Allen: 'a, run the short-loop test'. | 2026-09-22 | C31 |
| D18 | Add the whole-history move and rerun. Allen: 'a, add the whole-history move and rerun'. | 2026-09-22 | C32 |
| D19 | Take stock of road S and attempt 10. Allen: 'a, take stock of road S and attempt 10'. | 2026-09-22 | C33 |
| D20 | Conclude attempt 10 and open attempt 11. Allen: 'a, conclude attempt 10 and open attempt 11', with: 'is this the next natural step? am i beating a dead horse? i dont think so - I still think ED has legs ... all this testing is out of my wheelhouse and i barely know whats going on ... idk if we are making progress though ... what is attempt 11 all about?' | 2026-09-22 | C34 |

## Recorded steps (RD)

| ID | from | what was done | date |
|---|---|---|---|
| RD1 | D1 | ED_Attempt_10 opened: note 1 `Carry_Forward.md` (C1), written plainly, the README and this ledger. Opening road S, what sets the shape. | 2026-09-21 |
| RD2 | D2 | Note 2 `S1_What_ED_Conserves.md` written plainly: totals exhausted (C2), literature check (C3), why ED hits the wall (C4), the counting proposal with questions S1-Q1 and S1-Q2 and options (C5). Nothing computed. | 2026-09-21 |
| RD3 | D3 | Note 3 `S2_Counting_Test_Spec.md` written plainly: the counting-may-lean-crammed warning (C6), stage A sign check and stage B full test with expectations and exit rules (C7), questions C-Q1 to C-Q4, options. Nothing computed. | 2026-09-21 |
| RD4 | D4 | Stage A coded, checked (A0 exact) and run, about 20 minutes; revision FR to FRc recorded before results; note 4 `SA_Results.md` written plainly. | 2026-09-21 |
| RD5 | D5 | Flat-reference construction by biased flips written with expectations first and piloted at five biases; R0 failed for all that reached the density, so stopped with nothing counted; note 5 `Flat_Reference.md` with an edge-split construction proposed. | 2026-09-21 |
| RD6 | D6 | Reference built (one-link miss, fixed with three valence-6 splits, recorded), checked and counted; verdict 'counting leans toward flat at one tick'; note 6 `Flat_Reference_Results.md` written plainly. | 2026-09-21 |
| RD7 | D7 | Note 7 `S2B_Spec.md` written plainly: why counting whole histories may win (C15), the program, gates G1-G3, runs, readings, pass rule and other outcomes, honest cost, questions B-Q1 to B-Q3 (C16). Nothing built. | 2026-09-21 |
| RD8 | D8, C17 | Before building stage B, found that the 3D split and merge are not mutual inverses; stage A's 'same count by construction' statement corrected, its verdict withdrawn as a statement about histories; note 8 `Stage_A_Correction.md` written plainly with the question D9. Nothing built. | 2026-09-21 |
| RD9 | D10 | Note 9 `S2A2_Recount_Spec.md` written plainly: the general split, how its options are counted (exact, floor, estimate), checks R0-R2, expectation, exit rule, cost (C18). Nothing built. | 2026-09-21 |
| RD10 | D11 | Recount built, checked (R0 revised twice, recorded), run in about 20 minutes; verdict 'counting leans toward crowded slices'; note 10 `S2A2_Results.md` written plainly. | 2026-09-21 |
| RD11 | D12 | Note 11 `Road_S_Verdict.md` written plainly: what road S tried, Allen's decisions, five findings, the wall restated, what is left (including choice (i), set aside without evidence), what stands, cost and slips, four options with (a) proposed. Nothing computed. | 2026-09-21 |
| RD12 | D13 | Recount under narrow both ways built, checked (N0 fix recorded), run in about 20 minutes; verdict 'counting leans toward flat'; note 12 `S2A3_Narrow_Results.md` written plainly with the adoption question. | 2026-09-21 |
| RD13 | D14 | Narrow-merge tick p10.py and forward-growth check built; G0 passed; first run's grid start frozen (recorded), flat-reference starts added before rerun; note 13 `N1_Growth_Results.md` written plainly. | 2026-09-21 |
| RD14 | D15 | Note 14 `S2B_Narrow_Plan.md` written plainly before any stage B code: bundles, starts, gates, pass rule unchanged, flagged reading (C24). | 2026-09-21 |
| RD15 | D15 | Stage B core and ring gate built; G1 passed exactly after three recorded revisions (ring size, parent-swap move, exact test in place of the frequency rule); starts built; note 15 `S2B_G1_Results.md` written plainly. | 2026-09-21 |
| RD16 | D15 | 3D operations built; G2 passed after a proposal-efficiency revision; G3 run and failed; stopped for Allen rather than raising sizes, with the diagnosis; note 16 `S2B_G2_G3_Results.md` written plainly. | 2026-09-21 |
| RD17 | D16 | crowded_grown built (strongly crowded at exact counts); G3 rerun and passed at n = 16 with the spacetime reading judged there only (recorded); stage B runs launched with rules fixed in sb_run.py. | 2026-09-21 |
| RD18 | D16 | Stage B runs completed; results inconclusive by the rule (starts disagree, nothing moved); note 17 `S2B_Run_Results.md` written plainly with a short-loop diagnostic proposed. | 2026-09-22 |
| RD19 | D17 | Short-loop diagnostic run (FROZEN) with a labelled follow-up diagnostic; note 18 `S2B_Short_Loop_Results.md` written plainly with a whole-history move proposed. | 2026-09-22 |
| RD20 | D18 | Whole-history move built, exact on rings, rerun on short loops: FROZEN; note 19 `S2B_Global_Results.md` written plainly. | 2026-09-22 |
| RD21 | D19 | Note 20 `Taking_Stock.md` written plainly: findings, decisions, the wall restated, a reading kept not claimed, what stands, what is open, cost and slips, options with (a) proposed. Nothing computed. | 2026-09-22 |
| RD22 | D20, C34 | Attempt 10 concluded; ED_Attempt_11 opened with note 1 Carry_Forward.md (A11 C1), README and ledger; opening road L; new ground rule, a picture before every test. | 2026-09-22 |
