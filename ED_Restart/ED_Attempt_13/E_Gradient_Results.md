# With gradients: the end state is no longer the same from every start

*ED_Attempt_13, note 5. 2026-09-23 (RD5). Ledger: C5, from D2. Code `model/g_grad.py`, output `model/g_grad.txt`, data `model/e_runs/grad.json`. Expectations G0–G4 fixed in note 4 before any code. Written plainly.*

## The short answer

**Gradients survive** — they don't flatten away, so the run counts.
**Patterns hold on fewer relations than with noise** — about 3.2 per event against 4.15.
**And for the first time in this project, where a pattern started makes a difference to where it ends up.**

**But the readings are still 4.0–4.8, which is no dimension.** G3 fails.

## The numbers

Three starts, three seeds, about 8,500–9,300 events:

| start | reading | mean distance | relations per event | rate spread at the end | small world? |
|---|---|---|---|---|---|
| **ring** | 3.83, 3.98, 4.14 → **3.99** | 7.7–8.2 | **3.36–3.44** | 0.50× | yes |
| **3D grid** | 4.57, 4.83, 4.41 → **4.60** | 8.4–9.2 | **3.13–3.23** | 0.47× | **no** |
| **web** | 4.41, 4.71, 4.58 → **4.57** | 8.2–8.8 | **3.11–3.23** | 0.48× | mixed |

| | expectation | result |
|---|---|---|
| **G0** | Gradients survive — the gate | **Passed.** The rate spread settles around half its starting value in every run, nowhere near the void line at a tenth. Diffusion and passing-on reach a balance rather than flattening |
| **G1** | Fewer relations than the noise model's 4.15 | **Passed.** 3.39, 3.19, 3.16 |
| **G2** | **The end state is no longer the same from every start** | **Passed by its rule** — the ring ends at 3.99 against 4.60 for the 3D grid, a gap of 0.6 where the rule asked for 0.3. **But see the caution below** |
| **G3** | Readings below 3.9 with the small-world flag clearing | **Failed.** Readings went *up*, not down |
| **G4** | Reported | Rate spread settles at about half; the paper's own distance agrees with hop distance only moderately (correlation 0.35–0.65) |

## The caution on G2, which matters

**The gap between starts is 0.6. The spread between seeds of the same start is 0.3–0.4.** So the effect passed its pre-registered rule, but it is only about twice the noise. **I would not call it established on three seeds.** What can be said honestly: with noise rates the three starts agreed to within 0.1 of each other; with gradients they no longer do, and the ring is consistently the lowest of the three across every seed.

That is a direction, not a measurement. It needs more seeds before it revises A12 C11 and C12, and I've recorded it as unrevised for now.

## One thing that did change cleanly

**The 3D-grid start is no longer a small world** — all three seeds, where every previous model made it one. Its mean distance is 8.4–9.2 across 9,200 events, against about 10.6 for a real 3D grid that size.

**But its ball-growth reading went up to 4.6.** So the two readings now disagree: one says it isn't a small world, the other says it has no definite dimension. That's an honest oddity, not a result, and it's the kind of thing E-4 in note 2 was written to chase.

## Do the answers depend on my two numbers?

Both were varied by a factor of three, as promised:

| variation | reading | relations/event | rate spread |
|---|---|---|---|
| smaller variation when passing on (0.03) | 4.47 | 3.05 | 0.41× |
| larger (0.30) | 4.01 | 3.93 | 0.82× |
| slower diffusion (0.03) | 4.29 | 3.57 | 0.75× |
| faster diffusion (0.30) | 4.21 | 2.81 | 0.26× |

**The readings sit between 4.0 and 4.5 throughout.** The density and the gradient size move with my settings; the shape reading doesn't. So the failure of G3 is not an artefact of the two numbers I chose — which is the one useful thing about a negative that's robust.

## What this says

1. **Gradients are not self-erasing.** The paper's diffusion and its passing-on reach a balance at about half the starting spread. ED's own dynamic is stable here, which was the most likely way for this run to die and it didn't.
2. **Gradients make the model cheaper.** Neighbours tick alike, less has to be carried, and the pattern holds on 3.2 relations per event rather than 4.15. That is ED's content doing recognisable work.
3. **Gradients give a pattern some memory** — enough that starts no longer converge exactly. Weakly, on three seeds.
4. **They do not produce space.** The readings are 4.0–4.8 and, if anything, higher than the noise model's 3.9. **The fourth correction of the same kind has again improved the model's character without changing the answer.**

Note 4 said, before the run: *if gradients don't change the answer either, the honest reading is that ED's rules as written do not make space, and that becomes the result rather than a staging post.* **That is where this leaves it.**

## Options

| | option |
|---|---|
| **(a)** | **Settle G2 properly** — ten seeds per start, which is cheap, and either revise A12's convergence finding or drop the claim |
| **(b)** | **Chase the oddity:** the 3D-grid start is no longer a small world but reads 4.6. The two readings disagree, and one of them may be the wrong instrument for this object |
| **(c)** | **Take stock of attempt 13 and of the project** — four corrections of the same kind have now been made, each from ED's own words, and none has changed the answer |

**Proposed: (a) then (c).** (a) is an hour and it decides whether a real finding is on the table; (c) is where this is heading either way.
