# Event Density

**Event Density (ED) is an ontology** — an account of what the world is made of, underneath physics. It starts from one conviction: **time only runs one way.** Once something has happened, it can't be undone.

It is a theory of possibilities. It is not a theory of gravity or a theory of everything. It asks a different question: *what must be true for anything to have a structure at all?*

**Untunability** is what the testing found, and what this repository is named for: **quantities that established frameworks leave free, and tune by hand, turn out to be fixed by what ED conserves.**

---

## The idea

- **The world is a web of places,** called *loci*. The web keeps growing: new places keep being born.
- **Things spread across the web like ripples,** trying many paths at once.
- **When a ripple meets something already settled** it leaves a mark. Once that mark is made, it can't be brought back; something definite has happened — a **commitment**.
- **Commitments use up a budget,** so near a lot of settled matter, clocks and motion slow down.

Everything else is working out what that implies.

---

## What was tested

ED was turned into exact rules a computer can run, and tested against three questions:

1. **Does ED's structure constrain the free parameters of an established theory of quantum spacetime?**
2. **Does ED's requirement that clocks keep time together restrict the shape space can take?**
3. **Can ED's rules produce three-dimensional space, rather than being given it?**

Every test had its expected results written down before it ran.

---

## What we conclude

**1. Untunability: ED's conservation laws fix three numbers that causal dynamical triangulations tunes by hand.**

CDT builds spacetime from two kinds of four-dimensional block, stacked in time-slices, and three totals are left free to be tuned until the result looks like a universe:

| | what it counts | tuned through |
|---|---|---|
| **N₀** | the corner points | κ₀ |
| **N₄₁** | blocks with four corners on one slice and one on the next | Δ |
| **N₃₂** | blocks with three corners on one slice and two on the next | κ₄ |

**ED's conserved budgets fix all three.** Its commitment budget fixes N₀, its link budget fixes N₄₁, and conserving forward links fixes N₃₂ through an exact identity, N₁ᵀ = 2N₀ + N₃₂/2. Arithmetic, no new free parameters. In 2+1 dimensions the point they fix is reachable and sits inside the phase where space does not collapse.

**2. Below three dimensions, clocks cannot keep time together.** A patch's timing surplus grows faster than the connections available to shed it through, so in one or two dimensions large patches always break away. Measured, not just argued: the coupling needed rises without limit in one and two dimensions, and settles at three and above.

**3. Handedness cannot be written into mirror-symmetric rules.** A proved theorem, checked by a script here: symmetric rules give exactly zero drift. If the world has a handedness — and it does — its state picked it, not its laws.

**4. ED conditions space; it does not produce it.** Three-plus-one is a declared primitive of the ontology. Testing confirms the declaration is honest: ED carries a dimension it is given and never manufactures one. What it adds is that the primitive is *partly forced* — result 2 rules out one and two dimensions from ED's own content.

**Full statements with their scope: [RESULTS.md](RESULTS.md). The technical case for result 1: [CDT_Constraint.md](CDT_Constraint.md). What ED forbids, fixes and leaves open: [Constraints.md](Constraints.md).**

---

## Where it stands

ED is a consistent, runnable ontology that agrees with known physics and constrains what is possible. It has produced no new measurable prediction, and it doesn't claim to — its founding statement is that it supplies *"the conditions of possibility, not the full catalogue of outcomes."*

The open question it reaches from every direction: **ED says what may happen, not where a new event goes.**

---

## What's here

| | |
|---|---|
| [RESULTS.md](RESULTS.md) | the findings, each with its scope |
| [CDT_Constraint.md](CDT_Constraint.md) | result 1 in full, written for readers who know causal dynamical triangulations |
| [Constraints.md](Constraints.md) | what ED forbids, what it fixes, what it leaves open |
| [Negative_Results.md](Negative_Results.md) | what ED was tested for and did not do, and how thoroughly that was checked |
| [Handedness/](Handedness/) | the theorem: statement, proof, assumptions, and a script that checks it |

## Check the theorem yourself

```
python Handedness/check_result.py
```

Needs Python with numpy. It tests the theorem for up to six lanes, for random mirrors, and for hops reaching several places at once, plus two edge cases: traffic that only hops forward, and traffic without one-way time.

## Method

Tests were specified before they were run, with expected results recorded in advance. Published work was checked before claiming anything. Settings chosen to make something work are labelled as tuned. The complete working record, including every model that didn't work, is held separately and available on request.

## Further reading

- H. B. Nielsen and M. Ninomiya, "A no-go theorem for regularizing chiral fermions," *Physics Letters B* 105, 219 (1981).
- J. Ambjørn, J. Jurkiewicz and R. Loll on causal dynamical triangulations; the identities used in result 1 are from [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267).
- Full references in [Handedness/PAPER_Reflection-Symmetric Transport Carries No Handedness.md](Handedness/PAPER_Reflection-Symmetric%20Transport%20Carries%20No%20Handedness.md).
