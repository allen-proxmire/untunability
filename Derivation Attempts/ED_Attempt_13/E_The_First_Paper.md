# What the first paper says, and what our models have never contained

*ED_Attempt_13, note 3. 2026-09-23 (RD3). Ledger: C3. Reasoning only; nothing computed. Read from Allen's *Event Density and the Architecture of the Universe* (January 2026), the whole paper. This note revises note 2 before any of it is run. Written plainly.*

## First, a correction of mine

Earlier today I checked ED's inflation language against the old repo and told Allen his recall had the terms swapped. **His recall was right, and it's this paper:**

> **"It is the moment when ED diffusion outpaced ED production."** — §13, Inflation as ED Smoothing

His words were *"production of events outpaced production of space"*. Same two quantities, same relation, recalled from the right source. The phrasing I found in the old repo (*"complexity outpacing event-production capacity"*) is a different passage about the quantum–classical boundary. **I corrected him against the wrong document.**

## The thing that matters most, and it is a gap in every model we've built

The paper's §4 says what space is:

> **"Space is the pattern of stable relations formed by persistent ED gradients."**
> **"Distances correspond to differences in ED; directions correspond to pathways along which ED remains coherent; regions correspond to clusters of stable ED relations."**

**Every model in this project has had no ED gradients in it at all.**

In every run from road N onwards, each event's rate is drawn independently from a bell curve — that is **noise, not a gradient**. And in the generation models the rates are **redrawn every generation**, so nothing about the rates can persist even by accident. The paper says space is made of gradients that are **persistent** and **stable**. We have been building patterns whose rates are fresh noise at every tick.

**This is the same class of miss as the two before it:** the audit found ED's clocks were missing; D5 found a shared now had been built in; this finds the rates have no structure and no memory. All three were mine, and all three were invisible from inside the numbers.

## What follows for attempt 6's floor — and it is not small

Attempt 6's argument, which attempt 11 measured and which road P and road E both rest on, runs: *a patch of n clocks has a rate surplus growing like √n, its edge grows like n^((d−1)/d), so matching needs d > 2.*

**The √n is exactly the arithmetic of independent random rates.** It is the random-walk sum of n independent draws. With a **gradient** — rates that vary smoothly and coherently across the pattern — a patch's surplus is not a random walk at all. A region that is systematically faster than its surroundings has a surplus growing like **n**, not √n.

So the floor argument as measured may be an argument about noise, not about ED.

## And the paper says what happens to a surplus instead

Our models treat a patch's surplus as something that must be **carried away through the edge**, or the pattern isn't allowed. The paper says something different:

> **"The natural flow of becoming is from concentrated ED toward diffuse ED."** — §26
> Gradients flatten. That flattening **is** the arrow of time.

**In the paper, a surplus is not a problem to be held. It is the engine.** It drives diffusion, and the diffusion is what time is. Nothing in our models diffuses — rates never move, never spread, never flatten, because they are replaced each generation.

## One more thing, and it reframes twelve attempts

The paper is explicit about what ED does and does not claim:

> **"ED does not predict every structure in the universe. It explains why structure is possible."** — §32
> **"ED does not specify: the exact distribution of ED at any moment; the particular gradients that form galaxies or stars…"** — §34
> **"ED provides the conditions of possibility, not the full catalogue of outcomes."**
> **"It is a theory of why anything can have a structure at all."**

**The founding paper does not claim to derive three dimensions.** Twelve attempts have been trying to get something out of ED that ED's own first statement does not promise. That does not make ED right, and it does not make the failures less real — but it means the target may have been set by us rather than by the theory.

It also puts the project's one solid result in a different light. *ED's budgets fix the three numbers CDT tunes* (A11 C5) is exactly a "conditions of possibility" claim: not a prediction of a structure, but a constraint on what structures are available. **That is the kind of claim this paper says ED makes.**

## Two other correspondences worth recording, carefully

- **§6, ED thresholds:** *"Every structure exists only when the local rate of becoming exceeds the threshold needed to sustain it."* We found a threshold this attempt — **below about 5 relations per event, patterns fall apart** (A12 C7). Same shape of statement. Whether it is the same threshold is not established, and I am not claiming it is.
- **§29 and Penrose's cyclic cosmology:** the paper's end state is *ontological flatness* — no gradients, no stable relations, nothing to distinguish anything. **Our end state is the opposite in one respect and similar in another:** ours is sparse and featureless too, but it is reached by *adding* relations, not by gradients flattening. That may be a coincidence of shape, and I'd want it tested rather than told as a story.

## What this does to road E

**Note 2's road E — describe the end state — is premature as written.** The object it would describe is produced by a model with no gradients, no persistence in the rates, and no diffusion. Describing it carefully would be describing an artefact of noise.

**What road E should be instead:** put the missing piece in, then ask what the object is. That needs two meanings from Allen, and they are his to give:

| | question | what hangs on it | a default I'd propose |
|---|---|---|---|
| **E-Q1** | **Do rates pass on?** When an event passes on to its children, is the child's rate related to the parent's, or freshly drawn? | Everything. Without inheritance no gradient can persist, and the paper says space is *persistent* gradients | **Yes — a child's rate is its parent's, plus a small variation.** That is the least-structure way to let a gradient exist at all |
| **E-Q2** | **Do rates diffuse?** The paper says becoming flows from high ED to low ED and gradients flatten, and calls that the arrow of time | Whether the model has ED's own dynamic in it, or only its bookkeeping | **Yes — each tick, an event's rate moves a little toward its neighbours' rates.** The rate at which it moves is a number, and it would be mine unless ED supplies one |

**And a warning I want on the record before we build it:** with rates that diffuse, a pattern will tend to flatten toward uniform rates, and a uniform pattern trivially satisfies every sync condition. **A model that flattens its own gradients will "succeed" at sync while containing nothing.** Whatever gets built has to be able to show that — the paper's own §16 and §29 say exactly that this is where a universe ends up.

## Options

| | option |
|---|---|
| **(a)** | **Answer E-Q1 and E-Q2**, then rewrite road E's model with gradients that persist and diffuse, expectations fixed before any code |
| **(b)** | Describe the end state as it stands first (note 2 as written), then add gradients afterwards, so there's a before-and-after |
| **(c)** | Go back to attempt 6's floor and redo it with gradient rates rather than noise, since that argument underpins everything since |

**Proposed: (a), with (c) folded in** — the floor is cheap to recompute on gradient rates, and if it moves, a lot of what we've measured has to be read differently.
