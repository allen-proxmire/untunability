# H1 results: without the costs, ED's slices feel three-dimensional up close — and are far too compact overall

*ED_Attempt_09, note 4. 2026-09-21 (RD6). Ledger: C13–C15. Run `model/h1_run.py`: six slices (n = 24, 32, 52, two seeds each), grown with the link budget and the ceiling only, about 3.3 hours. Every reading was calibrated, and every pass mark fixed, before any slice grew. Written plainly.*

## What was run

Growth with **only the parts built as conditions**: the conserved link budget and the neighbour limit of 60. **No commitment cost, no curvature cost, no sync veto.** This is attempt 7's setting D, never measured at a size where it could show.

## The results

| | small (12,800) | medium (30,700) | **big (131,700)** | flat space at big size |
|---|---|---|---|---|
| neighbours per event | 14.2–14.3 | 14.1–14.3 | **14.2** | 14.0 |
| **how roomy it feels (d_s)** | too small to read | ~3.0–3.1 by distance | **2.81, 2.97** | 3.01 |
| curvature, middle value | −0.17, −0.14 | −0.16, −0.17 | **−0.17, −0.18** | 0.00 |
| **average distance between points** | 4.4–4.5 | 5.0 | **6.27, 6.32** | — |
| widest distance | 9–10 | 11–13 | **15** | 39 |
| mass dimension (d_H) | too small to read | too small to read | **5.46, 5.54** | 2.85 |

All six survived, with structure and both budgets exact throughout.

## What went right (C13)

**1. The stringiness is gone.** With the costs on (attempt 8), the space felt about **1.4**-dimensional up close — stringy. With the costs off it feels **2.8–3.0**, against flat space's 3.01. **This is the first time ED's growth has produced a slice that feels three-dimensional.**

At the big size, measured at every distance, it reads **2.7–3.3 from 1.6 steps out to 5.5 steps**, then rises and collapses as the walk runs out of room:

> 1.6: 2.92 · 2.1: 2.92 · 2.6: **2.71** · 3.3: 2.89 · 4.0: 3.23 · 4.8: 3.29 · 5.5: 3.28 · 6.0: 4.38 · 6.1: 1.72

Compare attempt 8's slices with the costs on: **a dip to 1.4** at the same distances.

**2. Density sits at flat.** 14.1–14.3 neighbours per event, against flat's 14.0. Attempt 8's commitment cost had it at 10.2.

**3. Curvature is bounded below**, by the mark fixed before growth (middle value at or above −0.25): **every slice passes**, at −0.14 to −0.18. The honest qualifier: about 70% of connections lean negative, and the worst reach the tree-like −0.5. The middle passes; the tail does not look flat.

**So H1's reading of your meanings is borne out: the costs were what made the slices stringy.** Removed, the slices feel three-dimensional and sit at flat density.

## What went wrong (C14)

**The slices are far too compact.** Every point is only a few steps from every other, and that stays true as they grow.

**The test fixed before any big-size number existed** (C8): average distance **near 5.9 means a small world; near 8.1 means three-dimensional space.**

> **It came in at 6.27 and 6.32.**

**Closer to the small world.** Across the three sizes, average distance grows as **V^0.150** — the way a roughly **7-dimensional** object would — where flat space grows as V^0.333, exactly three. The widest distance tells the same story: **15**, where flat space at the same size is **39**. The mass dimension reads **5.5**, where flat reads 2.85.

**An honest nuance:** it sits a little above the pure small-world line, not on it — the distances grow somewhat faster than a true small world's would. But it is nowhere near three-dimensional space.

### A plain picture

**Think of a city whose streets look perfectly normal up close — but with tunnels everywhere.** Walk a few blocks and it feels like an ordinary city. Try to measure how big the city is and it's tiny, because the tunnels connect everything to everything else.

That's what randomly wired connections do. **The conditions fix the density and remove the stringiness, but nothing stops the random shortcuts.** That's entropy: with no preference steering the wiring, a randomly wired pattern at the right density fills up with shortcuts.

## A common "now" — suggestive, not a result

The tilt reading couldn't be read on most slices: they're too compact to give enough distance steps. **On one reading of one big slice it came out at −0.631 — the value a cube grid gives.** And on both big slices the raw tilt falls steadily with distance (1.48 → 0.99 → 0.64 → 0.58), the direction a common "now" needs.

**That is one value from six attempts.** It's suggestive, and it's not a result. It also measures clock *readings*, where your decision (D5) says ED only claims *rates* — road R's question.

## Verdict (C15)

**By the outcomes fixed before the run (C5):** the slices meet some of the conditions — three-dimensional up close, curvature bounded below, density at flat — **but not the shape.** Globally they are small worlds. **ED's conditions alone don't beat the counting at large scales.**

> **H1 fixed what the costs broke. What's left is the large-scale shape, and nothing in ED's growth currently gives it one. That isolates H2 — weights that can cancel — and sharpens it: the thing H2 has to do is get rid of the shortcuts.**

## What this means for ED, plainly

- **Good:** your meanings, built faithfully as conditions, produce slices that feel like three-dimensional space up close. That's never happened before.
- **Not yet:** the large-scale shape. Random wiring makes shortcuts, and shortcuts shrink everything.
- **The question now is sharp:** what, in ED, stops shortcuts forming? Something that acts across the whole slice, not on single moves.

## Honest limits

- **Two seeds per size**, and the scale-resolved reading on one seed per size.
- **The walk runs out of room at about 6 steps** on the big slices, so "feels three-dimensional" is established up to about 5 steps, not beyond.
- **The small-world call rests on the average distance** at three sizes; it sits between the two predictions, closer to the small world.
- **Nothing derived.** Inputs supplied: still 3.
