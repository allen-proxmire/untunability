# H4: mostly one child — flat space still collapses, even with almost nothing happening

*ED_Attempt_09, note 9. 2026-09-21 (RD11). Ledger: C34–C38. Run `model/h4_run.py`: four runs at n = 24, 150 ticks, 13 minutes. Expectations fixed before running (C35). Written plainly.*

## What was run

Your decision (D11): **an event has mostly exactly one child.** 90% of events have exactly one; 10% use the old spread. Churn fell from about 50% of each slice per tick to **about 6%**. Growth otherwise used only ED's conditions — no costs, no veto.

## The results (C36)

**Average distance between points** (flat space: 11.49), tracked every 10 ticks:

| run | start | rewiring moves | tick 0 | 10 | 20 | 30 | 50 | 100 | 150 |
|---|---|---|---|---|---|---|---|---|---|
| **F1** | flat | on | 11.49 | **6.74** | 5.82 | 5.49 | 5.13 | 4.73 | **4.55** |
| **F2** | flat | on | 11.49 | **6.61** | 5.85 | 5.49 | 5.07 | 4.75 | **4.53** |
| **F0** | flat | **off** | 11.49 | **7.16** | 6.12 | 5.77 | 5.35 | 5.09 | **4.94** |
| **W1** | small world | on | 4.43 | 4.49 | 4.49 | 4.41 | 4.43 | 4.41 | **4.34** |

**Spacetime** (flat 3.61; within 0.5 reads 3+1): F1 **5.02**, F2 **5.01**, F0 **5.09**, W1 **5.26** — **none reads 3+1.**

Structure and both budgets exact in every run; about 5.7% of events merged per tick, as designed.

## What it shows

**1. Flat space collapses within about 20 ticks — even with only 6% of the slice changing each tick.** The average distance falls from 11.5 to about 6 in the first 20 ticks, and settles at about 4.5–5. **Lowering the churn barely slowed it.**

**2. It isn't the rewiring moves.** F0 — rewiring moves switched **off**, only rare births and deaths — collapses almost as fast (7.2 after 10 ticks, 4.9 at the end). **I expected F0 to stay flat. It didn't.** That expectation was wrong.

**3. From a small world, it stays a small world.** W1 sat at about 4.4 the whole way. **Nothing brings it back.** That part I did expect.

## What that means (C37)

**The churn wasn't the problem. Any random local change, however rare, drifts toward the small world.**

Think of a tidy room. It doesn't matter whether things get moved around fast or slowly — if they're moved at random, the room ends up messy, because there are vastly more messy arrangements than tidy ones. **Slowing the mess down only changes how long it takes.**

Each birth or death reconnects a few neighbours. Nothing prefers the flat arrangement over the countless crammed ones, so random reconnection wanders into them — fast.

**This is the cleanest statement of the wall yet:**

> **The problem isn't how much ED's growth changes each tick. It's that nothing in ED's growth prefers an extended shape. Any random change at all — even rare, even without rewiring moves — turns flat space into a small world within a few dozen ticks, and nothing turns it back.**

**Your decision still did something useful.** Slices now persist from tick to tick instead of being mostly rewritten. That removes the reason selection couldn't accumulate in S0 (C32). **A preference now has something to build on** — which it didn't before.

## A side effect to record (C38)

With 90% of events having exactly one child, **Budgeted Causality's pull toward balance is ten times weaker**. The slices shrank to about **83%** of their starting size with the rewiring moves on (97% with them off), where attempt 8's held within a few per cent. The balance point is unchanged; only the pull back toward it is weaker. Worth watching: a gentler balance is still a balance, but it drifts further before correcting.

## Where this leaves road H

| | tried | result |
|---|---|---|
| **H1** | remove the costs | slices feel 3D up close; still small worlds |
| **H2** | judge the spacetime | the shortcuts spoil it too |
| **H3 S0** | pick the best each tick | nothing accumulated — too much churn |
| **H4** | mostly one child | churn gone, **but flat still collapses; nothing brings it back** |

**Every road ends at the same place: nothing in ED's growth prefers an extended shape.** H4 removed the one obstacle that stopped a preference from working.

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Rerun the best-of-8 check at mostly-one-child** | Minutes to run. S0 failed because churn erased every gain; the churn is now gone. **If picking the best now accumulates and climbs toward flat, whole-history weighting becomes workable** |
| **(b)** | **Take stock of road H** | Four results that all point at the same wall; a good moment to see them together |
| **(c)** | **Amplitudes (H2a)** | The one remaining mechanism that doesn't need a tuned preference |

**Proposal: (a).** It's cheap, and it's the direct test of whether your decision unlocked anything.
