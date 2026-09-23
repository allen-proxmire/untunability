# Inputs and relations: a first table

*ED_Attempt_02, note 3. 2026-09-14 (RD3). Data: `table/inputs.csv`, `table/relations.csv`. Check: `checks/relations_check.py`. Ledger: C13–C28, D4.*

## What this is

In the spirit of Tao's exponent database (C4), this is a small, rerunnable table with two files.

**Inputs (42):**
- **The Standard Model's 19:** 3 couplings, the Higgs vacuum and self-coupling, 9 masses, 4 quark-mixing parameters, and the strong-CP angle.
- **The neutrino sector (up to 9)** and **two cosmology numbers:** Λ and the matter–antimatter excess.
- **Three structural facts:** 3 generations, 3 dimensions, and the gauge group.
- **Attempt 1's remaining free inputs (7).**

Each input has a working class from Allen's relation–gradient–boundary frame (D1) and a value where one was checked.

**Relations (16).** Everything known to constrain those inputs:
- **theorems**, such as anomaly cancellation and Ehrenfest's argument;
- **measurements**, such as three light neutrinos;
- **empirical patterns nobody has explained**, such as Koide;
- **ED-internal links**, such as the birth chance setting Λ.

**The class labels are a sort, not a result.** Relation covers how things couple and mix (masses, mixings, phases). Gradient covers force strengths and responses. Boundary covers states, edges, counts and cosmology.

## The unexplained patterns, computed (C27)

All five expected results, written down before running, came out as expected.

| relation | what it says | how close |
|---|---|---|
| **Koide** | The three charged-lepton masses satisfy a 2/3 rule | Within **2 parts in a million** |
| **Gatto–Sartori–Tonin** | The quark mixing (Cabibbo) angle ≈ √(down mass / strange mass) | 0.2243 vs 0.2247: within **0.2%** |
| **Quark–lepton complementarity** | The biggest quark and lepton mixing angles add to 45° | 46.6°: **1.6° over**, about 2 standard deviations |
| **Top coupling ≈ 1** | The top quark couples to the Higgs with strength about 1 | **0.991** |
| **Three generations** | Three light neutrino types | 2.984 ± 0.008 |

**Also unexplained, but not computed here:**
- the strong-CP angle is essentially **zero** (below 10⁻¹⁰);
- the Higgs vacuum sits **right at the edge of stability** for the measured masses;
- Λ is about (Planck time / age of the universe)²;
- the matter–antimatter excess;
- the three forces **nearly, but not exactly,** unify.

## Where the unexplained patterns cluster

| class | inputs | theorems | measurements | **unexplained patterns** |
|---|---|---|---|---|
| **Relation** (masses, mixings, phases) | 27 | 2 | 1 | **4:** Koide, GST, complementarity, top coupling ≈ 1 (plus strong-CP ≈ 0) |
| **Boundary** (states, edges, counts, cosmology) | 7 | 2 | 1 | **3:** vacuum at the stability edge, Λ ≈ (t_P/age)², the matter excess |
| **Gradient** (couplings, responses) | 8 | 0 | 1 | **1:** near-unification, which fails exactness |

**The reading.** The places where nature looks "thinner than it should", with numbers sitting on simple rules or special edges, are almost all **relation**-type and **boundary**-type. The gradient class shows the least.

**It matches attempt 1's walls.** ED's missing ingredients were relation- and boundary-type too: a loop phase, a horizon, a chosen state. Two independent views, ED's own failures and the Standard Model's unexplained coincidences, point at the same two regions:
- **how things relate:** the masses, mixings and phases, the flavour sector;
- **states sitting at edges:** a critical vacuum, a tiny Λ, exactly three generations.

## Caveats (important)

1. **Look-elsewhere.** With enough masses and angles, some simple formulas will fit by chance. Many past "mass formulas" failed when data improved. Koide's precision is striking, but it isn't proof of a principle.
2. **Scheme dependence.** Koide works with physical (pole) masses; with running masses it doesn't hold as cleanly. The top coupling is 0.99 with the pole mass and lower with the running mass.
3. **The classification is ours.** Moving a single input between classes changes the counts, and the numbers are small.
4. **These are known puzzles.** The flavour-sector coincidences are an active research area, with discrete flavour symmetries and Koide's own Z₃ form. Nothing here is new physics.

## Allen's X5D paper (`Primes/5_X5D_EXPDB`) (C13, D4)

**What it claims.** Tao's database, underneath its step-by-step code, computes one bounded 5-dimensional polyhedral region (coordinates σ, τ, ρ, ρ*, s). Every downstream result (zero-density estimates, energy bounds, the prime-gap bound) is a projection, rational supremum or lower envelope of it. The paper maps every claim to a function and line in the code.

**Checked against the vendored database code** (commit `af351a3`, February 2026):

| item | result |
|---|---|
| **Functions** | `compute_best_lver` at `additive_energy.py:296`, `lv_zlv_to_zd` at 300, `lver_to_zd` at 471, `best_zero_density_estimate` at 765, `compute_gap2` at `prime_gap.py:11`: **all exactly as the paper says** |
| **Constants** | Values match; three line numbers are off by two, likely a version difference |
| **Size** | The code has 23 modules and 11,007 lines, against the paper's 24 and about 10,700 |

**Assessment.**
- **It isn't bunk.** It's a careful, checkable structural reading of real code, and its code references hold.
- **What wasn't checked:** whether the region is truly *the* central object, and whether the convergence proofs hold.
- **Its limits,** by its own statement: it doesn't engage the number theory, and it doesn't change the database. So its value is clarity, not new bounds.

**What it gives this attempt.** Its picture is exactly D2:
- **Upstream generators:** measurements and theorems, each cutting a half-space.
- **Downstream shadows:** what we observe, as projections.
- **Information lost** at each projection.
- **A sensitivity question:** which new constraint cuts the most.

That's the right vocabulary for the table.

## What next (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Go deeper on the relation class:** gather what is known about the flavour-sector patterns (Koide's Z₃ form, discrete flavour symmetries, why the strong-CP angle is zero) and ask whether one structure ties several of them together | It's where the unexplained patterns cluster, and where ED's walls were |
| **(b)** | **Go deeper on the boundary class:** states at edges (vacuum criticality, Λ, three generations) | The second cluster; closest to ED's horizon and chosen-state walls |
| **(c)** | **Grow the table into a real database** (more relations, uncertainties, sensitivities), in the spirit of X5D | Better map, but no explanation by itself |

**Proposal: (a).** Treat it strictly as a literature map first, with the look-elsewhere caveat front and centre.

**Update:** (a) is done ([Relation_Class_Map.md](Relation_Class_Map.md)).
