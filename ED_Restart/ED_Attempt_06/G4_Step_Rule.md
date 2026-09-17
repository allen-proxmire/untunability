# Road G, part 4: the step-by-step rule (on paper)

*ED_Attempt_06, note 7. 2026-09-15 (RD8). Ledger: C33–C39. Literature and reasoning; nothing computed, no simulation. **Meaning questions G-Q11 and G-Q12 and the draft exit rule are for Allen.***

## Where part 3 left it (C33)

**Allen accepted G-Q8–G-Q10** (D7). Recorded:

> **Road G part 3:** rates can match across a pattern only if its least edge count outgrows the √count surplus of its random rates, so only above two dimensions, with no ratio needed for the floor. With commitment favouring the fewest directions and whole-number dimension (A5 D11's Q), three is the fewest. **A reason for three from ED's meanings, consistent, not derived.** Whether ED's rates actually match needs a strength ED doesn't supply; the step-by-step growth rule is still unwritten.

**What_ED_Needs, row 6** (three dimensions), now has a second reason.

## The question

**Write the growth rule itself:** at each step, which moves happen?
- **The moves:** add a locus nearby, or cut and rejoin two relations in pairs, locally.
- **They should favour** the fewest directions while rates can still match.
- **Only counts,** no dimension or ratio put in.

## What's known (C34)

| | what it says | source |
|---|---|---|
| **Local feedback finds the critical point** | A network rewired by a local rule (quiet nodes gain links, active nodes lose them) drives its average connectivity to the **critical value**, the edge between order and disorder | Bornholdt and Rohlf, *PRL* 84, 6114 (2000) |
| **Sync-driven rewiring** | Oscillator networks rewired by local phase differences organize into structures that sync better. Above a link density, **modular small-world** networks form | Papadopoulos et al., *Chaos* 27, 073115 (2017); adaptive-rewiring density study (2025) |
| **Growth ↔ whole-pattern measures** | Step-by-step causal-set growth can be tied to probability measures on completed patterns ("covtree") | Zalel, *CQG* (2020), arXiv:2008.02607 |
| **Collective successes put things in** | Triangulations get 4D from local moves with 4D building blocks and a time slicing. Causal-set actions use dimension-specific coefficients | A4 C58; A6 C21 |
| **Assumption Q's wording** | "Where a smooth description applies, ED's interval is a quadratic form" | A5 C36, D11 |

## On paper

### 1. What a step can see (C35)

- **A step rule sees only counts near where it acts.**
- **Dimension is how counts grow with distance, all the way out.** Two patterns can agree on every count within any fixed radius and still grow differently beyond it. *Firm.*
- **So a local rule can only produce a dimension collectively.** That's settled by running it, not on paper. The known collective successes put building blocks or dimension-specific numbers in (C34).

**There are two ways to write the rule:**

| | form | what it is |
|---|---|---|
| **(a)** | **A score for whole patterns** (a sum of local counts), with steps drawn by score | Static comparison, like an action. Growth can be tied to such measures (covtree) |
| **(b)** | **A process:** relations are added or rewired **where rates fail to match**, and **each relation costs commitment** | Allen's duality (A4 D25, D28) as a process: sync pulls relations in, commitment makes them costly |

### 2. Where the process heads (C36)

**Take form (b), ED's own picture:**
- a patch that can't match rates gets relations added across its edge;
- a relation that isn't needed costs, so it goes (cut and rejoin in pairs).

**On paper, by the part 3 scaling:**
- **Edges grow only until they just beat the √count surplus.** Any more is cost with no gain.
- **So the edge exponent settles just above ½,** and the dimension just above **two**, at the floor, **not three**.
- **A pattern tuned to a floor is a marginal pattern.** It's typically uneven, and nothing makes its dimension a whole number.

**The literature points the same way:**
- **Bornholdt–Rohlf:** local feedback of this kind drives a network to its critical point.
- **Sync-driven rewiring** gives modular small worlds.
- **Neither gives a smooth three-dimensional space.**

**The honest limit:** this is a scaling argument by analogy. Only a model could test it.

### 3. Why part 3's three doesn't carry over (C37)

- **Part 3's three is the fewest *whole-number* dimension.** Whole numbers came from smoothness (G-Q10).
- **Assumption Q is worded "where a smooth description applies."** It tells the interval's form once smoothness holds. It doesn't say when smoothness holds.
- **Road G's aim is to grow that smoothness.** So for road G, three is a **choice among smooth patterns**, not something growth reaches.
- **Form (a) with smoothness built into the score** would put smoothness in.
- **Form (b)** heads to the floor instead (C36).

**Part 3's verdict** ("a reason for three, consistent, not derived") **stands as a selection statement.** It doesn't give a growth rule.

## What it means (C38)

- **Road G reaches attempt 4's bar** (A4 C59), now in a sharper form. ED's meanings give:
  - the moves (C18);
  - a favoured combination (C25);
  - a reason for three among smooth patterns (C31).
- **But the process those meanings suggest heads to the floor,** just above two dimensions.
- **Smoothness (whole-number dimension) isn't produced** by any rule found from ED's meanings.
- **The missing piece is now specific:** what makes the pattern smooth. That's the same thing every programme in A4 C58 either put in or didn't reach.
- **Inputs:** unchanged (still 3 supplied).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **G-Q11** | **Is ED's growth a process:** relations added where rates fail to match, each relation costing commitment? | **Yes** | Time is step by step (A5 D11); the sync–commitment duality (A4 D20, D25, D28) |
| **G-Q12** | **For road G, must smoothness come out of the rule** rather than be assumed? | **Yes** | Road G's aim is to grow the pattern; assuming smoothness would be circular |

## Draft exit rule (Allen to confirm)

- **With both defaults:** record
  > **"Road G: ED's meanings give the moves, a favoured combination and a reason for three among smooth patterns; the step process they suggest (relations added where rates fail to match, each costing commitment) heads, on paper, to the floor just above two dimensions, not to a smooth three; no rule from ED's meanings found here produces smoothness."**
- **Close road G with that wall.**
- **After closing, options:**
  - take stock of attempt 6;
  - a model testing C36's scaling claim (rules, the dimension reading by counting outward plus the ball-cut, sizes, a stopping point and expected results written first), only if Allen wants;
  - literature on what produces smoothness from local rules.
- **If G-Q12 is rejected** (smoothness assumed as a labelled input): record the growth rule as a selection with smoothness put in (census: that input stays). Part 5 then writes form (a)'s score on paper.
- **No simulation.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide G-Q11, G-Q12**, confirm the exit rule, close road G | Settles road G |
| **(b)** | **Take stock of attempt 6** | Both roads end at walls, one with a new reason for three |
| **(c)** | **A model of the sync-plus-cost process** (expected results first) | Tests whether it really heads to the floor |

**Proposal: (a), then (b),** with (c) as an option in the stock-take.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C34 | Bornholdt and Rohlf, *PRL* 84, 6114 (2000), cond-mat/0003215 (abstract listing); Papadopoulos et al., *Chaos* 27, 073115 (2017), PMC5552408 (listing); adaptive rewiring connection-density study (ScienceDirect, 2025) (listing); Zalel, arXiv:2008.02607 (abstract) | 2026-09-15 |
| — | A4-ledger C58, C59, D20, D25, D28; A5-ledger C36, D11; A6 C18, C21, C25, C29–C32 | Earlier ledgers |
