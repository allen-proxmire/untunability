# The 2+1 runs, judged properly: ED looks like the spread-out phase, but the rule says "not settled"

*ED_Attempt_11, note 11. 2026-09-23 (RD15). Ledger: C20. Code `model/st3f_ed.py`, output `model/st3f_ed.txt`. Expectations E0–E3 fixed in the code before running. Written plainly.*

## The short answer

- **ED from a flat start matches the known spread-out phase**, at both sizes, on both readings that worked.
- **ED from a crowded start doesn't match it**, and its numbers jump around rather than settling.
- **By the rule: "ED's starts disagree — still not settled."**
- **But the strongest signal in the run is qualitative and clear: ED never collapses.** The collapsed reference swallows itself into one sheet; ED's runs don't, from either start.

## The numbers

| run | sheet growth rate | mean distance | sheet sizes (16 sheets) |
|---|---|---|---|
| **Size 20** | | | |
| ED, flat start | **0.305** | 4.25 | 317–489 |
| Spread-out reference | **0.282** | 4.35 | 345–485 |
| ED, crowded start | 0.456 | 4.51 | 293–489 |
| Collapsed reference | 0.385 | 4.01 | **7–4,956** |
| **Size 28** | | | |
| ED, flat start | **0.290** | 5.15 | 633–878 |
| Spread-out reference | **0.318** | 5.16 | 674–892 |
| ED, crowded start | 0.204 | 5.95 | 666–892 |
| Collapsed reference | 0.377 | 5.47 | **15–7,386** |

**ED's totals held exactly** at their values in every ED run, and no check failed there.

## What passed and what didn't

| | expectation | result |
|---|---|---|
| **E0** | No check failures below the drop | **As expected.** The only failures are in the collapsed reference, where the engine's check can't run (known, C17) |
| **E1** | The two references differ clearly | **Partly.** On sheet sizes, unmistakably — the collapsed reference has sheets from 7 to 7,386 events, the spread-out one from 674 to 892. On the growth rate, weakly: 0.28–0.32 against 0.38 |
| **E2** | ED matches the spread-out phase from both starts | **No** — the flat start does (0.305 vs 0.282; 0.290 vs 0.318; distances 4.25 vs 4.35 and 5.15 vs 5.16), the crowded start doesn't |
| **E3** | ED's two starts agree | **No** — 0.305 against 0.456 at size 20, 0.290 against 0.204 at size 28 |

**Also recorded:** the spacetime reading gave no number in any of these runs. Sixteen sheets is too few for it at these sizes, so that half of the pass rule couldn't be applied at all.

## What I take from it (labelled, not pre-registered)

1. **ED does not collapse.** That's the clearest difference between the two references, and ED sits firmly on the spread-out side of it, from both starts.
2. **From a flat start, ED's readings sit on top of the spread-out reference** at two sizes. That is what E2 asked for, and it happened.
3. **The crowded start is not converging.** Its rate went 0.456 at one size and 0.204 at the other, which is the behaviour of a run still wandering, not one settled at a wrong value.
4. **Two of the instruments are too weak here.** The spacetime reading gives nothing at 16 sheets, and the growth rate barely separates the two references. The sheet-size profile is the reading that actually discriminates, and it wasn't in the pass rule.

## Options

| | option |
|---|---|
| **(a)** | **Longer runs from the crowded start**, and more sheets (say 32) so the spacetime reading works; keep everything else |
| **(b)** | **Put the sheet-size profile in the pass rule** — it's the reading that separates the two references — and rerun |
| **(c)** | Leave the 2+1 question here and put the effort into road N, which tests ED's own content |

**Default taken (Allen asleep, "go on with your defaults"): (c) for now, with (a) and (b) recorded as the way back.** Road N is the untested part of ED; this run has already shown what it can with these instruments.
