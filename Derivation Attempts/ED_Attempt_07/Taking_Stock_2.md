# Taking stock: road C and attempt 7, second stock-take

*ED_Attempt_07, note 25. 2026-09-18 (RD44). Ledger: C86. Reasoning only; nothing computed. The first stock-take was note 11, before road C3 began.*

## What road C has reached

| step | result | status | runs |
|---|---|---|---|
| **C1** | ED's causal growth with slices given as circles reproduces 2D CDT (slope 2.05, mass dimension 2.17, structure exact) | **Pass** | 1 |
| **C2a** | **Budgeted Causality:** budget passed forward and conserved holds the balance with no tuning | **Pass**, retested on fresh seeds | 2 |
| **C2b** | **Synced Now:** a synced "now" needs slices of 3+ dimensions without a ratio; commitment picks the fewest | **Pass** on run 3 | 3 |
| **C3a** | Grow a flat 2D slice | **Not reached:** a local curvature cost flattens locally, not at large scale | 1 |
| **C3b** | Each bad 3D shape flagged by one ED meaning, flat by none | **Pass** | 1 |
| **C3c** | Grow a 3D slice | **Wall:** nothing balanced links, so density ran away | 1 |
| **C3d** | Same, with the link balance | **Wall:** the ceiling blocked splits and slices shrank | 1 + diagnostic |
| **C3e** | Same, with paired flips | **Wall:** sync collapses the slice; nothing measurable | 1 |

**Four model passes, four walls, and every wall's cause identified.**

## What is now known to work

| piece | evidence |
|---|---|
| **The event balance** | Held in every run of C3c, C3d and C3e |
| **The link balance** | Conserved exactly; density stopped running away after C3c |
| **The readings, when slices are wide enough** | The calibration gate passes at both sizes in C3d and C3e |
| **Paired cut-and-rejoin** | Link-neutral every tick; rewiring stays healthy; splits no longer starved |
| **The guards** | Runaways become recorded outcomes instead of crashes |

## What is still put in

| | put in | where |
|---|---|---|
| 1 | **The slice's dimension:** circles in C1 and C2a, tetrahedra in C3c–C3e | C2-Q7, C3-Q1 |
| 2 | **Whole-number dimension** | A6 G-Q10 |
| 3 | **The density** (6.699 links per event, the flat value) | C4-Q4 |
| 4 | **The knobs:** k, L\*, K, σ, α, λ, γ, the ceiling | throughout |
| 5 | **Commitment's push toward the fewest directions**, a labelled lead, still unmodelled | A6 G-Q7 |
| 6 | **The cosmic excess** (growth beyond the balance) | C12 |

**Inputs supplied: 3, unchanged all attempt.**

## The failures, sorted by whose they are

**ED's meanings, tested and found wanting so far:**
- **A local curvature cost doesn't flatten at large scale** (C3a, and the same in 3D).
- **Sync, read as "reward links that carry strain," crowds the slice** (C3e). Commitment and curvature at unit strength don't hold it back.

**My specification errors, each caught by a run and recorded:**

| | error | caught by |
|---|---|---|
| 1 | Readings undefined at the smallest size | C3a's run, then C3c |
| 2 | Estimating tick cost from early ticks only | C3c's 2.9 h against 1 h |
| 3 | The no-infinities ceiling left out entirely | C3c's runaway |
| 4 | A ceiling of 30, close enough to block growth | C3d, then the diagnostic |
| 5 | A budget gate that refused the moves that pay it down | C3d's move test, before any run |
| 6 | Flips read loosely, against attempt 6's "only in pairs" | C3e's fix |
| 7 | The crumpled test set below the ceiling, so any slice touching it reads crumpled | C3e |
| 8 | No floor on diameter, so "unmeasurable" and "crumpled" look alike | C3e |

**That list matters for reading the last three runs:** the walls are real, but the *labels* in C3d and C3e are not trustworthy, and two of the three attempts were spent on my bookkeeping rather than on ED.

## What the runs say about ED's picture

- **Growth with no pressure at pinned density gives a slice that is too small across.** Diameters fell in every setting, even those that held their size.
- **That is what random rewiring does:** shuffling links at a fixed count makes shortcuts, and shortcuts shrink diameters. It's the small-world effect.
- **Sync as specified makes it worse, not better.** A link between two strained regions relieves the most strain, and strained regions are far apart, so **sync rewards exactly the shortcuts that destroy geometry.**
- **That's a sharp, testable suspicion about the reading itself** (C3-Q7), not about its strength: sync may need to act only within a neighbourhood, or may not belong in the move cost at all. Its job in C2b was to pick the slice's dimension, not to shape the slice.

## Where attempt 7 stands overall

- **Three "consistent, not derived" results** (C1's check against CDT, Budgeted Causality, Synced Now), each earned against results fixed in advance and each retested or reproduced.
- **One structural difference from CDT that survived every run:** what CDT tunes, ED conserves.
- **The growth wall has moved but not fallen:** slice dimension is still put in, and no grown 3D slice has stayed flat.
- **Nothing observable, no new number.** The census is unchanged.

## Options

| | option | cost | what it settles |
|---|---|---|---|
| **(a)** | **Paper work on sync's form:** should sync act only locally, or not in the move cost at all? Then a cheap targeted test | Hours on paper, then about 1 h of compute | The ingredient that is failing, rather than its strength |
| **(b)** | **C3f as specced before:** fix the shape rule and the diameter floor, scan sync's strength below 1 | About 7 h | Whether a weaker sync balances, with labels that can be trusted |
| **(c)** | **Drop sync from growth entirely** and test commitment plus curvature alone at pinned density, with fixed labels | About 3 h | Whether the other two can hold a flat slice on their own |
| **(d)** | **Conclude attempt 7** and carry road C forward | — | — |

**Proposal: (a), then (c) and (b) together as one run,** since both need the same label fixes and the same machinery.
