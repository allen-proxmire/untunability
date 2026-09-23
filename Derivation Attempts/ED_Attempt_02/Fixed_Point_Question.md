# The fixed-point question, and what turned up instead

*ED_Attempt_02, note 5. 2026-09-14 (RD5–RD10). Ledger: C40–C64, D5–D7. Robustness: `checks/robustness_check.py`, `checks/robustness_followup_diagnostic.py`. Checks: `checks/fixed_point_check.py`, `checks/fixed_point_diagnostic.py`, `checks/discrete_hand_test.py`, `checks/lasting_states_check.py`, `checks/fourier_negative_diagnostic.py`, `checks/steepness_range_check.py`, `checks/conjugation_check.py`, `checks/fair_coin_family_check.py`, `checks/fair_coin_start_diagnostic.py`, `checks/basin_check.py`, `checks/fair_coin_labels_diagnostic.py`.*

## The question

**What attempt 1 needed.** Its handedness required a phase around the smallest lane loop that is neither 0 nor π, and three attempts to fix that phase by minimizing a cost all failed.

**What note 4 suggested.** Modular flavour models get their special values from a state sitting at a symmetry's fixed point, not from minimizing anything. So: does a symmetry of ED's three-channel structure fix that phase at a useful value, perhaps 120°?

## Answer to the question as asked: no (C41)

- **No symmetry sets the phase.** In the continuous-time rule attempt 1 used, the only operations that act on the loop phase have fixed points at 0 and π. That's the same wall that the costs hit.
- **Coin phases can't set it either.** In continuous time, phases on the lane mixings cancel around the lane loop.

## What turned up instead (C42, C43)

**ED's original rule was discrete-time: a coin step, then a shift** (version 0). That changes things.

**1. No standing phase is needed** (C42). In the coin-and-shift rule, the Right channel really moves right each step. With ED's own Grover coin and draws that carry motion into committed matter:
- the rule has a single resting state;
- that state has no drift when draw rates are equal, as mirror symmetry requires;
- unequal draw rates produce a flow (response 0.23, much larger than the continuous-time rule gave even with a tuned phase);
- the lossy step operator has the theorem's winding (1).

So attempt 1's "missing standing phase" came from its continuous-time stand-in, whose lanes don't really point anywhere.

**2. A lasting hand, chosen by chance** (C43). With draw rates that follow the local flow, which has one labelled tuned steepness:

| coin | result |
|---|---|
| **Fourier (120°)**, feedback +0.9 | **All 10 runs held the same strong flow (0.243), direction chosen by chance (4 one way, 6 the other), winding 1 in all 10.** The cleanest hand so far |
| Fourier, feedback −0.9 | Weaker lasting flows (0.010–0.025), winding 1 in 8 of 10 |
| Grover (ED's original), feedback −0.9 | Lasting flows (0.017–0.054), direction by chance, winding in only 2 of 10; uneven sizes, possibly not settled |
| Grover, feedback +0.9 | All died |
| Control (too gentle) | All died |

*The lasting-states check below revises this table: only the first row is a steady, uniform hand.*

**Score:** 3 of 6 expected results held. The misses came from my reasoning: I took the amplifying sign from the overall response, but the feedback reads the local flow. I also expected the other sign to die, which it didn't for the Fourier coin.

## What it means (C44)

**The ingredient list for ED's hand gets shorter.** In ED's discrete rule, a lasting, chance-chosen hand needs only:
1. **meetings that carry motion into committed matter;**
2. **draw rates that respond to the local flow** steeply enough (one tuned steepness).

**No standing phase is needed.** The ingredient that three attempts couldn't supply turns out to be unnecessary in ED's original form.

**Your 120° shows up here** (D5). With the Fourier coin, whose defining phases are 120°, the hand is clean and saturated, with the theorem's winding in every run. With the real Grover coin it's weaker and mostly without winding. It's a hint worth following, not a result: it rests on one steepness setting, and look-elsewhere still applies.

## What the lasting states are (C45–C47, RD6)

*Checks: `checks/lasting_states_check.py` (expected results written first), `checks/fourier_negative_diagnostic.py` (follow-up, not pre-registered).*

| setting | settled? | pattern | same state every run? | verdict |
|---|---|---|---|---|
| **Fourier, feedback +0.9** | **Yes, completely** | **Uniform:** same flow and amounts everywhere | **Yes:** one state and its mirror image (agree to 5 × 10⁻¹⁴) | **A real chance-chosen hand** |
| Fourier, feedback −0.9 | No: swings every ~2.8 steps | Uniform amounts, flow alternating spot to spot | Yes | **No hand:** averages to zero flow |
| Grover, feedback −0.9 | Yes | **Patchy:** amounts vary a lot, flow reverses 14–20 times around the ring | No: each run is different | **No uniform hand:** a patchwork of domains |
| Grover, feedback +0.9 | Still fading at 6,000 steps | Uniform | Yes | **Dies** |

**Score:** 2 of 4 expected results held.
- **Grover, feedback −0.9 missed:** I expected it not to settle; it settles, but patchily.
- **Grover, feedback +0.9 missed:** my bar for "settled" was too strict for a slow fade. That's a criterion error.

**What changes.**
- **Only one setting carries a hand:** the Fourier coin with feedback +0.9. The ingredient list above holds for that coin only.
- **ED's Grover coin gives no uniform hand** at this steepness.
- **C43's other "lasting flows" are downgraded.** Fourier with −0.9 was a snapshot of a swing; Grover with −0.9 is a patchwork.

## Across steepness (C52, RD7)

*Check: `checks/steepness_range_check.py` (expected results written first). Loop gains 1.5, 2, 3, 5, 10; six starts each.*

| setting | gain 1.5 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|
| **Fourier, feedback +0.9** | **hand** (0.2237) | **hand** (0.2392) | **hand** (0.2427) | **hand** (0.2429) | **hand** (0.2429) |
| Grover, feedback +0.9 | dies | dies | dies | wobbles (5 of 6) | wobbles (5 of 6) |
| Grover, feedback −0.9 | patchy | patchy | patchy | patchy | patchy |

- **The Fourier hand holds at every steepness.** Every run gives one state and its mirror image, with the theorem's winding, and the flow levels off at about 0.243. So the "one tuned steepness" becomes "steep enough".
- **The Grover coin never forms a hand from the starts tried.** It dies, wobbles, or breaks into patches. Only near-uniform starts were tried; see the fair-coin section for why that matters.
- **Score:** 2 of 3 expected results held. I expected Grover with +0.9 to stay dead; at steep settings it wobbles instead.

**What this means: the coin choice decides whether ED's discrete rule can hold a hand at all.**

## Conjugation and the mirror (D6, C48–C51)

**Allen's association:** the draw pairs ψ with ψ*, "its mirror image". Does that tie to the mirror symmetry?

**Allen's clarification:** the probability is ψ times its conjugate. For one amplitude, ψψ* = |ψ|², a real number with the phase removed. That's why ψ² would be wrong for complex ψ: squaring doubles the phase instead of removing it. In the checks, the state is kept as ρ = ψψ†, "ψ times its mirror", and probabilities are its diagonal, so this pairing is already built in. **What it implies:** replacing ψ by ψ* leaves every probability of that state unchanged. The two can only be told apart by how they evolve, which is set by the rule's complex phases (the coin).

*Check: `checks/conjugation_check.py` (expected results written first; all 5 held).*

- **For the Fourier coin, conjugation is the Left–Right swap.** Taking ψ* of the coin gives the same coin with Left and Right exchanged, exactly. The Grover coin is real, so conjugating it does nothing.
- **But the two hands are space mirrors of each other, not conjugates.** They match as mirror images to 6 × 10⁻¹⁵ and differ as conjugates by about 10⁻².
- **Standard physics agrees these are different mirrors.**
  - ψ → ψ* is the heart of *time* reversal (Wigner 1932), not space reflection.
  - A rule can tell a process from its time-reversed version only if it has complex phases. Kobayashi and Maskawa showed that such a phase in quark mixing needs at least three generations.
  - Complex hopping phases bias quantum-walk transport in one direction (Zimborás et al. 2013).
- **One more fact makes the Fourier coin special** (C53). A three-channel coin whose outcomes are all equally likely is, up to relabelling and phases, *only* the Fourier coin (Haagerup's classification), and no such coin is real. So "fair", "complex" and "120°" come together in three channels.

## The coin decision, laid out (C54)

| | Grover (V0-D1 default) | Fourier |
|---|---|---|
| **What it treats alike** | The **channels:** unchanged by any relabelling of Internal, Left, Right | The **outcomes:** each is equally likely (1/3) |
| **Outcome odds per step** | Stay 1/9, turn 4/9 each way | 1/3 each |
| **Real or complex** | Real | Necessarily complex; its conjugate is the mirror swap |
| **Unique?** | The standard channel-symmetric choice | The only fair three-channel coin, up to relabelling and phases |
| **Holds a hand?** | Never: no hand from any of 7 kinds of start, at matched gains, either sign (C58) | Always: from all 7 kinds of start at both gains (C58) |
| **Needs a phase chosen?** | No | No: the plain coin is the same under every channel relabelling (C59); a band of extra phases (0°–60°) also works robustly |

**Open caution.** "Up to phases" hides a question. The phase-dressed versions of the Fourier coin are equivalent as matrices, but they need not act alike in a coin-and-shift walk. So it isn't yet known whether *fairness alone* gives the hand, or whether the specific 120° phases matter.

**Also untouched:** ring size, meeting spacing, draw strength and feedback amplitude. Look-elsewhere still applies.

## The fair-coin family (C55–C57, RD8)

*Checks: `checks/fair_coin_family_check.py` (expected results written first), `checks/fair_coin_start_diagnostic.py` (follow-up, not pre-registered).*

**Every fair coin is one of a one-dial family** (confirmed on 200 random ones). It's the Fourier coin with an extra phase φ on the two moving channels, or its conjugate. The conjugate turns out to be the same thing started differently (see below). The same phase goes on Left and Right, which keeps the rule mirror-symmetric.

**Which phases hold a hand** (feedback +0.9; feedback −0.9 never did):

| φ | 300° | 330° | **0° (plain Fourier)** | 30° | 60° | 90° | 120° | 150° | 180° | 210° | 240° | 270° |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| near-uniform starts | hand | hand | **hand** | hand | hand | hand | 2 of 3 | dies | dies | dies | wobbles | wobbles |
| staggered starts | | | **hand** | | | | | **hand** | | | wobbles | dies/wobbles |

*A blank cell means not tried.*

**What held, what didn't.** 3 of 4 expected results held.
- **The miss taught something.** I expected the conjugate coins to match their partners. They match exactly as rules, but my check forgot that the matching also turns a near-uniform start into a staggered one.
- **The follow-up confirmed this.** The coin at 150° dies from near-uniform starts but **holds a steady hand from staggered starts**.
- **The same rule can die from one start and hand from another.**

**What it means.**
- **A band, not a point.** Hands appear across a wide band of phases, from 300° through 150°. The plain Fourier coin sits in the middle of that band, not at an edge.
- **"Fairness alone" isn't settled.** No hand has been found at 240° or 270°, but the starts tried were few.
- **"Grover never holds a hand" isn't settled either.** Every Grover run so far used near-uniform starts only.
- **Steepness differed by coin.** The common steepness gave the coins different effective gains (1.6 to 3.1). The coins that died had the lower gains.

## The basin check (C58–C60, RD9)

*Checks: `checks/basin_check.py` (expected results written first), `checks/fair_coin_labels_diagnostic.py` (follow-up, not pre-registered).*

Each coin's steepness was set to the same effective gain (3 and 10). Seven kinds of start were tried: near-uniform, staggered, two other wave patterns, two fully random and one random mixed.

**Hands out of 7 starts** (feedback +0.9):

| coin | gain 3 | gain 10 |
|---|---|---|
| **φ = 0° (plain Fourier)** | **7** | **7** |
| 30° | 7 | 7 |
| 60° | 7 | 7 |
| 90° | 7 | 6 |
| 120° | 6 | 5 |
| 150° | 2 | 1 |
| 180°, 210°, 240° | 0 | 0 |
| 270° | 0 | 1 |
| 300° | 6 | 3 |
| 330° | 7 | 4 |
| **Grover (either sign)** | **0** | **0** |

- **Feedback −0.9 gave no hands** for any coin.
- **Every hand has winding 1.** For a given coin and gain, every hand is the same state or its mirror image.
- **Score:** 3 of 4 expected results held. I expected a hand somewhere at 180° and 210° (none was found) and none at 270° (one was).

**What it settles.**
- **Fairness alone is not enough.** Fair coins hold a hand only within a band of phases. The core runs from 0° to 60° (every start, both gains). Nothing was found from 180° to 240°.
- **The plain Fourier coin needs no dial.** Relabelling its channels in all 36 possible ways always gives φ = 0 (C59). So "a fair coin with no extra phase" is one definite coin, whatever the channels are called, and it sits inside the robust core.
- **The Grover coin found no hand anywhere:** 28 runs across 7 kinds of start, 2 gains and both signs. The start-dependence that rescued the 150° coin doesn't rescue Grover.

**So the coin decision is now concrete** (C60):
- **Grover:** ED's discrete rule has shown no hand in these settings.
- **Plain Fourier:** a chance-chosen hand with the theorem's winding, robust across starts and steepness.

**Limits:**
- one ring size, meeting spacing, draw strength, feedback amplitude and feedback form;
- not a proof that Grover can't hold a hand;
- look-elsewhere still applies.

## The coin decision (D7, C61)

**Status: a working default, not a settled meaning.** Allen chose to keep the plain Fourier coin (entries ω^{jk}/√3, ω = e^{2πi/3}) as attempt 2's working default. Every result that uses it reads as conditional: *"if ED's coin is the fair coin, then…"*.

**The meaning stays open.** It's to be decided later, on grounds other than which coin gave a result. Attempt 1 is closed and unchanged.

**Why, on grounds that don't depend on the hand results:**
1. **Grover's symmetry argument doesn't hold up.** Grover is unchanged when you relabel the three channels any way you like. But ED's channels aren't interchangeable: Internal stays put, while Left and Right move. The only symmetry the structure really has is the mirror, and both coins respect it. The Fourier coin is also unchanged under every relabelling, up to phases (C59), so relabelling doesn't separate the two.
2. **The Fourier coin favours no outcome.** From any channel, each outcome has probability 1/3. Grover favours turning (4/9 each way) over staying (1/9). Up to relabelling and phases, Fourier is the only three-channel coin with this property (C53), and the plain one adds no phase. So adopting it adds no parameter.

**The honest caveat: a selection effect.** The Fourier coin was tested partly because of the 120° hint (D5), and it's being adopted *after* it held a hand and Grover didn't. Anywhere the hand is reported, that has to be said.

**Pre-commitments:**
- **The coin is now fixed.** No switching coins in response to robustness results.
- **The Grover results stay on the ledger.**

**Exit rule for the discrete handedness line** (confirmed by Allen before the robustness check ran, RD10):
- **"Found" means** a hand from at least 4 of the 7 starts, at effective gain 3 or 10.
- **The line ends if either:**
  - **(a)** for any one setting, the hand is found **only at its current value** (it's tuned in that setting); or
  - **(b)** the hand is **not found at the largest ring size** tested (it's a small-ring effect).

## The robustness check (C62–C64, RD10)

*Checks: `checks/robustness_check.py` (expected results and exit rule fixed first), `checks/robustness_followup_diagnostic.py` (follow-up, not pre-registered). Coin: plain Fourier (working default; results conditional on it).*

Each setting was varied one at a time, with each setting's own effective gain (3 and 10) and 7 starts.

| setting | values tried | hand found? | flow |
|---|---|---|---|
| **Ring size** | 12, 24, **36** | **All** | 0.2467, 0.2427, **0.2415**: settling, not vanishing |
| **Meeting spacing** | 2, 3 | Both | 0.243, 0.229 |
| **Draw strength** | 0.1, 0.3, 0.5 | All | 0.242, 0.243, 0.238 |
| **Feedback amplitude** | 0.3, 0.6, 0.9 | All | 0.052, 0.117, 0.243 |
| **Feedback shape** | smooth, clipped straight line | Both | 0.243 |

**Verdict under the exit rule you confirmed: the discrete handedness line does not end.**

**Score:** 6 of 8 expected results held.

**Two things turned up:**
- **Draw strength 0.6 was an invalid test value.** With feedback 0.9 it makes a draw probability of 1.14, which is impossible, and the numbers broke. I rechecked at 0.5, the largest valid value: a hand from every start. That was my design error, and it doesn't affect the verdict.
- **Weak feedback gives a flow without the winding.** At amplitudes 0.3 and 0.4 the hand is steady and uniform but has winding 0. From 0.5 up it has the theorem's winding 1. The verdict holds even counting only hands with winding.

**What it means** (C64). If ED's coin is the fair coin, its discrete rule holds a chance-chosen hand that doesn't depend on:
- ring size;
- meeting spacing;
- draw strength;
- feedback shape;
- the exact feedback strength (the winding needs moderate feedback or more).

**What it doesn't cover:**
- **The feedback was put in by hand.** "Draw rates follow the local flow" is not yet derived from ED's own picture of draws and commitment. That's now the largest open weakness.
- **The model is one-dimensional.**
- **The coin was adopted after seeing results.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| ~~(a)~~ | ~~Check what the lasting states are~~ | **Done** |
| ~~(b)~~ | ~~Steepness range~~ | **Done** |
| ~~(d)~~ | ~~Fair-coin family check~~ | **Done, but start-dependent** |
| ~~(d2)~~ | ~~Basin check~~ | **Done** (above) |
| ~~(c)~~ | ~~Decide the coin~~ | **Working default:** plain Fourier coin, results conditional on it; meaning still open (D7; above) |
| ~~(f)~~ | ~~Confirm the exit rule~~ | **Done** (RD10) |
| ~~(e)~~ | ~~Robustness check~~ | **Done:** the line does not end (above) |
| ~~(g)~~ | ~~The feedback question~~ | **Done:** see [Feedback_Question.md](Feedback_Question.md) (note 6) |
| **(h)** | **Two dimensions:** does a hand survive on a 2D lattice? | Moves past a one-dimensional toy; much more compute |
| **(i)** | **Interim write-up** of attempt 2, in plain language, no prediction language | Captures where things stand |

**Update:** (g) is done; the next steps continue in [Feedback_Question.md](Feedback_Question.md).

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C40 | Mackay, Bartlett, Stephenson, Sanders, "Quantum walks in higher dimensions", *J. Phys. A* 35, 2745 (2002): Grover and discrete Fourier transform coins as the natural equal-weighting coins for multi-channel walks | Abstract via search listing |
| C49 | Wigner time reversal as antiunitary (conjugation): Wikipedia, "Antiunitary operator"; Berkeley Physics 221 notes, "Time reversal" | Search listings |
| C50 | Kobayashi–Maskawa: one CP phase needs three generations: CERN Courier, "Event celebrates 50 years of Kobayashi–Maskawa theory"; arXiv:2404.19123 | Search listings |
| C51 | Zimborás et al., "Quantum transport enhancement by time-reversal symmetry breaking", *Sci. Rep.* 3, 2361 (2013), arXiv:1208.4049 | Abstract via search listing |
| C53 | Haagerup's classification: every 3×3 complex Hadamard matrix is equivalent to the Fourier matrix: Tadej and Życzkowski, "A concise guide to complex Hadamard matrices", *Open Syst. Inf. Dyn.* 13, 133 (2006); arXiv:1410.2134 | Search listings |
