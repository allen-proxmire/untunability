# Road W, part 1: waves on a direction-free random pattern (on paper)

*ED_Attempt_06, note 2. 2026-09-15 (RD2). Ledger: C2–C7. Literature and reasoning, with one arithmetic check. No simulation. **Meaning questions W-Q1–W-Q3 and the draft exit rule are for Allen.***

## What "on paper" means here

**On paper means reasoning, algebra and literature,** worked out before anything runs.
- **No model or simulation of ED is built.**
- **A script may check arithmetic,** and only with its expected results written first. One such check was run here (C5).

## The question

**Attempt 5's dispersion check** (A5 C24, C25) found that one-tick rules on a 3D grid must slow some short waves below light speed. **ED's pattern is decided to be direction-free and random,** not a grid (A5 D10).

**Road W asks:** on a random pattern with finite, nearby neighbours:
- **do waves travel at one speed in every direction?**
- **are no short waves slower than light?**

**Why it matters** (A5 C18, C20):
- **If some short waves travel slower than light,** detectors feel large Lorentz violation at ordinary energies (Husain and Louko). This holds even if the change only shows up near the grain.
- **Louko and Upton extend this** to inertial detectors in every dimension above two.

## What's known (C2)

| | what it says | source |
|---|---|---|
| **Long waves on random patterns** | The spreading rule on random points linked within a reach **approaches the ordinary smooth one** as the pattern gets finer, with known error rates | Hein, Audibert, von Luxburg (2007); García Trillos, Gerlach, Hein, Slepčev |
| **Randomness can trap waves** | **Anderson localization.** In 3D, weak disorder leaves waves near the middle of the band free to spread; strong disorder, or energies near the band edges, traps them | 3D mobility-edge measurement (Semeghini et al., *Nature Physics* 2015) |
| **Graininess blurs distant sources** | Random phase added along light's journey would blur images of distant quasars and gamma-ray sources. **Chandra, Fermi and VERITAS data rule out the stronger such models** | Perlman et al., *ApJ* 805, 10 (2015); Ng and Perlman (2022) |
| **Slow short waves leak** | Dispersion ω = \|k\|·f with f dipping below 1 anywhere gives large low-energy Lorentz violation in detectors | Husain and Louko 2016; Louko and Upton 2018 |
| **Grid walks already bounded** | A quantum-walk (cellular automaton) version of electromagnetism on a grid has **direction-dependent light speed at first order**. Gamma-ray burst GRB 221009A bounds its grid spacing to **below about 5.8×10⁻³⁶ m**, under the Planck length | arXiv:2506.20136 (2025) |
| **Equal-weight (Grover) walks trap waves** | On the square grid, the Grover walk (every neighbour treated alike) **localizes**: part of any wave stays put, from repeated eigenvalues. The Fourier walk doesn't | Inui, Konishi, Konno (2004); Higuchi, Konno, Sato, Segawa (2014); arXiv:1811.05302 |
| **Clean light cones are fragile** | In 2D, walks with a single light cone rely on symmetries that **generic unevenness breaks, gapping the cone**. Couplings that die off exponentially repair it | Beenakker, Sánchez Férnan, Tworzydło, arXiv:2607.05112 (2026) |
| **Long-range links** | A quantum-graphity foam with some non-local links keeps large-scale Lorentz invariance only if **long links are strongly suppressed** | Caravelli and Markopoulou, *Phys. Rev. D* 86, 024019 (2012) |
| **Causal sets** | Random discreteness makes particles "swerve," tightly bounded by relic neutrinos | Kaloper and Mattingly (A4 fork FC1) |

## On paper (C3, C4)

### 1. Long waves: good news for the pattern (C3)

- **On a random, direction-free pattern, long waves see a smooth medium,** the same in every direction on average (graph convergence results).
- **So the direction problem that sank grids** (A5 C24), and that bounds grid walks near the Planck length (arXiv:2506.20136), **averages away at long wavelengths.**
- **This supports** road J's direction-free assumption S′ and the decided pattern (A5 D10).

### 2. Short waves: slow at every wavelength, for one kind of rule (C4)

**The kind of rule:** each locus's wave is pushed by the differences with its neighbours, with positive weights (a spreading rule of the ordinary second-order kind).
- **The frequency then obeys** ω² ∝ Σ w(1 − cos k·Δ), summed over neighbour hops Δ.
- **Light speed is fixed by long waves,** where 1 − cos y ≈ y²/2.

**The one-line argument (firm):**
- **1 − cos y is less than y²/2 for every y ≠ 0.**
- **So every finite wave has f < 1**, whatever the hop lengths and however they're spread, as long as they point every way evenly.
- **At long wavelengths:**
  - **f² ≈ 1 − (kℓ)²/20** when all hops have one length ℓ;
  - **f² ≈ 1 − (kr)²/28** when links fill a reach r.

**With ticks (one update per tick):**
- **A finite tick pushes frequency up.** In principle this could cancel the slowing.
- **Cancelling needs a tick longer than stability allows:**
  - one hop length: cancelling needs (cτ/ℓ)² = 0.60, but stability requires at most 0.548;
  - within a reach: cancelling needs 0.429, but stability requires at most 0.368.
- **So every stable one-tick rule of this kind still has every short wave slower than light.**

**A suggestive bound for any one-tick rule:** phase advances at most π per tick, so waves shorter than about two grain spacings per tick at light speed travel slower than light. **On a random pattern, how short a wave the pattern carries isn't settled on paper.**

**What this doesn't cover:**
- **First-order walks** (the quantum walks of attempt 2, Grover or Dirac type) aren't of this kind. Their dispersion needs its own argument.
- **Scattering** (trapping, blurring) is a separate effect from the average wave.
- **Husain and Louko's result is for a smooth field.** Whether it carries over to a discrete random pattern isn't settled.

## The arithmetic check (C5)

`checks/w1_dispersion_bounds_check.py`, expected results written first:

| | expected | run 1 |
|---|---|---|
| **B1 shell** | f < 1 everywhere; slowing coefficient 1/20 | **As expected** |
| **B1 ball** | f < 1 everywhere; slowing coefficient 1/28 | **Not as expected**: max f² = 1.0029, fit 1/27.08 |
| **B2** | 1 − cos y < y²/2 for y ≠ 0 | **As expected** |
| **B3 shell, ball** | cancel 0.600 and 0.429; stability 0.548 and 0.368 | **As expected** |
| **B4 shell** | one-tick f < 1 at the stability limit and half of it | **As expected** |
| **B4 ball** | the same | **Not as expected**: max f = 1.0015 |

**The two misses stand.**
- **A follow-up diagnostic** (`checks/w1_ball_roundoff_diagnostic.py`, **not pre-registered**) found both excesses at the smallest wave tested (x = 0.001). There the ball formula subtracts two nearly equal numbers and loses its digits.
- **With the same formula written as a series,** the results come out as:
  - max f² = 0.99999996;
  - slowing coefficient 1/28.001;
  - one-tick max f = 0.9999999975.
- **So the misses are rounding in the script, not the argument.** B4 shell also passed only narrowly on rounding (printed 1.000000; the series gives 0.999999998).
- **The firm argument itself doesn't rest on the script.** It rests on 1 − cos y < y²/2.

## What it means (C6)

- **Long waves:** a direction-free random pattern fixes the grid's direction problem.
- **Short waves:** for spreading rules with positive weights, **every short wave is slower than light on any pattern, with or without ticks.** Husain and Louko's condition is met, structurally, not as a grid artefact.
- **First-order walks are open,** and the literature raises two warnings for them:
  - **equal-weight (Grover) walks trap waves** on grids;
  - **single light cones are fragile** under unevenness.
- **So the live question becomes:** does Husain and Louko's leak apply to a discrete random pattern, and how strongly?
- **Scattering is a second, separate risk.** Distant sources aren't blurred, neutrinos don't swerve, and long links must be rare.
- **Nothing here conflicts with a decided meaning yet.** ED hasn't decided a wave rule.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **W-Q1** | **Is ED's wave rule a one-tick rule:** each tick, each locus updated from its related neighbours? | **Yes** | One locus per tick is the top speed (A4 note 13); ticks carried from attempt 1 |
| **W-Q2** | **Do all related neighbours count equally, with no stored directions?** | **Yes, with the trapping poke recorded** | Least structure and direction-free. But equal-weight Grover walks trap waves on grids, so if ED's rule is a first-order walk this needs a look |
| **W-Q3** | **Is the pattern for now a hand-built stand-in:** random points linked within a fixed reach, until road G grows one? | **Yes, labelled as a stand-in** | Road G decides whether such a pattern can form |

## Draft exit rule (Allen to confirm)

- **If ED's wave rule is a positive-weight spreading rule:** record **"every short wave slower than light for ED's wave rule on any discrete pattern, with or without ticks; the Husain–Louko condition is structural"** (C4, C5). Road W's next step is **whether the leak applies to a discrete random pattern** (literature and paper).
- **If ED's rule is a first-order walk:** record the firm argument as not covering it. The next step is **literature on quantum walks on random graphs** (dispersion and trapping). A check with rules and expected results first follows only if Allen wants it.
- **Scattering stays a named second risk.**
- **No simulation.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide W-Q1–W-Q3** and confirm the exit rule | Settles which branch applies |
| **(b)** | **Then: does Husain and Louko's leak apply to a discrete pattern?** Literature and paper | The question road W now turns on |
| **(c)** | **Or turn to road G** (growth rule) | If the leak question needs the pattern to exist first |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C2 | Hein, Audibert, von Luxburg, *JMLR* 8 (2007), arXiv:math/0608522; García Trillos et al., arXiv:1801.10108; Semeghini et al., *Nature Physics* 11, 554 (2015), arXiv:1404.3528; Perlman et al., arXiv:1411.7262; Ng and Perlman, arXiv:2205.12852; Husain and Louko, arXiv:1508.05338; Louko and Upton, arXiv:1710.06954; arXiv:2506.20136; Inui, Konishi, Konno, *PRA* 69, 052323 (2004), quant-ph/0311118; Higuchi et al., *J. Funct. Anal.* 267 (2014); arXiv:1811.05302; Beenakker et al., arXiv:2607.05112; Caravelli and Markopoulou, arXiv:1201.3206 | Abstracts; arXiv:2506.20136 HTML for its bounds |
| C5 | `checks/w1_dispersion_bounds_check.py`; `checks/w1_ball_roundoff_diagnostic.py` (follow-up) | Run 2026-09-15 |
| — | A4-ledger note 13; A5-ledger C18, C20, C24, C25, D10 | Earlier ledgers |
