# The budget slows spreading: what happened, and what light bending demands

*2026-09-13. Closes V0-L1. Opens G37. Ledger: C192–C198. Code and tests: [Commitment_Rule/v1_budget/](Commitment_Rule/v1_budget/).*

## 1. What was built

**RD16 says the budget slows every process at a place.** Version 0 only slowed clock ticks. Now spreading slows too:
- **Everything at a locus runs at s = 1 − U,** where U is the budget used there.
- **It is built so that nothing is lost:** evolution stays unitary, and it has no left–right preference.
- **Where the budget is uniform,** it is exactly "the same thing, running slower".

## 2. What it does (C193, C194)

**Two effects, which I had wrongly lumped together:**

| effect | what happens | who feels it |
|---|---|---|
| **Lingering** | Spreading is slower near a mass, so a pattern's bandwidth builds up there and its centre drifts toward the mass. It's like light bending toward glass | Every pattern, whatever the sign of its commitment. It dominates for light-like patterns |
| **Pull** | Slowing the rest term (mass as concentrated commitment, D7) acts like a potential well | **Massive-like patterns fall toward the mass,** about 30× more strongly than lingering. **Only if commitment amounts are positive;** negative ones would rise |

**This matches how gravitational time dilation acts on energy in standard physics.** It's a requirement met, not evidence.

**Two of my frozen predictions were wrong** (F2 and F4): my starting pattern turned out to be light-like. Both are recorded.

---

## 3. The problem: light would bend only half as much (C195, C196)

**What's known** (Will's review of gravity tests, C195):
- **Starlight grazing the Sun bends by 1.75 arcseconds.**
- **About half of that comes from gravity's effect on time,** the part a clock feels. Soldner in 1804, and Einstein in 1911, found only that half.
- **The other half comes from gravity's effect on space:** near the Sun, "straight" lines are bent relative to straight lines far away.
- **Physicists write the size of the space part as γ.** General relativity has γ = 1, and the bending is (1 + γ)/2 times the full value.
- **The Cassini spacecraft measured γ − 1 = (2.1 ± 2.3) × 10⁻⁵** (C195). Half-bending (γ = 0) is excluded overwhelmingly.

**What that means for ED** (C196):
- **RD16 slows everything at a place by one factor.** That is a time-only effect, in the same class as the 1911 calculation.
- **So a light-like pattern crossing the Sun would bend by half the measured amount.**
- **RD16, as the whole story of what mass does, is ruled out by measurement.** (This uses the weak-field match U ≈ GM/rc², C104.)

**The standard way to say the full effect** (C197): weak gravity bends light as if space had a refractive index n ≈ 1 + 2GM/(rc²). **The "2" is time plus space.** RD16 alone gives n ≈ 1 + GM/(rc²).

---

## 4. G37: what supplies the space part?

| | option | what it means | verdict |
|---|---|---|---|
| **(a)** | **Crossing between loci pays twice** | At a place, ticking and internal change slow by s (RD16 as is). Moving from locus to locus is slowed by s² | **Matches γ = 1 at this order:** light sees n ≈ 1 + 2U. Slow massive patterns still fall by the rest-term pull, so Newtonian gravity is unchanged. **Cost:** revises RD16's "same rate for every process" into *ticking vs moving*. ED already splits ticking from moving (RD17, the Pythagorean split), so it has a natural place |
| **(b)** | **Mass adds loci or links around it** | More loci along a path near mass, so paths are longer | **Conflicts** with even births (RD29) and your view that committed loci don't create loci (D12) |
| **(c)** | **Keep RD16 as is** | Light bends by half | **Ruled out** by Cassini and by light-bending measurements |

**Proposal: (a).** It is the smallest change that matches the measurement, and it ties gravity to the moving/ticking split ED already has.

**Honest points about (a):**
- **The factor s² is chosen to match γ = 1.** ED doesn't derive it, and a derivation would be real progress. Your Pythagorean split (RD17) and the "why Pythagorean?" question (G26) are the place to look.
- **It only fixes first-order bending.** Higher-order tests, such as Mercury's perihelion (a second PPN parameter), would be the next check once ED has units.
- **It's a requirement, not a prediction.** GR already gets it right.

## Decided (2026-09-14): G37 = (a), RD35

**Ticking and internal change at a locus slow by s. Moving between loci slows by s².**

**Checked** (v1_budget, run 3, C199):
- **Moving slows by exactly s².** So light-like patterns see an effective refractive index of about 1 + 2U, the measured light bending.
- **Massive-like patterns fall as before:** toward the mass with positive commitment, 0.99 times the RD16 result.
- **One frozen prediction (M3) was wrong.** The 1D centre drift of a light-like pattern isn't a good stand-in for bending. That is recorded in [Commitment_Rule/v1_budget/Results.md](Commitment_Rule/v1_budget/Results.md).

---

## 5. The next constraint: Mercury (G38)

**Once light bending is right, the next test is second order: how clocks slow when gravity is a bit stronger.** Physicists call its size β. It shows up in Mercury's perihelion, the slow turning of its orbit (C200):
- **General relativity gives 43 arcseconds per century,** which matches observation.
- **In general,** the advance is (2 + 2γ − β)/3 times that.
- **Messenger data give β − 1 = (−4.1 ± 7.8) × 10⁻⁵.** So β = 1 to about 1 part in 10,000.

**ED's clock rate right now is s = 1 − U** (RD14). The amount of used budget is simply **subtracted** from what's left. Squared, that gives clocks a second-order term with **β = 1/2** (C201):
- **Mercury's orbit would turn 7/6 as fast:** about 50 arcseconds per century instead of 43.
- **That is ruled out by thousands of standard deviations.**

| | option | what it means | verdict |
|---|---|---|---|
| **(a)** | **Rate s = e^(−U):** each extra bit of used budget slows things by the same *share* of what's left, like compound discounting | Clocks get β = 1 at second order. Moving slows by e^(−2U) | **Matches Mercury at this order.** Side effect: the rate never quite reaches zero, so "full budget" becomes a limit rather than a wall |
| **(b)** | **Keep s = 1 − U:** used budget is subtracted | β = 1/2 | **Ruled out** by Mercury's perihelion |
| **(c)** | **Keep the rate linear, but make the budget itself nonlinear** (used budget feeds back on itself) | Could also shift β | More structure, and it would change the q = 1 budget results (C84, C85) |

**Proposal: (a).** Two honest points:
- **Like s², this is chosen to match a measurement, not derived.** But "a share of what's left" is arguably a more natural reading of a budget being used up than "subtract a fixed amount". Your call.
- **After β, the next checks are harder.** One is whether gravitational binding energy itself gravitates (the Nordtvedt effect, tested by lunar laser ranging). ED's budget rule is linear, so this may be a real problem later.

## Decided (2026-09-14): G38 = (a), RD36

**Used budget removes a share of what's left.** The rate is e^(−U) for ticking, and moving pays e^(−2U).

**Checked:**
- **The slowed generator passes every construction check** (C202).
- **Massive-like falling is unchanged in weak fields:** 0.9994 × the RD35 value.
- **A separate check computes β from the rate function** (C203):
  - linear rate: β = 0.5, perihelion 50.14″ per century, about 6,400σ from the measurement;
  - exponential rate: β = 1, perihelion 42.98″, within 1σ.

**On the frozen β check.** Its first run missed a tolerance because of my finite-difference step, not the physics. I fixed the step and recorded the change.

**Where the gravity side stands:** patterns fall, light bends by the measured amount, and Mercury's orbit turns at the measured rate. **All three are matched to measurement, not predicted.**

**Next hurdles:**
- **Does binding energy gravitate?** This is the Nordtvedt effect, tested by lunar laser ranging. ED's budget is linear in mass, so this could fail.
- **Can "moving pays twice" and the exponential rate be derived from the Pythagorean split?** (G26.)

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C195 | Will, "The confrontation between general relativity and experiment", *Living Rev. Relativ.* 17, 4 (2014), arXiv:1403.7377 | Paper text read: the (1+γ)/2 coefficient; the "1/2" from Newtonian and equivalence-principle arguments; the space-curvature γ/2; Cassini |
| C195 | Bertotti, Iess, Tortora, *Nature* 425, 374 (2003) | Search listing, and via Will |
| C197 | Schneider, Ehlers, Falco, *Gravitational Lenses* (Springer, 1992) | Search listings; not read directly |
| C197 | Narayan and Bartelmann, "Lectures on gravitational lensing", arXiv:astro-ph/9606001 | Search listings; not read directly |
