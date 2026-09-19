# Road C4: the link balance (on paper)

*ED_Attempt_07, note 20. 2026-09-18 (RD36). Ledger: C72–C74. Literature, reasoning and counting; nothing computed. **Meaning questions C4-Q1–C4-Q5 and the draft exit rule are for Allen.***

## Where C3c left it

**C2a balanced events. Nothing balanced links.** In C3c, tetrahedra per event ran from 5.7 to 20 or more **even with no pressure at all**, and the readings couldn't measure the dense slices that resulted (C70, C71).

> **The question here: what, in ED, fixes how many links hold the events together?**

## What's known (C72)

| | what it says | source |
|---|---|---|
| **The count of geometries grows exponentially** | The number of triangulations of a surface with N pieces grows like e^(μ_c·N) (Tutte). The same exponential bound is assumed, and was debated, in higher dimensions | Ambjørn, Carfora, Marzuoli, *The Geometry of Dynamical Triangulations* (hep-th/9612069); [hep-lat/9403019](https://arxiv.org/pdf/hep-lat/9403019) |
| **So a weight per building block has to be tuned** | In dynamical triangulations the bare cosmological constant is tuned to its critical value to reach the infinite-volume limit. Below it the geometry runs away; above it it collapses | DT and CDT reviews ([arXiv:1904.05755](https://arxiv.org/html/1904.05755), Scholarpedia) |
| **That's exactly C3c's failure** | With no weight (S0) the slice densified; with commitment at strength 1 the mean held but the extremes didn't | A7 C70 |
| **Self-organizing instead of tuning is a known idea** | Feedback that drives a system to its critical point without tuning: self-organized criticality, including attempts in quantum gravity | Zapperi, Lauritsen, Stanley (A7 C9); "Self-organized criticality in quantum gravity" ([hep-th/0412307](https://arxiv.org/pdf/hep-th/0412307)) |
| **ED already did this once, for events** | Budget passed forward and conserved holds the event count at L\* with no tuning of the average | A7 C31 (Budgeted Causality) |

## On paper

### 1. Two ED meanings C3c didn't use (C73)

| | decided meaning | where | what C3c did instead |
|---|---|---|---|
| **No infinities** | "There are no infinities in ED": a finite ceiling on how many neighbours an event can have | A4 D32, PF-Q1 | **No ceiling was imposed.** Events reached 224, 406, even 2,135 neighbours |
| **Commitment is a budget** | An event has a budget; commitments use it up | A4, C2a | The budget set **offspring**, but holding links cost nothing |

**So C3c left out a decided meaning and used only half of another.** That's enough to explain the runaway on its own.

### 2. The trick that worked for events, applied to links (C73)

**In C2a there were two readings of the budget:**
- **Reading A, "links held use up budget":** it destabilized the **event** count and ran away every time, so it was set aside.
- **Reading B, "budget passed forward and conserved":** it balanced the event count.

**Here the roles swap.** Reading A is about exactly this question: **holding links costs budget.** Applied to links rather than offspring, its sign is right:
- **A crowded event** holds many links, so its budget is used up and it can't take more.
- **A sparse event** has budget free and can take more.
- **Conserved total** means the slice's total link count is pinned by the total budget, not by a tuned weight.

**The counting.** Give each link a cost of one unit of commitment, split between its two ends. Then:
- **total links = total commitment budget**, exactly;
- **links per event = B_L / V**, which the budget fixes;
- **a move that adds a link needs free budget; a move that removes one frees it.**

**What that changes.** In dynamical triangulations the count of building blocks is held by a coupling that must be **tuned to a critical value**, with runaway on one side and collapse on the other. In ED it would be held by a **conserved quantity**, so:
- **no fine-tuning:** any budget value sits stable;
- **the flat value is a knob**, not an emergent number. A flat 3D slice has 6.70 links per event, so putting that number in as the budget would be putting flatness in, and that has to be said plainly (census guard);
- **what stays open** is whether, at that density, the three pressures give a **flat** slice rather than a crumpled or branched one at the same density.

### 3. What the ceiling does (C73)

**"No infinities" caps how many links one event can hold.**
- **It kills the extremes** C3c produced (one event with 2,135 neighbours).
- **It's the same thing that rules out the crumpled phase** in C56's table, now as a hard limit rather than a cost.
- **The ceiling's value is a knob,** though "finite" is already decided.

### 4. What this does not fix (C74)

- **Shape, not just density.** Fixing links per event leaves crumpled, branched and flat all possible at the same density. Curvature and sync still have to pick between them.
- **The readings.** C3c couldn't measure dense slices. With density pinned near the flat value the slices should be wide enough again, but the reading limit has to be checked directly (the flat calibration failed at 4,096 events).
- **The numbers.** Budget per event, ceiling and the three strengths are all knobs.

## What it means (C74)

- **C3c's runaway wasn't ED's failure. It was two decided meanings left out of the model:** no infinities, and commitment as a budget that holding links uses up.
- **The event balance and the link balance are the same trick twice:** a conserved budget instead of a tuned coupling.
- **The thing dynamical triangulations tune,** the weight per building block, ED would hold with a conservation law. That's the same move C2a made for the cosmological constant.
- **Consistent, not derived.** Nothing computed; inputs unchanged (3).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C4-Q1** | **Does holding a link use up an event's commitment budget** (C2a's reading A, applied to links rather than offspring)? | **Yes, labelled reading** | It's the natural reading of "commitments use up budget"; its sign is right for links, unlike for offspring |
| **C4-Q2** | **Is that budget conserved,** so the slice's total link count is pinned rather than tuned? | **Yes** | The C2a trick; no fine-tuning |
| **C4-Q3** | **Is there a hard ceiling on links per event** (no infinities), with its value a knob? | **Yes** | A4 D32, already decided; C3c left it out |
| **C4-Q4** | **Is the budget per event set to the flat value (6.70 links per event), recorded as a knob and as flatness partly put in?** | **Yes, recorded plainly** | Any other value would test a different density; the honest label is that the density is put in and the shape is what's tested |
| **C4-Q5** | **Do offspring keep C2a's reading B** (budget passed forward, conserved) as a separate budget from the link budget? | **Yes, two budgets** | Events and links are balanced by different readings; mixing them was what C3c got wrong |

## Draft exit rule (Allen to confirm)

**Next step: spec C3d, C3c with the link balance and repaired readings.**
- **The model:** C3c's moves, plus
  - a conserved link budget, so a move that adds links needs free budget;
  - a ceiling on links per event;
  - the three pressures as before, at unit strengths.
- **Readings repaired:** checked first on the flat and randomized calibrations at each size, with sizes chosen so the flat calibration reads flat (C3c's failure at 4,096 must not repeat).
- **Recording:**
  - **the density holds and some setting reads flat 3D:** "with the link balance and the ceiling, ED's meanings grow a flat 3D slice at the sizes run: consistent, not derived; the density, ceiling and strengths are knobs";
  - **the density holds but no setting reads flat:** "the link balance fixes density but not shape: ⟨shapes⟩", then take stock;
  - **the density doesn't hold:** a code or reading problem, recorded.
- **Expected results and ranges are fixed in the C3d spec before any code,** with an honest cost plan (C3c took over a day and needed guards).

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide C4-Q1–C4-Q5 and spec C3d** | The direct continuation |
| **(b)** | **Take stock of road C first** | Three model results and a wall-shaped finding; it may be a natural place to pause |
| **(c)** | **Repair the readings on paper first** (what reading measures a dense slice's dimension) | The other half of C3c's failure |

**Proposal: (a), with (c) folded into the C3d spec.**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C72 | Ambjørn, Carfora, Marzuoli, *The Geometry of Dynamical Triangulations* ([hep-th/9612069](https://arxiv.org/pdf/hep-th/9612069)); [absence of an exponential bound in 4D simplicial gravity, hep-lat/9403019](https://arxiv.org/pdf/hep-lat/9403019); [Critical phenomena in CDT, arXiv:1904.05755](https://arxiv.org/html/1904.05755); [CDT Scholarpedia](http://www.scholarpedia.org/article/Causal_Dynamical_Triangulation); [Self-organized criticality in quantum gravity, hep-th/0412307](https://arxiv.org/pdf/hep-th/0412307) | Listings and abstracts, 2026-09-18 |
| C73 | Counting: one unit of commitment per link gives total links = total budget and links per event = B_L/V; a flat 3D triangulation has E/V = 6.70 (C66) | Worked, 2026-09-18 |
| — | A4 D32 (no infinities), PF-Q1; A7 C9, C14, C31, C56, C66, C70, C71 | Ledgers |
