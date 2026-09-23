# The ledger

A record of every statement the work relies on: what it is, how sure we are, and why. Nothing gets used, written up or published unless it is in here.

It has four parts:

| file | what it holds |
|---|---|
| [Claims.md](Claims.md) | Every claim, with a status and its evidence. |
| [Assumptions.md](Assumptions.md) | Every assumption, and the claims that use it. |
| [Log.md](Log.md) | A dated, append-only record of what happened: new claims, status changes, runs, corrections. |
| `checks.txt` and `run_checks.py` | The commands that back every PROVED or COMPUTED claim, run in one go. |

---

## Statuses

Only these seven. A claim gets exactly one.

| status | means | evidence required |
|---|---|---|
| **PROVED** | Follows by a written argument from nothing but mathematics. | The proof is written out where anyone can follow it. A check command where a numerical check is possible. |
| **COMPUTED** | A script produces it. | A command in `checks.txt` that passes. |
| **CITED** | Established by someone else. | A reference checked against the source itself (not memory, not an AI summary), with the link and the date checked. |
| **CONDITIONAL** | Proved, but only from inputs that include assumptions. | The proof, plus the assumption IDs it rests on. |
| **ASSUMED** | Taken as a starting point. | Only in [Assumptions.md](Assumptions.md), with what it is used for. |
| **OPEN** | Not known yet. | What would settle it. |
| **WITHDRAWN** | Turned out wrong or unsupported. | Why. It stays in the ledger, it is never deleted. |

These words are **not** statuses and don't get used for claims: *derived, forced, inevitable, confirmed, established by the framework.*

---

## Rules

1. **No claim is surer than its weakest input.** A claim that uses an ASSUMED item is at best CONDITIONAL.
2. **Anything an AI writes enters as OPEN.** It moves up only when a command passes or a source is checked. This includes everything Claude wrote.
3. **Citations are checked at the source.** Author, title, journal, and that the source actually says what we say it says. Record the link and the date.
4. **Every check runs from one command.** `python run_checks.py` must pass before anything is published or built on.
5. **The log is append-only.** Add a dated line for every new claim, status change, run and correction. Never edit or delete old lines. Corrections are new lines.
6. **Predictions are frozen before the run.** Write the prediction and its pass/fail criteria, log the date, then run.
7. **A human outside the work checks what matters.** The *Outside check* column in Claims.md stays empty until someone other than you and the AI has looked.

---

## How to add something

- **A claim:** give it the next C-number in Claims.md, set its status, fill in evidence and inputs, and add a log line.
- **An assumption:** give it the next number in Assumptions.md, say what uses it, and add a log line.
- **A check:** write the script so it exits with an error on failure, add a line to `checks.txt`, and run `python run_checks.py`.
- **A correction:** change the status (to WITHDRAWN if it was wrong), keep the old text, and log what changed and why.

---

## Gate: before anything is published, built on, or run as an experiment

Tick each one, and log the date.

- [ ] **Three questions.** Are the assumptions precise? Does a real calculation connect them to the claim? Could the claim have come out wrong?
- [ ] **Different rule.** Has the same analysis been run on a deliberately different rule, or a null model?
- [ ] **Generic?** Is the behaviour something almost any model shows (spreading, relaxation, oscillation, lock-in from reinforcement)?
- [ ] **Settings.** Does the finding depend on a number chosen in the code? If so, is that said?
- [ ] **Free parameters.** How many were fitted, and what would a boring alternative score?
- [ ] **Restating?** Is it known physics in new words, or a known answer matched after the fact?
- [ ] **Weakest input.** Is the stated status no higher than the weakest input allows?
- [ ] **Literature.** Has someone checked whether it is already known?
- [ ] **Checks pass.** `python run_checks.py`.
- [ ] **Outside reader.** Has someone outside the work looked?
