# Road E: taking stock, in plain language

*ED_Attempt_08, note 8. 2026-09-20 (RD14). Ledger: C38. Reasoning only; nothing computed. Written plainly, because the technical notes have got ahead of what can be read.*

## What road E was for

**Attempt 7 ended stuck.** ED had a rule for growing space, and the space it grew didn't look like space. But every test had been done on tiny patches — about 19 steps across — so nobody knew whether the rule was wrong or the patches were too small to see anything.

**Road E had one job: make the patches bigger and look again.**

## What it did

**1. Built a faster model.** About 7 times quicker, and it uses a fraction of the memory — so patches ten times bigger became affordable. It was checked three separate ways against attempt 7's original, including re-running the old code six extra times to be sure the new one behaved the same. It does.

**2. Killed its own main experiment after 47 minutes** — and found something better in the process.

**3. Ran the real question and answered it.**

## The four things road E found

### It found that ED cannot collapse

**The pattern physically cannot reach the "crumpled" state** — everything packed onto everything. ED's conserved link budget and its no-infinities rule each forbid it independently, and the arithmetic is simple enough to check by hand.

**Why that matters:** in the leading rival theory, the crumpled state is half of a transition that blocks them from getting smooth spacetime. **ED doesn't have it.** This is the first time "what CDT tunes, ED conserves" has produced a hard structural consequence instead of being a slogan.

### It found that ED's space changes character with distance

**How roomy ED's space feels depends on how far you look.** Close up (2–3 steps) it feels stringy, about 1.4. Further out it opens up, through 2, through 3, and beyond.

**Nobody had ever looked.** Every number attempts 7 and 8 had reported was a single measurement taken at one distance — and it happened to be **the exact distance where the space feels narrowest**. So "branched" was always the bottom of a curve, reported as though it were the whole answer.

**The leading rival theory reports the same running behaviour**, and it's one of their headline results. Finding it in ED is a real discovery about the model, even though it didn't rescue the answer.

### It found that bigger patches are a dead end — and this is the important one

**The rise turned out to be an illusion of running out of room**, not real large-scale space. The test was written down in advance: measure how far a walk can get before it fills the patch. If the space were genuinely three-dimensional, ten times the volume should let a walk reach **about twice as far**.

> **Ten times the volume bought 26% more reach.**

ED's patches are extraordinarily compact — volume packs in as though the space were roughly **ten-dimensional**. Flat space, measured identically, gives exactly three.

**And here is what closes the road:** at that rate, **doubling the reach would take about 943 times the volume.** One of today's biggest runs took an hour and a half. Nine hundred times that is not a computing problem you solve with patience or a better machine.

> **This question cannot be answered by making patches bigger. Ever. On this rule.**

### It found that sync is pushing the wrong way

**With the sync rule switched off, the space came out more three-dimensional, not less** — 2.32 against 1.64, and the most space-like number this project has produced.

Sync was introduced to be the thing that picks out three dimensions. As applied here, it was doing the opposite.

**Allen then decided what sync actually means** (D10): a **whole slice agreeing**, not a veto on one move at a time. Tracing the record, sync became a per-move veto through three modelling steps, **none of which was a decision**. So every three-dimensional growth run in attempts 7 and 8 was testing a local veto, not sync. Those runs aren't wasted — they're now correctly labelled.

## The verdict

> **ED's growth rule makes stringy, extremely compact patterns rather than space, at every size that can be reached — and bigger sizes are now ruled out as a way of changing that answer. Attempt 7's wall stands, and the route road E was built to try is closed.**

**But: 2.32 is not 3 either.** Switching sync off helped and didn't fix it. The other local rules — commitment and curvature — are still there, and they arrived the same way sync did.

## What it cost

| | |
|---|---|
| **Compute** | about **28 hours** of recorded run time, plus timing runs and the scale curves — roughly **35 hours** in total |
| **Ledger** | 37 claims, 10 of Allen's decisions, 13 recorded steps, 8 notes |
| **Claude's recorded errors** | **14 in code or specification**, all caught by a test or a guard before reaching a result — plus **one error of interpretation**, where the branched reading was reported as "clear and negative" before the measurement windows had been checked |

## Where ED stands now

**Nothing has been derived.** Inputs supplied: still **3**. No new number, nothing measurable.

**What still stands from attempt 7:** the balance coming out of a conserved budget, and the argument for three dimensions from clocks agreeing. Neither is about *growing* the pattern, so neither is touched by this.

**What is now known that wasn't:** ED cannot crumple; ED's space runs with scale; bigger patches cannot settle the shape; and the sync rule in the growth model was never sync.

## The three roads open

| | road | what it is |
|---|---|---|
| **1** | **Whole-slice sync** | Test sync as Allen has now defined it, instead of the per-move veto. The first road that tests ED's own meaning rather than a modelling convenience. Item 4 of attempt 7's carry-forward, never opened |
| **2** | **The local costs** | Commitment and curvature are local sums that arrived exactly the way sync did, and they are what remains when the veto is removed. They deserve the same examination |
| **3** | **Can a single grown history give smooth space at all?** | ED says growth is a process — one tick at a time, what happened stays happened. Every established approach gets smooth spacetime from a **sum over many possible histories**, not from growing one. This may be a genuine tension between two of ED's own meanings, and it is the deepest question on the table |

**Road 3 is a conversation, not a model.** It is for Allen, and it may decide whether roads 1 and 2 are worth running at all.
