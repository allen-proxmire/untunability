# The model's first runs: timing trial and calibrations

*ED_Attempt_06, note 12. 2026-09-15 (RD18). Ledger: C61–C65. **No process readings were taken.** Decisions on how to proceed are for Allen.*

## What was run

**Allen confirmed note 11 and asked for the timing trial and calibrations only** (D13).

**Before any run:**
- the code was written in `model/`;
- every open choice was recorded in `model/IMPLEMENTATION_NOTES.md`;
- a smoke test checked that the code runs (not a result).

## 1. Calibrations, run 1 (C61)

**The readings were tested on four patterns whose answers are known.** The expected ranges were written in note 11 before any code.

| pattern | what came out | verdict |
|---|---|---|
| **3D random pattern** (16,000 loci) | mass dim 2.73, walk-return dim 2.77, **walk dim 2.18** | As expected |
| **3D cubic grid** (25³) | **mass dim 2.589** (range starts at 2.6), walk-return dim 3.05, walk dim 1.95 | **Not as expected** |
| **2D random pattern** (16,000) | mass dim 1.91, walk-return dim 1.78, **walk dim 2.214** (range ends at 2.2) | **Not as expected** |
| **Random 12-regular graph** (small world) | small-world flag raised | As expected |

**2 of 4 as expected.** Under exit rule X0, no model result counts until the readings are fixed and the calibrations pass on a rerun.

## 2. Why the readings missed (C62, a labelled follow-up)

**All three readings are biased at the grain scale:**
- **mass dimension:** read ball by ball, the slope rises with radius. On the grid it goes from 2.28 at radius 2 to 2.83 at radius 10, so a fit that starts at radius 2 reads low;
- **walk dimension:** early in the walk it reads too high on the 2D pattern (about 2.3), settling toward 2.14 later;
- **walk-return dimension:** it wanders early too.

**There's also finite-size bias at the end of the walk window.** On the 3D random pattern, walk dimension creeps up to 2.37 as the walk starts to feel the edges of a 16,000-locus pattern.

**Picture:** a ruler that's wrong at the tiny end (where the grain shows) and at the far end (where the pattern runs out). It's only trustworthy in the middle.

## 3. Timing trial (C63): the model froze

**The central setting, meant to grow to 1,000 loci, stopped at 50.** The stall guard fired after 10,000 failed births in a row. The script's plan estimates are **invalid**, because they assumed the run reached 1,000. The trial didn't time the plan.

## 4. Why it froze (C64, a labelled follow-up)

**The same run was reproduced up to the freeze and every possible birth site checked:**
- **41 of 50 loci had all 12 link slots full.** The rest (2 to 7 links) had only full neighbours;
- **every one of the 263 relations was blocked by the neighbour cap. None was blocked by curvature.**

**Picture:**
- sync pulls in new links every tick, but a new locus is born only every 10 ticks;
- rewiring moves links around but never frees a slot;
- so every locus fills its 12 slots;
- a newborn needs a link with room at *both* ends, and there are none left;
- **growth freezes.**

## What it means (C65)

- **The readings need a fix before any model result can count** (X0).
- **The model as specified can't grow at its central setting.** In ED's terms: clocks pulling in relations fill every locus to its limit before new loci can join.
  - That's a real property of these rules.
  - Whether it's a property of ED or of the particular modelling choices (births onto a relation with room at both ends; one sync pull per tick against one birth per ten ticks) isn't settled.
- **The best pre-registered outcome (X1) looks out of reach.** It needs the central setting to reach rest at all three sizes, and the one central run made froze at 50 loci. The rules stay as they are; this is recorded, not repaired.

## Options (Allen decides)

| | option | what it involves |
|---|---|---|
| **(a)** | **Fix the readings and rerun the calibrations** | See the proposed fix below. Needed before *any* model result counts, whatever happens next |
| **(b)** | **Keep the model as specified,** time the control and one scan corner likely to grow (K/σ = 30, c = 2), then decide on running the scan | Honours the pre-registration exactly. Settings that freeze count as failures. It may spend many hours measuring freezes |
| **(c)** | **Record the freeze as this model's finding, and write a revised model (M2) on paper** | M2 gets its own meaning questions (for example: can a newborn join a single locus with room? should sync pulls be as frequent as births?), expected results and exit rule. The freeze stays on record |
| **(d)** | **Stop the model line** | Record the freeze as the model result, then take stock or conclude attempt 6 |

**Proposal: (a), then (c).** The readings need fixing whatever happens next. The model as specified mostly measures its own freeze, so a revised model on paper, with its choices made in the open, is the better test.

## The proposed readings fix (for option (a); Allen to confirm before any rerun)

**The rule: read every dimension over the same middle range of scales,** away from the grain and away from the pattern's edge.

| reading | now | proposed |
|---|---|---|
| **Mass dimension, ball-cut** | radii 2 to r_max | radii **⌈r_max/2⌉ to r_max** (at least 3 radii, otherwise undefined and flagged) |
| **Walk-return and walk dimension** | from t = 10 until return probability falls to 10/N | from when the walk's spread √⟨r²⟩ reaches ⌈r_max/2⌉ **until it reaches r_max** (the same scales as the balls) |

**Held-out checks,** because the fix was chosen with the diagnostic in view:
- add two calibration patterns **not used in choosing it:**
  - a 3D random pattern with a different seed and mean degree 8 (16,000);
  - a 2D square grid (126 × 126);
- their expected ranges are the same as their dimension class's in note 11, written now, before any rerun;
- **all six must pass.**

**Honest flag:** read off the diagnostic's local slopes, the fix would move the 3D grid and 2D random pattern into range. **But the 3D random pattern's walk dimension would sit right at the 2.2 edge.** So the rerun may still miss. If it does, that's a real limit of what patterns this size can resolve.

## Sources

No new sources. The readings and the model follow notes 9 and 11.

---

## Update: Allen chose (a) then (c) (D14)

**Calibration run 2, with the fixed readings** (C70). Expected ranges unchanged from note 11; the two held-out patterns weren't used in choosing the fix.

| pattern | what came out | verdict |
|---|---|---|
| **3D random pattern** (mean 12) | mass dim 2.92, walk-return dim 2.90, walk dim 2.185 | As expected |
| **3D cubic grid** | mass dim 2.76, walk-return dim 3.03, walk dim 1.96 | As expected |
| **2D random pattern** | mass dim 2.04, walk-return dim 2.03, walk dim 2.16 | As expected |
| **Random 12-regular** | small-world flag raised | As expected |
| **Held-out 3D random pattern** (mean 8, new seed) | mass dim 3.01, walk-return dim 2.96, walk dim 2.17 | As expected |
| **Held-out 2D square grid** | mass dim 1.95, walk-return dim 2.00, walk dim 2.00 | As expected |

**All six as expected.** The readings are cleared for use (X0 lifted).

The 3D random pattern's walk dimension sat close to its 2.2 edge, as flagged beforehand. The fix was chosen with the diagnostic in view, which is why the two held-out patterns were added. Both passed.

**Option (c) is written:** CGP's freeze is recorded as its own finding (C66), and the revised model M2 is specified in [note 13](M2_Model_Spec.md).
