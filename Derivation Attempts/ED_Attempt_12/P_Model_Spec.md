# Road P: the model, on paper

*ED_Attempt_12, note 3. 2026-09-23 (RD3). Ledger: C3, D2. Specification; nothing computed. Written plainly; the technical box is at the end.*

## What you decided (D2)

All six as proposed: **keeping a shape means the readings hold** (within ±0.3 over a four-fold growth); **a pattern whose clocks can't hold together isn't allowed**; **an event passes on once and is then spent**; **space is the frontier**, with the accumulated pattern reported alongside; **relations never break**; **the 6.7 link budget is reported, not enforced**.

## The picture

**A generation of events, each with its own ticking rate.** Every one of them passes on — and is then spent, done, part of the past. Their children form the next generation. **Children of the same parent are linked to each other; children of neighbouring parents are linked to each other.** That, and only that, is how the shape gets carried forward: the new generation inherits the old one's neighbourhoods.

**Then the filter.** Before a generation is allowed to stand, its clocks have to be able to hold together. If they can't, the generation isn't allowed as it is — **the only way it can exist is by carrying more relations**, so relations are added where the strain is worst until the clocks hold. If no amount of relations within the ceiling can make it hold, **that pattern is destroyed** and the run ends there.

**Four starts:** a line, a flat grid, a 3D grid, and a small-world web. Each is grown until it is four times its starting size.

**And a control arm with the filter switched off**, same seeds, same everything. Without that, we can't tell what the filter did from what descent did on its own.

**What each outcome would look like:**

| what we'd see | what it means |
|---|---|
| The **line and the flat grid change or break**, the **3D grid stays itself** | **The filter bites.** ED's own content forbids sub-three-dimensional space from persisting. Road P's positive result |
| **Everything** ends up a small world, the 3D grid included | The filter overshoots — ED destroys everything, including what we'd want kept. A clean negative |
| **Everything keeps its shape**, the line included | Persistence is a restatement of "relations never break". Road P closes |
| The filter-off arm **also** destroys the line | It wasn't the filter. Whatever the main arm showed is void |

## The model, precisely

**Each generation:**

1. **Every event passes on once, then is spent.** Each parent has one child; a share of parents have two, so the generation grows slowly. Spent events keep every relation they had (relations never break) and keep their link to their children — they are the accumulated pattern, the past.
2. **The new generation's relations are inherited:** children of the same parent are linked; and for each relation between two parents, every child of one is linked to a child of the other. **This is the fix for attempt 11's leaky probe** — that version gave each parent relation a single cousin link, so relations bled away as the pattern grew (4.0 down to 2.2 per event). This version hands each child its parent's full neighbourhood, so a shape can be carried without thinning.
3. **The filter runs.** The generation's clocks are tested at a fixed pull. While they fail, relations are added where the strain is worst, up to the ceiling. Three outcomes: holds as inherited (nothing added), holds after repair (recorded: how many), or cannot be made to hold (**destroyed**).
4. **Readings taken** on the frontier — the dimension reading, mean distance, patch-edge exponent, small-world flag, relations per event — and on the accumulated pattern alongside.

**Repeated to four times the starting size**, three seeds each, both arms.

## Expected results, fixed now, before any code

| | expectation | confidence |
|---|---|---|
| **P0** | The 3D grid and the web hold their clocks at every generation | High |
| **P1** | **The main one:** the line and the flat grid do **not** survive as themselves — each is either forced above two dimensions by the repairs, or fails to hold at all | **About 55%** |
| **P2** | The 3D grid survives as itself, its reading within ±0.3 of where it started | About 40% |
| **P3** | Reported, no expectation: what the web start becomes; relations per event against ED's 6.7; how many relations the filter adds per generation, and whether that number grows with size |
| **P4** | **The control:** with the filter off, all four starts keep their shapes — attempt 11's probe 2, done properly. **If the line dies in this arm too, P1 is void** | High |

## What each result would license

- **P1 and P2 both hold:** ED forbids sub-three-dimensional space from persisting and keeps three-dimensional space once it is there. **A constraint ED derives from its own content** — and, stated plainly, *not* a derivation of space and *not* a reduction in ED's inputs.
- **P1 holds, P2 fails:** ED destroys everything, three dimensions included. The filter is real but indiscriminate, and this line of attack closes.
- **P1 fails:** persistence is a restatement of the rules. Road P closes, and what's left of ED is the budget result (A11 C5) and the measured sync floor (A11 C21).

## What is mine, and labelled as such

The growth factor per generation; the starting sizes; three seeds; the ±0.3 tolerance (your P-Q1, my number); the pull held at 1 in units of the rate spread (your D13); the bell-curve shape of the rate spread; and "where the strain is worst" as the rule for which relations get added — which is the same choice that most affected attempt 11's answer, carried forward unchanged so the two attempts can be compared.

**From ED:** events and relations; the ceiling; relations sticking; passing on once and being spent; passing on reaching a neighbourhood; clocks having to be able to hold together.

## Honest points

1. **The filter can only ever add relations, never move them.** So "destroyed" here means *changed beyond recognition*, not *annihilated*. That's the strongest version available while relations never break, and it's worth knowing that the rule you chose is what limits it.
2. **A line that gets repaired into something three-dimensional was still a line to begin with.** The result would be that ED can't *keep* sub-3D space, not that ED makes 3D space. I'll write it that way.
3. **The starts are supplied.** All four. That's the fourth input, and it doesn't go away in this attempt.
4. **Cost:** laptop-sized. Eight configurations at three seeds, each growing to four times its start — hours, not days, and no triangulations anywhere.

---

### Technical box

- **State:** frontier F_t (events with natural rates ω ~ unit spread, relations, degree ≤ 60) plus the accumulated pattern A_t ⊇ ∪F_s with parent–child relations.
- **Passing on:** each v ∈ F_t has c_v children, c_v = 1 with probability 1 − q and 2 with probability q (q set for a growth factor of about 1.1 per generation; labelled, Claude's). Parents are spent afterwards: they never parent again.
- **Inheritance:** siblings mutually linked; for each relation (p,q) ∈ F_t and each child a of p, one child b of q is chosen and (a,b) linked — degree-preserving, unlike A11's probe.
- **Filter:** locking of θ̇ᵢ = ωᵢ + K Σ sin(θⱼ − θᵢ) on F_{t+1} at K₀ = 1, judged as in A11 C21 (adaptive step, spread of long-run rates after transients). While not locked: add relations at the largest |x| from the linear solve L x = ω/K₀, partnered with events of opposite sign, in chunks, re-testing on the full dynamics. Destroyed = not lockable with every event at the ceiling.
- **Readings:** ball growth d_H and patch-edge exponent β (A5, A9 method), mean distance, small-world flag (A9), relations per event; on F_t and on A_t.
- **Pass rule:** "survives as itself" = |d_H(final) − d_H(start)| ≤ 0.3 with the clocks holding at every generation, over a four-fold growth in frontier size.
- **Starts:** ring; square-grid torus; cubic-grid torus; random 6-regular web — the same four objects calibrated in A11 C21, at about 2,000 events, grown to about 8,000.
- **Arms:** filter on; filter off (control). Three seeds each. Tools carried: `n1_sync.py`, `n2_grow.py`.
