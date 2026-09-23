# Road N, step 2b: passing on to a neighbourhood doesn't help — and two probes say why

*ED_Attempt_11, note 14. 2026-09-23 (RD18). Ledger: C23. Code `model/n2b_descent.py`, output `model/n2b_descent.txt`, data `model/n2_runs/step2b.json`. Expectations N4–N7 fixed in the code header before the run. The two probes at the end are diagnostics, labelled, not pre-registered. Written plainly.*

## The picture, before the numbers

Step 2 (C22) found that ED's grown patterns hold their clocks together but come out as small worlds with no dimension — and that the shape was decided by the **arrival rule** (a new event attaching to a random existing event) before the sync rule got a say.

**Step 2b changes exactly one thing, and it's a change ED already made:** A11 D4, *passing on reaches a neighbourhood*. So a new event attaches to its parent **and to one or two of the parent's neighbours**, instead of hanging off a single event. Nothing else differs.

**Why that might have fixed it:** an event glued into an existing neighbourhood can't create a shortcut between two far-apart parts of the pattern. Arrival stops tearing holes in distance.

**What would have counted as working (N5):** mean distance growing like a **power** of size instead of its logarithm, a defined dimension reading, and the small-world flag clear.

## The result: it doesn't help

| variant | relations per event | ball growth | mean distance, 2k → 4k → 8k | small world? | clocks hold? |
|---|---|---|---|---|---|
| **parent + 1 neighbour, near partners** | 4.6 → 4.8 | 4.42 at 8k | 5.49 → 5.80 → 6.13 | yes | **yes** |
| **parent + 2 neighbours, near partners** | 6.2 → 6.3 | never defined | 4.79 → 5.26 → 5.56 | yes | **yes** |
| **parent + 1 neighbour, partners anywhere** | 4.7 | 4.33 at 8k | 5.21 → 5.67 → 6.19 | yes | **yes** |

- **N4 as expected:** the clocks hold at every size, in every variant.
- **N5 fails in all three.** Mean distance grows with slope **0.08–0.12** against size. Three dimensions needs **0.33**; two needs 0.5; the 3D-grid control gives 0.33 exactly. The small-world flag is set everywhere.
- **N6 fails** (it only applies if N5 holds): where the dimension reading is defined at all it reads 4.3–4.4, worse than step 2's 4.2.
- **N7:** 4.6–4.8 relations per event with one neighbour, 6.2–6.3 with two.

**Gluing into a neighbourhood makes the pattern denser, not more spread out.** Mean distance went *down*, not up.

## Two probes, which say where the problem actually is

*(Diagnostics — single seed, no repeats, no error bars. Labelled as mine. Not claims.)*

### Probe 1: who is allowed to pass on decides the shape, on its own

Same model, but each event may pass on only a limited number of times, then it's spent:

| an event may pass on… | ball growth at 2k → 8k | mean distance growth | what it is |
|---|---|---|---|
| **once** | 0.99 → 0.98 | slope **1.00** | a **chain**. Exactly one-dimensional |
| **twice** | 2.80 → 3.52 | slope 0.16 | in between, and **drifting upward** |
| four times | 3.10 → 3.64 | slope 0.14 | nearly a small world |
| **any number** | undefined → 3.93 | slope 0.08 | a **small world** |

**Reading:** this one rule spans the whole range from a line to a small world. But no setting of it gives a *stable* three — the middle values drift upward with size, which is what a small world looks like before it's large enough to show it. **Three isn't a resting place here; it's somewhere the numbers pass through on the way up.**

### Probe 2: a shape is inherited, not chosen

Whole generations pass on at once, children of neighbouring parents linked to each other — the most faithful reading of D4 I can build. Started from four different shapes:

| started as | ball growth as it grows to ~3,000 events |
|---|---|
| a ring | 1.09 → **1.13** (stays a line) |
| a flat grid | 2.37 → **2.47** (stays flat) |
| a 3D grid | 2.84 → **3.15** (stays 3D) |
| a random web | 2.60 → **3.23** (stays a web) |

**Each one keeps what it started with.** Passing on to a neighbourhood copies a shape forward faithfully. It does not select one.

*(Caveat: the generation rule leaks relations — average relations per event drifts from 4.0 down to about 2.2 — so the numbers aren't clean. The pattern of inheritance is clear regardless.)*

## What road N has established

1. **A6's floor is real and now measured** (step 1, C21): below three dimensions clocks cannot hold together at large size; at three and above they can.
2. **ED's grown patterns do hold their clocks together** — every variant, every size, on fewer relations than ED's own budget allows. That part of ED works.
3. **But holding together doesn't pick three.** Small worlds hold together *more cheaply* than 3D grids, so "fewest relations that still hold" selects a small world. Minimality pushes away from three, not toward it.
4. **And the shape isn't being chosen by ED's rules at all — it's being carried.** Whatever shape a pattern starts with, passing on preserves it. **This is the same wall attempt 10 hit from the other side** (A10 C33: shape set by the start and carried forward, persistence rather than law) — reached now from ED's own clocks instead of from borrowed triangles. Two independent routes, same answer.

**That is a real result about ED, not about borrowed machinery.** It says the missing piece is not sync and not the budget: it is that **nothing in ED says where a new event goes**.

## What is still open — for Allen

**Decisions I took as defaults, which are yours to ratify or overturn:** what "fewest relations" means in practice (I add them where the strain is worst — the choice that most affects the answer); running 2b at all; the bell-curve shape of the rate spread; holding the pull fixed and letting relations vary rather than the reverse; the 6-regular web control in place of note 10's Erdős–Rényi one.

**Meaning questions ED has not answered, in order of how much hangs on them:**

1. **Who may pass on, and when is an event spent?** Probe 1 says this decides the shape by itself. A9 D3 — *commitment is passed on, not held* — reads to me like "an event passes on once, then it's done", but that is my reading of your words, not your decision.
2. **Where does the first shape come from?** If passing on carries a shape, the shape is an initial condition. Does ED claim to make the first one, or only to keep it?
3. **Can a relation ever break?** D12 says they stick. A pattern that only accumulates can never be pushed apart, which limits what shapes are reachable at all.
4. **What is "fewest directions" if not fewest relations?** As tested, it selects a small world. ED has no directions without space, so it needs another meaning or it needs dropping.
5. **Is space the whole accumulated pattern or only the frontier?** I read the whole; your own picture — the lit-up, committed part — may mean the frontier.
6. **What is the 6.7 link budget doing here?** These patterns hold on 3.8. The budget is borrowed from flat geometry (C16), and in this model it never binds.

## Options

| | option |
|---|---|
| **(a)** | **Answer question 1** (who may pass on) and re-run step 2 with it — the probe says it settles the shape on its own, and A9 D3 may already contain the answer |
| **(b)** | **Take stock of road N and attempt 11** — three results are in (the floor measured, minimality selecting small worlds, shape inherited), and they make a coherent statement about where ED actually stands |
| **(c)** | Redo the two probes properly (repeats, seeds, the relation leak fixed) before either of them is leaned on |

**No default taken this time.** (a) and (b) both need your say on what ED means, and the probes have already told us what more computing of the current model would show.
