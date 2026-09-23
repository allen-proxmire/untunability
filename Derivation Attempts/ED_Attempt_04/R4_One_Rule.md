# Road R4 on paper: one rule for motion, and the speed part

*ED_Attempt_04, note 13. 2026-09-15 (RD17, D25–D28). Ledger: C74–C77. Literature, reasoning and one arithmetic check (`checks/zigzag_clock_check.py`, expected results written first). **Meaning question R4-Q3 and the draft exit rule are for Allen.***

## Where R4 stands

**Allen accepted two readings** (D27):
- **R4-Q1:** "clocks want to sync" means **a body commits as much as it can along its path**. Height raises its commitment rate; speed lowers it (D25). At everyday speeds this is Newton's rule, orbits included (C71).
- **R4-Q2:** **light is uncommitted.** In Allen's words, "light is pattern until it is a particle/absorbed."

**The missing half:** ED has a reading for the height part (blocked loci slow clocks; A3 C38). **It has none yet for the speed part:** why moving slows a body's own commitment.

## Allen's idea for the speed part (D28)

> "speed is part of the rate of commitment? its zipping through loci, committing at each. its eating budget like mass does. syncing/ticking the other part? a duality would fit nature."

**Made precise in the simplest way:**
- **Every commitment is a hop** to a neighbouring locus, one per substrate tick. So at the substrate level **everything moves at one locus per tick,** which is c.
- **In one space direction,** a body makes n_R hops right and n_L hops left.

| | count |
|---|---|
| **Budget** (all hops) | t = n_R + n_L |
| **Net motion** | x = n_R − n_L |
| **Speed** | x / t |

- **Light never turns back** (n_L = 0). All its budget goes into motion.
- **A resting body turns back as often as it goes forward.** None of its budget goes into net motion.

**That is a real duality, and physics has it** (C74):
- **Feynman's checkerboard:** a massive particle is drawn as zigzagging at c, and each turn is weighted by its mass. The sum over zigzags gives the Dirac equation. Attempt 1 already cited this (A1 C295).
- **Penrose's zigzag electron:** an electron is two massless parts, a "zig" and a "zag", each turning into the other. **The mass is the coupling between them.** Jittering between the two gives a speed below c.
- **The energy budget splits the same way:** E² = (pc)² + (mc²)². At rest it's all mass; for light it's all motion.

**So "zipping through loci" versus "ticking" is the zig and the zag, and mass is the turning.** Light doesn't turn, so it has no ticks of its own, which fits R4-Q2.

## The catch: how the budget splits

**The duality alone doesn't fix time dilation.** It depends on which count is the body's own ticks. Three counts, all written from the picture:

| | a body's own ticks are… | own rate at speed v | check |
|---|---|---|---|
| **S1, leftover budget** | the hops not spent on net motion: t − \|x\| | **1 − v/c** (linear) | Z2 |
| **S2, pairings** | every right hop related to every left hop: 2√(n_R·n_L) | **√(1 − v²/c²)** (special relativity) | Z1, Z2 |
| **S3, turns** | the number of direction reversals | depends on how the zigzag's legs change with speed: **no slowing at all** if the legs just shift (S3a); **special relativity** if they stretch and shrink like a Doppler shift (S3b) | Z4 |

**Light has no ticks of its own under all three** (Z3).

**The squares come out exactly for S2.** It's plain arithmetic: 4·n_R·n_L + (n_R − n_L)² = (n_R + n_L)² (Z1). That's **(own ticks)² + (net motion)² = (budget)²**, a right triangle, the same shape as E² = (pc)² + (mc²)².

**Experiment decides between the counts** (C74, Z5). Muons circling at 29.33 times their resting energy lived 29.33 times longer than at rest (Bailey et al. 1977, matching special relativity to 0.2%):
- **S2 and S3b** give 29.33;
- **S1, the leftover-budget count,** gives about **1720,** which is 59 times too much. **Ruled out.**
- **S3a** gives no lengthening at all. **Ruled out.**

## What that means (C76)

- **Allen's duality is right in shape: budget, motion and ticking form a right triangle.** A straight subtraction (S1) is wrong.
- **The counts that work, S2 and S3b, are special relativity's spacetime interval written as hop counts.** We knew which counts would work before writing them down. So choosing one now would be fitting, whatever its label.
- **The pairing count (S2) has a relational reading:** a body's own time squared counts how its right hops relate to its left hops. That's suggestive for an ED whose space is the pattern of relations (D11). **But it was found knowing the answer.** At most it earns "consistent, not derived".
- **Light and mass fit neatly:** no turning means no ticks means uncommitted (R4-Q2); turning is mass.

**Holes:**
- **One dimension only.** In three dimensions a hop has many directions, and a fixed grid picks out preferred directions and a rest frame (A1 C48). Discrete quantum walks recover special relativity only approximately, bent at the smallest scales (Bisio, D'Ariano, Perinotti).
- **R4's first purpose is untouched:** whether gravity pulls on its own energy (A3 C44). This note is only about the speed part of the motion rule.

## Meaning question (Allen decides)

| | question | options | proposed default |
|---|---|---|---|
| **R4-Q3** | Which count is a body's own ticks? | **(a)** leftover budget (S1): ruled out by muons; **(b)** pairings of right and left hops (S2); **(c)** turns, with Doppler-stretched legs (S3b) | **(b), labelled "consistent, not derived".** It's the simplest count that agrees with experiment, needing no extra rule about legs. It was picked knowing the answer, and it is the interval in counting form |

## Draft exit rule (Allen to confirm)

**For the speed part on paper:**
- If Allen's chosen count **conflicts with time-dilation experiments** (S1, S3a), that reading **closes**.
- If it **agrees** (S2, S3b), record **"consistent, not derived"**, since the count is the interval in hop form and was chosen knowing the result.
- It would count as **"a reason from ED's meanings"** only if a meaning fixed *before* this note picked the count. None does; D28 as worded reads most naturally as S1.

**For any later three-dimensional model:** the grid, the hop rule, the tick count and the expected results are written down before the first run. **The preferred-direction problem** (A1 C48) is stated as a test in advance.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide R4-Q3** and confirm the exit rule; record the speed part's verdict | Closes the speed part honestly |
| **(b)** | **Then R4 part 2, gravity's self-feedback:** does the one rule, with the on/off height part, make gravity pull on its own energy? | R4's original purpose; the only gravity idea with the right sign |
| **(c)** | **Back to R5:** hole H1 (the dimension where particles live) | E-C's most pointed hole |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C74 | Feynman checkerboard: amplitude (iεm)^R for R reversals gives the 1+1 Dirac propagator (Wikipedia "Feynman checkerboard"; arXiv:2010.05088; A1 C295); Penrose's zigzag electron, *The Road to Reality* ch. 25, as described in arXiv:1107.4909 and HandWiki "Zitterbewegung"; the Feynman chessboard in 3+1 dimensions (*Frontiers in Physics*, 2023); Bisio, D'Ariano, Perinotti, "Special relativity in a discrete quantum universe", *Phys. Rev. A* 94, 042120 (2016), and "Quantum walks, deformed relativity and Hopf algebra symmetries", arXiv:1601.04592; Bailey et al., "Measurements of relativistic time dilatation for positive and negative muons in a circular orbit", *Nature* 268, 301 (1977) | Search listings, abstracts |
| C75 | `checks/zigzag_clock_check.py`, run 1 (`checks/zigzag_clock_check_run1.txt`): Z1–Z5 as expected | Computed |

**Update (D29):** Allen chose R4-Q3 = pairings and confirmed the exit rule. **Speed part verdict: consistent, not derived** (C78); the leftover-budget and shifted-leg readings are closed.

**Update (RD18):** R4 part 2, gravity's self-feedback, is in [R4_Part2_Self_Feedback.md](R4_Part2_Self_Feedback.md) (note 14).
