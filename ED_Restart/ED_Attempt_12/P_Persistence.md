# Road P: persistence — on paper

*ED_Attempt_12, note 2. 2026-09-23 (RD2). Ledger: C2. On paper; nothing computed. Written plainly.*

## The picture

**Space, in ED, is a pattern of events and the relations between them.** Nothing in ED says what shape that pattern has. What ED says is that **relations stick** once committed, that **clocks have to be able to hold together**, and that a **budget** rules how many events and relations there are.

Two attempts, by completely different routes, found the same thing: **whatever shape a pattern has, it keeps.** Attempt 12 asks whether that is a **result** or just a **restatement of the rules**.

## The trap, named first

**If relations can never break, of course the shape doesn't change.** Nothing can be undone, so nothing can be lost. Written that way, "ED keeps a shape" is nearly a tautology and worth nothing.

**So the road has to sharpen it into something that could fail.** Three ways it could:

| | the sharpened question | could it fail? |
|---|---|---|
| **P1** | **Does ED destroy what can't hold its clocks together?** A line and a flat sheet provably can't, at large size (A11 C21). So under ED's own rules, a pattern that starts as a line should not be able to *stay* a line as it grows | **Yes.** Attempt 11's probe started from a ring and it stayed a ring — but that probe had no sync filter running. With the filter in, it must either change or fail |
| **P2** | **Does a shape stay sync-able as it grows?** Keeping a shape is worth nothing if the clocks stop holding together once the pattern is large | **Yes.** The pull needed could start rising with size, which is exactly what failure looks like |
| **P3** | **Does persistence beat sheer number?** Crammed shapes outnumber spread-out ones enormously. Attempt 10 found counting never moved a history anyway | **Yes** — but it's expensive to test, and A10 already probed it. Carried, not opened |

## The reframe this road is really about

**ED may not be a generator of space. It may be a filter on it.**

- ED does **not** make three dimensions. Attempt 11 settled that: sync rules out one and two, and then "fewest relations" picks a small world, not a lattice.
- But ED **does** forbid something, and the forbidding is its own: **a pattern that cannot hold its clocks together cannot persist.** Below three dimensions, that's every pattern. Attempt 6 argued it; attempt 11 measured it.

**So the honest claim on the table is:** *whatever survives in ED is at least three-dimensional-capable — and ED cannot narrow it further than that.* One and two are ruled out. Three and small worlds both survive, and nothing in ED chooses between them.

**Under the census guard:** this is **a constraint ED derives, not a reduction in ED's inputs.** The input list doesn't get shorter. It should be written up as a restriction on what can exist, and never as a derivation of space.

## The first test, and what each outcome means

**What would be built:** the one configuration road N never ran — **all of ED's own parts at once**. Events that pass on and are then spent; whole generations arriving together, children of neighbouring parents linked; and **the sync filter running throughout**, adding relations only while the clocks fail to hold. Started from four different shapes: a line, a flat grid, a 3D grid, and a small-world web.

**What would be read:** what each one turns into as it grows — its dimension reading, whether the clocks still hold, and how many relations it needed.

| outcome | what it would mean |
|---|---|
| **The line and the flat grid are destroyed** (forced up, or they fail to hold) **while the 3D grid survives as itself** | **The filter bites.** ED forbids sub-three-dimensional space from persisting, using nothing but its own content. That is road P's positive result |
| **Everything is forced into a small world**, including the 3D grid | The filter bites but overshoots: ED destroys *everything* that isn't a small world, including the shape we want. A clean negative, and it would close the whole line of attack |
| **Everything keeps its shape, line included** | **Persistence is a restatement.** The rules simply don't allow change, and "ED keeps a shape" says nothing about the world. Road P closes |
| **The 3D grid stops holding together as it grows** | Worse than any of the above: ED can't even keep the shape we'd want it to keep |

## What ED has to say before this can be built — your calls

| | question | what hangs on it | a default I'd propose |
|---|---|---|---|
| **P-Q1** | **What does "keeps its shape" mean?** ED has no coordinates, so it can't mean the same pattern event-for-event | **The readings stay put** — the dimension reading holds within ±0.3 over a four-fold growth in size. Fixed before running |
| **P-Q2** | **What happens to a pattern whose clocks can't hold together?** This is the one the whole road rests on | **It isn't allowed** — it doesn't count as a history, which is attempt 6's own reading of Synced Now. The alternatives: it breaks into pieces that each hold, or nothing happens and rates simply never agree |
| **P-Q3** | **Who may pass on, and when is an event spent?** Attempt 11's probe showed this decides the shape on its own | **An event passes on once and is then spent** — my reading of A9 D3, *commitment is passed on, not held*. This is the one I'd most like you to rule on yourself |
| **P-Q4** | **Is space the frontier or the whole accumulated pattern?** | **The frontier** — the current generation is "space now", which matches your own picture of the lit-up committed part. The accumulated pattern reported alongside it |
| **P-Q5** | **Can a relation ever break?** | **No** — D12 stands. But the consequence should be stated: a pattern can never be pushed apart, so the only way a shape can change is by new events arriving |
| **P-Q6** | **Does the budget bind here?** ED's link budget is 6.7 per event; these patterns hold on 3.8 | **Report it, don't enforce it.** It's borrowed from flat geometry (C16) and enforcing it would be putting the answer in by hand |

## Expected results, to be fixed before any code

| | expectation | confidence |
|---|---|---|
| **P0** | Starting shapes that can hold their clocks together (3D grid, web) still hold as they grow | High |
| **P1** | **The main one:** the line and the flat grid do **not** survive as themselves — they are either forced above two dimensions or they stop holding together | **About 55%** |
| **P2** | The 3D grid survives as itself, reading within ±0.3 of where it started | About 40% |
| **P3** | Reported, no expectation: what the small-world start becomes, and relations per event in every case |

**If P1 and P2 both hold, road P has its result:** ED forbids sub-three-dimensional space from persisting, and keeps three-dimensional space once it's there. That is a real, limited, honest claim — and it is not the claim that ED makes space.

## Honest points up front

1. **This is a weaker claim than the project set out to prove**, and it should be said in those words. ED would explain why space that exists stays and stays workable. It would not explain why there is space, or why three.
2. **Shape stays a supplied input.** The list doesn't shrink. Attempt 12 will not write persistence up as a reduction.
3. **The probes this road is built on are single-seed diagnostics**, and one of them leaks relations as it grows. Road P's first test has to be done properly — repeats, seeds, controls — or its result is worth no more than the probes'.
4. **P-Q2 is the hinge.** If a pattern that can't sync is simply *allowed to exist anyway*, there is no filter and road P has nothing to test. The whole road rests on ED meaning what attempt 6 took it to mean.

## Options

| | option |
|---|---|
| **(a)** | **Answer P-Q1 to P-Q6**, then I write the model and its expected results on paper, then build it |
| **(b)** | Take **P-Q2 first, on its own** — what *does* happen to a pattern whose clocks can't agree? — before anything else, since the road collapses without it |
| **(c)** | Redo attempt 11's two probes properly first, so road P is built on something solid |

**Proposed: (a)**, with P-Q2 and P-Q3 the two I'd most want in your own words rather than mine.
