# Stage B, gates G2 and G3: the 3D program works; the crowded start isn't crowded enough

*ED_Attempt_10, note 16. 2026-09-21 (RD16). Ledger: C27, C28. Code `model/sb_3d.py`, `model/sb_g2.py`, `model/sb_g3.py`; outputs `model/sb_g2.json`, `model/sb_g3.json`. Written plainly.*

## The short answer

- **G2 passed.** The history-counting program works on 3D slices: 40,000 steps, and not one invalid slice, wrong count or mismatched replay.
- **G3 failed.** The readings can't tell the flat start from the "crowded" start. The rule says "raise the sizes", **but size isn't the problem: the crowded start is barely crowded.** At ED's exact event and link counts, random rewiring leaves a slice nearly as spread out as flat.

**That needs your decision before any real runs.**

## G2 (C27)

**First try:** it worked, but only **1% of proposed changes were accepted** — most proposals picked changes that couldn't happen. Real runs would have taken days.

**Revision:** smarter proposals, with the counting balance corrected for them:
- merges pick among events that can actually merge;
- splits pick among real neighbours;
- link-removing flips pick from the list of places where one can happen.

The program now applies a change, works out the odds of reversing it, and keeps or undoes it.

**Result:**

| start | steps | failures | changes accepted | time per step |
|---|---|---|---|---|
| Flat | 20,000 | **0** | 20% | 0.4 ms |
| Crowded | 20,000 | **0** | 0.15% | 0.3 ms |

Every slice was structure-checked every 500 steps, its counts every step, and every tick replayed every 2,000 steps. All exact. **G2 passed.**

**A concern for later:** a history started from the crowded slice barely moves. Crowded slices have few events that can step back out, so most changes are refused.

## G3 (C28)

| | flat | crowded | gap | needed |
|---|---|---|---|---|
| **How distance grows with size** | 0.327 | 0.293 | **0.034** | 0.1 |
| **Spacetime reading, size 12** | 3.43 | 3.70 | **0.27** | 1.0 |
| **Spacetime reading, size 16** | 3.56 | 3.74 | **0.18** | 1.0 |

For comparison: flat space grows at about 0.33; attempt 9's small worlds grew at about **0.15**. **The crowded start grows at 0.29 — nearly flat.**

**Why:** the crowded start has to have exactly the same number of events and links as the flat reference (your C-Q2 and B-Q1). At ED's density, rewiring at random only goes so far, and pushing harder breaks the step that brings the link count back. **Attempt 9's strong small worlds all lost events** (down to about 83%), which pushed the links per event up to about 8. **With both counts held exactly, that route to crowding is closed.**

## What it might mean

**Two readings, and I can't tell yet which is right:**

1. **My construction is too weak.** A strongly crowded slice with ED's exact counts may exist and I just haven't built one.
2. **Holding both counts exactly may itself keep space from getting badly crowded.** If so, that's part of the answer: much of attempt 9's collapse came *with* losing events.

**Raising the sizes won't separate these.** The crowded start is nearly flat at every size.

## Options (you decide)

| | option | what it tells us |
|---|---|---|
| **(a)** | **Build a strongly crowded start with ED's exact counts another way:** grow one of attempt 9's small worlds from a slightly bigger grid so it shrinks to the right number of events, then bring its links to ED's count. **About an hour.** If it stays strongly crowded, the full stage B test can run as planned | Settles reading 1 against 2, and gives stage B its proper second start |
| **(b)** | **Run stage B from the flat start only:** does counting whole histories keep flat space flat, where growing forward drifted (note 13)? | A weaker test — it can't show counting *chooses* flat, only whether it *keeps* it |
| **(c)** | Follow the rule literally and raise the sizes | Won't help, for the reason above |

**Proposal: (a), then the full stage B run.**
