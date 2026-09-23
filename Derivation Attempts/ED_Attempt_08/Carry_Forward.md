# What attempt 7 hands to attempt 8

*ED_Attempt_08, note 1. 2026-09-19 (RD1). Ledger: C1. A summary of A7-ledger C103, C104, C105 and RD56; nothing tested.*

## The meanings, carried

**From attempts 4–6** (A7 note 1, unchanged): presence and influence kept separate; mass as what a body sends out; sameness, not place; time as order, space as pattern; motion as committing as much as possible along a path; light uncommitted until absorbed; pairings as a body's ticks; mutual influence; no infinities, finite neighbours; what happened stays happened; paired cut-and-rejoin; handle-free kinds; antiparticle as reversed mirror; the grain as a count; a direction-free random pattern; entropy as a crossing count; a strict one-way time order with a quadratic interval where things look smooth; **the pattern is the order itself** — links point earlier to later, space is a slice, growth only adds to the future, and a slice does not split or merge.

**Decided in attempt 7:**

| area | meaning | A7 source |
|---|---|---|
| **The balance** | **Budget is passed forward and conserved.** Each event splits its budget over its forward links; a new event sums what arrives. Holding a link does not spend it | D8 |
| **Sync** | **A shared "now."** Rates differ from place to place and **persist**; links pull them together; "now" is where they agree | D11, D12 |
| **Links** | **The link budget is conserved too**, pinning the weave's density where dynamical triangulations tune it | D30 |
| **Rewiring** | **Cut-and-rejoin only in pairs**, as attempt 6 decided; single flips drain the budget growth needs | D35 |
| **Sync in growth** | **A condition, not a reward.** A reward pays for shortcuts and flattens the tick field | D39, D41 |
| **Readings** | Judge the **grown spacetime**, not the slice alone; a calibration gate, with **"too small to measure" as its own honest outcome** | D40 |
| **Names** | **Commitment Dynamics** (framework), **Budgeted Causality** (the balance), **Synced Now** (three dimensions) | D15 |

## Inputs supplied so far

| input physics assumes | ED's status |
|---|---|
| **The Born rule** | Supplied, in form (A2 C11) |
| **Horizon entropy ∝ area** | Supplied, conditional on two readings and a direction-free three-dimensional pattern (A5 C17) |
| **Exactly one time dimension** | Supplied, conditional on a reading and the quadratic interval (A5 C37) |

**Three, unchanged through attempt 7.** Everything else is relocated, reinterpreted, inherited, or not reached ([What_ED_Needs.md](../What_ED_Needs.md)).

## The walls, carried

| | wall | state after attempt 7 |
|---|---|---|
| **1** | **The rest frame** | A risk, with one new reading: in three dimensions the local "nows" line up with distance, so a single large-scale rest frame **comes out of** sync rather than being imposed (C28). Local Lorentz invariance untouched |
| **2** | **The dark sector** | Untouched. Stuck states are dark; leakage when links rewire is open |
| **3** | **Growth** | **Restated, not removed.** ED now has a growth rule that holds the counts, keeps the topology and rewires without splitting — and it runs from crumpled to branched with **no flat three-dimensional middle** at reachable sizes (C103). The wall is now about **shape**, not about having a rule |
| **4** | **Numbers** | Inherited, and attempt 7 added knobs: k, L\*, K, σ, α, λ, γ, the ceiling, the link density, the sync threshold, the run length |
| **5** | **The handle-free rule** | Chosen, not derived |

**Also open:** spin and charge; which knot is which particle; PF-Q2; the discrete-to-continuum step; the time-ordered smoothness theory; short waves in the moving sector.

## What attempt 7 learned that attempt 8 can use

**Results that stand** (four passes):
- **C1:** ED's causal growth reproduces 2D CDT exactly, against a known answer.
- **C2a, Budgeted Causality:** the balance self-organizes from a budget passed forward and conserved. **What CDT tunes, ED conserves.**
- **C2b, Synced Now:** a shared "now" survives at large scales only in three or more dimensions; commitment picks the fewest.
- **C3b:** each bad 3D shape trips exactly one of ED's meanings; flat trips none.

**Tools** (in `../ED_Attempt_07/model/`, reusable):
- **`c3c.py`** — a 3-torus as a rotation system: topology-safe splits and merges under the 3D link condition, Pachner 2–3 and 3–2 flips with proposal corrections, and a `check()` that verifies degree sums, link spheres and orientation exactly.
- **`c3d.py`, `c3e.py`, `c3f.py`** — the conserved link pool with its ceiling, paired flips, and sync as a one-pass condition with per-tick bookkeeping.
- **`c3a.py`/`c3b.py` readings** — ball growth with a calibration gate, walk-based spectral dimension, diameter and mean distance, and neck strain from the linear sync steady state.
- **A resumable runner** with per-job JSON and pickled state.

**Cost and method lessons:**
- **Resolution was the binding limit.** A 13,824-event slice is 24 events across; most slice readings came back "too small to measure," while spacetime readings worked at 250k–292k events.
- **Pure Python capped the size.** Roughly 3 hours per run at these sizes, with memory pressure at 4–6 workers.
- **Measure before you tighten.** The one run that changed the picture was the one where a units bug was found by measuring how often a gate fired.
- **Nine of Claude's specification and code errors** were caught by runs or tests in attempt 7. Two of the three 3D attempts were spent on them. **Add a cheap instrument to every gate.**

## The opening road

| road | question |
|---|---|
| **E: resolution** | Does a flat three-dimensional middle exist at slices ten times larger, where geometry can actually be measured — or does ED's growth run crumpled-to-branched at every size? |

**Why this one:** road C ended on a single question it could not answer with the resolution it had. Nothing on paper settles it; only bigger slices do. **That needs a compiled model** — arrays instead of Python objects, with Numba or C for the inner loop — reproducing `c3c`–`c3g` exactly before it is trusted.

**Suggested order:**
- **E1 on paper:** what the port must reproduce bit for bit, what would count as a flat middle at the larger size, and the exit rule.
- **E2:** the port, checked against attempt 7's runs on identical seeds.
- **E3:** the larger runs.

**Also carried, not opened:**
- **Road D:** does ED's balance need genuine chance, or would incommensurate periods — Allen's prime wheel — do? (A7 C83, `../ED_Attempt_07/Possible_Roads.md`.)
- **The 2D result judged on the grown spacetime** (A7 C89): CDT's own slices are fractal, so C3a was held to a stricter standard than CDT meets.
- **Sync acting other than move by move.** In Synced Now it acted on whole slices.
- **Is ED's conserved balance a critical point, or an ordinary one?** The deep question behind Budgeted Causality.
