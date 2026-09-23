# Road N: space is not assumed

*ED_Attempt_11, note 9. 2026-09-22 (RD13). Ledger: C18, D11. On paper; nothing computed. Written plainly, from Allen's D9 and the audit (C16).*

## Why this road

The audit found that every model since attempt 7 assumed space is a sheet of triangles — a borrowed assumption — while ED's own content (clocks, rates, sync) was left out entirely. **This road puts ED's content in and takes the sheet out.**

## What attempt 6 actually showed (and it fits this road exactly)

Attempt 6's "rates can match" was **not** a geometric argument. It was this:

- **Take any patch of n clocks.** Their rates differ a little at random, so the patch as a whole runs fast or slow by a surplus that grows like **√n**.
- **The only thing that can pull the patch into line is its neighbours**, through the relations crossing the patch's edge, and each relation can pull only so much (ED's "no infinities").
- **So rates can match across the pattern only if the edge keeps up with the surplus.** The edge grows like n^((d−1)/d); the surplus like √n. That needs **d > 2**.

| dimension | edge against surplus | rates can match? |
|---|---|---|
| 1 | edge stays two points | never |
| 2 | both grow like √n — a tie | lost by a hair |
| **3** | edge grows faster | **yes** |

**No coupling ratio is needed for the floor**; it comes from the exponents alone. With "fewest directions" on top, three is the first dimension that works. **That is ED's own mechanism for three dimensions, and it never mentions triangles.** It's a condition a *network* must satisfy — which is precisely what this road needs.

## The picture

**Events, each with a rate.** Relations between events. **No background sheet, no coordinates, no dimension anywhere in the rules.**

- A pattern **survives** if its clocks can hold together — if the edge of every patch can keep up with the patch's surplus.
- **Dimension is not put in. It's read off at the end** — from how fast balls grow, how relations cross patch edges, how distance grows with size.
- **Your picture in the same words:** an uncommitted pattern doesn't touch nodes and so isn't anywhere; a particle is a pattern of commitments and so is somewhere; space is the lit-up, committed part.

## What ED needs to say before this can be built (your calls)

| | question | what hangs on it | a default I'd propose |
|---|---|---|---|
| **N-Q1** | **Is there a background at all** — a dimensionless relational substrate whose nodes get lit up — or only events and their relations? | Whether "space is permanent once laid down" is even sayable. **Careful:** if the background has a built-in dimension, three is put in by hand | **Only events and relations** (least structure). Your background version stays recorded as the alternative |
| **N-Q2** | **What is "rates can match"?** Attempt 6 used a collective condition — a patch against its edge — not a pairwise one | Everything. A pairwise "rates within a window" rule would make space one-dimensional, a line of rates | **Collective**, as attempt 6 had it: a pattern is allowed if every patch's edge can hold it |
| **N-Q3** | **Do relations stick?** Once two events commit, is that permanent, as the Generative papers' commitment-irreversibility says? | Whether space is remade each tick or accumulates | **Yes, they stick** — that matches your "once lit, it stays" |
| **N-Q4** | **Does the budget still rule size?** | Whether Budgeted Causality carries over | **Yes** — it's ED's own and it survived the audit |
| **N-Q5** | **What reading counts as "3D space appeared"?** Fixed before any run | Whether the test can be honest | Balls grow like the cube of their radius over a range of scales; distance grows with size like the cube root; relations crossing a patch edge grow like its area — the three readings already calibrated in attempts 5–9 |

## The first test, and its picture

**What would be built:** a growing network of events carrying rates — no sheet, no triangles, no coordinates. The budget sets how many events there are. A pattern is kept only if its patches can hold together in attempt 6's sense.

**What would be read:** ball growth, distance against size, and edge-against-patch growth.

**What the outcomes mean:**
- **Readings land near three** — ED's own rules make three-dimensional space, with no geometry assumed. That is the result the whole project has been after, and it would come from clocks rather than from sheets.
- **Readings land near one or two** — the sync condition doesn't lift a network into three dimensions on its own; something else is needed.
- **Readings run away (very high dimension, small-world)** — the same wall as attempts 7–9, but now clearly about ED's own rule rather than the borrowed one.

**Cost:** the network is far cheaper than triangulations — no manifold bookkeeping. Days rather than weeks, and it reuses the readings we already have.

## Honest points up front

1. **Attempt 6's argument selects among dimensions; it doesn't by itself build a network.** It says which patterns can hold together. The road's real question is whether ED's growth *produces* such patterns, or only tells us which ones would survive.
2. **"Fewest directions" is doing work.** The floor gives d > 2; three is picked by minimality. That extra step is a meaning, not a result.
3. **This is not a fresh start.** Budgeted Causality, the ceiling, commitment, and the three inputs all carry over. What's dropped is the sheet.
4. **If a background is assumed (N-Q1, your version), it must be dimensionless** — otherwise three dimensions are smuggled in, and the census guard fails.

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Answer N-Q1 to N-Q5**, then I write the model and its expected results on paper, then build it |
| **(b)** | Take the road's questions one at a time, starting with N-Q2 (what "rates can match" means), before anything else |
| **(c)** | Wait for the 2+1 runs first |

**Proposal: (a).** The 2+1 runs finish on their own; this road doesn't need them.
