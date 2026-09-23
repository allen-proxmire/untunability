# What attempt 6 hands to attempt 7

*ED_Attempt_07, note 1. 2026-09-16 (RD1). Ledger: C1. A summary of A6-ledger C90 and RD30; nothing tested.*

## The meanings, carried

**From attempts 4–5** (A6 note 1): presence and influence kept separate; mass as what a body sends out; sameness, not place; time as order, space as pattern; motion as committing as much as possible along a path; light uncommitted until absorbed; pairings as a body's ticks; mutual influence; no infinities, finite neighbours; what happened stays happened; paired cut-and-rejoin; handle-free kinds; antiparticle as reversed mirror (an association); the grain as a count; a direction-free random pattern; entropy as a crossing count; a strict one-way time order, with a quadratic interval where things look smooth (labelled).

**Decided in attempt 6:**

| area | meaning | A6 source |
|---|---|---|
| **Waves** | One-tick rule; neighbours count equally, no stored directions; matter feels the pattern only through the walk; matter acts at points, treating links alike | D3, D4, D11 |
| **The dark sector** | Light is the moving sector; stuck states are real but dark, with no role assigned | D11 |
| **Growth** | Distance is a hop count; growth can end and re-route links, only in pairs; moves are local; growth is a process (links added where rates fail to match, each costing commitment); smoothness must come out of the rule, not be assumed | D5, D8 |
| **Three dimensions** | "Clocks want to sync" means rates can match; growth favours the fewest directions where rates can still match (labelled lead); a link's pull is bounded; rates differ at random; dimension is a whole number where things look smooth | D6, D7 |
| **Smoothness** | Sync includes contraction (curvature bounded below, labelled reading); quadratic energy (new labelled reading); no infinities gives a dimension ceiling | D10 |
| **Time order** | **The pattern is the order itself:** links point from earlier to later, and space is a slice (events none of which comes before another). **Growth only adds to the future. A slice of space doesn't split or merge** (labelled reading) | D22 |

## Inputs supplied so far

| input physics assumes | ED's status |
|---|---|
| **The Born rule** | Supplied, in form (A2 C11) |
| **Horizon entropy ∝ area** | Supplied, conditional on two readings and a direction-free three-dimensional pattern (A5 C17) |
| **Exactly one time dimension** | Supplied, conditional on a reading and the quadratic interval (A5 C37) |

**Everything else is relocated, reinterpreted, inherited, or not reached** ([What_ED_Needs.md](../What_ED_Needs.md)).

## The walls, carried

| | wall | state |
|---|---|---|
| **1** | **The rest frame** | A risk. What's left of the leak is the ordinary slow-short-wave question |
| **2** | **The dark sector** | Stuck states are dark; leakage when links rewire is open |
| **3** | **Growth** | **The open problem:** a finite-neighbour causal growth rule where space doesn't branch, with slice dimension three from sync and commitment |
| **4** | **Numbers** | G, masses, couplings, sync strength: inherited |
| **5** | **The handle-free rule** | Chosen, not derived |

**Also open:** spin and charge; which knot is which particle; PF-Q2; the discrete-to-continuum step; the time-ordered smoothness theory; short waves in the moving sector.

## What attempt 6 learned that attempt 7 can use

**Tools** (in `../ED_Attempt_06/model/`, reusable):
- **Calibrated dimension readings** (readings v2): mass dimension, ball-cut, walk-return and walk dimension. They passed 6 of 6 test patterns, including 2 held out.
- **A resumable job runner.** One result file per job, so a stop or reboot loses only jobs in progress.

**Findings to build on:**
- **Space grown without time** gives rings, rough tangles, stalls or small worlds (A6 C89). That's the baseline a time-ordered model is compared against.
- **2D CDT:** causal growth where space doesn't split is exactly a random tree, dimension 2, once slices are given as lines (A6 C87). **That's a known answer to check against.**

**Cost lessons:**
- time *every* reading before planning a run;
- cost rises steeply with how many links each point may have;
- project from a spread of settings, not the cheapest ones;
- windows update reboots can interrupt overnight runs.

**Working habits:**
- revise and retest;
- write expected results before each run;
- record everything.

## The opening road

| road | question | two parts |
|---|---|---|
| **C: causal growth** | Can a finite-neighbour causal growth rule, where space doesn't split or merge, grow a smooth pattern, **and** do sync and commitment make its slices three-dimensional? | **C1:** with slices given as lines, does ED's causal growth reproduce 2D CDT's known result (a random tree, dimension 2)? That checks the causal machinery against a known answer. **C2:** with nothing built in, do sync and commitment make slices settle at dimension three? |

**Suggested order:**
- **C1 on paper first:** the rule, meaning questions, the known result as expected results, readings.
- **Then a small model.**
- **Then C2.**
