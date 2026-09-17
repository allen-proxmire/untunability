"""Runs the version 2 tests in Spec.md and reports each frozen prediction. Exit code: V2-P1, P2, P4 (code properties)."""
import math
import sys

import numpy as np

from rule_v2 import RIGHT, Rule, max_winding, mirror_perm, pure, real_rule

L, D, GAMMA, V0, DT, T = 48, 3, 1.0, 0.05, 0.01, 200.0


def code_ok(rule, rho):
    herm = float(np.max(np.abs(rho - rho.conj().T)))
    amount = abs(float(np.real(np.trace(rho))) - 1.0)
    mineig = float(np.min(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))))
    return amount < 1e-12 and herm < 1e-12 and mineig >= -1e-8, (amount, herm, mineig)


def main():
    results = {}
    rng = np.random.default_rng(2468)
    u = np.arange(L)
    k = 2 * math.pi * 3 / L
    psi_c = np.zeros(3 * L, dtype=complex)
    psi_c[3 * u + RIGHT] = np.exp(1j * k * u)
    p = mirror_perm(L)
    noisy = [pure(1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)) for _ in range(10)]

    # V2-P2 mirror check
    rule = Rule(L, D, GAMMA, 0.5, V0)
    r1, _ = rule.evolve(noisy[0].copy(), 20.0, DT)
    r2, _ = rule.evolve(noisy[0][np.ix_(p, p)], 20.0, DT)
    merr = float(np.max(np.abs(r1[np.ix_(p, p)] - r2)))
    print("V2-P2 mirror check: max error %.2e" % merr, flush=True)

    # V2-P4 no draws
    rule0 = Rule(L, D, 0.0, 0.5, V0)
    _, pur0 = rule0.evolve(noisy[1].copy(), 50.0, DT)
    pdrift = float(np.max(np.abs(pur0 - pur0[0])))
    print("V2-P4 no draws: purity drift %.2e" % pdrift, flush=True)

    # V2-P5, P6 reciprocity and contrast
    wrng = np.random.default_rng(1357)
    w_real, w_theta = [], []
    for Lr in (12, 13, 16):
        H0 = real_rule(Lr)
        Ht = real_rule(Lr, theta=0.4)
        for _ in range(30):
            gam = wrng.uniform(0, 2, 3 * Lr)
            w_real.append(max_winding(H0, gam, Lr, wrng))
            w_theta.append(max_winding(Ht, gam, Lr, wrng))
    print("V2-P5 real rule, random losses: windings %s" % sorted(set(w_real)), flush=True)
    print("V2-P6 with lane phases 0.4: nonzero in %d of %d; values %s" % (sum(w != 0 for w in w_theta), len(w_theta), sorted(set(w_theta))), flush=True)

    # V2-P7..P10 dynamics
    ok_code, pur_ok, final_w = True, True, []

    def run(name, g, rho0):
        nonlocal ok_code, pur_ok
        rule = Rule(L, D, GAMMA, g, V0)
        J0 = float(np.sum(rule.currents(rho0)))
        g0 = rule.rates(rho0)
        rho, pur = rule.evolve(rho0.copy(), T, DT)
        good, (amount, herm, mineig) = code_ok(rule, rho)
        ok_code &= good
        rise = float(np.max(np.diff(pur))) if len(pur) > 1 else 0.0
        pur_ok &= rise <= 1e-12
        J1 = float(np.sum(rule.currents(rho)))
        g1 = rule.rates(rho)
        c = rule.committed
        w = max_winding(rule.H, g1, L, np.random.default_rng(99), nphi=300, npts=15)
        final_w.append(w)
        print("%s: J(0) %+.3e, J(200) %+.3e; purity %.4f -> %.4f (largest rise %.1e); R/L rate spread t0 %.3f t200 %.3f; "
              "winding %d; amount err %.1e, herm %.1e, min eig %.1e"
              % (name, J0, J1, pur[0], pur[-1], rise, float(np.ptp(g0[3 * c + RIGHT])), float(np.ptp(g1[3 * c + RIGHT])), w, amount, herm, mineig), flush=True)
        return J0, J1

    rho_c = pure(psi_c)
    results["P7"] = run("V2-P7 current start g 0.5", 0.5, rho_c)
    results["P7m"] = run("mirror current start g 0.5", 0.5, rho_c[np.ix_(p, p)])
    results["P8"] = run("V2-P8 current start g -0.5", -0.5, rho_c)
    noisy_J = []
    for i, r0 in enumerate(noisy):
        noisy_J.append(run("V2-P9 noisy start %d" % i, 0.5, r0)[1])

    checks = [
        ("V2-P1 amount, Hermitian, positive in every run", ok_code),
        ("V2-P2 mirror check to 1e-9", merr < 1e-9),
        ("V2-P3 purity never rises (1e-12)", pur_ok),
        ("V2-P4 no draws: purity constant to 1e-9", pdrift < 1e-9),
        ("V2-P5 real rule with losses: all windings 0", all(w == 0 for w in w_real)),
        ("V2-P6 lane phases: at least one nonzero winding", any(w != 0 for w in w_theta)),
        ("V2-P7 current start g 0.5: |J(200)| < 0.01 |J(0)|", abs(results["P7"][1]) < 0.01 * abs(results["P7"][0])),
        ("V2-P8 current start g -0.5: |J(200)| < 0.01 |J(0)|", abs(results["P8"][1]) < 0.01 * abs(results["P8"][0])),
        ("V2-P9 noisy starts: max |J(200)| < 1e-3", max(abs(j) for j in noisy_J) < 1e-3),
        ("V2-P10 winding at final rates 0 in all dynamic runs", all(w == 0 for w in final_w)),
    ]
    print("\nFrozen predictions:")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    recorded = [
        ("V2-P1, P2, P4 code properties", checks[0][1] and checks[1][1] and checks[3][1]),
        ("run-1 purity and winding results reproduce (P3, P5, P10 right; P6 nonzero in 75 of 90)",
         checks[2][1] and checks[4][1] and checks[9][1] and sum(w != 0 for w in w_theta) == 75),
        ("run-1 currents reproduce (P7 J(200) 5.609e-05, P8 5.338e-05, P9 all below 1e-3)",
         abs(results["P7"][1] - 5.609e-05) < 5e-08 and abs(results["P8"][1] - 5.338e-05) < 5e-08 and checks[8][1]),
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
