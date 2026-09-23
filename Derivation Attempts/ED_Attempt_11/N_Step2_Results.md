# Road N, step 2: ED's patterns hold their clocks together — and they are not three-dimensional

*ED_Attempt_11, note 13. 2026-09-23 (RD17). Ledger: C22. Code `model/n2_grow.py`, output `model/n2_grow.txt`, data `model/n2_runs/step2.json`. Expectations N1–N3 fixed in note 10 before any code; two revisions recorded in the code header before the run. Written plainly.*

## The picture, before the numbers

**What was built:** a pattern of events, each with its own ticking rate, and relations between them. **No sheet, no triangles, no coordinates, no dimension anywhere in the rules.** Events arrive one at a time, each bringing a single relation to an existing event. After each batch, relations are added **only while the clocks can't hold together, and stopped the moment they can** — ED's "fewest directions", made exact.

**What was read afterwards:** how fast balls grow (the dimension reading), how fast the relations crossing a patch's edge grow with the patch, how mean distance grows with size, and whether the pattern is a small world.

**What the outcomes would mean** — fixed in note 10:
- **readings near 3** → ED's own rules make three-dimensional space, with nothing geometric assumed. The result the project has been after.
- **readings near 4 or higher, or a small world** → holding clocks together doesn't hold a pattern *down* to three; something else must.
- **can't hold together at all** → Synced Now doesn't carry over to grown patterns.

## The short answer

**The middle one, unambiguously.**

- **ED's grown patterns do hold their clocks together** — at every size, at a fixed pull, with room to spare. **N1 as expected.**
- **They carry 3.5 to 3.8 relations per event** — comfortably *below* ED's own link budget of 6.7. **N3 reported.**
- **They are small worlds with no definable dimension.** Ball growth reads 4.0–4.2 and *rises* with size; mean distance grows like the logarithm of size, not its cube root. **N2 fails.**

## The numbers

| pattern | relations per event | ball growth | patch-edge exponent | mean distance | small world? | clocks hold? |
|---|---|---|---|---|---|---|
| **ED, 2,000 events** | 3.56 | — | — | 5.81 | yes | **yes** |
| **ED, 4,000** | 3.74 | 4.03 | 0.93 | 6.10 | yes | **yes** |
| **ED, 8,000** | 3.79 | **4.22** | 0.96 | 6.54 | yes | **yes** |
| *ED, near-partner variant, 8,000* | 3.77 | 4.17 | 0.98 | 6.58 | yes | **yes** |
| Ring (1D control) | 2.00 | 1.00 | 0.00 | 2,000 | no | — |
| Flat grid (2D control) | 4.00 | 1.93 | 0.50 | 44.5 | no | — |
| **3D grid (control)** | 6.00 | **2.67** | **0.68** | **15.0** | no | — |
| **Random web (control)** | 6.00 | — | — | 5.47 | **yes** | — |

*(all at 8,000 events unless stated; "—" means the reading returns no value, which is itself the small-world signature)*

**Read the last two rows against ED's.** ED's grown patterns sit on top of the **random web**, not the 3D grid — same mean distance, same small-world flag, same refusal to give a dimension. The 3D grid's mean distance grows like the cube root of size (9.7 → 12.0 → 15.0 as size goes 2k → 4k → 8k, a factor of 1.55 against the predicted 1.59); ED's barely grows at all (5.81 → 6.10 → 6.54).

The patch-edge exponent says the same thing another way: **0.96**, meaning the relations crossing a patch's edge grow almost as fast as the patch itself. In three dimensions that number is 0.68; in two, 0.50. At 0.96 there is no "edge" to speak of — every patch touches everything.

## Why it comes out this way

**Holding clocks together is far too weak a filter to pick out three dimensions.** It rules out the line and the flat sheet — that part of attempt 6 is real and step 1 confirmed it. But it does **not** rule out small worlds. Small worlds are, if anything, *better* at it: ED's patterns lock with 3.8 relations per event where the 3D grid needs 6.

So when ED is told "carry as few relations as you can while still holding together", the cheapest answer is **not** a 3D lattice. It's a random web. **Minimality pushes away from three dimensions, not toward it.**

**And the shape was largely settled before sync got a say.** Each new event arrives attached to a *randomly chosen* existing event. That alone builds a pattern with log-sized distances, and relations that stick (D12) can only shorten distances further — nothing in the model can ever lengthen one. The dimension was lost at the arrival rule, not at the sync rule.

**I tested whether that could be patched at the margin:** a second variant in which a strained event may only reach partners already within three relations of it, so no new long shortcut is ever added. Every number is the same (4.17 against 4.22; 3.77 against 3.79). It doesn't help, because the long shortcuts are in the arrival tree, not in the added relations.

## What this does and doesn't say about ED

**It does not sink attempt 6.** The floor argument passed its own test in step 1. What fails is the extra step — "fewest directions picks three" — which note 9 already flagged as *a meaning doing real work*. It turns out to do the wrong work: fewest relations picks a small world.

**It sharpens the real gap.** ED has no notion of *near* that is independent of its relations. A new event may attach anywhere, so there is nothing for space to be made of. The audit (C16) said ED's clocks were missing from the model; this says that putting the clocks in isn't enough on its own — **something has to say where a new event goes.**

**And ED already has a candidate for that, from road L.** A11 D4: *passing on reaches a neighbourhood.* If a new event attaches to its parent **and to the parent's neighbours**, locality comes out of descent rather than being assumed — no coordinates, no sheet, and nothing borrowed. That is ED's own content, already decided, and it is the one rule in ED that speaks to where a new event goes.

## Options

| | option |
|---|---|
| **(a)** | **Step 2b: attachment by descent.** Re-run exactly this model with one change — a new event attaches to its parent *and to the parent's neighbourhood* (A11 D4), rather than to a random event. Everything else identical, expectations fixed first. This is the one change ED itself supplies |
| **(b)** | Accept the negative result as it stands: sync plus minimality does not make space, and ED needs a further meaning before the question can be put again |
| **(c)** | Attack minimality instead: make "fewest directions" mean fewest *distinct directions* rather than fewest relations — but ED has no directions without space, so this needs a new meaning from you |

**Default taken under the standing instruction (Allen asleep): (a)**, with expectations written before the run and reported separately from N1–N3, which are now closed as recorded above.
