# Road P: the filter erases every shape — including the one we wanted kept

*ED_Attempt_12, note 4. 2026-09-23 (RD6). Ledger: C5. Code `model/p_persist.py`, output `model/p_persist.txt`, data `model/p_runs/roadP.json`; run 1 invalid and archived (C4). Expectations P0–P4 fixed in note 3 before any code. The pull check at the end is a diagnostic, labelled, not pre-registered. Written plainly.*

## The short answer

**Persistence is not what ED gives.** Once the sync requirement is actually switched on, a pattern does not keep its shape — it **loses it completely**, and every starting shape ends up in the same place.

**That place is a small world, not three-dimensional space.**

By note 3's own table this is the second outcome: *the filter bites, but it overshoots — ED destroys everything, the shape we'd want kept included.*

## The numbers

**With the filter on**, at about 8,000 events, three seeds each:

| start | was | ends at | mean distance | relations per event | relations the filter added |
|---|---|---|---|---|---|
| **ring** | 1.0 | **4.2** | 500 → 5.8 | 2.0 → 6.2 | 7,019 |
| **flat grid** | 1.85 | **4.0** | 22.5 → 6.0 | 4.0 → 6.3 | 4,681 |
| **3D grid** | 2.36 | **3.8** | 9.7 → 6.3 | 6.0 → 6.9 | 2,125 |
| **web** | no dimension | **4.2** | 4.6 → 5.7 | 6.0 → 6.8 | 1,884 |

**All four converge.** Same reading, same mean distance, same relation count, from starts as different as a line and a random web. **The pattern forgets where it came from.**

**With the filter off** (the control):

| start | ends at | against the same shape at that size | keeps its shape? |
|---|---|---|---|
| ring | 1.01 | 1.00 | **yes** |
| flat grid | 2.28 | 1.93 | no — drifts up by 0.35 |
| 3D grid | 3.20 | 2.69 | no — drifts up by 0.51 |
| web | 3.91 | none | — |

## What passed and what didn't

| | expectation | result |
|---|---|---|
| **P0** | The 3D grid and the web hold their clocks at every generation | **As expected** |
| **P1** | The line and the flat grid don't survive as themselves | **True — but the rule voids it.** The flat grid drifts upward in the control arm too, and note 3 said that voids P1. **The ring case is clean, though:** kept at 1.01 with the filter off, destroyed to 4.2 with it on. The line's destruction *is* the filter's doing |
| **P2** | The 3D grid survives as itself | **No.** It goes to 3.82 with the filter and 3.20 without, against 2.69 for a real 3D grid that size |
| **P3** | Relations per event, reported | 6.2, 6.3, 6.9, 6.8 — see the check below |
| **P4** | With the filter off, all four keep their shapes | **No.** Only the ring does |

## The thing I have to take back

**Two hours ago I called "a shape is carried, not chosen" the finding of record.** This run says otherwise. That finding was measured with the sync requirement switched *off*. Switch it on — which is what ED actually asks for — and shape is not carried at all. It is **erased**, in every case, and replaced by the same end state.

The two-route agreement between attempt 10 and attempt 11 still stands as a statement about *counting and inheritance without sync*. It does not stand as a statement about ED.

## The check that didn't clear

Relations per event settled at 6.2–6.9, and **ED's own link budget is 6.699** — a number derived from flat geometry in attempt 7 and never given to this model. That looked like the most interesting thing in the run, so it got tested rather than reported.

**The test:** the same growth at pulls of 0.5, 1 and 2. If the settled number is a property of ED rather than of my setting, it shouldn't move.

| pull | relations per event |
|---|---|
| 0.5 | **9.60** |
| 1.0 | 6.21 |
| 2.0 | 5.94 |

**It moves.** The match with 6.699 is a consequence of my having set the pull to 1, and it is not claimed. *(Recorded, not leaned on: the number flattens above a pull of 1 — doubling the pull moves it only 6.21 → 5.94. One seed, three points.)*

## What road P has established

1. **ED does not keep a shape.** With its own sync requirement enforced, every shape is destroyed, including three-dimensional ones.
2. **What it does instead is converge.** Four very different starts reach the same end state — which is a stronger and more surprising property than persistence, and it *is* ED's own doing. But the end state is a small world with no dimension.
3. **Local repairs don't save it.** The filter was restricted to adding relations between events already within three relations of each other — the least shape-destroying repair available. Seven thousand local repairs still destroy a line's shape entirely.
4. **The question road P was opened to answer is answered, negatively.** Persistence was the one statement two attempts agreed on, and enforcing ED's own sync rule dissolves it.

## What's left

**One live lead, from Allen's reading of ED's inflation language** (*"event-structure complexity outpacing event-production capacity"*, ED-Orientation, the ED-08/00.1 cosmology summary — his own phrasing was close, with the two terms swapped):

The knob that moved attempt 11's readings from a chain, through about three, to a small world is exactly the **ratio of event production to relation production**. Every setting of it drifted upward with size. **Is there a ratio at which the reading stops drifting?** That's a balance point, and it's a sharp question rather than a story: it either exists or it doesn't.

**Its honest cost, if it exists:** unless ED supplies the ratio from something it already says, tuning it to land on three is a dial, and by the census guard that is not a derivation.

## Options

| | option |
|---|---|
| **(a)** | **Take stock of road P** — it's answered, and the answer changes what attempt 11 concluded |
| **(b)** | **Test the balance point** — scan the ratio of event production to relation production and look for the one value where the reading stops drifting with size |
| **(c)** | Ask what else could stop the filter from overshooting — the filter as built can only add relations, because relations never break (D2 P-Q5). A rule that let a relation lapse is the obvious missing piece, and it is a meaning question for Allen |

**No default taken.** (b) is the live lead and (c) is a meaning only Allen can settle.
