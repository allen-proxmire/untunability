# Road J, part 1: the Jacobson route (on paper)

*ED_Attempt_05, note 2. 2026-09-15 (RD2, D1). Ledger: C2–C6. Literature and reasoning; nothing computed. **Meaning questions J-Q1–J-Q5 have least-structure defaults for Allen to accept, change or veto; the exit rule is a draft for Allen to confirm.***

## Why this road

The inputs table ([What_ED_Needs.md](../What_ED_Needs.md)) found one place where ED could **cross off an input** rather than relabel one: Einstein's equations, via Jacobson.

## Jacobson's chain (C2)

**Jacobson (1995)** gets Einstein's equations from:
1. **Entropy proportional to horizon area,** S = ηA.
2. **Unruh's temperature:** an accelerating observer sees the vacuum as warm, T = κ/2π.
3. **Heat:** the energy flowing across a small local horizon.
4. **The first law, δQ = T dS,** required for *every* small local horizon through every point, in every direction.

**Out comes Einstein's equation,** with Newton's G set by the area coefficient η.

**Jacobson (2016):** the same result from "the entanglement in small balls of space is at its maximum, at fixed volume, in the vacuum".

**Where each input sits:**

| input | in physics |
|---|---|
| Entropy ∝ area | Assumed; motivated by black holes and entanglement |
| Unruh temperature | Needs Lorentz invariance |
| First law | Standard thermodynamics |
| "Every direction" | Needs no preferred frame |
| The coefficient η | Sets G; not explained |

## Where area entropy comes from in physics (C3)

| source | what it says |
|---|---|
| **Entanglement** (Bombelli, Koul, Lee, Sorkin 1986; Srednicki 1993) | The entropy of quantum fields hidden behind a surface grows like the surface's **area**, not the volume. The coefficient depends on the short-distance cutoff |
| **Causal sets** (Dou and Sorkin 2003) | **Counting the causal links that cross a horizon,** near a slice of spacetime, gives a number **proportional to the horizon's area**. The links act as "horizon atoms" |
| **The coefficient and G** (Susskind and Uglum 1994; Jacobson 1994, induced gravity) | The cutoff-dependent part of the entropy goes together with Newton's G. The fields that make the entropy are the same fields that set G |
| **Unruh without Lorentz invariance** | Unruh's thermality relies on Lorentz invariance and fails for general frame-dependent dispersion (Campo and Obadia 2010). Small corrections keep it at low energy, and some treatments with a preferred-frame field recover it |
| **The old ED repo's reading** (`Paper_KhronometricEquationOfState_Jacobson`) | Wrote out the local derivation for its own gravity class. It rests on gravity papers that the outside review found don't hold, and its area-law result "assumes the emergent geometry" |

## ED's version (C4)

**The chain in ED's words:**
1. **The entropy of a surface is the count of relations crossing it** (J-Q1, J-Q2).
2. **In a pattern where each locus has finitely many nearby neighbours, that count grows like the surface area.** That's the ball-cut: the geometry of any short-range pattern. ED already decided finite neighbours (A4 D32).
3. **Heat is the motion and energy carried across the surface** by matter and influence. Influence carries motion (A4 D30).
4. **Temperature is Unruh's,** inherited at low energy (J-Q4).
5. **The first law for every local horizon** gives Einstein's equation. **G is set by how many relations cross each unit of area,** a number tied to ED's grain.

**What would be ED's own:** in physics, "entropy ∝ area" is an assumption. **In ED it would follow from two meanings:** entropy counts relations crossing a surface, and neighbours are finite and nearby. **The form would be supplied; the coefficient would stay inherited.**

**A trade-off worth seeing clearly:**
- **Finite neighbours** is exactly what gave ED a rest frame (the preferred-frame wall, A4 C87).
- **It's also exactly what makes the count an area law.** Causal sets have no rest frame but infinitely many links, so Dou and Sorkin had to restrict their count to links near a slice.
- **So the choice that creates ED's rest-frame problem is the one that makes Jacobson's input natural.** The pinch moves to Unruh's temperature, which needs Lorentz invariance.

## Pokes (C5)

| | poke | what it means |
|---|---|---|
| **P1** | **Which relations count?** Physics' area law is entanglement: uncommitted correlations. ED's centre is commitments | J-Q1 has real options: all relations, only live ones, or only commitments |
| **P2** | **Unruh needs Lorentz invariance** | The preferred-frame wall is inherited here. The literature suggests low-energy survival is plausible, but ED doesn't derive it |
| **P3** | **"Area" needs geometry.** A surface only has an area if the pattern behaves like space | This is A4's hole H1. A ball-cut on ED's own pattern needs a growth rule |
| **P4** | **The coefficient.** G depends on counting every kind of relation, and physics finds the coefficient depends on the number of field kinds | The number stays inherited |
| **P5** | **Prior art.** Entropy as a count of links (causal sets) and gravity induced by the same fields that carry entropy (Sakharov; Jacobson 1994) are known | ED's version is its own only if the count follows from ED's meaning of relations. Otherwise: consistent, not derived |
| **P6** | **Particles need revision** (A4 D14) | The route doesn't rest on what a particle is; heat only needs matter and influence to carry energy |

## Meaning questions (Allen decides)

| | question | proposed default (least structure) | why |
|---|---|---|---|
| **J-Q1** | **What does ED's entropy of a surface count?** (a) every relation crossing it; (b) only live (uncommitted) relations; (c) only commitments | **(a) every relation crossing it** | No distinction between kinds is the least structure. (b) would match entanglement, (c) ED's centre; both add a rule |
| **J-Q2** | **Is each relation counted once,** whatever it carries? | **Yes** | A commitment carries nothing numerical (A4 D4). A pure count has no weights to fit |
| **J-Q3** | **Is heat the motion and energy carried across the surface** by matter and influence? | **Yes** | Influence carries motion and energy (A4 D30) |
| **J-Q4** | **Is the temperature Unruh's, inherited at low energy,** with its dependence on the preferred-frame wall named? | **Yes** | Anything else would need a derivation that isn't on the table |
| **J-Q5** | **Does the pattern behave like three-dimensional space at horizon scales?** (A4's assumption S, labelled; checked later by a ball-cut on ED's own pattern) | **Yes, as a labelled assumption** | Area needs geometry. Building the pattern is a later, separate step |

## Draft exit rule (Allen to confirm)

**For road J part 2, on paper, with the J-Q answers:**
- **If "entropy ∝ area" follows from J-Q1, J-Q2, finite nearby neighbours (A4 D32) and assumption S alone:** record the form as **"a reason from ED's meanings"** for Jacobson's area input, with the coefficient inherited. Record Einstein's equation overall as **"consistent, not derived"**, since Unruh's temperature and the first law are inherited.
- **If the count needs weights, a choice of which relations made to get area, or long-range relations:** record **"Jacobson's input restated, not supplied"**, and road J closes.
- **If a decided meaning contradicts a step** (for example, the rest frame breaking Unruh beyond small corrections): record the conflict and name the bound.
- **The census:** list the inputs of Jacobson's chain and of ED's version. **It counts as a reduction only if ED's list is shorter by at least the area-entropy input,** with no added free parameters.
- **No model is built at this step.** Any ball-cut model later gets its rules and expected results written first.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide J-Q1–J-Q5** and confirm the exit rule; then road J part 2 on paper | The route is set up; the paper step is short |
| **(b)** | **Change J-Q1 first,** if "every relation" isn't what ED's entropy means to you | It's the load-bearing meaning |

**Proposal: (a).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C2 | Jacobson, "Thermodynamics of spacetime: the Einstein equation of state", *Phys. Rev. Lett.* 75, 1260 (1995), arXiv:gr-qc/9504004; Jacobson, "Entanglement equilibrium and the Einstein equation", *Phys. Rev. Lett.* 116, 201101 (2016), arXiv:1505.04753 | Abstracts and listings |
| C3 | Bombelli, Koul, Lee, Sorkin, "Quantum source of entropy for black holes", *Phys. Rev. D* 34, 373 (1986); Srednicki, "Entropy and area", *Phys. Rev. Lett.* 71, 666 (1993); Solodukhin, "Entanglement entropy of black holes", *Living Rev. Relativ.* 14, 8 (2011); Dou and Sorkin, "Black hole entropy as causal links", *Found. Phys.* 33, 279 (2003), arXiv:gr-qc/0302009; Susskind and Uglum, *Phys. Rev. D* 50, 2700 (1994); Jacobson, "Black hole entropy and induced gravity", arXiv:gr-qc/9404039; Campo and Obadia, arXiv:1003.0112; "Rescuing the Unruh effect in Lorentz violating gravity", arXiv:2312.03070; ED Generative `physics-papers/readings/Paper_KhronometricEquationOfState_Jacobson.md` (read directly) | Listings and abstracts; the EDG paper read directly |
| — | A4-ledger C87, C92, D4, D30, D32; `What_ED_Needs.md` | Earlier ledger |

**Update (D6, RD3):** Allen accepted J-Q1–J-Q5 and the exit rule. Part 2 is in [J2_Jacobson_Part2.md](J2_Jacobson_Part2.md) (note 3).
