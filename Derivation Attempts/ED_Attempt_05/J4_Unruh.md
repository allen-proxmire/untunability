# Road J, part 4: Unruh's temperature in ED (on paper)

*ED_Attempt_05, note 5. 2026-09-15 (RD6). Ledger: C18–C21. Literature and reasoning; nothing computed. **Meaning questions U-Q1 and U-Q2 and the draft exit rule are for Allen.***

## Where road J stands

- **Jacobson's chain has four inputs:** entropy ∝ area, Unruh's temperature, the first law, and local Lorentz structure.
- **One is now supplied:** entropy ∝ area, from ED's reach, counted (C17).
- **Part 4 asks about the second:** can ED supply Unruh's temperature, or does it have to be inherited?

## What physics knows (C18)

| | what it says |
|---|---|
| **Why the vacuum looks warm to an accelerating body** (Bisognano–Wichmann) | A rigorous theorem: the vacuum restricted to the region an accelerating observer can reach is **thermal with respect to boosts,** at temperature T = a/2π (in natural units). **It rests on the vacuum's boost symmetry,** that is, on Lorentz invariance |
| **Without Lorentz invariance** (Campo and Obadia) | General frame-dependent dispersion breaks the thermality |
| **Even if the breaking is only at high energy** (Husain and Louko 2016; Louko and Upton 2018) | For a field whose dispersion is ω = \|k\|·f(\|k\|/M), normal at low energy and modified only near a high scale M, **atoms modelled as Unruh–DeWitt detectors see drastic Lorentz violation at low energy, whenever f dips below 1 anywhere,** that is, whenever some short-wavelength modes travel slower than light |
| **Experiment** | **Not directly observed.** Electron spin polarization in storage rings can't be cleanly attributed to it. A Bose–Einstein-condensate simulation (2019) showed thermal fluctuations matching Unruh's. Several detection schemes are proposed |
| **Causal sets** | No Unruh-detector treatment on causal sets turned up in this search. That doesn't mean none exists |

## Three ways ED could get a temperature (C19)

| | route | what it needs | verdict on paper |
|---|---|---|---|
| **U-A** | **Inherit Unruh at low energy,** as J-Q4 already does | The vacuum's relations look the same to every uniformly moving body at horizon scales: **emergent boost invariance** | Not supplied, just labelled. **It's the preferred-frame hole in another form** |
| **U-B** | **Define temperature as heat over entropy change,** T = δQ/dS | Nothing new | **Circular.** The first law becomes a definition, and Jacobson's derivation loses all its content. No Einstein equation comes out. **Ruled out** |
| **U-C** | **An ED-native route:** an accelerating path's reach boundary sits at a fixed distance. The crossing relations' far ends are spread over boost angle. If their statistics repeat with a period of 2π in boost angle, the reachable part looks thermal at a/2π | **The same boost invariance as U-A,** in ED's words. It's Bisognano–Wichmann restated | Not a new supply |

**One thing that doesn't count:** "the temperature goes like one over the distance to the reach boundary" follows from there being only one length around. It's dimensional analysis, not ED content. **The 1/2π needs the boost periodicity.**

## A new risk: slow short waves (C20)

- **Husain and Louko's leak is concrete:** if any short-wavelength modes travel slower than light, low-energy detectors see large Lorentz violation.
- **Discrete hopping usually does exactly that.** On a grid, the fastest signal is one step per tick, and short waves typically travel slower than long ones (for a simple lattice, the speed factor is sin(x)/x, below 1).
- **ED's motion picture has one locus per tick as the top speed** (A4 note 13).
- **So ED's hop rule may put ED in Husain and Louko's leaking case.** Whether it does depends on how ED's short-wavelength modes actually travel, which no attempt has worked out.
- **Recorded as a risk, not a conflict.** It's the fine-tuning leak of A4 C84, now showing up in the very step Jacobson needs.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **U-Q1** | **Is ED's temperature independent of heat and entropy,** not defined as their ratio? | **Yes** | Otherwise the first law is empty and nothing is derived (U-B) |
| **U-Q2** | **Do ED's vacuum relations look the same to every uniformly moving body at horizon scales,** as a labelled assumption? | **Yes, labelled.** It is exactly what Unruh's temperature needs, and it carries the preferred-frame hole openly | ED's meanings don't supply it. Labelling it keeps the dependence visible |

## Draft exit rule (Allen to confirm)

- **If thermality at a/2π follows from ED's meanings with only S′:** record **"second input supplied"**.
- **If it needs U-Q2's emergent boost invariance** (the expected case on paper): record **"Unruh's temperature inherited, as an explicit assumption carrying the preferred-frame hole"**. Road J closes with **one input supplied** (C17).
- **Husain and Louko's leak is recorded as a named risk.** Any later check of how ED's short waves travel gets its rules and expected results written first. If ED's decided meanings force slower-than-light short waves, the risk becomes a conflict, with its source named.
- **Dimensional arguments don't count.**
- **No model is built at this step.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide U-Q1 and U-Q2** and confirm the exit rule; record road J's close | Road J will have done what it can on paper |
| **(b)** | **Then a short dispersion check,** with rules first: how do waves travel in ED's hop rule? Does anything go slower than light? | It turns C20's risk into a yes or no |
| **(c)** | **Or turn to the particle repair** (A4 leads L1 and L3) | Attempt 4's standing conflict |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C18 | Bisognano–Wichmann theorem and the modular-flow formulation of the Unruh effect, as described in Scholarpedia "Unruh effect", arXiv:2403.18937, arXiv:math-ph/0604023; Campo and Obadia, arXiv:1003.0112; Husain and Louko, "Low energy Lorentz violation from modified dispersion at high energies", *Phys. Rev. Lett.* 116, 061301 (2016), arXiv:1508.05338; Louko and Upton, *Phys. Rev. D* 97, 025008 (2018), arXiv:1710.06954; storage-ring and experimental-status discussions (arXiv:hep-th/0101054; "Notes on the experimental observation of the Unruh effect", arXiv:2205.06591); Hu et al., "Quantum simulation of Unruh radiation", *Nature Physics* (2019) | Listings and abstracts |
| — | C2, C13, C17 (this ledger); A4-ledger C84, C87, note 13 | This and earlier ledgers |

**Update (D8):** Allen accepted U-Q1 and U-Q2 and closed road J. **Verdict: Unruh's temperature inherited, as an explicit assumption carrying the preferred-frame hole** (C22). **Road J closes with one input supplied** (C17). The slow-short-wave risk goes to a dispersion check.

**Update (RD8):** the dispersion check is in [Dispersion_Check.md](Dispersion_Check.md) (note 6): no conflict, and three constraints on any future 3D hop rule (C25).
