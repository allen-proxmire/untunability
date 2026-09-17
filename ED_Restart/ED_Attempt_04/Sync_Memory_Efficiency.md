# Sync, memory, and the shape of efficiency

*ED_Attempt_04, note 11. 2026-09-15 (RD15, D20–D23). Ledger: C61–C67. Repo reading, literature and reasoning; nothing computed. It covers Allen's four points, what the old ED repo already tried, and what they do to R4 and route E-C.*

## Allen's four points

1. **"Clocks want to sync."** It isn't commitment attracting commitment. Everything is "trying to get to the center of the sync": a uniformity attraction. A thrown ball becomes more unsynced and tries to sync back up; "the ground is the best it can do" (D20).
2. **No records are held.** "There's nowhere to hold a record." A draw is fixed only in that it happened, and that is reflected in whatever the current state is (D21).
3. **Maybe short-lived memory,** "like a chain might have some memory with it" (D22).
4. **The shape of efficiency.** Allen's Architectural Distillation (AD) method is "basically what Tao did but generalized". Isn't that "what all the constraints come out to be"? (D23)

## 1. Clocks want to sync (C61, C64)

**What physics says:**
- **Clocks run slower near mass,** and things fall toward slower clocks.
- **A freely moving object takes the path on which its own clock ticks the most** between two events: the "principle of maximal aging" (Taylor and Wheeler).
- **A thrown ball** rises to where clocks run faster, but moving fast slows its clock. The path it actually takes is the best balance of the two.

**Where Allen's picture and physics agree:**
- **The ball comes back.**
- **At rest on the ground, its clock matches the ground's.** That is "synced", and the ground stopping it is "the best it can do".

**Where they differ (pokes):**
- **Orbits.** A satellite never syncs back; it stays unsynced forever. Maximal aging handles orbits. A sync picture has to say why an orbit doesn't decay toward sync.
- **Sync with what?** Falling is toward *slower* clocks, not toward matching a neighbour's rate. Averaging with neighbours would spread differences out, not pull things in.
- **"Most ticks" is only a local best.** In a tunnel through the Earth, free fall is not the global maximum (Gomes 2026). The older picture, speed plus height changing clock rates, gets it right. That older picture is close to Allen's.

**What the old ED repo already found (C63):**
- **A chain's tick is a rhythm:** "re-committing with finite memory is a rhythm". More memory makes a slower clock.
- **A coupling with finite reach locked nearby chains to a shared rate:**
  - the spread within a group fell from 0.084 to 0.0005;
  - distant groups kept their different rates, which is time dilation;
  - global sync did not happen, and the paper calls that correct, because universal sync would freeze everything.
- **Status:** both the memory channel and the coupling were **"honest additions"**, not derived, and measured only in simulation.

**What it does to R4:**
- **R4's idea changes** from "loci want to be on" to "clocks want to match nearby rates".
- **Local sync is supported,** but only where it was added by hand.
- **Global sync is the old repo's own poke** against the synced ball (D8): perfectly uniform becoming is no becoming.
- **The open R4 question:** does local rate-matching pull things toward *slower* clocks, which is falling, and does it leave orbits alone?

## 2. No records are held (C65)

**What changes:**
- **Route E-C leaned on records** (note 10). Under D21 nothing is stored. The past is in the present state only.
- **E-C restated: selection by what the present can carry.**
  - **In three dimensions** a knot's kind is part of the present state, and the present keeps it.
  - **In four or more,** differences of kind relax away, so the present carries no lasting differences.
  - **So "4 is never considered" becomes:** nothing from a fourth direction survives into the present.
- **It's leaner:** there's no storage, only state.
- **The old repo agrees in spirit.** A committed fact is "persistent without any sustaining channel", while live correlations fade.

**Pokes:**
- **"The past is in the present state" is the ordinary idea of state.** It isn't new.
- **The circularity guard still applies:** dimension can't be defined by knots.
- **Annihilation (C55) still has to be faced.**

**E-Q4 revised:** does "4 is never considered" mean a fourth direction never forms, or that it leaves nothing the present keeps? **Default:** leaves nothing the present keeps.

## 3. Short-lived memory (C63, C66)

**What the old ED repo has:**

| memory | what carries it | how long it lasts | status there |
|---|---|---|---|
| **Chain-carried "history" value** | Each chain carries a value that fades and is topped up by each commitment | Set by a fade rate, **a free parameter** | **Added, not a primitive.** Simulation only. It made a **slow clock (time dilation), not mass** |
| **V5 kernel** (between chains) | Correlations between chains, fading with time | Memory time **matched to data in each regime** | Posited. The outside review: "no predictive content", since the memory time "fits any exponential relaxation" |
| **V1 kernel** (within a chain) | A chain's past participation reaching its present | Set at the Planck length by assumption | Postulated. The review calls its arguments "informal" |
| **Live versus committed** | Uncommitted correlations fade; committed facts stay as structure | Fading unless sustained | The accounting matches D21 |

**So Allen isn't way off.** The old repo tried exactly "a chain has some memory". It found:
- **Memory gives a chain its tick,** and more memory means a slower tick.
- **Nearby ticks can lock together.**
- **Memory made a clock, not mass.**

**But the memory's length was never derived.** It was a free fade rate or a fitted time. That's the trap.

**The lesson for attempt 4:**
- **Short memory is where a clock's rate could come from.** A tick is re-committing with some memory. Sync is ticks locking. That ties D20 and D22 together.
- **It counts only if the memory length comes from ED's meanings.** ED already has one short-lived thing without adding anything: **what's uncommitted is live until a draw**, and a draw ends it.

**E-Q5 (new):** is there short-lived memory beyond what's uncommitted? **Default:** no. What's uncommitted is live until a draw, and that's the only short-lived thing. Anything more needs its length to come from ED's meanings, not a fitted rate.

## 4. The shape of efficiency (C62, C67)

**What AD does, in one line:**
- constraints from the axioms give an **envelope** (what's forbidden, what's forced, the bounds);
- the equations give the **extremes** and where things settle;
- the interactions give a **constraint surface** with faces;
- then it asks whether the whole is minimal, tight and optimal.

Applied to Tao, Trudgian and Yang's exponent database, AD found the whole computation lives on one five-dimensional shape, **with the best value (3/2) at a single corner.**

**Allen's question: isn't that what all constraints come out to be?** The pattern is old, and it works:

| where | the shape | where the answer sits |
|---|---|---|
| Linear optimization | Constraints cut out a many-sided shape | At a corner |
| Biology (Shoval et al. 2012) | Trade-offs between tasks give a triangle or tetrahedron | Best compromises fill it; the corners are single-task specialists |
| Tao–Trudgian–Yang exponent database | Known bounds and their relations | The best exponent at an extreme point |
| Thermodynamics (Sivak–Crooks; Frim–DeWeese) | A geometry on the states a system can pass through | Least-waste paths are its straight lines. Efficiency is bounded by the cycle's shape |
| Quantum correlations | The set of possible correlations | Quantum mechanics reaches the Tsirelson bound and stops |
| Free fall | All paths between two events | The one with the most ticks |

**So yes: constraints always come out to a shape, and nature often sits at a special point of it.**

**The catch:**
- **"Efficient" needs a named quantity.** Something has to be the thing that's most or least.
- **Without naming it, any point on any boundary can be called efficient.** That's the fitting trap in a new form.
- **The honest version:** the shape comes from the constraints; the efficiency is which quantity is extremized; **ED has to name that quantity from its meanings before looking where the world sits.**

**Two kinds of special point:**
- **Edges and corners** are where a quantity is at its most: the best exponent, the most ticks.
- **The centre** is where things are most uniform. In attempt 3, **the fair coin sat at the centre of the coin-odds shape**, with Grover on the edge ("the attractor is the shape").
- **Allen's "center of the sync" is a centre-seeking picture:** uniformity, not a corner. So ED may have both kinds, uniformity (sync, fair coin) and extremes (most ticks). Which one applies where would have to be fixed from the meanings.

**The three-dimensional results, as a shape:**
- **Each root boxes dimension in from both sides:**
  - knots need at least 3 to exist and at most 3 to last;
  - spreading needs at most 3 for orbits and at least 3 for gravity.
- **Each root's allowed region shrinks to a single point: 3.** In AD's words, the envelope is tight.

**A caution about AD itself:**
- **AD scored the old ED 6/6 twice** (the PDE and the substrate).
- **The old repo's own outside review** found much of that corpus restated textbook physics with parameters inherited, V5's memory times included.
- **AD checks whether the parts fit together, not whether anything is derived.** It says so itself. So it can't be the bar for attempt 4.
- **The old ED PDE even took "dimensional universality" as an axiom,** the opposite of picking three.

**Two parts of AD would help attempt 4:**
- **Mode 1:** forbidden and forced configurations from the meanings alone. Note 9's knot argument already has that form.
- **The census:** independent constraints versus free parameters. A result with more free parameters than constraints is a fit, and the count makes that visible.

## What it does to E-C and R4

- **E-C survives, and is leaner:** selection by what the present can carry (D21), with the uncommitted as the only short-lived thing (E-Q5's default).
- **E-C can be written as a shape:**
  - constraints from ED's meanings cut down the possible dimensions;
  - the quantity is named first: lasting differences the present can carry;
  - then check what's left.
- **R4 is reshaped:** clocks matching nearby rates (D20), with the old repo's local-sync result as a worked example of a mechanism that was added by hand. The pokes are orbits, and falling toward slower clocks rather than averaging.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Write E-C on paper as a shape:** answer E-Q1–E-Q5 (or accept the defaults), confirm the exit rule, add the constraint/free-parameter count as a guard, then do the argument | The live road, now leaner; the shape framing gives it a clear form |
| **(b)** | **R4 on paper, reshaped:** does matching nearby clock rates pull toward slower clocks, and does it leave orbits alone? | The sync picture's two pokes, checked before any model |
| **(c)** | **A short method note:** "the shape of efficiency" for ED. Constraints from meanings, the quantity named first, then look | Turns D23 into a rule every road follows |

**Proposal: (a), with (c) folded in** as its first section.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C61 | Taylor and Wheeler's principle of maximal aging, as described in Science 2.0 and a Physics Forums thread; Gomes, "Boomeranging through the Earth", arXiv:2609.04231 | Abstract, listings |
| C62 | Architectual Distillation repo: README, ad_docs/AD_methodology.md, ad_core/01 and 03, evaluations/AD_Evaluation_EventDensity.md, atlas/entries/ED_Substrate_AD_Entry.md, the exponent-database architecture spec, AD_Note_SubstrateBeneathTheShadow.md; Tao, Trudgian, Yang arXiv:2501.16779 and the ANTEDB site; Shoval et al., *Science* 336, 1157 (2012), with Edelaar's Comment and the authors' Response; Sivak and Crooks, arXiv:1201.4166; Frim and DeWeese, arXiv:2112.10797; Tsirelson's bound (Wikipedia; arXiv:1807.09115) | Repo read directly; abstracts and listings |
| C63 | ED Generative: `Paper_RelationalTick_v1.md`, `Paper_MassWithoutMass_BindingInertia.md`, `Paper_QuantumDarwinism_RecordBandwidth.md`, `Paper_090_V5Kernel.md`, `Paper_089_V1Kernel.md`, `Paper_113_ArcM_H1_MassStructuralForm.md`, dwell notes, `REVIEW_2026-09-12.md` | Searched by a read-only agent; key passages checked directly (sync numbers, "honest additions", live versus committed, slow clock not mass) |

**Update (D25):** Allen: 'you gotta put it all together'. Sync and maximal aging are one rule: a body's path makes its own commitment as large as it can, with height raising the rate and speed lowering it; orbits follow, and the orbit poke in §1 is withdrawn (C71). E-C as a shape: [E_C_As_A_Shape.md](E_C_As_A_Shape.md) (note 12).

**Update (RD17):** R4 started on paper in [R4_One_Rule.md](R4_One_Rule.md) (note 13): Allen's speed/ticking duality (D28) and three tick counts checked against muon lifetimes.
