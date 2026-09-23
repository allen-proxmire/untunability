# H2 step 1: the shortcuts spoil the spacetime too

*ED_Attempt_09, note 6. 2026-09-21 (RD8). Ledger: C20–C22. Run `model/h2_spacetime.py`: flat calibration at two sizes, then H1's four conditions-only slices re-grown exactly and their spacetimes read, 0.6 h. The pass mark was fixed from the calibration before any grown spacetime was read. Written plainly.*

## The question

H1's slices feel three-dimensional up close but are riddled with shortcuts (C13–C15). Attempt 7 decided the **whole spacetime** is what should be judged (A7 D40), because CDT's own single slices are stringy and only its spacetime looks like space. **Do H1's shortcuts spoil the spacetime, or only the slices?**

## The calibration (C20)

A flat spacetime — the flat slice stacked 21 times, each point linked only to itself in the next copy — reads **3.61** at the medium size and **3.67** at the larger, not the ideal 4. The measuring method reads low, just as it reads a flat slice as 2.66 instead of 3.

**Pass mark, fixed before any grown spacetime was read: within 0.5 of flat.**

## The result (C21)

| | spacetime reading | flat | gap | reads 3+1? |
|---|---|---|---|---|
| medium, seed 0 | **5.75** | 3.61 | +2.14 | **no** |
| medium, seed 1 | **5.80** | 3.61 | +2.19 | **no** |
| larger, seed 0 | **6.07** | 3.67 | +2.40 | **no** |
| larger, seed 1 | **6.12** | 3.67 | +2.45 | **no** |

All four re-grown slices matched their H1 runs exactly.

**The shortcuts carry straight through into the spacetime.** It reads about 6 where flat reads about 3.6, and **the gap widens with size** (2.1 → 2.4). Flat spacetime is read cleanly across 5–13 steps; these only across 2–4, because everything is a few steps from everything else.

**Removing the costs did not help the spacetime.** For comparison at the same sizes: attempt 8's runs with the veto read 5.68–6.42, without it 6.65–6.94. H1's conditions-only spacetime sits among them.

This matches the expectation written down before the run (at least 1.0 above flat).

## What it means (C22)

**H1 made single slices feel three-dimensional up close. It did nothing for the spacetime.** The shortcuts are not a detail of how a slice is measured — they are the large-scale shape of what ED's growth makes.

**Step 1 of H2 is answered:** the spacetime is spoiled too, so nothing short of something that acts on **whole histories** or **whole slices** is in view. That makes **H2-Q3** the next thing, and it's yours:

> **Do your D11 and D12 — "many could have happened", "the present doesn't know its own past" — mean ED weighs whole histories against each other, rather than growing one forward and keeping it?**

If yes, the next step is to specify, on paper, what ED's version of weighing whole histories would be — including what would play the role that CDT's shape-setting couplings play, which the census guard would count.

## A consequence for the older record

Every spacetime reading in attempts 7 and 8 was set against an ideal of about 4. Against the calibrated flat reference (3.6–3.7) **they sat 1.9–3.3 above flat, not 1.5–2.9** — further off than recorded at the time.

## Honest limits

- **Two seeds per size**, two sizes; the largest size is out of memory's reach for this reading (A8 C31).
- **One spacetime construction**: in-slice links plus forward links to children and absorbers, as attempts 7 and 8 built it.
- **Nothing derived.** Inputs supplied: still 3.
