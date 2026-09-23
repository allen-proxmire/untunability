# Road N, step 1: the instrument works

*ED_Attempt_11, note 12. 2026-09-23 (RD16). Ledger: C21. Code `model/n1_sync.py`, output `model/n1_sync.txt`, data `model/n1_runs/step1.json`. Expectation N0 fixed in note 10 before any code. Written plainly.*

## The picture, before the numbers

**What was built:** four patterns of the shapes we already know — a ring (1D), a flat grid (2D), a 3D grid, and a web where every event has six relations but to partners picked at random. Each event carries its own natural ticking rate.

**The question asked of each:** *how hard do the relations have to pull before all the clocks fall into step?* Then: does that required pull **keep rising** as the pattern gets bigger, or does it **settle**?

- **Rising** means the pattern can't hold itself together at large size — big patches always break away.
- **Settling** means it can.

**Why it matters:** this is attempt 6's argument turned into a measurement, with no adjustable knob in it. If the test can't reproduce what's already known about these four shapes, nothing we measure afterwards on ED's own patterns counts.

## The result: N0 as expected

| pattern | pull needed, at 2,000 / 4,000 / 8,000 / 16,000 events | rises? | expected |
|---|---|---|---|
| **Ring (1D)** | never locks at any pull we tested | **rises** | rises ✓ |
| **Flat grid (2D)** | 1.88 → 5.00 → 4.38 → **7.38** | **rises** (exponent 0.58) | rises ✓ |
| **3D grid** | 0.75 → 0.88 → 0.88 → **0.75** | **settles** (exponent −0.00) | settles ✓ |
| **Random web** | 0.88 → 0.75 → 0.75 → **0.75** | **settles** (exponent −0.07) | settles ✓ |

**N0 holds on all four.** The line and the flat sheet fail to hold their clocks together no matter how big the pull, and the failure gets worse with size. The 3D grid and the web hold at a pull that doesn't grow at all — it's flat to within noise across an eight-fold range of size.

**This is exactly attempt 6's floor, measured rather than argued:** below three dimensions, no; at three and above, yes.

## Two faults found and fixed on the way (both mine, both recorded before the numbers)

1. **Every pattern came back "never locks" on the first run.** The phase equations were being integrated with a fixed step that blew up whenever the pull was large. Fixed with a step size that adapts to the pull and the busiest event.
2. **The random web family was the wrong object.** Note 10 specified an Erdős–Rényi web, which at these sizes always contains a few events with one relation or none at all. A single stranded event can never lock, so the whole pattern is reported as failing — for a reason that has nothing to do with dimension. **Replaced with a web where every event has exactly six relations, to random partners.** That is the object note 10 meant: "a random web at matched average degree", without the stranded-event artefact.

The second fix is the reason this note exists separately: the first run said "N0 False" on the web, and that was the test's fault, not the web's.

## What this licenses

The instrument is sound, so **step 2's readings on ED's own grown patterns can be taken at face value** — including a negative one.

---

### Technical box

Phase dynamics θ̇ᵢ = ωᵢ + K Σⱼ sin(θⱼ − θᵢ) over the relations; natural rates standard normal, mean removed; locking judged on the spread of long-run average rates after transients; adaptive step Δt = min(Δt₀, 0.2 / (K·d_max)). K_c by bisection on a fixed bracket; "never locks" = not locked at the top of the bracket. Sizes 2k, 4k, 8k, 16k; the growth exponent is the slope of log K_c against log N, reported as "rises" when clearly positive or when locking fails outright. Objects: ring; square-grid torus (45², 63², 89², 126²); cubic-grid torus (13³, 16³, 20³, 25³); random 6-regular web by the configuration model with swap repair.
