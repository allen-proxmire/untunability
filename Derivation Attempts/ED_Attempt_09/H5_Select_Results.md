# H5: picking the best still doesn't build up — even with slices that persist

*ED_Attempt_09, note 10. 2026-09-21 (RD12). Ledger: C39–C41. Run `model/h5_select.py`: two runs at n = 24, 100 ticks each, 25 minutes. Pass rules fixed before running (C39). Written plainly.*

## What was run

Each tick, grow **eight** possible next slices and keep the one with the **fewest directions** (the largest average distance between points). This time with **mostly one child** (D11), so slices hold together from tick to tick — the thing that stopped S0 from working.

## The results (C40)

**Average distance between points** (flat space: 11.49):

| run | start | picking the best: start → end | ordinary run at the end | gain | gap to flat closed |
|---|---|---|---|---|---|
| **B-W** | small world | 4.43 → **4.45** | 4.41 | +0.03 | **0%** |
| **B-F** | flat | 11.49 → **4.80** | 4.73 | +0.07 | **1%** |

**Neither passes** the rule fixed beforehand (a rising trend over the last 50 ticks *and* ending more than 1.0 above the ordinary run). Both trends are flat or slightly downward.

- **From a small world, picking the best didn't climb at all.** It wandered around 4.4–4.6 for 100 ticks.
- **From flat space, picking the best didn't even slow the collapse.** Tick 10: 6.80 against the ordinary run's 6.74. Tick 100: 4.80 against 4.73.
- **Spacetime:** 5.30 and 5.05 against flat's 3.61. Neither reads 3+1.
- **The stringy risk didn't happen.** The end slices' strain (9.2–9.6) is small-world, not stringy.

## Why (C41)

**Picking one of eight is a very weak push, and the pull toward the small world is strong.**

Each tick, the eight candidates differ only by the few changes that tick made, so the best of them is only a little better than the rest. Meanwhile, **every random change pulls toward the crammed arrangements**, because there are so many more of them. The small gain from picking is cancelled by the pull back — every tick.

**The strength needed grows with the size of the slice.** The number of crammed arrangements grows with the slice, so a push strong enough to hold a slice flat has to grow with it too. Picking one of eight is fixed; it can't keep up. **That is exactly the "strength" problem from H3** (C25): a preference only beats entropy if its strength is large and grows with size — which is what CDT gets by tuning a coupling in a weighing over whole histories.

## Where road H now stands

| | tried | result |
|---|---|---|
| **H1** | remove the costs | slices feel 3D up close; still small worlds |
| **H2** | judge the spacetime | the shortcuts spoil it too |
| **H3 S0** | pick the best, old churn | didn't build up — churn erased it |
| **H4** | mostly one child | churn gone, but flat still collapses and never returns |
| **H5** | pick the best, low churn | **still doesn't build up — entropy outpulls a weak preference** |

**Five results, one wall:** nothing in ED's growth prefers an extended shape, and a *weak* preference can't overcome the count of crammed shapes. **What's left needs a *strong* preference that grows with size** — tuned (as CDT does) or set by ED itself (as the budget sets size).

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Take stock of road H**, and probably of attempt 9 | Five results agree; the next step is a different kind of work, and the choice between them is yours |
| **(b)** | **Build a proper weighing over whole histories with a tuned strength** (CDT's route, "route i") | Tells us whether *any* strength gives 3D space. A real build — days — and it adds a tuned setting |
| **(c)** | **Route (ii) on paper:** is there something ED conserves that would set the shape's balance by itself, as the budget sets its size? | The ED-shaped hope, and the most important open question. No design exists yet |
| **(d)** | **Amplitudes (H2a)**, or **roads R and I** | Different questions altogether |

**Proposal: (a).** The road has answered its question clearly, and what comes next is a choice of direction rather than another test.
