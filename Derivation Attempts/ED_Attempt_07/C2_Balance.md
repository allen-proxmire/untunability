# Road C2, part 1: the balance (on paper)

*ED_Attempt_07, note 5. 2026-09-16 (RD6). Ledger: C9–C12. Literature, reasoning and arithmetic; nothing computed. **Meaning questions C2-Q1–C2-Q4 and the draft exit rule are for Allen.***

## The question

**In C1, each event's offspring averaged exactly 1,** so space neither grew nor shrank on average. That was **put in**, the way CDT tunes a number. **What, in ED, keeps space at that balance?**

## What's known (C9)

| | what it says | source |
|---|---|---|
| **In CDT, the balance is the cosmological constant** | In 2D there is one coupling, the cosmological constant. Tuning it to its critical value (ln 2) gives the infinite-volume limit, and that's where smooth geometry lives | Ambjørn and Loll, *Nucl. Phys. B* 536, 407 (1998); CDT reviews |
| **Too many offspring: hyperbolic** | Causal maps built from **supercritical** trees are hyperbolic: exponential volume growth, a random walk that escapes at positive speed. **Not a finite dimension** | Budzinski, *Electron. J. Probab.* 24 (2019), arXiv:1806.10588 |
| **Too few: space dies out** | A subcritical branching process goes extinct | Branching-process theory |
| **Feedback can find the balance** | In a self-organized branching process, the offspring mean rises when things die out and falls when they run away. **The mean is driven to exactly 1** | Zapperi, Lauritsen, Stanley, *PRL* 75, 4071 (1995) |
| **Size-dependent offspring** | If the offspring mean depends on population size and approaches 1 like 1/(size), the population **grows linearly** (size over time settles to a gamma distribution). If it approaches 1 faster than 1/size², it dies out | Klebaner, *Adv. Appl. Probab.* 16, 30 (1984) |

## On paper

### 1. The balance isn't optional (C10)

| offspring average | what space does | geometry |
|---|---|---|
| **Below 1** | Shrinks and dies out | None |
| **Exactly 1** (critical) | Grows slowly (C1: length 1 + 2t) | **Smooth, finite-dimensional** (C1 passed) |
| **Above 1** | Grows exponentially | **Hyperbolic, no finite dimension** |

**So a smooth, finite-dimensional pattern needs the balance.** It isn't a detail; it's a condition. That's why CDT has to tune its cosmological constant.

### 2. The real universe is balanced to about 1 part in 10⁶¹ (C10)

- **Space's volume grows as the universe expands.** In counts, the number of events in a slice grows by a fraction of about **3H** per unit time, where H is the expansion rate.
- **Per Planck tick** (arithmetic, H₀ = 67.4 km/s/Mpc): 3·H₀·t_P ≈ **3.5 × 10⁻⁶¹**. At late times, set by dark energy alone, it's ≈ 2.9 × 10⁻⁶¹.
- **So the universe sits at the balance to about one part in 10⁶¹, and it's slightly above it.** That tiny excess *is* the cosmological expansion, the same role CDT's cosmological constant plays.
- **Honest:** explaining why the excess is 10⁻⁶¹ is the cosmological constant problem. **ED doesn't solve it.** What ED can hope for is a reason the balance sits *near* 1 without tuning, with the tiny excess's value taken from measurement.

### 3. Two known ways to reach the balance without tuning (C11)

| | mechanism | what it gives |
|---|---|---|
| **(a) Feedback** | Offspring rise where space is sparse and fall where it's crowded | The mean self-organizes to 1 (Zapperi et al.) |
| **(b) Size dependence** | The excess per event shrinks as 1/(size): a **fixed total excess per tick shared across the whole slice** | Linear growth, like C1's 1 + 2t, without being conditioned to survive (Klebaner) |

### 4. What ED's meanings offer (C11)

- **ED's budget is already a feedback.** In ED, commitments use up a budget, which is why clocks slow near settled matter. So:
  - **where a slice is crowded,** more commitment has used up more budget, and there are **fewer offspring;**
  - **where it's sparse,** budget is free, and there are **more offspring.**
  - **That's mechanism (a), from an existing meaning**, and it acts **locally**. ED has no global view, so local feedback fits better than (b), which needs to know the whole slice's size.
- **"Clocks want to sync" pulls the same way.** A crowded region's clocks run slow relative to a sparse neighbour's. Evening out rates means evening out crowding.
- **The tiny leftover excess** would be the cosmological expansion, with its value inherited, read as an association with ED's "loci born at a rate" (What_ED_Needs row 23).

### 5. Honest limits (C11)

- **Feedback needs a response strength:** how strongly crowding lowers offspring. That's a knob, counted by the census guard, **but the balance itself would then come out, not be tuned.**
- **In the literature, feedback reaches exact criticality only in certain limits** (for example, slow feedback compared with fast growth). How close ED's version gets needs a model.
- **Getting the average right isn't the same as keeping the geometry smooth.** Feedback could introduce correlations that roughen it. **C1's readings would test that directly.**
- **The 10⁻⁶¹ excess is not explained.**

## What it means (C12)

- **The balance is a condition for smooth geometry,** not a detail (subcritical dies, supercritical is hyperbolic).
- **ED's budget meaning is a natural local feedback toward it,** and the literature shows such feedback can self-organize branching to exactly critical.
- **If a model confirms it,** ED would supply the balance CDT has to tune, leaving the tiny cosmic excess inherited.
- **Consistent, not derived, until modelled.** Inputs unchanged (still 3).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C2-Q1** | **Must ED explain the balance** (offspring averaging 1), not put it in? | **Yes** | Otherwise C2 just reuses C1's input |
| **C2-Q2** | **Does the balance come from commitment's budget:** crowded regions have fewer offspring, sparse regions more? | **Yes, labelled reading** | Commitments use up budget (ED's core idea); it's a local feedback, which the literature shows can self-organize to exactly 1 |
| **C2-Q3** | **Is the feedback local:** each event's offspring set by crowding in its own neighbourhood, not by the whole slice? | **Yes** | ED has no global view; locality |
| **C2-Q4** | **Is the tiny leftover excess read as the cosmological expansion, with its value inherited?** | **Yes, labelled association** | About 3.5 × 10⁻⁶¹ per tick; ED doesn't explain the number |

## Draft exit rule (Allen to confirm)

**Next step: a model C2a on paper, then run.** It's C1 with the fixed average replaced by ED's local budget feedback: each event's offspring chance falls as its neighbourhood gets crowded.

- **It passes if, without tuning the average:**
  - the offspring average settles at 1;
  - slice length grows slowly (not exponentially, not dying);
  - C1's readings still hold (mass dimension in [1.7, 2.3], walk-return dimension ≤ 2.3);
  - **across a range of response strengths.**

  Record: **"The balance self-organizes from ED's budget: consistent, not derived; the response strength is a knob."**
- **If it dies out, runs away, or roughens the geometry across the range:** record "balance put in", and go on to slice dimension (C2 part 2) with the balance as an input.
- **Expected results and exact ranges are fixed in the C2a spec before any code.**
- **Revise and retest is allowed.** Any revision is recorded with its reason.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide C2-Q1–C2-Q4** and confirm the exit rule | Fixes the balance question |
| **(b)** | **Spec C2a on paper:** the exact local feedback rule, response strengths, readings and expected results | Then a quick run, like C1 |
| **(c)** | **Go straight to slice dimension** (C2 part 2), with the balance put in for now | If you'd rather tackle three first |

**Proposal: (a), then (b).** C2a is cheap: it reuses C1's code and readings, and it answers whether ED supplies what CDT tunes.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C9 | Ambjørn and Loll, *Nucl. Phys. B* 536, 407 (1998); critical cosmological constant ln 2 in 2D CDT (Scholarpedia and CDT reviews, arXiv:1004.0352, 1507.04566; listings); Budzinski, "Supercritical causal maps", arXiv:1806.10588 (listing); Zapperi, Lauritsen, Stanley, *PRL* 75, 4071 (1995) (listings); Klebaner, *Adv. Appl. Probab.* 16, 30 (1984) (abstract, Cambridge Core) | 2026-09-16 |
| C10 | Arithmetic: H₀ = 67.4 km/s/Mpc = 2.184 × 10⁻¹⁸ s⁻¹, t_P = 5.391 × 10⁻⁴⁴ s; 3H₀t_P = 3.53 × 10⁻⁶¹; with Ω_Λ = 0.685, 3H_Λt_P = 2.92 × 10⁻⁶¹ | Computed, 2026-09-16 |
| — | A7-ledger C1–C8; What_ED_Needs row 23 | Earlier records |
