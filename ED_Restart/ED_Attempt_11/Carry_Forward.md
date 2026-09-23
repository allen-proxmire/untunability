# What attempt 10 hands to attempt 11

*ED_Attempt_11, note 1. 2026-09-22 (RD1). Ledger: C1. A summary of A10-ledger C33, C34 and RD22; nothing tested. Written plainly.*

## What we've learned, attempts 7 to 10, in one page

| attempt | the question | what we learned |
|---|---|---|
| **7** | Can ED grow a 3D slice? | Growth makes crammed "small worlds", not spread-out space. **A conserved budget sets the size** (Budgeted Causality) — a real result |
| **8** | Is it just the patch size? | No — it's the growth rule. **ED can't crumple** into one lump |
| **9** | Is the *kind* of rule right? | Costs push the wrong way; conditions work. Without costs, slices feel 3D up close for the first time. **But nothing in ED's growth prefers spread-out space**, and crammed shapes win by sheer number |
| **10** | Where could that preference come from? | **Not from a new conserved quantity** — there's none left. **From counting histories** — and which way counting pushes **depends on what can happen in one tick.** With narrow moves (an event appears on a link, and leaves by stepping back out), **counting pushes toward flat, one tick at a time** — the first time ED's own rules have leaned toward flat with nothing tuned. Over whole histories: untested, because **under ED's rules, shape barely moves at all** |

**The thread:** each attempt removed a wrong answer and narrowed the question. **It now sits on something that's yours to decide: what exactly happens in one tick** — how one slice becomes the next.

## Decided in attempt 10, carried

| | meaning | A10 source |
|---|---|---|
| **The rule** | A list of what's allowed; **every allowed history counts once** | D3 |
| **Links** | Only within a slice or to the next | D3 |
| **A history** | The spacetime itself — events, links, parents | D4 |
| **Counts** | Every slice keeps exactly its number of events and links | D4, D8 |
| **Each tick** | At most 10% of events change; changes at separate places | D4, D8 |
| **Moves** | **Narrow both ways** | D14 |

**Flagged, not decided:** whether a single flip may ride in a link-balanced bundle (A10 D15).

## Results that stand

- **Budgeted Causality** — now covering both of a slice's totals: *what CDT tunes, ED conserves.*
- **Synced Now.**
- **ED can't crumple.**
- **Narrow moves make counting lean toward flat, per tick** (A10 C22).
- **Under ED's rules, a history's large-scale shape is extremely persistent** (A10 C30–C32).

**Inputs supplied: still 3.** Nothing derived.

## Tools

- **The history-counting program** (`../ED_Attempt_10/model/sb_core.py`, `sb_3d.py`) — exact on rings, clean in 3D.
- **Narrow-move growth** (`p10.py`).
- **Flat and crowded starts at ED's exact counts** (`sb_build.py`).
- **The one-tick counters** (`sa_count.py`, `sa2_count.py`, `sa3_count.py`).

## Lessons

- **A start that stays put may only mean nothing moved** — it bit twice more in attempt 10.
- **Check that the moves undo each other before counting** (A10 C17).
- **New for attempt 11: a picture before every test.** Before anything runs, a short plain paragraph: what's being built, what flat and crammed would look like, and what each outcome would mean for ED.

## The opening road

| | road | the question |
|---|---|---|
| **L** | **What is one tick?** | Right now, each event passes on to mostly one child, in the same place. In the rival theory, one slice joins the next through **a whole layer**: each event reaches forward to **a patch** of the next slice, and a slice's shape is weighed by how many ways that layer can be filled. **Should ED's "passing on" work like that?** |

**On paper first,** in pictures, with you. It's a question about what passing on means, so it's in your territory, not the program's.

**Carried, not opened:** whole-history counting with narrow moves (the tools are ready if a faster way to move histories turns up); amplitudes; roads R, I and D.
