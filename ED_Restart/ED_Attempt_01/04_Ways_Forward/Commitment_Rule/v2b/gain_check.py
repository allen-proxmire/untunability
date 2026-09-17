"""Gain check (G50 = a, RD48): can version 2b's feedback loop amplify itself at zero flow?

Open loop. Hold the phases fixed and uniform (theta on every bond: Right-lane hops e^{i theta}, Left-lane e^{-i theta})
and hold the draw rates fixed and uniform: gamma[x, RIGHT] = Gamma (1 - delta), gamma[x, LEFT] = Gamma (1 + delta) at
every committed locus (every D-th), draws dropping lane content into the Internal channel (rule_v2b). The Lindbladian
is then linear, so its steady state is found exactly (sparse solve with the trace fixed to 1). Measure the steady local
velocity at the committed loci, v = mean over x of (j_{x-1} + j_x) / (2 n_x), the quantity the rate feedback reads.
Response chi = (v(+delta) - v(-delta)) / (2 delta), delta = 1e-3.

Closing the loop with delta = g tanh(v / V0) gives loop gain |g| |chi| / V0 at zero flow; the even state is unstable
(a hand can start from noise) when this exceeds 1, i.e. when V0 < |g| |chi|. Since |g| <= 1 (rates stay >= 0), the
largest V0 that allows it is V0* = |chi|. Version 2b used g = 0.5, V0 = 0.05 (loop gain 10 |chi|).

Analysis before running. (T) With theta = 0 the generator is real in the real gauge (C275 analysis B) and the jump
operators are real, so the unique steady state is real in that gauge and every current vanishes, for any delta: chi = 0.
Flow-set phases (theta = theta0 tanh(|v|/V0)) vanish at zero flow, so their loop gain at zero flow is zero: they
cannot start a hand from noise (consistent with C278). (M) With delta = 0 the rule is mirror-symmetric, so v = 0;
v is odd in delta. (T') Time reversal maps theta -> -theta and v -> -v at fixed rates, so chi is odd in theta.

Grid fixed before running: theta in {0, 0.4, 0.8, 1.2}, Gamma in {0.3, 1, 3}, D in {2, 3, 4}; L = 48; plus theta = -0.4
and delta = 1e-2 at (Gamma 1, D 3), and a uniqueness check at (theta 0.4, Gamma 1, D 3).

Predictions frozen before the first run (2026-09-14):
  G1 (code) Every steady state: trace 1 to 1e-10, Hermitian to 1e-10, smallest eigenvalue >= -1e-9, residual
     max |L x| < 1e-9; two different trace-row placements agree to 1e-8 at the base setting.
  G2 theta = 0: |v| < 1e-10 for every Gamma, D and delta = +-1e-3.
  G3 delta = 0, theta != 0: |v| < 1e-10.
  G4 |v(+delta) + v(-delta)| < 1e-10 everywhere, and chi(-0.4) = -chi(0.4) to 1e-8 (Gamma 1, D 3).
  G5 theta != 0: |chi| > 1e-6 in at least 20 of the 27 settings.
  G6 At (theta 0.4, Gamma 1, D 3), chi from delta = 1e-2 is within 1% of chi from delta = 1e-3.
  G7 At version 2b's settings (theta 0.4, Gamma 1, D 3): loop gain 10 |chi| < 1.
  G8 Largest |chi| over the grid < 0.1.
Reading rule frozen with the predictions: if every |chi| < 1e-6, rate feedback can't start a hand in this rule (door
shut). Otherwise a hand can start whenever V0 < |g| |chi|; V0* = max |chi| is reported, and the next step would be a
frozen dynamic test at a setting below V0*, flagged openly as a tuned choice.
Exit code: G1 (code properties).

Changes after freezing (2026-09-14):
  1. Run 1 (gain_check_run1.txt) computed every setting and extra, then crashed in the final summary print (a format
     string with one argument too many), before the verdicts were printed. Fixed the print; added a per-setting line
     printing the solve checks already computed (ok flag, residual, smallest eigenvalue). No computation, grid,
     prediction or reading rule changed. Rerun as run 2.
  2. Run 1's theta = 0 rows gave large, non-odd velocities (up to 3.7), unlike theta != 0 (clean, odd to rounding,
     |chi| 0.012-0.096). Suspected cause, checked by gain_nullspace_diagnostic.py (not pre-registered): the theta = 0
     Liouvillian has more than one steady state, so the solve is ill-posed there.
  3. Run 2 (gain_check_run2.txt): G3, G5, G6, G7, G8 RIGHT; G1, G2, G4 WRONG. Every theta != 0 solve passed its checks;
     every theta = 0 solve failed (residuals tiny but smallest eigenvalue down to -2.1: a non-positive mixture of steady
     states). The diagnostic (C282) found 13 steady states at theta = 0 on a 12-locus ring, all carrying zero current
     (below 5e-15), and a unique one at theta = 0.4. So G1, G2 and G4 failed on Claude's assumption of a unique steady
     state, not on the physics they checked. The exit code now checks the theta != 0 solves and that run 2's recorded
     results reproduce.
"""
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from rule_v2b import LEFT, RIGHT, RuleB

L, DELTA = 48, 1e-3


def rates(rule, Gamma, delta):
    d = np.zeros(rule.n)
    x = rule.committed
    d[3 * x + RIGHT] = Gamma * (1 - delta)
    d[3 * x + LEFT] = Gamma * (1 + delta)
    return d


def liouvillian(rule, theta, d):
    n = rule.n
    N = n * n
    H = rule.hamiltonian(np.full(L, float(theta)))
    I = sp.identity(n, format="csr")
    Lv = -1j * (sp.kron(I, H) - sp.kron(H.T, I))
    diag = -0.5 * (np.kron(np.ones(n), d) + np.kron(d, np.ones(n)))
    gain = sp.csr_matrix((d[rule.src], (rule.dst + n * rule.dst, rule.src + n * rule.src)), shape=(N, N))
    return (Lv + sp.diags(diag) + gain).tocsr()


def steady(Lv, n, r):
    N = n * n
    mask = np.ones(N)
    mask[r] = 0.0
    didx = np.arange(n) * (n + 1)
    A = sp.diags(mask) @ Lv + sp.csr_matrix((np.ones(n), (np.full(n, r), didx)), shape=(N, N))
    b = np.zeros(N, dtype=complex)
    b[r] = 1.0
    x = spla.spsolve(A.tocsc(), b)
    return x


def measure(rule, theta, Gamma, delta, r=0):
    n = rule.n
    Lv = liouvillian(rule, theta, rates(rule, Gamma, delta))
    x = steady(Lv, n, r)
    rho = x.reshape((n, n), order="F")
    resid = float(np.max(np.abs(Lv @ x)))
    tr = abs(complex(np.trace(rho)) - 1)
    herm = float(np.max(np.abs(rho - rho.conj().T)))
    mineig = float(np.min(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))))
    j = rule.currents(rho, np.full(L, float(theta)))
    nn = rule.amounts(rho)
    c = rule.committed
    v = float(np.mean(0.5 * (j[(c - 1) % L] + j[c]) / nn[c]))
    ok = tr < 1e-10 and herm < 1e-10 and mineig >= -1e-9 and resid < 1e-9
    return v, ok, rho, (tr, herm, mineig, resid)


def main():
    code_ok, nz_ok = True, True
    g2, g3, g4odd, chis = [], [], [], {}
    for D in (2, 3, 4):
        for Gamma in (0.3, 1.0, 3.0):
            rule = RuleB(L, D, Gamma, 0.0, 0.0)
            for theta in (0.0, 0.4, 0.8, 1.2):
                vp, okp, _, infop = measure(rule, theta, Gamma, DELTA)
                vm, okm, _, infom = measure(rule, theta, Gamma, -DELTA)
                print("  solve checks: ok %s/%s; residual %.1e/%.1e; min eig %.1e/%.1e"
                      % (okp, okm, infop[3], infom[3], infop[2], infom[2]), flush=True)
                code_ok &= okp and okm
                if theta != 0.0:
                    nz_ok &= okp and okm
                chi = (vp - vm) / (2 * DELTA)
                g4odd.append(abs(vp + vm))
                if theta == 0.0:
                    g2 += [abs(vp), abs(vm)]
                    v0 = float("nan")
                else:
                    v0, ok0, _, _ = measure(rule, theta, Gamma, 0.0)
                    code_ok &= ok0
                    g3.append(abs(v0))
                    chis[(theta, Gamma, D)] = chi
                print("D %d Gamma %.1f theta %.1f: v(+d) %+.3e, v(-d) %+.3e, v(0) %+.1e, chi %+.4e, V0* = |chi| %.2e"
                      % (D, Gamma, theta, vp, vm, v0, chi, abs(chi)), flush=True)

    rule = RuleB(L, 3, 1.0, 0.0, 0.0)
    vp, _, rho_a, _ = measure(rule, -0.4, 1.0, DELTA)
    vm, _, _, _ = measure(rule, -0.4, 1.0, -DELTA)
    chi_neg = (vp - vm) / (2 * DELTA)
    vp2, _, _, _ = measure(rule, 0.4, 1.0, 1e-2)
    vm2, _, _, _ = measure(rule, 0.4, 1.0, -1e-2)
    chi_big = (vp2 - vm2) / (2e-2)
    _, _, r1, info1 = measure(rule, 0.4, 1.0, DELTA, r=0)
    _, _, r2, _ = measure(rule, 0.4, 1.0, DELTA, r=3 * 5 * (rule.n + 1))
    uniq = float(np.max(np.abs(r1 - r2)))
    base = chis[(0.4, 1.0, 3)]
    print("theta -0.4 (Gamma 1, D 3): chi %+.4e (theta +0.4: %+.4e)" % (chi_neg, base))
    print("delta 1e-2 (theta 0.4, Gamma 1, D 3): chi %+.4e" % chi_big)
    print("uniqueness: two trace-row placements differ by %.1e; base residual %.1e" % (uniq, info1[3]))
    big = max(abs(c) for c in chis.values())
    arg = max(chis, key=lambda k: abs(chis[k]))
    print("largest |chi| %.3e at theta %.1f, Gamma %.1f, D %d; version 2b loop gain 10|chi| = %.3e"
          % (big, arg[0], arg[1], arg[2], 10 * abs(base)))

    checks = [
        ("G1 code properties and uniqueness", code_ok and uniq < 1e-8),
        ("G2 theta 0: |v| < 1e-10 everywhere", max(g2) < 1e-10),
        ("G3 delta 0, theta != 0: |v| < 1e-10", max(g3) < 1e-10),
        ("G4 v odd in delta (1e-10) and chi odd in theta (1e-8)", max(g4odd) < 1e-10 and abs(chi_neg + base) < 1e-8),
        ("G5 theta != 0: |chi| > 1e-6 in at least 20 of 27", sum(abs(c) > 1e-6 for c in chis.values()) >= 20),
        ("G6 linear: delta 1e-2 within 1% of delta 1e-3", abs(chi_big / base - 1) < 0.01 if base != 0 else False),
        ("G7 version 2b loop gain 10|chi| < 1", 10 * abs(base) < 1),
        ("G8 largest |chi| < 0.1", big < 0.1),
    ]
    print("\nFrozen predictions:")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    recorded = [
        ("theta != 0 solves pass their checks; uniqueness at the base setting", nz_ok and uniq < 1e-8),
        ("run-2 verdicts reproduce (G3, G5-G8 right)", all(checks[k][1] for k in (2, 4, 5, 6, 7))),
        ("run-2 chi values reproduce (base +3.2235e-02, largest 9.568e-02)", abs(base - 3.2235e-2) < 5e-6 and abs(big - 9.568e-2) < 5e-5),
    ]
    ok = True
    print("\nRecorded results reproduce:")
    for name, passed in recorded:
        ok &= passed
        print("%-4s %s" % ("PASS" if passed else "FAIL", name))
    print("ALL PASS" if ok else "SOME FAIL")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
