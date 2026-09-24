# Working rules

*The standards this work ran under. Each one is here because breaking it cost real time.*

---

## Part one: the rules

### 1. Write the rule before the story

The first thing you write is a rule a computer can run. Interpretation comes after.

A template for starting from nothing:

- **State:** a graph or grid, perfectly uniform.
- **The first difference:** one site differs.
- **The rule:** how a difference spreads, and the fact that it cannot un-spread (the arrow).
- **The run:** watch what grows.

If a statement can't be turned into code or a formula, it is not yet a starting point. It is a hope about one.

### 2. Test every result with three questions

"Assume x, y, z, get A" is legitimate physics — Jacobson got Einstein's equations that way — when all three answers are yes:

1. **Are the assumptions precise?** Definite enough to calculate with, not words.
2. **Does a real calculation connect the assumptions to A?** A must not be the assumptions restated.
3. **Could A have come out wrong?** If no possible outcome would count against it, it isn't a result.

### 3. Run the same analysis on a different rule

Before believing any "law" that emerges, run the identical analysis on a deliberately different rule.

- **If the law survives the change of rule,** it belongs to the setup — the grid, the box, the threshold, the analysis — not to the idea.
- **The interesting result** is the one a generic rule would *not* give.

### 4. Know what's generic

These show up in almost any model, so finding them means nothing: diffusion; exponential decay; damped oscillation; symmetry echoes (a square box gives four-fold patterns); area laws.

### 5. Settings are not laws — but a knob is not a sin

If a pattern depends on a number you chose in the code — a threshold, a weight of 1.0, a target of 0.5 — the pattern belongs to that choice. Names for the parts your simulation needs are software components, not physics.

**That is not an argument for zero free parameters.** Physics is full of knobs: the Standard Model, inflation, ΛCDM, general relativity's constants. Nobody demands a theory have none. What matters is whether a knob is doing work.

**A good parameter** corresponds to something meaningful, changes behaviour predictably, could in principle be measured, and ties several observations together.

**A bad parameter** was moved from 0.37 to 0.42 because the graph looked wrong.

**And the distinction worth protecting is which knobs are ontology and which are engineering.** An ontology names what is fundamental. The operational rules that generate familiar structure from it — neighbour selection, thresholds, stability criteria, transport laws — are a separate layer, and adding them is not a betrayal of the ontology. *Matter curves spacetime* is an ontological claim; the field equations are an operational model, and they arrived a decade apart.

Keep the two layers labelled. That, rather than a parameter count, is what stops a model from quietly becoming a fit.

### 6. Three kinds of "accurate"

Only the third is evidence about the world.

1. **The code matches its own equation.** Verification. It proves no bugs, not physics.
2. **A toy world shows regularities.** Facts about the toy.
3. **The model matches real data it wasn't tuned to.** Evidence.

### 7. Freeze predictions before the data

- **Write the number, the parameters and the rules down first.** State the pass/fail criteria in advance.
- **Apply them to data you haven't looked at.**
- **Don't adjust the formula after a miss and call the new version confirmed.** When every outcome can be explained, no outcome is evidence.

### 8. Count the free parameters

A flexible curve fitted separately to each dataset will fit anything of the right shape.

- **Compare against existing theories,** not against nothing.
- **Ask what a boring alternative would score.**

### 9. Make sure the test exercises the mechanism

Check that the experiment actually creates the condition your prediction needs.

### 10. Restating is not deriving

- **Known physics in new vocabulary is a restatement.** Call it "consistent with", not "derived".
- **A measured constant on your input list can't be a prediction.** Using G, ħ or a₀ as inputs means you didn't predict them.
- **Matching a known answer isn't deriving it.** Choosing the formulation in which your model matches the known answer is matching.

### 11. One setup, start to finish

Don't switch coordinates, parametrizations or definitions partway through an argument. If two documents use the same quantity, they must use it the same way.

### 12. Name every assumption

List all of them, including the modelling choices that turn words into equations. Never claim a result follows from fewer assumptions than it does.

### 13. Check by calculation against established physics

- **Agreement with your own earlier work is not evidence.**
- **A claim that gives a definite number gets computed** and compared with what is already known.
- **Any contradiction that survives the calculation gets recorded,** not explained away.

### 14. AI is a calculator and an adversary, not a co-author

- **Ask it to break the idea and to run the numbers, not to write the paper.**
- **Two AIs agreeing tells you nothing.** The moment something gets computed, you learn something.
- **Keep audit tables and tier labels honest.** Their form can look like rigour without being rigour.

---

## Part two: how they were applied

The rules above are the standing ones. These are the practices the testing actually ran under, and the ones worth carrying to anything that comes next.

**Meanings fixed before models.** What a term means is settled in writing before anything is built on it, and the person whose idea it is decides — not the person writing the code. A default proposed and not objected to is not a decision.

**Expected results written before the run.** Every test states what each outcome would mean *before* it produces one, including which outcome would end the line of work.

**Instruments calibrated on known answers.** A measurement is not used on an unknown until it reproduces the right answer on objects whose answer is already known. Two instruments failed that check and were replaced rather than used.

**Build the test that can destroy the result.** Where a finding is attractive, the next test is the one designed to remove it. Five results were withdrawn this way.

**Closed records.** Once concluded, a piece of work is referenced and never edited. Corrections go in new documents that say what they correct.

**Tuned settings labelled.** Any number chosen to make something work is marked as chosen, with who chose it.

**The census guard.** A result counts as a reduction only if the input list gets *shorter*, with no new free parameters. Constraining somebody else's free parameters is a different kind of claim, and is labelled as one.

**An exit rule agreed in advance.** "If three honest attempts fail, stop and write it up." Agreed before the attempts, and applied.

---

*These rules are the reason the results in this repository come with their scope attached. A framework that cannot be wrong about anything is not saying anything.*
