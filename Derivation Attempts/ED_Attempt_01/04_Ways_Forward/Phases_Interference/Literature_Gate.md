# Literature gate: phases that interfere (P09)

*Done 2026-09-13. Ledger: C26–C30, A7.*

## The question

The reinforced-walk simulation failed its gate because random walks with reinforcement are already understood (see `../Sim_Spontaneous_Direction/Literature_Gate.md`). The candidate ingredient those walks lack is phases that can interfere (P09). So the question is:

> Can a system whose rules look the same in a mirror, carrying phases that interfere, pick a preferred direction by itself? And if so, would showing it be specific to ED?

## Verdict: the gate fails again

1. **Yes, and it is already published, in experiment and theory.** A mirror-symmetric ring carrying interfering light waves picks one direction of circulation by itself once the light is strong enough.
2. **It depends on a setting ED doesn't fix.** It needs *feedback*: the state has to change how the state itself travels (in optics, the light's intensity changes the refractive index). Whether a direction appears depends on the kind and strength of that feedback. ED's primitives don't specify one (A7).

So phases alone don't make a new, ED-specific question. Phases plus a feedback law ED can't yet state is the same situation as the reinforced walk.

---

## What is known

### 1. Spontaneous direction on a symmetric ring, observed

- **Q.-T. Cao et al., "Experimental demonstration of spontaneous chirality in a nonlinear microresonator", *Physical Review Letters* 118, 033901 (2017),** arXiv:1607.01459. Abstract checked 2026-09-13.
  - A ring resonator with no built-in mirror or time asymmetry.
  - Above a few hundred microwatts, one circulation direction wins, with an output ratio of 20:1.
  - The cause is the Kerr nonlinearity coupling the clockwise and counter-clockwise waves.
- **L. Del Bino, J. M. Silver, S. L. Stebbings and P. Del'Haye, "Symmetry breaking of counter-propagating light in a nonlinear resonator", *Scientific Reports* 7, 43142 (2017).** Checked 2026-09-13.
  - Same kind of system. The ring "picks" one of two states.
  - Mechanism: unequal powers shift the refractive index unequally, and positive feedback amplifies the imbalance.

This is the magnet picture from the handedness result, realised with interfering waves: symmetric rules, and a direction chosen by the state.

### 2. The same thing on a lattice, in the language of winding numbers

- **P. Fittipaldi de Castro and W. A. Benalcazar, "Solitons with self-induced topological nonreciprocity", arXiv:2405.14919 (2024).** Abstract checked 2026-09-13. Preprint; journal status not checked.
  - A lattice whose couplings are symmetric (reciprocal).
  - With a nonlinearity, localized waves (solitons) develop one-way motion by themselves, depending on their power.
  - The authors connect this to point-gap topology, the same winding-number idea as the handedness result. That connection is from the abstract page summary; the paper was not read in full.

### 3. Feedback can force a direction, but chosen by design

- **R. Shen and C. H. Lee, "Observation of feedback-directed quantum dynamics in large-scale quantum processors", arXiv:2604.11900 (2026).** Abstract checked 2026-09-13.
  - Measurement plus conditional feedback in quantum circuits produces directional flow.
  - The direction is set by how the protocol is designed, not spontaneously.

---

## What this means

| system | rules mirror-symmetric? | interfering phases? | feedback | direction picked by itself? |
|---|---|---|---|---|
| Reinforced random walk (linear) | Yes | No | Past choices change odds | No (C18) |
| Ant mill walk | Yes | No | Strong, cancellable | Yes (C24) |
| Nonlinear ring resonator | Yes | Yes | Intensity changes propagation | Yes, above a threshold (C26) |
| Nonlinear lattice solitons | Yes | Yes | Intensity changes propagation | Yes, depending on power (C27) |
| Feedback quantum circuits | No (by design) | Yes | Measurement-conditioned | No, set by design (C28) |

- **The common factor is feedback, not phases.** Every case where a direction is chosen spontaneously has the state feeding back on its own motion, strongly enough.
- **Both the handedness result and these papers say symmetry breaking comes from the state.** The published systems are concrete examples of what the handedness result says must happen if a direction appears.
- **An ED version would only be new if ED fixed the feedback law.** Right now nothing in the primitives does (A6, A7).

## What would be worth doing instead

Everything so far points to the same missing piece: **ED has no definite rule for what a commitment does to what happens next.** Every question tried (reinforcement, phases, spontaneous direction) ends at "it depends on a law ED doesn't state."

The recommended next step is not another simulation. It is writing the commitment rule itself (Rule 1: a rule a computer can run), directly from P02, P04, P09 and P11, without choosing it to make anything come out. Once that rule exists:

- whether it contains feedback, and how strong, stops being a setting and becomes a consequence;
- the questions above become testable in a way that is specific to ED;
- and each one still goes through its own literature gate.

## Sources

- Cao et al. (2017): https://arxiv.org/abs/1607.01459 and https://link.aps.org/doi/10.1103/PhysRevLett.118.033901
- Del Bino et al. (2017): https://pmc.ncbi.nlm.nih.gov/articles/PMC5318886/
- de Castro and Benalcazar (2024): https://arxiv.org/abs/2405.14919
- Shen and Lee (2026): https://arxiv.org/abs/2604.11900
