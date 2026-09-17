# The draw rebuilt (RD50): test spec

*Written 2026-09-14, before any test was run. Frozen once `run_tests_draw.py` is first run. Changes after that go in a dated section at the bottom, and all tests are rerun.*

## What changes from version 1's draw

| loose point (C286) | version 1 | rebuilt |
|---|---|---|
| **1. When** a mark is unrecoverable | A "detector" event, given as an input | **Meaning (RD50):** part of the mark is out of reach of every future path. **Working stand-in here:** at least R* = 3 fragments hold near-perfect copies of the same distinction (record distinguishability sin θ ≥ 1 − δ, δ = 0.01). R* and δ are modelling choices, not part of ED |
| **2. What** a draw fixes | A single locus and channel of the system | **Only which record the fragments hold** (which way the system went). Everything inside that record stays coherent |
| **3. Where** the mark goes | Not tracked | **The environment has a state:** F fragments of committed matter, each with two channels, unmarked and marked. The mark stays in them |
| **4. Probabilities** | Amount squared, assumed | Still assumed: a record's probability is the amount in that record |
| **5. Moment, not rate** | Detector event | **A draw happens at the meeting that makes the record redundant** |
| **6. Budget** | Unspecified | Still unspecified (not needed for these tests) |

**The pieces.**
- **The pattern** is ψ[u, K, e₀, …, e_{F−1}]: the system on a ring (version 0's spreading, three channels), plus F fragments.
- **A meeting** (RD27): wherever the system is at one of the given loci (any channel), a fragment turns from unmarked toward marked by angle θ. It is linear and conserving, and it never draws. The meeting's loci define the **distinction** its record is about.
- **The draw:** after each meeting, if the distinction just written now has R ≥ R* near-perfect fragments, pick a record value (all unmarked or all marked) with probability equal to the amount in it, and keep only that part. This happens once per distinction.
- **The eraser:** measuring fragments in the "unmarked + marked" / "unmarked − marked" basis and keeping one outcome. This is used in tests only.

## Limits (stated before running)

- **The stand-in isn't the meaning.** Under the horizon meaning, a lab mark stays recoverable in principle until it leaves reach, as in standard quantum physics. The stand-in instead makes records final at R*. So the stand-in is wrong about erasing R* or more copies (test D8b shows it), and it must not be used to claim anything about reversibility.
- **1D, no units.** Fragments are abstract two-channel parts of committed matter.
- **Which interaction a meeting uses is a test input,** as in V1-L2.
- **Probabilities are assumed, not derived** (item 4).

---

## Setup (as version 1)

- **System ring:** 31 loci. Starts in the Internal channel at loci 13 and 17 with amplitudes 1/√2 and e^{iφ}/√2 (unless stated).
- **Screen:** 8 spreading steps; the system share at each locus is summed over channels and fragments, then normalized.
- **Visibility:** screens at φ = 0, π/2, π give a + Re(c e^{iφ}), so V = \|c\|/a where a > 10⁻⁹.
- **V0:** the no-mark visibility. Ratios V/V0 are compared where V0 > 10⁻⁶.
- **Families:** a mark "at locus 13" means meetings with loci {13}.

## Tests and frozen predictions

| test | what | prediction | confidence |
|---|---|---|---|
| **D1a (code)** | Random system pattern, 3 fragments: spreading and meetings | Amount conserved to 10⁻¹² | High |
| **D1b (code)** | Mirror: events at loci 9 and {9, 10} vs mirrored loci, 2 fragments, no draw | Mirror of one result equals the other to 10⁻¹² | High |
| **D2** | No mark (1 fragment, never met) | V/V0 = 1 everywhere to 10⁻⁸; no draw | High |
| **D3 (Englert)** | One partial mark at 13, θ = π/6, π/4, π/3 | V/V0 = \|cos θ\| everywhere to 10⁻⁸ (D = sin θ, so D² + (V/V0)² = 1); no draw | High |
| **D4 (eraser)** | One full mark (θ = π/2, R = 1 < R*) | Unconditioned V < 10⁻¹⁰; conditioned on either eraser outcome, V/V0 = 1 to 10⁻⁸; no draw | High |
| **D5 (redundant mark)** | Amplitudes cos 0.4 at 13 and e^{iφ} sin 0.4 at 17; 3 full marks at 13 | A draw happens; record probabilities are cos² 0.4 and sin² 0.4 to 10⁻¹²; disagreeing records weigh < 10⁻¹²; each branch has amount < 10⁻¹⁵ on the other path before spreading; averaged screen V < 10⁻¹⁰ | High |
| **D6 (fixes only what the mark distinguishes)** | Start ½ at 12, ½ e^{iψ} at 14, 1/√2 at 17. 3 full marks with loci {12, 13, 14}. Vary the inner phase ψ | Conditioned on "marked", the inner visibility equals that of the lone pattern (\|12⟩ + e^{iψ}\|14⟩)/√2 to 10⁻⁸. **Reported contrast:** version 1's detector draw on the same start gives inner visibility 0 in every outcome | High |
| **D7 (code, no signalling)** | A partner B entangled with the paths (13 with B = 0, 17 with B = 1), 3 full marks at 13 | B's reduced state averaged over draws equals B's reduced state with no draw, to 10⁻¹² | High |
| **D8a** | Two full marks (R = 2 < R*) | No draw; unconditioned V < 10⁻¹⁰; conditioned on each of the 4 joint eraser outcomes, V/V0 = 1 to 10⁻⁸ | High |
| **D8b (the stand-in's limit)** | Three full marks (R = 3 = R*) | A draw happens; conditioned on each of the 8 joint eraser outcomes, V < 10⁻¹⁰. **Standard quantum physics would give V/V0 = 1 here.** The model is deliberately final at R* | High (by construction) |

**What passing means.**
- **The rebuilt draw reproduces the known single-mark, partial-mark and eraser results**, keeps coherence inside the record, and doesn't signal.
- **Passing is a requirement met, not evidence for ED** (Rule 4).
- **D8b records openly where the stand-in departs from standard physics.**

### Allen's predictions

*(Optional. Fill in and date before running.)*

---

## Changes after freezing

**2026-09-14, after run 1 (`results_draw_run1.txt`).** D1a, D1b, D2, D3, D4, D7, D8a and D8b right; D5 and D6 wrong.

**D5 and D6 were test-harness errors (Claude's), not rule failures.**
- **The bug:** the harness picked the "marked" and "unmarked" branches by testing for amplitude exactly zero.
- **Why it fails:** after three quarter-turn meetings, rounding leaves about 10⁻⁴⁹ in amplitude (amount 2.9 × 10⁻⁹⁷) where there should be none, because cos(π/2) is not exactly 0 in floating point. So both branches passed the test and the wrong one was used.
- **The rule's own numbers were right:** no disagreeing records, other-path amount 2.9 × 10⁻⁹⁷, averaged V = 0.
- **Fixed:** branches are now identified by amount > 10⁻¹². Run 1's verdicts stand as the record; run 2 is rerun with the fix.

**2026-09-14, after run 2 (`results_draw_run2.txt`).** All ten predictions right. The exit code now requires the code checks and all ten verdicts to reproduce.
