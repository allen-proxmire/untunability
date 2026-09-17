# New Rules

Working rules for whatever comes next. Each one is here because breaking it cost real time.

---

## 1. Write the rule before the story

The first thing you write is a rule a computer can run. Interpretation comes after.

A template for starting from nothing:

- **State:** a graph or grid, perfectly uniform.
- **The first difference:** one site differs.
- **The rule:** how a difference spreads, and the fact that it cannot un-spread (the arrow).
- **The run:** watch what grows.

If a statement can't be turned into code or a formula, it is not yet a starting point. It is a hope about one.

## 2. Test every result with three questions

"Assume x, y, z, get A" is legitimate physics (Jacobson got Einstein's equations that way) when all three answers are yes:

1. **Are the assumptions precise?** They should be definite enough to calculate with, not words.
2. **Does a real calculation connect the assumptions to A?** A must not be the assumptions restated.
3. **Could A have come out wrong?** If no possible outcome would count against it, it isn't a result.

## 3. Run the same analysis on a different rule

Before believing any "law" that emerges, run the identical analysis on a deliberately different rule.

- **If the law survives the change of rule,** it belongs to the setup (the grid, the box, the threshold, the analysis), not to the idea.
- **The interesting result** is the one a generic rule would *not* give.

## 4. Know what's generic

These show up in almost any model, so finding them means nothing:

- **Diffusion:** things spreading out and smoothing.
- **Exponential decay:** anything relaxing toward equilibrium (RC circuits, cooling, drug clearance).
- **Damped oscillation:** any two quantities pushing on each other near equilibrium (RLC circuits, springs, predator–prey cycles).
- **Symmetry echoes:** a square box gives four-fold patterns, and straight lines on a torus give rational-slope classes.
- **Area laws:** the edges cut by any region's boundary scale with its surface.

## 5. Settings are not laws

If a pattern depends on a number you chose in the code (a threshold, a weight of 1.0, a target of 0.5), the pattern belongs to that choice. Names for the parts your simulation needs are software components, not physics.

## 6. Three kinds of "accurate"

Only the third is evidence about the world.

1. **The code matches its own equation.** This is verification. It proves no bugs, not physics.
2. **A toy world shows regularities.** These are facts about the toy.
3. **The model matches real data it wasn't tuned to.** This is evidence.

## 7. Freeze predictions before the data

- **Write the number, the parameters and the rules down first.** State the PASS/FAIL criteria in advance.
- **Apply them to data you haven't looked at.**
- **Don't adjust the formula after a miss and call the new version confirmed.** When every outcome can be explained, no outcome is evidence.

## 8. Count the free parameters

A flexible curve fitted separately to each dataset will fit anything of the right shape. High R² with three free parameters per material is weak.

- **Compare against existing theories,** not against nothing.
- **Ask what a boring alternative would score.**

## 9. Make sure the test exercises the mechanism

Check that the experiment actually creates the condition your prediction needs. (Photobleaching doesn't make a concentration gradient, so a FRAP test can't test a mechanism that needs one.)

## 10. Restating is not deriving

- **Known physics in new vocabulary is a restatement, however it's tiered.** Call it "consistent with", not "derived".
- **A measured constant on your input list can't be a prediction.** Using G, ħ or a₀ as inputs means you didn't predict them.
- **Matching a known answer isn't deriving it.** Choosing the formulation in which your model matches the known answer is matching.

## 11. One setup, start to finish

Don't switch coordinates, parametrizations or definitions partway through an argument. If two papers use the same quantity, they must use it the same way.

## 12. Name every assumption

List all of them, including the modelling choices that turn words into equations. Never claim a result follows from fewer assumptions than it does.

## 13. Check by calculation against established physics

- **Agreement with your own earlier work is not evidence.**
- **A claim that gives a definite number gets computed** and compared with what is already known.
- **Any contradiction that survives the calculation gets recorded,** not explained away.

## 14. AI is a calculator and an adversary, not a co-author

- **Ask it to break the idea and to run the numbers, not to write the paper.**
- **Two AIs agreeing tells you nothing.** The moment something gets computed, you learn something.
- **Keep audit tables and tier labels honest.** Their form can look like rigor without being rigor.

## 15. Get a human physicist early

Show them the rule while it is one page long.

## 16. One result at a time

- **Start small.** A small true result beats a large unsupported framework.
- **Make it modest and correct**, then stop.
- **Use this structure:** a result, its assumptions, a check anyone can run, and an honest statement of how far it reaches. The Event Density Streamlined repository is the template.
