# With commitment: the churn stops, the numbers move toward three — and the shapes still aren't kept

*ED_Attempt_12, note 9. 2026-09-23 (RD12). Ledger: C12, from D6. Code `model/l_local2.py`, output `model/l_local2.txt`, data `model/p_runs/local2.json`. Expectations M1–M4 fixed in the code header before the run. Written plainly.*

## The short answer

**D6 did what it was meant to do.** The churn stops: patterns let go of a third to a half as many relations as before. And the readings move **down**, closer to three than anything since this road opened.

**But the shapes are still not kept, and the end state is still a small world.** M2 fails.

## The numbers

At about 8,000 events, three seeds each:

| start | reading | mean distance | relations per event | added | dissolved |
|---|---|---|---|---|---|
| **ring** (was 1.0) | 3.93, 3.98, 4.04 | 500 → 6.8 | 2.0 → **4.20** | ~5,500 | **~2,100** |
| **3D grid** (was 2.36) | 3.75, 4.86, 3.86 | 9.7 → 7.1 | 6.0 → **4.17** | ~4,750 | ~6,000 |
| **web** (no dimension) | 3.76, 3.92, 3.92 | 4.6 → 6.9 | 6.0 → **4.15** | ~4,700 | ~5,700 |

| | expectation | result |
|---|---|---|
| **M1** | Patterns hold without fragmenting | **As expected.** Every run in one piece |
| **M2** | The ring and the 3D grid read as themselves | **No.** Both land near 3.9, against 1.00 and 2.69 for real ones |
| **M3** | The churn falls sharply — **the check on whether D6 bites at all** | **Yes.** The ring let go 2,143 relations where C11 let go 12,800; the others 5,700–6,000 against 15,400–17,300 |
| **M4** | Relations per event, and whether the starts still converge | **4.15, 4.17, 4.20** — still one common end state, reached from a line, a lattice and a random web alike |

## The trend across the three rules, labelled as an observation and not a claim

Each time one of my assumptions was replaced by something ED actually says, the end state moved:

| the filter | relations per event | reading |
|---|---|---|
| global lock, relations permanent *(mine)* | 6.2 | 4.2 |
| local patches, relations lapse the moment they're idle *(mine)* | 3.0 | 4.8 |
| **local patches, a relation persists while it is part of a commitment *(D5 + D6, ED's)*** | **4.2** | **3.9** |

**ED's own rule gives the lowest reading of the three.** That is worth noticing and worth not over-reading: 3.9 is still flagged a small world, which means the number is not a dimension at all — it's what the reading returns when there isn't one. Three points on a trend with no error bars is a direction, not a result.

## What the pull does

| pull | reading | mean distance | relations per event |
|---|---|---|---|
| 0.5 | none | 5.2 | 6.60 |
| 1.0 | 3.75 | 7.1 | 4.16 |
| 2.0 | 3.92 | 9.9 | 2.98 |

As before: the density and the distances depend on my setting; the reading doesn't move much between pulls 1 and 2.

## Where this leaves road P and attempt 12

**Every assumption of mine that could be replaced has been replaced**, and the answer has not changed in kind:

- no shared now (D5) — replaced, still converges;
- relations free to dissolve (D4) — replaced, still converges;
- commitment persisting rather than lapsing instantly (D6) — replaced, still converges.

**ED's rules converge; they do not select.** Three very different starts reach one common end state. That end state is sparse, spread out, holds its rates patch by patch — and has no dimension.

**What did change, and it is not nothing:** every correction moved the end state toward the sparser, more spread-out side, and toward a lower reading. If there were a fourth correction of the same kind, this is the direction it would come from — but I don't have a candidate, and I'd rather say so than invent one.

## Options

| | option |
|---|---|
| **(a)** | **Take stock of attempt 12** — road P, the balance point, the reach, local sync and commitment are all in, and together they say something clear |
| **(b)** | Ask what the common end state **is** — it's reached from everywhere, it's sparse, it holds its rates locally, nothing chose it. That's a describable object, and nobody has looked at it directly |
| **(c)** | Keep hunting for a fourth assumption of mine to replace — I don't have one, and looking for one without a candidate is how fitting starts |

**Proposed: (a), with (b) as the first thing attempt 13 might do.**
