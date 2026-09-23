# ED_Attempt_01

**Event Density, attempt 1: concluded 2026-09-14 under its exit rule.**

This folder holds the whole first attempt to turn Event Density (ED) from a picture into a definite, runnable rule and test it: every claim, decision, script and write-up. It was worked on under the name "ED restart"; some old output files and log lines still mention that path.

## Start here

| if you want | read |
|---|---|
| The short version, no physics background needed | [06_Write_Up/ED_Plain_Language.md](06_Write_Up/ED_Plain_Language.md) |
| What the terms mean (draw, commitment, budget, exit rule, …) | [06_Write_Up/Definitions.md](06_Write_Up/Definitions.md) |
| The full write-up, with ledger references | [06_Write_Up/ED_Interpretation_Draft2.md](06_Write_Up/ED_Interpretation_Draft2.md) |
| A one-page summary of the ledger | [Stock_Take.md](Stock_Take.md) |
| Which choices were solid or shaky, and why | [Audit.md](Audit.md) |

## Where it ended

- **Where the rule matches physics:** ED's rule reproduces known physics where it was checked. That covers quantum interference and the eraser, no faster-than-light signalling, general relativity at the orders checked, and a constant dark energy. Each match was reached by fitting the rule to existing measurements.
- **ED's own contributions:**
  - a proved handedness theorem (mirror-symmetric rules can't have handedness written into them);
  - a physical account of when a measurement becomes final (a mark beyond the reach of every future path);
  - a documented record of what didn't work.
- **Handedness in ED's own rule:** a hand chosen by chance appears only with three ingredients ED doesn't supply. Three attempts to make ED supply the key one failed, so under the exit rule agreed in advance, ED is written up as an interpretation.
- **The outside-review packet** in `05_Outside_Review` is on hold (D20).

## Layout

| folder or file | what's in it |
|---|---|
| [00_Rules](00_Rules/README.md) | The working rules the attempt followed |
| [01_Ledger](01_Ledger/README.md) | Every claim (301) with its status and evidence, the rule decisions (RD1–RD55) and definitions (D1–D20), a dated log, and 36 checks that rerun with one command |
| [02_Result_Handedness](02_Result_Handedness/README.md) | A frozen copy of the public handedness result at commit `5690a59` (the same content as this repository's root) |
| [03_Philosophy](03_Philosophy/) | Philosophy notes, including the uniformity note (D16). Some references are unchecked (C19) |
| [04_Ways_Forward](04_Ways_Forward/) | The working notes and all rule code. `Commitment_Rule/` holds versions v0, v1, v1_budget, v2, v2b, v3_draw (the rebuilt draw) and v4; `Standing_Phase/` holds the three final attempts; the topic notes cover measurement, locus birth, dark energy, gravity checks and handedness |
| [05_Outside_Review](05_Outside_Review/) | A review packet for the handedness theorem, on hold |
| [06_Write_Up](06_Write_Up/README.md) | The write-up, plain-language version and definitions |
| [Stock_Take.md](Stock_Take.md), [Audit.md](Audit.md) | Summary and audit of the whole attempt |

## Rerunning the work

```bash
cd 01_Ledger
python run_checks.py
```

This needs Python with numpy and scipy. Some checks take several minutes. Each script states what it tests, and each has a section recording any changes made after it was first run.

## How the attempt was run

- **Ledger first.** Every claim entered the ledger with a status, and every decision was recorded with its options and reasons.
- **Tests before results.** Tests were specified before running, and every failure was recorded, including mistakes in the test code.
- **Literature before claims.** Published work was checked before claiming anything, with sources marked by how they were checked.
- **Tuned settings labelled.** Settings chosen to make something work are marked as tuned.
- **An exit rule agreed in advance** (RD52) and applied (RD55).

The full history is in [01_Ledger/Log.md](01_Ledger/Log.md).
