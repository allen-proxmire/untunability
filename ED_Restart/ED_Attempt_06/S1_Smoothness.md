# Smoothness, on paper

*ED_Attempt_06, note 9. 2026-09-15 (RD12). Ledger: C42–C46. Literature and reasoning; nothing computed, no simulation. **Meaning questions S-Q1–S-Q3 and the draft exit rule are for Allen.***

## The question

**Road G closed on smoothness** (C40):
- ED's own growth process heads to just above two dimensions;
- three is only the answer among *smooth* patterns;
- nothing found makes the pattern smooth.

**This note asks:**
- **what, mathematically, makes a rough space smooth,** with a whole-number dimension and no fractal roughness?
- **could any of ED's meanings supply it?**

## What's known (C42)

| | what it says | source |
|---|---|---|
| **Three conditions give smoothness** | Take a rough space with **(1) Ricci curvature bounded below, (2) dimension bounded above by a finite N, (3) a quadratic energy** (its Sobolev space is a Hilbert space): the "RCD(K,N)" spaces. Such a space is **rectifiable**: at almost every point it looks like ordinary flat space of some dimension ≤ N | Mondino and Naber, arXiv:1405.2222 |
| **One whole-number dimension** | That dimension is the **same almost everywhere** and a whole number | Bruè and Semola, *CPAM* (2020), arXiv:1804.07128 |
| **Stable** | These conditions survive taking limits: limits of such spaces are such spaces | RCD literature (e.g. Pan–Wei survey) |
| **Heat spreads normally** | In RCD(K,N) spaces, heat spreads with **Gaussian** bounds (distance² ∝ time) | Jiang, Li, Zhang (2016) |
| **Fractals fail** | On the Sierpinski gasket, heat spreads **sub-Gaussian**, with walk dimension log₂5 ≈ 2.32, not 2. Its energy measures are singular | Barlow and Perkins (1988); Kusuoka |
| **Curvature as contraction** | Ollivier's coarse Ricci curvature: **how much two neighbours' random-walk steps draw together** compared with their distance. Positive curvature gives a spectral gap | Ollivier, *JFA* 256, 810 (2009) |
| **Graph curvature and loops** | Lower bounds on a graph's Ollivier curvature rise with **triangles** (neighbours that are themselves linked) | Jost and Liu, *DCG* 51, 300 (2014) |
| **Graph curvature and growth** | Graphs with nonnegative (Bakry–Émery-type) curvature have **polynomial volume growth** and Gaussian heat bounds | Bauer, Horn, Lin, Lippner, Mangoubi, Yau, *JDG* 99, 359 (2015); 2026 preprint on volume doubling |
| **Graphs converge** | Ollivier curvature of random geometric graphs converges to the Ricci curvature of their manifold, at mesoscopic neighbourhoods | van der Hoorn, Lippner, Trugenberger, Krioukov, *PRR* 3, 013211 (2021); *DCG* (2023) |
| **Time-ordered version** | A synthetic **timelike** Ricci bound exists for Lorentzian spaces (TCD(K,N)), stable under limits, a rough analogue of the strong energy condition | Cavalletti and Mondino, *Camb. J. Math.* 12, 417 (2024) |
| **Triangulations** | CDT's four-dimensional de Sitter phase **survives without its preferred time slicing**; the causal structure stays | Jordan and Loll, arXiv:1307.5469 (2013) |
| **Short loops** | Condensing short cycles drives random graphs into a geometric phase | Trugenberger (C16); Kelly, Trugenberger, Biancalana, arXiv:1901.09870 |

## On paper

### 1. Smoothness isn't a separate miracle (C43)

**In the mathematics of rough spaces, smoothness follows from three conditions:**

| | condition | in plain words |
|---|---|---|
| **(1)** | **Curvature bounded below** | Neighbouring regions never spread apart faster than some bound |
| **(2)** | **Dimension bounded above** | Some finite ceiling on how many directions there can be |
| **(3)** | **Quadratic energy** | The cost of a difference goes like its square: the Pythagorean kind of rule |

**Together they give** *(firm, for the continuum spaces the theorems cover)*:
- smooth almost everywhere;
- one whole-number dimension;
- normal heat spreading.

**Fractals are excluded:** their heat spreads abnormally (walk dimension 2.32 on the gasket, not 2).

**So the 2.1-dimensional patterns** that road G's process heads toward **fail these conditions.** They are exactly what the conditions rule out.

### 2. What ED's meanings could supply (C44)

| condition | a reading from ED's meanings | status |
|---|---|---|
| **(1) Curvature bounded below** | **"Clocks want to sync"** (A4 D20): Ollivier curvature *is* a contraction, neighbours' steps drawing together. **Sync as contraction that is never beaten by spreading apart** | **A reading, labelled.** New: road G read sync only as "rates can match" |
| **(2) Finite dimension ceiling** | **"No infinities"** (A4 D32): every count is finite, so the number of directions has a ceiling | Close to the meaning as decided. It gives a ceiling, not the value |
| **(3) Quadratic energy** | **ED already uses quadratic rules:** the Born rule (probability = amplitude × its conjugate, A2 C11) and the quadratic interval (A5 D11's Q) | **A new reading, labelled.** Q's wording is "where a smooth description applies", so (3) can't be borrowed from Q (the lesson from note 8). The Born rule is about states, not the pattern's energy |

**None of the three puts the dimension in.** N is only a ceiling, and the dimension comes out as some whole number ≤ N.
- **Part 3's floor** (rates can match only above two dimensions) **plus commitment's push to the fewest** then picks **three**, provided N ≥ 3.
- **Now three comes out of conditions rather than from an assumed smoothness.**

### 3. What it asks of the discrete pattern: loops (C45)

- **The theorems are about continuum spaces.** For ED's pattern, the conditions must hold in the large-scale limit.
- **A curvature bound in continuum units becomes, at the grain, curvature that is nearly nonnegative.** Any finite negative bound, scaled down to the grain, shrinks toward zero.
- **On graphs, curvature that isn't negative needs triangles:** neighbours that are themselves linked, which means **many short loops** (Jost–Liu).
- **So a smooth ED pattern needs its relations rich in short loops.** Trees and the sparse, tuned patterns from road G's process are loop-poor and fail.

**This connects walls 2 and 3:**
- **wall 3 (smoothness) needs many short loops;**
- **wall 2 (stuck states) is worst exactly where loops are many,** at least 1 − 2/(mean neighbours) stuck.

**The two walls pull against each other through the same thing.** This is a real tension, recorded. Particles are loops too; that's a flagged resemblance (look-elsewhere), not a finding.

**What this suggests for road G's process:**
- **sync pulls relations in where rates fail;**
- **commitment makes relations cost;**
- **plus "never let neighbourhoods spread apart beyond a bound",** which keeps short loops.

That is a specification a model could test. It isn't a derivation.

### 4. Honest limits (C45)

- **The discrete-to-continuum step isn't established** for general patterns. Curvature convergence is proved for random geometric graphs, which are built inside a manifold. Nonnegative graph curvature gives polynomial growth, not smoothness by itself.
- **ED is time-ordered.** The Lorentzian version (TCD) exists, but I haven't checked its structure theory (rectifiability, whole-number dimension) here.
- **Readings (1) and (3) are new readings,** labelled. The census guard counts them unless Allen takes them as what "sync" and ED's quadratic rules already mean.
- **"Curvature bounded below" might not follow from sync.** Sync is about rates matching; a curvature bound is about neighbourhoods contracting. They're related through random walks and spectral gaps, not identical.

## What it means (C45)

- **Smoothness has a known mathematical recipe:** curvature bounded below, a finite dimension ceiling, quadratic energy.
- **ED's meanings offer a reading for each:**
  - sync as contraction;
  - no infinities;
  - ED's quadratic rules.
- **With those readings, three comes out of conditions rather than from assumed smoothness.** Part 3's floor does the rest.
- **Verdict shape, if accepted:** consistent, not derived. The wall is reframed as conditions a growth rule must keep, not removed.
- **The price is loops.** Smoothness needs many short loops, and that is where the stuck-state wall is worst.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **S-Q1** | **Does "clocks want to sync" include that neighbouring regions never spread apart faster than a bound** (curvature bounded below, as contraction)? | **Yes, as a labelled reading** | Ollivier curvature is a contraction of neighbours; sync is neighbours drawing together (A4 D20) |
| **S-Q2** | **Is the cost of a difference in ED's pattern quadratic,** the same kind of rule as the Born rule and the interval? | **Yes, as a new labelled reading** | ED already uses quadratic rules; not borrowed from Q, whose wording presupposes smoothness |
| **S-Q3** | **Does "no infinities" give a finite ceiling on the number of directions?** | **Yes** | Every count in ED is finite (A4 D32) |

## Draft exit rule (Allen to confirm)

- **With S-Q1–S-Q3 accepted:** record
  > **"Smoothness: curvature bounded below, a finite dimension ceiling and quadratic energy give a smooth-almost-everywhere space with one whole-number dimension, fractals excluded; ED's meanings supply these as readings (sync as contraction, no infinities, quadratic energy); with part 3's floor and commitment's push, three follows among such patterns; on a discrete pattern this needs curvature nearly nonnegative at the grain, i.e. many short loops, against the stuck-state wall; the discrete-to-continuum step is not established. Consistent, not derived; the smoothness wall is reframed as conditions a growth rule must keep."**
- **Then options:**
  - a model of the constrained process (sync pulls relations in, relations cost, neighbourhoods don't spread apart), with rules, the dimension reading (counting outward plus the ball-cut, and heat spreading as a smoothness test), sizes, a stopping point and expected results written first;
  - loops on paper (short loops for smoothness against stuck states);
  - conclude attempt 6.
- **If S-Q1 or S-Q2 is rejected:** record the recipe as literature, and the smoothness wall stands as in C40.
- **No simulation.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide S-Q1–S-Q3** and confirm the exit rule | Settles whether the wall is reframed |
| **(b)** | **Loops, on paper:** smoothness needs short loops; stuck states live on loops. Is there a way through? | The tension this note found |
| **(c)** | **A model of the constrained process** (expected results first) | Tests whether it grows a smooth three |
| **(d)** | **Conclude attempt 6** | Carry the reframed walls into attempt 7 |

**Proposal: (a), then (b).** The loops tension decides whether a model would even be testing a consistent ED.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C42 | Mondino and Naber, arXiv:1405.2222; Bruè and Semola, arXiv:1804.07128; Pan and Wei survey (listing); Jiang, Li, Zhang, arXiv:1407.5289 (listing); Barlow and Perkins (1988) via Grigor'yan's notes and listings; Kusuoka energy measures (arXiv:1411.2371 listing); Ollivier, arXiv:math/0701886 (listing); Jost and Liu, *DCG* 51 (2014) (listing); Bauer et al., arXiv:1306.2561 (listing); arXiv:2607.15522 (2026 preprint, listing); van der Hoorn et al., arXiv:2008.01209 and arXiv:2009.04306 (listings); Cavalletti and Mondino, arXiv:2004.08934 (listing); Jordan and Loll, arXiv:1307.5469 (abstract); Kelly, Trugenberger, Biancalana, arXiv:1901.09870 (listing) | 2026-09-15 |
| — | A2-ledger C11; A4-ledger C58, D20, D32; A5-ledger C36, D11, C31; A6 C12, C15, C16, C29–C40 | Earlier ledgers |
