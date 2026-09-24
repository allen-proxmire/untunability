# Results

*The findings, each with its scope. Last updated 2026-09-23.*

**Event Density (ED) is an ontology** — an account of what the world is made of, from which physics is supposed to follow. **Untunability** is the name for the part of it that has been tested and held: the claim that quantities other frameworks leave free are fixed by what ED conserves.

Each result below had its expected outcome recorded before it was tested. The working record is held separately and available on request.

---

## 1. Untunability: a conservation law fixes three numbers CDT tunes

Causal dynamical triangulations is a well-developed approach to quantum spacetime. Its bulk counts leave **three totals free** — **N₀**, the corner points; **N₄₁**, the blocks with four corners on one time-slice and one on the next; and **N₃₂**, the blocks with three on one slice and two on the next. Those three are what its couplings κ₀, Δ and κ₄ are tuned against.

**ED's conserved budgets fix all three.** The event budget fixes N₀, the link budget fixes N₄₁, and conserving forward links fixes N₃₂ through an exact identity, N₁ᵀ = 2N₀ + N₃₂/2. The result is a single point with nothing tuned — and in 2+1 dimensions that point sits **inside the phase where space doesn't collapse**, rather than the collapsed one.

Exact algebra. No new free parameters.

**Scope.** It is a statement about CDT's framework, not about nature: *if* spacetime is a CDT-like triangulation, this conservation removes the freedom. It predicts nothing newly measurable. The step linking ED's budgets to CDT's totals rests on recorded modelling decisions. **No one who works on CDT has reviewed it.**

**And it splits in two when checked against the literature.** In **2+1 it holds**: ED's conservation fixes the order parameter at exactly 1/3, and a validated run reaches that value inside the extended phase, at around k0 = 3.2. In **3+1 it is unresolved and currently leaning against**: ED needs a vertex density N0/N4 of 0.044, while the published measurements near the A-C transition are 0.152-0.164 — about three times larger. That number decides it, and anyone with a CDT code could settle it in an afternoon.

**The honest framing, also found by checking:** CDT treats these totals as ensemble variables that fluctuate, with the couplings fixing only their averages. ED fixes the counts themselves. So the claim is *microcanonical* — ED picks a definite point, and the question is whether CDT's ensemble ever reaches it.

**Full version, with the identities and the caveats: [CDT_Constraint.md](CDT_Constraint.md). The negative findings are in [Negative_Results.md](Negative_Results.md).**

---

## 2. The rate-matching floor, measured

ED says events carry rates that must be able to match across a pattern. The argument: a patch's rate surplus grows like the square root of its size, the relations crossing its edge grow more slowly in one or two dimensions, so large patches always break away.

**That was turned from an argument into a measurement.** On a line and on a flat grid, the pull needed to hold the clocks together **rises without limit** as the pattern grows. On a three-dimensional grid and on a random web, it **settles** and stops rising.

So ED's own content rules out one and two dimensions.

**Scope.** It doesn't pick three — three and everything above it pass equally. And it says nothing about where a pattern's shape comes from.

*Working record: attempt 11, claim C21.*

---

## 3. The handedness theorem

A proved theorem, checked by a script in this repository: in a hopping model, **mirror-symmetric rules give exactly zero drift.** Handedness cannot be written into rules that look the same in a mirror — if a world has one, its state picked it, the way a magnet picks a direction its laws don't prefer. And handedness is possible at all only because time runs one way.

**Scope.** The mathematics is simple and something close to it is already known (Nielsen–Ninomiya). ED's own rules can settle into a handed state, but only with three ingredients supplied rather than derived.

*Where: [Handedness/](Handedness/).*

---

## 4. On the rules tested, ED conditions space rather than producing it

**No dimension appeared under any rule set tested.**

This was tested in the regime ED's own papers specify (thick participation, not the sparse minimum), with **ED's own definition of dimension** — *"the number of independent participation directions available at scale"* — calibrated first on shapes already known: a ring reads 1, a flat grid 2, a cubic grid 3, a random web nothing.

Then, starting from a pattern with no dimension and growing it under every rule ED supplies: **sixteen runs, two sizes, eight seeds — none ever appears.**

These rules carry a dimension they are given, blur it as the pattern grows, and never make one. That is a result about this formalisation; it is not a proof that no ED mechanism could.

**3+1 is a declared primitive of the ontology**, not something it claimed to derive. What the testing adds is that the declaration is honest: dimension is genuinely an input, not something assumed and then presented as a result. Taken with result 2, the primitive is *partly forced* — one and two dimensions are excluded by ED's own content, narrowing the input from any number of dimensions to three or more.

*Working record: attempt 13, claims C10, C11, C15.*

---

## 5. Further findings

- **Patterns fragment below about five connections per event.** A threshold on how sparse a web can be and still hold together. *(Working record: attempt 12, claim C7.)*
- **ED never collapses.** In the 2+1 runs, from either starting condition, it never produced the collapsed phase CDT falls into outside its tuned window. *(Working record: attempt 11, claim C20.)*
- **A regular lattice cannot be ED's substrate.** On a grid, the connections crossing a surface depend on which way it faces (1.00, 1.41, 1.73), which would make gravity direction-dependent. ED's connections must point every way equally.
- **ED's growth degrades directional structure as it grows** — at a similar rate whatever the dimension. *(Working record: attempt 13, claim C15.)*

---

## What is supplied, and what is derived

**Supplied:** the Born rule, the area law, 3+1 dimensions, and a starting shape in every model.

**Derived:** nothing. The untunability result is a reduction in a *rival framework's* free numbers, not in ED's own input list.

That distinction is kept deliberately. A result counts as a reduction only if ED's own list of what must be assumed gets shorter, with no new free parameters. None has.

---

## What would change the picture

1. **Something in ED that says where a new event goes.** Thirteen attempts each reached this wall from a different direction. ED specifies what may happen, not where. Until it does, a shape must be supplied.
2. **A second untunability result** of the same form: *a free parameter of an established framework is not free, given this conservation.*
3. **A checkable difference from the standard account.** None has been produced.

---

## Method

Every test was specified before it ran, with its expected outcome recorded in advance and its instruments calibrated against objects whose answers were already known. Published work was checked before anything was claimed. Settings chosen to make something work are labelled as tuned.

The working record — thirteen model builds with their ledgers, dated notes, code and data — is held separately and available on request.
