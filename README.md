# Event Density

**Event Density (ED) is an ontology** — an account of what the world is made of, underneath physics. It starts from one conviction: **time only runs one way.** Once something has happened, it can't be undone.

It is not a theory of gravity or a theory of everything. It asks a different question: *what must be true for anything to have a structure at all?*

**Untunability** is the part of ED that has been tested and held. These are quantities other frameworks must *tune*, turn out to be fixed by what ED conserves.**

This repository holds what survived testing, and the complete record of thirteen attempts that produced it — including everything that failed.

---

## The idea

- **The world is a web of places,** called *loci*. The web keeps growing: new places keep being born.
- **Things spread across the web like ripples,** trying out many paths at once.
- **When a ripple meets something already settled,** it leaves a mark. Once that mark can't be brought back, something definite has happened — a *commitment*.
- **Commitments use up a budget,** so near a lot of settled matter, clocks and motion slow down.

That's the picture. Everything else is working out what it implies.

---

## What survived testing

**1. A conservation law fixes three numbers a rival framework tunes by hand.** Causal dynamical triangulations has three totals that must be tuned until the spacetime it produces looks right. ED's conserved budgets fix all three, exactly, with no new free parameters.

**Checked against the literature, this splits.** In **2+1 it holds**: the value ED fixes is reachable, inside the phase where space doesn't collapse, on a program validated against published results. In **3+1 it is unresolved and leaning against**: ED needs a vertex density of 0.044 where published measurements near the nearest phase boundary are 0.152–0.164. One number decides it. → **[CDT_Constraint.md](CDT_Constraint.md)**

**2. Below three dimensions, clocks can't hold together.** Argued first, then measured: in one and two dimensions the pull needed to hold a pattern's clocks together rises without limit as it grows; at three and above it settles. ED's own content rules out one and two — it does not pick three.

**3. The handedness theorem.** Mirror-symmetric rules give exactly zero drift, so handedness can't be written into them. Proved, and checked by a script here.

**And a well-defended negative: nothing in ED creates a dimension.** Tested with ED's own definition of dimension, calibrated on known shapes, in the regime ED's own papers specify — sixteen runs, from a pattern with no dimension, and none ever appeared. **3+1 is a declared primitive of the ontology, not something it claimed to derive.** What the testing adds is that the declaration is honest.

**Full statements with their limits: [RESULTS.md](RESULTS.md). The framing: [Constraints.md](Constraints.md).**

---

## What didn't work

A lot, and every failure is written down.

- **Dark energy.** ED's distinctive versions were ruled out or disfavoured by astronomical data. What fits is the ordinary constant version.
- **Gravity.** Every simpler version of the budget failed a real measurement, and each fix made ED more like Einstein's theory.
- **Space.** Thirteen attempts could not get three dimensions out of ED, including the last one, which asked in ED's own terms with ED's own instrument.
- **Handedness in ED's own rules.** ED can settle into a handed state, but only with three ingredients added by hand. Three attempts to make ED supply the key one all failed.
- **The gap behind all of it.** ED says what may happen, not **where a new event goes.** Every attempt reached that same wall from a different direction.

---

## Where it stands

- **ED is an ontology:** a consistent, runnable account that agrees with known physics and constrains what is possible.
- **It doesn't tell us something about nature we didn't already know** — no new measurable prediction has come out of it.
- **Its lasting contributions:**
  - the untunability result: three tuned numbers of an established framework are not free — established in 2+1, open in 3+1;
  - the rate-matching floor, turned from an argument into a measurement;
  - the handedness theorem;
  - a clear, physical account of what makes a measurement final;
  - an unusually complete record of what doesn't work, and why.

---

## How the work was done

- **Tests set up in advance,** so results couldn't be quietly reinterpreted afterwards.
- **Every failure recorded,** including mistakes in the test code itself.
- **Literature checked first,** before claiming anything.
- **Tuned settings labelled** as tuned.
- **Results withdrawn when they didn't hold.** Five were, including one that matched a number to within 8% and was dropped within the hour once it moved when a setting moved.
- **An exit rule agreed ahead of time:** "if three honest attempts fail, stop and write it up."

---

## What's in this repository

| | |
|---|---|
| **Results** | [RESULTS.md](RESULTS.md) — what survived, each with what it does not show |
| **The untunability result** | [CDT_Constraint.md](CDT_Constraint.md) — written for readers who know causal dynamical triangulations |
| **The framing** | [Constraints.md](Constraints.md) — what ED forbids, fixes and leaves open |
| **The thirteen attempts** | [ED_Restart/Project_Write_Up.md](ED_Restart/Project_Write_Up.md), with the attempts themselves in [ED_Restart/](ED_Restart/) — each with its notes and a ledger of claims, decisions and a dated log. Attempts are closed records: referenced, never edited |
| **What ED needs** | [ED_Restart/What_ED_Needs.md](ED_Restart/What_ED_Needs.md) — what physics assumes, against what ED supplies |
| **The handedness theorem** | [handedness/](handedness/) — the one-page statement, the full proof, its assumptions, and a script that checks it |

## Check the theorem yourself

```
python handedness/check_result.py
```

Needs Python with numpy. It tests the theorem for up to six lanes, for random mirrors, and for hops reaching several places at once, plus two edge cases: traffic that only hops forward, and traffic without one-way time.

## Further reading

- H. B. Nielsen and M. Ninomiya, "A no-go theorem for regularizing chiral fermions," *Physics Letters B* 105, 219 (1981).
- J. Ambjørn, J. Jurkiewicz and R. Loll, on causal dynamical triangulations — the identities used in the untunability result are from [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267).
- The full reference list is in [handedness/Paper.md](handedness/Paper.md).
