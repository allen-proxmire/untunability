# Road E with gradients: the model, on paper

*ED_Attempt_13, note 4. 2026-09-23 (RD4). Ledger: C4, from D2. Specification; nothing computed. Written plainly; the technical box is at the end.*

## What you decided (D2)

**E-Q1 yes: rates pass on.** A child's rate is its parent's, with a small variation.
**E-Q2 yes: rates diffuse.** Each tick, an event's rate moves a little toward its neighbours'.

**And a condition you attached:** only if it isn't chasing something new you said. **It isn't.** Both come from *Event Density and the Architecture of the Universe*, §4 and §26 — January 2026, before this restart began. **The rule now on the record: a road is only worth building if what it adds was written down in ED beforehand.**

## The picture

**Until now, every event in every model has ticked at a rate drawn out of a hat, and in the generation models a fresh rate was drawn every tick.** There was no such thing as a fast region or a slow region — only noise.

**Now there is.** An event inherits its parent's rate, so a fast patch stays fast and its children are fast. Rates spread toward their neighbours, so sharp differences soften over time. **That is a gradient: a region that is systematically faster than the region beside it, persisting because it is passed on, softening because it diffuses.**

And your paper says that's what space is made of:

> *"Space is the pattern of stable relations formed by persistent ED gradients. Distances correspond to differences in ED."*

**What would be read:** the same calibrated readings as before — how balls grow, how distances grow with size, whether it's a small world — **plus two new ones that only make sense now there are gradients:**
- **do gradients survive at all, or does everything flatten?**
- **the paper's own distance** — difference in rate along a path — read alongside hop-count distance, to see whether they agree.

## The trap, and the void condition that guards it

**A flat pattern satisfies every sync condition trivially.** If rates diffuse until every event ticks at the same rate, every patch has no surplus, every patch holds, nothing is strained, and the model will report perfect success while containing nothing at all.

**So this is pre-registered as a void condition, not a result:**

> **If the spread of rates across the pattern falls below a tenth of what it started at, the run is void** and is reported as *the pattern flattened*, never as *the pattern held together*.

Your paper says a universe does end that way — §16 and §29, heat death as ontological flatness. So flattening is a real outcome. It is just not a success, and the write-up must not be able to confuse the two.

## The model

Everything from the local-sync model (C9, C11) is unchanged: events pass on once and are spent; neighbourhoods are inherited; every patch must be able to shed its surplus through its own edge, checked exactly, with no shared now; relations are added across the starved patch's edge; a relation persists while it is part of a commitment (D6).

**The two changes, and only these two:**

1. **A child's rate is its parent's, plus a small variation.** Gradients persist because they are passed on.
2. **Each tick, an event's rate moves a little toward its neighbours' rates.** Gradients soften; this is the paper's diffusion, and it is the arrow of time in ED's own terms.

## Expected results, fixed now, before any code

| | expectation | confidence |
|---|---|---|
| **G0** | **The void check:** gradients survive long enough to matter — the rate spread does not collapse below a tenth of its start before the pattern reaches its final size | About 55%. **If this fails, nothing else in the run counts** |
| **G1** | With gradients, patterns hold their rates on **fewer** relations than with noise — under 4.15 per event, because neighbours now tick alike and less has to be carried | About 70% |
| **G2** | **The main one:** the end state is no longer the same from every start — gradients give a pattern something to remember, so a 3D grid and a random web no longer converge on one object | **About 40%** |
| **G3** | **The one that would matter most:** the readings come out lower than the 3.9 of the noise model, and the small-world flag clears on at least one start | **About 20%.** Written low on purpose |
| **G4** | Reported, no expectation: whether the paper's own distance (difference in rate along a path) agrees with hop-count distance; how big the gradients are at the end; what the rate spread does over the run |

## What each outcome would mean

- **G0 fails — everything flattens:** ED's own diffusion erases its own gradients under these rules, and space, in the paper's sense, cannot persist in this model. That is a real and reportable negative about the mechanism, not about our instruments.
- **G2 holds:** gradients give a pattern a memory, and the convergence found in attempt 12 was a consequence of rates being noise. **That would revise A12 C11 and C12**, the same way attempt 12 revised attempt 11.
- **G2 fails:** convergence survives the addition of gradients, and attempt 12's finding stands as ED's own, not as an artefact.
- **G3 holds:** the readings move toward a dimension once ED's own content is in. That would be the first positive movement in the project on this question, and it would need repeating at more sizes and seeds before it was said aloud.

## What is mine, and labelled

**How big the variation is** when a rate passes on, and **how fast rates diffuse.** Both are numbers ED does not supply. They will be set to the smallest values that let a gradient exist at all, reported plainly, and **varied afterwards** — the answer is theirs as much as ED's until that's checked, exactly as the pull was in C5 and C11.

Also mine: sizes, seeds, the bell curve the first generation's rates come from, and the tenth-of-the-start threshold in the void condition.

## Honest points

1. **This does not make space from nothing.** Starts are still supplied. What it can settle is whether gradients change what ED's rules do to a pattern.
2. **Nothing here is a reduction.** Two new numbers of mine go in. Under the census guard the input list gets *longer*, and the write-up will say so.
3. **The most likely single outcome is G0 failing** — diffusion flattening everything. That is why it is written first and why it voids the rest.
4. **This is the fourth correction of the same kind** (clocks, shared now, dissolution and commitment, now gradients). Each one has improved the model's character and none has changed the answer. If gradients don't either, the honest reading is that ED's rules, as written down, do not make space — and that becomes the result rather than a staging post.

---

### Technical box

- **Rates:** generation 0 drawn from a unit bell curve. A child takes its parent's rate plus a draw of size **σ_pass** (Claude's, default 0.1 of the initial spread). Each tick, before the condition is checked, every rate moves toward the mean of its neighbours' by a fraction **α** (Claude's, default 0.1). Mean removed each tick so the condition is well posed.
- **Void check:** the standard deviation of rates across the frontier, recorded every generation; the run is void if it falls below 0.1 of generation 0's.
- **Condition, repair, dissolution, growth:** exactly C9/C11/C12 — max-flow feasibility over all patches, additions across the min cut, a relation persisting once it has carried anything.
- **Readings:** ball growth, patch-edge exponent, mean distance, small-world flag, relations per event, share in one piece; plus **rate-distance** (the accumulated |Δrate| along shortest paths) against hop distance, and the rate spread over time.
- **Starts:** ring, cubic torus, 6-regular web, about 2,000 events, grown four-fold, three seeds.
- **Afterwards:** σ_pass and α each varied by a factor of about three, as the pull was in C11.
