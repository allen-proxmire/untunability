# Road F results: ED's grown slices cannot hold a common "now" — with or without the veto

*ED_Attempt_08, note 11. 2026-09-20 (RD17). Ledger: C48–C50. Runs `model/f1_calibrate.py` and `model/f1_measure.py` (five slices re-grown, 1.9 h on three workers). The measurement rule and the pass threshold were fixed before any grown slice was touched.*

## The scale, fixed first

The reading was calibrated on three objects whose answer is known, five seeds each, and **passed**: ordered, separated by 0.27 and 0.35, on every seed, with the solve matching attempt 7's to machine precision.

| | tilt exponent |
|---|---|
| **ring (d = 1)** | **−0.013** |
| **square torus (d = 2)** | **−0.280** ← the threshold |
| **cube torus (d = 3)** | **−0.627** |
| ED's flat slice (d = 3) | −0.671 |

**Fixed before measuring:** a grown slice supports a common "now" if its exponent is **at or below −0.280**, two being the literature's lower critical dimension for frequency synchronisation.

## The result (C48)

| slice | events | run d_s | tilt exponent | verdict |
|---|---|---|---|---|
| **n = 24, veto** | 15,557 | 1.393 | **−0.130** | **fails** |
| **n = 32, veto** | 36,980 | 1.432 | **−0.134** | **fails** |
| **n = 52, veto** | 156,172 | 1.685 | **−0.132** | **fails** |
| n = 32, control | 33,045 | 1.784 | — | **not measurable** |
| n = 52, control | 141,743 | 2.319 | — | **not measurable** |

**The veto slices fail at every size, and they fail identically.** −0.130, −0.134, −0.132 across a tenfold range in volume — sitting between one and two dimensions, nearer the ring than the square torus. **A slice grown under the per-move veto cannot hold the thing the veto was imposed to enforce.**

**The controls are not measurable under the rule fixed in advance.** They are more compact than the veto slices — diameters 13 and 17 against 19 to 25 — so their ladders stop at r = 8, four rungs, and dropping the two saturated top rungs leaves two, below the three a fit needs. **This is the possibility F1-4 named before the run: the resolution wall, not a result.**

## What the controls would have said, labelled as post-hoc (C49)

**These fits were not fixed in advance and are not a result.** They are here because "not measurable" could be hiding a clear pass, and the honest thing is to look and say what is there.

| | all four rungs | dropping one |
|---|---|---|
| n = 32 control | −0.185 **above** | −0.122 **above** |
| n = 52 control | −0.325 *below* | −0.221 **above** |

**Three of the four sit above the threshold.** There is **no hidden clear pass**. The one that dips below does so by 0.045 and uses the rung most likely to be saturated.

**So the most likely reading, stated as a reading:**

> **ED's grown slices do not support a common "now" — with the sync condition or without it. The veto makes it worse; removing it does not restore it.**

## What this does to C42's claim (C50)

**C42 claimed the per-move veto drives the slice below the dimension at which a common "now" is possible, destroying the condition it enforces.**

**Half of that is confirmed and half is not.**

- **Confirmed:** the veto slices do not support a common now, at three sizes, unambiguously.
- **Not confirmed:** that removing the veto restores it. The controls are better — −0.12 to −0.33 against the veto's −0.13, and their spectral dimension is 2.32 against 1.69 — but they do not clearly cross the threshold.

**So road F lands on its second outcome, not its third.** From note 10's table:

> *"Sync as a condition was doomed from the start: the slices cannot satisfy it, and forcing it move by move mangled the geometry instead. The question becomes what growth rule could make a slice that supports a common now — and that is a much sharper question than 'why isn't it flat'."*

**That is where we are.** Allen's correction on what sync means (D10) stands on its own reasoning and is not weakened by this; what this shows is that **fixing sync's form is not enough**, because ED's growth does not produce slices that can carry a common "now" in the first place.

## The size-independence, again

Every quantity road F measured is **flat in size**: −0.130, −0.134, −0.132 over a tenfold volume range. Road E found the same thing in the walk's reach (V^0.101), in the fitting window (2–4 hops at every size), and in the spectral dimension curve. **ED's grown slices are the same object at every scale we can reach**, which is why more compute has stopped buying answers.

## Honest limits

- **One seed per slice.** Three reading seeds each, but one growth seed.
- **The controls are unmeasured**, and the post-hoc fits above are not a substitute.
- **A finer ladder would help** — every integer r instead of doubling — and would probably make the controls measurable. It was **not** done here, because the looser fits above already show which way they point, and changing the measurement after seeing that would be the forking path this project keeps guarding against. **It is Allen's call whether to re-measure that way.**
- **Nothing is derived.** Inputs supplied: still 3.
