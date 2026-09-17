# G35: what counts as an interaction that triggers a draw?

*2026-09-13. Ledger: C103–C119. Follows [A_vs_D.md](A_vs_D.md). Since RD26, interaction is the only thing that makes a pattern draw, so this is now the heart of the rule.*

**Allen's picture:** "when two patterns meet… not one pattern meeting the committed world", then "this is more like photon–photon interactions".

---

## 1. What experiments say, in plain words

### Fact 1: two patterns meeting does not, by itself, make a draw

| what meets | what happens | ledger |
|---|---|---|
| Two light beams crossing in empty space | They pass straight through each other. Light scattering off light is forbidden in classical physics. It was first seen directly only in 2017, in 13 events at the LHC, using the most extreme electromagnetic fields available | C103 |
| Two single photons arriving together at a half-silvered mirror | They interfere with *each other* and leave together (the Hong–Ou–Mandel effect). No draw, no record | C105 |
| Photons made to interact through a cloud of excited atoms | They pair up, attract, and come out **entangled**. A strong interaction, and still no draw | C106 |
| Neighbouring atoms made to collide in a lattice | They become entangled, then **disentangled again**, smoothly, depending on the collision | C107 |
| An atom handing a single photon to a mirror-box and taking it back | The photon goes back and forth many times without the pattern breaking | C108 |
| Qubits in a quantum processor | Billions of gate interactions, one draw at the end | C101 |

**So Allen's instinct, as far as it goes, is right:** the clean case is two patterns meeting. **What experiments show is that such meetings *hinge* the patterns together (entangle them) rather than drawing.**

### Fact 2: interference is lost exactly to the extent a meeting leaves a distinguishing mark somewhere else

- **Atoms hit by single photons** (Chapman 1995, C109). An atom travels both paths at once, and one photon bounces off it. If the two paths are close together compared with the photon's wavelength, the photon can't tell them apart and the fringes stay. Move the paths apart and the fringes fade. Then, surprisingly, they come back at some separations. Pick out only the atoms whose photon went in one narrow direction, and the lost fringes return.
- **The exact trade-off** (Englert 1996, C110): *how visible the fringes are* and *how well the mark could tell the paths apart* obey D² + V² ≤ 1. More mark, less interference, smoothly.
- **Nobody has to look.** Hot C70 molecules lose their interference by giving off heat radiation that nobody detects (C112).
- **Erasers** (C111). A mark can later be read in a way that doesn't reveal the path. Sorting the results by that reading brings the fringes back.

### Fact 3: once a mark exists elsewhere, *where* the draw happens can't be seen from one side

This follows from no-signalling (C52) and ED's local draw (RD22). One side's statistics can't depend on whether or when the far part is drawn.

**Erasers don't undo a draw.** They work by sorting records *after both parts have drawn*, which is exactly RD22's picture. **D1 is safe:** nothing is ever taken back.

---

## 2. What that does to G35

**G35 splits into two questions** (C119):

| | question | status |
|---|---|---|
| **G35a** | Which meetings count? | **Settled by experiment.** Meetings hinge. What removes interference is a distinguishing mark left elsewhere, smoothly, by D² + V² ≤ 1. |
| **G35b** | What finally turns a hinge into a draw? | **Not settled by any experiment.** Fact 3 shows why: the answer can't be seen in one side's statistics. This is the famous *measurement problem* in ED's words. |

**Proposal for G35a (RD27 if adopted):** *two patterns that meet hinge into one pattern. A meeting by itself never draws.*

---

## 3. Options for G35b

| | option | verdict |
|---|---|---|
| **(i)** | Every meeting draws | **Ruled out** by every row of Fact 1 (C114) |
| **(ii)** | A draw happens when a whole unit of amount changes hands (links to RD25: outcomes come in whole units) | **Ruled out** (C116). A single photon passes back and forth between an atom and a cavity without breaking (C108), and Chapman's fringes come back, which a draw that fixed the atom's path could not allow |
| **(iii)** | A draw happens when a hinge reaches a locus at full budget (the "too many balls in the roller" picture) | **Ruled out as the everyday trigger** (C104, C117). To match gravity's clock slowing, used budget is about GM/(rc²). That gives 7 × 10⁻¹⁰ at Earth's surface, 2 × 10⁻⁶ at the Sun's, 0.17 at a neutron star's, and about 10⁻²³ for one electron at a Planck-length step. The cap is reached only near black-hole conditions, not in any lab |
| **(iv)** | A draw is relative: every meeting is a draw *for the two parties*, and not for anyone else (Rovelli's relational quantum mechanics, C113) | **Closest to Allen's first picture,** and it has no free numbers. **But it conflicts with D1** (C118): a draw that holds for one party can still be undone for another, so a commitment would not be a step that can't be taken back |
| **(v)** | **A draw happens when a meeting leaves a mark that can no longer be brought back together** | **Fits every experiment above and matches D1 word for word:** a draw *is* the step that can't be taken back. **Weakness:** "can no longer be brought back together" isn't yet exact, and until it is, the idea is circular (new gap G36) |

**Proposal for G35b: (v), as the working rule, with G36 open.**

**What (v) costs.** Here ED says the same as standard quantum physics with decoherence. ED's own testable content still has to come from the budget and gravity, clock ticks and locus birth (as already recorded in [A_vs_D.md](A_vs_D.md)).

**What it gains.**
- No free numbers.
- No conflict with D1, RD22, RD25 or RD26.
- Version 1 code can model it directly: a detector part that always draws what reaches it.

---

## 4. A lead for G36 (exploration, not a proposal)

**G36 asks:** what does "can't be brought back together" mean, exactly, with no number? One candidate uses only ED's graph:

> **A mark can't be brought back when some of it is out of reach, so that no future path on the graph can ever bring it to meet the rest.**

**Heat radiation escaping to deep space is like that.**

**How it ties to G29b.** On a fixed, finite graph everything could eventually meet again, so nothing would ever draw. On a graph where loci are still being born (RD21), regions can move permanently out of reach. That would tie *when draws happen* to *locus birth*, a real link between two open pieces of ED.

**Risk.** It puts the draw late and far away, and makes the everyday draw depend on the large-scale graph. Fact 3 says lab statistics would be the same, but it needs a literature gate before anything is built on it.

---

## Questions for Allen

1. **G35a:** do you accept *"patterns that meet hinge; a meeting by itself never draws"*?
2. **G35b:** go with **(v)**, a draw when a mark can't be brought back together? Or does **(iv)**, the relative draw, fit your picture better, even at the cost of D1?
3. **Your photon picture check:** photons pass through each other almost always, and when they are made to interact they entangle rather than draw. Does that match what you meant?

## Sources checked

| ledger | source | how it was checked |
|---|---|---|
| C103 | ATLAS Collaboration, *Nature Physics* 13, 852 (2017), arXiv:1702.01625 | Abstract |
| C105 | Hong, Ou, Mandel, *PRL* 59, 2044 (1987) | Search listing only |
| C106 | Firstenberg et al., *Nature* 502, 71 (2013) | Abstract |
| C107 | Mandel et al., *Nature* 425, 937 (2003), arXiv:quant-ph/0308080 | Abstract |
| C108 | Brune et al., *PRL* 76, 1800 (1996) | Search listing only |
| C109 | Chapman et al., *PRL* 75, 3783 (1995) | Abstract wording from a search listing |
| C110 | Englert, *PRL* 77, 2154 (1996) | Abstract wording from a search listing |
| C111 | Scully and Drühl, *PRA* 25, 2208 (1982) | Bibliographic details only |
| C111 | Kim et al., *PRL* 84, 1 (2000), arXiv:quant-ph/9903047 | Abstract |
| C112 | Hackermüller et al., *Nature* 427, 711 (2004), arXiv:quant-ph/0402146 | Abstract |
| C113 | Rovelli, *Int. J. Theor. Phys.* 35, 1637 (1996), arXiv:quant-ph/9609002 | Abstract |

---

## Decided (2026-09-13, RD27 and RD28)

- **G35a (RD27):** patterns that meet hinge into one pattern. A meeting by itself never draws.
- **G35b (RD28):** option (v). A draw happens when a meeting leaves a mark that can no longer be brought back together.
  - Only what the mark distinguishes gets fixed, and only for the part that interacts (RD22).
  - The exact meaning is open (G36).

## Allen's picture: forced commitment (D10)

**Allen:** measurement has always meant a pattern meeting a committed part of the world and being forced to commit; possibilities collapse to one outcome. "Forced commitment" was the old term.

**The term survives. It only needs one condition added** (C124):

> A pattern is forced to commit when it leaves a **distinguishing mark** in a committed part of the world, and that mark **can't be brought back together**.

**Why the condition is needed.**
- Light going through a glass lens meets committed matter, yet nothing is forced: the glass ends up the same whichever way the light went.
- A photon hitting a detector leaves a mark that spreads into billions of atoms and heat, and can never be gathered back.

**What makes a part of the world "committed".** Marks in it spread beyond bringing back. That describes large, warm, open things, like detectors, air and walls.

**What changed from the old version:**
- Forcing needs a mark, not just contact.
- A lone pattern is never forced by spreading (RD26).

**This is close to a famous idea.** Bohr, and Wheeler after him, said a quantum event isn't finished until it is brought to a close by an irreversible act of amplification (C122). Zurek's decoherence picture is the modern version: the environment "monitors" the system (C121). **ED's difference is that the draw is real** (D1). In the decoherence picture, by contrast, nothing is ever actually drawn.

## Literature gate for G36, first pass

**The lead was:** a mark can't be brought back when part of it is out of reach of every future path.

**Known in part.**
- **Bousso and Susskind (2011, C120):** use the edge of the region an observer can ever reach, its horizon, as a one-way membrane that decides what counts as "the environment".
- **Nomura (2011, C123):** a similar horizon-based picture.
- Both papers treat outcomes as branches of many worlds, not as real draws.

**A real risk for ED** (C125). Bousso and Susskind find that if the reachable region has a finite size, the horizon's one-way-ness isn't perfect, so outcomes are never *completely* definite.

For ED that means:
- **If** the part of the graph anyone can ever reach is effectively finite, then "can't be brought back" is only approximately true, and D1's draws would be approximate too.
- **ED escapes this only if** locus birth (RD21) keeps the reachable region growing without limit.

That is now the key question for G36. It links directly to G29b (what makes new loci, and how often).
