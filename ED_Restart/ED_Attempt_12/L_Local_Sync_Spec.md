# The local sync model, on paper

*ED_Attempt_12, note 7. 2026-09-23 (RD9). Ledger: C9, from D4 and D5. Specification; nothing computed. Written plainly; the technical box is at the end.*

## What changed, and why this is a different model

**D5: there is no shared now.** Every test so far asked whether the whole pattern could be brought to one common rate — a single lock across everything at once. That is a shared now, and ED has denied having one since attempt 6. It was my assumption, not ED's, and it is the reason the filter never stopped repairing.

**D4: a relation can dissolve.** Every test so far could only ever add. Each generation inherited every repair the last one needed — a ratchet. With D4 the pattern can also let go, and ED's own D13 then works in both directions.

**So this model asks a question none of the earlier ones did:** with no shared now, and with relations free to come and go, what shape does ED's growth settle on?

## The condition, in plain words

Attempt 6's argument, which was never actually implemented, says this:

> **Take any patch of the pattern.** Its clocks run a little fast or slow on average, so the patch as a whole has a surplus to shed. The only way to shed it is through the relations crossing the patch's edge, and each of those can carry only so much. **The patch holds if its edge can carry its surplus.**

**The whole pattern holds if every patch does.** No patch anywhere is starved.

**That is a local condition and it needs no shared now.** Nothing has to happen at the same time anywhere; nothing has to agree on a moment. Each patch only has to be able to pass its surplus to its neighbours.

**And it can be checked exactly, at every scale at once, with no new dial** — that is the piece I had wrong before. Asking "can every patch, of every size, shed its surplus?" turns out to be a single well-posed question with an exact answer, not something that needs a patch size chosen by me. *(The technical box says how.)*

## The model

**Growth, unchanged from road P:** every event passes on once and is then spent; children inherit their parents' neighbourhoods; relations per event carried forward.

**Then, each generation, two steps instead of one:**

1. **Where a patch is starved, relations are added across its edge.** Not "where the strain is worst" by a proxy — the test itself names the starved patch and the edge it needs, so relations go exactly there.
2. **Where a relation carries nothing, it dissolves.** The pattern keeps the fewest relations that still let every patch shed its surplus.

**That is D13 applied both ways, which is what ED has said all along and what we had only ever done half of.**

## What each outcome would mean

| what we'd see | what it means |
|---|---|
| **Shapes are kept** — a ring stays a line, a 3D grid stays 3D, each carrying few relations | **The overshoot was mine.** ED's own sync condition is satisfiable locally, and a pattern under it keeps what it is. Road P's negative was about my global filter, not about ED |
| **Everything still converges on a small world** | The overshoot is ED's after all, and it survives both corrections. That closes the line properly, and honestly |
| **A small-world start *thins out*** under dissolution, toward something with a dimension | **The most interesting outcome available.** It would mean ED's rules don't just permit shape, they *select* it — the thing the project has been looking for since attempt 5 |
| **Patterns fall apart** — dissolution goes too far and they fragment | The two halves of D13 don't balance, and ED needs something more to say about when a relation goes |

## Expected results, fixed before any code

| | expectation | confidence |
|---|---|---|
| **L1** | Patterns satisfying the local condition exist, and the growth reaches them without fragmenting | High |
| **L2** | **Shapes are kept** — the ring and the 3D grid each still read as themselves after four-fold growth | **About 50%** |
| **L3** | **The one I most want to see:** a small-world start sheds relations and reads *lower* than it started | **About 25%** |
| **L4** | Reported, no expectation: relations per event each start settles on, against ED's budget of 6.7 and against the fragmentation threshold of about 5 found in C7 |

## What is mine, and what is ED's

**ED's:** events and relations; the ceiling; passing on once and being spent; passing on reaching a neighbourhood (A11 D4); a patch holding its rates against its own edge (A6); relations able to dissolve (D4); no shared now (D5); the fewest relations that still hold, both ways (D13).

**Mine, labelled:** the growth rate per generation; the starting sizes and seeds; the bell-curve rate spread; **the pull K, which sets how much one relation can carry** — still the one number ED doesn't supply, still held at 1 in units of the rate spread (D2 P-Q6 / A11 D13), and still to be varied afterwards to see what the answers depend on.

## Honest points

1. **This is the first model in which ED's sync condition appears in the form attempt 6 actually argued for.** Everything from attempt 7 onward used either geometry or a global lock. That's worth stating rather than glossing.
2. **It does not make space from nothing.** The starts are still supplied. What it can settle is whether ED *keeps* or *selects* a shape — not where the first one came from.
3. **If shapes are kept, that is persistence** — and persistence, as note 2 said, is a constraint rather than a reduction. It doesn't shorten ED's input list.
4. **If a small world thins toward a dimension, that would be a selection**, and it would be the first one. It's also the least likely of the outcomes, and it's written down at 25% for that reason.
5. **The pull is still a supplied number.** If the answers move when it moves, they are its answers as much as ED's, and the run has to check that rather than assume it.

---

### Technical box

- **State:** frontier of events with natural rates ω (mean removed, unit spread), relations with degree ≤ 60, no coordinates.
- **The condition (A6, exact, all scales at once):** a pattern holds if there is an assignment of carrying f to its relations with |f_e| ≤ K on every relation and net outflow ω_i at every event. By the max-flow/min-cut theorem this exists precisely when **every** patch S satisfies |Σ_{i∈S} ω_i| ≤ K·e(S), with e(S) the relations crossing S's edge — attempt 6's inequality, at every scale, with no patch size to choose. Checked by one max-flow computation (rates scaled to integers); when it fails, the minimum cut **names the starved patch**.
- **Repair (D13, adding):** relations added across the returned min cut, between the starved patch and its complement, preferring events with the largest unmet surplus, up to the ceiling.
- **Dissolution (D4 + D13, letting go):** relations carrying no load in the flow solution are removed greedily, each removal kept only if the condition still holds.
- **Growth:** as road P — pass on once and be spent, siblings and cousins linked, relations per event carried forward (C4's conserving rule).
- **Readings:** ball growth, patch-edge exponent, mean distance, small-world flag, relations per event, share of the pattern in one piece; judged against a fresh object of the same kind at the same size (C4's rule).
- **Starts:** ring, cubic torus, 6-regular web, at about 2,000 events, grown four-fold, three seeds.
- **Afterwards:** the pull varied over 0.5, 1, 2 on whichever start matters most, as in C5's check.
