# The dispersion check: do ED-style hops slow short waves?

*ED_Attempt_05, note 6. 2026-09-15 (RD8, D8). Ledger: C23–C25. One arithmetic check (`checks/dispersion_check.py`, rules and expected results written first; all seven as expected), plus reasoning. **ED has no decided three-dimensional hop rule, so the rules below are representative, built from decided meanings.** Claude set them; Allen authorized the run (D8).*

## Why this check

- **Road J closed** with one input supplied, and Unruh's temperature inherited (C22).
- **It left a named risk** (C20): if short waves travel slower than light anywhere, low-energy detectors see large Lorentz violation (Husain and Louko).
- **Discrete hopping often does exactly that.** This check asks whether ED-style hops do.

## The rules

**Built from decided meanings:**
- **one locus per tick** is the top speed (A4 note 13);
- **light doesn't turn** (A4 D27);
- **mass is turning** (A4 C74).

| | rule | what it is |
|---|---|---|
| **R1** | **1D light** | Right-movers hop right, left-movers hop left, no turning |
| **R2** | **1D matter** | A fair turn each tick (angle π/4), then the same hop |
| **R3** | **3D light** | The simplest no-turn rule in three dimensions: one hop along each axis per tick, direction set by the relation's two-state pointer. Close in form to Bisio, D'Ariano and Perinotti's Weyl walk |

**"Speed" here** is the phase speed f = ω/|k|, Husain and Louko's quantity. **f < 1 means slower than light.**

## The results (C23, all as expected)

| | what | result |
|---|---|---|
| **E1** | 1D light | **Exactly light speed at every wavelength** (f = 1 to 10⁻¹⁶). No slow short waves |
| **E2** | 1D matter | Top speed **0.707**, and a gap of π/4. That's mass, not the leak |
| **E3** | 3D rule | Its dispersion formula confirmed: cos ω = cos kx cos ky cos kz − sin kx sin ky sin kz |
| **E4** | 3D, along an axis | Exactly light speed |
| **E5** | 3D, very long waves (\|k\| = 0.01) | **Faster than light along one diagonal, slower along another,** by \|k\|/(3√3): +0.00192 and −0.00193 |
| **E6** | 3D, shorter waves (\|k\| = 0.5) | **0.884** (slow) along one diagonal, **1.079** (fast) along another |
| **E7** | 3D, averaged over directions (as a randomly oriented pattern would average) | **Slower than light on average:** 0.9905 at \|k\| = 0.5, and 0.99853 at \|k\| = 0.2, about 1 − 0.038\|k\|² |

## What it means (C24)

**In one dimension, ED's meanings keep light exact.** No slow short waves, so the risk doesn't arise there.

**In three dimensions, the simplest ED-style rule:**
- **picks out directions at the lowest order:** light's speed shifts in proportion to its energy, one way along some diagonals and the other way along others. That breaks the direction-free assumption S′ that road J needed;
- **is slower than light on average,** even after averaging over orientations. **So Husain and Louko's condition, a dip below light speed, survives the averaging.**

**A general point, not just this rule:**
- **Any one-tick rule on a cubic grid runs into it.** With one tick per step, a wave's frequency can't exceed π, while the grid's wavenumbers reach π√3 at the corners of its zone.
- **So somewhere f ≤ 1/√3.** A dip below light speed is unavoidable for such rules in three dimensions.
- **In one dimension the zone only reaches π,** which is why R1 can stay exact.
- **Caveat:** Husain and Louko's result is for smooth dispersions. Whether it applies in the same form to a grid's repeating dispersion isn't settled here.
- **A direction-free, non-grid pattern has no such zone,** so this general point doesn't apply to it. That case is open.

**A rough comparison, labelled as not a test:**
- **The speed shift along the worst directions** is about 0.19 × (energy / grain energy).
- **If the grain were the Planck length,** that would sit at or just past the gamma-ray-burst limit on shifts linear in energy (about 1/6 of that, from LHAASO).
- **Road J's G relation puts the grain at or above the Planck length** (ℓ_g = √(k·s₀)·ℓ_P), which would make it worse.
- **This isn't a test:** R3 isn't ED's decided rule, the grid's orientation is unknown, and photons aren't this two-state field.

## The verdict (C25)

**Under road J's rule** (C21, confirmed D8), the risk becomes a conflict only if ED's *decided* meanings force slower-than-light short waves.
- **In 1D they don't:** light is exact.
- **In 3D, ED has no decided hop rule,** so there's no conflict.

**Verdict: no conflict. The risk is sharpened into constraints on any future 3D hop rule for ED.** It must:
1. **pick out no directions at the lowest order** (S′, and the photon limits);
2. **not dip below light speed anywhere** (Husain and Louko), which a one-tick rule on a cubic grid can't manage, unless the leak is shown not to apply to grid dispersions;
3. **keep one locus per tick as the top speed** (A4 note 13).

**A meaning question for whenever ED's 3D hop rule is chosen:**

**H-Q1:** Is ED's pattern a grid-like structure, or a direction-free random pattern (S′)?
- **A grid** faces the constraints above directly.
- **A random pattern** avoids the zone argument, but its dispersion hasn't been worked out.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **The particle repair** (A4 leads L1 and L3) | Attempt 4's standing conflict; road J is closed |
| **(b)** | **Waves on a direction-free random pattern:** do they travel at light speed without dipping below it? Rules first | The one kind of pattern that might satisfy all three constraints |
| **(c)** | **Update the inputs table and take stock of attempt 5** | Road J and this check are complete units |

**Proposal: (a).** Road J did its job. The particle conflict has been waiting since attempt 4, and (b) will matter when a growth rule is built.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C23 | `checks/dispersion_check.py`, run 1 (`checks/dispersion_check_run1.txt`) | Computed |
| — | Husain and Louko, *PRL* 116, 061301 (C18); Bisio, D'Ariano and Perinotti's Weyl walks (A4 C74); LHAASO GRB 221009A linear limits (A4 C84); C10, C20–C22 (this ledger) | This and earlier ledgers |
