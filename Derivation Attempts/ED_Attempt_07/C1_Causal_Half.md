# Road C1: the causal half (on paper)

*ED_Attempt_07, note 2. 2026-09-16 (RD2). Ledger: C2–C5. Literature, reasoning and arithmetic; nothing computed. **Meaning questions C1-Q1–C1-Q4 and the draft exit rule are for Allen.***

## The question

**Does ED's causal growth, where space doesn't split, reproduce the known two-dimensional answer?**
- **What's given:** each slice of space is a line closed into a circle.
- **The known answer:** 2D causal dynamical triangulations (CDT).

**Why start here:**
- **It's a check of the machinery against an answer we already know,** before asking the harder question (C2: do sync and commitment make slices three-dimensional?).
- **If ED's causal rule can't reproduce 2D CDT,** something in the rule or the readings is wrong, and we find out cheaply.

## What's known (C2)

| | what it says | source |
|---|---|---|
| **Causal triangulations are trees** | Every 2D causal triangulation is built from a Galton–Watson tree: each point in one slice has some number of offspring in the next | Durhuus, Jonsson, Wheater; Krikun and Yambartsev |
| **The uniform case is critical** | For the uniform infinite causal triangulation, offspring have probability p(c) = (1/2)^(c+1): average exactly 1, the balance where space neither grows nor shrinks on average | Critical Lorentzian triangulation literature |
| **It must not die out** | A critical tree dies out almost surely, so the infinite triangulation is the tree **conditioned to survive**: Kesten's tree, one infinite spine whose points have "size-biased" offspring, with ordinary finite trees hanging off it | Kesten; Janson; conditioned Galton–Watson trees |
| **Dimension exactly 2** | The uniform infinite causal triangulation has fractal (Hausdorff) dimension exactly 2 | Sisko, Yambartsev, Zohren, *J. Stat. Phys.* (2013), arXiv:1203.2869 |
| **Spectral dimension at most 2** | Almost surely recurrent: spectral dimension ≤ 2, and exactly 2 for reduced versions | Durhuus, Jonsson, Wheater, *J. Stat. Phys.* (2010), arXiv:0908.3643 |

## On paper

### 1. ED's causal rule, with slices given (C3)

**Events and links, in ED's terms:**

| | rule | ED meaning behind it |
|---|---|---|
| **Slices** | Slice t is a circle of L_t events, each linked to its two neighbours in the slice. **Given as a circle for C1** | Space is a slice of the order (A6 D22). Slice dimension given, since C1 checks only the causal half |
| **Future links** | Each event x in slice t links forward to a run of **c_x + 1 consecutive events** in slice t+1. Neighbouring events **share exactly one** future event: the last of x's is the first of the next event's | Links point from earlier to later; growth only adds to the future (A6 D22) |
| **No splitting** | Because the runs follow each other around the circle, slice t+1 is again **one circle**, in the same cyclic order. Space doesn't split, merge, or reorder | A slice doesn't split or merge (A6 D22) |
| **How many** | c_x is random, independent, with p(c) = (1/2)^(c+1): average 1 | **The critical balance, put in for C1** (see §3) |
| **Survival** | One event per slice carries the spine: size-biased offspring, one child continuing the spine. So the pattern never ends | The universe doesn't stop (Kesten's tree) |

**Firm, by construction:**
- **Exactly one tree:** each event in slice t+1 has exactly one "first" past link, so parent links form a tree.
- **Slice length follows the tree:** L_{t+1} = Σ c_x over slice t.
- **Forward links:** the number of forward links out of slice t is Σ (c_x + 1) = **L_{t+1} + L_t**.
- **The order is strict:** every link points from slice t to slice t+1, so there are no loops back in time.

### 2. The known answer, as expected results (C4)

**For Kesten's tree with mean-1 offspring and offspring variance σ²,** expected generation size is exactly 1 + σ²·t.

**Arithmetic:** for p(c) = (1/2)^(c+1), the variance is (1−½)/(½)² = **2**.

| | expected | on what grounds |
|---|---|---|
| **Slice length** | Mean over seeds of L_t ≈ **1 + 2t**; fitted slope in **[1.8, 2.2]** | Kesten's tree, σ² = 2 (arithmetic) |
| **Mass dimension** of the spacetime pattern | **d_H in [1.7, 2.3]** | Exactly 2 (Sisko et al.); the range is the 2D calibration class from A6 |
| **Walk-return dimension** | **d_s ≤ 2.3** | At most 2 (Durhuus et al.), plus tolerance |
| **Walk dimension** | Reported. Expected **≥ 1.8,** since d_w = 2·d_H/d_s ≥ 2 when d_s ≤ 2 | Alexander–Orbach relation |
| **Structure** | Every slice one circle; order strict; forward links = L_{t+1} + L_t in every slice; parent links form one tree | By construction (§1): **exact** |

### 3. What C1 puts in, honestly (C4)

- **Slice dimension 1:** given, by design. C2 is where slice dimension has to come out.
- **Criticality** (average offspring exactly 1):
  - **This is the balance CDT gets by tuning a number** (its cosmological constant).
  - Too few offspring and space shrinks away; too many and it blows up.
  - **For C1 it's put in,** because the known answer needs it.
  - **What balances space's growth in ED is a real question for C2.** A natural candidate from attempt 6 is commitment's cost against sync's pull.
- **No cap on offspring:** every count is finite (a geometric distribution has all its moments), but it isn't bounded by a fixed number.
  - **A cap would change the known answer:** it lowers the average below 1, and space dies out.
  - "No infinities" (A4 D32) holds; "finite neighbours" holds as finite, not as a fixed cap. Flagged for C2.

## What it means (C4)

- **C1 is a machinery check, not new physics.**
- **If it passes:** ED's time order plus "space doesn't split" gives honest two-dimensional geometry once the slice is given, the same as 2D CDT. That confirms the causal half works in ED's terms before C2 asks for three.
- **If it fails:** the rule or the readings are wrong, and we fix them before C2.
- **Two things are put in and named:** slice dimension (by design) and the critical balance (C2's first question).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C1-Q1** | **For C1, is each slice of space given as a circle of events** (one space direction)? | **Yes** | C1 checks only the causal half; C2 is where slice dimension must come out |
| **C1-Q2** | **Does each event link forward to a run of consecutive events in the next slice, with neighbours sharing exactly one?** | **Yes** | The concrete form of "space doesn't split, and order within a slice is kept" |
| **C1-Q3** | **Is the number of new links random with average exactly 1** (space neither grows nor shrinks on average), **with one surviving spine so the pattern never ends?** | **Yes, as the known case, flagged as put in** | The known answer needs it; what balances growth in ED is C2's question |
| **C1-Q4** | **No fixed cap on forward links in C1:** every count finite, none bounded by a set number? | **Yes, flagged** | A cap changes the known answer; "no infinities" still holds |

## Draft exit rule (for the C1 model; Allen to confirm)

- **Pass:** every structural check exact, **and** slice-length slope in [1.8, 2.2], **and** d_H in [1.7, 2.3], **and** d_s ≤ 2.3. Record: **"C1: ED's causal growth with no splitting reproduces 2D CDT: the causal half checked."** Go to C2.
- **Structural check fails:** a code bug. Fix it (recorded), rerun.
- **Readings miss with structure exact:** first run a **flat causal calibration** (every event exactly one offspring, a regular strip with dimension 2 everywhere) through the same readings.
  - If the flat strip passes and the tree doesn't, record "C1 not reproduced" and look at why.
  - If the flat strip also misses, the readings need fixing for this kind of pattern. Record it, fix, rerun.
- **The growth rule is not changed after seeing results.** C1's rule is the known one.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide C1-Q1–C1-Q4** and confirm the exit rule | Fixes C1 |
| **(b)** | **Then specify the C1 model:** sizes, seeds, readings, timing, written before any code | A small model; readings timed first this time |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C2 | Durhuus, Jonsson, Wheater, arXiv:0908.3643 (listing); Krikun and Yambartsev, critical Lorentzian triangulation (listings); offspring p(c) = (1/2)^(c+1) for the uniform infinite causal triangulation (listings); Sisko, Yambartsev, Zohren, arXiv:1203.2869 (listing); Kesten's tree and conditioned Galton–Watson trees (arXiv:1304.4035; Janson, Springer and DMTCS listings) | 2026-09-16 |
| — | A4-ledger D32; A6-ledger C87, C89, D22 | Earlier ledgers |
