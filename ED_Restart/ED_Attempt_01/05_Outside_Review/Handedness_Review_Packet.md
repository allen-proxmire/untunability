# Outside review packet: the handedness result

*Prepared 2026-09-14 (RD51). Nothing has been sent. Allen chooses whether and to whom. Ledger: C1–C12, C30, C236–C241, C269, C275, C277, C281–C289.*

## For the reviewer

**Who we'd like to ask:** a physicist who works on non-Hermitian topology or lattice chirality.

**How long it takes:** the result is one page of mathematics plus a script. We're asking whether it's right, whether it's already known in this exact form, and whether the way we now use it is sound.

**Public repository:** https://github.com/allen-proxmire/event-density-streamlined (commit `5690a59`). Its `README.md` explains the result in plain words; `tools/check_result.py` checks it numerically.

## 1. The result, precisely

**Setup.**
- **Transport with N channels on a 1D lattice:** H(k) = Σ_{m=−R}^{R} e^{imk} C_m, with the C_m independent N × N complex matrices (no Hermiticity assumed).
- **A reflection:** S H(k) S⁻¹ = H(−k), for some S with S² = 1.

**Claim.**
- **(i)** If transport is symmetric under such a reflection, the winding number of det(H(k) − E) about any point E off the curve is zero, for every N, R and S.
- **(ii)** If transport is Hermitian (C_{−m} = C_m†), det H(k) is real and the winding is zero.
- **(iii)** Forward-only hopping gives winding N, so the invariant isn't trivially zero.

**Plain reading.** One-way (non-Hermitian) transport makes a net handedness possible; mirror-symmetric rules keep it out of the laws. Any handedness must be chosen by the state.

## 2. What we already know about its novelty

- **The mathematics is elementary,** and a closely related statement is published: reflection combined with a transpose (C30).
- **Nielsen–Ninomiya** forbids net chirality for local, reversible lattice hopping (C236). Non-Hermitian and Floquet systems escape it (Bessho and Sato, C239).
- **The winding of det(H − E)** is the standard point-gap invariant, and it's tied to the skin effect (Kawabata, Sato, Shiozaki, C8).
- **We couldn't find the exact form** (reflection without transpose, any S, any range) in a short search (C12, open).

## 3. How it's used in Event Density, and the honest status

Event Density (ED) is a discrete, irreversible substrate model. The public result assumed that ED's irreversibility shows up as one-way transport (assumption A5).

**What we found since** (details in the ledger):
- **ED's actual rule has Hermitian, time-reversal-symmetric spreading.** Irreversibility enters only through draws (measurement-like events) at committed matter. With draws modelled as dephasing, or as non-unital jumps whose rates respond to the local flow, **no lasting flow and no winding appear** (C269, C275, C278). Reason: the generator is gauge-equivalent to a real symmetric matrix, so H_eff = H − (i/2)Γ is complex symmetric for any diagonal loss, and its winding is zero (C275).
- **With a standing lane phase** (loop flux neither 0 nor π), **non-unital jumps** (lane content dropping into a rest channel) and **a steep flow-dependent rate asymmetry** (open-loop gain 3), a mean-field Lindblad model settles into a lasting flow. Its direction is chosen by chance (6 of 10 one way). The no-jump H_eff then has winding 1 in all runs (C281, C288). The damping sign and a lower gain decay.
- **So A5 isn't delivered by ED's rule as written.** It holds only under these tuned choices (C289). The mechanism resembles reservoir-engineered nonreciprocity (Metelmann and Clerk, C276).

## 4. Questions for the reviewer

1. **Is the result right,** and is the exact form (reflection without transpose, any S, any hop range) already published? Where?
2. **Is (i) immediate from the non-Hermitian symmetry classification** (which class, which table entry)? If so, we'd cite that and say so.
3. **In the tuned model, is the winding of the no-jump Hamiltonian H_eff the right measure of handedness** for an open system? Should we use a Liouvillian invariant, or the steady-state current, instead?
4. **Is there a standard result on spontaneous nonreciprocity** from a fixed flux, dissipation and state-dependent rates (mean-field)? We'd want to cite it rather than rediscover it.
5. **Anything wrong, overclaimed or naive** in how we connect the theorem to irreversibility?

## 5. How to check

- **The theorem:** run `python tools/check_result.py` in the public repository (commit `5690a59`).
- **The later computations** (not public; available on request):
  - `v2/run_tests_v2.py` (draw-rate feedback);
  - `v2b/run_tests_v2b.py` (phases and non-unital draws);
  - `v2b/gain_check.py` (open-loop response);
  - `v2b/tuned_test.py` (the lasting hand);
  - `v3_draw/run_tests_draw.py` (the rebuilt draw).

  Each has predictions frozen before running, with every miss recorded.
