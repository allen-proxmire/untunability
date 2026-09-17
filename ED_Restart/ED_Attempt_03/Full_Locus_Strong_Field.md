# A full locus: what it means for black holes

*ED_Attempt_03, note 5. 2026-09-15 (RD5, RD6, D2). Ledger: C26–C34. Checks: `checks/strong_field_check.py`, `checks/escape_check.py` (expected results written first). **Status: ED's strong-field line closed under its exit rule (C33).***

## Allen's decision (D2)

**"A full locus is part of ED's meaning."** So the budget cap, U ≤ 1, is a real rule of ED. Note 4 showed that once the budget was tied to gravity, the cap fixes where gravity saturates. This note works out what that means for black holes, and checks it against what's observed.

## ED's black hole, from its own rules

Three pieces from attempt 1, now read together:

| rule | what it does | source |
|---|---|---|
| **Clocks slow by e^(−U); motion slows by e^(−2U)** | That's the **exponential metric** | A1 RD35, RD36 |
| **U = GM/(rc²) far from a mass** | Matches weak-field gravity | A1 C104 |
| **U can't exceed 1** | A full locus (D2) | A1 RD14 |

**Together they give a black hole with two parts:**
- **Outside:** the exponential metric. It has **no horizon**; light aimed straight out always escapes (C20).
- **Inside, where U would exceed 1:** a **saturated core**. Everything there runs at a fixed e^(−1) ≈ 0.37 of the far-away rate. It's a region of constant slowing with no horizon and no singularity.

**One assumption carried in.** U = GM/(rc²) is used right down to the core. Attempt 1's gravity matched general relativity only at the orders tested (A1 RD37), so the strong-field details are an extension, not a derivation.

## The numbers this fixes (C30)

*Check: `checks/strong_field_check.py`. All four expected results held.*

| | ED (full locus) | general relativity |
|---|---|---|
| **Light's circular orbit** | at 2 GM/c² | at 3 GM/c² |
| **Shadow size** | 2e GM/c² ≈ 5.437 | 3√3 GM/c² ≈ 5.196 |
| **So the shadow is** | **4.6% larger** | — |
| **Deepest redshift** | **1 + z = e ≈ 2.72**, at the core edge | unbounded, at the horizon |

**These are specific numbers, and they come from ED's own rule.** That's the first time in attempt 3 an ED rule has fixed a physics number. **But they depend on the rate law e^(−U),** which attempt 1 chose to match Mercury (A1 RD36), not derived.

## What observations say

**1. Black-hole images: not ruled out (C26).**
- **What's measured:** the Event Horizon Telescope's Sgr A* shadow comes out slightly *smaller* than general relativity's: −8% ± 9% or −4% ± 9–10%, depending on the mass estimate.
- **ED's +4.6%** sits **1.4 and 1.0 standard deviations** above those.
- **So shadow size alone doesn't exclude it.** The same analyses note that images are especially strict on shadows *larger* than general relativity's, and better mass estimates would sharpen this.

**2. Horizon evidence from missing surface glow: strong tension (C27, C28, C31).**
- **The known argument.** If a black hole had no horizon, matter falling in would have to release its energy somewhere visible.
  - **Sgr A*:** any visible surface can emit less than **0.4%** of the accretion power (Broderick, Loeb, Narayan).
  - **X-ray binaries:** black-hole systems are about **100 times dimmer** than neutron-star systems in quiet phases, and never show the thermonuclear bursts that happen on surfaces (Narayan, McClintock and others).
- **ED's core can't hide that energy.** A rough estimate (reasoning, not a model):
  - matter falling to the core edge gives up about **63%** of its rest energy (1 − e^(−1));
  - light made there escapes on its first try about **16%** of the time;
  - with no horizon, what doesn't escape at first is reabsorbed and re-emitted, so over time the energy gets out, weakened by at most a factor of e.

  **That's far above 0.4%.**
- **The cap is what makes this sharp.** Without the cap, the exponential metric's redshift grows without limit toward the centre, and energy could be hidden very deep. A full locus stops that at a factor of e.
- **Limits:** ED's core dynamics aren't modelled: how matter behaves inside a saturated core, and how the core grows. So this is strong tension by reasoning, not a computed exclusion.

**3. Gravitational-wave echoes: no evidence either way (C29).**
- **What a search found:** a search of the LIGO–Virgo–KAGRA O3 run found no significant echoes.
- **Why that doesn't settle it:** echoes could be below current sensitivity.

## What it means (C32)

- **Good.** Making a full locus part of ED's meaning gives ED its **first specific, own-rule physics numbers**: a shadow 4.6% larger, and a deepest redshift of e. That's the source of specificity attempt 3 was looking for, of the boundary kind (note 2).
- **Bad.** Those same numbers mean **ED's black holes have no horizon and a shallow core.** The standard horizon evidence, especially Sgr A*'s missing surface glow, is in strong tension with that.
- **Honest status.** ED with a full locus and its current rate law makes a real strong-field claim, and existing evidence leans hard against it. The tension rests on reasoning, since ED's core isn't modelled, but the reasoning is the same one used to argue that horizons exist.
- **What would have to give,** if the tension holds:
  - **the rate law** (e^(−U) was matched, not derived);
  - **the strong-field use of U = GM/(rc²)** (matched only at tested orders); or
  - **the full-locus meaning** (D2).

  Changing any of these because of this evidence has to be recorded as exactly that.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(l)** | **A short, bounded escape check** under an exit rule fixed first. Compute the fraction of energy released at ED's core that reaches far away (single emission and with re-emission), using the exponential metric outside. *Draft exit rule:* if that fraction exceeds Sgr A*'s 0.4% limit, record that **a full locus with ED's current rate law conflicts with the horizon evidence**, and close ED's strong-field line | Turns the reasoning into a computed claim; cheap |
| **(m)** | **Consolidate attempt 3** without the check: the specificity search found ED's one own edge, its numbers, and strong tension | A clean stopping point |
| **(n)** | **Revisit what could give** (rate law, strong-field U, or D2), recorded as a response to evidence | Allen's call; risks fitting |

**Proposal: (l), with its exit rule confirmed first.**

## Escape check results (C33, C34)

*Check: `checks/escape_check.py`, run 1. The exit rule and its exact form were confirmed by Allen before running (RD6).*

| reading | energy reaching far away, as a share of the rest energy that fell in |
|---|---|
| Heat released at the core edge | 63.2% |
| **(1) First emission, outward light only** | **10.2%** |
| (2) First emission, all directions, light passing through the core | 20.4% |
| (3) Steady state: trapped light reabsorbed and re-emitted, with no horizon to swallow it | 63.2% |

**The smallest reading, 10.2%, is about 25 times Sgr A*'s 0.4% limit.**

**Verdict under the exit rule: it fires. A full locus with ED's current rate law conflicts with the horizon evidence, and ED's strong-field line closes.** All five expected results held.

**A correction to the section above.** It said light escapes on its first try "about 16% of the time". That counted only outward light. ED's core is flat and has no horizon, so inward light passes through and comes out the other side, which makes the first-try share 32%. The verdict uses the smaller figure, the one kindest to ED.

**Limits:**
- **Thermalization is assumed.** The check assumes infalling matter comes to rest and heats up at the core edge. In a steady accretion flow, gas meeting gas at the core does that, but ED's core dynamics aren't modelled.
- **The weak-field gravity strength is used down to the core,** as noted above.

**What closing means.** By the rule, no change to the rate law, the strong-field budget or the full-locus meaning is tried now, unless Allen opens a new line with its own exit rule.

## Next steps after the verdict (Allen decides)

| | step | why |
|---|---|---|
| **(m)** | **Write up attempt 3 in plain language** | The specificity search has a clear result |
| **(o)** | **The dark-energy clip's data test** (A1 G41) | The other live edge, though its size is borrowed |
| **(p)** | **The counting route** (note 1, option c) | The relation-class route, not yet explored |

**Proposal: (m).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C26 | Vagnozzi et al., "Horizon-scale tests of gravity theories and fundamental physics from the Event Horizon Telescope image of Sagittarius A*", arXiv:2205.07787 (2022); EHT Sgr A* paper VI, arXiv:2311.09484 | Search listings |
| C27 | Broderick, Loeb, Narayan, "The event horizon of Sagittarius A*", *Astrophys. J.* 701, 1357 (2009) | Abstract via search listing |
| C28 | Narayan, Garcia, McClintock and collaborators: arXiv:astro-ph/9712015, arXiv:astro-ph/0012452, arXiv:astro-ph/0310692; Narayan & McClintock review | Search listings |
| C29 | Search for gravitational-wave echoes in O3, arXiv:2309.01894; "How loud are echoes from exotic compact objects?", arXiv:2010.14578 | Search listings |
