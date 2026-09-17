# Taking stock: road C and attempt 7 (on paper)

*ED_Attempt_07, note 11. 2026-09-16 (RD19). Ledger: C40, C41. Reasoning and a literature check; nothing computed. **The options at the end are for Allen.***

## What road C set out to do

**Attempt 6 ended at the growth wall** (A6 C88, wall 3):
> "A finite-neighbour causal growth rule where space doesn't split, with slice dimension three from sync and commitment."

**Road C split it in two:** the causal half (C1), and slice dimension from sync and commitment (C2). C2 turned out to need the balance first (C2a).

## What was reached

| | step | result | status | runs |
|---|---|---|---|---|
| **C1** | ED's causal growth, with slices given as circles and no splitting | **Reproduces 2D CDT:** slice length 1 + 2t (slope 2.05), mass dimension 2.17, walk-return dimension 1.89, structure exact | **PASS,** against a known answer | 1 |
| **C2a** | What keeps offspring averaging exactly 1? | **Budgeted Causality:** budget passed forward and conserved holds slices at L\* in every seed, with no tuning of the average. The naive reading runs away every time. Geometry stays 2D | **PASS** after one averaging revision (Allen's prime-triangle point), **retested on fresh seeds** | 2 |
| **C2b** | Does sync pick slice dimension? | **Synced Now:** with persistent clock rates and bounded pull, "now" flattens at large scales without a tuned ratio only for slices of 3 or more dimensions; 1D tilts more with size, 2D holds a ratio-set tilt. Holds on grids (matching the exact answer) and on random slices. Fresh-each-tick rates keep a "now" everywhere, so **persistence** makes the floor | **PASS** on run 3, after a regime fix and an averaging fix, **on fresh seeds** | 3 |
| **Frame** (C28) | Does the wobble touch the rest frame? | In 3D, local frames scatter up close and converge with distance: **one large-scale rest frame comes out of sync.** Seen in all three C2b runs | Reported reading, as expected | — |

**Tally:**
- **3 model passes,** each with expected results written first;
- **2 recorded revisions,** both about how to average: ratios telescoped, wobbles pooled as squares;
- **1 recorded reporting error, corrected** (a chart);
- **0 inputs removed.**

## What is still put in

| | put in | where |
|---|---|---|
| 1 | **Slices given,** as circles (C1, C2a) or as 1-, 2-, 3-dimensional slices (C2b). **Nothing grows a 3D slice yet** | C2-Q7 |
| 2 | **Whole-number dimension** (so "fewest above two" means three) | A6 G-Q10, assumption Q |
| 3 | **Commitment favours the fewest directions:** a labelled lead, not modelled | A6 G-Q7 |
| 4 | **Knobs:** k and L\* (balance); K and σ (sync). C2b's result doesn't depend on K/σ in 3D, but ED doesn't supply them | C19, C27 |
| 5 | **Strong coupling only** | C24 |
| 6 | **The cosmic excess** (growth beyond the balance): inherited | C12 |

## Where attempt 7 stands against the walls

| | wall | at the end of attempt 6 | now |
|---|---|---|---|
| **1** | **Rest frame** | A risk | **Unchanged risk locally.** New: the large-scale frame is produced by sync, not by the slicing (a "yes" reading of PF-Q2). A small frame jitter, set by σ/K, would need checking against measured bounds |
| **2** | **Dark sector** | Leakage open | Not touched |
| **3** | **Growth** | The open problem | **Two of its three pieces now have model support:** causal growth without splitting is smooth (C1), and the balance comes from budget (C2a). **Sync picks three among given slices** (C2b). **Still missing: a rule that grows 3D slices.** |
| **4** | **Numbers** | Inherited | Inherited (k, L\*, K, σ added to the list of unsupplied numbers) |
| **5** | **Handle-free rule** | Chosen | Not touched |

**Inputs supplied: 3** (unchanged). **What_ED_Needs row 6** (three dimensions) now has three consistent reasons: lasting kinds (A4), rates can match (A6), a synced now in the causal pattern (A7).

## Literature check on the new result (C40)

- **Oscillator floors are known:** rates match only above two dimensions, phases only above four (Hong–Park–Choi 2005; renormalization-group and lattice studies).
- **This check found no paper using them to explain why space has three dimensions,** or tying the rate floor to a synced "now" staying space-like. That's a statement about this search, not a claim of novelty.
- **Nearest relatives:**
  - **Energetic causal sets** (Cortês–Smolin, C37): conserved labels on causal links, emergent spacetime.
  - **Hogan's work on exotic correlations in emergent space-time:** Planck-scale drift between the phases of separate clocks.
  - **CDT without a preferred slicing** (Jordan–Loll): a de Sitter universe still emerges.

## Is this good? (C41)

**Yes, and here is exactly how good.**

**What's genuinely strong:**
- **It's the first time ED's growth wall has moved with models behind it.** Attempt 6's two models grew rings, tangles and small worlds. Attempt 7's three models each passed against expected results fixed first.
- **The pieces fit one picture:**
  - time as order gives smoothness;
  - budget gives the balance;
  - sync gives a "now";
  - commitment gives the fewest directions.

  Each piece came from an existing ED meaning, not a new one.
- **Three dimensions now has a picture you can draw.** "Now" folds into time in 1D and 2D and flattens in 3D. It rests on physics that's independently known (oscillator floors), checked inside ED's own pattern, including random slices.
- **The rest frame gets a new angle:** sync makes the large-scale frame, rather than a grid imposing it.
- **The record is clean.** Every miss, revision and correction is in the ledger, and each pass was re-earned on fresh seeds.

**What keeps it from being more:**
- **Consistent, not derived.** The census guard hasn't moved: 3 inputs.
- **C1 and C2b confirm known mathematics in ED's setting.** C1 is CDT; C2b's grid exponents are fixed by the equations. The ED content is the **readings** (budget passed forward, sync as a "now," persistent rates) and the fact that they fit together, not new mathematics.
- **The hardest piece is still open:** growing a 3D slice without splitting. Until something grows one, three is **selected**, not grown.
- **No number yet**, and nothing observable that differs from standard physics.

**In one line:** attempt 7 turned attempt 6's precise open problem into a working picture with model support for each part, and the part everyone else also finds hard, growing the slice itself, is still ahead.

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Road C3, on paper: growing a 2D slice without splitting.** Each event's offspring placed on a surface; sync and budget acting; does the slice stay 2D and smooth? A 2D slice is the smallest case that isn't a circle | The missing piece of wall 3. Start with 2D, since 3D costs far more |
| **(b)** | **Checks on C2b:** weak coupling; clock rates carried on C2a's grown circles | Hardens Synced Now before building on it |
| **(c)** | **Write-up:** a plain-language attempt 7 document using the working names (Commitment Dynamics, Budgeted Causality, Synced Now); possibly a repo note, like the Jacobson note | Road C's results are worth stating while they're fresh |
| **(d)** | **Conclude attempt 7** and carry forward | If you'd rather open the growth rule as attempt 8's road |

**Proposal: (c), then (a).** Write up what's reached while it's clear, then take on growing the slice.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C40 | Hong, Park, Choi, [PRE 72, 036217 (2005)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.72.036217); [Renormalization group approach to oscillator synchronization, arXiv:0810.3075](https://arxiv.org/pdf/0810.3075); [Critical properties of two-dimensional oscillator arrays, arXiv:0711.3775](https://arxiv.org/pdf/0711.3775); [Hogan, Statistical model of exotic rotational correlations in emergent space-time, arXiv:1607.03048](https://arxiv.org/pdf/1607.03048); searches on synchronization and the dimension of space, and on emergent simultaneity from clock synchronization | Listings and abstracts, 2026-09-16 |
| — | A7 C1–C39, D1–D15; A6 C88, C90; What_ED_Needs | Ledgers |
