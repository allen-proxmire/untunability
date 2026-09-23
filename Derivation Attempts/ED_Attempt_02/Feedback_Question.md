# The feedback question

*ED_Attempt_02, note 6. 2026-09-14 (RD11). Ledger: C65–C72. Checks: `checks/feedback_candidates_check.py` (expected results written first), `checks/feedback_strong_diagnostic.py` (follow-up, not pre-registered). Coin: plain Fourier (working default; results conditional on it, D7).*

## The question

Note 5's hand needs **draw rates that follow the local flow**: where stuff is flowing right, right-movers get caught less and left-movers more. That keeps the flow going.

**Where did that come from?** Attempt 1 put it in as a **test setting**: "the rate law, its sign and mean-field form are test settings" (A1-ledger RD46). It was never derived from ED. So the question is whether ED's own picture of draws and meetings supplies it.

## What the literature says (C66–C68)

- **This shape is well known.** In flocking models, each particle lines up with the local average motion, and a one-dimensional crowd picks a direction by chance (Czirók, Barabási and Vicsek, 1999). There are quantum versions too (Takasan, Adachi and Kawaguchi, 2024; Yamagishi, Hatano and Obuse, 2024).
- **But in those models the lining-up is also a rule put in by hand.**
- **One example where it comes from real physics:** light circling a ring both ways (Del Bino et al., 2017). An interaction between the two directions lets one suppress the other, so only one survives.

So having the feedback isn't unusual. **Getting it for free from the underlying physics is the hard part.**

## ED's own candidate (C69)

ED's rebuilt draw supplies three pieces (A1-ledger RD50):
- meetings at committed matter **pass motion into that matter**;
- **the environment has a state**, so committed matter can keep what it receives;
- the draw itself only fixes the record.

Add one ordinary assumption from collision counting: **how often a meeting happens depends on relative speed**. The result:
- committed matter picks up momentum from the flow, so it drifts with the flow;
- right-movers then meet it less often, and left-movers more often;
- that's **feedback of the right sign, with nothing to tune**. It settles where catches from both sides balance, which sets the strength to exactly 1 in the check's units.

My rough estimate before running was that it's about a quarter as strong as a hand needs.

## What the check found (C70, C71)

| feedback | hand? |
|---|---|
| **ED's candidate** (committed matter keeps momentum) | **No, from all 7 starts** |
| Same law at strength 1 (instantaneous form) | No |
| Strength 2 | No |
| Strength 4 | **A lasting flow from 5 of 7 starts** (flow about 0.38–0.43, winding 1), but it ripples instead of sitting still |
| Strength 8 | A lasting flow from 4 of 7 starts; the rest flip back and forth with no net flow |

**Score:** 2 of the 3 expected results that could be tested held; the fourth, that every hand has winding 1, had no hand to test. I expected a steady hand at strength 4 or 8. What formed instead was a rippling one, only visible in the follow-up.

## What it means (C72)

- **ED's own feedback points the right way but is too weak**, by a factor of roughly 3 or 4.
- **So far, ED's rule hosts a hand but doesn't make one.** With the fair coin and a feedback about four times stronger than ED's own pieces give, a chance-chosen hand forms and lasts. But that extra strength is something we added.
- **This is the honest status of the discrete handedness line.** It's more than attempt 1 had, and still short of "ED makes a hand".

**One ED-native amplifier is in view:** the rebuilt draw's **redundancy threshold**. A record counts as fixed once three copies exist (R\* = 3), and a threshold like that responds steeply by construction.

**A warning to keep in front:** "3 copies" sits suspiciously close to "3–4 times too weak". That closeness is **not evidence**. It's exactly the kind of coincidence that look-elsewhere warns about. Any test has to derive the law from the draw's definition first, then run it, with the exit rule fixed before.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(j)** | **Derive a meeting-rate law from the draw's redundancy threshold**, written out before any run, then test it under an exit rule fixed first. Draft exit rule: *if the derived law holds no hand (found as in RD10), close the discrete handedness line as "hosted, not made"* | The one remaining ED-native source of the missing strength |
| **(k)** | **Close the line now as "hosted, not made"** and write up attempt 2 | If (j) looks like reaching |
| **(h)** | **Two dimensions** | Doesn't address the feedback |

**Proposal: (j), with its exit rule confirmed first.**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C65 | ED_Attempt_01 ledger (RD46, RD50) and notes (Feedback_In_Rule.md, v3_draw/Results.md) | Read directly |
| C66 | Czirók, Barabási, Vicsek, "Collective motion of self-propelled particles: kinetic phase transition in one dimension", *Phys. Rev. Lett.* 82, 209 (1999), arXiv:cond-mat/9712154 | Abstract via search listing |
| C67 | Takasan, Adachi, Kawaguchi, "Activity-induced ferromagnetism in one-dimensional quantum many-body systems", *Phys. Rev. Research* 6, 023096 (2024), arXiv:2308.04382; Yamagishi, Hatano, Obuse, "Proposal of a quantum version of active particles via a nonunitary quantum walk", *Sci. Rep.* 14, 28648 (2024), arXiv:2305.15319 | Abstracts via search listings |
| C68 | Del Bino, Silver, Stebbings, Del'Haye, "Symmetry breaking of counter-propagating light in a nonlinear resonator", *Sci. Rep.* 7, 43142 (2017), arXiv:1607.01194 | Abstract via search listing |

**Update:** (j) is done ([Threshold_Law.md](Threshold_Law.md), note 7). The derived law holds no hand, and the discrete handedness line is closed under its exit rule as "hosted, not made".
