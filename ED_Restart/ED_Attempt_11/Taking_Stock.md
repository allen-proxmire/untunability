# Taking stock: road N and attempt 11

*ED_Attempt_11, note 15. 2026-09-23 (RD19). Ledger: C24. Reasoning only; nothing computed. Written plainly.*

## The one-paragraph version

Attempt 11 asked what one tick is, built ED's tick as a layer, and found by exact algebra that **ED's budgets fix all three numbers CDT has to tune by hand** — the strongest thing the project has. It then checked the instrument against published CDT and passed. Then you challenged the whole frame: ED doesn't need space, it's a network of events and rates. The audit agreed — every model since attempt 7 had kept ED's budgets and thrown away ED's clocks. So road N rebuilt ED with clocks and no geometry at all, and found: **ED's clocks really do hold together, cheaply; but nothing in ED's rules chooses a shape. A shape is carried, not made.** Attempt 10 found the same thing from the opposite direction. That agreement is the real product of the last two attempts.

## What attempt 11 established

### Road L — ED's tick as a layer

| | finding |
|---|---|
| **The strong one (C5)** | In 3+1, CDT has three free totals and tunes them. ED's conserved budgets fix two, and conserving forward links fixes the third: **N1T = 2N0 + N32/2**. So ED sits at **one point** of CDT's map with nothing tuned. Exact algebra, not a simulation |
| Placement, 3+1 (C7) | ED's ratio N32/N41 = 1.00 against CDT's standard working point 1.26. Close, not equal |
| Placement, 2+1 (C8) | ED lands at τ = 1/3, which is **inside** the extended phase — the phase where space doesn't collapse |
| The instrument (C17) | The program run as plain CDT reproduces the published behaviour: a steady fall then a sharp drop, and collapse above it. **It passed.** It also corrected us: the extended phase reads 0.22–0.29 on our slice measure, not 0.5, so our earlier pass rule had been testing the wrong thing |
| ED's 2+1 runs (C20) | **ED never collapses.** From a flat start its readings sit on top of the extended reference at both sizes; from a crowded start they wander. By the rule: starts disagree, not settled |

### The audit (C16)

The model we had been testing kept ED's budgets and conditions, borrowed the substrate, the moves and the layer, and contained **none of ED's clocks, rates or sync** — including attempt 6's Synced Now, the one result that ever got three dimensions out of ED's own content. Your challenge was right, and it changed the direction of the attempt.

### Road N — ED with clocks and no geometry

| | finding |
|---|---|
| **Step 1 (C21)** | Attempt 6's floor, **measured** rather than argued: the line and the flat grid can never hold their clocks together as they grow; the 3D grid and the web hold at a pull that doesn't rise at all. The instrument passed on all four known shapes |
| **Step 2 (C22)** | ED's grown patterns **do** hold their clocks together — at every size, on 3.5–3.8 relations per event, *below* ED's own budget of 6.7. But they are small worlds with no dimension, sitting on the random-web control rather than the 3D grid |
| **Step 2b (C23)** | Passing on to a neighbourhood (D4) doesn't help: still a small world, and denser rather than more spread out |
| **Probe 1** | Who may pass on spans the whole range on its own — once gives a chain, any number gives a small world — and **nothing in between is stable at three** |
| **Probe 2** | A shape is **inherited**: a ring stays a ring, a flat grid stays flat, a 3D grid stays 3D, a web stays a web |

## The finding that matters: two routes, one answer

**Attempt 10** (borrowed triangles, counting whole histories): every history stayed at its start, flat and crowded, long loops and short, with and without whole-history moves. Reading kept: shape is set by where a history starts and carried forward — persistence, not law.

**Attempt 11** (ED's own clocks, no geometry anywhere): whatever shape a pattern starts with, passing on preserves it.

**Different machinery, different assumptions, opposite starting points, same answer.** When two roads that share almost nothing land on the same place, that place is probably real.

## What this says ED is, and is not

**What ED does, on the evidence:**
- Its budgets **fix** what CDT tunes. That is a reduction in free numbers, and it is exact.
- Its sync condition is **real and measurable** — below three dimensions clocks cannot hold together at large size.
- Its patterns **hold together cheaply**, on fewer relations than its own budget allows.
- It **keeps a shape** once there is one. Commitment that sticks is what buys that.

**What ED does not do, on the evidence:**
- It does not **make** three dimensions. Sync rules out one and two; "fewest relations" then selects a small world, not a 3D lattice.
- It does not say **where a new event goes**, and that is the thing that decides the shape.
- So it does not derive space. It carries space.

## The honest cost, under the census guard

If "ED explains why a shape persists" becomes the claim, then **the shape itself becomes a supplied input** — a fourth, alongside the three you already supply. ED's input list would **grow, not shrink.** By the census guard that is not a reduction, and it should not be written up as one.

Set against that, the one genuine reduction still stands: **ED's budgets fix three numbers CDT tunes, with no new free numbers.** That claim survived the audit and everything since.

## What attempt 11 cost, and what I got wrong

Roughly 15–20 hours of computing, 15 notes, C1–C24, D1–D13, RD1–RD19, and two programs (the compiled 2+1 sampler, about 60× faster in accepted moves; and the road N model).

Mine, all recorded before their results: the counterweight tuning that froze run 1; comparing the two samplers at equal sweeps instead of equal accepted moves; a wrapper that didn't seed the engine; the pass rule that tested smooth slices instead of extended spacetime (caught by the instrument check); an Erdős–Rényi web with stranded events reported as "can't lock"; adding relations between random pairs and calling it "fewest"; and a linear feasibility test that passed patterns the full dynamics rejected.

## What is still open

**Meanings ED hasn't settled** (from note 14): who may pass on and when an event is spent; where the first shape comes from; whether a relation can ever break; what "fewest directions" means if not fewest relations; whether space is the accumulated pattern or the frontier; what the 6.7 budget is doing when patterns hold on 3.8.

**Carried, untouched:** the two 2+1 options (32 slices and longer crowded runs; the slice-size profile in the pass rule); roads R, I and D; amplitudes; A9's H3-Q2; A10's flagged flip-pairing reading (D15).

**Not yet done properly:** both probes are single-seed diagnostics, and the inheritance probe leaks relations as it grows.

## Options

| | option |
|---|---|
| **(a)** | **Conclude attempt 11 and open attempt 12 on persistence** — make "ED keeps a shape and keeps it sync-able" the thing being tested, state plainly that shape is then a fourth input, and open with the one configuration road N never tried: spent events, generation-wise growth, and the sync filter all running together. That test is also the sharpest test of persistence, so it serves both purposes |
| **(b)** | Conclude attempt 11 and open attempt 12 on **who may pass on**, treating it as a meaning question first and a test second |
| **(c)** | Keep attempt 11 open and run the untested configuration now, before concluding anything |
| **(d)** | Conclude attempt 11 and pause |

**Proposed: (a).** It is the only option where the last two attempts add up to a single statement instead of two failures, it names the cost honestly, and its first test is one we have not run.
