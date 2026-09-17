# Road R4, part 2: gravity's self-feedback (on paper)

*ED_Attempt_04, note 14. 2026-09-15 (RD18, D29). Ledger: C79–C82. Literature, reasoning, and one arithmetic check (`checks/conservation_weights_check.py`, expected results written first). **Meaning questions R4-Q4 to R4-Q6 and the draft exit rule are for Allen.***

## Where it starts

**The response side is done:**
- **A body commits as much as it can along its path** (R4-Q1).
- **The height part** has an on/off reading (A3 C38).
- **The speed part** uses pairings: consistent, not derived (C78).

**The sourcing side is what's missing.** General relativity needs a source to count its parts with these weights (C3):

| part | needed | plain counting gives |
|---|---|---|
| Motion | 2 | ½ |
| Gravity's own energy | 2 | −½ |
| Internal energy | 1 | 1 |
| Pressure | 3 | 0 |

**What already failed:**
- **On/off exclusion only subtracts,** so it moves the Moon test the wrong way (A3 C42–C44).
- **Commitments can restate the matter weights but not derive them,** and can't carry gravity's own energy under D2 and D4 (R1, C7).
- **Allen's "loci want to be on" (D7) had the right sign,** but any rule written now would be written knowing the target.

## The fact that changes the question (C79, C80)

**The standard framework for testing gravity** (the parametrized post-Newtonian, or PPN, framework; Will) describes any metric theory with ten numbers:
- **γ and β:** how much mass curves space, and how nonlinear gravity is;
- **α1, α2, α3 and ξ:** whether there's a preferred frame or location;
- **ζ1–ζ4, and α3 again:** whether **total momentum is conserved,** that is, whether action equals reaction.

**In any theory that conserves total momentum and angular momentum, every ζ and α3 is zero.**

**A source's weights are built from those numbers:**

| part | weight |
|---|---|
| Motion | (2γ + 2 + α3 + ζ1) / 2 |
| Gravity's own energy | 3γ − 2β + 1 + ζ2 |
| Internal energy | 1 + ζ3 |
| Pressure | 3γ + 3ζ4 |

**The Moon test:** η = 4β − γ − 3 − (10/3)ξ − α1 + (2/3)α2 − (2/3)ζ1 − (1/3)ζ2.

**The check** (K1–K4) confirms the arithmetic:
- **K1:** with **γ = 1, β = 1, no preferred frame, and action equal to reaction,** the weights are **exactly 2, 2, 1, 3,** and the Moon number is **exactly 0.**
- **K2:** plain counting reproduces attempt 3's numbers (17/6 and 10/3), so the bookkeeping matches.
- **K3:** the Moon test alone only fixes one combination, 2ζ1 + ζ2. **Conservation fixes each weight separately.**
- **K4:** β off by one part in 10,000 moves the Moon number to 4 × 10⁻⁴, about the current bound.

**So gravity's self-feedback isn't a separate mechanism waiting to be found.** Once light bending (γ = 1) and Mercury (β = 1) come out right, **the feedback weights are exactly what action = reaction requires.**

**Where γ and β come from in ED:**
- **Both were attempt 1's matched rules:** clocks slow by e^(−Φ) and motion by its square, which gives γ = 1.
- **Attempt 3's on/off picture made them consequences in form:** β = 1 when influence spreads unslowed (A3 C38, C42 case F0).

## ED's version: does a relation push back? (C81)

**The question:**
- **In ED, gravity's influence between two bodies is a relation,** and space is the pattern of relations (D11).
- **A relation is between two.** So: is influence **mutual**? Does a body that is moved by influence also send it, with what it sends equal to what it responds with?

**If yes:**
- **every ζ and α3 is zero** by meaning, with **no free parameters**;
- **with γ = β = 1 already on record,** the weights 2, 2, 1, 3 and the Moon number 0 follow.

**ED already balances motion in one place.** In attempt 2, meetings passed motion into committed matter, and momentum balance pinned the feedback strength at exactly 1 (A2 C69).

**Experiment backs action = reaction very tightly:**
- **Active and passive gravitational mass are equal** to 4 × 10⁻¹⁴ (lunar laser ranging, 2023).
- **Earlier:** Kreuzer (1968) and Bartlett–Van Buren (1986).
- **Conservation numbers:** ζ2 < 4 × 10⁻⁵, α3 < 4 × 10⁻²⁰.

**The census:** one meaning, zero free parameters, fixing five numbers at once (ζ1–ζ4, α3). **There are no knobs to fit.** The risk is in *choosing* it, because we know general relativity has it.

## What it costs (pokes)

| | poke | what it means |
|---|---|---|
| **P1** | **Influence must carry motion and energy.** For action = reaction to include gravity's own energy, influence has to carry momentum that can be counted | R1 said influence carries no commitments (D2, D4). Carrying motion is neither commitment nor presence, so **D2 stands, but it's a new property:** R4-Q5 |
| **P2** | **Light must send influence.** Light responds (it bends), and it's uncommitted (R4-Q2). Action = reaction says it also sends | **Consistent with physics:** radiation gravitates, about twice its energy (Tolman, C4). But **"mass is what a body sends out" (D3)** has to include uncommitted pattern: R4-Q6 |
| **P3** | **Preferred frame.** Conservation doesn't set α1, α2 or ξ. A fixed grid picks out a rest frame (A1 C48) | Bounds: α1 < 3.4 × 10⁻⁵, α2 < 1.6 × 10⁻⁹. **The main open gravity hole,** the same one as the speed part's in three dimensions |
| **P4** | **First post-Newtonian order only** | The strong field is already closed (attempt 3's exponential metric conflicts with horizons) |
| **P5** | **It's general relativity's known structure.** Coupling universally to all energy, gravity's own included, and requiring consistency, gives GR (Feynman; Deser 1970) | **Whether that route is unique is disputed** (Padmanabhan 2008; Linnemann, Smeenk and Baker). Either way it earns **"consistent, not derived"**, unless "influence is mutual" is ED's meaning on its own grounds |
| **P6** | **Allen's sync idea isn't what supplies the weights.** It supplied the response rule. The additive sign comes from action = reaction, not from cooperation | Honest: D7's route isn't needed here, and no cooperative rule's weights are computed |
| **P7** | **The old ED repo made participation one-sided at decoupling surfaces** (horizons), where mutuality fails | That's strong field, already closed; noted, not reopened |

## Meaning questions (Allen decides)

| | question | proposed default (least structure) | why |
|---|---|---|---|
| **R4-Q4** | **Is influence mutual?** Does action equal reaction, with total motion conserved across bodies and influence? | **Yes** | A relation is between two (D4, D11). ED's meetings already balance motion (A2 C69). Experiment checks it to 4 × 10⁻¹⁴ |
| **R4-Q5** | **Does influence carry motion and energy,** without being presence or commitment? | **Yes** | Needed for R4-Q4 to cover gravity's own energy. Keeps D2 (influence is never presence) and C7 (no commitments in influence) |
| **R4-Q6** | **Does uncommitted pattern (light) send influence?** | **Yes,** by R4-Q4: what responds also sends | Radiation gravitates. D3's "what a body sends out" is read to include pattern |

## Draft exit rule (Allen to confirm)

- **If the answers fix every conservation number at zero** (with γ = β = 1 already on record): record **weights 2, 2, 1, 3 and Moon number 0** as **"consistent, not derived"**. That is general relativity's conservative structure, and "influence is mutual" is new with this note.
- **If a conservation number is left open,** or the preferred-frame numbers can't be kept at zero: record which, and the bound it faces. **That part stays open.**
- **If influence is not mutual:** the ζ's are free, and the Moon test fails unless they're tuned. **R4 part 2 closes as "self-feedback added by hand",** as in attempts 1 and 3.
- **No cooperative rule's weights are computed.** That route isn't needed, and computing it now would be fitting.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide R4-Q4–R4-Q6** and confirm the exit rule; record part 2's verdict | Closes the self-feedback question |
| **(b)** | **The preferred-frame hole on paper:** can a discrete pattern of relations avoid a rest frame (α1, α2, and the speed part in three dimensions)? | Now the one open gravity question; it ties together A1 C48, note 13's hole and P3 |
| **(c)** | **Consolidate attempt 4's write-up** | Ten parts and growing |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C79 | Will, "The Confrontation between General Relativity and Experiment", *Living Rev. Relativ.* 17, 4 (2014), arXiv:1403.7377 (listing); ζ's and α3 measure violation of total-momentum conservation and vanish in fully conservative theories, with bounds (arXiv:1307.8144, arXiv:2402.13951, arXiv:2006.09652, listings); the Nordtvedt formula (arXiv:gr-qc/0103036, listing); LLR η bound about 4 × 10⁻⁴ (arXiv:1702.02795); active = passive mass: Kreuzer (1968), Bartlett and Van Buren, *Phys. Rev. Lett.* 57, 21 (1986), and lunar laser ranging to 3.9 × 10⁻¹⁴, *Phys. Rev. Lett.* 131, 021401 (2023), arXiv:2212.09407; Deser, "Self-interaction and gauge invariance", *Gen. Rel. Grav.* 1, 9 (1970); Feynman, *Lectures on Gravitation* (as described in arXiv:2102.11220); Padmanabhan, "From gravitons to gravity: myths and reality", arXiv:gr-qc/0409089; Linnemann, Smeenk, Baker, "GR as a classical spin-2 theory?" (PhilSci archive) | Abstracts and listings |
| C80 | `checks/conservation_weights_check.py`, run 1 | Computed |
| — | A2 C69; A3 C38, C42–C44; A4 C3, C4, C7, C78 | This and earlier ledgers |

**Update (D30):** Allen accepted R4-Q4–R4-Q6 and confirmed the exit rule. **Verdict: weights 2, 2, 1, 3 and Moon number 0, consistent, not derived** (C83). The preferred-frame numbers stay open.

**Update (RD19):** the preferred-frame numbers left open here are taken up in [Preferred_Frame_Hole.md](Preferred_Frame_Hole.md) (note 15).
