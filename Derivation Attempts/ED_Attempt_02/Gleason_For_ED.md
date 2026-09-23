# Gleason for ED: are the draw probabilities forced?

*ED_Attempt_02, note 2. 2026-09-14 (RD2). Ledger: C2, C7–C12. Check: `checks/gleason_check.py`.*

## The question

**The input in question.** In attempt 1, the chance of each draw outcome was simply assumed: the amount in that outcome (the "amount squared", or Born rule). Note 1 listed it as *possibly forced*.

**What Gleason's theorem says (1957).** If states live in a complex space of three or more dimensions, outcomes are subspaces, and the chance of an outcome doesn't depend on which other outcomes it's grouped with (*non-contextuality*), then the Born rule is the **only** consistent probability rule.

**So: does ED meet those conditions?**

## Condition by condition

| Gleason's condition | in ED | from | holds? |
|---|---|---|---|
| **States are vectors in a complex space** | Patterns are complex amplitudes over loci and channels | P09 (phases); A1-ledger rule versions 0–3 | **Yes** |
| **"Amount" is squared length** | Amount adds up over separate channels, and meetings conserve it | P04; A1-ledger RD27 | **Yes.** Check G4: ED's meetings conserve only the squared amount |
| **Three or more dimensions** | A single locus already has 3 channels; shared patterns have many more | A1-ledger RD13 | **Yes** |
| **Outcomes are subspaces** | A draw fixes a record, the set of states consistent with it | A1-ledger RD28, RD50, C291 | **Yes** |
| **Chances add up over mutually exclusive outcomes** | A record's values split the amount into separate parts | P04; A1-ledger C291 | **Yes** |
| **Non-contextuality** | **For shared (entangled) patterns, it's required by no faster-than-light signalling**, one of ED's forced decisions (A1-ledger RD22). **For a single isolated pattern, nothing in ED implies it yet** | A1-ledger RD22 | **Yes** for shared patterns; **assumed** for isolated ones |

## The check (C11)

Alternative "p-rules" give each outcome a chance proportional to (amount)^(p/2); p = 2 is the usual rule. The expected results were written down before running, and all four came out as expected.

| check | what it asks | result |
|---|---|---|
| **G1 grouping** | Does an outcome's chance depend on how it's split into directions? | Only p = 2 is independent (to 10⁻¹⁶). Other rules are off by 3–13% |
| **G2 signalling** | In ED's rebuilt-draw setup, can A change B's chances by how finely A records? | Only p = 2 leaves B untouched (10⁻¹⁶). Other rules shift B by up to 2%: **signalling, which RD22 forbids** |
| **G3 dimension** | Is there a non-Born rule that still adds up? | In 2 dimensions, yes: a "closest direction wins" rule adds up on every basis. In 3 dimensions it breaks on 258 of 1,000 bases. **The dimension condition matters, and ED always meets it** |
| **G4 ED's meetings** | Which amounts do ED's own meetings conserve? | The squared amount exactly; the 1-norm changes by 27% and the 3-norm by 0.2% |

**What the check doesn't show on its own.** It only tests the p-rules. That *every* non-Born rule is excluded is Gleason's theorem, and Busch's extension to imperfect measurements (C7). That's mathematics, not simulation.

## Verdict (C12)

**The draw probabilities move from "assumed" to "forced, given ED's structure".** ED's structure (complex patterns, additive amount conserved by meetings, records as outcomes, no signalling) leaves only the amount-squared rule. One assumption remains: non-contextuality for a single, isolated pattern. Published routes cover it:
- **Masanes, Galley and Müller** derive it from "how you split a system into parts can't change the physics" (C9). Kent disputes their derivation, and they have replied.
- **Zurek's envariance** derives it from symmetries of entangled states (C10), which is close to ED's picture of marks and records.

## What this means for the hole

**Good for tidiness, but it isn't the missing piece.** The probabilities turned out to be a feature of the valley: standard quantum structure that ED shares with everything else, and that almost any consistent substrate would be forced into.

**That's useful to know.** It removes the last "relation"-class input except the standing phase. **The source of specificity isn't in the probabilities.** It has to be in the numbers, counts and directions that note 1 lists as free.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C2 | Gleason (1957); statement in standard references | Search listings |
| C7 | Busch, "Quantum states and generalized observables: a simple proof of Gleason's theorem", *Phys. Rev. Lett.* 91, 120403 (2003), arXiv:quant-ph/9909073 | Abstract via search listing |
| C8 | Aaronson, "Is quantum mechanics an island in theoryspace?", arXiv:quant-ph/0401062 (2004) | Search listing |
| C9 | Masanes, Galley, Müller, "The measurement postulates of quantum mechanics are operationally redundant", *Nat. Commun.* 10, 1361 (2019); Kent's critique and the authors' response in *Quantum* (2025) | Abstract via search listing |
| C10 | Zurek, "Probabilities from entanglement, Born's rule from envariance", *Phys. Rev. A* 71, 052105 (2005) | Abstract via search listing |
