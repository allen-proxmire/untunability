# Moving committed matter: a new line

*ED_Attempt_02, note 8. 2026-09-14 (RD14, D10); confirmed 2026-09-15 (RD15). Ledger: C76 onward. Check: `checks/moving_matter_check.py`. **Status: closed under its exit rule (C77): moving matter doesn't make a hand either.** The exit rule was confirmed as drafted and model (ii) chosen; its rules were written in full before any code ran. Coin: plain Fourier (working default; results conditional on it, D7).*

## The question

**In ED, committed matter is made of the same stuff as everything else. If it can move, can ED's own pieces make a hand?**

## Why matter was pinned before

In every model so far, committed matter sits at fixed spots on the ring, every second position. It's a background that the moving stuff bumps into, the way a detector or a crystal is treated as fixed. That was **a simplification carried over from attempt 1**. It was never a claim that ED's matter can't move.

**Allen's instinct is the physical one: of course matter moves** (D10).

## What this line is, and isn't

- **It isn't a rescue of the closed line.** That line's verdict, "hosted, not made" (RD12, C74), stays on the record unchanged.
- **It's a new question with its own assumptions,** stated on their own grounds, and **its own exit rule fixed before anything is built.**
- **Stated openly:** part of the reason to ask now is that the pinned version failed. That's why the exit rule has to come first, and why the line gets one build only.

## What I worked out at design time (C76)

**1. Moving alone doesn't change the balance that capped the feedback.**
- The cap came from **momentum balance**: committed matter keeps the motion passed into it, so a settled state needs catches from the two sides to balance (note 7).
- If matter moves but nothing else changes, consider a steady flow that's the same all around the ring. Each spot's committed matter still holds a constant momentum: what drifts in, drifts out. So the catches still have to balance, and the cap is the same.
- Moving matter could still change **patterns** (matter bunching up), but a patterned state isn't a hand.

**2. What would change the balance is motion coming back out.**
- Right now, what committed matter releases back into the flow comes out evenly, like everything else the fair coin handles.
- If what's released **carries the matter's own motion**, as stuff thrown off a moving object moves with it on average, then two things change:
  - **The balance loosens.** The momentum committed matter receives is partly given back, so catches no longer have to balance exactly. A rough estimate suggests this *weakens* the old route, by about half.
  - **A second route opens.** Released stuff pushes the flow along in the matter's direction, feeding the flow directly.
- **Whether the net effect is stronger or weaker isn't known without a check.** I'm not writing a guess here. Expected results go into the check script before it runs.

**So the fork really has two parts:**
- **Does committed matter move?** In ED, yes.
- **Does what it gives back carry that motion?** That's the part that matters.

## Model options (Allen picks)

Everything from note 7 stays except what's listed, including the relative-speed meetings (T1), the threshold catches (T4), the fair coin, 7 starts and the "found" standard. **None of the options has a feedback strength to tune.**

| | option | what changes | notes |
|---|---|---|---|
| **(i)** | **Moving only** | Committed matter drifts with its own velocity, carrying its amount and momentum along. Released stuff comes out evenly, as before | The smallest change. By point 1 above it keeps the same balance, so it's close to a formality |
| **(ii)** | **Moving, and giving back its motion** *(least-structure default)* | As (i), plus: stuff released from committed matter carries the matter's velocity on average. Stay stays at 1/3, and left and right shift by ±u/2, so the average released velocity equals the matter's velocity u. No new number is chosen | The smallest model where moving *can* matter. Its extra assumption is ordinary kinematics: what's thrown off a moving thing moves with it |
| **(iii)** | **Committed matter as a second ED walker** | Committed matter is its own population, walking by the same coin-and-shift rule and coherent inside its record (as the rebuilt draw allows). Catches move amount from the moving stuff into committed matter, keeping direction | The most faithful to ED, and the most new rules to write: how amount returns, and how catches keep direction. More room for choices that could quietly tune the result |

**My recommendation: (ii).** It's the smallest model where the question has teeth, and its one added assumption has no knob. (i) is nearly settled by reasoning. (iii) is closer to ED but needs more new rules, each a place where choices could creep in.

## Exit rule (drafted here, then confirmed unchanged by Allen before building, RD15)

1. **One build.** The chosen model's rules are written in full before any run and **can't be revised after one.** Code bugs can be fixed with a dated record, rules can't.
2. **Fixed settings:**
   - plain Fourier coin;
   - rings 24 and 36;
   - base draw strength 0.3 and 0.05;
   - 7 starts;
   - rest amount of committed matter 1, with 10 as a check that it doesn't matter.
3. **"Found"** means a hand, steady, the same all around the ring and with winding 1, from **at least 4 of the 7 starts**, at either base strength.
4. **The line ends**, recorded as "moving matter doesn't make a hand either", if:
   - **(a)** the hand isn't found on ring 24; or
   - **(b)** it's found on ring 24 but not on ring 36, meaning it's a small-ring effect.
5. **If found:** the result reads as "made, conditional on the fair coin and this model's stated assumptions". It then goes through the same robustness check as before (RD10) before anything more is said.
6. **No stacking.** If this line ends, no further variant of committed matter is tried unless Allen opens it as a new line with its own rule.

## Confirmed (RD15)

Allen chose to run this line once, with the exit rule above as drafted and model (ii).

## Model (ii): the rules in full, written before building

Everything not listed here is exactly note 7's derived law:
- the fair coin and the coin-and-shift walk;
- threshold catches P₃ with relative-speed meeting counts;
- λ set by the base draw strength Γ;
- mean-field populations.

| | rule |
|---|---|
| **M1: committed matter everywhere** | Every locus x carries a committed amount c_x and a momentum P_x. At the start, c_x = m₀ at the even loci (the old committed spots) and 0 at the odd ones, and P_x = 0. The matter's velocity is u_x = clip(P_x / c_x, −1, 1), or 0 where there is no matter |
| **M2: meetings follow the matter** | At every locus, lane amplitude meets committed matter with mean count proportional to the local amount and the relative speed: μ_R = λ (c_x / m₀)(1 − u_x) and μ_L = λ (c_x / m₀)(1 + u_x). The catch probability is P₃(μ). Where there is no matter, nothing is caught |
| **M3: what's caught is given back, carrying the matter's motion** | Caught amount is released in the same step. A share 1 − \|u_x\| is released exactly as before, into the Internal channel at x. A share \|u_x\| leaves one locus in the matter's direction, into the Right channel at x + 1 if u_x > 0 or the Left channel at x − 1 if u_x < 0. The average velocity of the released stuff is u_x. **At u_x = 0 this is exactly the closed model** |
| **M4: momentum bookkeeping** | Each step, the matter at x gains the momentum it catches and loses the momentum it gives back: ΔP_x = (p_R n_R − p_L n_L) − u_x (p_R n_R + p_L n_L), with n the lane populations at x after the walk |
| **M5: committed matter moves** | After the catches, a share \|u_x\| of the matter at x, with its momentum, moves one locus in its direction, and the rest stays. Amount and momentum travel together |

**Where this differs from the draft's one-line summary.** The draft wrote the release as "stay 1/3, left and right ±u/2". The rule above (M3) gives the same average release velocity u, but it **turns back into the closed model exactly when the matter is still**. That makes carrying motion the only change from note 7, so any difference in results comes from it. This was decided before building.

**What the check does** (settings from the exit rule):
- **Rings:** 24 and 36.
- **Base strengths:** Γ = 0.3 and 0.05.
- **Starts:** 7.
- **Rest amount:** m₀ = 1 for the verdict; m₀ = 10 on ring 24 as a check that it doesn't matter.
- **Harness first:** with carrying and moving switched off, the model has to reproduce note 7's derived law step for step.

## Results (C77, C78)

*Run 1, `checks/moving_matter_check_run1.txt`. Nothing above was changed after the run.*

**Harness first:** with carrying and moving switched off, the model matched note 7's derived law exactly (difference 0).

| setting | base strength 0.3 | base strength 0.05 |
|---|---|---|
| **Ring 24**, rest amount 1 | **Dead from all 7 starts** (flow ≤ 4 × 10⁻⁶) | **Dead from all 7** (flow ≤ 5 × 10⁻⁵) |
| **Ring 36**, rest amount 1 | Dead from all 7 | Dead from all 7 |
| Ring 24, rest amount 10 (check) | Dead from all 7 | Dead from all 7 |

- **The committed matter never picked up a real velocity:** 0.000 on average in every run.
- **It was still slowly evening out** from its starting every-other-spot pattern, nudged by tiny velocities. That's the only thing still changing.

**Verdict under the exit rule: no hand on ring 24. The line ends: moving matter doesn't make a hand either.**

**Score:** all 5 expected results held.

## What it means

- **Letting committed matter move, and give its motion back, doesn't lift the cap.** ED's own feedback stays too weak to start a flow, just as with pinned matter.
- **By the no-stacking clause, the handedness question rests for attempt 2.** No further version of committed matter gets tried unless Allen opens a new line.
- **The overall reading is unchanged** (note 7). Given the fair coin, ED's discrete rule can **host** a chance-chosen hand, but its own pieces don't **make** one.

## Next steps (Allen decides)

| | step |
|---|---|
| **(m)** | **Return to note 1's question**, the source of specificity, with what attempts 1 and 2 learned |
| **(p)** | **Pause and consolidate**, including, if Allen asks, copying attempt 2 into the EDS repo as attempt 1 was |

**Proposal: (m).**
