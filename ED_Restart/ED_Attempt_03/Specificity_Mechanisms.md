# Where specific numbers come from

*ED_Attempt_03, note 1. 2026-09-15 (RD1). Ledger: C1–C6. A thinking and literature note; no model.*

## The question

Theories are good at explaining **kinds** of behaviour. Particular numbers usually get measured and plugged in: the electron's mass, a force's strength, a mixing angle.

**A source of specificity is something inside a theory that forces one particular value.** Two attempts showed that ED, like its cousins, gets the kinds of behaviour right. So this note asks: what are the known ways a theory pins down numbers, and which could ED have?

## The known ways (literature, C1–C4)

| way | how it works | example | class (Allen's frame) |
|---|---|---|---|
| **Attractor in the flow** | As you change the energy scale, a coupling gets pulled toward the same value almost whatever it started at | The top quark's coupling: Pendleton–Ross fixed point and Hill's quasi-fixed point make its low-energy value nearly independent of its high-energy value (C1) | **Gradient** |
| **Sitting at an edge** | The state sits right at a boundary, for example two vacua exactly balanced, and that condition fixes the numbers | Froggatt and Nielsen (1996) assumed balanced vacua and got top 173 ± 5 GeV and Higgs 135 ± 9 GeV; the measured Higgs puts our vacuum near the edge of stability (C2) | **Boundary** |
| **A fixed point where a coupling must sit** | At very high energy a coupling is forced to a special value, and that fixes it at low energy | Shaposhnikov and Wetterich (2010) got a Higgs mass of 126 GeV from a fixed point at zero in asymptotically safe gravity, before the 2012 measurement of about 125 GeV (C3) | **Boundary** |
| **Symmetry and its special points** | A symmetry fixes ratios or angles, or the state sits at a point the symmetry singles out | Modular flavour symmetry's special points (A2 note 4); 120° angles from three-fold symmetry | **Relation** |
| **Counting and whole numbers** | Topology or quantization only allows whole numbers | Windings, charge quanta, flux quanta | **Relation** |
| **No source: many options plus selection** | Counting allows a huge number of possibilities; which one we're in isn't forced | String theory's landscape of flux vacua (Bousso–Polchinski), with selection often anthropic (C4) | None |

**Two honest notes on the examples:**
- **They're mixed successes.** The Pendleton–Ross value came out lower than the top mass we measure. Froggatt–Nielsen's Higgs value was about 10 GeV high. Shaposhnikov–Wetterich landed close, but rests on assumptions about gravity that aren't established.
- **Getting a number right isn't proof of the mechanism.** Look-elsewhere applies here too.

## What ED's structure has already fixed (C5)

Across attempts 1 and 2, ED did pin some things down:

| what got fixed | how | source |
|---|---|---|
| **The probability rule** (amplitude times conjugate) | Forced by Gleason's theorem plus no signalling | A2 note 2 |
| **The fair coin** | The only three-channel coin with equal odds, up to relabelling and phases | A2 note 5 |
| **Windings are whole numbers** | Topology | A1 theorem |
| **The feedback's strength** | Capped by conserving the motion passed into committed matter | A2 notes 7–8 |

**The pattern:** every one came from a **constraint** (a uniqueness theorem, a conservation law, a count), not from something settling where an attractor pulls it. That's also what closed the handedness question: a constraint fixed the feedback strength, and at a value too low for a hand.

## Putting it together (C6)

- **The mechanisms sort onto relation–gradient–boundary.** Attractors are gradient-type. Edges and fixed points are boundary-type. Symmetry and counting are relation-type.
- **Attempt 2 found the unexplained numbers cluster in relation and boundary** (A2 note 3). Those are exactly the classes where constraint-type mechanisms live.
- **ED's own successes are constraint-type too.**

**So if ED has a source of specificity, the evidence points to constraints rather than dynamics:**
- **boundaries:** where a state has to sit;
- **counts:** what's allowed to be whole-numbered.

ED has one boundary-type ingredient that no earlier note tested as a source of numbers: **the horizon.** Attempt 1's rebuilt draw defines "final" as out of reach of every future path, with a capacity of about 10¹²². That's a boundary fact built into ED's meaning.

**A caution to keep in front:** it's easy to take a big number like 10¹²² and find matches. Any step here has to ask what the horizon *constrains* before looking at what numbers come out.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Boundary-class literature map:** vacuum near-criticality, the cosmological constant, horizon and holographic bounds, and what each constrains | The cluster attempt 2 never mapped (A2 note 3, option b), and where ED's horizon lives |
| **(b)** | **What ED's horizon constrains:** from ED's own definition of the draw, what does "out of reach of every future path" force, before any numbers | ED's one untested boundary-type ingredient |
| **(c)** | **Counting in ED:** what in ED's structure is forced to be whole-numbered (channels, windings, records at threshold), and what that allows | The relation-class route |

**Proposal: (a), then (b).** Map the boundary class first, so ED's horizon is judged against how boundary mechanisms actually work, not against number matches.

**Update:** (a) is done ([Boundary_Class_Map.md](Boundary_Class_Map.md), note 2). One correction to (b) came out of it: ED's 10¹²² is 1/Λ taken from observation, so the horizon's size can only be an input.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C1 | Carena, Olechowski, Pokorski, Wagner, arXiv:hep-ph/9309293 (1993), describing Pendleton–Ross and Hill's fixed points for the top Yukawa coupling | Search listing; original papers not read |
| C2 | Froggatt, Nielsen, "Standard model criticality prediction: top mass 173 ± 5 GeV and Higgs mass 135 ± 9 GeV", *Phys. Lett. B* 368, 96 (1996); Degrassi et al., *JHEP* 08 (2012) 098; Buttazzo et al., "Investigating the near-criticality of the Higgs boson", *JHEP* 12 (2013) 089 | Search listings |
| C3 | Shaposhnikov, Wetterich, "Asymptotic safety of gravity and the Higgs boson mass", *Phys. Lett. B* 683, 196 (2010), arXiv:0912.0208 | Abstract via search listing |
| C4 | Douglas, "The string theory landscape", *Universe* 5, 176 (2019); Denef, Douglas, arXiv:hep-th/0404243; nLab, "landscape of string theory vacua" | Search listings |
