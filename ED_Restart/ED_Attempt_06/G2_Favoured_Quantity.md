# Road G, part 2: what growth favours (on paper)

*ED_Attempt_06, note 5. 2026-09-15 (RD6). Ledger: C20–C26. Literature and reasoning; nothing computed, no simulation. **Meaning questions G-Q5–G-Q7 and the draft exit rule are for Allen.***

## Where part 1 left it (C20)

**Allen accepted G-Q1–G-Q4 and the exit rule** (D5):
- distance is a hop count;
- growth can end and re-route relations in pairs;
- moves are local;
- the favoured quantity isn't named yet.

**Recorded:**

> **Road G part 1:** adding alone cannot expand; ED's paired, local rewiring can, but with nothing favoured its long-run patterns are the uniform ones, which aren't space-like; a growth rule needs one named favoured quantity from ED's meanings.

**Part 2 compares the three candidates.** Each gets three tests:
- **Does it favour a resting, direction-free, three-dimensional pattern?**
- **Does it add a strength or a constant?** (census guard)
- **Is it circular?**

## What's known (C21)

| | what it says | source |
|---|---|---|
| **Sync prefers small worlds** | How easily a network synchronizes is set by its spectrum. Adding a few random shortcuts to a lattice makes it far easier to sync | Barahona and Pecora, *PRL* 89, 054101 (2002) |
| **The best sync networks** | "Entangled networks": extremely uniform, short distances, large loops, no communities | Donetti, Hurtado, Muñoz, *PRL* 95, 188701 (2005) |
| **Sync on lattices depends on dimension** | Locally coupled oscillators with random rates on a d-dimensional grid: **phases stay out of sync up to d = 4. Rates match collectively in three dimensions,** with the lowest dimension for rate matching d = 2 | Hong, Park, Choi, *PRE* 72, 036217 (2005) |
| **Discrete actions carry the dimension** | The causal-set action's coefficients are **different for each dimension** | Benincasa and Dowker (2010); Dowker and Glaser, arXiv:1305.2588; Glaser |
| **Knots need a space** | A cycle's knot type depends on how it sits in space. Even "intrinsically knotted" graphs (K₇) are defined by **every embedding in 3D space** containing a knot | Conway and Gordon (1983) |
| **Longest chain = proper time** | In a random causal set the longest chain measures proper time | Brightwell and Gregory (1991); A4 fork FC |
| **Withdrawn, not used** | A 2026 preprint on long-range order in D-dimensional Kuramoto oscillators (arXiv:2604.22151) was withdrawn | noted only |

## On paper

### (i) "Clocks want to sync" (C22)

- **Uniformity alone picks no dimension.** A tree and a lattice of any dimension can both have every locus alike. *Firm.*
- **Favouring sync as much as possible favours small worlds:** shortcuts and entangled networks. That's no finite dimension. It pushes the wrong way.
- **The weak reading, "rates can match across the pattern,"** gives a floor. On grids, random rates match collectively only above two dimensions (Hong, Park, Choi). **So this reading favours d ≥ 3, with no ceiling.**
- **It adds a strength:** matching needs coupling above a threshold set by how different the rates are. That's a ratio, and a free parameter unless ED fixes it.

**Verdict for (i):** maximal sync pushes toward infinite dimension. "Rates can match" gives only a floor, d ≥ 3.

### (ii) "Commit as much as possible" (C23)

**Read for the pattern itself,** three ways:

| reading | what it favours | status |
|---|---|---|
| **Most time-order relations** among N events | Every pair related: a single chain. By counting ordered pairs (Myrheim–Meyer), dimension 1, **no space at all** | *Firm* |
| **Longest chain** (most proper time) | Again a single chain | *Firm* |
| **Most relations,** with finite neighbours | Every locus filled to its cap. Trees and grids of any dimension manage it | *Firm*: **neutral** |

**Verdict for (ii):** it pushes toward the fewest dimensions, down to none, or it's neutral. It never picks 3 by itself.

### (iii) "What the present can carry" (C24)

- **A loop's kind (its knot type) is only defined when the loop sits in a space.** An abstract pattern of relations doesn't give its loops knot types.
- **Even Conway and Gordon's intrinsic knotting quantifies over embeddings in 3D space.**
- **So as a growth weighting, (iii) presupposes three-dimensional space.** It's circular for road G.
- **And kinds are sparse:** particles are rare, so they can't weight empty space.

**Verdict for (iii):** it stays a consistency result (A4 C69, A5 C31: only three dimensions carry many lasting kinds). It isn't a growth weighting.

## Putting them together: a shape (C25)

**(i) and (ii) push in opposite directions:**
- **(ii), commit as much as possible,** pushes toward fewer dimensions.
- **(i), rates must be able to match,** forbids d ≤ 2.

**The fewest dimensions in which clocks can still sync is three.** The shape (A4 D23, C67) has two faces:
- a floor from sync;
- a push down from commitment.

They meet at a single point, **d = 3**.

**This is Allen's duality** (A4 D25, D28): commitment and syncing as two sides of one picture, a body's path accounting for both. Here, read for the pattern itself.

**It matches attempt 4's E-C point** (d = 3 from lasting kinds) by a different route. Two routes landing on a small integer is **weak evidence** (look-elsewhere).

**Honest limits:**
- **The floor is a grid result** with random rates and local coupling. ED's pattern is random, not a grid.
- **"Lowest dimension" is a statement about infinitely large systems.** ED has no infinities (D32). In a finite pattern, one or two dimensions desync only as the pattern gets large. With the universe's count of loci, that's effectively the same, but it's a size statement, not a sharp one.
- **Matching needs coupling above a threshold:** a ratio the census guard counts unless ED fixes it.
- **(ii)'s firm result is about time-order.** Reading it as "fewest space directions" is a reading, labelled.
- **It picks a dimension, not a growth rule.** How moves are weighted step by step is still unwritten.
- **Sync on general graphs** is governed by their spectral dimension, which isn't checked here.

## What it means (C25)

- **None of the three candidates alone** favours a resting three-dimensional pattern:
  - (i) pushes up;
  - (ii) pushes down;
  - (iii) is circular.
- **Together, (i) as a floor and (ii) as a push down** give a shape whose only point is d = 3.
  - It's suggestive, not derived.
  - It rests on a grid result, a threshold ratio and a labelled reading.
- **The census guard:** if the threshold ratio has to be put in, the growth rule has an added input.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **G-Q5** | **Set (iii) aside as a growth weighting,** keeping it as a consistency result? | **Yes** | A loop's kind needs a space, so weighting by it is circular (C24) |
| **G-Q6** | **For the pattern, does "clocks want to sync" mean rates can match across it,** rather than as much sync as possible? | **Yes** | Maximal sync gives small worlds, not space (C22); Allen's picture is rates pulled together (A4 D20) |
| **G-Q7** | **Is what growth favours the combination:** as few directions as possible, while rates can still match (the duality, A4 D25, D28)? | **Yes, as a labelled working lead** | The only combination of existing meanings found with a single point, d = 3 (C25). Look-elsewhere flagged |

## Draft exit rule (Allen to confirm)

- **With G-Q5–G-Q7 accepted:** record **"road G part 2: no single candidate favours a resting 3D pattern; the combination (fewest directions with rates able to match) gives the single point d = 3, suggestive, resting on a grid result, a threshold ratio and a labelled reading."**
- **Road G part 3 on paper:**
  1. Can "rates can match" be written as a count on ED's own random, finite pattern, without a coupling ratio or dimension-specific coefficients? (Literature on sync and spectral dimension on general graphs first.)
  2. Does the floor survive on random patterns?
- **Record then:**
  - **ratio needed:** "d = 3 as the fewest dimensions where rates can match, conditional on an added ratio" (census guard: an input added);
  - **no ratio needed:** "a reason for three from ED's meanings, consistent, not derived."
- **A model comes only later,** with rules, the dimension reading (counting outward plus the ball-cut), sizes, a stopping point and expected results written first.
- **If G-Q7 is rejected:** record that the candidates fail the bar ((i) up, (ii) down, (iii) circular), and road G stays open with its missing input.
- **No simulation.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide G-Q5–G-Q7** and confirm the exit rule | Settles the working lead |
| **(b)** | **Road G part 3:** "rates can match" on ED's own pattern, on paper | Whether the floor survives without a ratio |
| **(c)** | **Take stock of attempt 6** | Two roads, one wall, one lead |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C21 | Barahona and Pecora, *PRL* 89, 054101 (2002) (listings); Donetti, Hurtado, Muñoz, *PRL* 95, 188701 (2005), cond-mat/0502230 (listing); Hong, Park, Choi, *PRE* 72, 036217 (2005) (abstract); Hong, Chaté, Park, Tang, *PRL* 99, 184101 (2007) (abstract: global coupling, not used for dimensions); arXiv:2604.22151 (withdrawn, not used); Dowker and Glaser, arXiv:1305.2588, and BDG action literature (listings); Conway and Gordon (1983) and intrinsic knotting literature (listings) | As shown, 2026-09-15 |
| — | A4-ledger C67, C69, D20, D23, D25, D28, D32; A4 fork FC1; A5-ledger C31; A6 C16–C19 | Earlier ledgers |
