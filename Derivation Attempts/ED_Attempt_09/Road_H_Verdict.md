# Taking stock of road H, in plain language

*ED_Attempt_09, note 11. 2026-09-21 (RD13). Ledger: C42. Reasoning only; nothing computed.*

## What road H asked

Attempt 8 showed that ED's growth rule, not the size of the patch, was why ED's space came out wrong. **Road H asked: is the *kind* of rule right?** ED grows its pattern one step at a time, with local preferences and positive weights.

## What it did, run by run

| | what we tried | what happened |
|---|---|---|
| **H1** | Took out the commitment and curvature costs and kept only ED's conditions (the budgets and the neighbour limit) | **Space felt three-dimensional up close for the first time** (2.8–3.0, where flat is 3.0) and density sat exactly at flat. **But the slices were small worlds** — every point a few steps from every other |
| **H2** | Judged the whole spacetime, as attempt 7 had decided | **The shortcuts spoil the spacetime too** — it reads about 6 where flat reads about 3.6 |
| **H3** | Weighed whole histories, favouring the fewest directions; first a feasibility check | **Picking the best didn't build up**: about 58% of each slice was rewired every tick, erasing any gain. And the floor let stringy slices through |
| **H4** | Mostly one child, so slices change slowly | **Churn fell to 6%, but flat space still collapsed into a small world within about 20 ticks** — even with the rewiring moves off — and never came back |
| **H5** | Picked the best again, now that slices persist | **Still didn't build up.** It neither climbed from a small world nor slowed the collapse from flat |

## What you decided along the way

| | decision |
|---|---|
| **Commitment** | Is passed on, not held, so the link budget already expresses it; the per-link cost was dropped (D3) |
| **Curvature and quadratic energy** | Are conditions the slice must meet, not costs to minimise (D3) |
| **Sync** | Means clocks can tick at the same rate **across the whole pattern** — no single shared "now" (D5) |
| **Histories** | **ED weighs whole histories** against each other (D9) |
| **Children** | An event has **mostly exactly one child** (D11) |

**Still open, and yours:** whether "fewest directions" is what commitment really means (H3-Q2), and where the floor's line should sit (it's currently toothless).

## What road H found, one line each

1. **The parts built as conditions work; the parts built as costs don't.** (C2)
2. **Without the costs, ED's space feels three-dimensional up close** — the first time ever. (C13)
3. **The shortcuts are the large-scale shape, not a measuring quirk** — they spoil the spacetime. (C21)
4. **Flat space turns into a small world under any random change, however rare, and never turns back.** The churn rate only sets how fast. (C37)
5. **A weak preference can't beat the count of crammed shapes.** The push needed grows with the size of the slice. (C41)
6. **A correction:** the leading rival theory doesn't get space from cancellation; it weighs whole histories with a *tuned* strength. (C16)
7. **Flat spacetime reads 3.6, not 4**, so every earlier spacetime gap was bigger than recorded. (C20)

## The wall, as it now stands

> **Nothing in ED's growth prefers an extended shape. Any random change drifts toward crammed small worlds, because there are so many more of them. Beating that needs a strong preference that grows with the size of the slice — and ED doesn't have one.**

**That's sharper than where attempt 9 started.** It isn't about the settings, the churn, the costs or how sync is built. **It's about one missing ingredient**: something that prefers extended space strongly enough.

## Where the missing ingredient could come from

| | route | what it is | what it would tell us |
|---|---|---|---|
| **(i)** | **Tune it**, as CDT does | Build a proper weighing over whole histories and turn up the strength until something happens | Whether *any* strength gives 3D space. Days to build; the strength becomes a tuned setting — weaker than Budgeted Causality, which tuned nothing |
| **(ii)** | **Find what ED conserves that sets it**, as the budget sets size | On paper first: is there a quantity ED conserves that would automatically push toward extended shape as a slice grows? | If found, **the most important result this project could produce.** No design exists yet |
| — | **Amplitudes** (held back) | Weights that can cancel | Possibly a different mechanism; no working example |
| — | **Roads R and I** | Your rate-matching and interaction ideas | Different questions, not about shape |

## What stands, unchanged

**Budgeted Causality** and **Synced Now** — neither is about growing the pattern. **ED can't collapse** (attempt 8). **Inputs supplied: still 3.** Nothing derived.

## What it cost

| | |
|---|---|
| **Compute** | about 6 hours |
| **Ledger** | 41 claims, 12 of your decisions, 12 recorded steps, 11 notes |
| **Claude's slips** | **one code defect** (an extra random draw in the new growth step), caught before any use; **two weak test designs** (a pass rule a one-tick bump could satisfy, and a floor set too loosely), each caught by its own run; and **one earlier claim corrected** (that cancellation is what makes the rival theory work) |

## Options (you decide)

| | option | why |
|---|---|---|
| **(a)** | **Conclude attempt 9 and open attempt 10 on "what sets the shape?"**, starting with route (ii) on paper, with route (i) as the test | Attempt 9's question — is the kind of rule right? — is answered: it's missing a strong preference for extended shape. The next question is what could supply it |
| **(b)** | Stay in attempt 9 and take route (ii) on paper | Same work, same ledger |
| **(c)** | Build route (i) now | Answers "does any strength work?" directly; days of work |
| **(d)** | Switch to roads R and I, or amplitudes | Different questions |
| **(e)** | Pause | Nothing in the record needs finishing |

**Proposal: (a).** Route (ii) is the question that would make the answer ED's own, and it costs nothing but thought to start.
