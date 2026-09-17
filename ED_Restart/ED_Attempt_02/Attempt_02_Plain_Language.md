# Event Density, attempt 2: the plain-language version

*ED_Attempt_02. 2026-09-14; updated 2026-09-15 with note 8. Written for a reader who hasn't followed the work. Every claim points to the ledger (`01_Ledger/`); the notes carry the details. Terms from attempt 1 are defined in [ED_Attempt_01's Definitions](../ED_Attempt_01/06_Write_Up/Definitions.md); new ones are at the end.*

## Where attempt 2 started

**Attempt 1 ended under its own exit rule.** ED could reproduce familiar quantum behaviour. But its version of **handedness**, a flow that picks one direction by chance and keeps it, needed a fixed "twist" in the rule, and three tries couldn't supply one without tuning.

**Attempt 2 began with a bigger question.** ED and many similar ideas keep producing plausible general behaviour. None of them explain the particular numbers of physics: particle masses, force strengths, mixing angles. What's missing?

## Part 1: mapping the hole (notes 1–4)

**The missing piece looks like a source of specificity** (note 1). Theories explain *kinds* of behaviour well; the numbers get measured and plugged in. Whatever would pin those numbers down is probably not more motion rules. It's more like one of these:
- **a symmetry**, the way three-fold symmetry forces 120° angles;
- **a count**, the way a winding must be a whole number;
- **a boundary**, the way where a guitar string is clamped picks its note.

**One item came off the list: ED's probabilities are forced** (note 2; C11). The rule that probability is an amplitude times its conjugate isn't a free choice in ED. Given ED's structure and "no faster-than-light signalling", a known theorem (Gleason's) forces it.

**The unexplained numbers cluster in two places** (note 3; C27). We sorted 42 inputs of physics using Allen's relation–gradient–boundary frame. The unexplained patterns sit mostly in:
- **relations:** how things couple;
- **boundaries:** where the state sits.

**The closest known idea to "one principle, several numbers"** (note 4; C39) is modular flavour symmetry. Its special values come from the state **sitting at a special point of a symmetry**, not from any cost being minimized.

## Part 2: a hand in ED's original rule (note 5)

**The question as asked failed** (C41). No symmetry of ED's three channels fixes the twist at a useful value.

**The detour turned something up** (C42). Attempt 1 had used a simplified continuous-time model. ED's **original** rule is a coin step, then a move, and in that rule **no twist is needed at all**. Attempt 1's missing ingredient came from the simplification.

**With draw rates that follow the local flow, a hand appears** (C43–C64):

| check | what it showed |
|---|---|
| **What the lasting states are** | Only one setting gave a real hand: steady, the same all around the ring, and the same state from every start apart from its direction |
| **Steepness** | The hand holds across a sevenfold range, so it needs "steep enough", not one tuned value |
| **The coin** | It only works with the **fair coin**, where stay, left and right are equally likely each step. The coin attempt 1 used (Grover) never made a hand in 28 runs |
| **The fair-coin family** | Among coins with equally likely outcomes, a hand forms only for a band of phases. The plain Fourier coin sits in the middle, and it's the same coin however the channels are labelled |
| **Robustness** | The hand survives changes in ring size (12 to 36), meeting spacing, draw strength, and the feedback's shape and strength |

**The coin is a working default, not a settled meaning** (D7). Results read "*if* ED's coin is the fair coin, then…". It was chosen after seeing that it works, and that selection effect is stated wherever the hand is reported.

## Part 3: where the feedback comes from (notes 6–7)

**The weak spot.** The feedback, "draw rates follow the local flow", was put in by hand as a test setting (C65). The literature has the same shape: flocking models, where walkers line up with the local motion, also pick a direction by chance. But they build the lining-up in by hand too (C66–C68).

**ED's own pieces supply a feedback** (C69–C72). Meetings pass motion into committed matter, the matter keeps it, and meetings happen more often at higher relative speed. That feedback points the right way, but **it's too weak: a hand needs between 2 and 4 times more**.

**The draw's threshold doesn't close the gap** (C73–C75). ED's rebuilt draw only makes a catch final once 3 marks exist, and that does make the rule steeper, up to 3 times. But committed matter that keeps its momentum forces the catches from both sides to balance. **That balance pins the feedback strength below what a hand needs, however steep the rule is.** This was worked out before running, and the run agreed.

**So the handedness line closed under its exit rule, confirmed before the run, as "hosted, not made".** ED's rule can *host* a chance-chosen hand if you supply the fair coin and extra feedback. Its own pieces don't *make* one.

## What stands, what closed, what's open

**Stands:**
- ED's probabilities are forced, not chosen.
- Unexplained physics clusters in relations and boundaries.
- ED's original rule needs no twist.
- The fair coin is the one three-channel coin that hosts a hand.
- Conserving the motion passed into committed matter caps ED's feedback. That's a structural finding, not a tuning.

**Closed:**
- **The discrete handedness line, with committed matter pinned in place** (RD12).
- **The moving-matter line** (note 8; RD15, C77). Committed matter that moves and gives back its motion doesn't make a hand either. With this, the handedness question rests for attempt 2.

**Open:**
- **Which coin is ED's** (D7).
- **The source of specificity** itself (note 1).

## Honest limits

- **It's a toy:** one dimension and small rings.
- **My written-down expected results held about two times in three.** Writing them down first is what caught the misses.
- **Some numbers are modelling choices, not ED.** The "3 marks" threshold is one of them, so the 3s it produces aren't evidence.
- **Associations are kept as hints, not findings.** Allen's 120°, ψψ\*, "square" and the recurring 3s are logged (D5, D6, D8, D9) and tested only where a test could be written first.

## Words used here

| word | meaning |
|---|---|
| **Hand** | A lasting flow in one direction, with the direction picked by chance and the rule itself symmetric |
| **Winding** | A whole-number count, 0 or 1 here, that the handedness theorem ties to a genuine hand |
| **Coin** | The rule for how stuff at a spot splits among staying, moving left and moving right each step |
| **Fair coin** | A coin where all three outcomes are equally likely every step (the Fourier coin) |
| **Feedback** | Draw rates that change with the local flow, so that a small flow can grow |
| **Committed matter** | Settled stuff that moving stuff meets. In most of these models it sits at fixed spots; note 8 lets it move |
| **Hosted, not made** | The rule allows a hand when an extra ingredient is supplied, but doesn't produce one from its own pieces |
| **Exit rule** | A condition, fixed before a test runs, that says when a line of work ends |
