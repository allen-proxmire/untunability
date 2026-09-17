# The C2a model: does the balance come from ED's budget? (specification, on paper)

*ED_Attempt_07, note 6. 2026-09-16 (RD7). Ledger: C13–C15. **A specification only: no code written, nothing run.** Meaning questions C2a-Q1–C2a-Q3 and the expected results are for Allen to confirm; running is a separate yes.*

## Accepted in note 5 (C13)

**Allen accepted C2-Q1–C2-Q4** (D6):
- ED must explain the balance;
- it comes from commitment's budget, with crowded regions getting fewer offspring;
- the feedback is local;
- the tiny leftover excess is the cosmic expansion, with its value inherited.

## First, on paper: the budget reading matters (C14)

### Reading A: "links held use up budget" (naive)

- **An event's budget shrinks with the number of past links it holds.**
- **Count, from C1's construction:** forward links out of slice t number L_t + L_{t+1}, all arriving at the L_{t+1} events of slice t+1. So the **average number of past links per new event = 1 + L_t / L_{t+1}.**
- **Follow the sign:**
  - **space shrinking** (L_{t+1} < L_t) → more past links per event → less budget → fewer offspring → **shrinks further;**
  - **space growing** → fewer past links → more budget → more offspring → **grows further.**
- **So reading A pushes away from the balance:** runaway growth or extinction.

### Reading B: "budget passed forward, conserved"

- **Each event splits its budget equally across its forward links.** A new event's budget is the sum it receives.
- **No budget is created or lost,** so every slice holds the same total B.
- **Average budget per event in slice t** = B / L_t.
- **Offspring rise with budget received:** mean offspring μ = 1 + k·(b/b_ref − 1), where b_ref = B/L\* is the budget per event at a reference slice size L\*, and k is the response strength.
- **Averaged over a slice:** μ̄ = 1 + k·(L\*/L_t − 1), so on average L_{t+1} = L_t + k·(L\* − L_t).
  - **crowded** (L_t > L\*): fewer offspring;
  - **sparse:** more offspring.
  - **It pulls toward L\*.**
- **Stability window** (arithmetic): the gap to L\* shrinks by a factor (1 − k) per slice.
  - **0 < k < 2:** settles;
  - **k = 2:** oscillates without settling;
  - **k > 2:** oscillates with growing swings and fails.

**So reading B is the precise form of C2-Q2** ("crowded → fewer offspring"), and reading A is its wrong-signed cousin.

**Recorded:** reading B was chosen after this sign check showed reading A can't give a balance. That's revise-and-retest, and it's on the record.

**What reading B gives, and doesn't:**
- **It gives the balance without tuning the average to 1.** But slices then hover at a fixed size L\* instead of growing.
  - **The space is a closed tube,** not an expanding universe.
  - **Growth would need budget to be created,** at a tiny rate. That's the cosmic excess of C2-Q4, left for later.
- **k and L\* are knobs,** counted by the census guard.

## The model

**Built on C1** (note 3): slices are circles; forward runs of c+1 consecutive events; neighbours share one; space doesn't split.

**Changes from C1:**

| | C1 | **C2a, reading B** | C2a, reading A (contrast) |
|---|---|---|---|
| **Start** | One event on a spine | **Slice 0 of L\* events, each with budget b_ref; no spine** (the pattern must survive on its own) | Slice 0 of L\* events; no spine |
| **Offspring of event x** | Mean exactly 1 | **Geometric with mean μ_x = max(0, 1 + k·(b_x/b_ref − 1))** | Geometric with mean μ_x = max(0, 1 − k·(p_x − 2)), where p_x is x's number of past links (2 is the balanced average) |
| **Budget** | — | **x splits b_x equally across its c_x + 1 forward links; a new event's budget is the sum received** | — |

A geometric distribution with mean μ has P(c) = p(1−p)^c, with p = 1/(1+μ). μ = 0 means no offspring.

## Sizes and seeds

| part | what | sizes |
|---|---|---|
| **Balance runs** (cheap: no readings) | Reading B at k ∈ {0.5, 1, 1.5, 2.5} × L\* ∈ {100, 200}; reading A at k ∈ {0.5, 1} × L\* = 200 | **20 seeds each**, T = 400 slices |
| **Geometry runs** (readings) | Reading B at k ∈ {0.5, 1, 1.5}, L\* = 200 | **3 seeds each**, T = 200 slices (about 40,000 events, the same size as C1's flat strip) |

**Calibration:** C1's flat strip at this exact size met F0 (C8), so the readings are already calibrated for it. No new calibration is needed.

## Readings (fixed before code)

| | reading | procedure |
|---|---|---|
| **B1** | Survival | Did the pattern reach slice T without dying (no events) or running away (more than 10·L\* events in a slice)? |
| **B2** | Balance | Mean offspring over slices T/2…T, and mean slice length over slices T/2…T relative to L\* |
| **B3** | Budget conservation (reading B) | Total budget of every slice equals B to within 10⁻⁹ relative |
| **S2** | Structure | As C1: one circle per slice (3 or more events), forward links only one slice ahead, forward count = L_t + L_{t+1} |
| **R1–R5** | Dimensions | A6 readings v2, as C1 |

## Expected results, written down before any code

| | expected | grounds |
|---|---|---|
| **E1** | Structure exact and budget conserved in every run | By construction |
| **E2** (reading B, k = 0.5, 1, 1.5; both L\*) | In every setting, **at least 19 of 20 seeds survive** (B1); **median over seeds** of mean offspring in [0.98, 1.02]; **median** mean slice length within **±10% of L\*** | The stable window 0 < k < 2 (C14) |
| **E3** (reading B, k = 2.5) | **Fails E2 in a majority of seeds** at both L\*: dies, runs away, or mean slice length outside ±10% | Outside the stable window (C14) |
| **E4** (reading A, both k) | **Majority of seeds die or run away** before T | Wrong-signed feedback (C14) |
| **E5** (reading B geometry, k = 0.5, 1, 1.5, L\* = 200) | **Median over 3 seeds:** d_H in [1.7, 2.3], d_s ≤ 2.3; structure exact | A random tube at scales below its circumference behaves like C1's 2D geometry |

## Exit rule (Allen to confirm)

| | outcome | recorded as |
|---|---|---|
| **Pass** | E1, E2, E5 met | "**The balance self-organizes from ED's budget passed forward and conserved: consistent, not derived; k and L\* are knobs; space settles as a fixed-size tube, and growth would need budget creation (the cosmic excess, inherited).**" Then on to C2 part 2 (slice dimension) |
| **E3 or E4 not as expected** | — | Recorded as a finding about the feedback's stability. **It doesn't block a pass on E2 and E5** |
| **E2 or E5 fails** | — | "**Balance put in**"; go on to slice dimension with the balance as an input. Revise-and-retest is allowed, with the reason recorded |
| **E1 fails** | Code bug | Fix it (recorded), rerun |

## Running order (when Allen says run)

1. **Timing:** one balance run, and readings on one geometry run.
2. **Balance runs.**
3. **Geometry runs.**

**Estimate:** about 30–40 minutes. Code goes in `ED_Attempt_07/model/`, reusing C1's builder and the copied readings.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C2a-Q1** | **Is ED's budget passed forward along links:** each event shares its budget across its future links, a new event's budget is what it receives, and the total is conserved from slice to slice? | **Yes, labelled reading** | It's the precise form of "crowded → fewer offspring" (C14); the naive "links held use up budget" pushes the wrong way |
| **C2a-Q2** | **Does more budget received mean more offspring,** with response strength k? | **Yes** | The simplest local feedback; k is a knob |
| **C2a-Q3** | **For C2a, is the total budget fixed** (no creation), so space settles at a fixed size, leaving budget creation (the cosmic excess) for later? | **Yes** | Tests the balance on its own first; expansion is a separate step |

## Next step

**Decide C2a-Q1–C2a-Q3 and confirm the expected results and exit rule.** Then say run.
