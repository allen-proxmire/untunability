# Road N: the model, on paper

*ED_Attempt_11, note 10. 2026-09-22 (RD14). Ledger: C19, D12. Specification; nothing computed. Written plainly; the technical box is at the end.*

## What you decided (D12)

No background — only events and relations. "Rates can match" is collective, a patch against its edge. Relations stick once committed. The budget still rules size. Three dimensions means the three calibrated readings.

## The model in plain words

**Events, each with its own natural rate** — a clock that would tick at its own speed if left alone. **Relations between events** let neighbours pull each other's ticking into line. **Nothing else.** No sheet, no coordinates, no dimension anywhere in the rules.

**What ED supplies:**
- the **budget**, which fixes how many events there are and how many relations they may carry;
- the **ceiling**, which caps how hard any one relation can pull;
- **commitment**, which makes a relation stick once made;
- **"fewest directions"** — ED's preference for carrying as few relations as it can.

**What is measured afterwards:** whether the clocks can hold together, and what dimension the pattern reads.

## The mechanism being tested

Attempt 6's argument, in one line: **a patch's rate surplus grows like the square root of its size, the pull available grows like its edge, so only patterns whose edges grow fast enough can hold together — which needs more than two dimensions.**

**Add ED's "fewest relations" on top and you get a sharp claim:**

> **A pattern that carries as few relations as it can, while still holding its clocks together, should sit just above the floor — and the first dimension above two is three.**

That is the thing to test, and it is made only of ED's own parts.

## How to test it without smuggling anything in

**The one number ED doesn't supply is how hard a relation pulls.** Attempt 6 was careful about this: the *floor* needs no such number, but whether rates actually match does. So the test never fixes that number. Instead:

> **For each pattern, find the weakest pull that still holds it together, and watch how that changes as the pattern grows.**

- **If the pattern can't hold together** — one or two dimensions — the pull needed **keeps rising** as it grows. Big patches always break away.
- **If it can** — three or more — the pull needed **settles** at some value and stops rising.

That's a yes/no answer with no knob in it.

## The three steps

**Step 1 — check the instrument on known patterns.** Lines, flat grids, 3D grids, and random webs, with random rates.
- **Expected** (published, and attempt 6's argument): the pull needed keeps rising on the line and the flat grid, and settles on the 3D grid and the random web.
- **If that fails**, our test of "holding together" is wrong and nothing later counts.

**Step 2 — ED's own patterns.** Grow a pattern under ED's rules: the budget fixes the number of events and relations, the ceiling caps each relation, relations stick, and the pattern carries **as few relations as it can while still holding together**.
- **Read:** does the pull needed settle as it grows? Then: what dimension does the pattern read?

**Step 3 — the readings, fixed now.** Balls growing like the cube of their radius, distance growing like the cube root of size, and relations crossing a patch edge growing like its area — all three calibrated in attempts 5 to 9.

## Expected results, fixed before any code

| | expectation | confidence |
|---|---|---|
| **N0** | Step 1 reproduces the known behaviour: pull-needed rises without limit on the line and the flat grid, settles on the 3D grid and the random web | High — it's published |
| **N1** | ED's grown patterns hold together at all (pull-needed settles) | Moderate |
| **N2** | **The main one:** a pattern carrying as few relations as it can, while holding together, reads between 2.5 and 3.5 on all three readings, at two sizes | **About 40%.** This is the claim; I don't want to talk it up |
| **N3** | Reported, no expectation: how many relations per event that pattern ends up carrying, against ED's own link budget of 6.7 | — |

**What each outcome means:**
- **N2 holds:** ED's own rules — clocks, budget, ceiling, fewest relations — give three-dimensional space, with no geometry assumed anywhere. That is the result the project has been chasing since attempt 5, reached through ED's own machine rather than a borrowed one.
- **Readings land near 4 or higher:** holding together doesn't hold a pattern *down* to three; something else must, and "fewest directions" isn't enough.
- **ED's patterns can't hold together at all:** the mechanism fails on ED's own patterns, and Synced Now doesn't carry over to grown patterns.

## Cost

**Days, not weeks, and it's laptop-sized.** No triangulations, no manifolds. The heavy part is finding the weakest pull that still holds each pattern together, which is a small solve repeated many times; the readings already exist.

## Two questions left for you

| | question | default |
|---|---|---|
| **N-Q6** | **How spread out are the natural rates?** Everything scales with this, and ED doesn't supply it | Treat it as the unit — measure pull in units of the rate spread, so the number drops out |
| **N-Q7** | **"Fewest directions" made exact:** the pattern carries the smallest number of relations per event that still holds together | Yes — that's what makes the claim sharp |

---

### Technical box

- **State:** N events; event i has natural rate ω_i drawn from a fixed spread; a relation set with degree capped at the ceiling; phases θ_i.
- **Holding together:** run the standard phase dynamics θ̇_i = ω_i + K Σ_j sin(θ_j − θ_i) over the relations; the pattern holds if every event's long-run average rate is the same within tolerance (frequency locking), measured after transients.
- **The weakest pull:** bisection on K to find K_c(N), the smallest coupling that locks, at sizes N = 2k, 4k, 8k, 16k. Rising K_c(N) means no matching in the large-size limit; settling K_c(N) means matching is possible. This is the ratio-free form of attempt 6's floor.
- **Step 1 objects:** ring, square-grid torus, cubic-grid torus, and an Erdős–Rényi web at matched average degree.
- **Step 2 growth:** start from a small pattern; add events under the budget; add relations only while the pattern fails to hold together, and stop as soon as it holds (this is "fewest relations that still hold"); relations stick (D12); the ceiling caps degree; repeat to the target size.
- **Readings:** ball growth d_H and the edge-against-patch exponent from attempts 5 and 9; the spectral dimension curve from attempt 8; small-world flag as in attempt 9.
- **Controls:** the same readings on the step-1 objects, so ED's numbers are read against known patterns at the same sizes.
