# Taking stock of attempt 8, in plain language

*ED_Attempt_08, note 12. 2026-09-21 (RD18). Ledger: C51. Reasoning only; nothing computed.*

## What attempt 8 set out to do

Attempt 7 ended stuck: ED's rule for growing space made something that didn't look like space, but every test had been on tiny patches. **Attempt 8's job was to find out whether that was the rule or the patch size.**

## What it did

| | what happened | outcome |
|---|---|---|
| **Built a fast model** | 7× faster, a fraction of the memory, checked three ways against attempt 7 | **Works; it is attempt 7's model** |
| **Pilot run** | 47 minutes, cancelled a 15-hour experiment | **ED cannot collapse** — found on the way |
| **E4: bigger patches** | Patches ten times bigger, 13 runs, then measured at every distance | **Bigger patches are a dead end** |
| **Road 3: one history or many** | A conversation, no compute | **Two decisions of Allen's** |
| **Road F: whole-slice sync** | Sync as Allen means it, measured properly | **Grown slices can't hold a common "now"** |

## The findings, one line each

1. **ED cannot collapse.** The link budget and the no-infinities rule each forbid the crumpled state. In the rival theory that state is half of what blocks smooth spacetime; ED doesn't have it. *(C22)*
2. **ED's space changes character with distance.** Stringy up close, opening out further away. Every earlier number was the narrowest point of that curve. *(C36)*
3. **Bigger patches cannot settle the shape.** Ten times the volume bought 26% more reach; doubling the reach would take about 943 times the volume. That's a wall, not a compute problem. *(C37)*
4. **Sync had drifted.** It became a veto on single moves through three modelling steps, none of them decided. Allen: sync means a whole slice agreeing. *(D10, C32)*
5. **ED's past is a set of possibilities.** Allen: once something happens it's fixed, but many things could have happened; the present doesn't know its own past. ED has been an ensemble theory all along. *(D11, D12)*
6. **ED's ensemble can't cancel.** Its weights are all positive, so it lands on whatever shapes are most numerous — and stringy shapes vastly outnumber smooth ones. The Born rule, one of ED's three inputs, has the machinery that cancels; the growth model doesn't use it. *(C41, Claude's reading)*
7. **Grown slices can't hold a common "now".** With the veto they fail at every size, identically. Without it they are better but show no pass. Fixing sync's form isn't enough. *(C48–C50)*

## What still stands from before

**Budgeted Causality** (the balance coming out of a conserved budget) and **Synced Now** (the reason for three dimensions from clocks agreeing). Neither is about growing the pattern, so nothing in attempt 8 touches them.

## The census

**Inputs supplied: still 3.** Nothing derived. No new number, nothing measurable. One knob redefined: the sync threshold now uses a median over eight seeds, because the old single-seed version wobbled by 23%.

## The walls

| | wall | end of attempt 7 | now |
|---|---|---|---|
| **1** | **Rest frame** | A risk, with a large-scale frame coming out of sync | **Unchanged** |
| **2** | **Dark sector** | Untouched | **Untouched** |
| **3** | **Growth** | ED's rule runs "crumpled to branched" with no flat middle | **Sharper and narrower.** ED can't crumple at all; the rule makes compact, stringy patterns at every reachable size; bigger sizes can't change that; and the patterns can't carry a common "now". **The wall is now about the *kind* of rule** — local, step by step, positive weights — not its settings |
| **4** | **Numbers** | Inherited | **Unchanged**; one knob redefined |
| **5** | **Handle-free rule** | Chosen | **Untouched** |

## What it cost

| | |
|---|---|
| **Compute** | about **40 hours** |
| **Ledger** | 50 claims, 15 of Allen's decisions, 17 recorded steps, 12 notes |
| **Claude's errors** | **15 in code or specification**, all caught by a test or a guard before reaching a result; **2 in reasoning** — calling E4 "clear and negative" before checking the measurement windows (C35), and mixing up two kinds of scaling exponent (C47), caught by the calibration |

## Where this leaves ED

**Every tweak to the growth rule has now been tried at the scale where it could show.** Settings, size, sync's form. The same result keeps coming back, and it comes back identically at every size.

**That points past the settings to the kind of rule.** Three possibilities are left, and each is a meanings question before it is a model:

| | road | the question |
|---|---|---|
| **2** | **The local costs** | Commitment (α·E) and curvature (an edge sum) are local sums that arrived the same way sync did. Do they mean what ED means? |
| **G** | **Amplitudes in growth** | Should ED's growth carry weights that can cancel — its own Born rule doing work — instead of probabilities? |
| — | **The one open measurement** | A finer measuring ladder would probably make road F's controls readable. Small, and deliberately not done without Allen's say |

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Conclude attempt 8 and open attempt 9 on the kind of rule**, starting on paper with road 2 and road G | Attempt 8's question — is it the rule or the size? — is answered: it's the rule. The next question is a different kind, about what ED's growth *is*, and deserves a clean ledger |
| **(b)** | **Stay in attempt 8** and take road 2 on paper | Cheap, and the same audit that fixed sync |
| **(c)** | **Run the finer ladder** on road F's controls first | Closes the one open measurement; small |
| **(d)** | **Pause** | Nothing in the record needs finishing |

**Proposal: (a).** Attempt 8 answered what it was opened to answer, and the answer points somewhere new.
