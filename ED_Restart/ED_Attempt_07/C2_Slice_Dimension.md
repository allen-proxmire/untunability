# Road C2, part 2: slice dimension from sync and commitment (on paper)

*ED_Attempt_07, note 8. 2026-09-16 (RD10). Ledger: C19–C25. Literature, reasoning and scaling arithmetic; nothing computed. **Meaning questions C2-Q5–C2-Q7 and the draft exit rule are for Allen.***

## Where part 1 left it (C19)

**Allen chose (a)** (D9): the telescoped offspring measure is adopted as C2a's balance check. That's a revise-and-retest step, prompted by his prime-triangle point (D8). The measure was adopted after seeing run 1, and that's recorded. **C2a is recorded as:**

> **"The balance self-organizes from ED's budget passed forward and conserved: consistent, not derived; k and L\* are knobs; space settles as a fixed-size tube, and growth would need budget creation (the cosmic excess, inherited)."**

**What C1 and C2a still put in:** each slice was **given as a circle**, so slices are one-dimensional and spacetime is two-dimensional. Part 2 asks what makes slices **three-dimensional**.

## What's known (C20)

| | what it says | source |
|---|---|---|
| **CDT builds slice dimension in** | Its building blocks are d-dimensional simplices glued with a time slicing | CDT reviews |
| **Causality alone doesn't make slices smooth** | In 4D CDT's de Sitter phase, a single spatial slice has Hausdorff dimension about 3 but spectral dimension about 1.5: **the slices are fractal**, even though the whole spacetime looks 4D | Ambjørn, Görlich, Jurkiewicz, Loll, arXiv:1111.6938; review arXiv:1905.08669 |
| **Random 2D surfaces are far from flat** | 2D Euclidean dynamical triangulations have Hausdorff dimension 4 | Ambjørn and Watabiki, *Nucl. Phys. B* 445 (1995) |
| **The global slicing isn't essential** | CDT with only local light-cone causality, no preferred time slicing, still grows a de Sitter universe in 2+1 dimensions | Jordan and Loll, *PLB* 724, 155 (2013); *PRD* 88, 044055 (2013) |
| **Oscillator floors** | Locally coupled oscillators with random frequencies on d-dimensional grids: **rates match only above d = 2; ticks stay out of step up to d = 4** (in the strong-coupling regime, tick differences grow with size) | Hong, Park, Choi, *PRE* 72, 036217 (2005) |
| **Networks** | Spectral dimension ≤ 2: no sync | Millán, Torres, Bianconi (A6 C28) |
| **ED so far** | Rates can match only above two dimensions, no ratio needed for the floor; commitment favours the fewest directions; so three is the fewest whole number (A6 C31). The sync-plus-cost process without time order heads to the floor, not smooth three (A6 C36) | A6 notes 6–7 |

## On paper

### 1. C1 and C2a put sync in, twice (C21)

- **Slices were given** (as circles).
- **Every link goes from one slice to the next.** So every chain of events from slice t to slice t+s has exactly s steps.
- **Every clock ticks in step by construction.** The slicing *is* a perfect sync across all of space. CDT puts in the same thing.
- **Jordan–Loll show the global slicing can be dropped** while keeping local causality. So in ED, a common time across space is something sync should *produce*, not something to assume.

### 2. What sync means in a time-ordered pattern (C22)

**Picture it.**
- **Each place's clock runs at a slightly random rate** (A6 G-Q9) and is pulled toward its neighbours by a bounded amount (G-Q8).
- **A "slice" is then the set of events where the clocks read the same tick count.**
- **If rates don't match, that surface tears:** one region's clocks run away from another's.
- **Even when rates do match, tick counts wobble across space.** The surface is rough.

**When is a rough slice still a slice?** In ED, influence moves at most one hop per tick.
- **Two events L hops apart** whose tick counts differ by **less than L** can't influence each other. Then the slice is **space-like**, a real "now."
- **If the counts differ by L or more,** one could be in the other's past. **The slice has folded into time.**

**How rough is the slice?** This is the standard strong-coupling calculation (as in Hong–Park–Choi), in ED's words:
- **Settled clocks balance each rate difference against the pull from neighbours:** pull strength K times the local curvature of the tick count equals the rate surplus σ.
- **So the tick-count wobble across a slice region of size L grows like (σ/K) · L^((4−d)/2).**
- **The tilt** (wobble over distance) goes like **(σ/K) · L^((2−d)/2).**

| slice dimension d | wobble across L | tilt at large L | a real "now"? |
|---|---|---|---|
| **1** | L^1.5 | **grows** | **No.** Large regions fold into time |
| **2** | L^1 | **constant**, set by σ/K | **Only if σ/K is small enough:** a ratio |
| **3** | L^0.5 | **shrinks to zero** | **Yes, for any σ/K,** at large scales |
| **4 and up** | bounded | shrinks | Yes |

**So a common "now" across space needs slice dimension ≥ 3 without a ratio.**
- **It's A6's rate floor seen as geometry:**
  - below two, rates can't match;
  - at two, the tie is decided by a ratio;
  - above two, the slice flattens out.
- **The new part:** the floor now has a picture in ED's time order. **Sync is what keeps "now" from folding into time.**

### 3. Commitment caps it (C23)

- **More slice directions mean more neighbours per event,** so more links to hold and more budget split per link (C2a's reading B).
- **Commitment favours the fewest directions** (A6 G-Q7, the labelled lead).
- **The fewest whole-number slice dimension where "now" holds without a ratio is 3.** So spacetime is **3 + 1 = 4**.

### 4. The honest limits (C24)

| | limit |
|---|---|
| **Persistent rates** | The floor needs rate differences that **persist** along a worldline. If each event's rate were fresh random every tick, wobble would grow only like L^((2−d)/2) and **every** dimension would give a real "now": sync would give no reason for three. **That's a meaning question (C2-Q5)** |
| **Whole numbers** | d = 2.1 also passes the floor. **Three still needs whole-number dimension** (A6 G-Q10, assumption Q). 4D CDT's fractal slices show causality alone doesn't supply smooth slices |
| **Strong-coupling regime** | The wobble calculation is the linear, strong-pull regime. Weak pull is harder (Hong–Park–Choi use numerics there) |
| **The rule is still missing** | Nothing here lets a slice *change* its dimension as it grows. It's a **selection** among slice dimensions, like A6's, now with a causal picture. A growth rule for d-dimensional slices without splitting is the open problem (wall 3) |
| **Known physics** | The wobble exponents are known for grids. What would be new is checking them **inside ED's causal, budget-balanced pattern** |

## What it means (C25)

- **With time order, "clocks want to sync" has a geometric meaning:** it keeps "now" space-like.
- **With persistent random rates, that holds without a ratio only for slices of dimension 3 or more.** Commitment's fewest directions and whole numbers give **three**, so spacetime is four-dimensional.
- **It's A6's reason for three, now tied to the causal pattern.** Road C's two parts meet here:
  - causal growth gives the smooth direction in time (C1);
  - budget gives the balance (C2a);
  - sync and commitment pick the slice dimension.
- **Consistent, not derived.** It's still a selection among slice dimensions, not a rule that grows three; whole numbers are still assumed.
- **Inputs:** unchanged (still 3). **Census:** nothing added if C2-Q5–C2-Q7 hold.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C2-Q5** | **Do rate differences persist along a worldline,** rather than being drawn fresh each tick? | **Yes** | Rate comes from local commitment counts, and what happened stays happened (A4 R4, G-Q9). **If no, sync gives no reason for three** |
| **C2-Q6** | **In a time-ordered pattern, does sync mean a common "now" holds:** tick counts across space never differ by as much as the hop distance, at large scales? | **Yes, as the causal form of G-Q6** | It's what "rates can match" looks like once time is order; it adds no new idea |
| **C2-Q7** | **Check the floor first with slices given** as 1-, 2- and 3-dimensional, before any rule that lets slice dimension change? | **Yes** | A known answer first, as in C1 |

## Draft exit rule (Allen to confirm)

**Next step: model C2b on paper, then run.**
- **The model:** C2a's budget-balanced causal growth, but with slices given as d-dimensional rings/tori (d = 1, 2, 3) and no global clock. Each place has a persistent random rate and a bounded pull from its slice and past neighbours; the tick count is carried forward along links.
- **The reading:** the tick-count wobble W(L) across slice regions of size L, and the tilt W/L.
- **It passes if** the wobble exponent reads near 1.5, 1 and 0.5 for d = 1, 2, 3 (ranges fixed in the spec), and the tilt grows, holds or shrinks accordingly. Record: **"A common now needs slice dimension ≥ 3 without a ratio in ED's causal pattern; with commitment's fewest directions and whole numbers, three: consistent, not derived."**
- **If the exponents don't separate the dimensions:** record "the floor isn't seen in ED's causal pattern," and take stock of road C.
- **Expected results, sizes and exact ranges are fixed in the C2b spec before any code.** Revise and retest is allowed and recorded.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide C2-Q5–C2-Q7, confirm the exit rule, spec C2b on paper** | Checks the floor inside ED's own pattern; cheap |
| **(b)** | **Work on paper on a growth rule for d-dimensional slices without splitting** | The real open problem (wall 3); original and harder |
| **(c)** | **A fresh-seed retest of C2a's revised balance check** (seconds to run) | Makes the adopted measure a clean retest, not just a re-measure |

**Proposal: (a), with (c) run alongside if you say run.**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C20 | Ambjørn, Görlich, Jurkiewicz, Loll, "Causal Dynamical Triangulations in Four Dimensions", [arXiv:1111.6938](https://arxiv.org/abs/1111.6938) (listing; slice d_H ≈ 3, d_s ≈ 1.5); CDT review [arXiv:1905.08669](https://arxiv.org/pdf/1905.08669) (listing); Ambjørn and Watabiki, *Nucl. Phys. B* 445 (1995), d_H = 4 in 2D Euclidean quantum gravity (listings, [arXiv:1108.3327](https://arxiv.org/pdf/1108.3327)); Jordan and Loll, [arXiv:1305.4582](https://arxiv.org/pdf/1305.4582), [arXiv:1307.5469](https://arxiv.org/abs/1307.5469) (abstracts); Hong, Park, Choi, [PRE 72, 036217](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.72.036217), [cond-mat/0408553](https://arxiv.org/pdf/cond-mat/0408553) (abstract: phase lower critical dimension 4, frequency 2) | 2026-09-16 |
| C22 | Scaling arithmetic: steady state K∇²φ = −(ω − ω̄), so φ_k = ω_k/(K k²), W² ∝ (σ/K)² ∫_{1/L} k^(d−1−4) dk ∝ (σ/K)² L^(4−d) for d < 4; tilt W/L ∝ L^((2−d)/2). Fresh-each-tick noise instead gives W² ∝ L^(2−d) | Worked, 2026-09-16 |
| — | A6-ledger C28–C37, D6, D7; A7 C1, C8, C16–C18 | Earlier records |
