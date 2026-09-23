# Road G, part 1: what a growth rule has to do (on paper)

*ED_Attempt_06, note 4. 2026-09-15 (RD5). Ledger: C16–C19, after road W's verdict (C15). Literature and reasoning; nothing computed, no simulation. **Meaning questions G-Q1–G-Q4 and the draft exit rule are for Allen.***

## Road W, closed (C15)

**Allen accepted W-Q4 and W-Q5 and the exit rule** (D4). Recorded:

> **Road W:** long waves are direction-free on a random pattern (C3). ED's direction-free walk on a random pattern with loops has at least a share 1 − 2/(mean neighbours) of states that never move (C12, C13). The Husain–Louko leak as computed doesn't transfer; in ED it turns on these stuck states and on unevenness (C11).

**Road W is closed with that wall.** "No stored directions" stays, and matter feels the pattern only through the walk.

## The question

**Road G** (note 1): starting from the One Being, which is nothing (A5 D3), with draws as the first difference:
- **what rule adds loci and relations** so that a direction-free, three-dimensional pattern grows **and stays that way**,
- rather than showing 3 only at one chosen moment?

**Attempt 4's bar** (A4 C59): every known programme either
- **puts the dimension in,**
- **reads it at one moment,** or
- **gets something that isn't space-like.**

None grows three dimensions as a resting state with nothing put in. Missing the bar is the expected outcome.

## What's known (C16)

| | what it says | source |
|---|---|---|
| **Earlier survey** | Quantum graphity puts a preferred degree in; triangulations put their building blocks in; generic causal sets are three-layer, not space-like; Rideout–Sorkin percolation isn't space-like; a thinned complete graph shows about 3 only near one moment | A4 C58 |
| **Label-free growth** | Rideout and Sorkin derive the whole family of step-by-step causal-set growth rules from causality plus "discrete general covariance" (nothing depends on labels) | *Phys. Rev. D* 61, 024002 (2000) |
| **Weighting rescues** | A path integral weighted by a gravitational action strongly suppresses the commonest non-space-like causal sets (Kleitman–Rothschild orders), in one phase | Loomis and Carlip, *CQG* 35, 024002 (2018); Carlip et al. (2022) |
| **Loops plus curvature** | Combinatorial quantum gravity: a weighting by graph curvature (Ollivier) drives short loops to condense. Ground states are pieces of negatively curved manifolds, whose large-scale spectral dimension is three | Trugenberger, *JHEP* 09 (2017) 045; *JHEP* 04 (2022) 019 |
| **Needs density** | That graph action matches the smooth one on sufficiently dense random geometric graphs, which are built in a space | Kelly, Trugenberger, Biancalana, *PRD* 105, 124002 (2022) |
| **Growing complexes** | Growing simplicial complexes give chains, manifolds, hyperbolic or scale-free networks; the building-block dimension is put in | Bianconi and Rahmede, *PRE* 93, 032315 (2016); *Sci. Rep.* 7, 41974 (2017) |
| **Random rules branch** | Rules picked at random give tree-like, exponential growth. Polynomial growth needs special (nilpotent) structure, and its degree is then a whole number | Wolfram Physics technical introduction; Gromov (1981); Bass–Guivarc'h |
| **Random attachment is shallow** | Attaching each new point to a random earlier one gives depth about e·log N | Devroye (1987); Pittel (1994) |
| **Random rewiring** | Swapping pairs of links at random drifts to a uniformly random graph with the same neighbour counts. Random regular graphs have diameter about log N and are near-optimal expanders, tree-like up close | Double-edge swap literature (Fosdick et al. 2018); Bollobás and Fernandez de la Vega (1982); Friedman |

## On paper (C17)

### 1. Adding never stretches

- **Adding loci or relations can only add paths.** It never makes any existing distance longer.
- **Firm:** growth that only adds keeps every distance among what's already there the same or shorter.
- **So adding alone can't give expansion,** where distances between existing things grow everywhere at once.
- **Distances grow only when relations end or re-route.** That's what the thinned complete graph does (A4 C58): its radius grows as links are removed.

### 2. Adding at random makes a small world

- **If a new locus links to loci picked at random,** the pattern's depth grows only like log N. Counting outward then gives no finite dimension.
- **To grow three dimensions, a new locus has to join loci already close to each other.**
- **Then it shortens nothing** (a detour through it is never shorter than two hops). **But it doesn't push anything outward either.**
- **With finite neighbours** (D32), adding can only happen where loci still have room.
- **So adding alone grows like a crystal or a coral:** outward from where there's room, with an inside and an edge. Cosmic expansion has no edge.

### 3. Rewiring at random forgets the shape

- **ED already allows cutting and rejoining in pairs** (A5 D10). Cut a–b and c–d, rejoin a–c and b–d: every locus keeps its neighbour count, and distances can grow. **So paired rewiring can expand.**
- **With nothing favoured,** random paired swaps drift to a random graph with the same counts. Those have diameter about log N and no finite dimension.
- **Keeping swaps local slows the drift but doesn't change where it ends,** if local swaps can eventually reach every arrangement. That's why uniformly weighted triangulations crumple or branch (A4 C58).
- **Firm:** a rule that treats all reachable patterns alike ends among typical patterns, and typical patterns aren't space-like.

### 4. So: something must be favoured

- **The known rescues all weight the patterns:** by an action (Loomis and Carlip), or by curvature and short loops (Trugenberger).
- **A growth rule for ED needs one named quantity that growth favours.** This is attempt 4's finding again: "efficiency" needs a named quantity (A4 C67).

## What ED's meanings supply (C18)

| ED meaning | what it gives a growth rule |
|---|---|
| **Time is a strict one-way order** (A5 D11) | Growth is step by step, like Rideout–Sorkin |
| **No stored directions** (road W) | Nothing depends on labels: Rideout–Sorkin's covariance |
| **Commitments can end but stay happened; cut and rejoin in pairs** (A5 D10) | Paired rewiring, which keeps every neighbour count and can expand |
| **The ball's relations are sameness, not commitments** (A4 D24) | Thinning is allowed (attempt 4's route E-A) |
| **Finite neighbours, no infinities** (A4 D32) | Moves stay local; counts are capped |

**What ED lacks: the favoured quantity.** Candidates already among ED's meanings (not decided):

| | candidate | what it would favour | risk |
|---|---|---|---|
| **(i)** | **Clocks want to sync** (A4 D20) | Uniform patterns, every locus alike | How strongly: a strength is a free parameter unless a meaning fixes it |
| **(ii)** | **Commit as much as possible along a path** (A4 D27, C71) | Patterns with the most proper time | Written for bodies in a pattern, not the pattern itself |
| **(iii)** | **What the present can carry** (E-C, A4 C69) | Three dimensions, the only case with many lasting kinds | Selects rather than grows. Kinds are sparse, so how could they weight empty space? |

**The census guard applies:** a favoured quantity counts as a reduction only if it's already an ED meaning and brings no new strength or constant.

**Links to road W:**
- **A three-dimensional pattern needs many loops,** and loops are where the stuck states live (C12).
- **Short loops condensing is exactly what Trugenberger's weighting favours.**
- **A flagged resemblance** (look-elsewhere): particles are loops too (A5 C31).

## What it means (C18)

- **Firm:**
  - adding alone can't expand;
  - random attachment and random rewiring both lose finite dimension;
  - a rule that favours nothing ends among patterns that aren't space-like.
- **ED's existing meanings already allow the needed moves:** step-by-step, label-free, paired and local.
- **ED doesn't yet name what growth favours.** That's road G's missing input, and it's where the bar (A4 C59) sits.
- **Row 23 (expansion):** ED's expansion can't come from adding loci alone. It needs relations to end or re-route in pairs, or sameness relations to thin.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **G-Q1** | **Is distance the count of hops along the pattern's relations?** | **Yes** | Counting outward (A4 D24); the grain is a count (A5 D10) |
| **G-Q2** | **Can growth also end and re-route relations, only in pairs,** besides adding loci? | **Yes** | Adding alone can't expand (§1); pairs are ED's existing rule (A5 D10) |
| **G-Q3** | **Are all moves local:** only among loci a few hops apart? | **Yes** | Finite neighbours (D32); random long links make a small world (§2) |
| **G-Q4** | **What does growth favour?** | **None named yet.** Compare candidates (i)–(iii) on paper first | Naming one before comparing would be choosing without reasons, a fitting risk |

## Draft exit rule (Allen to confirm)

- **With G-Q1–G-Q3 accepted and G-Q4 left open:** record **"road G part 1: adding alone cannot expand; ED's paired, local rewiring can, but with nothing favoured its long-run patterns are the uniform ones, which aren't space-like; a growth rule needs one named favoured quantity from ED's meanings."**
- **Road G part 2** then compares (i)–(iii) on paper:
  - does each favour a resting, direction-free, three-dimensional pattern?
  - does it add a strength or constant (census guard)?
  - is it circular (does it read dimension through what it favours)?
- **A model comes only later,** with the rules, the dimension reading (counting outward plus the ball-cut), sizes, a stopping point and expected results written first.
  - A 3 seen only at one moment is recorded as a moment.
  - A 3 put in is recorded as put in.
- **No simulation at this step.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide G-Q1–G-Q4** and confirm the exit rule | Fixes what the rule may do |
| **(b)** | **Road G part 2:** compare the favoured-quantity candidates on paper | Where the bar sits |
| **(c)** | **Take stock of attempt 6** | Two roads walked; one wall, one missing input |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C16 | Rideout and Sorkin, *PRD* 61, 024002 (2000), gr-qc/9904062; Loomis and Carlip, arXiv:1709.00064; Carlip et al., arXiv:2209.00327; Trugenberger, arXiv:1610.05934 and arXiv:2112.03778 (abstracts); Trugenberger, arXiv:2311.17526 (abstract); Kelly, Trugenberger, Biancalana, arXiv:2102.02356 (abstract); Bianconi and Rahmede, arXiv:1511.04539, arXiv:1607.05710 (listings); Wolfram Physics technical introduction (listing); Gromov's polynomial growth theorem and Bass–Guivarc'h (Kleiner arXiv:0710.4593; listings); Devroye (1987), Pittel (1994) (listings); Fosdick et al., arXiv:1608.00607; Bollobás and Fernandez de la Vega, *Combinatorica* 2 (1982); Friedman's theorem (Bordenave, arXiv:1502.04482) (listings) | As shown, 2026-09-15 |
| — | A4-ledger C58, C59, C67, C69, C71, D20, D24, D27, D32; A5-ledger D3, D10, D11, C31; A6 C3, C11–C14 | Earlier ledgers |
