# Can option A or option D be tested? How to decide

*2026-09-13. Ledger: RD25, C98–C101, T11. Follows [G34_Unpacked.md](G34_Unpacked.md).*

## The two options, in one line each

- **(A)** A lone pattern that spreads past a limit draws by itself, even with nothing to interact with.
- **(D)** A lone pattern stays spread until it interacts. Nothing draws by itself.

Both keep the picture Allen agreed to (RD25): **outcomes are whole units; patterns spread smoothly in fractions.**

---

## What each one predicts

- **(D) predicts exactly what standard quantum physics predicts for lone particles.** There is nothing extra to see.
- **(A) predicts one extra thing:** interference would vanish once a lone pattern is spread far enough, with no outside cause to blame.

**A note on which experiments count.** Many collapse-model tests look for tiny random kicks in ordinary compact matter: extra heating of ultra-cold cantilevers (C100), or faint X-rays from germanium (C43). Those test GRW-style collapses that happen at a steady rate. **ED's option A is different:** it only triggers when a pattern is spread thin, so compact matter would feel nothing, and those tests don't directly bound it. The tests that matter for A are **how far a lone pattern can spread and still interfere.**

## What experiments show so far

| what was spread | how far | still interfered? | ledger |
|---|---|---|---|
| Caesium atoms | Two halves 54 cm apart, about 1 second | Yes | C65 |
| Molecules of 2,000 atoms (over 25,000 Da) | Through a 2 m interferometer | Yes | C98 |
| Single photons | Time-bin patterns carried over 421 km of fibre | Yes | C92 |

None shows an unexplained loss of interference.

## Why A and D can't be told apart directly, and how to decide anyway

**1. Experiments can only ever *find* A, never prove D.** If A is true, some experiment will one day see interference vanish with nothing to blame. If D is true, every experiment just keeps working. Each longer or larger experiment pushes A's limit further out.

**2. Counted in loci, A's limit has to be absurdly small.**
- A pattern spread over 54 cm covers (0.54 m ÷ step size)³ loci.
- If the steps are anywhere near as small as physicists expect for the grain of space, that is an astronomically large number of loci. So b_min would have to be astronomically small.
- Draws from thinness would then never happen in any experiment anyone could build.
- **In practice A would behave exactly like D, while carrying a number that does nothing.**

**3. A only matters if steps are coarse, and coarse steps would show up elsewhere.**
- **One test:** photons of very different energies from a distant gamma-ray burst arrived together (Fermi telescope, GRB 090510). That rules out one kind of graininess, where speed depends on energy, down to about the Planck length (C99).
- **What it doesn't rule out:** other kinds of graininess. So it's a strong hint against coarse steps, not a proof.

**4. Quantum computers make the same point from another direction** (C101). A 53-qubit processor held a pattern spread over 2⁵³ possibilities, about ten thousand million million, and only drew an outcome when measured. That is Allen's oracle picture in working hardware.

## Proposed decision rule (to freeze before deciding)

> **Choose (D)** by least structure, **unless** ED gives an independent reason for steps coarse enough that a thinness limit could show up in a feasible experiment.
> **Revisit** if any experiment ever shows an unexplained loss of interference for a well-isolated lone pattern (test T11).

**What choosing D costs.** For lone particles, ED says nothing standard quantum physics doesn't. ED's own testable content then has to come from what isn't standard:
- the commitment budget and gravity;
- clock ticks;
- strong gravity;
- locus birth (RD21).

**What it gains.** One fewer free number, and nothing that experiments already squeeze.

---

## Allen's points this round

### "A smallest unit on a scaleless graph seemed wrong"
**The two fit together.** Scaleless (RD15) means there is no built-in *size* in metres. A smallest unit of *amount* is a *count*: one whole electron, one whole photon. Counts are exactly what a scaleless graph allows. And "outcomes are whole units" is about what a draw produces, so nothing has to wait for loci to be laid down, beyond there being loci for the draw to land on.

### The oracle picture
**Allen:** in quantum computing, the oracle just reads the pattern; the answer is in the pattern, so the pattern has to divide into fractions.

**That is how quantum algorithms work.**
- **The pattern holds fractions and phases** across all the possible answers at once.
- **The oracle marks the right answer by flipping its phase.**
- **An interference step concentrates the pattern onto the marked answer.**
- **A measurement then draws one whole outcome.**

**Two connections to the rule:**
- **It needs phases to be kept** between steps, which is exactly RD11 (drawn content keeps its phase).
- **The coin used in version 0 is that interference step.** The Grover coin is the same "inversion about the average" as Grover's search algorithm, applied to the three lanes at a locus.

So the oracle picture supports "patterns spread in fractions, outcomes whole", and it is already built into version 0.

## Decided (2026-09-13, RD26)

**Allen accepted the decision rule and chose (D), with no coarse steps.**

**What "coarse" meant.** Everything in ED is discrete, and that isn't in question. Discrete means space comes in steps. *Coarse* means those steps are big enough to show up in experiments. Steps can be discrete and still far too small to notice, the way a photograph is made of pixels that are invisible at normal viewing distance. "No coarse steps" means the pixels of space are too fine for any lab to see.

**Consequences:**
- **RD19 (draw when too thin) and b_min are retired.** Lone patterns draw only when they interact.
- **The commitment rule now has no free numbers of its own,** apart from unit conversions (C102).
- **What counts as an interaction is now the rule's main open piece (G35).**
- **Version 0's code still uses the retired thinness trigger.** Version 1 replaces it.
