# Event Density, attempt 7: the plain-language version

*ED_Attempt_07. Written 2026-09-16 (RD20); rewritten 2026-09-19 (RD54) after road C closed. For a reader who hasn't followed the work. Every claim points to the ledger (`01_Ledger/`); the notes carry the details. Earlier write-up: [attempt 6](../ED_Attempt_06/Attempt_06_Plain_Language.md). The cross-attempt inputs table is [What_ED_Needs.md](../What_ED_Needs.md).*

## What attempt 7 was for

**Attempt 6 ended at one precise open problem** (A6 C88): grow ED's pattern step by step, with finite neighbours, where space never splits or merges, and have sync and commitment make it three-dimensional.

**Attempt 7 took that on as road C, causal growth.** The habits stayed the same:
- **Allen decides what ED means.** Claude proposes the least-structure default; nothing counts until Allen says so.
- **Expected results come first.** Every model had its expected results and exit rule written down before any code.
- **Revise and retest is normal.** Every miss, revision and correction is in the record, including Claude's own mistakes.

**Working names** (Allen, D15): **Commitment Dynamics** for the framework, **Budgeted Causality** for the balance result, **Synced Now** for the three-dimensions result.

**Verdict labels:** **pass** means a model met results fixed in advance; **consistent, not derived** means ED can say it without contradicting known physics, but something is still put in.

## 1. The causal half: ED's growth matches a known answer (C1)

**The picture:** space at each tick is a slice of events, here given as a circle. Each event links forward to a run of events in the next slice, neighbours sharing exactly one future event, so the slice never splits, merges or reorders. Each event's number of children is random, averaging one.

**That is two-dimensional causal dynamical triangulations (CDT)**, whose answers are known exactly.

**The model:** slice length slope **2.05** against the exact 2, mass dimension **2.17**, walk-return dimension **1.89**, structure exact. **Pass.**

The average of exactly one child was **put in**, the way CDT tunes its cosmological constant. Which raised the next question.

## 2. Budgeted Causality: where the balance comes from (C2a)

**Why it matters:** fewer than one child on average and space dies; more and it explodes into a shape with no dimension; exactly one gives smooth geometry. The real universe sits at that balance to about one part in 10⁶¹.

**ED's answer:** each event carries a budget.
- **The naive reading** — holding links uses up budget — pushes *away* from the balance and ran away in every run.
- **Budget passed forward and conserved** pulls toward it: each event splits its budget over its forward links, and new events sum what arrives.

**The model:** slices held their size in every seed, and the geometry stayed two-dimensional. The one miss was the **average itself**: averaging each tick's growth ratio reads high whenever sizes swing. **Allen recognised it as his prime-triangle angles** — measure it as a log-ratio and the ups and downs cancel. Measured that way the offspring average is **1.000** everywhere. The measure was adopted and **retested on fresh seeds: pass.**

**Recorded:** the balance self-organizes from ED's budget passed forward and conserved. Consistent, not derived; k and L\* are knobs; space settles as a fixed-size tube, and growth would need budget creation — the cosmic excess, inherited.

**This is ED's one structural difference from CDT, and it survived everything: what CDT tunes, ED conserves.**

## 3. Synced Now: why three dimensions (C2b)

**The idea:** clocks at different places tick at slightly different rates and pull each other into line, but only so much. "Now" is where the clocks agree, and it wobbles. If the wobble tilts "now" as steeply as influence travels, "now" folds into time.

| slice dimension | the tilt of "now" | a real "now" at large scales? |
|---|---|---|
| 1 | grows | no |
| 2 | holds, at a value set by a ratio | only with a tuned ratio |
| **3** | shrinks | **yes, with nothing tuned** |

Sync needs three or more dimensions; commitment favours the fewest; so three. It only works because each place's rate **persists** — with rates redrawn every tick, every dimension keeps a "now."

**Three runs.** The first left the regime the calculation covers; the second missed at the edges because the average was taken the wrong way — **Allen's averaging lesson again**, wobbles add as squares; the third, on fresh seeds, **passed**: wobble exponents 1.54, 1.02, 0.42 on grids against the exact 1.50, 0.99, 0.47, and 1.68, 0.96, 0.54 on random slices.

**A side result on the rest frame:** in three dimensions the local "nows" scatter up close and line up with distance, so **one large-scale rest frame comes out of sync** rather than being imposed.

## 4. Trying to grow space (C3a, C3b)

**In 2D (C3a):** growth with no preference made a crumpled random surface; a local curvature cost tidied things up close (busiest event 12 neighbours instead of 79) but the surface still roughened as it grew. **Not reached.** It matched the literature exactly, and it taught the lesson that shaped everything after: **local costs don't act at large scales.**

**The static check (C3b): pass.** Given stand-in slices of each bad shape, each of ED's meanings caught its own:
- **commitment** caught crumpling (links per event growing 5×);
- **quadratic energy** caught ballooning;
- **sync** caught branching — the strain landed on a neck link in every single run;
- **flat 3D slices tripped nothing.**

## 5. Growing a 3D slice: five runs (C3c–C3g)

| run | what happened | what it taught |
|---|---|---|
| **C3c** | Density ran away, even with no pressures | Nothing balanced the **links**. ED balanced events, not the weave |
| **C3d** | Slices shrank to 0.6–0.8 of their size | The "no infinities" ceiling was tight enough to block growth itself |
| **C3e** | Sync, written as a reward, collapsed the slice | Rewiring was stealing the link budget growth needed. Fixed by doing cut-and-rejoin **in pairs**, which attempt 6 had already decided |
| **C3f** | Everything held — counts, structure, budgets, rewiring — and the pattern still wasn't flat | The sync setting came out **identical** to the control, exposing a units bug in Claude's code |
| **C3g** | With that fixed, sync finally acted | Slices widened for the first time (diameter 12.5 → 15.0, flat is 18), and the spacetime reading moved 6.44 → 6.33, where flat should be about 4 |

**Then one dial was turned.** Tightening sync's threshold kept changing the pattern — and not toward flat. Slices overshot the flat width (25 and 23 against 18), and once the readings resolved they said **branched**: spectral dimension 1.35 and 1.59, the tree-like signature. Tighter still, and growth strangled.

## 6. The wall (C103)

> **ED's local growth rules, with its conserved budgets and its three meanings, move the pattern along a line from crumpled to branched. At the sizes reachable here, there is no flat three-dimensional middle between them. The counts are solved; the shape is not.**

**Random 3D geometry has the same shape:** crumpled and branched meeting with nothing smooth between. CDT escapes it by summing over all geometries with a causal slicing, not by growing one history under local rules.

**What the wall is not:** not a code failure (structure, budgets, ceiling and rewiring were exact in every run; the cost bookkeeping matched a full recomputation to 5 × 10⁻¹³), not a failure of sync's reading (once fixed, it was the only thing that moved the pattern), and not a claim about bigger patterns — every slice here was at most 24 events across.

## Where attempt 7 stands

| | |
|---|---|
| **Passes** | Four: the CDT match, Budgeted Causality, Synced Now, the static three-meanings check |
| **Reasons for three dimensions** | Three, all consistent, not derived: lasting kinds (attempt 4), rates able to match (attempt 6), a synced now (attempt 7) |
| **Structural difference from CDT** | What CDT tunes, ED conserves — for events and for links |
| **Inputs supplied** | **3**, unchanged all attempt |
| **New numbers, or anything measurable** | None |

## Honest limits

- **Consistent, not derived, throughout.** No input was removed; the census guard never moved.
- **C1 and C2b confirm known mathematics inside ED's setting.** What is ED's own is the readings — budget passed forward, sync as a "now," persistent rates — and that they fit together.
- **Still put in:** the slice's dimension, whole-number dimension, the density, the knobs (k, L\*, K, σ, α, λ, γ, the ceiling), commitment's push toward the fewest directions, and the cosmic excess.
- **Resolution is a real limit.** Slices of 14,000 events are 24 across, which is why many readings came back "too small to measure." Proper slice geometry needs roughly ten times more events, which needs a compiled model.
- **Nine specification or code errors were Claude's**, each caught by a run or a test and each recorded: readings undefined at the smallest size; tick costs estimated from early ticks; the ceiling left out; a ceiling too tight; a budget gate that refused the moves that paid it down; flips read loosely against a decided meaning; a crumpled test set below the ceiling; no floor on diameter; and a units mismatch that made the sync condition inert.
- **Two of the three 3D runs went on that bookkeeping** rather than on ED.

## Carried forward

1. **Larger sizes**, via a compiled model, to see whether a flat middle exists where geometry can be measured.
2. **The 2D result judged on the grown spacetime**, the way everything else now is. CDT's own slices are fractal, so C3a was held to a stricter standard than CDT meets.
3. **Road D:** does ED's balance need genuine chance, or would incommensurate periods — Allen's prime wheel — do?
4. **Sync acting other than move by move.** In Synced Now it worked on whole slices, not on single moves.

## Words used here

| word | meaning |
|---|---|
| **Slice** | All the events at one tick: space at a moment |
| **Budget** | What an event passes forward or holds; conserved |
| **Balance** | Offspring averaging exactly one, so space neither dies nor explodes |
| **Wobble** | How much clock readings differ across a region |
| **Tilt** | Wobble over distance; "now" folds into time if it reaches one hop per tick |
| **Crumpled** | Everything close to everything |
| **Branched** | Stringy and tree-like, with thin necks |
| **Flat** | Ordinary space: volume growing like distance cubed |
