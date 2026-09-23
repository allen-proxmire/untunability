# The threshold law

*ED_Attempt_02, note 7. 2026-09-14 (RD12). Ledger: C73 onward. Check: `checks/threshold_law_check.py`. Coin: plain Fourier (working default; results conditional on it, D7).*

**Exit rule, confirmed by Allen before this derivation was written (RD12):** if the derived law holds no hand, with "found" as in RD10 (a hand from at least 4 of the 7 starts), the discrete handedness line is closed as **"hosted, not made"**. **This derivation is written before any run and may not be revised after one.**

## What ED's rebuilt draw says (attempt 1, RD50; v3_draw Spec and code)

- **A meeting** marks a fragment of committed matter. Wherever the system is at the meeting's loci, a fresh fragment turns from unmarked toward marked. It's reversible and never draws by itself.
- **A draw** happens once **R\* = 3** fragments hold near-perfect marks of the same distinction. It fixes only the record: which way the system went.
- **The environment has a state:** the marks stay in the fragments.
- **Motion passes into committed matter** as part of what a meeting at committed matter does (v3_draw Results; version 4).

## Derivation

**Assumptions** (each labelled; none chosen to fit a result):

| | assumption | source |
|---|---|---|
| **T1** | During one step, meetings between a lane's amplitude and the committed matter at a locus happen independently (Poisson), with mean count proportional to their **relative speed**: μ_R = λ(1 − u), μ_L = λ(1 + u), where lanes move ±1 locus per step and u is the committed matter's velocity | Ordinary collision counting; C69 |
| **T2** | Each meeting writes a full, near-perfect mark on a fresh fragment | The rebuilt draw's meeting, at full angle |
| **T3** | The distinction is "the system was in this lane, at this locus, at this step"; marks don't carry over to the next step | One step, one distinction |
| **T4** | Motion passes into committed matter **irreversibly only when the record is fixed.** Before R\* marks, the meeting can still be undone. So the chance per step that a lane's amplitude is caught is the chance of at least R\* = 3 meetings: **p = P₃(μ) = 1 − e^{−μ}(1 + μ + μ²/2)** | The draw's threshold |
| **T5** | Committed matter keeps the momentum passed to it and stays at its locus: momentum P_x gains p_R n_R − p_L n_L each step (the expected Right catch minus Left catch); velocity u_x = clip(P_x / m₀, −1, 1), with rest amount m₀ = 1 | The environment has a state; C69 |
| **T6** | Mean-field populations; λ is set by the base draw probability Γ through P₃(λ) = Γ | As in all earlier checks |

**The derived law:** p_R = P₃(λ(1 − u_x)) and p_L = P₃(λ(1 + u_x)), with u_x from T5.

## What the derivation implies, worked out before running

**1. The threshold does steepen the meeting law.** Near u = 0, the fractional rate difference is κ(λ) times u, where κ(λ) = λ · P₃′(λ) / P₃(λ):
- κ → **3** as λ → 0, when meetings are rare;
- κ = **1.73** at Γ = 0.3;
- κ falls toward 0 when meetings are plentiful.

So R\* = 3 turns into a steepness of at most 3.

**2. But momentum bookkeeping cancels the steepness.** Committed matter stops gaining momentum only when the catches balance: p_R n_R = p_L n_L. So in any settled state, **p_R / p_L = n_L / n_R**. The rate difference equals the lane imbalance, *whatever the meeting law's shape*. The law's steepness only changes how fast u reaches that balance, not where it ends up.

Linearizing near the symmetric state gives du/dt ∝ κ(aχ − 1) u, where aχ is the fixed loop gain of the lane imbalance (C70). κ only scales the speed. Whether the symmetric state is stable depends on aχ alone, exactly as for the plain kinematic candidate (K1, C69–C70), which gave no hand.

**So, before running:** the derived law has the same settled states and the same stability as K1. It is expected to hold no hand at any base strength. The factor-of-3 coincidence (note 6) doesn't survive the derivation: the threshold supplies steepness, and momentum balance throws it away.

## The check

*Expected results written in `checks/threshold_law_check.py` before running.*
- **The derived law:** at Γ = 0.3 and Γ = 0.05, where the threshold is steepest (κ about 2.8), from 7 starts each.
- **"Found"** at either Γ counts for the exit rule.
- **A comparison, not counted for the exit rule:** the same threshold law with u read instantly as the lane imbalance, skipping the momentum balance. That's the version where the steepness would *not* cancel. It shows what the balance removes.

*(Results are added below this line after the run, without changing anything above.)*

---

## Results (C74, C75)

*Run 1, `checks/threshold_law_check_run1.txt`. Nothing above the line was changed.*

| law | base strength 0.3 | base strength 0.05 |
|---|---|---|
| **Derived law** (threshold catches, momentum kept) | **Dead from all 7 starts** (flow below 10⁻¹¹) | **Dead from all 7 starts** |
| Comparison without momentum balance (not counted) | Dead from 6, unsettled from 1 | Rates lock fully one way from all 7 starts, large flows, **but never settle** |

**Verdict under the exit rule: the derived law holds no hand. The discrete handedness line is closed as "hosted, not made".**

**Score:** 5 of 6 expected results held. The miss was my estimate of the threshold's steepness at the low base strength: it's 2.41, not about 2.8.

## What it means

- **The derivation's reasoning held up.** The threshold does make the meeting law steeper. But when committed matter keeps the momentum it receives, the catches have to balance, and that pins the feedback strength below what a hand needs, whatever the law's shape.
- **The comparison shows what the balance removes.** Without it, the same steep law locks the rates one way, though it still doesn't settle into a steady hand.
- **This is itself a structural finding.** In ED's picture, conservation of the motion passed into committed matter sets how strong the feedback can be, and it isn't strong enough.

**What attempt 2 keeps:**
- **Draw probabilities are forced by ED's structure** (note 2).
- **Unexplained inputs cluster** in the relation and boundary classes (note 3).
- **ED's discrete rule needs no standing phase** (note 5).
- **The fair coin is the one three-channel coin that hosts a hand** (note 5).
- **ED's rule can host a chance-chosen hand, but doesn't make one** from its own pieces (notes 6–7).

**No goalpost moving.** Changing the assumptions after this run to rescue the hand isn't allowed (RD12). A different picture of committed matter, for example matter that can move, would have to be a new line with its own exit rule, fixed first.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(k)** | **Plain-language write-up of attempt 2**, with no prediction language | The handedness line has closed; capture what was learned |
| **(m)** | **Back to note 1's question** (the source of specificity) with what attempt 2 learned | The bigger question this attempt started from |
| **(n)** | **A new line on moving committed matter**, only with its own exit rule fixed first | The one assumption that would change the momentum balance; risks reaching |

**Proposal: (k).**

**Update:** the write-up (k) is done ([Attempt_02_Plain_Language.md](Attempt_02_Plain_Language.md)). The moving-matter fork is opened as a new line, not a revision of this one: [Moving_Committed_Matter.md](Moving_Committed_Matter.md) (note 8). That line also ended under its own exit rule (C77).
