# Road R1: commitments as sources of gravity

*ED_Attempt_04, note 2. 2026-09-15 (RD2, RD3, D1–D6). **Status: closed on paper (RD3).** Ledger: C3–C8. On paper, with one bookkeeping check (`checks/bar_weights_check.py`, expected results written first). No candidate's weights were computed.*

## Where R1 starts

**Allen accepted all six picture defaults** (D1–D6):
- a body's own presence doesn't block its own clocks;
- gravity's influence is separate from presence;
- mass is what a body sends out;
- **a commitment carries nothing numerical yet;**
- two bodies can't be present at the same locus;
- attempt 1's smooth budget and cap are retired.

**The question** (from attempt 3, note 7): in general relativity, a source's motion, its pressure and gravity's own energy make gravity slightly stronger, with specific weights. On/off exclusion can't supply them, because it only subtracts. **Can a body's commitments supply them instead?**

**The first consequence:** because a commitment carries no number (D4), on its own it adds nothing. So R1 has to say *what a commitment carries*, and that has to come from ED's meaning, fixed before any weights are computed. Before choosing, it helps to know the bar.

## The bar (C3)

*Bookkeeping check: all four expected results held.* In ED's terms, general relativity needs a source to count its parts with these weights:

| part of a source | general relativity needs | plain energy counting gives | gap |
|---|---|---|---|
| **Motion** | **2** | ½ | +3/2 |
| **Gravity's own energy** | **2** | −½ | +5/2 |
| **Internal energy** (heat, binding inside) | **1** | 1 | **0** |
| **Pressure** | **3** | 0 | +3 |

- **The check reproduces attempt 1's two earlier counting cases exactly** (A1 C207), so the translation is right.
- **Internal energy already meets the bar.** The gaps are motion, pressure and gravity's own energy.

## What's known: pressure counts three times (C4)

- **Tolman and Whittaker's "active gravitational mass" (1934–35).** A source gravitates with its energy **plus its pressure counted once in each of the three space directions**: ρ + 3p.
- **Radiation gravitates about twice** as much as the same energy in matter, because its pressure counts too.
- **Pressure and gravity's own energy are linked.** For a body held together by its own gravity, 3p adds up to minus the gravitational self-energy (the virial theorem).

## Candidate meanings for what a commitment carries (C5–C7)

| | meaning | where it comes from | outcome |
|---|---|---|---|
| **R1-a** | **Commitments are the body's ticks.** Its source is how often it commits | Attempt 1's clock ticks (A1 RD18, RD24); "mass is what it sends out" (D3) | **Fails, already known.** Ticks slow with motion and with gravity, so every weight goes the wrong way. That's note 7's subtractive case (A3 C42: Moon-test number 13/3, where 0 is needed) |
| **R1-b** | **Each commitment counts once,** with no direction | The least structure | **Fails, already known.** It's plain energy counting (Moon-test number 17/6; A1 C207, C208) |
| **R1-c** | **A commitment that crosses between loci counts once per space direction it crosses** | A commitment is a relation between loci, so it crosses space, and space has three directions | **Pressure 3 and motion 2 would come out, but only because this *is* Tolman's formula in ED words.** Adopting it makes ED consistent with general relativity, not derived from ED, unless ED's meaning of a commitment requires "once per direction" for its own reasons |

**Gravity's own energy (weight 2) can't come from commitments at all, under Allen's decisions** (C7):
- **Commitments** link present loci of one body (D4).
- **Gravity's influence** is never presence (D2).
- **So influence carries no commitments,** and gravity's own energy can't be counted through them.
- **Supplying that weight would mean changing D2,** so that the field itself carries commitments. Doing that *because* the weight is needed would be fitting.

## What it means (C8)

**On paper, R1's answer is nearly settled without computing anything:**
- **The two meanings that come from ED on their own grounds fail,** and their failures are already on record.
- **The meaning that works for motion and pressure is general relativity's known source formula,** restated.
- **Gravity's own energy is out of reach** under the picture as decided.

**So commitments can at most restate general relativity's matter weights. They can't derive them, and they can't supply gravity's own-energy weight.** That matches attempts 1 and 3: ED's meanings explain some of how gravity *acts*, but not what *sources* it.

## Draft exit rule, if R1 is pursued further (Allen to confirm)

1. **Pick one meaning** (R1-a, R1-b or R1-c) as a decision about ED's meaning, before computing its weights.
2. **Compute all four weights and the Moon-test number.**
3. **R1 closes** as "commitments don't supply gravity's weights" if any weight misses the bar beyond the measured bounds.
4. **If the chosen meaning hits the matter weights only because it restates Tolman's formula,** record "consistent, not derived".
5. **Gravity's own-energy weight is judged separately.** Under D2 and D4 it can't come from commitments.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Close R1 on paper** as above: commitments can restate general relativity's matter weights but not derive them, and can't supply gravity's own energy under D2 | The outcome is determined by results already on record; computing would only confirm it |
| **(b)** | **Adopt R1-c as ED's meaning** and compute it, recording it openly as consistent with general relativity, not derived | Only worth it if "once per direction" feels like what a commitment *is* to Allen, independent of the target |
| **(c)** | **Revisit D2** so gravity's influence can carry commitments | Opens gravity's own energy, but changing a decision to reach a target is fitting, and would have to be recorded as such |

**Proposal: (a),** then road R2 (matter excludes matter), or pause.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C4 | Tolman (1934) and Whittaker (1935): active gravitational mass from T₀⁰ − T₁¹ − T₂² − T₃³, i.e. ρ + 3p; Tolman on disordered radiation gravitating about twice as much; virial theorem relating 3p to gravitational self-energy. As described in "Gravitational and inertial mass in general relativity" (arXiv:1010.5557), "About the mass problem" (arXiv:0906.2170), arXiv:2101.12570; Whittaker, *Proc. R. Soc. A* (1935) | Search listings; originals not read |
| — | Attempt 1: C206–C208, RD18, RD24, RD37. Attempt 3: C42–C44 | Read directly |
