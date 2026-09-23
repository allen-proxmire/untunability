# Eight seeds: the negative holds, the positive does not

*ED_Attempt_13, note 9. 2026-09-23 (RD9). Ledger: C11. Code `model/s_solid.py`, output `model/s_solid.txt`, data `model/e_runs/solid.json`. Expectations S1–S4 fixed in the file before it ran. Written plainly.*

## What I have to take back

An hour ago, on three seeds, I reported two things:

1. **the negative** — a pattern with no dimension never acquires one;
2. **the positive** — in the thick regime, ED's rules preserve a dimension exactly.

**The negative holds. The positive does not.**

## The numbers

Eight seeds, two size ranges (about 8,000 and about 16,000 events), thickness 25:

| start | definite readings, at 8,000 | at 16,000 | gap ratios |
|---|---|---|---|
| **ring** | **8 of 8**, all 1.0 | **8 of 8**, all 1.0 | 3.4–3.9 |
| **cubic torus** | **1 of 8** | **1 of 8** | 1.47–1.68 |
| **random web** | **0 of 8** | **0 of 8** | 1.00–1.01 |

| | expectation | result |
|---|---|---|
| **S1** | ring reads 1 in at least 7 of 8, at both sizes | **Passed.** 16 of 16, with the cleanest gaps in the whole project |
| **S2** | cubic torus reads 3 in at least 5 of 8, at both sizes | **Failed, badly.** 1 of 8 at each size |
| **S3** | web reads nothing definite, 8 of 8, at both sizes | **Passed.** 16 of 16 |

## Why the earlier number was wrong

C10 reported "exactly 3 in five of nine runs". Those nine were **three seeds at three thicknesses** — so a seed that worked tended to work at every thickness, and a seed that didn't, didn't. It was really about two seeds of three, counted nine ways. **Eight independent seeds give one of eight.**

That is the difference between a result and an artefact of counting, and it is exactly what this run existed to find.

## What actually survives

1. **A line is preserved perfectly.** 16 runs of 16, reading exactly 1, with gap ratios of 3.4–3.9 — the cleanest signal anywhere in this project. ED's rules carry one-dimensionality without degrading it.
2. **Nothing creates a dimension.** 16 runs of 16 from a random web, no definite reading, gap ratios of 1.00–1.01 — no structure at all.
3. **A three-dimensional start is NOT preserved cleanly.** It mostly loses its signature: the modes still cluster into six at the looser tolerances, but the grouping is no longer sharp, and under a rule fixed in advance it fails seven times out of eight.

## What that changes

**"ED's rules carry a dimension" is too strong.** The honest version:

> **ED's rules carry one dimension perfectly, degrade three, and create none.**

The asymmetry is itself interesting and was not visible before: the structure ED preserves best is the one that can't hold its clocks together (a line fails the sync condition), and the structure it degrades is the one that can. **ED's growth is hardest on exactly the shape the project wants.**

I don't have an explanation for that, and I'm not going to invent one.

## Recorded

- **C10's negative stands**, now on 16 runs instead of 9.
- **C10's positive is withdrawn.** The claim that the thick regime preserves a dimension exactly rested on correlated seeds.
- The rule that caught it was written before the run, and the run was proposed before the numbers were known.
