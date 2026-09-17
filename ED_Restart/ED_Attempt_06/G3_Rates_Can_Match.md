# Road G, part 3: can rates match on ED's own pattern? (on paper)

*ED_Attempt_06, note 6. 2026-09-15 (RD7). Ledger: C27–C32. Literature and reasoning; nothing computed, no simulation. **Meaning questions G-Q8–G-Q10 and the verdict are for Allen.***

## Where part 2 left it (C27)

**Allen accepted G-Q5–G-Q7 and the exit rule** (D6). Recorded:

> **Road G part 2:** no single candidate favours a resting 3D pattern; the combination (fewest directions with rates able to match) gives the single point d = 3, suggestive, resting on a lattice result, a threshold ratio and a labelled reading.

**Part 3 asks two things:**
- **can "rates can match" be written with ED's own counts,** on a random, finite pattern, without a coupling ratio put in?
- **does the floor (no matching at two dimensions or fewer) survive** there?

## What's known (C28)

| | what it says | source |
|---|---|---|
| **Clusters depend on dimension** | Oscillator lattices with spread-out rates form clusters whose pattern depends on the lattice's dimension | Sakaguchi, Shinomoto, Kuramoto, *Prog. Theor. Phys.* 77, 1005 (1987) |
| **A chain can't lock** | For a chain with random rates, the chance of locking goes to zero as it grows, **unless the coupling grows like √N** | Strogatz and Mirollo, *Physica D* 31, 143 (1988) |
| **Grids** | Phases never sync up to d = 4. **Rates match collectively in d = 3**; the lowest dimension for rate matching is 2 | Hong, Park, Choi, *PRE* 72, 036217 (2005) |
| **Networks** | Beyond grids, what matters is the spectral dimension. **Networks with d_S ≤ 2 can't synchronize**; with d_S > 4, some coupling always syncs them | Millán, Torres, Bianconi, *Sci. Rep.* 8, 9910 (2018); *PRE* 99, 022307 (2019) |
| **Whole numbers** | A pattern that looks the same from every locus (vertex-transitive) and grows polynomially grows with a **whole-number** exponent | Trofimov (1984); with Gromov (1981) |
| **ED's ball-cut** | Relations crossing a sphere grow like its area on a direction-free random pattern | A5 C7, C17; EDG ball-cut exponent 2.008 in 3D |

## On paper (C29)

### The picture

**Take any patch of n clocks in the pattern.**
- **Their rates are a little random,** so the patch as a whole runs fast or slow by a surplus. For independent random differences, the surplus grows like **√n**.
- **The only thing that can pull the patch into line is its neighbours,** through the relations crossing its edge. Each relation can pull only so much (no infinities, D32). **So the most pull grows like the edge count.**
- **The edge count is the ball-cut** (A5 C17). In a d-dimensional pattern it grows like **n^((d−1)/d)**.

**Rates can match across the pattern only if the edge keeps up with the surplus as patches grow:**

> n^((d−1)/d) must outgrow √n, that is, (d − 1)/d > 1/2, that is, **d > 2**.

| dimension | edge vs surplus | rates can match? |
|---|---|---|
| **1** | edge stays 2 points; surplus grows | **Never.** Big enough patches always break away (Strogatz–Mirollo) |
| **2** | edge grows like √n, a tie | **Tie, lost by a hair:** fluctuations tip it against (grids: lowest dimension 2; networks: d_S ≤ 2 can't) |
| **3** | edge n^(2/3) beats √n | **Yes,** for some coupling strength |

### No ratio in the floor

- **The ratio** (how hard a relation pulls, against how random rates are) **only decides whether small patches lock.**
- **The dimension floor comes from exponents alone:** below two dimensions no ratio saves large patches, and above two some ratio works.
- **So "rates *can* match" (G-Q6's wording) needs no ratio.** Whether ED's rates *actually* match needs a real strength, and ED doesn't supply that number.

### What counting on ED's pattern needs

- **The patches that matter are the ones with the least edge for their size.** In a space-like pattern those are balls, and their edge count is the ball-cut.
- **In a small-world pattern, edges are huge and sync is easy.** That's (i)'s wrong-way push again, already set aside.

## Where three comes from, and where it doesn't (C30)

**(ii) pushes toward the fewest dimensions; the floor forbids d ≤ 2.**
- **If dimension can be any number,** there is **no fewest**: 2.1 beats 3, and 2.01 beats 2.1. Fractal patterns with dimension between 2 and 3 pass the floor.
- **Three is the fewest *whole-number* dimension above two.** So the single point d = 3 needs **dimension to be a whole number.**

**What could make it a whole number:**

| source | status |
|---|---|
| **The pattern looks the same from every locus** (Trofimov) | ED's pattern is random, not exactly the same from every locus |
| **"Where things look smooth, the pattern behaves like a smooth space"** (A5 D11's labelled assumption Q) | Smooth spaces have whole-number dimension. **An existing labelled assumption, not a new one** |

**A check on fitting:** the reading "rates," not "ticks in step," was fixed before this step (G-Q6, D6, from A4 D20).
- **If sync meant ticks in step (phases),** the floor would be 4 and the fewest whole number 5, **which doesn't match.**
- **Recorded:** the reading was chosen before the floor was worked out.

## What it means (C31)

- **The floor survives on ED's own terms.** It's written with ED's counts: the ball-cut against √count, a bounded pull (no infinities), rates made random by the random pattern.
- **It needs no ratio.**
- **Three is the fewest whole-number dimension where rates can match.** Whole numbers rest on the existing labelled smoothness assumption (A5 D11).
- **By C26's exit rule** (no ratio needed): **"a reason for three from ED's meanings, consistent, not derived."**
- **It's attempt 4's E-C point reached a second way,** from sync and commitment rather than from lasting kinds. The look-elsewhere guard still applies.
- **Still missing:**
  - the step-by-step weighting of moves (the growth rule itself);
  - the strength that decides whether ED's rates actually match.
- **Census:** no input added if G-Q8–G-Q10 hold as existing meanings. The input list doesn't get shorter either: three dimensions (row 6) now has two reasons, not a derivation.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **G-Q8** | **Can a single relation pull a clock's rate only so much per tick?** | **Yes** | No infinities (D32) |
| **G-Q9** | **Do clock rates differ a little at random from place to place,** because the pattern is random? | **Yes** | The pattern is random (A5 D10); clock rate comes from local commitment counts (A4 R4) |
| **G-Q10** | **Is dimension a whole number because the pattern behaves like a smooth space where it looks smooth,** A5 D11's assumption Q? | **Yes, the same labelled assumption** | Without it, "fewest" has no answer (C30) |

## Draft verdict (C26's rule; Allen to confirm with G-Q8–G-Q10)

> **Road G part 3:** rates can match across a pattern only if its least edge count outgrows the √count surplus of its random rates, so only above two dimensions, with no ratio needed for the floor. With commitment favouring the fewest directions and whole-number dimension (A5 D11's Q), three is the fewest. **A reason for three from ED's meanings, consistent, not derived.** Whether ED's rates actually match needs a strength ED doesn't supply; the step-by-step growth rule is still unwritten.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide G-Q8–G-Q10** and record the verdict | Settles part 3 |
| **(b)** | **Road G part 4:** write the step-by-step weighting of moves as counts, on paper | The growth rule itself; a model would come after, with expected results first |
| **(c)** | **Take stock of attempt 6** | Two roads walked: a wall (W), a reason for three and a missing rule (G) |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C28 | Sakaguchi, Shinomoto, Kuramoto, *Prog. Theor. Phys.* 77, 1005 (1987) (abstract listing); Strogatz and Mirollo, *Physica D* 31, 143 (1988) (abstract listing); Hong, Park, Choi, *PRE* 72, 036217 (2005) (abstract, A6 C21); Millán, Torres, Bianconi, *Sci. Rep.* 8, 9910 (2018), arXiv:1802.00297, and *PRE* 99, 022307 (2019), arXiv:1811.03069 (listings); Trofimov (1984) via arXiv:1908.06044 and listings; Gromov (1981) (A6 C16) | 2026-09-15 |
| — | A4-ledger D20, R4 (C71–C78), D32; A5-ledger C7, C17, D10, D11; A6 C21–C26 | Earlier ledgers |
