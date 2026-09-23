# Handedness and the weak force

*2026-09-14. Main line from [../Audit.md](../Audit.md), section 4. Ledger: C236–C241, G43.*

## 1. The tension, in one paragraph

**ED's one real result** (the public handedness theorem) says mirror-symmetric transport can't have a net handedness. Irreversibility is needed too: without it the winding is always zero.

**ED's primitives contain no mirror** (A1).

**Nature is handed:** the weak force treats left and right differently (Wu 1957, C224).

**So ED must get handedness from somewhere.** This note looks at what's known, and what that means for ED.

## 2. What the lattice literature says

| result | what it says | ledger |
|---|---|---|
| **Nielsen–Ninomiya (1981)** | On an ordinary (static) lattice, handed particles always come in equal left and right numbers. "Absence of neutrinos on a lattice": a no-go theorem for putting the weak force on a lattice | C236 |
| **Ginsparg–Wilson and Lüscher (1998)** | A modified, exact chiral symmetry avoids the doubling. The no-go is dodged because the symmetry works differently from what the theorem assumed | C237 |
| **Kaplan (1992): domain walls** | Handed particles live on a defect in an extra dimension, with the unwanted partners decoupled | C238 |
| **Lüscher (2000)** | Lecture notes on gauge-invariant lattice versions of anomaly-free chiral gauge theories. The weak force on a lattice remains technically hard | C238 |
| **Bessho and Sato (2021)** | **In dynamical systems (periodically driven or non-Hermitian), the no-go theorem is lifted.** Bulk chiral fermions are *permitted*, because of a bulk topology only those systems have | C239 |
| **Mohapatra and Senjanović (1975)** | **The laws can be exactly left–right symmetric while parity is maximally violated at low energy,** because the symmetry is broken spontaneously | C240 |

## 3. What that means for ED (C241)

**Two facts fit together in a way that matters for ED:**

1. **Irreversibility opens the door.** ED's transport is non-Hermitian: commitment can't be undone (P11, A5). That is exactly the class of system where Bessho and Sato show handed fermions are allowed. The bulk topology they use is the same kind of winding ED's theorem is about.
2. **A mirror closes it.** ED's own theorem says that if the rules are mirror-symmetric, that winding is zero.

**So ED has the ingredient that permits handedness (irreversibility), and is missing the one that selects it (mirror breaking).**

### ED's options (G43)

| | option | what it means | honest assessment |
|---|---|---|---|
| **(i)** | **A handed ingredient** (drop A1) | Put a left–right difference into the rules | Works, but explains nothing. It's what the Standard Model does |
| **(ii)** | **Spontaneous handedness** | The rules stay mirror-symmetric, and the state settles into one handedness, like a pencil falling one way | **The published home is left–right symmetric models** (C240). It matches ED's "first difference" and chance (Way Forward 1). Left–right models predict extra heavy force carriers, which the LHC is searching for |
| **(iii)** | **Handedness in the starting conditions** | The universe began handed | An initial condition, not an explanation |

**Proposal: (ii).**

### Where this reconnects to earlier work

The first simulation idea (Sim_Spontaneous_Direction) asked whether a mirror-symmetric rule could develop a preferred direction on its own. It stopped at its literature gates: **reinforced walks and nonlinear phase feedback are known to give spontaneous chirality** (C18, C29). The missing piece then was a definite commitment rule, and **ED now has one.**

**The new angle:**
- **Handedness here means non-Hermitian winding** (the theorem's quantity).
- **Spontaneous winding in an irreversible system** would be exactly the situation where Bessho and Sato's handed fermions can exist.

**That joins ED's result, ED's irreversibility, and a known way the no-go theorem is lifted.**

### Honest caveats

- **The distance to the weak force is large.** A winding in a toy transport rule is not the weak interaction's SU(2) structure, its anomaly cancellation, or three generations of particles. How ED's winding would map onto real particle handedness is not established.
- **ED's rule currently has no feedback law** (A7). Spontaneous handedness needs the state to affect its own transport, and P12 is the natural place for that (C34).
- **Each piece is published.** What would be ED's own is only the combination: irreversibility, a mirror-symmetric rule, and spontaneous winding.

## 4. Proposed next step

1. **A literature check first:** spontaneous symmetry breaking producing non-Hermitian winding. Has anyone shown a mirror-symmetric non-Hermitian system choosing a handedness by itself, for example through nonlinear gain and loss, or feedback in a skin-effect lattice?
2. **If it's open:** a toy in the style of rule version 1. Take a mirror-symmetric, irreversible transport rule whose hops are adjusted by a P12-style feedback from the pattern, and ask, with frozen predictions, whether the winding of det H becomes nonzero by itself, and whether left and right are chosen equally often across runs.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C236 | Nielsen and Ninomiya, "Absence of neutrinos on a lattice (I)", *Nucl. Phys. B* 185, 20 (1981) | Search listing |
| C237 | Lüscher, "Exact chiral symmetry on the lattice and the Ginsparg–Wilson relation", *Phys. Lett. B* 428, 342 (1998), arXiv:hep-lat/9802011 | Abstract |
| C238 | Kaplan, "A method for simulating chiral fermions on the lattice", *Phys. Lett. B* 288, 342 (1992), arXiv:hep-lat/9206013 | Abstract |
| C238 | Lüscher, "Chiral gauge theories revisited", arXiv:hep-th/0102028 (2000) | Contents listing |
| C239 | Bessho and Sato, "Nielsen–Ninomiya theorem with bulk topology: duality in Floquet and non-Hermitian systems", *PRL* 127, 196404 (2021), arXiv:2006.04204 | Abstract |
| C240 | Senjanović and Mohapatra, "Exact left-right symmetry and spontaneous violation of parity", *Phys. Rev. D* 12, 1502 (1975) | Search listing |

## 5. Toy results (2026-09-14)

**What was run.** One lane of amplitudes on a ring. The hops forward and back are equal unless the pattern carries a current; a current makes its own direction easier (feedback), and the rule is mirror-symmetric and irreversible. Predictions were frozen before each run (`01_Ledger/checks/handedness_toy.py`).

**Run 1: noise only (C248).**
- Every run ended with a hand (+1 in 94, −1 in 106), and no hand was preferred.
- **But this didn't show what it was meant to.** The current never grew, so the hand was about a millionth in size, just leftover noise. My prediction's criterion was too weak; that's recorded as my design error.

**Follow-up F: a deliberate seed current (C248).**
- A seed of 0.3 or more locks in a full hand. A seed of 0.01 stays tiny over the run.
- The hand always follows the seed's direction, and a mirrored seed gives the opposite hand.

**Diagnostic: is there a threshold? (C251, not pre-registered)**
- **No.** Run longer, the small seeds keep growing, slowly at first and then faster. A 0.15 seed locks in by t = 150, and a 0.01 seed is still creeping at t = 240.
- **So the symmetric state is only marginally stable:** any imbalance eventually wins, and bigger ones win sooner.

**What this does and doesn't show.**
- **Does:** a mirror-symmetric, irreversible, ED-style rule can pick a hand by itself, and the first imbalance decides which. This is the mechanism RD41 needs.
- **Doesn't:** the feedback reads the whole ring's current at once, so every locus shares one hand by construction and domains can't form. A local version is needed to see domains or a takeover. It is also one lane, a toy rule, and the mechanism is known (C244, C245).

**Next (G46):** the local-feedback toy. See [Baryogenesis_Seed.md](Baryogenesis_Seed.md).

## 6. Local toy results (2026-09-14)

**What changed from §5.** Each bond's hops now depend only on the flow near it, so different parts of the ring can pick different hands. Linear theory and predictions were frozen before running (`01_Ledger/checks/handedness_local_toy.py`).

**Run 1 (C263).**
- **The calculation held:** the even state is unstable (growth 1.57 measured, 1.62 predicted).
- **Noise:** in all 20 runs, one hand ended over the whole ring (left 13, right 7, within chance).
- **One seed:** its hand took the whole ring in every run.
- **Saturation:** a ring already locked into one hand kept it against an opposite seed, 5 of 5.
- **Score:** 4 of 10 predictions right. I had expected lasting separate domains. Two of the misses were my design errors, both recorded.

**Diagnostic: a ring 8 times longer (C267, not pre-registered).**
- **Domains form everywhere at once.** By t = 5 there is about one domain per 5 loci.
- **Then they merge,** fast at first and then slower: 828 domains, then 130, 16, and 2 by t = 800.
- **The seed doesn't win on the long ring.** Its hand covers about half the ring for most of the run, because domains formed everywhere before it could spread. **The seed's clean wins in run 1 were a small-ring effect.**

**What this means (C268).**
- **A first difference decides the hand only across a region that is in contact** and merges before the choice is fixed.
- **For the whole visible universe to share one hand,** the choice has to be made while all of it was in contact. That is the same condition physics already has: symmetry breaking before inflation (C254).
- **Locked-in hands resist change.** That's the "too saturated" part of D15, and it held.
- **Published homes:** domain walls (C254), Viedma ripening (C264), 1D flocking (C262).

**Next (G47).** Proposal: close the toy line. The next real step is feedback in ED's actual rule (A7, the P12 reading), or an outside review of the handedness result (C12).
