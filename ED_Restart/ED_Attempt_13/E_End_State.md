# Road E: what ED's rules actually make — on paper

*ED_Attempt_13, note 2. 2026-09-23 (RD2). Ledger: C2. On paper; nothing computed. Written plainly; the technical box is at the end.*

## The picture

**There is an object sitting in the run data that nobody has described.**

Start from a line, a flat grid, a 3D grid or a random web. Grow it under ED's rules — events passing on once and being spent, neighbourhoods inherited, patches able to shed their rates through their own edges, relations dissolving unless they're part of a commitment. **Whatever you start from, you end up with the same thing.**

We know four things about it and no more: it carries about **4 relations per event**, its distances are **short but growing** (about 7 across 8,000 events), it is **flagged a small world**, and the ball-growth reading returns about **3.9**, which — because the small-world flag is set — means *no dimension*, not *dimension 3.9*.

**That's all. Nobody has asked what it is.** Every test so far asked whether it was three-dimensional space, got "no", and moved on.

## The discipline this road needs

Description is the easiest thing in the world to do badly. A network can be made to sound profound with no content at all. So **every statement about the object gets measured against references at the same size and the same relation count** — a random regular web, a 3D grid, a small-world rewiring, a tree, and a preferential-attachment web. If the object can't be told apart from a random web, that is the finding, and it gets written that way.

**And the readings are fixed before looking**, as always.

## The five questions

| | question | why it matters |
|---|---|---|
| **E-1** | **Is it one object, or only one set of readings?** Three starts agreed on relations per event and mean distance. Do they also agree on the shape of the neighbourhood, the spread of relation counts, the clustering, the spectrum? | If not, "convergence" was a coincidence of two numbers, and C11/C12 need correcting |
| **E-2** | **How do its distances really grow?** Like the logarithm of size (a small world) or like a power (a dimension we can't see at these sizes)? | The one measurement that could revive the dimension question, and it needs sizes up to about 32,000 to answer |
| **E-3** | **Is it sitting exactly on the edge of holding together?** ED's rule keeps the fewest relations that still let every patch shed its surplus. **The cheapest pattern that holds is one that only just holds.** So its patches should sit near equality in attempt 6's inequality rather than comfortably inside it | **The main one.** If it holds, the object has a name: it is a *critical* pattern, sitting on the floor attempt 6 derived. That is a real characterisation, and it comes straight from ED's own minimality |
| **E-4** | **Does it have structure at some scale**, even if it has no dimension overall? The spectral reading (attempt 8's tool) can show a definite value at one scale and not another | A pattern can be a small world at large scales and three-dimensional up close. Attempt 9 saw exactly that once |
| **E-5** | **Is it the same object at every size?** | Everything we've said about it comes from one size range. If the readings drift, we've been describing a transient |

## Expected results, fixed now

| | expectation | confidence |
|---|---|---|
| **E1** | The three starts give the same object, not just the same two numbers — neighbourhood statistics agreeing within the seed spread | About 60% |
| **E2** | Distances grow like the logarithm of size, not like a power | About 70% |
| **E3** | **The main one:** the object's patches sit near equality in attempt 6's inequality — it only just holds together | **About 45%** |
| **E4** | The spectral reading gives a definite value at some scale even though ball growth gives none | About 30% |
| **E5** | Reported, no expectation: the spread of relations per event, clustering, and how every reading moves from 2,000 to 32,000 events |

## What each outcome would mean

- **E3 holds:** ED's rules make a **critical** pattern — the cheapest thing that still holds its rates, sitting exactly on the floor attempt 6 derived. That is a describable, nameable result about what ED makes, and it follows from ED's own minimality rather than from anything supplied. **It is still not space**, and the write-up will say so in the same breath.
- **E3 fails and the object sits comfortably inside the floor:** then minimality isn't reaching the edge, and something else is stopping it — worth knowing, and it would point at the repair rule.
- **E2 fails — distances grow like a power:** the dimension question reopens, at a value we'd then have to read honestly, high or low.
- **E1 fails:** convergence was two numbers agreeing, not one object. C11 and C12 get corrected, the way C5 was.
- **E4 holds:** the object is one thing up close and another far away, which is what attempt 9 saw and never followed up.

## The honest points

1. **This is description, not a test of ED.** Nothing here can make ED right or wrong. It says what ED's rules produce, which is worth having written down after twelve attempts of asking whether it was something else.
2. **No reduction is available on this road.** Under the census guard, describing an object doesn't shorten ED's input list. Nothing here will be written up as a reduction.
3. **The starts are still supplied** — but for the first time that matters less, because the object is the same whatever you start from. That is the one respect in which this road is about ED rather than about the start.
4. **A literature step belongs in the middle of it, not at the end:** once the object's statistics are in hand, they get checked against known classes of network — random regular, critical percolation clusters, small-world rewirings, scale-free webs. If it is a known object, it gets named, and that is the honest outcome. If it isn't, that's worth knowing too, and the claim has to be made carefully.

## Cost

**Laptop-sized, and mostly cheap.** The object is produced by code that already exists. The expensive part is one size, 32,000 events, for E2 and E5 — a few hours at most. Everything else is measurements on patterns we can generate in minutes.

## Options

| | option |
|---|---|
| **(a)** | **Answer E-1 to E-5 as written** — they need no meanings from Allen, only agreement that these are the right questions to ask of the object |
| **(b)** | Add a question: whether the object depends on the *rates* — everything so far used one bell curve, and the object might be a property of that rather than of ED |
| **(c)** | Narrow to E-3 alone, the critical-pattern question, and leave the rest |

**Proposed: (a) with (b) folded in.** (b) is a real gap — the rate spread is mine, not ED's, and if the object is an artefact of a bell curve, that should be found now rather than after it has been described.
