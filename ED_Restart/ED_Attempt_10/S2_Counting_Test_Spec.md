# S2: the counting test, on paper

*ED_Attempt_10, note 3. 2026-09-21 (RD3). Ledger: C6, C7, D3. Specification only; nothing computed. Written plainly; the technical detail is in the box at the end and in C7.*

## What you decided (D3)

- **S1-Q1, yes:** ED's rule is a list of what's allowed, and every allowed history counts once. A present is weighed by how many histories could have led to it.
- **S1-Q2, yes:** links join only events in the same slice or the next one.

## A warning I found while writing this (C6)

Writing the spec turned up a real risk, and you should hear it before anything is built.

**Counting rewards whatever has the most ways to happen.** In ED, an event with many neighbours has many more ways to split than an event with few — roughly the square of its neighbour count. So a slice with some very crowded events (hubs) has more possible next steps, and more possible last steps, than a flat slice where every event has about the same number of neighbours. **Counted that way, the count could lean *toward* crammed shapes, not away from them.** There's a known result that counting paths does exactly this on networks: it piles up where the options are densest (Burda et al., the "maximal entropy random walk").

**Why CDT might still work and ED might not:** in CDT, the slice-to-slice step is a whole layer that can be filled in many ways, and the counting is of those layers. In ED, the step is simpler: each event has a parent, and the next slice is the last one with a few splits and merges. **That difference may matter.** I can't tell on paper which way ED's counting leans.

**So I've split the test in two**: a cheap check of which way counting leans (hours), before the expensive test (days).

## Stage A: which way does counting lean? (under an hour)

**What it does:** take slices of different shapes and count, for each, **how many different ways it could have come from the previous tick** — the number of one-tick histories leading into it. Compare flat slices with crammed ones.

**The slices:**

| | 3D slices (13,824 events) | 2D slices (6,400 events) |
|---|---|---|
| **Flat** | the flat cube grid | the flat grid |
| **Flat, rewired** | flat with random paired flips | attempt 7's randomized surface |
| **Collapsed from flat** | grown as attempt 9's F1, 150 ticks (2 seeds) | grown as attempt 7's uniform rule (2 seeds) |
| **Small world** | grown as attempt 9's W1 (2 seeds) | grown as attempt 7's Q1 rule (2 seeds) |

**The reading:** the count of one-tick histories per event. The difference from flat, times the number of events, is how strongly counting prefers or disfavours each shape. **This preference grows with the slice by construction** — exactly the kind attempt 9 said was missing (A9 C41). The question is its direction.

**Expected results, fixed now:**

| | expectation | confidence |
|---|---|---|
| **A0** | The counting code matches a brute-force count (try every change, keep the valid ones) exactly on small slices, 2D and 3D | High — it's a code check |
| **A1** | Grown slices pass the structure and budget checks exactly; flat slices give the same count every time | High |
| **A2** | **My honest expectation: counting leans toward the crammed and rewired slices,** because crowded events have more ways to split | Low |

**What happens next, fixed now:**

| if | then |
|---|---|
| A0 or A1 fails | A code problem; fix it and rerun, recorded |
| **Flat has the higher count** in 3D, beyond the spread between seeds | **Counting leans toward flat.** Go on to stage B |
| **Crammed has the higher count** in 3D, beyond the spread | **Record: "with ED's slice-to-slice step, counting leans toward small worlds."** Stage B isn't built. Take stock on paper of what joins one slice to the next — ED's one-parent step versus CDT's layers — as a question for you |
| Too close to call | Build stage B small, in 2D only, and let it decide |

**Limit, labelled:** one tick back isn't the full history count. It's the first factor of it, and it tells the direction, not the final answer.

## Stage B: count whole histories (days; only if stage A allows)

**What it does:** a program that visits whole ED spacetimes — a stack of slices joined by parent links — each allowed one equally often. Then read the spacetime with the calibrated readings, as attempt 7 decided.

**Calibrations first, as a gate:**
- **Rings as slices.** With 1D slices, ED's counting is exactly the same count as 2D CDT, which is solved exactly and gives a two-dimensional spacetime. The program has to reproduce that before anything else runs.
- **Flat stacks.** The spacetime reading on a stack of flat 2D slices, calibrated as attempt 9 did for 3D (flat reads 3.61–3.67 there, not 4).

**Then:**
1. 2D slices.
2. 3D slices, if 2D is clean.

**Pass, fixed now:**
- **The spacetime reads within 0.5 of its flat calibration.**
- **The slices aren't small worlds:** mean distance grows with size close to the flat rate.
- **The result is the same from a flat start and from a small-world start.** That's the decisive part: counting would be *choosing* flat, not just keeping it.

B's full expected results, sizes and cost are written in its own spec before any code, once stage A has run.

## Questions for you (defaults proposed)

| | question | default | why |
|---|---|---|---|
| **C-Q1** | **What counts as one history is the spacetime itself** — the events, their links and their parents. Making the same changes in a different order isn't a new history | **Yes** | Least structure; it's how CDT counts |
| **C-Q2** | **Every slice has exactly the same number of events** (the budget passed forward and conserved) | **Yes** | The simplest form of Budgeted Causality for counting; the test is about shape, not size |
| **C-Q3** | **"Mostly one child" means each tick changes at most 10% of events** — splits, merges and paired flips all count | **Yes** | A9 D11, with its 10% carried as a labelled setting; keeps slices persistent |
| **C-Q4** | For stage B only: **time loops round** (the last slice joins the first), so no slice is special | **Yes** | A sampling convenience CDT uses; labelled as a technical choice, not a meaning |

## Options (you decide)

| | option | why |
|---|---|---|
| **(a)** | **Decide C-Q1 to C-Q4 and run stage A** | Under an hour; tells us whether the days of stage B are worth spending |
| **(b)** | Skip A and build B | Gives the full answer, but may spend days on a test that leans the wrong way |
| **(c)** | Talk through the warning first | It may say something about what joins one slice to the next |

**Proposal: (a).**

---

### Technical box (for the record)

- **Stage A count.** For a slice S with V events and m = round(0.1·V) changes per tick (C-Q3), the number of allowed single changes is a_v per event: split pairs passing ED's split rule, collapses passing the link condition, and the paired-flip sites involving v, apportioned per site.
- **One-tick history count.** Approximated by n(S) = e_m(a_1, …, a_V), the elementary symmetric polynomial, which counts unordered sets of m changes at distinct events and so follows C-Q1. It's computed in log space by the standard O(V·m) recursion.
  - It ignores conflicts between changes at neighbouring events. That's labelled, and the brute-force comparison in A0 is done on single changes.
  - The move set is its own inverse (a split undoes a collapse, and a flip pair undoes a flip pair), so histories into S and out of S have the same count. Both are reported as a check.
- **Reported per slice:**
  - s(S) = ln n(S) / V;
  - Δs against flat, and V·Δs;
  - the mean and spread of a_v, the degree spread, and the mean distance (to confirm the shape).
- **Seeds:** grown slices use seeds 0 and 1; "beyond the spread" means the gap exceeds twice the difference between seeds.
- **Code:** 3D uses attempt 8's port and attempt 9's p9.py; 2D uses attempt 7's c3a.py.
- **Cost:** the 3D growth is about 13 minutes on 4 workers, as in H4; the 2D growth about 20 minutes at n = 80; counting takes minutes.
- **Literature:** Burda, Duda, Luck, Waclaw, "Localization of the maximal entropy random walk", PRL 102, 160602 (2009) ([arXiv:0810.4113](https://arxiv.org/abs/0810.4113)): uniformly counted paths localize in the regions of a network with the most options. 2D CDT's strip count between rings of lengths l and l′ is the binomial C(l + l′ − 1, l − 1), the same as the number of ways l events can have l′ children in total, which is the basis of the ring calibration ([Ambjørn–Loll, hep-th/9805108](https://arxiv.org/abs/hep-th/9805108)).
