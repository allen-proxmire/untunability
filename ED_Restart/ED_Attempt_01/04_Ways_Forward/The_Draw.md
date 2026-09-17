# The draw: what's loose, and what "can't be brought back" could mean

*2026-09-14. Started under G51 = (c), RD49. Ledger: G36, RD22, RD26–RD28, RD31, C114, C117, C120–C125, C143, D10, D17, C284–C287, G52.*

## 1. What ED says a draw is

**Allen's picture (D10).** Measurement is a pattern meeting a committed part of the world and being forced to commit.

**The rules so far.**
- **No draw from spreading alone (RD26).** A lone pattern stays spread.
- **Meetings don't draw by themselves (RD27).** Patterns that meet hinge into one pattern.
- **A draw happens when a meeting leaves a mark that can no longer be brought back together (RD28).** Only what the mark distinguishes is fixed, and only for the part that interacts (RD22).
- **What "can no longer be brought back" means exactly is open (G36).**

## 2. What's loose (C286)

You said the draw description seemed loose (D17). It is, in six places.

| | what | how the models handled it |
|---|---|---|
| 1 | **When** a mark counts as unrecoverable | Never defined. Version 1 used a "detector" as an input; versions 2 and 2b used a draw rate Γ, which is a free number |
| 2 | **What** a draw fixes | RD28 says only what the mark distinguishes. The models instead fixed a locus and channel (v1, v2) or dropped a lane into Internal (v2b) |
| 3 | **Where the mark goes** | Never tracked. The environment has no state, so nothing checks that the mark's content is conserved |
| 4 | **The probabilities** | The usual quantum rule (amount squared) is assumed, not derived |
| 5 | **Draws as rates** | ED says a draw happens at a moment, when the mark becomes unrecoverable, not at a steady rate |
| 6 | **The budget** | Whether a draw uses budget, and how much, is unspecified |

**Why it matters.** Versions 2 and 2b rested on items 1, 2, 3 and 5, and their results depended on those choices (C275, C278, C283).

## 3. Candidate exact meanings of "can't be brought back"

**(i) The horizon meaning.** A mark can't be brought back once part of it has left the reach of every future path.
- **It is number-free.**
- **ED's space now has such a horizon.** Constant births (RD43) make space grow like our universe with constant dark energy, which has a permanent event horizon.
- **Published home:** Bousso and Susskind use the causal-diamond horizon as a one-way membrane that fixes the environment (C120). Danielson, Satishchandran and Wald show any Killing horizon, including a cosmological one, eventually decoheres a spatial superposition by carrying "which-path" information across (C284).
- **The catch (C143, now sharper).** A permanent horizon has a finite capacity, about 10¹²² (C272, C273). Within a finite capacity, decoherence isn't completely irreversible (C120). So draws would be exact only for the life of the horizon, not absolutely. That is **the same 10¹²² you raised** (C274), now setting how exact a draw can be. RD31's aim of exact draws would become "exact up to the horizon's capacity".
- **Timing.** Everyday outcomes look settled almost at once, because records spread fast. The horizon crossing that makes them final comes much later. No experiment can tell the difference.

**(ii) The redundancy meaning.** A mark can't be brought back once it has been copied into enough independent pieces that recovering it would mean gathering them all.
- **Published home:** Zurek's quantum Darwinism, where objective records are redundant copies spread through the environment (C285).
- **Timing matches the lab:** redundancy builds fast.
- **The catch:** it needs a threshold ("enough copies"), which is a number we'd have to pick. It is exact only in the limit.

**(iii) The budget meaning.** A draw happens when the mark uses budget, since used budget can't be returned (P11).
- **The catch:** earlier checks rejected the obvious forms. Every meeting drawing contradicts experiments (C114), and a full-budget trigger only happens near black holes (C117). It would need a restriction that isn't in ED.

## 4. Proposal (G52)

| | option | assessment |
|---|---|---|
| **(a)** | **Horizon meaning** as what "can't be brought back" is | Number-free; fits constant births; exact up to the horizon's capacity (10¹²²). No new rule |
| **(b)** | **Redundancy meaning** | Right timing; needs a chosen threshold |
| **(c)** | **Budget meaning** | Probably fails (C114, C117) |
| **(d)** | **(a) as the meaning, (b) as the working model in simulations** | **Proposal.** The ontology stays number-free. Simulations get a practical stand-in whose threshold is openly a modelling choice, not part of ED |

**If (d) is chosen, first steps:**
1. **Revise RD31:** exact draws become "exact up to the horizon's capacity".
2. **Settle what a draw fixes (item 2):** what the mark distinguishes, not a locus and channel by default.
3. **Give the environment a state (item 3),** so the mark's content is tracked.
4. **Rebuild the draw in version 1's rule** with frozen predictions, and check it still reproduces the known eraser and interference results.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C284 | Danielson, Satishchandran, Wald, "Black holes decohere quantum superpositions", *IJMPD* 31, 2241003 (2022), arXiv:2205.06279; "Killing horizons decohere quantum superpositions", *PRD* 108, 025007 (2023) | Search listings |
| C285 | Riedel, Zurek, Zwolak, "The rise and fall of redundancy in decoherence and quantum Darwinism", *New J. Phys.* 14, 083010 (2012), arXiv:1205.3197; experimental redundancy tests (Quanta Magazine report, 2019) | Search listings |
| C120 | Bousso and Susskind, *PRD* 85, 045007 (2012) | Abstract (checked 2026-09-13) |

## 5. Built (2026-09-14)

**The draw is rebuilt** ([Commitment_Rule/v3_draw/Results.md](Commitment_Rule/v3_draw/Results.md), C291).
- **All ten frozen predictions right.**
- **Three of the six loose points are now settled:** when (a stand-in for the horizon meaning), what (only the record) and where the mark goes (the environment's state).
- **It reproduces** the partial-mark and eraser results, keeps coherence inside the record, and doesn't signal.

**Still open:** probabilities, budget, and the stand-in's erasure limit (C292). **Next:** G53.
