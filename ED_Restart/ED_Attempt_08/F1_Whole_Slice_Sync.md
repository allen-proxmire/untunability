# Road F, part 1: sync as a whole slice agreeing (on paper)

*ED_Attempt_08, note 10. 2026-09-20 (RD16). Ledger: C42–C45. **Reasoning only; no code, nothing run.** The first road that tests ED's own meaning rather than a modelling convenience. Questions F-Q1–F-Q5 are for Allen; running is a separate yes.*

## Why this road is first

**Allen decided (D10) that sync means a whole slice agreeing, not a move-by-move veto.** Every three-dimensional growth run in attempts 7 and 8 used the veto. So the thing ED actually means has **never been tested in growth at all.**

## What "a whole slice agreeing" means precisely

**Synced Now already said it** (A7 C2b). Clocks tick at slightly different rates; links pull them together; "now" is where they agree. The result was a **scaling law**:

> Across a region of size **L**, the clocks' spread is **W(L)**, and the **tilt** of "now" is **W(L)/L**.
>
> | slice dimension | what the tilt does as L grows |
> |---|---|
> | 1 | grows |
> | 2 | holds |
> | **3** | **shrinks** |

**A slice supports a common "now" exactly when its tilt shrinks with scale.** That is a property of the whole slice, measurable on a finished slice, needing no moves at all.

**So road F's reading of D10 is not an invention.** It is Synced Now's own statement, put back where it started.

## The measurement

For a grown slice: solve for the steady tick field (the same solve the `neck_strain` reading already uses), then for each radius r take the spread of the field inside balls of radius r, averaged over centres, and form **tilt(r) = spread(r)/r**.

**Shrinking tilt = a common now survives. Flat or growing tilt = it does not.**

Everything needed is already built: the steady-state solve, the ball distances from 200 centres.

## What the literature says the threshold is (C42)

Hong, Park and Choi give the **lower critical dimension for frequency synchronisation as 2** (and 4 for phase). Below dimension two, coupled clocks with persistent rate differences **cannot hold a common rhythm at large scales**, no matter how strong the coupling.

**And that is exactly the quantity E4 measured:**

| | spectral dimension | above the critical 2? |
|---|---|---|
| **Veto on** (three seeds, n = 52) | **1.635 – 1.685** | **No** |
| **Veto off** (two seeds, n = 52) | **2.318 – 2.319** | **Yes, barely** |
| Flat, for reference | 3.007 | Yes |

> **The per-move veto drives the slice below the dimension at which a common "now" is possible. It destroys the condition it was imposed to enforce.**

That is a claim, not yet a measurement — the tilt has never been measured on a grown slice — and testing it is what road F is for.

## The design, least structure first (C43)

**Sync as a filter, not a driver.** Grow with commitment and curvature only — no sync anywhere in the move loop — and then **ask of the finished slice whether it supports a common now.**

This is how Synced Now used sync: a **diagnostic** applied to a given slice. Nothing is added to growth; a property is measured.

| | |
|---|---|
| **Calibrate** | Flat slices should show **shrinking** tilt; randomised (crumpled) slices should not. **If the reading cannot tell those two apart, the road stops there** |
| **Measure** | The E4 control slices — commitment and curvature, no veto — at n = 24, 32, 52 |
| **Contrast** | The E4 veto slices at the same sizes |
| **Cost** | The slices re-grow deterministically; about **2.5 hours**, almost all of it re-growing n = 52 |

**Nothing new is built.** One reading is added to tools that already exist.

## What the three outcomes mean (C44)

| outcome | what it records |
|---|---|
| **Grown slices support a common now** (tilt shrinks) | **Sync does not belong in the growth loop at all.** ED's growth already produces slices that can hold a common "now", and the veto was both unnecessary and harmful. The wall is then entirely about the local costs, and road 2 becomes the whole question |
| **They do not** (tilt flat or growing) | **Sync as a condition was doomed from the start:** the slices cannot satisfy it, and forcing it move by move mangled the geometry instead. The question becomes what growth rule could make a slice that supports a common now — and that is a much sharper question than "why isn't it flat" |
| **The veto slices fail and the controls pass** | **The strongest result road F could give:** the veto is self-defeating, measured rather than argued, and D10's correction is vindicated in the model as well as in the meanings |

**In every case road F says something.** That is why it is worth two and a half hours where road E cost thirty-five.

## What road F does not do (C45)

- **It does not make space.** The controls read spectral dimension 2.32, not 3. Removing the veto helped and did not fix it. **Commitment and curvature remain, and they are road 2.**
- **It does not test sync as a driver.** If a whole-slice condition should *shape* growth rather than judge it, that is a further road and needs its own design — a condition on a **tick** rather than a move, which costs a whole tick per rejection.
- **It does not touch the classical/quantum gap** recorded in note 9: whatever road F finds, ED's growth still uses positive weights and cannot cancel.

## Questions for Allen

| | question | proposed default | why |
|---|---|---|---|
| **F-Q1** | **Whole-slice sync measured as the tilt across scales**, from the steady tick field? | **Yes** | It is Synced Now's own statement, not a new construction |
| **F-Q2** | **Sync as a filter on finished slices, not a driver in the move loop** | **Yes** | The direct reading of D10, and how Synced Now used it |
| **F-Q3** | **Calibrate on flat and randomised first, and let the calibration stop the road** | **Yes** | E4's gate caught two defects before any result; the same discipline |
| **F-Q4** | **Measure on the E4 slices**, re-grown, rather than new runs | **Yes** | Free comparison with everything already recorded |
| **F-Q5** | If grown slices cannot hold a common now, is that a result about **ED** or about **the growth rule**? | **The growth rule** | Synced Now derived the property for *given* slices; it never claimed grown ones would have it |

## Next step

**If the defaults hold:** write the reading, calibrate it on flat and randomised, and report the calibration **before** measuring any grown slice.

## Addendum: the calibration changed, before any of it was run (2026-09-20, D14)

**Section 4 proposed calibrating on flat against randomised. That is the wrong contrast, and thinking it through before writing the code showed why.**

**Both of them pass.** A randomised slice is compact and effectively high-dimensional, so a common "now" survives on it easily — just as it does on flat. A calibration where both objects give the same answer tests nothing.

**The right contrast is Synced Now's own:** objects where a common "now" survives against objects where it does not.

| calibration object | dimension | Synced Now's prediction for the tilt | exponent |
|---|---|---|---|
| **Ring** | 1 | **grows** | **+0.5** |
| **Square torus** | 2 | **holds** | **0** |
| **Cube torus** | 3 | **shrinks** | **−0.5** |
| Triangulated 3-torus (ED's flat slice) | 3 | shrinks | −0.5 |
| Randomised slice | high | shrinks | more negative |

**The reading must reproduce +0.5, 0 and −0.5 on the first three**, which are trivial graphs needing no growth at all. If it cannot, it is not measuring what Synced Now measured and the road stops.

**And the measurement is Synced Now's, not a new one.** Attempt 7's C2b measured the structure function **G(r) = ⟨(φ_a − φ_b)²⟩ over pairs at hop distance exactly r**, on a doubling ladder r = 1, 2, 4, 8…, from about 20 sources, requiring at least 100 pairs per rung. The tilt is **√G(r) / r**. This road reuses that construction exactly, on a slice's steady tick field instead of a simulated one.

**Recorded before any calibration was run**, so the change of contrast cannot be a response to what the first contrast showed.
