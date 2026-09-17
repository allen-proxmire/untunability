# Literature gate: commitment rule version 0

*Done 2026-09-13. Ledger: C55–C60, test T8, gap G23.*

## The questions

1. Is version 0 already a known model?
2. Where exactly does it differ from known models?
3. Is any part of it already contradicted by experiment?

## Verdict

- **Q1: yes, in its main parts.** Version 0 is a discrete spontaneous-collapse model of the GRW "flash" kind, with the standard amplification mechanism. Each of its central ideas has a close published relative.
- **Q2: less than hoped.** The budget's slowing of ticks near mass, if it matches measured clocks (which it must), is ordinary gravitational time dilation. Every relativistic collapse model already has that. In weak gravity it gives no observable difference. What could still be ED's own is listed below.
- **Q3: there is a conflict.** Treating a lone particle's own time as its count of collapse ticks can't match three kinds of experiment at once. **Version 0 should not be coded until gap G23 is decided.**

---

## What is already published

| ED idea | closest published relative | ledger |
|---|---|---|
| A commitment is a real, one-way collapse event; a chain is its sequence of ticks | GRW spontaneous collapse, flash version (Bell; Tumulka 2006) | C36, C42 |
| Big hinged things resolve constantly, small things rarely | GRW amplification: an object's centre of mass localizes at the sum of its parts' rates | C45 |
| Collapse tied to gravity | Diósi–Penrose (the parameter-free version is ruled out) | C36, C43 |
| Gravity and time dilation make things classical | Pikovski, Zych, Costa, Brukner (2015): time dilation couples a composite particle's internals to its position and decoheres it with no environment; on Earth enough for micron-scale objects | C55 |
| Time is what physical ticks count, and that breaks perfect quantum evolution | Gambini, Porto, Pullin (2004): with realistic physical clocks, quantum mechanics stops being exactly unitary and a universal decoherence appears | C56 |
| Collapse on a discrete substrate | Leckey and Flitney (2023): a spontaneous collapse model motivated by fully discrete physics (abstract only read) | C57 |

**So the combination may be new, but none of the parts is.** Whether the combination adds anything testable is Q2.

---

## Q2: where could ED actually differ?

### The budget and clocks: an explanation, not a new prediction (C59)
- **What the budget does:** it slows ticks where mass uses up the budget.
- **What test T1 and T3 require:** that slowing must *equal* the measured gravitational time dilation.
- **Every relativistic collapse model already has that:** collapses happen in each particle's own time, so near a mass they happen less often as seen from far away. That is just time dilation.

So if ED gets clocks right, the budget changes nothing observable about collapse in weak gravity. It gives ED a *story* for why time dilation happens (mass uses up commitment capacity). That has explanatory value, but it isn't a prediction that could distinguish ED from GRW.

### What could still be ED's own
1. **The budget fixing r₀ or q** (C50, C51). If the per-part rate or the spreading factor came out of the budget rather than being chosen, ED would have a number that GRW and Diósi–Penrose don't.
2. **Strong gravity.** Where the budget is nearly used up, the straight-proportion rule and GR's time dilation formula can differ. That is untestable today, but it is a real difference.
3. **The handedness question** (C32). Whether ED's collapses make transport effectively one-way is specific to ED's rule, not to GRW.

---

## Q3: the conflict (C60, test T8)

**The problem is in two decisions.**
- **RD9:** a chain *is* its sequence of ticks.
- **G14:** a chain's own time is its tick count.

Taken together, a lone particle's clock runs only when it collapses. Three experimental facts can't all hold under that:

| fact | what it forces |
|---|---|
| **Single electrons and C60 molecules interfere** (C39) | A lone particle must collapse *rarely*, or it could never spread enough to interfere |
| **Collapse rates are limited by experiment** (C43, C45) | Collapses of small things must be rare. GRW's proposed rate is about once per 10¹⁶ seconds per particle |
| **Isolated unstable particles age at the relativistic rate:** muons moving at γ = 29.33 lived exactly as long as special relativity predicts, to 2 parts in 1000 (Bailey et al., 1977) (C58) | A lone muon's internal clock runs steadily, decaying in about 2.2 microseconds of its own time, whether or not it collapses |

If a lone muon's time only advanced when it collapsed, and it collapses about once per 10¹⁶ seconds, it would essentially never decay. It decays in microseconds. So **a lone particle's clock can't be its collapse count.**

### G23 — what does the budget slow down? — needs Allen

**Proposal.** The local rate factor (the share of budget left) slows **every** process at a place, not just collapses:
- spreading between ticks,
- internal evolution, such as a muon's decay,
- and collapses.

That is what time dilation means physically: everything at a place runs slower together, so clocks of every size agree. Then:

- **"Commitment is the tick" still holds for big hinged things**, like clocks, the Earth or you. They tick constantly (amplification), so their tick count and their time agree.
- **A lone particle's time runs through its spreading and internal evolution** between its rare ticks. It still has one history of tick events (RD9 stands). Its *clock* just isn't those ticks.
- **The budget's clock effect (T1)** now applies to all processes, which is what the NIST clocks and the muons both show.

**What it changes:** G14's "a chain's own time is its tick count" becomes "a chain's own time is the locally slowed substrate time it lives through; its ticks are events in that time."

---

> **Correction, 2026-09-13.** The muon measurement (C58) tests time dilation from **speed** (γ = 29.33), not from gravity, so the budget does not explain it. The conflict in Q3 still stands, because it is about lone particles ageing steadily while collapsing rarely. But the fix needs a speed effect too (worksheet G25), and not only the budget (G23, decided as RD16).

## Recommended step

Allen decides G23. After that, version 0 is consistent with everything checked so far, and can be written as code, mirror-checked (T2), and tested on T1 (direction), T4, T7 and T8.

## Sources

- Pikovski, Zych, Costa, Brukner (2015): https://arxiv.org/abs/1311.1095
- Gambini, Porto, Pullin (2004): https://arxiv.org/abs/hep-th/0406260
- Leckey and Flitney (2023): https://arxiv.org/abs/2303.03096
- Bailey et al. (1977), muon time dilation: https://ui.adsabs.harvard.edu/abs/1977Natur.268..301B/abstract
- Bassi, Dorato, Ulbricht (2023), collapse models review: https://arxiv.org/abs/2310.14969
- Earlier gate sources: Tumulka (2006), Carlesso and Donadi (2019), Donadi et al. (2021), in ledger C42, C45, C43
