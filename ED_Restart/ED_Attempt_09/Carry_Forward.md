# What attempt 8 hands to attempt 9

*ED_Attempt_09, note 1. 2026-09-21 (RD1). Ledger: C1. A summary of A8-ledger C51, C52 and RD19; nothing tested. Written plainly.*

## The question attempt 8 answered

**Was attempt 7's wall the growth rule or the patch size? The rule.** Bigger patches, a fast model, corrected sync — the same result came back at every size, identically.

## The meanings, carried

**From attempts 4–7** (A8 note 1, unchanged): presence and influence kept separate; mass as what a body sends out; sameness, not place; time as order, space as pattern; motion as committing as much as possible along a path; light uncommitted until absorbed; pairings as a body's ticks; mutual influence; no infinities, finite neighbours; paired cut-and-rejoin; handle-free kinds; the grain as a count; a direction-free random pattern; entropy as a crossing count; a strict one-way time order; the pattern is the order itself, space a slice, growth only adding to the future, slices never splitting or merging; budget passed forward and conserved; the link budget conserved; sync as a shared "now" with persistent rates.

**Decided in attempt 8:**

| | meaning | A8 source |
|---|---|---|
| **Sync** | **A whole slice agreeing, not a veto on single moves.** It drifted into a per-move veto through three modelling steps, none of them decided | D10 |
| **The past** | **Once something has happened it is fixed, but many things could have happened** | D11 |
| **Memory** | **The present doesn't know its own past.** A node passes its commitment on; history isn't recorded anywhere; to the present, any set of events that led to it is possible. **ED is an ensemble theory, and has been all along** | D12 |

## Inputs supplied

**Still 3:** the Born rule in form (A2 C11), horizon entropy's area law (A5 C17), one time dimension (A5 C37). Nothing derived in attempt 8.

## The walls, carried

| | wall | now |
|---|---|---|
| **1** | **Rest frame** | A risk; a single large-scale frame comes out of sync (A7 C28) |
| **2** | **Dark sector** | Untouched |
| **3** | **Growth** | **About the kind of rule.** ED cannot crumple (A8 C22); its local, step-by-step, positive-weight growth makes compact, stringy slices at every reachable size (A8 C37); bigger sizes cannot change that; and the slices cannot hold a common "now" (A8 C48–C50) |
| **4** | **Numbers** | Inherited; the sync threshold now a median over eight reading seeds (A8 C16, C20) |
| **5** | **Handle-free rule** | Chosen, not derived |

## Results that stand

- **Budgeted Causality** — the balance comes out of a conserved budget. *What CDT tunes, ED conserves.*
- **Synced Now** — three dimensions from clocks agreeing.
- **ED cannot crumple** — the link budget and the no-infinities ceiling each forbid it (A8 C22). In the rival theory that state is half of what blocks smooth spacetime.
- **ED's spectral dimension runs with scale** (A8 C36).

## Tools (in `../ED_Attempt_08/model/`, reusable)

| | |
|---|---|
| **`p3.py`, `p3_ops.py`, `p3_core.py`** | The fast port of attempt 7's model: 7.2× faster, 755 MB at 140,608 events, validated three ways (A8 C8, C15) |
| **`p3_readings.py`** | Attempt 7's readings, fed from the port |
| **`p3_dscurve.py`** | The spectral dimension at every distance, not one fitted number |
| **`f1_tilt.py`** | The tilt reading for a common "now", calibrated on a ring, a square torus and a cube torus |
| **`p3_verify.py`, `p3_tier3*.py`** | The three-tier validation ladder |

## Lessons worth keeping

- **Calibrate on objects whose answer is known**, and let the calibration stop the road. It caught five defects in attempt 8 before any result existed.
- **Fix the pass criterion before the data that tests it exists.** Twice in attempt 8 a criterion needed changing; both times the change was recorded before the data came in.
- **Look at where a reading is measured, not just its number.** The single fitted dimension was always the narrowest point of a curve (A8 C35).
- **On this machine, memory binds before time** at 140,000 events (A8 C25, C31).
- **Two Claude reasoning errors** in attempt 8, both about what a number meant rather than how it was computed (A8 C35, C47).

## The opening road

| | road | the question |
|---|---|---|
| **H** | **What kind of rule?** | ED's growth is local, step by step, with positive weights. Every setting of that has been tried. Is the kind of rule right? |

**Two parts, both on paper first:**

- **H1 — the local costs.** Commitment (α·E) and curvature (an edge sum) got into the model the same way sync did. **Do they mean what ED means?** The same check Allen gave sync.
- **H2 — weights that can cancel.** ED's ensemble uses only positive weights, so it lands on the most numerous shapes. ED's own Born rule works with weights that can cancel, and the growth model doesn't use it. **Should ED's growth carry amplitudes?** A large meanings question, and Allen's alone.

**Also carried, not opened:** the finer measuring ladder for road F's no-sync slices (A8 C50); the spacetime reading at 140,000 events, which needs about 6.5 GB (A8 C31).
