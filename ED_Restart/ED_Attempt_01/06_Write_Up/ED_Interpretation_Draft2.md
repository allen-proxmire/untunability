# Event Density: an interpretation with a runnable rule

*Draft 2, 2026-09-14 (revised from draft 1 at Allen's request). Written under the exit rule (RD52, RD55): three attempts to make ED fix its one missing ingredient failed, so ED is written up for what it honestly is. Every claim below points to the ledger (`01_Ledger/Claims.md`, 301 claims; `Assumptions.md`, RD1–RD55 and D1–D18). The 36 computational checks rerun with one command (`01_Ledger/checks.txt`).*

---

## Summary

**What Event Density (ED) is.** ED pictures the world as a growing web of places (loci), with one feature built in: time runs one way. Things spread across the web as waves until a meeting leaves a mark that can't be brought back. That irreversible mark is a real event, a *commitment*. Commitments use up a budget that slows clocks and motion near mass, and the web keeps growing as new loci are born.

**What it does.** ED has been built as a definite, runnable rule and tested against known physics.

| area | result |
|---|---|
| **Quantum** | Reproduces interference, the which-path/visibility trade-off, the quantum eraser, and no faster-than-light signalling |
| **Gravity** | Reproduces general relativity at every order checked: light bending, Mercury's perihelion, the Nordtvedt test |
| **Dark energy** | Gives a plain cosmological constant, which fits current distance data |

**What is ED's own.**
1. **A handedness theorem.** A world whose rules look the same in a mirror can't have handedness written into those rules; any handedness must be chosen by the state. One-way time is what makes handedness possible at all.
2. **A physical account of measurement.** A draw happens when part of a mark has left the reach of every future path. Draws are exact up to the capacity of the cosmic horizon, about 10¹²².
3. **A documented demonstration** that ED's rule *can* hold a handed state chosen by chance, but only with three ingredients the rule doesn't yet supply.

**What ED is not (yet).** Every fit matched an existing measurement, and every distinctive variant ED tried either failed against data or failed to follow from ED's own primitives. Those failures are recorded here in full.

**Why it may still be worth reading.**
- **A careful attempt.** It develops an irreversible-substrate picture of physics with tests specified before running, recorded failures and literature checks at every step.
- **Its negative results are useful:** what doesn't work, and why.
- **Its one theorem is clean.**

---

## 1. Starting commitments

ED began as a philosophical picture (*Contrast First Ontology*, D16) and a list of primitives, written in prose. The ones that carry weight here:

| primitive | content | how it's used |
|---|---|---|
| **P11** | Commitment is irreversible: no operation undoes it | Time runs one way; draws are real events |
| **P03, P05, P07** | Loci are uniform; channels are distinct; transport is local | The graph and its lanes |
| **P09** | Each channel carries a U(1) phase | Complex hop amplitudes |
| **P04** | Channels carry non-negative bandwidth | The budget |
| **P12** | Each chain carries a stability score, Σ = Coh − Str − Grad | Read as a preference for how phases and links settle (RD33); not fully defined |
| **A1** | No primitive is a mirror reflection | ED's rules are mirror-symmetric |

**Allen's picture of measurement (D10).** Measurement is "a pattern meeting a committed part of the world and being forced to commit". The rule makes that exact (section 2.3).

**Commitment is not memory (D1).** A commitment is a step that can't be taken back, but no locus keeps a record of past traffic. Any feedback must come from the present state.

---

## 2. The rule as it stands

### 2.1 Spreading

- **Lanes.** Each locus has an Internal channel and a pair of lanes per direction. In the 1D test bed that means Right and Left.
- **Spreading.** Patterns spread by a local, reversible generator: lanes hop to neighbouring loci and mix at each locus with a parameter-free (Grover) coin (RD13, V0-D1).
- **Rest term.** A positive rest term represents concentrated commitment (D7).
- **3D is imposed, not derived.** Neither random splitting nor P12-driven rewiring of links produced three dimensions (C154, C188, RD34).

### 2.2 Meetings and marks

- **Meetings don't draw.** Patterns that meet hinge into one joint pattern (RD27).
- **Marks cost interference.** Interference falls exactly as much as the meeting's mark distinguishes the paths (D² + V² ≤ 1; C110, C114, C115).
- **No spontaneous draws.** A lone pattern never collapses by spreading (RD26). Interference survives in experiments over large distances and masses (C65, C92, C98).

### 2.3 The draw

**Meaning (RD28, RD50).** A draw happens when a meeting leaves a mark that can no longer be brought back together, meaning part of the mark has left the reach of every future path.
- **Why it's exact only up to 10¹²².** With constant dark energy (section 2.5) that horizon is permanent, with a capacity of about 10¹²² distinguishable states. Within a finite capacity, decoherence isn't completely irreversible (C120, C143).
- **Published homes:** Bousso and Susskind's causal-diamond membrane (C120); horizon decoherence of superpositions by Danielson, Satishchandran and Wald (C284).

**What a draw fixes.** Only the record the mark holds, and only for the part that interacted (RD22). Everything inside that record stays coherent. Fixing more, for example every part of an entangled pattern at once, would allow faster-than-light signalling (C81).

**The working model (not part of ED).** In simulations, a mark counts as unrecoverable once it is copied into 3 near-perfect independent fragments of committed matter. That is redundancy in Zurek's sense (C285). The model:
- reproduces partial marks, the eraser and no signalling, and keeps coherence inside the record (C291);
- **is wrong about erasing three or more copies,** where standard quantum physics would restore interference (C291, D8b). It must not be used for claims about reversibility.

**Finality doesn't change population behaviour.** Drawing records and keeping them coherent give identical averaged dynamics. Finality matters only for erasure (C293).

**Still assumed.** Draw probabilities (amount squared) and whether a draw uses budget (C286, C292).

### 2.4 The budget and gravity

**The budget.** Each locus has a used budget U, set by committed mass and its neighbours, with q = 1 (RD14, RD23). In 3D it falls off like 1/r only with q = 1 (C84, C85).

**Slowing.** Ticking and internal change slow by e^(−U); moving between loci slows by e^(−2U) (RD35, RD36).

**What each step matched.**

| step | matches | ledger |
|---|---|---|
| Moving pays twice | Light bending (γ = 1) | C196–C199 |
| Rate e^(−U) rather than 1 − U | Mercury's perihelion (β = 1) | C201–C203 |
| The budget feeds back on itself with GR's post-Newtonian weights | The Nordtvedt test (a linear budget fails by about 10⁴) | C207, C208, RD37 |

**Verdict.** ED's gravity is general relativity in budget language. Each step was chosen to match a measurement.

### 2.5 Locus birth and dark energy

**Constant births.** Loci are born everywhere with a constant chance per step (RD29, RD43). If one step is a Planck time and a locus a Planck volume, that chance must be about 2.9 × 10⁻⁶¹ per step to give today's dark energy.

**The same 10¹²².** That chance squared gives Λ l_P² ≈ 2.85 × 10⁻¹²² (C211). It's the same number as the horizon's entropy and Lloyd's count of cosmic operations. They agree because the horizon's size is set by the universe's age (C272, C273). That is arithmetic, not evidence.

**What ED says about dark energy: nothing new.** Its one free number is the cosmological-constant problem in new clothes. Distinctive alternatives were tested and failed (section 5).

---

## 3. What the rule reproduces

| result | how checked | ledger |
|---|---|---|
| Interference, partial which-path marks (D² + V² ≤ 1), the quantum eraser, reversible hinging | Rule versions 1 and 3 (the rebuilt draw) | C127–C129, C291 |
| No faster-than-light signalling with local draws | Rule tests | C81, C291 |
| 1/r budget in 3D; the cap is reached only near black holes | Computation | C84, C85, C104 |
| Light bending, Mercury, Nordtvedt | Analytic and numerical post-Newtonian checks | C196–C208 |
| Constant dark energy fits DESI DR2 BAO and combined data | χ² fits | C221, C246 |

**These are requirements met, not evidence for ED.**

---

## 4. The handedness theorem and its status in ED

### 4.1 The theorem (public; proved)

**Setup.** Transport with N channels on a 1D lattice, H(k) = Σ_{m=−R}^{R} e^{imk} C_m.

**Statement.**
1. If transport is symmetric under a reflection (S H(k) S⁻¹ = H(−k), S² = 1), the winding number of det(H(k) − E) about any point is zero, for every N, R and S.
2. If transport is Hermitian (reversible), the winding is zero as well.
3. Forward-only hopping has winding N, so the invariant isn't trivially zero (C1–C4).

**Plain reading.** One-way time makes a net handedness *possible*; mirror-symmetric rules keep it out of the laws; so any handedness is chosen by the state.

**Novelty.** The mathematics is elementary. A closely related statement (reflection with transpose) is published (C30). The theorem is a relative of Nielsen–Ninomiya (C236) and of the non-Hermitian escape from it (Bessho and Sato, C239). Whether the exact form is published is open (C12). It is posted publicly with a check script.

### 4.2 Does ED's rule deliver the theorem's assumption? (A5)

The theorem assumed that ED's irreversibility makes transport one-way (A5). Working that out in ED's actual rule:

| finding | ledger |
|---|---|
| **ED's spreading is reversible and two-way symmetric** (it can be gauged real). No draw-rate pattern can give winding, and draws that only mix wipe out any flow | C269, C275 |
| **A lasting hand, chosen by chance, with the theorem's winding, appears only with three ingredients:** a standing lane-loop phase (an arrow of time in the phases, neither 0 nor π); meetings that carry motion into committed matter; and a response steeper than the loop's threshold. Settings chosen to amplify, labelled as tuned: 10 of 10 runs held a hand, 6 one way and 4 the other | C281–C289 |
| **The hand survives the rebuilt draw,** run for run, and doesn't depend on draws being final | C293, C294 |

**So A5 is not delivered by ED's rule as written. It is delivered only under choices ED doesn't make.**

### 4.3 Can ED fix the missing ingredient? Three attempts (the exit rule)

| attempt | what was tried | result | ledger |
|---|---|---|---|
| **1** | P12's coherence as read (phases close to 0 around small loops) | Every small-loop phase fixed at 0: time-reversal symmetric, no hand | C296 |
| **2** | A "close at π" coherence, frustrated in 3D, picks a chirality in the lane mixings; put that into the rule | Every steady state carries zero flow; no hand | C297, C299, C300 |
| **3** | Coherence also scoring the smallest square loops in space | Lane loops stay at 0 or ±π at every weight | C302 |
| **(literature)** | A phase from mass or proper time (Feynman's checkerboard, Dirac quantum walks) | Lane loops at π; no hand | C295 |

**Outcome (C303).** ED does not fix the ingredient its hand needs. Under the exit rule, the handedness line ends here.

---

## 5. Negative results

Recorded because they're informative, and because a program that lists its failures is easier to trust.

| idea | why it failed | ledger |
|---|---|---|
| **Every meeting draws** | Contradicts crossing light, two-photon interference, entangling collisions | C114 |
| **A draw when a locus's budget is full** | The cap is reached only near black holes | C117 |
| **Spontaneous draws when a pattern is too thin** | Interference survives far beyond any such scale | RD26, C98 |
| **One slowing factor for everything** | Gives half the measured light bending | C196 |
| **A linear budget** | Fails the Nordtvedt test by about 10⁴ | C207 |
| **Random splitting or P12 rewiring as the origin of 3D** | Neither gives 3D | C154, C188 |
| **Everpresent (fluctuating, one-sided) births as dark energy** | Ruled out by DESI distances (best Δχ² = 77) | C221–C223 |
| **Horizon-set births (holographic dark energy)** | Disfavoured once supernovae and the CMB are added (Δχ² = +32.8) | C246–C250 |
| **Draw-rate feedback as a source of handedness** | Draws only mix; reciprocity forbids winding | C275, C277 |
| **Phases set by the flow** | Zero loop gain at zero flow | C282 |
| **A seed deciding the hand over a large space** | Only regions in contact are decided; hands form everywhere and merge | C267, C268 |
| **Coherence readings as the source of the standing phase** | Three attempts failed | C296–C303 |

---

## 6. Neighbouring programs

| program | relation to ED |
|---|---|
| **Causal set theory** (Bombelli, Lee, Meyer, Sorkin; Rideout and Sorkin) | The closest neighbour for spacetime: discrete and growing. The everpresent-Λ idea is Sorkin's (C140, C210). ED adds waves spreading on the web and a budget for gravity |
| **Decoherence and quantum Darwinism** (Zurek) | ED's measurement agrees with it operationally. ED adds that the final draw is a real event, set by the horizon (C121, C285) |
| **Horizon-based accounts of measurement** (Bousso and Susskind; Danielson, Satishchandran and Wald) | ED's draw meaning has its home here (C120, C284) |
| **Objective-collapse models** (GRW, Penrose) | ED is *not* one: it has no spontaneous collapse, and so adds no deviations from quantum mechanics |
| **Quantum walks and Dirac cellular automata** (Meyer; Bialynicki-Birula) | ED's spreading is a quantum walk. Their mass-as-coin structure is why a mass phase gives no hand (C295) |
| **Spontaneous chirality** (Frank; Viedma; 1D flocking; reservoir-engineered nonreciprocity) | The mechanism behind ED's tuned hand is known physics (C256, C262, C264, C276) |
| **Philosophy** (Hegel's being and becoming; the Past Hypothesis; Penrose's conformal cyclic cosmology) | Homes for ED's picture of a uniform start and end, with a real entropy tension (C259–C261, C265, C266) |

---

## 7. Open problems

| problem | ledger |
|---|---|
| **A lane-loop phase from ED's primitives:** the one ingredient that would make ED's handedness a consequence | C303 |
| **Draw probabilities** (assumed); whether a draw uses budget | C286, C292 |
| **Why moving and ticking split Pythagorean-style;** an ED reason for GR's weights | G26, RD37 |
| **3D, and particle properties** (spin, charge, generations): no account | C189 |
| **Units:** time-dilation size, collapse bounds, no preferred frame (never tested on the lattice) | T3, T5, T6 |
| **Outside review** of the handedness theorem: a packet is ready | C12 |

---

## 8. Method

Recorded because it's what makes the rest believable.
- **Tests specified before every run,** in the check script or spec.
- **Every failure recorded,** including Claude's own design errors and test-code bugs, alongside the physics failures.
- **Literature checks before claims.** Sources are marked by how they were checked (abstract, paper text, or search listing only).
- **Settings chosen to make something work are labelled as tuned.**
- **An exit rule agreed in advance** (RD52), and applied (RD55).

---

## 9. What would reopen ED

ED should be reopened if any of these appears:
1. **A lane-loop phase neither 0 nor π that follows from ED's primitives,** not chosen. The tuned-test machinery is ready to test it (C288, C293).
2. **A derivation of draw probabilities** from the horizon meaning.
3. **A derivation of 3D,** or of any particle property.
4. **A reviewer finding the theorem's exact form new and useful,** or finding an error.

---

## Appendix: rerunning the work

- **All checks:** `python 01_Ledger/run_checks.py` (36 checks; some take minutes).
- **Key scripts:**
  - `04_Ways_Forward/Commitment_Rule/v3_draw/run_tests_draw.py` (rebuilt draw);
  - `v4/run_tests_v4.py` (tuned hand on the rebuilt draw);
  - `v2b/gain_check.py`;
  - `Standing_Phase/attempt1_coherence.py`, `attempt2_frustration.py`, `attempt3_squares.py`.
- **The public theorem:** https://github.com/allen-proxmire/event-density-streamlined (`tools/check_result.py`).

*Draft 2: for Allen's review. Wording, emphasis, and whether to include the philosophy section are his calls.*
