# The whole-history move: still frozen

*ED_Attempt_10, note 19. 2026-09-22 (RD20). Ledger: C32, D18. Code `model/sb_core.py` (global_step), `model/sb_g1_exact.py` (PG = 0.3), `model/sb_short.py` (PG = 0.3); outputs `model/sb_g1_exact_global.json`, `model/sb_short_global.txt`. Written plainly.*

## The short answer

**Still frozen.** Even with the new move, neither history went anywhere: the gap between them was 2.18 at the start and 2.19 at the end. **Stage B can't answer its question with this approach.**

## What was done

- **The whole-history move** applies the same change to every slice at once. It's allowed only where the change avoids every tick's recorded changes.
- **Checked exactly on rings first** (as G1): every move is exactly as likely as its reverse, all 25 histories are reached, and the weights are exact. **Passed.**
- **Small 3D check:** no failures.
- **Short-loop rerun** (4 slices, size 12, both starts, 1,000 passes), under the same pre-written outcomes.

## The results (C32)

| start | average distance, start → end | whole-history moves accepted |
|---|---|---|
| Flat | 5.84 → 5.81 | 20 |
| Crowded | 3.66 → 3.62 | 17 |

**Verdict: FROZEN.** No check failed. **My expectation ("partial at most") held.**

**Why:** almost all the whole-history moves got through in the first pass. After that, the ticks filled up with short-lived back-and-forth changes — which counting favours — and those cover about a fifth of every slice, blocking nearly every whole-history change.

## What stage B has shown, overall

1. **The tools are sound** — exact on rings, clean in 3D, able to tell flat from crowded.
2. **Under ED's rules, a counted history is dominated by brief back-and-forth changes in every tick,** while its large-scale shape barely moves. **Shape is extremely persistent.**
3. **Which shape counting prefers is still unanswered.** Every way I tried to move a whole history got stuck.

## Options (you decide)

| | option |
|---|---|
| **(a)** | **Take stock of road S and attempt 10** — what it found, what's settled, what's open |
| **(b)** | Keep trying to move whole histories (e.g., moves that carry a change *through* the ticks' recorded changes) — possible, but open-ended |

**Proposal: (a).** Road S has a lot to show, and the remaining question needs a different approach, not another push on this one.
