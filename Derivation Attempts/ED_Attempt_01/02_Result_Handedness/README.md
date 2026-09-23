# Event Density: one result

Event Density (ED) is an attempt to describe the world as a discrete substrate in which time runs one way: once something happens, it can't be undone. This repository holds one result about that kind of world, and only what the result needs.

**The result: a world whose rules look the same in a mirror can't have handedness written into those rules. If it has a handedness, the handedness was chosen by the state the world is in.**

## The idea in plain words

Picture a highway with several lanes. Traffic hops forward or backward from one stretch of road to the next, and at each hop it can also switch lanes in some pattern. That pattern of hops is the *transport*.

Now ask whether the traffic has a preferred direction: on balance, does it flow more one way along the road than the other? That left–right preference is what *handedness* means here. A number called the *winding number* measures it, and zero means no net preference. On a road that loops back on itself, a preference shows up as a steady drift. On a road with ends, it shows up as traffic piling up at one end.

The result says that **if the rules for hopping look the same in a mirror, the preference is exactly zero**, for any number of lanes and any hopping pattern. A mirror swaps forward with backward and flips the lanes left to right. If the rules survive that flip, every bit of preference one way is matched by the same amount the other way, and they cancel.

Two things give the result its content:

- **A preferred direction is only possible because time runs one way.** If hopping forward and hopping backward were perfect time-mirrors of each other, the preference would be zero no matter what. The irreversibility is what opens the door.
- **A preferred direction really does appear when the mirror symmetry is broken.** For traffic that only ever hops forward, the winding number equals the number of lanes.

Put together: **one-way time makes handedness possible, and mirror-symmetric rules keep it out of the laws.** So if an ED world has a handedness, it wasn't written into the rules. It was picked by the state, the way a magnet picks a direction that its laws don't prefer.

This is a "you can't get there from here" result. The best-known result of that kind about handedness is the Nielsen–Ninomiya theorem: on a regular lattice with local, reversible hopping, left-handed and right-handed particles always come in equal numbers. The two are relatives, not the same. Nielsen–Ninomiya forbids a net handedness even without mirror symmetry, but only for reversible hopping. This result allows irreversible hopping, which can escape that kind of zero, and shows that mirror-symmetric rules still force it. It is far smaller, but it is the same kind of guardrail: it says where handedness has to come from.

## Precisely

Write the transport of N lanes (channels) as H(k) = e^{ik}A + e^{−ik}B, where A is the forward hop, B the backward hop, and k the wavenumber. If the transport is symmetric under reflection, the winding number of det H(k) is zero for every N and every A.

The same holds for hops that reach any number of sites, H(k) = Σ_{m=−R}^{R} e^{imk} C_m, and for any way a mirror can act on the lanes (any matrix S with S² = 1).

## What it assumes

- **From ED:** space is uniform, phases are carried between neighbouring points, channels are distinct objects, the phase is a complex number, and time runs one way. None of ED's rules is a mirror reflection.
- **Modelling choices:** the form of H(k) above, how a reflection acts on it, and the winding number as the measure of handedness.

## How far it reaches

The result is modest. It is the general principle that a mirror-symmetric system can't carry a mirror-odd quantity, made explicit for this model and shown for every number of channels. A closely related statement is already published, for a mirror symmetry combined with a transpose, so the exact form here may well be known too. It is about this model of transport only. It does not say how nature's handedness arose, or which force in nature is handed.

## Check it yourself

```
python tools/check_result.py
```

The script (needs numpy) tests the result for 1 to 6 channels, for random mirrors and for hops reaching up to three sites. It also runs the two cases above: forward-only traffic, and traffic without one-way time.

## Files

- [Paper.md](Paper.md): the full proof, every assumption, the controls and the limits.
- [Result.md](Result.md): the statement and proof on one page.
- [Assumptions.md](Assumptions.md): everything the result assumes.

## References

- H. B. Nielsen and M. Ninomiya, "A no-go theorem for regularizing chiral fermions," *Physics Letters B* 105, 219 (1981).
- K. Kawabata, M. Sato and K. Shiozaki, "Higher-order non-Hermitian skin effect," *Physical Review B* 102, 205118 (2020).
- The references for the winding number and the Hatano–Nelson model are in [Paper.md](Paper.md).
