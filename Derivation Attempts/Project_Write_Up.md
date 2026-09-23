# Event Density, tested: what thirteen attempts established

*A cross-attempt write-up, 2026-09-23. Not part of any attempt's ledger, and no closed record is edited. Sources: the ledgers of ED_Restart attempts 1–13, and Allen Proxmire's ED papers of January and February 2026. Written plainly.*

---

## What this is

Event Density (ED) is Allen Proxmire's ontology: the universe is made of **becoming** before it is made of things. Events happen; how densely they happen in a region is its event density; differences in that density are what everything else is made of.

This document reports what happened when that ontology was **tested** — thirteen attempts, each with its meanings fixed before anything was computed, its expected results written down before anything was run, and every miss recorded.

**What ED claims** was settled during attempt 13, from Allen's own January paper:

> *"ED does not predict every structure in the universe. It explains why structure is possible... conditions of possibility, not the full catalogue of outcomes."*

So a result here does not have to **derive** a structure. It has to state a **constraint** on what structures are available, and show that it holds.

---

## What was established

### 1. ED's budgets fix three numbers a rival theory tunes by hand

**The strongest result, and the only genuine reduction.**

Causal Dynamical Triangulations (CDT) is a well-developed approach to quantum spacetime. It has three totals that must be **tuned** until the universe it produces looks right. ED does not tune them: two are fixed by its conserved budgets, and conserving forward links fixes the third.

**ED lands on one point of CDT's map with no dials touched** — and in 2+1 dimensions that point sits *inside* the phase where space does not collapse.

Exact algebra, not a simulation. No new free numbers. And it is exactly the kind of claim ED's own ontology says it makes: a constraint on what is available, not a prediction of a structure.

*(Attempt 11, C5, C8. The program that produced the surrounding runs was checked against published CDT results and reproduced them, including a known phase transition — attempt 11, C17.)*

**Added 2026-09-23, after the attempts were concluded, from a literature check.** Three questions were put to the literature rather than left open, and the answers split this result:

- **The identities are standard; the reading is not.** In CDT these totals are *ensemble* variables whose averages the couplings fix. ED fixes the counts themselves, so the claim is **microcanonical**: ED picks a definite point, and the open question is whether CDT's ensemble reaches it. That is a sharper and more falsifiable statement than "ED sits at a point of CDT's map".
- **In 2+1 the claim strengthens.** The value ED fixes (τ = 1/3) is reachable at about k₀ = 3.2, inside the extended phase — measured on the validated program rather than extrapolated, which was the earlier caveat.
- **In 3+1 the claim is unresolved and leaning against.** ED requires a vertex density N0/N4 of 0.044. The published order parameter near the A–C transition measures 0.152–0.164 ([arXiv:1203.3591](https://arxiv.org/abs/1203.3591), Fig. 21) — about three times larger. No value is published at CDT's canonical point, and that single number decides it.

*Recorded here rather than in attempt 11's ledger, which is a closed record.*

### 2. Below three dimensions, clocks cannot hold together

ED says events carry rates, and that rates must be able to match across a pattern. Attempt 6 argued that this needs more than two dimensions: a patch's rate surplus grows like the square root of its size, the relations crossing its edge grow more slowly in one or two dimensions, so large patches always break away.

**Attempt 11 measured it.** On a line and on a flat grid, the pull needed to hold the clocks together rises without limit as the pattern grows. On a three-dimensional grid and on a random web, it settles and stops rising.

An argument became a measurement. *(Attempt 11, C21.)*

### 3. Nothing in ED creates a dimension

**The central negative, and the most heavily tested claim in the project.**

Attempt 13 did three things no earlier attempt had: it ran in the regime ED's own papers specify (thick participation, not the sparse minimum), it used ED's own definition of dimension (*"the number of independent participation directions available at scale"*, paper 10), and it calibrated that instrument on shapes already known — a ring reads 1, a flat grid 2, a cubic grid 3, a random web nothing.

Then: grow a pattern from a **random web**, which has no dimension to begin with, under every rule ED supplies — passing on, spent events, inherited neighbourhoods, gradients that persist and diffuse, patches shedding their rates through their own edges.

**Sixteen runs, two sizes, eight seeds: no dimension ever appears.** Not weakly, not marginally — no structure at all in the readings.

*(Attempt 13, C10, C11.)*

**This also corrected the record.** The borrowed instrument used for the previous twelve attempts — ball growth — disagrees with ED's own definition by **more than a whole dimension, in both directions**. Twelve attempts of "no dimension" were measured with the wrong ruler, in the wrong regime. The answer came out the same, but only attempt 13's version is evidence.

### 4. ED's growth degrades directional structure as it grows

New in attempt 13, and stated as a constraint rather than a mechanism.

A clean three-dimensional lattice reads exactly 3 at every thickness, and survives having **100% of its relations locally re-pointed**. But grown under ED's rules, its signature blurs steadily — the modes stay, their spread widens — until it can no longer be read. A line, which starts with twice the margin, survives.

**It is not hostile to three dimensions.** It is corrosive to all directional structure, and three has less room before it goes. *(Attempt 13, C14, C15.)*

### 5. Patterns fall apart below about five relations per event

A threshold nobody had measured. Below it, a growing pattern fragments into disconnected pieces. Above it, it holds together and copies itself more faithfully as the count rises. *(Attempt 12, C7.)*

### 6. ED never collapses

In the 2+1 runs, from either starting condition, ED's rules never produced the collapsed phase that the rival theory falls into outside its tuned window. From a flat start, ED's readings sat on top of the extended phase's at both sizes. *(Attempt 11, C20.)*

---

## What was not established

- **Three dimensions from ED.** Not derived, not selected, not produced.
- **Space produced rather than supplied.** Every model was given a starting shape. ED carries it, blurs it, and constrains it — it does not make it.
- **Where a first shape comes from.** Untouched.

**The census, honestly:** three inputs are supplied (the Born rule, the area law, one time dimension), plus a starting shape in every model. **Nothing has been derived.** The budget result is a reduction in a *rival theory's* free numbers, not in ED's own input list.

---

## Six things ED was found to be missing, and who found them

The most useful pattern in the whole project. Five times, a model turned out to lack something ED had already written down — and three of those were caught by Allen from the meaning alone, with no numbers in front of him.

| | what was missing | found by |
|---|---|---|
| 1 | **ED's clocks.** Four attempts had tested a borrowed picture of space with no rates in it at all | Allen |
| 2 | **No shared now.** A global lock had been built into the test; ED has denied one since attempt 6 | Allen |
| 3 | **Relations that dissolve, and commitment that persists.** Every repair had been permanent — a ratchet | Allen |
| 4 | **Gradients.** Rates were random noise, redrawn every tick; ED says space *is* persistent gradients | from the January paper |
| 5 | **Thickness.** Every model ran at the sparse minimum; ED says dimension exists only in thick participation | from paper 11 |
| 6 | **ED's own instruments.** Dimension and distance are defined in ED's papers, and neither was what was being measured | from paper 10 |

Each correction changed the model's behaviour measurably. **None changed the answer.**

---

## What was got wrong, and withdrawn

Recorded because a project that never withdraws anything is not measuring.

- A number matching ED's link budget to within 8% — **withdrawn within the hour**, once it moved when a setting moved.
- "A shape is carried, not chosen", agreed by two attempts — **corrected**: it had been measured with ED's sync requirement switched off.
- "The thick regime preserves a dimension exactly" — **withdrawn**: three seeds counted nine ways; eight independent seeds gave one in eight.
- "ED's growth is hardest on exactly the shape we want" — **withdrawn**: it is hardest on everything.
- A test whose noise model destroyed every shape at 2% and told us nothing — **rebuilt** before it was read.

**The method that produced the surviving results: fix the rule before the run, and build the run that can destroy the result.** Every claim above survived something written down in advance that could have killed it.

---

## Where this leaves ED

**On the evidence, ED is a theory of conditions.**

It says what a pattern of events must satisfy to hold together, and that condition is real and measurable. It fixes numbers another theory has to guess. It carries a shape forward and blurs it as it grows. It never collapses.

**It does not make space, and it does not pick three.** On its own account — *conditions of possibility, not the full catalogue of outcomes* — it was never claiming to.

**That is a smaller claim than the one the project spent thirteen attempts testing, and it is the one the evidence supports.** It is also the claim ED's own founding paper makes.

---

## What would change the picture

Three things, in order of how much they would settle:

1. **Something in ED that says where a new event goes.** This is the gap every attempt eventually reached. ED specifies what may happen, not where. Until it does, a shape must be supplied.
2. **A second genuine reduction.** The budget result shows the form such a claim takes: *a rival theory's free parameter is not free, given ED's conservation.* Whether there are others is untested.
3. **A prediction that differs from the standard account and can be checked.** None has been produced here.

---

## How to read the record

Each attempt has its own folder under `Derivation Attempts/`, with a `README.md` listing its notes in order, and an `01_Ledger/` holding three files: **Claims** (what was established, with status and evidence), **Assumptions** (Allen's decisions, and the road decisions taken from them), and a dated **Log**. Attempts are closed records: referenced, never edited.

The most load-bearing notes, if you read only a few:

- **Attempt 11**, `L_Layer.md` and `L_Literature.md` — the budget result and where ED sits on the rival theory's map.
- **Attempt 11**, `Audit.md` — what in the model was ED's, what was borrowed, and what was missing.
- **Attempt 13**, `E_The_First_Paper.md` and `E_Paper_11_Dimension.md` — what ED's own papers say that the models never contained.
- **Attempt 13**, `E_The_Answer.md`, `E_Solid.md` and `A_Asymmetry_Results.md` — the central negative, its strengthening, and the deflation of a result that did not survive.
- **`What_ED_Needs.md`** — the standing count of what ED supplies against what physics assumes.
