# The standing phase: can ED fix it?

*Started 2026-09-14 under G54 = (a), RD52. Exit rule (proposed, to confirm): three frozen attempts, then write ED up as an interpretation. Attempts used: **1 of 3**. Ledger: C290, C295–C298, G55.*

## What we're looking for

**The target.** The tuned hand (C288, C293) needed a small-loop phase that is **neither 0 nor π**. Only then is time-reversal symmetry broken, so that draws that carry motion off can tilt the flow. Up to now we set that phase by hand. The goal is for ED to fix it from its own primitives.

**The small loop:** hop right in the Right lane, switch lanes, hop back in the Left lane, switch back. In ED's real rule it sits at exactly π.

## Literature first (C295)

- **Feynman's checkerboard and the Dirac quantum walks.** Mass enters as a quarter-turn phase at each change of direction. That puts the lane loop at π: time-reversal symmetric, so no hand. **A phase "from mass or proper time" is already settled in the literature: it gives no hand.**
- **Quantum walks are classified by their symmetries,** including time reversal (Cedzich et al.). So the phase has to break time reversal to matter.
- **Frustrated phase models,** such as the triangular XY antiferromagnet (Miyashita and Shiba), can't satisfy every loop. Their ground states pick a chirality by chance (+120° or −120°). That's a known way for in-between phases to be forced rather than chosen.

## Attempt 1: P12's coherence, as read (Wilson's form) — failed (C296)

**What we did.** On ED's lane graph (every channel at a locus mixes with every other; lanes hop), we let every hop and mixing phase vary. Then we minimized "phases should close to 0 around every small loop".

**Result.** Every small-loop phase is fixed at 0, in 1D and in 3D. That is time-reversal symmetric, so **no hand**. It confirms the tension noted for your sidebar (C290).

**Score:** 4 of 5 frozen predictions right. The 3D miss was my criterion: some starts got stuck in local minima. Those minima were also all 0 or π.

## The lead found along the way (C297)

**The variant.** "Phases should close to π", which is where ED's real lane loops already sit.
- **In 1D** it's satisfiable: all loops at π, still no hand.
- **In 3D** it's **frustrated.** With 7 channels all mixing at each locus, the loops can't all reach π.

**What the frustrated best state does.**
- **Every small triangle of mixings** at a locus carries a phase of ±1.21 or ±2.66 radians. That includes the one the 1D rule uses (Internal, +x, −x): −1.21.
- **Those phases flip under a mirror and under time reversal,** so the ground state picks a chirality by chance, like the triangular XY antiferromagnet.
- **The lane loops stay at π.**

**What we don't know yet.** Whether that chosen chirality makes ED's rule hold a lasting flow with winding. It might do so even without flow feedback, because the mirror is already broken by the chosen phases.

**What it depends on.**
- **The reading:** "close to π" isn't RD33's reading.
- **The coin:** every channel mixing with every other (the Grover coin, a convenient default). A coin that mixes fewer channels may not be frustrated.

## Attempt 2: the frustration route — failed (C299, C300)

**What we did (G55 = a, RD53).**
- **The phase:** gave ED's 1D rule the frustrated mixing phase, a triangle phase of ±1.209.
- **Everything else as before:** draws carry motion into committed matter. No lane-loop phase and no flow feedback were set by hand.

**Result: no lasting flow.**
- **With no feedback,** every flow ended below 5 × 10⁻⁵, with random signs, for both chirality signs. The winding was 0.
- **The reason:** a diagnostic found the rule has several steady states with this phase (4 or 13), and **every one of them carries zero flow**. That also broke the exact solve, so the frozen steady-state predictions were ill-posed (recorded).
- **With the tuned feedback added,** flows only reached about 5 × 10⁻⁵ and never locked in. Compare that with 0.11 when the lane-loop phase is set.

**Score:** 2 of 5 predictions came out "right", but one right verdict came from the ill-posed solve and the other was vacuous. So in substance attempt 2 failed.

**What it tells us.**
- **The ingredient the hand needs is a phase on the lane loop itself** (hop, switch, hop back, switch), neither 0 nor π.
- **A chirality in the mixings doesn't substitute for it.**
- **Both readings of coherence so far leave the lane loops at 0 or π.**

**Attempts used: 2 of 3.**

## Attempt 3: longer loops — failed (C302)

**What we did (G56 = a, RD54).** Coherence scored four kinds of loop:
- the on-site loops;
- the lane loops;
- **the smallest square loops in space:** 48 per locus, using lane hops in two directions with lane switches at the corners.

Square loops share hop phases with the lane loops, so they might have forced the lane loops off 0 and π. We tried squares weighted ¼, 1 and 4 times.

**Result.**
- **Wilson reading (prefer 0):** every loop at 0. Time-reversal symmetric, so no hand.
- **"Close at π" reading:** the squares are frustrated too (most loops end at neither 0 nor π), **but the lane loops stay at exactly ±π** at every weight. No lane-loop phase is forced, so the dynamic test never ran.

**Score:** 2 of 3 predictions right; the one that mattered (T3) was wrong.

## The exit rule is reached (C303)

**Three frozen attempts, three failures.** Across them, no reading of P12's coherence we tried forces a lane-loop phase other than 0 or π. So ED doesn't yet fix the one ingredient its hand needs.

**What the line did establish:**
- **Coherence as read** (Wilson) always gives time-reversal-symmetric phases. Your sidebar's catch (C290) is confirmed.
- **A "close at π" coherence is frustrated in 3D** and picks a chirality by chance, but only in the mixings and the squares, never in the lane loops (C297, C302).
- **A mixing chirality doesn't hold a flow;** the hand needs the lane-loop phase (C300).
- **A mass or proper-time phase** puts lane loops at π (C295).

## Decision: G57

| | option | notes |
|---|---|---|
| **(a)** | **Apply the exit rule:** write ED up as what it honestly is. That means an interpretation with a runnable rule, the handedness theorem, the rebuilt draw, and the negative results. Then Allen decides on the review packet | **Proposal.** It's what the rule was for |
| **(b)** | Keep going past the exit rule by another route (budget gradients, births) | Not recommended: no lead, and it would weaken the discipline that keeps ED credible |
| **(c)** | Pause ED | Loses nothing, but leaves the write-up undone |

## Decision: G56 (done: (a), attempt 3 run)

| | option | notes |
|---|---|---|
| **(a)** | **Attempt 3: longer loops.** Let coherence also score larger loops that use lane hops in different directions (spatial squares in 3D), so lane loops might be frustrated and forced off 0 and π | The only structural lead left. Weaker than attempt 2's was |
| **(b)** | **Stop now** and write ED up as an interpretation (theorem, negative results, the rebuilt draw), and send the review packet | Honest; two serious attempts failed |
| **(c)** | Attempt 3 by another route (budget gradients, births) | No concrete lead |

**Proposal: (a) as the last attempt, frozen.** If it fails, (b). The exit rule also still needs Allen's confirmation.

## Decision: G55 (done: (a), attempt 2 run)

| | option | notes |
|---|---|---|
| **(a)** | **Attempt 2: the frustration route.** Put the frustrated mixing phases into ED's rule, with draws that carry motion off, and test with frozen predictions for a lasting flow and winding, with the hand set by the chosen chirality | Needs Allen to decide whether "coherence prefers loops closing at π" is an acceptable reading of Coh. He wrote P12 |
| **(b)** | Attempt 2 by another route (budget, births) | No concrete lead yet |
| **(c)** | Stop here and write ED up | Early; one attempt used |

**Proposal: (a),** if the π reading is acceptable to Allen.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C295 | Jacobson and Schulman, "Quantum stochastics: the passage from a relativistic to a non-relativistic path integral", *J. Phys. A* 17, 375 (1984); Feynman checkerboard notes (arXiv:1012.1564) | Search listings |
| C295 | Meyer (1996); Bialynicki-Birula (1994); Dirac cellular automata on a trapped-ion computer, *Nat. Commun.* (2020) | Search listings |
| C295 | Cedzich, Geib, Grünbaum, Stahl, Velázquez, A. H. Werner, R. F. Werner, *Ann. Henri Poincaré* 19, 325 (2018), arXiv:1611.04439 | Search listing |
| C295 | Miyashita and Shiba (1984), triangular antiferromagnetic XY model; chiral-mode domains observed in optical triangular lattices, *Phys. Rev. Research* (2023) | Search listings |
