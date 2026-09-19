# Road C: the verdict

*ED_Attempt_07, note 30. 2026-09-19 (RD53). Ledger: C103. Reasoning only; nothing computed. Road C is closed with this note.*

## The wall

> **ED's local growth rules, with its conserved budgets and its three meanings, move the pattern along a line from crumpled to branched. At the sizes reachable here (up to 13,824 events per slice, 150 ticks), there is no flat three-dimensional middle between them. The counts are solved; the shape is not.**

**Said plainly:** ED can now grow a pattern that keeps its size, keeps its weave, never tears, and rewires itself without splitting. It cannot make that pattern look like ordinary space. Loosen the rules and it clumps together; tighten them and it strings out; nothing in between came out flat.

## What road C reached

| | result | status |
|---|---|---|
| **C1** | ED's causal growth, with slices given as circles, reproduces 2D CDT exactly | **Pass** |
| **C2a** | **Budgeted Causality:** the balance comes from a budget passed forward and conserved, with nothing tuned | **Pass**, retested on fresh seeds |
| **C2b** | **Synced Now:** a shared "now" survives at large scales only in three or more dimensions, and commitment picks the fewest | **Pass** on run 3 |
| **C3b** | Each bad 3D shape is flagged by one existing ED meaning, and a flat 3D slice by none | **Pass** |
| **C3a** | Grow a flat 2D surface | **Not reached** (and judged by a standard later corrected, C89) |
| **C3c–C3g** | Grow a 3D slice that stays smooth | **The wall above** |

**Inputs supplied: 3**, unchanged through the whole attempt.

## What is solved, and stayed solved

- **The event balance** (C2a), holding in every 3D run since.
- **The link balance** (C4, C3d), pinning what dynamical triangulations must tune.
- **Topology-safe moves:** link-condition merges, star splits, and paired cut-and-rejoin as attempt 6 decided.
- **The readings,** once a slice is wide enough, with a calibration gate that passes and a "too small to measure" outcome that is honest about resolution.
- **Guards** that turn runaways into recorded outcomes rather than crashes.

## What the wall is not

- **Not a code failure.** Structure, both budgets, the ceiling and rewiring were exact in every run of C3f and C3g; the cost bookkeeping matches a full recomputation to 5 × 10⁻¹³.
- **Not a failure of sync's reading.** Once the units bug was fixed, sync as a condition did act, and it was the only ingredient that moved the pattern at all.
- **Not a statement about larger sizes.** Every run here was at most 24 events across. The flat middle, if it exists, may live beyond that.

## Where the wall sits in the literature

- **Random 3D geometry has the same shape:** crumpled and branched phases meeting at a first-order transition, with no smooth phase between (C54, C72).
- **CDT escapes it** by summing over geometries with a causal time slicing, not by growing a single history under local weights.
- **ED's difference held throughout:** what CDT tunes, ED conserves. That bought the counts, and it did not buy the shape.

## Carried forward

| | open question | what it needs |
|---|---|---|
| **1** | Does a flat middle exist at sizes about ten times larger? | A compiled model; a day or two of work, then runs |
| **2** | Does the 2D result change when judged on the grown spacetime, as everything else now is? | A rerun of C3a's surfaces with spacetime readings |
| **3** | Does ED's balance need genuine chance, or would incommensurate periods do? | Road D, parked (C83) |
| **4** | Can sync act as something other than a move-by-move condition? | Paper work; C2b's version acts on whole slices, not moves |

## Status

**Road C is closed with the wall above.** Attempt 7 stays open for the write-up and stock-take.
