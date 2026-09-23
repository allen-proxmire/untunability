# The balance point: there isn't one — the rate doesn't move the dimension at all

*ED_Attempt_12, note 6. 2026-09-23 (RD8). Ledger: C7. Code `model/b_balance.py`, output `model/b_balance.txt`, data `model/p_runs/balance.json`. Expectations B1–B3 fixed in note 5 before any code. Written plainly.*

## The short answer

**No balance point — and for a more interesting reason than "we didn't find one".**

**The rate of relations per event doesn't move the dimension at all.** A ring grown with 16 relations per event is still a line. A 3D grid grown with 5 or with 16 is still three-dimensional. The rate changes how *thick* a pattern is and how faithfully it copies itself — it does not change what shape it is.

**B1 fails on both starts.** The drift never changes sign, because there is nothing for it to cross.

## The numbers

**Starting from a ring**, grown to 8,000 events:

| relations per event | reading at the end | a real ring reads | mean distance |
|---|---|---|---|
| 2 | 1.02 | 1.00 | 1,045 |
| 4 | 0.99 | 1.00 | 570 |
| 6 | 0.98 | 1.00 | 513 |
| 8 | 1.00 | 1.00 | 502 |
| 12 | 0.99 | 1.00 | 500 |
| **16** | **0.99** | 1.00 | 500 |

**Eight times the relations, and it's still a line.** All that changes is the thickness — mean distance falls from 1,045 to 500 and then stops.

**Starting from a 3D grid:**

| relations per event | reading at the end | a real 3D grid reads | in one piece? |
|---|---|---|---|
| 2 | 3.40 | 2.58 | **no — 47%** |
| 3 | 3.32 | 2.67 | **no — 65%** |
| 4 | 3.24 | 2.67 | **no — 82%** |
| 5 | 3.21 | 2.69 | yes |
| 6 | 3.25 | 2.69 | yes |
| 8 | 3.01 | 2.69 | yes |
| **12** | **2.71** | **2.69** | yes |
| 16 | 2.50 | 2.69 | yes |

**Below about 5 relations per event the pattern falls apart** — relations can't keep pace with events, and it breaks into pieces. That is the "events outpacing relations" side, and it's real. **Above that it holds together, and the more relations it carries the more faithfully it copies its own shape** — at 12 per event the grown pattern reads 2.71 against a real 3D grid's 2.69.

**But at no rate does it become something other than what it started as.**

| | expectation | result |
|---|---|---|
| **B1** | A balance point exists — the drift changes sign | **No.** The gap to a real shape grows slowly at every rate, and never shrinks |
| **B2** | If it exists, it reads 2.5–3.5 | Doesn't apply |
| **B3** | Reported | Below ~5 relations per event patterns fragment; above it they hold and copy themselves more faithfully as the rate rises; the two starts agree that the rate doesn't change shape |

## What this says about the inflation idea

Allen's reading — *events outpacing the production of space* — **is half right, and the half that's right is the half we'd already half-seen.**

- **It does control whether a pattern holds together.** Too few relations per event and it fragments. That's a genuine "production" balance, and it has a threshold, somewhere around 5 for these patterns.
- **It does not control dimension.** Nothing about the rate makes a line into a sheet or a sheet into a solid.

**So the 1D → 3 → small-world sweep we saw in attempt 11 was never about this rate.** It was about *where* new relations are allowed to reach. Here, relations only ever form between children of **neighbouring** parents — strictly one step — and that alone preserves dimension no matter how many of them there are.

## The thing this points at, which is sharper than the balance point

Road P's filter destroyed every shape. It was allowed to repair within **three** relations. Inheritance, which reaches **one**, preserves shape perfectly at any rate.

**So the destruction may be about the filter's reach, not about how much repair it does.** Seven thousand repairs at one step's reach might leave a line a line; a few hundred at three steps might not. That is a cheap and decisive test, and it's the natural next one.

## Options

| | option |
|---|---|
| **(a)** | **Test the reach.** Rerun road P's filter with repairs restricted to two steps instead of three, and again at three, on the same starts. If shape survives at two and dies at three, the reach is the whole story |
| **(b)** | Take stock of attempt 12 — road P is answered and so is the balance point |
| **(c)** | Settle the meaning question road P raised: whether a relation can ever lapse (D2 P-Q5 says no), since the filter can only add |

**Proposed: (a).** It's under an hour, it's the one question both results now point at, and it needs no new meaning from Allen.
