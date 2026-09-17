# Can the budget fix a free number?

*2026-09-13. Option 1 from the open items. Ledger: C83–C91, decisions G32–G34.*

## Why this matters

Rule version 0 has three numbers chosen by hand:

- **r₀**, the base draw rate;
- **q**, how far used budget spreads;
- **b_min**, how thin a lone pattern gets before it draws.

GRW, the nearest published collapse model, has two. Until ED fixes at least one of its numbers, ED's collapse rule is GRW in different words.

## Result in one table

| number | what it does | verdict | how |
|---|---|---|---|
| **q** | How far a mass's use of the budget reaches | **Can be fixed at exactly 1** | Gravity isn't screened over any distance tested. q = 1 is the only value that needs no fine-tuning. With q = 1 the rule settles only in 3 or more dimensions, and gives 1/r in 3D |
| **r₀** | Base draw rate per part | **No longer needed** | Later decisions took over its job. The clock-tick rate follows from a pattern's amount, with a choice of units |
| **b_min** | How thin before a lone draw | **Not fixed by the budget as it stands** | Candidate: a smallest unit of bandwidth per locus. That turns b_min into one universal number with a testable consequence |

**Net, if all three are adopted: from three free numbers to one** (C90). That's one fewer than GRW. None of it is evidence about nature yet. The one part that could make ED *testably different* is the last row.

---

## 1. q can be fixed at 1 (C87)

**What q does.** Used budget at a locus = mass there + q × the neighbours' average. With q below 1, a mass's effect dies out exponentially beyond a distance of about √(q / 6(1 − q)) steps in 3D. That is a *screened* gravity.

**Gravity isn't observed to be screened.** LIGO's measurement of gravitational waves from GW170104 limits the graviton's mass to 7.7 × 10⁻²³ eV. Read as a screening range, that means gravity reaches unscreened over at least 10¹⁶ metres (C86). For any small step size, q would then have to be 0.99999… with an absurd number of nines. The only value that isn't a finely tuned "almost 1" is **exactly 1**.

**What q = 1 does, checked by computation** (C84, C85, criteria frozen before running):

| space | does the budget around a mass settle? | measured |
|---|---|---|
| 1D | **No:** it keeps growing as space gets bigger | centre value doubles when the box doubles |
| 2D | **No:** it keeps growing, slowly | +0.41, +0.43, +0.43 per doubling |
| 3D | **Yes** | 1.478 → 1.497 → 1.503, approaching the known 1.516 |

This is Pólya's theorem about random walks (1921): a wanderer is certain to come back home in 1D and 2D but not in 3D (C83). And in 3D the settled budget falls off like 1/r, the shape of Newtonian gravity, to within about 5%.

**Honest limits:**
- **Fixed by consistency, not derived.** q is set by consistency with long-range gravity and by avoiding fine-tuning.
- **It rules out 1 and 2 dimensions, not 4 or more.** So it doesn't explain why space is 3D.
- **A 1/r falloff comes from almost anything that spreads in 3D** (Rule 4), so matching it is a requirement met, not evidence.
- **New problem (C91).** In a finite universe with q = 1, the total used budget keeps growing forever: a source and no loss. Something has to balance it. Loci still being born (RD21) is a candidate, not yet worked out.
- **The 1D test ring can't use q = 1,** because it never settles there. Version 0's ring tests used q below 1, which is fine for checking local logic.

## 2. r₀ is no longer needed (C88)

**Its original job** (RD14) was "the chance per step that a part draws". That was defined before two later decisions:

- **RD18:** clock ticks are separate from draws.
- **RD19:** a lone pattern draws when it's spread too thin; other draws come from interaction (D6), and hinged patterns amplify those triggers (RD10).

So nothing is left for a base draw rate to do.

**The clock-tick rate.** It follows from a pattern's amount: mass is concentrated commitment (D7), and a particle's natural clock rate scales with its mass (the Compton clock, C61). The overall scale is a choice of units, which RD15 (only counts and ratios are real) allows: say a pattern holding a full locus's budget ticks once per step.

**Honest limit:** r₀ is removed by bookkeeping and a choice of units. Nothing is predicted by removing it.

## 3. b_min is not fixed, but there is a candidate (C89)

**Why the budget doesn't fix it.** The per-locus budget is an *upper* limit on what a locus can hold. "Too thin" needs a *lower* limit, and nothing in ED so far gives one.

**Candidate (G34): bandwidth comes in a smallest unit, ε.** The substrate is already discrete in space. This would make it discrete in *amount* too. Then:

- **A pattern of total amount a can cover at most a/ε loci** before some locus would hold less than one unit. At that point it has to draw.
- **b_min stops being a number chosen per pattern** and becomes one universal constant, ε.
- **It predicts something checkable: the more amount a pattern has, the more loci it can spread over before a forced draw.**

> **Correction, 2026-09-13.** The comparison below mixes several scales, and is withdrawn until they are separated. See [G34_Unpacked.md](G34_Unpacked.md).

**That trend is the opposite of the published gravity-collapse models.** In Károlyházy's and Diósi's models, heavier objects stay spread out over *shorter* distances (C64). So this is a place where ED could be told apart from them, if it survives experiment:

- **T9:** caesium atoms stayed spread over 54 cm (C65).
- **T10 (new):** light also carries amount (bandwidth), even with no rest mass, and single photons keep their spread-out time-bin patterns coherent over hundreds of kilometres of fibre in quantum key distribution (C92). Low-amount patterns like single photons would have the *tightest* limit under this rule, so light puts a strong upper bound on how big ε can be.

**Where that probably leads.** If ε has to be extremely small to pass T9 and T10, lone patterns essentially never draw by thinness in any experiment, and draws come from interaction. That lands close to ordinary decoherence plus real collapse on interaction. It would be a coherent place for ED to end up, but it needs the numbers checked once units exist.

---

## Decisions for Allen

| # | ID | question | proposal |
|---|---|---|---|
| 1 | **G32** | Fix q = 1? | **Yes.** Long-range gravity leaves no natural alternative. The open problem it creates, total budget growing in a finite universe (C91), is recorded |
| 2 | **G33** | Retire r₀? | **Yes.** Its job was taken over by RD18 and RD19; the clock scale is a units choice |
| 3 | **G34** | Does bandwidth come in a smallest unit ε at a locus? | **Unpacked in [G34_Unpacked.md](G34_Unpacked.md).** Outcomes come in whole units, but that can't set "too thin", so the choice becomes (A) keep the spreading limit with one number, or (D) lone patterns draw only on interaction |

## Sources checked

- LIGO/Virgo, GW170104, *Phys. Rev. Lett.* 118, 221101 (2017): graviton mass bound (C86)
- Pólya (1921) and Watson (1939), via MathWorld's "Pólya's Random Walk Constants" and Zucker, *J. Stat. Phys.* 145, 591 (2011) (C83)
- Boaron et al., "Secure quantum key distribution over 421 km of optical fiber", *Phys. Rev. Lett.* 121, 190502 (2018) (C92)
- Earlier: Károlyházy and Diósi coherence lengths (C64), 54 cm atom interference (C65), Compton clock (C61)
