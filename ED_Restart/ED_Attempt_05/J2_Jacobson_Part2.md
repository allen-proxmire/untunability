# Road J, part 2: does ED's count supply Jacobson's input? (on paper)

*ED_Attempt_05, note 3. 2026-09-15 (RD3, D6). Ledger: C7–C12. Reasoning, plus one arithmetic check (`checks/crossing_count_check.py`, expected results written first) and a labelled follow-up diagnostic. Nothing about ED itself was simulated.*

## The meanings used (decided, D6)

| | meaning |
|---|---|
| **J-Q1** | ED's entropy of a surface **counts every relation crossing it** |
| **J-Q2** | **Each relation counts once,** with no weights |
| **J-Q3** | **Heat** is the motion and energy carried across by matter and influence |
| **J-Q4** | **The temperature is Unruh's,** inherited at low energy |
| **J-Q5** | **At horizon scales the pattern behaves like three-dimensional space** (a labelled assumption) |

**Plus, from attempt 4:**
- **finite, nearby neighbours** (A4 D32);
- **a commitment carries nothing numerical** (A4 D4).

## Step 1: the count grows like area (C7, C8)

**The geometry:**
- **Take a pattern whose relations point every way equally on average.**
- **The expected number of relations crossing any surface is half the total relation length per unit volume, times the area:** N = ½·L_V·A. This is a standard result of integral geometry (in stereology, P_A = ½ L_V).

**The check** (C7):

| | what | result |
|---|---|---|
| **K1** | Random segments crossing a plane, against ½·L_V per area | ratio **1.011** ✓ |
| **K3** | A random short-range pattern (links between points closer than r) crossing a sphere of radius 16 | 12,881 crossings against 12,791 from the formula (**1.007**); crossings grow like **R^2.12**, an area law ✓ |
| **K4** | The same points with **long-range** links only | crossings grow like **volume**. Run 1's fitted exponent was 3.20, **above its pre-set range of 2.8–3.1: NOT AS EXPECTED.** A follow-up diagnostic (not pre-registered) found the smallest ball happened to hold fewer points than average; with the actual counts, observed and expected agree within 2%, and over 40 ball centres the exponent is 2.99 |

**So the entropy S = s₀·N grows like area, provided three things hold:**
1. **Neighbours are finite and nearby,** so the relation length per volume is finite. ED decided this (A4 D32). Long-range relations would make it grow like volume instead (K4).
2. **Relations point every way equally on average.** This is new; see step 2.
3. **Each crossing relation adds the same entropy s₀,** and the relations' states are independent or only correlated over short distances (J-Q2).

## Step 2: a finding, directions have to go (C9)

**On a cubic grid, the count depends on which way the surface faces** (K2 ✓):

| surface faces… | relations crossing per unit area |
|---|---|
| along an axis | **1.000** |
| between two axes | **1.415** |
| along the body diagonal | **1.732** |

**Why this matters:**
- **That's a count per unit area, so it doesn't smooth out at large scales.**
- **Jacobson needs the same entropy coefficient for a horizon facing any direction** (his "every direction" step).
- **A grid-like ED would give horizons facing a diagonal up to 73% more entropy,** and Einstein's equation would come out direction-dependent.

**So ED's relations must point every way equally on average.**
- **Random growth by draws** can supply that (A4 PF-c).
- **The rest frame is a separate matter,** and it stays.

**Sharpened assumption S′:** at horizon scales the pattern behaves like three-dimensional space, **and its relations point in every direction equally on average.**

## Step 3: the rest of the chain (C10)

- **Heat** (J-Q3) is standard.
- **Temperature** (J-Q4) is Unruh's, inherited. Because ED has a rest frame (A4 C87), its survival at low energy is assumed, not shown.
- **The first law on every local horizon gives Einstein's equation.**

**The coefficient ties G to how densely relations cross:**
- **Setting the entropy per area,** s₀·L_V/2, **equal to** 1/(4ℓ_P²) gives **ℓ_P² = 1/(2·s₀·L_V).**
- **For relations about one grain long, with k neighbours per locus:** L_V ≈ k/(2ℓ_g²), so **ℓ_P² ≈ ℓ_g²/(k·s₀).**
- **In words: the Planck length is the grain spacing divided by √(k·s₀).**
- **The values are inherited; the relation is ED's structure.**
- **Every kind of relation adds to the count,** which matches physics' finding that the coefficient depends on the number of field kinds.

## The census (C11)

| Jacobson's chain | ED's version |
|---|---|
| **Entropy ∝ area** (assumed) | **Follows from:** entropy = the count of crossing relations (J-Q1, J-Q2), finite neighbours (A4 D32), relations pointing every way equally (S′) |
| The area coefficient (sets G) | Inherited; tied to s₀, the grain and the neighbour count |
| Unruh's temperature | Inherited, with the rest-frame dependency |
| The first law | Inherited |
| Heat as energy flux | Inherited (J-Q3) |
| Every direction / local Lorentz | Inherited, and ED's relations must also point every way equally |
| Smooth geometry | Assumption S′ |

**The honest count:** one assumption (entropy ∝ area) comes out, and one meaning (entropy counts crossing relations) goes in. No free parameters are added. **The list is not shorter.**

## The exit rule's verdict (C11)

- **The count needs no weights, no subset of relations chosen to get area, and no long-range relations,** so the rule's first branch holds, with S sharpened to S′.
- **"Entropy ∝ area": a reason from ED's meanings.** The coefficient is inherited.
- **Einstein's equation overall: consistent, not derived.**
- **The census: not a reduction.** An assumption is swapped for a meaning.
- **No conflict with a decided meaning was found.** The Unruh step still depends on the rest-frame wall, named, not resolved.
- **Prior art:** causal-set link counting (Dou and Sorkin) and induced gravity. ED's version is the finite-neighbour, direction-free counting form of the same idea.

## What it means (C12)

**Road J gives ED a clean reading of what sources gravity:**
- **entropy is how many relations cross a surface;**
- **area comes for free** from finite, nearby relations that point every way;
- **G measures how densely relations cross.**

**It isn't fewer inputs yet.** For that, "entropy is the count of crossing relations" would have to follow from something ED already has. **One candidate is already in ED:**
- **a draw happens once a record is out of reach** (A1 RD50);
- **the present state is all there is** (A4 D21).

If hidden information *is* exactly the relations that reach beyond what the present can reach, then entropy wouldn't be a new meaning. **It would be ED's notion of reach, counted.** That could turn the swap into a reduction, but it has to be fixed as a meaning *before* any count is compared with anything.

**The direction finding joins the preferred-frame hole:** directions can go (random growth), the rest frame stays, and Unruh's temperature is where it pinches.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Road J part 3, on paper:** is hidden information exactly the relations that reach beyond reach (tying entropy to A1's draw rule)? A meaning question and an exit rule first | The one route that could make this a reduction rather than a swap |
| **(b)** | **Unruh in ED, on paper:** can a direction-free pattern with a rest frame give an accelerating body a thermal count at low energy? | The pinch point of the whole chain |
| **(c)** | **Close road J with this verdict** | If (a) looks like reaching |

**Proposal: (a).** It's short, and it's where the census could change.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C7 | `checks/crossing_count_check.py`, run 1 (`checks/crossing_count_check_run1.txt`); `checks/crossing_count_k4_diagnostic.py` (`…_run1.txt`), follow-up, not pre-registered | Computed |
| C8 | The stereological relation P_A = ½ L_V (Cauchy–Crofton type), derived here for isotropic segments and for a random short-range pattern; integral-geometry background as described in listings (Crofton formulae notes, Notre Dame thesis; arXiv:0812.2735) | Derived on paper and checked numerically; listings |
| — | C2–C6; A1-ledger RD15, RD50; A4-ledger C87, D4, D21, D32, PF-c | This and earlier ledgers |

**Update (RD4):** Part 3, whether entropy is ED's reach counted, is in [J3_Jacobson_Part3.md](J3_Jacobson_Part3.md) (note 4).
