# H1: do commitment and curvature mean what ED means? (on paper)

*ED_Attempt_09, note 2. 2026-09-21 (RD2). Ledger: C2–C5. **Reasoning and existing run values only; nothing new computed.** Questions H1-Q1–H1-Q4 are for Allen. Written plainly.*

## What H1 asks

The model grows ED's pattern using two **costs** — numbers it tries to keep low when picking moves:

- **commitment**, written **α·E**: every link costs a little, so fewer links is preferred;
- **curvature**, written **λ·Σ(valence − 5.10)²**: every edge whose count of surrounding pieces differs from the flat value costs a little, so flat-looking edges are preferred.

**Sync got into the model the same way, and turned out not to mean what ED means** (A8 D10). H1 asks the same of these two.

## The pattern attempt 8 left behind (C2)

**Line up everything in the growth model by how it was built:**

| | ED's meaning | built as | what it does |
|---|---|---|---|
| **No infinities** | A finite limit on neighbours | a **condition**: moves past 60 are refused | **Works.** Forbids the crumpled state (A8 C22) |
| **Link budget** | Links are passed forward and conserved | a **conserved quantity** | **Works.** Forbids the crumpled state too, and holds density where it should be (A8 C22) |
| **Sync** | A whole slice agreeing | a **local veto** on single moves | **Harmful.** Makes slices stringier and unable to hold a common "now" (A8 C48–C50) |
| **Curvature** | *(below)* | a **local cost** | **Only acts up close.** Flattens nearby, not at large scales (A7 C53) |
| **Commitment** | *(below)* | a **local cost** | *(below)* |

> **The parts built as conditions work. The parts built as local costs don't.**

That's worth holding onto for the rest of this note.

## Commitment (C3)

### What it meant

| | |
|---|---|
| **Attempts 4–5** | Motion is a body **committing as much as possible along its path** |
| **Attempt 6 (D8)** | Growth adds links **where clocks' rates fail to match**, each one costing commitment |
| **Attempt 9 (A8 D12, Allen, two days ago)** | *"A node doesn't stay committed, it **passes it on**."* |

### What it became

**Attempt 7, C3-Q8:** *"each link costs, so degree is penalised"* — cited as already decided. **The words "where rates fail to match" dropped out.** Every link now costs the same, whatever the clocks are doing. Same drift as sync: a statement about **clocks** turned into a flat **count**.

### What it does — and this one is measured

| what's switched on | mean degree | share of link budget used |
|---|---|---|
| **commitment on** (four runs) | **10.2 – 10.3** | **77–79%** |
| **commitment off** (four runs) | **14.2 – 14.3** | **98–99%** |
| *flat slice* | *14.00* | — |

**Without commitment, density sits almost exactly at flat. With it, density drops 27% below flat.** Attempt 7 already wrote down which way that pushes: *"commitment pushes toward few links, which is branched"* (A7 note 15).

### Why it was put there

To stop the pattern **crumpling** — everything piled onto everything (A7 notes 12 and 15). **But attempt 8 showed the link budget and the ceiling already forbid crumpling, each on its own** (A8 C22). So commitment's job is done twice over by the parts that work, and **what's left of it is the push toward sparse and stringy.**

### And the meaning points the same way

Your D12 says commitment is **passed on, not held**. The α·E cost charges for **holding** links. That is the reading attempt 7 tested for offspring in C2a — *holding uses up budget* — and found pushing **the wrong way**. The reading that worked was *passed forward and conserved*, and **that is exactly what the link budget already is.**

> **Claude's reading, labelled:** ED's commitment is already in the model — as the link budget. The α·E cost is a second, older reading of the same word, doing a job that's already done and pushing the density below flat.

## Curvature (C4)

### What it meant

Attempt 6's smoothness note (A6 S1) took a **mathematical recipe for smooth space** — Mondino and Naber's — which says a rough space **looks flat almost everywhere** if it satisfies **three conditions**:

| | condition | ED's reading (A6 D10) |
|---|---|---|
| **1** | **Curvature bounded below** — neighbouring regions never spread apart faster than some bound | **Sync as contraction** (S-Q1, labelled) |
| **2** | **Dimension bounded above** | **No infinities** (S-Q3) |
| **3** | **Quadratic energy** — the cost of a *difference* between values on the space goes like its square | **Like the Born rule** (S-Q2, labelled) |

**All three are conditions a space either satisfies or doesn't. None is a cost for growth to minimise.**

### What it became

**Attempt 7, C3-Q3 and C3-Q9:** a quadratic **cost** on how far each edge's count of surrounding pieces sits from 5.10.

**That merges conditions 1 and 3 into one thing that is neither:**

- condition 1 is **one-sided** (spreading apart must not *exceed* a bound); the cost is **two-sided**, penalising both directions;
- condition 1 is about **how random walks draw together** across a region; the cost is about **one edge at a time**;
- condition 3 is about **the energy of values living on the space**, like clock readings; the cost is about **the shape of the space itself**.

### And the one condition built faithfully is the one that works

**Condition 2 — dimension bounded above — was built as a condition:** the ceiling of 60 neighbours. It's the one that forbids crumpling. The other two became costs, and neither reaches large scales.

> **Claude's reading, labelled:** ED's curvature meaning is a pair of conditions from a smoothness theorem. They were turned into a local penalty on edges. The theorem says spaces *meeting* the conditions look flat; it says nothing about growth that *minimises* a penalty getting there.

## What this adds up to (C5)

**All three of ED's shaping meanings were written as conditions or as things passed along, and all three reached the model as local costs or vetoes.** Every one that stayed a condition works. Every one that became a cost doesn't.

**Which suggests a clean test, and it's cheap:**

> **Grow with only the conditions** — the link budget and the ceiling, no commitment cost, no curvature cost, no sync veto — **then check the finished slices against the conditions**: the scale-resolved spectral dimension, the tilt for a common "now", and a direct measure of **curvature bounded below** (Ollivier's contraction, the actual condition 1).

This is attempt 7's **setting D**, never measured at size — at 13,824 events it was "too small to measure". It has never been run at 140,000.

### What it could show

| outcome | what it means |
|---|---|
| **Slices meet the conditions** | **The costs were the problem.** ED's meanings, built as conditions, grow smooth slices — a major result |
| **They don't, and look stringy or compact** | **ED's conditions alone don't beat the counting.** With every cost removed, the shape is left to entropy — and that isolates **H2, weights that can cancel**, as the one question left |
| **Too small to measure again** | The resolution wall; recorded plainly |

**Honest expectation:** the second. Attempt 7's setting D at 13,824 events came out dense (mean degree 14.3, right at flat) but very compact (diameter 9–12 against flat's 18). **Density right, shape wrong** — which is what you'd expect if entropy, not cost, is running the shape. **But it has never been measured where it could show, and it's the last test before H2.**

## Questions for Allen

| | question | proposed default | why |
|---|---|---|---|
| **H1-Q1** | **Commitment is passed on, not held — so the link budget already expresses it**, and the separate α·E cost is dropped? | **Yes** | Your D12; attempt 7's C2a showed "holding uses budget" pushes the wrong way; measured, α·E drops density 27% below flat |
| **H1-Q2** | **"Curvature bounded below" is a condition on slices**, not a cost in growth? | **Yes** | That's how attempt 6 wrote it, from a theorem about conditions |
| **H1-Q3** | **"Quadratic energy" is a property of values living on the space** (like clock readings), not a penalty on the space's shape? | **Yes** | That's what the theorem means by it, and attempt 6 compared it to the Born rule, which is about values |
| **H1-Q4** | **Test it:** grow with the budget and ceiling only, at n = 24, 32, 52, and check the slices against the conditions — with a calibrated curvature reading added | **Yes** | Setting D has never been measured at size; about 3 hours; the last test before H2 |

## What H1 does not do

- **It doesn't touch weights that can cancel.** If the conditions-only slices come out stringy, that's H2.
- **The ceiling of 60 is still a knob.** It's saturated in every run, meaning some events have four times flat's neighbours. "No infinities" says finite; 60 was chosen because 30 blocked growth. Worth watching, not changing yet.
