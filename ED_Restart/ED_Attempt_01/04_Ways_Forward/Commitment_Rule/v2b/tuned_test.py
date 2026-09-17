"""Tuned dynamic test (G51 = c, RD49): at settings chosen to make version 2b's loop amplify, does a lasting hand form?

LABELLED AS TUNED. The settings were picked from the gain check (C281, C283) to give the largest response: a standing
phase theta = 0.8 on every bond (phase_mode "const"), Gamma = 0.3, every 2nd locus committed (D = 2), draws dropping
lane content into the Internal channel, rate feedback gamma[x, RIGHT] = Gamma (1 - g tanh(v_x/V0)),
gamma[x, LEFT] = Gamma (1 + g tanh(v_x/V0)) with V0 = 0.03 and g = +0.9 or -0.9. A lasting hand here would show the rule
can hold one under these choices, not that ED predicts it.

Ring L = 24 (for speed; the gain check used L = 48, chi = +0.0957 at these settings, loop gain g chi / V0 = 2.87 for
g = +0.9). The response on this ring is measured first, exactly (steady state with fixed phase and rates, delta = 1e-3).
RK4, dt = 0.01, t = 600. Ten noisy starts psi = 1 + 0.1 xi (seed 1357), a control with V0 = 0.2 (loop gain about 0.43).
Measures: total current J, the committed loci's mean |tanh(v_x/V0)|, winding of H_eff at the end.

Predictions frozen before the first run (2026-09-14):
  T0  chi on L = 24 is within 30% of 0.0957 (so the loop gain for g = +0.9, V0 = 0.03 exceeds 1).
  T1  (code) Every run: amount to 1e-12, Hermitian to 1e-12, smallest eigenvalue >= -1e-8; the one-step mirror error
      (a noisy start and its mirror image) is below 1e-15.
  T2  g = +0.9: at least 8 of 10 runs end with |J(600)| > 1e-3.
  T3  g = -0.9: all 10 runs end with |J(600)| < 1e-4.
  T4  Among T2's lasting runs, between 2 and 8 have J > 0 (the hand is chosen by chance).
  T5  In T2's lasting runs, the committed loci's mean |tanh(v_x/V0)| at the end exceeds 0.5 (the rates are far from even).
  T6  In at least half of T2's lasting runs, the final winding of H_eff is nonzero.
  T7  Control V0 = 0.2, g = +0.9, starts 0-4: all end with |J(600)| < 1e-4.
Reported: the mirror error at t = 20 (an amplifying loop can grow rounding, C279), purity, J over time.
Exit code: T1 (code properties).

Changes after freezing (2026-09-14):
  1. Run 1 (tuned_test_run1.txt): all eight predictions RIGHT. chi on L = 24 = +0.1008 (loop gain 3.02; control 0.45).
     Mirror: one step 1.7e-18, t = 20 8.3e-17. g = +0.9: all 10 runs held a flow, |J(600)| = 0.114 (6 positive,
     4 negative), mean |tanh(v/V0)| 0.997, |winding| 1 in all 10, purity 0.184-0.186; |J| was still creeping up
     (about 0.100 at t = 200 to 0.114 at t = 600), so the state may not be fully steady. g = -0.9: all 10 died
     (|J(600)| <= 5e-7, purity 0.1073). Control V0 = 0.2: all 5 died (|J(600)| <= 4e-10).
     Note: final_winding reports the largest |winding|, so the sign of the winding is not recorded.
  2. The exit code now checks the code properties and that run 1's recorded results reproduce.
"""
import math
import sys

import numpy as np

from gain_check import measure
from rule_v2b import RuleB, mirror_perm, pure

L, D, GAMMA, THETA, V0, DT, T = 24, 2, 0.3, 0.8, 0.03, 0.01, 600.0


def main():
    base = RuleB(L, D, GAMMA, 0.0, 0.0)
    vp = measure_small(base, 1e-3)
    vm = measure_small(base, -1e-3)
    chi = (vp - vm) / 2e-3
    print("T0 chi on L = 24: %+.4e (L = 48: +9.568e-02); loop gain g 0.9, V0 0.03: %.2f; V0 0.2: %.2f"
          % (chi, 0.9 * chi / V0, 0.9 * chi / 0.2), flush=True)

    rng = np.random.default_rng(1357)
    starts = [pure(1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)) for _ in range(10)]
    p = mirror_perm(L)
    ra = RuleB(L, D, GAMMA, 0.9, THETA, V0, phase_mode="const")
    rb = RuleB(L, D, GAMMA, 0.9, THETA, V0, phase_mode="const")
    a1, b1 = ra.step(starts[0].copy(), DT), rb.step(starts[0][np.ix_(p, p)], DT)
    m1 = float(np.max(np.abs(a1[np.ix_(p, p)] - b1)))
    a20, _ = ra.evolve(a1, 20.0 - DT, DT)
    b20, _ = rb.evolve(b1, 20.0 - DT, DT)
    m20 = float(np.max(np.abs(a20[np.ix_(p, p)] - b20)))
    print("T1 mirror: one step %.1e; t = 20 %.1e" % (m1, m20), flush=True)

    code = {"ok": True}

    def run(label, g, v0, i):
        rule = RuleB(L, D, GAMMA, g, THETA, v0, phase_mode="const")
        rho = starts[i].copy()
        Js = []
        for _ in range(6):
            rho, pur = rule.evolve(rho, T / 6, DT)
            Js.append(rule.total_current(rho))
        amount = abs(float(np.real(np.trace(rho))) - 1)
        herm = float(np.max(np.abs(rho - rho.conj().T)))
        mineig = float(np.min(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))))
        code["ok"] &= amount < 1e-12 and herm < 1e-12 and mineig >= -1e-8
        x = rule.committed
        j = rule.currents(rho, rule.theta)
        n = rule.amounts(rho)
        vx = 0.5 * (j[(x - 1) % L] + j[x]) / n[x]
        sat = float(np.mean(np.abs(np.tanh(vx / v0))))
        w = rule.final_winding(np.random.default_rng(99))
        print("%s start %d: J at t = 100..600: %s; purity %.4f; mean |tanh(v/V0)| %.3f; winding %d"
              % (label, i, " ".join("%+.2e" % q for q in Js), pur[-1], sat, w), flush=True)
        return Js[-1], sat, w

    plus = [run("g +0.9 V0 0.03", 0.9, V0, i) for i in range(10)]
    minus = [run("g -0.9 V0 0.03", -0.9, V0, i) for i in range(10)]
    control = [run("control g +0.9 V0 0.2", 0.9, 0.2, i) for i in range(5)]

    lasting = [r for r in plus if abs(r[0]) > 1e-3]
    checks = [
        ("T0 chi on L 24 within 30% of 0.0957", abs(chi / 0.0957 - 1) <= 0.3),
        ("T1 code properties; one-step mirror < 1e-15", code["ok"] and m1 < 1e-15),
        ("T2 g +0.9: at least 8 of 10 with |J| > 1e-3", len(lasting) >= 8),
        ("T3 g -0.9: all |J| < 1e-4", all(abs(r[0]) < 1e-4 for r in minus)),
        ("T4 both directions among lasting (2 to 8 positive)", len(lasting) >= 8 and 2 <= sum(r[0] > 0 for r in lasting) <= 8),
        ("T5 lasting runs: mean |tanh(v/V0)| > 0.5", len(lasting) > 0 and all(r[1] > 0.5 for r in lasting)),
        ("T6 nonzero winding in at least half the lasting runs", len(lasting) > 0 and 2 * sum(r[2] != 0 for r in lasting) >= len(lasting)),
        ("T7 control V0 0.2: all |J| < 1e-4", all(abs(r[0]) < 1e-4 for r in control)),
    ]
    print("\nLasting runs (g +0.9): %d of 10; positive %d" % (len(lasting), sum(r[0] > 0 for r in lasting)))
    print("\nFrozen predictions (settings labelled as tuned):")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    recorded = [
        ("code properties; one-step mirror < 1e-15", checks[1][1]),
        ("run-1 chi reproduces (+0.10083)", abs(chi - 0.10083) < 1e-4),
        ("run-1 g +0.9: 10 lasting, 6 positive, |J(600)| in [0.11, 0.12], |winding| 1",
         len(lasting) == 10 and sum(r[0] > 0 for r in lasting) == 6
         and all(0.11 <= abs(r[0]) <= 0.12 and r[2] == 1 for r in plus)),
        ("run-1 g -0.9 and control died (|J(600)| < 1e-6), winding 0",
         all(abs(r[0]) < 1e-6 and r[2] == 0 for r in minus + control)),
    ]
    ok = True
    print("\nRecorded results reproduce:")
    for name, passed in recorded:
        ok &= passed
        print("%-4s %s" % ("PASS" if passed else "FAIL", name))
    print("ALL PASS" if ok else "SOME FAIL")
    return ok


def measure_small(rule, delta):
    v, ok, _, info = measure(rule, THETA, GAMMA, delta)
    if not ok:
        print("  steady-state solve check failed: %s" % (info,))
    return v


if __name__ == "__main__":
    import gain_check
    gain_check.L = L
    sys.exit(0 if main() else 1)
