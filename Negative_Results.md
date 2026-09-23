# Negative results: what ED was tested for and did not do

*Allen Proxmire, 2026-09-23. A companion to [RESULTS.md](RESULTS.md). The working record behind it is in the [ED-generative repository](https://github.com/allen-proxmire/ED-generative), under `Derivation Attempts/`.*

---

## Why this document exists

A framework is only worth as much as the things it rules out about itself. These are the tests ED was put through that came back negative, stated as findings rather than as a narrative.

They are here rather than in the main results because they are a different kind of claim: **not "ED does X", but "ED does not do X, and here is how thoroughly that was checked."**

---

## 1. ED does not produce a spatial dimension

**The test.** Grow a pattern under every rule ED supplies — events passing on a conserved budget, commitments that persist, neighbourhoods inherited from parents, rates that pass on and diffuse, patches required to shed their timing surplus through their own edges — starting from a pattern that has **no dimension at all** (a random web). Then measure whether one appears.

**How it was measured.** With ED's own definition of dimension, from the ontology's own papers: *the number of independent participation directions available at scale.* On a pattern of events and connections this is a definite quantity — the slowest modes come in groups, two per independent direction. **Calibrated first on shapes whose answers are known:** a ring reads 1, a flat grid 2, a cubic grid 3, a random web nothing.

**The result.** Sixteen runs, two sizes (8,000 and 16,000 events), eight independent seeds: **no dimension ever appeared.** The modes showed no grouping at all — the separation between them stayed within 1% of nothing.

**Controls in the same runs:** a ring start read exactly 1 in sixteen of sixteen, with a clean separation. So the instrument was working; there was simply nothing to find.

**What this is not.** It is not evidence against the ontology. **3+1 is a declared primitive of ED**, not something it claimed to derive. What the test establishes is that the declaration is honest — dimension is genuinely an input, not something assumed and later presented as a result.

---

## 2. ED's growth degrades directional structure

**The test.** Take a pattern that *does* have a dimension — a three-dimensional grid — and grow it under ED's rules. Does it keep its shape?

**The result.** It blurs. The mode structure that marks out three directions stays present but its internal spread widens steadily as the pattern grows, until the dimension can no longer be read cleanly. A one-dimensional pattern survives, because its signature starts with roughly twice the margin.

**Checked against the alternatives.** Not an artefact of thickness: a clean lattice reads exactly 3 at every connection density tested. Not ordinary noise: a lattice survives having 100% of its connections locally re-pointed. Not the randomness in how a parent's neighbourhood is divided: making that division consistent changes nothing.

**What it says.** ED's growth is corrosive to directional structure generally, at a similar relative rate whatever the dimension. It is not selectively hostile to three.

---

## 3. Nothing in ED says where a new event goes

**The finding behind the other two.** ED specifies what may happen — an event passes on its budget, commitments stick, rates must be able to match — but not **where** a new event attaches.

Thirteen independent model builds reached this from different directions. It is the reason a starting shape has to be supplied in every model, and the single most likely place for the ontology to be extended.

---

## 4. Approaches that were ruled out

| approach | outcome |
|---|---|
| **A further conserved quantity** that would prefer extended space | None exists beyond the budgets already identified |
| **Costs** (energy-like penalties) as the mechanism preferring extended space | Push the wrong way; conditions work where costs don't |
| **Counting histories** as the source of a preference for extended space | Shape barely moves under counting; histories stay where they start |
| **Distinctive dark-energy mechanisms** (fluctuating births; births tied to the horizon) | Ruled out or disfavoured against astronomical data; the ordinary constant version is what fits |
| **Simpler gravitational budgets** | Each failed a real measurement, and each repair made the account more like general relativity |
| **A regular lattice substrate** | Excluded: on a grid, connections crossing a surface depend on which way it faces (1.00, 1.41, 1.73 for edge, face-diagonal and body-diagonal), which would make gravity direction-dependent |

---

## 5. What is supplied rather than derived

**Supplied:** the Born rule, the area law, 3+1 dimensions, and a starting shape in every model.

**Derived:** nothing, in the strict sense. The untunability result ([CDT_Constraint.md](CDT_Constraint.md)) reduces a *rival framework's* free parameters, not ED's own input list.

This distinction is kept deliberately: a result counts as a reduction only if ED's own list of what must be assumed gets shorter, with no new free parameters added.

---

## 6. How thoroughly this was checked

Thirteen model builds, each with its meanings fixed and its expected results recorded before anything ran. Instruments were calibrated against objects with known answers before being used to measure anything unknown, and two were found wanting and replaced.

**Five results were withdrawn on their own checks**, including one that matched a number to within 8% and was dropped once it moved when a setting moved, and one that rested on three correlated seeds and did not survive eight independent ones.

The complete record — ledgers, dated notes, code and data — is in the [ED-generative repository](https://github.com/allen-proxmire/ED-generative) under `Derivation Attempts/`.
