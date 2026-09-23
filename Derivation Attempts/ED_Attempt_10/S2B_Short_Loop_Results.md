# Short-loop test: frozen too, and why

*ED_Attempt_10, note 18. 2026-09-22 (RD19). Ledger: C31, D17. Code `model/sb_short.py` (outcomes in its header, fixed before running), output `model/sb_short.txt`; a labelled diagnostic afterwards. Written plainly.*

## The short answer

**Frozen, by the rule.** Even with only 4 slices round the loop, neither start moved at large scale in 1,000 passes. The gap between them was **2.18 at the start and 2.18 at the end.** No check failed.

**So the loop length wasn't the problem. The program's moves themselves can't carry a whole history anywhere** at this rate.

## The results

| start | average distance, start → end | unevenness of neighbour counts | changes accepted |
|---|---|---|---|
| **Flat** | 5.84 → 5.82 | 3.19 → 3.20 | 20% |
| **Crowded** | 3.66 → 3.64 | 15.33 → 15.33 | 7% |

**My expectation** (that they'd move or meet) **was wrong.**

## Why (a diagnostic afterwards, labelled — not a pre-planned test)

After 40 passes, I compared every slice with where it started:

| start | links changed from the start | average change in neighbour count | flips done |
|---|---|---|---|
| Flat | about **1.3%** | 0.1 | **none** |
| Crowded | about **0.7%** | 0.08 | some |

**What that shows:**
1. **Lots of changes happen, but they're short-lived.** A change gets made in one slice and undone in the next. Every slice stays a small cloud around the same shape. The ticks fill with these back-and-forth changes (about 100 per tick), because counting rewards having many of them.
2. **For the whole history to move, every slice has to shift together.** Each slice can only differ from its neighbours by 10%, and the program moves one slice at a time. So the history's overall shape wanders extremely slowly.
3. **From the flat start, no flips happened at all.** Flat slices have no spot for a link-removing flip, and the mixed bundles that could create one never came up. So flat histories could only split and merge. **A narrow split or merge never changes the neighbour count of the two events at the ends of the link** — only the events around it change, by one each. That makes reshaping very slow.

## What it means

**The question is still open, but the reason is now clear:** with mostly one child and a 10% limit per tick, a history is very stiff in time. Counting fills each tick with brief back-and-forth changes, while the overall shape just rides along from wherever it started.

**That's partly a finding about ED, not just the program:** under your rules, **a slice's large-scale shape is extremely persistent.** Whatever shape a history has, it keeps it for a very long time. That's persistence, not a choice between shapes.

## Options (you decide)

| | option | what it tells us |
|---|---|---|
| **(a)** | **Add a "whole-history" move:** apply the same change to every slice at once. It's a standard way to speed up exactly this kind of slow, collective motion, and it keeps the counting exact. I'd check it on rings exactly first (as G1), then rerun the short and long loops. **A few hours** | Lets the history's overall shape actually move, so the two starts can meet — **and where they meet answers stage B's question** |
| **(b)** | Take stock of road S and attempt 10 now | The tools work; one-tick counting under narrow moves favours flat; whole-history counting is stuck at this speed |

**Proposal: (a)** — it's the step that can actually answer the question. If it still doesn't move, (b).
