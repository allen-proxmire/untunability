# Event Density, attempt 7: the plain-language version (in progress)

*ED\_Attempt\_07. Written 2026-09-16 (RD20), after road C's first stock-take (note 11). For a reader who hasn't followed the work. Every claim points to the ledger (`01\_Ledger/`); the notes carry the details. Earlier write-up:* [*attempt 6*](../ED_Attempt_06/Attempt_06_Plain_Language.md)*. The cross-attempt inputs table is* [*What\_ED\_Needs.md*](../What_ED_Needs.md)*.*

## 

## What attempt 7 is for



**Attempt 6 ended at one precise open problem** (A6 C88): grow ED's pattern step by step, with finite neighbours, where space never splits or merges, and have sync and commitment make space three-dimensional.



* **Growing space without time order** gave rings, rough tangles, stalls and small worlds.
* **The literature pointed to the missing piece:** in growth models, causality (space not branching in time) is what separates smooth geometry from fractal geometry.



**Attempt 7 takes that problem on as road C, causal growth.** It keeps the same habits:



* **Allen decides what ED means.** Claude proposes the least-structure default, and nothing is decided until Allen says so.
* **Expected results come first.** Every model has its expected results and exit rule written before any code.
* **Revise and retest is the normal workflow.** Every miss, revision and correction is recorded.



**Working names** (Allen, D15; labels, not renamings):



* **Commitment Dynamics:** the framework as it now stands.
* **Budgeted Causality:** the balance result.
* **Synced Now:** the three-dimensions result.



**The verdict labels used below:**

* **Pass:** a model met its expected results, fixed in advance.
* **Consistent, not derived:** ED can say it without contradicting known physics, but something is still put in, or the answer was known.

## 

## 1\. The causal half: ED's growth reproduces a known answer (C1, notes 2–4)



**The picture:**



* **Space at each tick is a slice of events,** here given as a circle.
* **Each event links forward** to a run of events in the next slice, and neighbouring events share exactly one future event. So the slice never splits, merges or reorders.
* **Each event's number of children is random,** averaging exactly one.



**The known answer:** this is two-dimensional causal dynamical triangulations (CDT). Mathematically it's a random tree, and its answers are known exactly: slice length grows like 1 + 2t, and the spacetime is two-dimensional.



**The model** (C8): slice length slope **2.05**, mass dimension **2.17**, walk-return dimension **1.89**, structure exact. **Pass.**



**What it shows:** ED's causal growth, with no splitting, gives smooth geometry. The average of exactly one child was **put in**, as CDT tunes its cosmological constant.

## 

## 2\. The balance: Budgeted Causality (C2a, notes 5–7)



**Why the balance matters** (C10):



* fewer than one child on average and space dies;
* more than one and it grows exponentially into a hyperbolic shape with no dimension;
* exactly one gives smooth geometry.



The real universe sits at the balance to about one part in 10⁶¹.



**ED's candidate:** each event has a **budget.**



* **The naive reading** (links held use up budget) pushes *away* from the balance. It ran away in every run (C14, C16).
* 
* **Budget passed forward and conserved:** each event splits its budget over its forward links, and new events sum what arrives. This pulls *toward* the balance (C14).



**The model:** slices held at their target size in every seed, and the geometry stayed two-dimensional (C16).



**The one miss was the average itself.** The average of each tick's growth ratio reads high whenever sizes swing.



* **Allen saw that it's the same as his prime-triangle angles** (D8): measure growth as a log-ratio and the ups and downs cancel.
* **Measured that way,** the offspring average is 1.000 in every setting (C17).
* **The measure was adopted and retested on fresh seeds** (C19, C31): **pass.**

**Recorded:**



> \*\*"The balance self-organizes from ED's budget passed forward and conserved: consistent, not derived; k and L\\\* are knobs; space settles as a fixed-size tube, and growth would need budget creation (the cosmic excess, inherited)."\*\*



**Prior art:** Cortês and Smolin's energetic causal sets also conserve quantities along causal links (C37).



## 3\. Three dimensions: Synced Now (C2b, notes 8–10)



**The idea** (C22):



* **Clocks at different places tick at slightly different rates,** and neighbours pull each other into line, but only so much.
* **"Now" is where the clocks read the same.** It wobbles.
* **If the wobble tilts "now" as steeply as influence travels,** "now" folds into time: one "now" event could sit in another's past.



**How the tilt grows with region size depends on the slice's dimension:**



|slice dimension|the tilt of "now"|a real "now" at large scales?|
|-|-|-|
|**1**|grows|no|
|**2**|holds, at a value set by a ratio|only with a tuned ratio|
|**3**|shrinks|**yes, with nothing tuned**|



* **Sync needs three or more dimensions, and commitment favours the fewest directions,** so three.
* **This only works if each place's rate persists** (Allen, C2-Q5). If rates were redrawn every tick, every dimension would keep a "now."



**The model** (slices given as 1-, 2- and 3-dimensional grids and random slices, with a fresh-rate control) took **three runs:**



* **Run 1** (C32): two 1D runs left the regime where the calculation applies.
* **Run 2** (C34): the exponents missed at the edges of their ranges, because the median of each seed's slope is noisy in 1D.

  * The exact answer, worked out with no simulation, confirmed the physics (C35).
  * **Wobbles add as squares, so they should be averaged that way:** Allen's averaging lesson again.
* **Run 3** (C38), on fresh seeds with the fixes: **pass.** Wobble exponents 1.54, 1.02, 0.42 on grids (exact: 1.50, 0.99, 0.47) and 1.68, 0.96, 0.54 on random slices. The tilt grows, holds and shrinks, and fresh rates keep a "now" everywhere.



**Recorded:**

> \*\*"A common now needs slice dimension ≥ 3 without a ratio in ED's causal pattern; with commitment's fewest directions and whole numbers, three: consistent, not derived."\*\*



**A side result on the rest frame** (C28, all three runs): in 3D, the local "nows" scatter up close and line up with distance. **One large-scale rest frame comes out of sync,** rather than being imposed by a grid.

## 

## Where attempt 7 stands (note 11)



||road C|status|
|-|-|-|
|**C1**|Causal growth without splitting is smooth|Pass|
|**C2a**|Budgeted Causality: the balance from budget|Pass, retested|
|**C2b**|Synced Now: three from sync and commitment|Pass on run 3|
|**C3**|**Growing a slice with more than one dimension**|Started on paper|



**Inputs supplied: 3** (unchanged: the Born rule in form, horizon entropy's area law, one time dimension). Three space dimensions now has three consistent reasons: lasting kinds (attempt 4), rates able to match (attempt 6), and a synced "now" in the causal pattern (attempt 7).

## 

## Honest limits



* **Consistent, not derived.** No input has been removed.
* **C1 and C2b confirm known mathematics inside ED's setting.** What's ED's own is the readings (budget passed forward, sync as a "now," persistent rates) and how they fit together.
* **Still put in:**

  * slices given, not grown;
  * whole-number dimension;
  * commitment's push toward the fewest directions, not modelled;
  * the knobs k, L\*, K, σ;
  * strong coupling only.
* **No number and no observable difference** from standard physics yet.
* **Revisions made along the way** (all recorded): two changes to how to average, one regime fix, one harness fix, and one chart shown with wrong points and corrected.

## 

## Words used here



|word|meaning here|
|-|-|
|**Slice**|All the events at one tick: space at a moment|
|**Offspring**|The events an event links forward to that are new|
|**Budget**|What an event passes forward, split over its links and conserved|
|**Balance**|Offspring averaging exactly one|
|**Wobble**|How much clock readings differ across a region|
|**Tilt**|Wobble divided by distance; "now" folds into time if it reaches one hop per tick|
|**Persistent rate**|A place's clock keeps its own slight rate from tick to tick|



