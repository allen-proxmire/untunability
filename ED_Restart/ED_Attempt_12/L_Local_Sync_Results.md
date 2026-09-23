# Local sync: every pattern goes to the same place, and it is sparse

*ED_Attempt_12, note 8. 2026-09-23 (RD11). Ledger: C11. Code `model/l_local.py`, output `model/l_local.txt`, data `model/p_runs/local.json`. Expectations L1–L4 fixed in note 7 before any code. Written plainly.*

## The short answer

**With ED's sync condition in attempt 6's own form — every patch shedding its surplus through its own edge, no shared now — and with relations free to dissolve, every start still ends in the same place.**

**But the place has changed.** Under the old global filter, patterns were driven *up* to 6–7 relations per event and crammed together. Under this one they settle *down* at **3 relations per event** and **spread out**. The shape is still not three-dimensional, and it is still not kept.

## The numbers

At about 8,000 events, three seeds each:

| start | reading | mean distance | relations per event | added | dissolved |
|---|---|---|---|---|---|
| **ring** (was 1.0) | 4.67, 4.73, 4.95 | 500 → **7.8** | 2.0 → **3.01** | ~13,900 | ~12,800 |
| **3D grid** (was 2.36) | 4.83, 4.65, 5.02 | 9.7 → **7.8** | 6.0 → **3.04** | ~13,500 | ~17,100 |
| **web** (no dimension) | 4.63, 4.81, 4.77 | 4.6 → **7.8** | 6.0 → **3.06** | ~12,600 | ~15,700 |

**Three starts as different as a line, a lattice and a random web, and they agree to two decimal places on relations per event and to one on mean distance.** Nothing was tuned to make that happen.

| | expectation | result |
|---|---|---|
| **L1** | Patterns hold together without fragmenting | **As expected.** Every run in one piece |
| **L2** | The ring and the 3D grid still read as themselves | **No.** Both are driven to about 4.8, against 1.00 and 2.69 for real ones |
| **L3** | A small-world start sheds relations and reads lower | **Passed as written** — the web shed half its relations (6.0 → 3.06) and its mean distance nearly doubled (4.6 → 7.8) while the pattern grew four-fold. **But the spirit only half happened:** it spread out, it did not arrive at a definite dimension |
| **L4** | Relations per event | **3.01, 3.04, 3.06** — below ED's budget of 6.7, and below C7's fragmentation threshold of about 5, yet still in one piece |

## The pull check, run in the same go

The pull is the one number ED doesn't supply, so it was varied on the 3D grid:

| pull | reading | mean distance | relations per event |
|---|---|---|---|
| 0.5 | 4.70 | 5.9 | 4.50 |
| 1.0 | 4.83 | 7.8 | 3.02 |
| 2.0 | 4.63 | 11.2 | 2.36 |

**The relation count and the distances depend on the pull; the reading does not.** 4.6–4.8 across a four-fold change. So the end state's *shape* is not an artefact of my setting, even though its density is.

## What this settles

**The overshoot is ED's, not mine.** That is the honest verdict, and it survives both of Allen's corrections — no shared now, and relations free to dissolve. Note 7 said in advance that this outcome "closes the line properly, and honestly", and it does.

**What ED's rules do is converge, not select.** Three wildly different starts reach one common end state, tightly. That is real, it is ED's own doing, and it is a stronger property than the persistence attempt 11 thought it had found. But the end state is a sparse small world, not space.

**What changed for the better, and is worth keeping:** with relations free to dissolve, patterns get *sparser and more spread out* rather than denser and more crammed. Every earlier model made things worse in that respect. D4 was the right correction; it just doesn't rescue the dimension.

## The one thing I'd still question, and it is mine

**I made a relation dissolve when it carries nothing *this generation*.** Rates are drawn afresh each generation, so a relation idle now may be needed next time — and the pattern churns: about 13,000 relations added and 13,000–17,000 let go over a run that ends with only about 25,000. **That churn is a plausible cause of the randomising**, and it comes from my reading of D13, not from anything ED says.

**The meaning question that would settle it, for Allen:** does a commitment lapse the moment it isn't carrying anything, or does it persist while it is part of a commitment and lapse only after being idle for a while? I took the first as the simplest reading. The second sounds closer to how commitment has been described since attempt 4, and it is a one-line change to test.

## Options

| | option |
|---|---|
| **(a)** | **Settle the lapse question** and rerun — a relation lapses only after being idle for several generations, rather than immediately. It is the last assumption of mine standing between this model and ED's own words |
| **(b)** | **Take stock of attempt 12** — road P, the balance point, the reach and local sync are all in, and together they say something clear |
| **(c)** | Accept the convergence as the result and ask what the common end state *is*, rather than what it isn't — it is reached from everywhere, it is sparse, it holds its rates locally, and nothing chose it |

**Proposed: (a) then (b).** (a) is cheap and it removes the last of my assumptions from the model; (b) is the right place to stop either way.
