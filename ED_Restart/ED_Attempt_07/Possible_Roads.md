# Possible roads (parked, not started)

*ED_Attempt_07. Started 2026-09-18 (RD42). Ledger: C83. Roads worth testing later, recorded so they aren't lost. Nothing here is decided or underway.*

## Road D: does ED need the dice? (C83)

**Where it came from.** Allen's prime work, in side conversation: the sieve makes randomness without any chance in it. Many incommensurate periods (the wheel) interfere, and the survivors look random by most tests. ED, by contrast, **assumes** randomness in several places.

**Where ED currently uses chance:**

| | what is random | where |
|---|---|---|
| **Offspring** | The number of children each event has | C1, C2a, C3a–C3e |
| **Clock rates** | Each place's slight rate difference | C2b, C3c–C3e |
| **Move choices** | Which partner, which split, which flip | C3a–C3e |
| **The Born rule** | Supplied in form | A2 C11, one of the three supplied inputs |

**The question.**

> **Does ED's balance need genuine chance, or would incommensurate periods do?**

**The test, sketched (cheap, since C2a runs take seconds):**
- **Keep C2a exactly as it is** (budget passed forward and conserved, k = 1, L\* = 100 and 200, T = 400), with one change.
- **Replace the offspring draw** with a deterministic rule: each event carries a few incommensurate periods (a wheel), and its offspring count comes from where those periods stand, with no random numbers anywhere.
- **Read it with the same pre-registered checks:** survival, telescoped offspring average, mean slice length, and the geometry readings.
- **Expected results and ranges fixed before any code,** as always.

**What each outcome would mean:**

| outcome | record |
|---|---|
| **The balance still self-organizes** | ED's balance doesn't need fundamental chance, only enough incommensurate structure. That narrows what ED assumes, and touches the census guard |
| **It doesn't** | The balance needs genuine chance, which sharpens what the Born-rule input is doing in ED |
| **It self-organizes but the geometry changes** | Chance and pseudo-chance differ in ED, and where they differ is the result |

**Honest limits:** deterministic pseudo-randomness passing a few checks isn't the same as being random; the periods and their number would be knobs; and this is about the *balance*, not about the Born rule itself.

## A reading habit to carry forward (C83)

**From the same conversation:** for primes, the drift of a statistic is often guaranteed, and the content lives in the fluctuations after the trend is divided out, sorted by class (residue modulo 6, modulo 30).

**The ED version:** our runs report medians and exponents. They don't subtract the expected trend and look at what's left, sorted by local class (degree, curvature, distance from a neck).

- **It costs nothing extra:** existing C2a, C3d and C3e results already hold the data.
- **Worth doing** when the next set of results is read.
