"""Runs the version 2b tests in Spec.md and reports each frozen prediction. Exit code: B1 (code properties)."""
import math
import sys

import numpy as np

from rule_v2b import RuleB, mirror_perm, pure

L, D, GAMMA, V0, THETA0, DT, T = 48, 3, 1.0, 0.05, 0.4, 0.01, 300.0


def main():
    rng = np.random.default_rng(2468)
    noisy = [pure(1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)) for _ in range(10)]
    p = mirror_perm(L)

    ra = RuleB(L, D, GAMMA, 0.5, THETA0, V0)
    rb = RuleB(L, D, GAMMA, 0.5, THETA0, V0)
    e1, _ = ra.evolve(noisy[0].copy(), 20.0, DT)
    e2, _ = rb.evolve(noisy[0][np.ix_(p, p)], 20.0, DT)
    merr = float(np.max(np.abs(e1[np.ix_(p, p)] - e2)))
    print("B1 mirror check: max error %.2e" % merr, flush=True)

    state = {"code": True, "rise": False}

    def run(label, g, theta0, i, mode="flow"):
        rule = RuleB(L, D, GAMMA, g, theta0, V0, phase_mode=mode)
        rho0 = noisy[i]
        J0 = float(np.sum(rule.currents(rho0, rule.theta)))
        rho, pur = rule.evolve(rho0.copy(), T, DT)
        amount = abs(float(np.real(np.trace(rho))) - 1)
        herm = float(np.max(np.abs(rho - rho.conj().T)))
        mineig = float(np.min(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))))
        state["code"] &= amount < 1e-12 and herm < 1e-12 and mineig >= -1e-8
        rise = float(np.max(np.diff(pur)))
        state["rise"] |= rise > 1e-9
        J1 = rule.total_current(rho)
        w = rule.final_winding(np.random.default_rng(99))
        x = rule.committed
        print("%s start %d: J(0) %+.3e, J(300) %+.3e; purity %.4f -> %.4f (largest rise %+.1e); mean theta %.3f; "
              "R/L rate difference mean %+.3f; winding %d; amount err %.1e, herm %.1e, min eig %.1e"
              % (label, i, J0, J1, pur[0], pur[-1], rise, float(np.mean(rule.theta)),
                 float(np.mean(rule.d[3 * x + 2] - rule.d[3 * x + 1])), w, amount, herm, mineig), flush=True)
        return J1, w

    b3 = [run("B3/B5 theta0 0, g +0.5", 0.5, 0.0, i) for i in range(5)]
    b4 = [run("B4 g 0, theta0 0.4", 0.0, THETA0, i) for i in range(5)]
    b6p = [run("B6 g +0.5, theta0 0.4", 0.5, THETA0, i) for i in range(10)]
    b6m = [run("B6 g -0.5, theta0 0.4", -0.5, THETA0, i) for i in range(10)]
    cst = []
    for g in (0.5, -0.5):
        for i in range(5):
            cst.append(run("reported constant theta 0.4, g %+.1f" % g, g, THETA0, i, mode="const"))

    def lasting(rs):
        return [r for r in rs if abs(r[0]) > 1e-2]

    lp, lm = lasting(b6p), lasting(b6m)
    b6a_sign = "+" if len(lp) >= 8 else ("-" if len(lm) >= 8 else None)
    if b6a_sign == "+":
        last, other = lp, b6m
    elif b6a_sign == "-":
        last, other = lm, b6p
    else:
        last, other = [], []
    checks = [
        ("B1 code properties and mirror check", state["code"] and merr < 1e-9),
        ("B2 purity rises in at least one interval", state["rise"]),
        ("B3 theta0 0: final winding 0 in all", all(w == 0 for _, w in b3)),
        ("B4 g 0: |J(300)| < 1e-3 in all", all(abs(j) < 1e-3 for j, _ in b4)),
        ("B5 theta0 0: |J(300)| < 1e-3 in all", all(abs(j) < 1e-3 for j, _ in b3)),
        ("B6a one sign of g: at least 8 of 10 with |J| > 1e-2", b6a_sign is not None),
        ("B6b other sign: all |J| < 1e-3", b6a_sign is not None and all(abs(j) < 1e-3 for j, _ in other)),
        ("B6c both directions among lasting runs (2 to 8 positive)", b6a_sign is not None and 2 <= sum(j > 0 for j, _ in last) <= 8),
        ("B6d nonzero winding in at least half the lasting runs", b6a_sign is not None and sum(w != 0 for _, w in last) * 2 >= len(last)),
    ]
    print("\nB6 lasting runs: g +0.5 %d of 10, g -0.5 %d of 10" % (len(lp), len(lm)))
    print("\nFrozen predictions:")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    all_runs = b3 + b4 + b6p + b6m + cst
    recorded = [
        ("amount, Hermitian, positive in every run", state["code"]),
        ("run-1 B2-B5 results reproduce", all(c[1] for c in checks[1:5])),
        ("run-1: every |J(300)| < 1e-4 and every final winding 0", all(abs(j) < 1e-4 and w == 0 for j, w in all_runs)),
        ("run-1 mirror error reproduces (1.45e-4)", abs(merr - 1.45e-4) < 0.1e-4),
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
