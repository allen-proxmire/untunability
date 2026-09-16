# Gravity's area law, from ED's ideas

**In short:** in 1995, Ted Jacobson showed that Einstein's equations of gravity follow from one physical assumption about horizons, plus standard physics. ED's own ideas supply that assumption.

**It's a reading, and conditional:**
- it rests on ED's pattern of connections being smooth and three-dimensional at large scales, which ED assumes rather than builds;
- the numbers, including the strength of gravity, are still taken from physics as measured;
- close versions of the idea already exist.

**Treat it as a reason from ED's ideas, not a new derivation.**

## Jacobson's argument

Jacobson asked what happens at a **horizon**: a boundary beyond which something can't be seen or reached, like the edge of what a steadily accelerating observer can ever receive.

**He used three ingredients:**
1. **Entropy** (roughly, missing information) belonging to a horizon **grows in proportion to its area.** This is the one physical assumption.
2. **A horizon has a temperature,** the one an accelerating observer sees (Unruh's temperature).
3. **Energy crossing a horizon changes its entropy** in the way ordinary thermodynamics says heat changes entropy.

**Asking that this hold for every small horizon, everywhere, forces Einstein's equations.** Gravity comes out as a kind of thermodynamics of spacetime.

**Ingredients 2 and 3 are standard physics.** Ingredient 1, entropy growing like area, is the input nobody derives from something deeper. That's the one ED addresses.

## What ED says

**1. What "can't be brought back" means.** In ED, something becomes final when it's out of reach of every possible future path. That boundary is a horizon.

**2. Entropy is the count of connections crossing it.** ED's world is a web of connections, and the present is all there is. So the information missing from one side of a horizon is the connections that belong to the present but reach across the boundary. Count them, and that's the entropy.

**3. That count grows like area,** as long as connections are:
- **finite and short-range** (no connection reaches far away);
- **pointing every way equally, on average.**

Picture a surface cutting through a tangle of short threads: double the area, and you cut twice as many threads.

**Put 1–3 together and ED supplies ingredient 1:** a horizon's entropy is the number of ED connections crossing it, and that number is proportional to its area.

## The checks

These are numerical checks with expected results written down before they ran:

| check | expected | result |
|---|---|---|
| **Random short segments** crossing a plane | the textbook rate | **1.011** × that rate |
| **A random short-range web** crossing a sphere | the formula for area scaling | **1.007** × the formula; crossings grew with radius as **R^2.12**, close to area's R² |
| **A regular cubic grid** | depends on direction | **1.00, 1.41 and 1.73** for surfaces facing along an edge, a face diagonal and a body diagonal |

**The grid result matters.** On a regular grid, a diagonal-facing horizon would get up to 73% more entropy than an edge-facing one, and Jacobson's derivation would give different gravity in different directions. **So ED's connections must point every way equally:** a random web, not a grid.

**One pre-set expectation was missed.** For connections that reach far, crossings grew as R^3.20 at one sampling point, against a pre-set range of 2.8–3.1. A follow-up that wasn't planned in advance traced it to sampling a single ball at small radius. Averaged over 40 centres, the exponent was 2.99. The miss stays on record as a miss.

## What this does and doesn't show

**Supplied by ED's ideas:** that horizon entropy is proportional to area. ED's version adds no new free numbers.

**Still taken from physics:**
- **The strength of gravity (G).** In ED it gets a meaning, how densely connections cross a surface, but its value is taken from measurement.
- **Unruh's temperature.** A rigorous theorem ties it to space looking the same to every steadily moving observer. ED's web has a preferred rest frame, so ED can only *assume* that symmetry holds well enough at large scales.
- **The thermodynamics** of ingredient 3, and the local structure of spacetime.

**So Einstein's equations as a whole are consistent with ED, not derived by it.**

**The key condition:** everything above assumes ED's web is smooth, three-dimensional and direction-free at horizon scales. **That's assumed, not built.**
- **ED's attempt 6** tried to grow such a web from ED's rules, and didn't find a way.
- **Its models grew space without using time's one-way order,** and got loops, rough tangles or "small worlds" instead of three dimensions.
- **Attempt 7 is now testing growth that uses time order,** where space isn't allowed to split. That's the ingredient the literature says makes geometry smooth.

**Close to known work:**
- **Counting causal links crossing a horizon** gives area-proportional entropy in causal set theory (Dou and Sorkin).
- **Entanglement across a surface** gives an area law in quantum field theory (Bombelli, Koul, Lee, Sorkin; Srednicki).

**ED's contribution is interpretive:** its own ideas about finality and the present pick out that count as *the* entropy. The mechanism itself isn't new.

## References

- T. Jacobson, "Thermodynamics of spacetime: the Einstein equation of state," *Physical Review Letters* 75, 1260 (1995), [gr-qc/9504004](https://arxiv.org/abs/gr-qc/9504004).
- T. Jacobson, "Entanglement equilibrium and the Einstein equation," *Physical Review Letters* 116, 201101 (2016), [arXiv:1505.04753](https://arxiv.org/abs/1505.04753).
- W. G. Unruh, "Notes on black-hole evaporation," *Physical Review D* 14, 870 (1976).
- D. Dou and R. D. Sorkin, "Black hole entropy as causal links," *Foundations of Physics* 33, 279 (2003), [gr-qc/0302009](https://arxiv.org/abs/gr-qc/0302009).
- L. Bombelli, R. K. Koul, J. Lee and R. D. Sorkin, "Quantum source of entropy for black holes," *Physical Review D* 34, 373 (1986).
- M. Srednicki, "Entropy and area," *Physical Review Letters* 71, 666 (1993), [hep-th/9303048](https://arxiv.org/abs/hep-th/9303048).
- L. Bombelli, J. Henson and R. D. Sorkin, "Discreteness without symmetry breaking: a theorem," *Modern Physics Letters A* 24, 2579 (2009), [gr-qc/0605006](https://arxiv.org/abs/gr-qc/0605006).
