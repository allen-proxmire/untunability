# H3: weighing whole histories (on paper)

*ED_Attempt_09, note 7. 2026-09-21 (RD9). Ledger: C23–C28. **A specification only: nothing run.** Allen decided (D9): **ED weighs whole histories.** This note works out what that means for the model, using only meanings already decided, and marks every new setting it would need. Questions H3-Q1–H3-Q6 are for Allen. Written plainly.*

## What changes

**Until now:** grow one history forward, one tick at a time, and keep it. The past is never revisited.

**Now:** consider **many whole histories** (every slice from the start to the end) and **weigh them against each other.** A history that fits ED's meanings better counts for more. What we measure is what the *weighted collection* of histories looks like, not what one lucky run happened to do.

**This is how causal dynamical triangulations works** (C16), and your D11–D12 ("many could have happened", "the present doesn't know its own past", "you can undo history") say it's what ED means too.

## 1. What a history is (C23)

**A history is the whole spacetime**: slices at ticks 0 to T, each linked forward to the next — every event to its children, or to whatever absorbed it. **Every history must satisfy the conditions that work** (C2):

- slices never split or merge;
- the budget is passed forward and conserved;
- the link budget is conserved;
- no event has more than 60 neighbours.

**Nothing here is new.** These are the rules the model already enforces.

## 2. What the weight is — built from meanings already decided (C24)

**There are two things to put in the weight.** Both come from attempt 6.

### The floor: rates can match across the whole pattern

That's your D5. It rules out patterns so thin and stringy that clocks can't keep in step (below two dimensions).

**But sync alone can't be what sets the shape — it likes shortcuts.** Attempt 6 recorded this (A6 C22): *sync alone favours small worlds.* Clocks keep in step most easily when everything is close to everything. That's also standard network science: small-world networks synchronise more easily. **So sync is a floor, not a shaper.** It stops strings; it doesn't stop shortcuts.

### The preference: the fewest directions

Attempt 6's lead for why three (A6 D6): **growth favours as few directions as possible, while rates can still match.** Sync says "at least more than two"; fewest directions says "no more than you need". **Between them: three.**

**Shortcuts are exactly "too many directions."** A small world behaves like a space of very high dimension — H1's measured roughly seven. **"Fewest directions" is the one ED meaning that pushes against shortcuts.**

**And it's commitment's proper home.** Attempt 6 noted *maximal commitment favours a single chain* — the fewest directions possible (A6 C23). In attempt 7 that became a cost per link (α·E); H1 dropped that cost because the link budget already expresses "passed on" (H1-Q1). **What was lost with it was the "fewest directions" part** — and that part belongs on whole histories, not single moves.

> **Proposed weight, from decided meanings only:** among histories that meet the conditions and in which rates can match across the whole pattern, **favour those with the fewest directions.**

## 3. The honest problem: every preference needs a strength (C25)

**"Favour fewest directions" needs a number saying how strongly.** Too weak, and entropy wins — small worlds, as now. Too strong, and the pattern collapses to strings. **Somewhere between is a balance — and in CDT that balance is found by tuning a setting to a critical value.**

**That's exactly what ED avoided for size.** Budgeted Causality — ED's strongest result — got the size balance **without tuning**, by conserving a budget instead. *What CDT tunes, ED conserves.*

**So there are two ways forward, and they're very different:**

| | route | what it is |
|---|---|---|
| **(i)** | **Tune the strength**, as CDT does | A new setting, counted by the census guard. A **scan** tells us whether any strength gives three-dimensional space. Doable now |
| **(ii)** | **Find what conserves it**, as Budgeted Causality did for size | Is there a conserved quantity in ED that sets the shape balance by itself? **A research question — no design exists yet.** If found, it would be the most important result this project could produce |

**Recommendation: (i) as a test, while keeping (ii) as the real goal.** If no strength gives three-dimensional space, (ii) is moot. If one does, the question becomes whether ED can find it by itself.

## 4. Two more things the weight needs pinned down (C26)

**The floor has no teeth at the model's current settings.** Your bounded pull (A6 D7) is what stops clocks locking when rates differ too much. But the model's clock-rate spread is **a thousand times smaller** than what the pull can handle, so **every connected slice passes** — the floor never bites. Attempt 7 hit this too (A7 C92). **To make the floor mean something, the rate spread has to be large enough that the pull's limit matters.** That spread is a setting that already exists; its value would change.

**"Curvature bounded below" means every connection, not the middle one.** The theorem attempt 6 took it from requires a bound on the *lowest* curvature. H1 tested the middle value; about 5% of H1's connections sit at the tree-like −0.5. **As a condition, the bound is a number — a setting.**

## 5. How to actually weigh whole histories (C27)

| | method | true to D9? | cost |
|---|---|---|---|
| **S0** | **Feasibility check on existing data:** do H1's grown histories vary at all in "number of directions"? If every one is equally a small world, weighting has nothing to choose between | — | minutes |
| **S1** | **Rewind and regrow.** Pick a tick, throw away everything after it, regrow from there, and keep the new future if it scores better (by the weight), or sometimes even if worse. Repeat thousands of times | **Yes** — it weighs whole histories, and it's the model doing what D12 says: undoing history | hours to days; short histories at small size first |
| **S2** | **Change the spacetime anywhere, CDT-style** | Yes | a new model, days to build |

**S1 is the natural first step.** It reuses the fast model entirely: the growth rule becomes the way new futures are *proposed*, and the weight decides which histories count. Done correctly, it samples exactly the weighted collection of histories.

## 6. What counts as a result, fixed now

**Judged on the spacetime**, as A7 D40 decided, against the calibrated flat spacetime (3.61 medium, 3.67 larger; C20):

| outcome | what it records |
|---|---|
| **Some strength gives a spacetime within 0.5 of flat** | **ED's meanings, weighed over whole histories, can give three-dimensional space** — with one tuned setting, counted by the census guard. Then route (ii): can ED find that strength itself? |
| **No strength does** | **Fewest directions, over whole histories, isn't enough.** Amplitudes (H2a) return, and the meanings need another look |
| **S0 shows no variation** | Weighting can't work at these sizes; recorded plainly before spending anything more |

## Questions for Allen

| | question | proposed default | why |
|---|---|---|---|
| **H3-Q1** | **The weight: histories meeting the conditions, with rates able to match across the pattern (the floor), weighted toward the fewest directions (the preference)?** | **Yes** | Every piece is already decided (A6 D6, D7; D5); nothing is invented |
| **H3-Q2** | **"Fewest directions" is commitment's proper form** — a preference over whole histories, not a cost per link? | **Your call** | It reinterprets commitment; H1 dropped the per-link cost, this would restore the part that was lost |
| **H3-Q3** | **Tune the preference's strength as a scan** (route i), labelled as a new setting, while treating route (ii) as the real goal? | **Yes** | The only way to learn whether any strength works |
| **H3-Q4** | **Give the floor teeth**: raise the clock-rate spread so your bounded pull actually limits locking? | **Yes** | Otherwise the floor is decorative; the setting already exists |
| **H3-Q5** | **Curvature bounded below applies to every connection**, with the bound as a setting? | **Yes** | That's what the theorem requires |
| **H3-Q6** | **S0 first, then S1 (rewind and regrow)** on short histories at small size | **Yes** | Cheapest honest path; S0 can stop it for minutes' cost |

## The census, stated plainly

**This adds up to three settings:** the preference's strength, the curvature bound, and a larger clock-rate spread (a changed value, not a new setting). **Inputs supplied: still 3.** If route (i) works, the honest record is *"three-dimensional with one tuned strength"* — worse than Budgeted Causality, which tuned nothing. **Route (ii) is what would make it ED's.**
