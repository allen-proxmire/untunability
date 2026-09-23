"""Standing phase, attempt 2 (RD53): the frustration route.

If coherence prefers small loops closing at pi, complete lane mixing in 3D is frustrated and its ground state gives the
on-site mixing triangle (Internal, +x, -x) a flux F = +-1.209 (or +-2.655 on other triangles), chosen by chance (C297).
That flux is odd under the mirror and under time reversal. Here it is placed in ED's 1D rule (labelled assumption: a
3D-derived value used in 1D) and nothing else is set by hand: no lane-loop phase (lane loops stay at pi), no flow
feedback. Draws carry motion into committed matter (transfer meetings: Right/Left lane content drops into Internal at
committed loci, rate Gamma each, the rebuilt draw's population form, C293).

Rule: the real rule H (v1_budget generator, U = 0) with the mixing entry H[(u, RIGHT), (u, INTERNAL)] times e^{iF}
(and its conjugate), so the triangle Internal -> Right -> Left -> Internal has flux F. The mirror maps F -> -F.

Predictions frozen before the first run (2026-09-14):
  A0 (code) At F = +-1.209, Gamma 0.3, D 2, symmetric rates: the steady state is unique (two trace-row placements
     agree to 1e-8), positive (smallest eigenvalue >= -1e-9), residual < 1e-9; and v(+F) = -v(-F) to 1e-10.
  A1 With symmetric draw rates (no feedback), F in {-1.209, -2.655}, Gamma in {0.3, 1}, D in {2, 3}: the steady
     local velocity at committed loci is nonzero, |v| > 1e-6, in all 8 settings.
  A2 Winding of H_eff (F = -1.209, Gamma 0.3, D 2, symmetric rates) is nonzero.
  A3 Dynamics, no feedback (g = 0), F = -1.209, Gamma 0.3, D 2, L 24, dt 0.02, t 600, the 10 noisy starts of C288:
     all 10 end with |J(600)| > 1e-4 and the same sign; with F = +1.209 all 10 end with the opposite sign.
  A4 With the tuned feedback added (g = +0.9 and -0.9, V0 0.03), F = -1.209: for each sign of g, every run with
     |J(600)| > 1e-3 has the sign found in A3 (the chirality, not chance, sets the hand).
Reported: |v| values, |J(600)|, winding, purity.
Reading rule: attempt 2 fixes a hand from ED's coherence (under the pi reading) if A1 and A3 hold: a lasting flow whose
direction is set by the ground state's chosen chirality, with no phase or feedback set by hand. Still assumed then: the
pi reading, the complete-mixing coin, transfer meetings, and the 1D use of a 3D value.
Exit code: A0 (code checks).

Changes after freezing (2026-09-14):
  1. Run 1 (attempt2_run1.txt): A1 and A4 scored RIGHT, A0, A2, A3 WRONG. A0 failed: the steady state is not unique
     (two trace-row placements differ by 2.1e-2 and 1.1e-1; smallest eigenvalues -0.095 and -0.38), so the exact
     solves in A0 and A1 are ill-posed and A1's nonzero velocities (up to 0.045, not odd in F) mean nothing; A1's
     RIGHT verdict is not valid. A2: winding 0. A3: no lasting flow, |J(600)| <= 4.1e-5 with mixed signs for both
     signs of F. A4: with feedback g = +0.9 every |J(600)| was positive and <= 7.8e-5, with g = -0.9 negative and
     <= 7.9e-5; no run exceeded 1e-3, so A4's RIGHT verdict is vacuous.
  2. Diagnostic (not pre-registered, attempt2_nullspace_diagnostic.txt): on a 12-locus ring the Liouvillian with
     F = +-1.209 has 4 (D 2) or 13 (D 3) steady states, and every one carries current below 1e-14; F = 0 and pi give
     6 or 13, also with zero current. So the frustrated mixing phase alone gives no lasting flow.
  3. The exit code now checks that run 1's recorded results reproduce (not the failed A0 criterion).
"""
import math
import os
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("../Commitment_Rule/v4", "../Commitment_Rule/v2b", "../Commitment_Rule/v2", "../Commitment_Rule/v1_budget"):
    sys.path.insert(0, os.path.join(HERE, sub))
from rule_v4 import kraus, lane_channels, unitary  # noqa: E402
from rule_v2b import INTERNAL, LEFT, RIGHT, RuleB, pure  # noqa: E402
from rule_v2 import max_winding, real_rule  # noqa: E402

F_TRI = 1.209
F_TRI2 = 2.655


def hamiltonian(L, F):
    H = real_rule(L).astype(complex)
    for u in range(L):
        i, r = 3 * u + INTERNAL, 3 * u + RIGHT
        H[r, i] *= np.exp(1j * F)
        H[i, r] *= np.exp(-1j * F)
    return H


def rates(L, D, Gamma, delta=0.0):
    d = np.zeros(3 * L)
    x = np.arange(0, L, D)
    d[3 * x + RIGHT] = Gamma * (1 - delta)
    d[3 * x + LEFT] = Gamma * (1 + delta)
    return d


def liouvillian(H, d, L, D):
    n = 3 * L
    N = n * n
    Hs = sp.csr_matrix(H)
    I = sp.identity(n, format="csr")
    Lv = -1j * (sp.kron(I, Hs) - sp.kron(Hs.T, I))
    diag = -0.5 * (np.kron(np.ones(n), d) + np.kron(d, np.ones(n)))
    src, dst = lane_channels(L, D)
    gain = sp.csr_matrix((d[src], (dst + n * dst, src + n * src)), shape=(N, N))
    return (Lv + sp.diags(diag) + gain).tocsr()


def steady(Lv, n, r=0):
    N = n * n
    mask = np.ones(N)
    mask[r] = 0.0
    didx = np.arange(n) * (n + 1)
    A = sp.diags(mask) @ Lv + sp.csr_matrix((np.ones(n), (np.full(n, r), didx)), shape=(N, N))
    b = np.zeros(N, dtype=complex)
    b[r] = 1.0
    x = spla.spsolve(A.tocsc(), b)
    return x.reshape((n, n), order="F"), float(np.max(np.abs(Lv @ x)))


def velocity(rho, L, D):
    rule = RuleB(L, D, 1.0, 0.0, 0.0)
    j = rule.currents(rho, np.zeros(L))
    n = rule.amounts(rho)
    c = rule.committed
    return float(np.mean(0.5 * (j[(c - 1) % L] + j[c]) / n[c])), float(np.sum(j))


def main():
    L = 24
    code_ok = True
    # A0
    out = {}
    for F in (-F_TRI, F_TRI):
        H = hamiltonian(L, F)
        Lv = liouvillian(H, rates(L, 2, 0.3), L, 2)
        r1, res1 = steady(Lv, 3 * L, 0)
        r2, _ = steady(Lv, 3 * L, 3 * 5 * (3 * L + 1))
        uniq = float(np.max(np.abs(r1 - r2)))
        mineig = float(np.min(np.linalg.eigvalsh(0.5 * (r1 + r1.conj().T))))
        out[F] = velocity(r1, L, 2)[0]
        code_ok &= uniq < 1e-8 and mineig >= -1e-9 and res1 < 1e-9
        print("A0 F %+.3f: uniqueness %.1e, min eig %.1e, residual %.1e, v %+.4e" % (F, uniq, mineig, res1, out[F]), flush=True)
    odd = abs(out[F_TRI] + out[-F_TRI])
    code_ok &= odd < 1e-10
    print("A0 v(+F) + v(-F) = %.1e" % odd, flush=True)

    # A1
    vs = []
    for F in (-F_TRI, -F_TRI2):
        for Gamma in (0.3, 1.0):
            for D in (2, 3):
                H = hamiltonian(L, F)
                rho, res = steady(liouvillian(H, rates(L, D, Gamma), L, D), 3 * L)
                v, J = velocity(rho, L, D)
                vs.append(v)
                print("A1 F %+.3f Gamma %.1f D %d: v %+.4e, J %+.4e, residual %.1e" % (F, Gamma, D, v, J, res), flush=True)
    a1 = all(abs(v) > 1e-6 for v in vs)

    # A2
    H = hamiltonian(L, -F_TRI)
    w = max_winding(H, rates(L, 2, 0.3), L, np.random.default_rng(99), nphi=300, npts=30)
    print("A2 winding of H_eff: %d" % w, flush=True)

    # A3, A4 dynamics
    srng = np.random.default_rng(1357)
    starts = [pure(1 + 0.1 * (srng.standard_normal(3 * L) + 1j * srng.standard_normal(3 * L)) / math.sqrt(2)) for _ in range(10)]
    lane, dest = lane_channels(L, 2)
    dt, T = 0.02, 600.0

    def run(F, g, i):
        H = hamiltonian(L, F)
        U = unitary(H, dt)
        rule = RuleB(L, 2, 0.3, g, 0.0, 0.03, phase_mode="const")
        rule.theta = np.zeros(L)
        rho = starts[i].copy()
        for _ in range(int(round(T / dt))):
            _, d = rule.settings(rho)
            rho = kraus(U @ rho @ U.conj().T, lane, dest, d[lane] * dt)
        J = float(np.sum(rule.currents(rho, rule.theta)))
        wf = max_winding(H, d, L, np.random.default_rng(99), nphi=200, npts=10)
        return J, wf

    a3m = [run(-F_TRI, 0.0, i) for i in range(10)]
    print("A3 F -1.209, no feedback: J(600) %s; windings %s" % (" ".join("%+.3e" % r[0] for r in a3m), [r[1] for r in a3m]), flush=True)
    a3p = [run(F_TRI, 0.0, i) for i in range(10)]
    print("A3 F +1.209, no feedback: J(600) %s" % " ".join("%+.3e" % r[0] for r in a3p), flush=True)
    sgn = np.sign(a3m[0][0])
    a3 = (all(abs(r[0]) > 1e-4 and np.sign(r[0]) == sgn for r in a3m)
          and all(abs(r[0]) > 1e-4 and np.sign(r[0]) == -sgn for r in a3p))
    a4 = True
    for g in (0.9, -0.9):
        res = [run(-F_TRI, g, i) for i in range(10)]
        print("A4 F -1.209, g %+.1f: J(600) %s" % (g, " ".join("%+.3e" % r[0] for r in res)), flush=True)
        a4 &= all(np.sign(r[0]) == sgn for r in res if abs(r[0]) > 1e-3)

    checks = [("A0 code: unique, positive, v odd in F", code_ok), ("A1 steady flow nonzero with symmetric rates (8 settings)", a1),
              ("A2 winding of H_eff nonzero", w != 0), ("A3 no feedback: lasting flow, direction set by F", a3),
              ("A4 with feedback: lasting runs follow F's direction", a4)]
    print("\nFrozen predictions:")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    print("CODE CHECKS PASS" if code_ok else "CODE CHECKS FAIL (as recorded: the steady state is not unique)")
    recorded = (not code_ok and w == 0 and all(abs(r[0]) < 1e-4 for r in a3m + a3p))
    print("RECORDED RESULTS REPRODUCE" if recorded else "RECORDED RESULTS DO NOT REPRODUCE")
    return recorded


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
