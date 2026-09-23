"""Check C248: can a mirror-symmetric, irreversible ED-style transport rule pick a handedness by itself? (RD41, G43)

Rule (a toy, not ED's full rule): one lane of complex amplitudes psi_x on a ring of L = 64 loci, evolving in
continuous time as d psi / dt = -i (H psi), (H psi)_x = t_f psi_{x-1} + t_b psi_{x+1}, then renormalized so the total
amount stays 1 (irreversible, non-Hermitian when t_f != t_b). The hops depend instantaneously on the pattern's own
current J = sum_x Im(psi_x* psi_{x+1}) (no memory of past traffic, consistent with D1):
  t_f = 1 - g tanh(J / J0),  t_b = 1 + g tanh(J / J0),  J0 = 0.05.
Mirror (x -> -x) sends J -> -J and swaps t_f and t_b, so the rule has no built-in handedness. For a plane wave
e^{ikx}, Im E(k) = (t_b - t_f) sin k, so a current makes its own direction grow: feedback that can run away.
Handedness = winding of E(k) = t_b e^{ik} + t_f e^{-ik} about 0 (+1 if |t_b| > |t_f|, -1 if |t_f| > |t_b|),
computed as in hatano_nelson.py.
Runs: 200 seeds; start psi = (1 + eps xi_x) / norm, xi complex unit Gaussian, eps = 1e-3; RK4, dt = 0.02, 3,000 steps.

Known context (not ED's): spontaneous chirality in mirror-symmetric nonlinear resonators (Del Bino et al. 2017, C244);
self-induced topological nonreciprocity with winding numbers in nonlinear lattices (de Castro and Benalcazar 2024;
Longhi 2025, C245). This toy checks the mechanism inside an ED-style rule; the mechanism itself is not new.

Predictions frozen before the first run (2026-09-14):
  P1  g = 0 (no feedback): every run ends with winding 0 (t_f = t_b exactly).
  P2  Mirror check at g = 0.5: evolving the mirror image of one run's start gives the mirror image of its end (to 1e-9)
      and the opposite winding.
  P3  g = 0.5: at least 90% of runs end with winding +1 or -1.
  P4  g = 0.5: among runs with nonzero winding, the share with +1 is between 0.35 and 0.65 (no built-in preference).
  P5  g = 0.5, start exactly uniform (no noise, J = 0): ends with winding 0 (the symmetric state is a fixed point;
      the choice of hand comes from fluctuations, i.e. chance).

Changes after freezing (2026-09-14):
  1. Run 1 (handedness_toy_run1.txt): all five predictions RIGHT (g 0.5: +1 in 94 runs, -1 in 106, 0 in none; share +1
     0.470), BUT the result does not show what P3 was meant to test. The median |J| at the end was 7.17e-8 at g = 0.5,
     the same as at g = 0 (7.17e-8): the current never grew. The hop difference t_b - t_f = 2 g tanh(J/J0) was
     therefore about 1e-6, and the winding (nonzero for any difference) just recorded the sign of leftover noise.
     P3's criterion (any nonzero winding) was too weak; that is Claude's design error. The verdicts stand as recorded.
  2. Added: the size of the handedness, |t_b - t_f|, is reported for the run-1 seeds.
  3. Added follow-up test F, predictions frozen before it was first run. Start = uniform + delta * e^{+-i k x}
     (k = 2 pi / L), normalized, so the start carries a controlled current of either sign; g = 0.5; same evolution.
     F1  delta = 0.01: final |t_b - t_f| < 0.01 (small currents die out; the symmetric state is stable).
     F2  delta = 1.0: final |t_b - t_f| > 0.5 (a large current sustains itself: a handed state exists).
     F3  whenever the final |t_b - t_f| > 0.1, the final hand has the sign of the initial current.
     F4  mirrored starts (e^{-ikx} instead of e^{+ikx}) end with the opposite winding whenever the handedness is above 0.1.
  4. The exit code now checks the code properties (P1, P2, P5) and that the recorded run-1 counts reproduce; F is reported.
  5. Run 2 (handedness_toy_run2.txt): F1-F4 RIGHT. A diagnostic afterwards (handedness_threshold_diagnostic.py, not
     pre-registered) shows F1's parenthetical reading is wrong: small currents do not die out. At delta 0.01 the
     difference t_b - t_f creeps up (1.96e-4 to 1.98e-4 by t = 240) and at delta 0.1 it grows and speeds up (0.022 to 0.17);
     delta 0.15 and above lock in fully (|t_b - t_f| = 1) by t = 120. There is no threshold in this toy: the symmetric
     state is only marginally stable, and the time to lock in grows as the seed shrinks. The F1 verdict stands as recorded.
"""
import math
import sys

import numpy as np

L, J0, DT, STEPS, RUNS, EPS = 64, 0.05, 0.02, 3000, 200, 1e-3
KGRID = np.linspace(-math.pi, math.pi, 4001)[:-1]


def current(psi):
    return float(np.sum(np.imag(np.conj(psi) * np.roll(psi, -1))))


def hops(psi, g):
    s = math.tanh(current(psi) / J0)
    return 1 - g * s, 1 + g * s


def rhs(psi, tf, tb):
    return -1j * (tf * np.roll(psi, 1) + tb * np.roll(psi, -1))


def evolve(psi, g):
    for _ in range(STEPS):
        tf, tb = hops(psi, g)
        k1 = rhs(psi, tf, tb); k2 = rhs(psi + 0.5 * DT * k1, tf, tb)
        k3 = rhs(psi + 0.5 * DT * k2, tf, tb); k4 = rhs(psi + DT * k3, tf, tb)
        psi = psi + DT * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        psi = psi / np.linalg.norm(psi)
    return psi


def winding(tf, tb):
    f = tb * np.exp(1j * KGRID) + tf * np.exp(-1j * KGRID)
    if np.min(np.abs(f)) < 1e-12:
        return 0
    ph = np.angle(f)
    steps = np.angle(np.exp(1j * np.diff(np.append(ph, ph[0]))))
    return int(round(steps.sum() / (2 * math.pi)))


def start(rng):
    xi = (rng.standard_normal(L) + 1j * rng.standard_normal(L)) / math.sqrt(2)
    psi = 1 + EPS * xi
    return psi / np.linalg.norm(psi)


def mirror(psi):
    return psi[(-np.arange(L)) % L]


def main():
    res = {}
    for g in (0.0, 0.5):
        rng = np.random.default_rng(12345)
        ws, js = [], []
        for _ in range(RUNS):
            end = evolve(start(rng), g)
            tf, tb = hops(end, g)
            ws.append(winding(tf, tb))
            js.append(current(end))
        res[g] = (np.array(ws), np.array(js))
        w = res[g][0]
        print("g %.1f: winding +1 %d, -1 %d, 0 %d; |J| median %.3e" % (g, np.sum(w == 1), np.sum(w == -1), np.sum(w == 0), np.median(np.abs(js))))

    rng = np.random.default_rng(777)
    s0 = start(rng)
    e1 = evolve(s0, 0.5)
    e2 = evolve(mirror(s0), 0.5)
    merr = float(np.max(np.abs(mirror(e1) - e2)))
    w1, w2 = winding(*hops(e1, 0.5)), winding(*hops(e2, 0.5))
    print("mirror check: max error %.1e; windings %d and %d" % (merr, w1, w2))

    uni = np.ones(L, dtype=complex) / math.sqrt(L)
    eu = evolve(uni, 0.5)
    wu = winding(*hops(eu, 0.5))
    print("uniform start: winding %d, J %.1e" % (wu, current(eu)))

    w0, w5 = res[0.0][0], res[0.5][0]
    handed = w5[w5 != 0]
    share_plus = float(np.mean(handed == 1)) if len(handed) else float("nan")
    checks = [
        ("P1 g = 0: all windings 0", bool(np.all(w0 == 0))),
        ("P2 mirror check: mirrored end and opposite winding", merr < 1e-9 and w1 == -w2 and w1 != 0),
        ("P3 g = 0.5: at least 90% handed", float(np.mean(w5 != 0)) >= 0.9),
        ("P4 g = 0.5: share of +1 among handed between 0.35 and 0.65", 0.35 <= share_plus <= 0.65),
        ("P5 uniform start stays at winding 0", wu == 0),
    ]
    print("share handed at g 0.5: %.3f; share +1 among handed: %.3f" % (float(np.mean(w5 != 0)), share_plus))
    print("\nOriginal frozen predictions (first-run verdicts are the record; see note on P3):")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))

    js5 = res[0.5][1]
    dt = 2 * 0.5 * np.abs(np.tanh(js5 / J0))
    print("\nsize of handedness at g 0.5 (run-1 seeds): |t_b - t_f| median %.2e, max %.2e; share above 0.1: %.3f"
          % (np.median(dt), dt.max(), float(np.mean(dt > 0.1))))

    print("\nFollow-up F (predictions frozen before first run):")
    kx = 2 * math.pi * np.arange(L) / L
    finals = {}
    for delta in (0.01, 0.1, 0.3, 1.0):
        for sgn in (+1, -1):
            psi = np.ones(L, dtype=complex) + delta * np.exp(1j * sgn * kx)
            psi = psi / np.linalg.norm(psi)
            j_init = current(psi)
            end = evolve(psi, 0.5)
            tf, tb = hops(end, 0.5)
            finals[(delta, sgn)] = (j_init, tb - tf, winding(tf, tb))
            print("  delta %.2f sign %+d: initial J %+.3e -> final t_b - t_f %+.3e, winding %+d" % (delta, sgn, j_init, tb - tf, winding(tf, tb)))
    big = [(k, v) for k, v in finals.items() if abs(v[1]) > 0.1]
    f_checks = [
        ("F1 delta 0.01: final |t_b - t_f| < 0.01", all(abs(finals[(0.01, s)][1]) < 0.01 for s in (1, -1))),
        ("F2 delta 1.0: final |t_b - t_f| > 0.5", all(abs(finals[(1.0, s)][1]) > 0.5 for s in (1, -1))),
        ("F3 handed ends have the sign of the initial current", all(np.sign(v[1]) == np.sign(v[0]) for _, v in big)),
        ("F4 mirrored starts end with opposite winding", all(finals[(d, 1)][2] == -finals[(d, -1)][2]
                                                             for d in (0.01, 0.1, 0.3, 1.0) if abs(finals[(d, 1)][1]) > 0.1)),
    ]
    for name, passed in f_checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))

    recorded = [
        ("P1, P2, P5 code properties", checks[0][1] and checks[1][1] and checks[4][1]),
        ("run-1 counts reproduce (+1: 94, -1: 106, 0: 0)", int(np.sum(w5 == 1)) == 94 and int(np.sum(w5 == -1)) == 106),
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
