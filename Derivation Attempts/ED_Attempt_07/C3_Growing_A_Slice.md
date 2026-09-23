# Road C3: growing a slice with more than one dimension (on paper)

*ED_Attempt_07, note 12. 2026-09-16 (RD21). Ledger: C42–C46. Literature, reasoning and counting; nothing computed. **Meaning questions C3-Q1–C3-Q5 and the draft exit rule are for Allen.***

## The question

**C1 and C2a grew slices, but only circles.** C2b showed sync picks three dimensions, but its slices were **given.** Road C3 asks:

> **Can ED's causal growth grow a slice of more than one dimension that never splits or merges, stays smooth, and keeps its dimension, from finite neighbours, the budget and sync?**

**The smallest case past a circle is a surface** (a 2D slice). That's where C3 starts.

## What's known (C42)

| | what it says | source |
|---|---|---|
| **Random surfaces are fractal** | Random triangulated surfaces (2D Euclidean dynamical triangulations) have Hausdorff dimension **4**, not 2, though spectral dimension 2 | Ambjørn–Watabiki (1995), C20 |
| **Bounding local curvature doesn't fix it** | Allowing only vertices of degree 5, 6 or 7 **doesn't change** the large-scale fractal behaviour | Bowick, Catterall, Thorleifsson (LATTICE96, hep-lat/9608076) |
| **A curvature-squared cost gives a crossover** | Random surfaces weighted by a curvature-squared term look **flat up to a scale** and fractal beyond it; three states (crumpled, flat, branched polymer) are seen at finite size | DT studies with higher curvature terms (listings) |
| **Random 3D and 4D geometry has two bad phases** | Euclidean DT in 3D and 4D: a **crumpled** phase (Hausdorff dimension → ∞, huge-degree vertices) and a **branched-polymer** phase (Hausdorff dimension 2, spectral dimension 4/3) | EDT reviews; Jonsson–Wheater, NPB 515 (1998) |
| **Causality helps, but slices can still be rough** | CDT's time slicing gives a good phase between the bad ones; in 4D CDT single slices are still fractal (Hausdorff ≈ 3, spectral ≈ 1.5) | C20 |
| **3D causal slices have a known combinatorics** | Slices of 3D causal triangulations map one-to-one onto certain coloured 2D cell complexes | Durhuus–Jonsson, arXiv:1712.07502 |
| **Torus slices** | 2+1 CDT with torus slices is studied for global shape as well as size | Budd–Loll, PRD 88, 024015 (2013) |
| **Growth versus ensembles** | Peeling and Eden-type growth *explore* existing random maps. This search found no study of surfaces *grown* by local vertex splits with a curvature or sync feedback | Budd (arXiv:1506.01590); Curien's lecture notes |

## On paper

### 1. What "no splitting" means for a surface (C43)

**For a circle,** no splitting meant each event's children form a run and neighbours share one event (C3).

**For a surface,** the slice is a triangulated surface of fixed topology (take a torus, which has no boundary and can be flat). No splitting or merging means **the topology never changes.** Two local moves do that:

| move | what happens | counts |
|---|---|---|
| **Vertex split** (an event has two children) | Pick two neighbours u, w of event v. The ring of v's neighbours is cut at u and w into two arcs. One child takes one arc, the other child takes the other, and the children are linked to each other and to both u and w | +1 event, +3 links, +2 triangles; the degrees of the two children add to deg v + 4, and u and w each gain one |
| **Edge collapse** (an event has no child of its own) | The event's place merges into a neighbour's child | The inverse of a split. **Allowed only if the link condition holds**, which is exactly what keeps the surface from pinching or splitting |

- **Several children** means several splits in a row.
- **Checked by counting:**
  - a split keeps vertices − edges + faces unchanged (+1 − 3 + 2 = 0), so the topology holds;
  - the average degree on a torus stays exactly 6.

### 2. What the budget and offspring do (C43)

**C2a's reading B carries over:**
- each event splits its budget over its forward links;
- the number of new events follows the budget;
- the slice's event count settles at L\*.

**What's new is *where* children go:** which pair u, w each split uses. That choice sets the local degrees, and so the curvature. On a surface, curvature at an event is 6 − degree.

### 3. The real problem: keeping the surface flat (C44)

- **The size is handled** (C2a).
- **The shape isn't.** Degree, and so curvature, wanders as splits and collapses pile up. The literature says the typical random surface is fractal (Hausdorff 4), and **bounding degrees to 5–7 doesn't stop it.**
- **What could keep it flat, from ED's meanings:**

| | candidate | ED meaning | what the literature suggests |
|---|---|---|---|
| **(i)** | **Uniform choice** (no preference) | None: least structure | For equilibrium random surfaces, fractal. For growth, unknown |
| **(ii)** | **Quadratic curvature cost:** prefer splits that keep degrees near 6 | **Quadratic energy** (A6 S-Q2, decided) | Flat up to a crossover scale, then fractal, in equilibrium ensembles. Unknown for growth |
| **(iii)** | **Sync:** a split is favoured where it helps rates match | **Clocks want to sync** (G-Q6, C2-Q6) | **In 2D, sync is marginal** (C2b): the tilt of "now" holds at a ratio-set value. So sync gives no large-scale flattening push in 2D |

**The honest reading:** on a surface, ED's own sync result says 2D is the borderline case. A 2D slice is the **smallest test of the growth machinery**, but ED's meanings don't expect sync to flatten it at the largest scales. The machinery matters because the same moves generalize to 3D, where they're bistellar moves.

### 4. Why 3D may be different: each bad phase breaks one ED meaning (C45)

**Random 3D geometry fails in two ways** (C42). Each one violates a different ED meaning:

| bad phase | what it looks like | which ED meaning it breaks |
|---|---|---|
| **Crumpled** | Everything close to everything; some events with enormous numbers of neighbours | **Commitment:** each link costs, and huge-degree events are the most expensive. Also **no infinities** (a finite ceiling on neighbours) |
| **Branched polymer** | Tree-like; spectral dimension 4/3 | **Sync:** rates can't match at spectral dimension ≤ 2 (C20, A6 C28). A branched slice can't hold a synced "now" |

- **So in 3D, the two meanings between them rule out both bad phases.** Commitment rules out crumpling, sync rules out branching, and what's left is the middle, where CDT finds its good phase.
- **In 2D the branched side isn't ruled out by sync** (marginal), which is one more reason 2D is a machinery test, not the target.
- **This is a lead on paper,** not a result. The census guard applies: it would count only if a model grows a 3D slice with no dimension or smoothness put in.

## What it means (C46)

- **Road C3's problem is now specific:**
  - **size** is handled by the budget (C2a);
  - **topology** is handled by splits and collapses under the link condition;
  - **shape** is the open part.
- **The literature says** random surfaces and random 3D geometries are fractal or branched by default, and local degree bounds don't fix that.
- **ED's meanings offer quadratic curvature cost (all dimensions) and sync plus commitment (3D).** In 3D those two rule out the two bad phases between them.
- **A 2D slice** is the cheapest test of the growth machinery. ED's own sync result doesn't expect it to stay flat at the largest scales.
- **Consistent, not derived.** Nothing computed. Inputs unchanged (3).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3-Q1** | **For a slice with more than one dimension, does "never splits or merges" mean its topology never changes,** with vertex splits and link-condition collapses as the only moves? | **Yes** | The direct form of A6 D22 for surfaces; local; finite neighbours |
| **C3-Q2** | **Do offspring follow C2a's budget** (budget passed forward and conserved), with no child meaning a collapse and extra children meaning splits? | **Yes** | Keeps Budgeted Causality; the balance is already earned |
| **C3-Q3** | **Is the curvature cost quadratic in (6 − degree)** for a surface, as the form of the decided quadratic-energy meaning? | **Yes, labelled reading** | A6 S-Q2; the least-structure quadratic |
| **C3-Q4** | **Run the uniform choice as the baseline** alongside the curvature-cost choice? | **Yes** | Shows what growth does with no preference; recorded either way |
| **C3-Q5** | **Start with a 2D torus slice as a machinery test,** knowing ED's sync result treats 2D as borderline, and **keep 3D as the target**? | **Yes** | Cheapest case; the moves carry over to 3D |

## Draft exit rule (Allen to confirm)

**Next step: model C3a, specified on paper, then run.**
- **The model:** a torus slice grown by C2a's budget with splits and link-condition collapses.
  - Two choice rules: uniform, and quadratic curvature cost at strengths λ ∈ {0.5, 1, 2}.
  - Slice sizes around L\* = 400, 1,600, 6,400.
  - Readings:
    - slice mass dimension and spectral dimension (readings v2);
    - the degree spread;
    - whether the degree spread grows with slice size;
    - the spacetime readings.
- **Recording** (exact ranges fixed in the spec):
  - **Uniform choice gives a flat slice** (slice dimension about 2, degree spread not growing): record "growth alone keeps a surface flat."
  - **Only the curvature cost gives it, at every size run:** record "quadratic energy keeps a grown surface flat at the sizes run: consistent, not derived; λ a knob."
  - **Flat only up to a size set by λ:** record "flat up to a crossover, as in equilibrium; 2D not reached at large scales" and go on to the 3D form on paper.
  - **Neither:** record "growing a flat 2D slice isn't reached with ED's local moves," and take stock.
  - **Structure checks** (topology, link condition, budget conservation) must be exact.
- **Expected results are fixed in the spec before any code.** Revise and retest is allowed and recorded.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide C3-Q1–C3-Q5, confirm the exit rule, spec C3a on paper** | The machinery test |
| **(b)** | **Skip to 3D on paper:** bistellar moves, and the two-bad-phases argument written as counts | The target, but heavier; 2D machinery first is cheaper |
| **(c)** | **Literature step first:** growth of random triangulations by vertex splitting, and 3D CDT's slice geometry | This check found no grown-surface studies; a deeper search could change the plan |

**Proposal: (a).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C42 | Ambjørn and Watabiki, *NPB* 445 (1995) (C20; [arXiv:1108.3327](https://arxiv.org/pdf/1108.3327)); Bowick, Catterall, Thorleifsson, [Suppressing curvature fluctuations in dynamical triangulations, hep-lat/9608076](https://arxiv.org/abs/hep-lat/9608076) (abstract); [Simulation of dynamical triangulation in 2D with higher order curvature terms](https://www.sciencedirect.com/science/article/abs/pii/0920563293903273) and related listings (crumpled, flat, branched-polymer states; crossover); [10D Euclidean dynamical triangulations, hep-lat/0306030](https://arxiv.org/pdf/hep-lat/0306030) (crumpled and branched-polymer phases, d_H → ∞ and d_H = 2, d_s = 4/3; Jonsson and Wheater, *NPB* 515, 549, 1998) (listing); Durhuus and Jonsson, [arXiv:1712.07502](https://arxiv.org/abs/1712.07502) (abstract); Budd and Loll, [arXiv:1305.4702](https://arxiv.org/abs/1305.4702) (abstract); Budd, [arXiv:1506.01590](https://arxiv.org/pdf/1506.01590) and Curien's peeling notes (listings) | 2026-09-16 |
| C43 | Counting: a vertex split adds 1 vertex, 3 edges, 2 faces (Euler characteristic unchanged); the children's degrees sum to deg v + 4; the average degree on a torus triangulation is exactly 6 (3F = 2E, V − E + F = 0) | Worked, 2026-09-16 |
| — | A6 D22, S-Q2 (D10), G-Q6, G-Q7; A7 C3, C14, C20, C31, C38, C39 | Ledgers |
