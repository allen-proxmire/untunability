"""Discrete-time hand test (follow-up to fixed_point_check and its diagnostic, RD5).

The diagnostic found that ED's original coin-and-shift walk (rule version 0, Grover coin) with transfer meetings responds
to a Right/Left draw-rate difference with chi = 0.229 and gives the lossy step operator winding 1 at a large rate
difference, with no lane phase at all; the Fourier (120-degree) coin responds too (chi about 0.165 from an eigenvector
whose eigenvalue was less accurate). So in the discrete rule the standing phase that attempt 1 needed may not be needed.
This test asks whether ED's discrete rule holds a lasting, chance-chosen hand with rate feedback and no phase set by hand.

Rule: ring L = 24; walk step W = shift . coin (A1-ledger rule_v0.walk_step); transfer meetings at every 2nd locus
(Right/Left content drops into Internal with probability p per step, A1-ledger C293); rate feedback
p[x,R] = Gamma(1 - g tanh(v_x/V0)), p[x,L] = Gamma(1 + g tanh(v_x/V0)), Gamma = 0.3, where v_x is the displacement per
unit amount at committed locus x after the coin. V0 = |0.9 chi| / G, with loop gain G = 3 (the steepness is the one
tuned setting, labelled) or G = 0.5 (control). g = +-0.9. 4,000 steps; the 10 noisy starts of A1-ledger C288.

Expected results, written down before the first run (2026-09-14):
  H0 Direct iteration (L 8, from the fully mixed state, fixed rates) reproduces the diagnostic's displacements to 1e-6:
     Grover +-2.2926e-4 at delta +-1e-3; Fourier +-1.6515e-4.
  H1 Grover, gain 3: for the sign of g with g*chi > 0, at least 8 of 10 runs end with |v| > 1e-3, with between 2 and 8
     positive; for the other sign, all 10 end with |v| < 1e-4.
  H2 Fourier, gain 3: the same as H1.
  H3 Grover control, gain 0.5, amplifying sign: all 10 end with |v| < 1e-4.
  H4 Grover, gain 3: in at least half of the lasting runs, the lossy step operator at the final rates has nonzero winding.
  H5 (code) Mirror: one step of the feedback dynamics on a noisy start and on its mirror image agree to 1e-15.
Exit code: H0 and H5 (code), with H1-H4 reported.

Changes after freezing (2026-09-14):
  1. Run 1 (discrete_hand_test_run1.txt): H0, H3, H5 AS EXPECTED; H1, H2, H4 NOT AS EXPECTED.
     Grover: with g = +0.9 (expected amplifying, from the global chi > 0) all runs died (|v| <= 3.8e-5); with g = -0.9
     all 10 held lasting flows, |v| 0.017-0.054, 4 positive and 6 negative, winding nonzero in 2 of 10.
     Fourier: with g = +0.9 all 10 held |v| = 0.243 exactly, 4 positive and 6 negative, winding 1 in all 10; with g = -0.9
     all 10 also held lasting flows, |v| 0.010-0.025, winding 1 in 8 of 10.
     Control (Grover, gain 0.5): all died (below 1e-16).
     Claude's design error: the amplifying sign was taken from the global response chi, but the feedback reads the local
     displacement at committed loci, whose response to the rates need not share its sign; and 'the other sign dies' did
     not hold for the Fourier coin. The uneven Grover magnitudes suggest some runs may not be steady (oscillating or
     patterned); not yet checked.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
import fixed_point_diagnostic as fd  # noqa: E402
from rule_v4 import kraus, lane_channels  # noqa: E402

GAMMA, D, STEPS = 0.3, 2, 4000


def iterate_steady(C, delta, L=8, steps=20000, tol=1e-14):
    n = 3 * L
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    half = len(lane) // 2
    p = np.concatenate([np.full(half, GAMMA * (1 - delta)), np.full(half, GAMMA * (1 + delta))])
    rho = np.eye(n, dtype=complex) / n
    for i in range(steps):
        new = kraus(W @ rho @ W.conj().T, lane, dest, p)
        if np.max(np.abs(new - rho)) < tol:
            rho = new
            break
        rho = new
    return fp.displacement(rho, Cf, L)


def step(rho, W, Cf, lane, dest, L, g, V0):
    x = np.arange(0, L, D)
    r = Cf @ rho @ Cf.conj().T
    dd = np.real(np.diag(r)).reshape(L, 3)
    nn = np.real(np.diag(rho)).reshape(L, 3).sum(axis=1)
    vx = (dd[x, fp.RI] - dd[x, fp.LE]) / np.maximum(nn[x], 1e-300)
    s = np.tanh(vx / V0)
    p = np.concatenate([GAMMA * (1 - g * s), GAMMA * (1 + g * s)])
    return kraus(W @ rho @ W.conj().T, lane, dest, p), s


def run_set(C, chi, gain, g, starts, L=24):
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    V0 = abs(0.9 * chi) / gain
    finals, windings = [], []
    for rho0 in starts:
        rho = rho0.copy()
        for _ in range(STEPS):
            rho, s = step(rho, W, Cf, lane, dest, L, g, V0)
        v = fp.displacement(rho, Cf, L)
        finals.append(v)
        if abs(v) > 1e-3:
            windings.append(winding_at(W, L, s, g))
    return finals, windings, V0


def winding_at(W, L, s, g):
    n = 3 * L
    lane, dest = lane_channels(L, D)
    half = len(lane) // 2
    pR, pL = GAMMA * (1 - g * s), GAMMA * (1 + g * s)
    scale = np.ones(n)
    scale[lane[:half]] = np.sqrt(1 - pR)
    scale[lane[half:]] = np.sqrt(1 - pL)
    phis = np.linspace(0, 2 * np.pi, 301)
    eigs = []
    for ph in phis:
        Wt = W.copy()
        for a in range(3):
            for b in range(3):
                Wt[a, 3 * (L - 1) + b] *= np.exp(1j * ph)
                Wt[3 * (L - 1) + a, b] *= np.exp(-1j * ph)
        eigs.append(np.linalg.eigvals(scale[:, None] * Wt))
    eigs = np.array(eigs)
    rng = np.random.default_rng(3)
    best = 0
    for z in [0.0] + list(rng.uniform(-1, 1, 30) + 1j * rng.uniform(-1, 1, 30)):
        if np.min(np.abs(eigs - z)) < 1e-3:
            continue
        tot = np.sum(np.angle(eigs - z), axis=1)
        best = max(best, abs(int(round(np.sum(np.angle(np.exp(1j * np.diff(tot)))) / (2 * np.pi)))))
    return best


def main():
    hg = (iterate_steady(fp.GROVER, 1e-3), iterate_steady(fp.GROVER, -1e-3))
    hf = (iterate_steady(fp.FOURIER, 1e-3), iterate_steady(fp.FOURIER, -1e-3))
    print("H0 direct iteration: Grover v(+-d) %+.4e %+.4e; Fourier %+.4e %+.4e" % (hg + hf), flush=True)
    h0 = (abs(hg[0] - 2.2926e-4) < 1e-6 and abs(hg[1] + 2.2926e-4) < 1e-6
          and abs(hf[0] - 1.6515e-4) < 1e-6 and abs(hf[1] + 1.6515e-4) < 1e-6)
    chi_g, chi_f = (hg[0] - hg[1]) / 2e-3, (hf[0] - hf[1]) / 2e-3
    print("chi: Grover %.4e, Fourier %.4e" % (chi_g, chi_f), flush=True)

    L = 24
    rng = np.random.default_rng(1357)
    starts = []
    for _ in range(10):
        psi = 1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)
        psi /= np.linalg.norm(psi)
        starts.append(np.outer(psi, psi.conj()))

    W, Cf = fp.walk_matrix(L, fp.GROVER), fp.coin_full(L, fp.GROVER)
    lane, dest = lane_channels(L, D)
    mi = fp.mirror_perm(L)
    a1, _ = step(starts[0], W, Cf, lane, dest, L, 0.9, abs(0.9 * chi_g) / 3)
    a2, _ = step(starts[0][np.ix_(mi, mi)], W, Cf, lane, dest, L, 0.9, abs(0.9 * chi_g) / 3)
    h5_err = float(np.max(np.abs(a1[np.ix_(mi, mi)] - a2)))
    print("H5 mirror one step: %.1e" % h5_err, flush=True)

    results = {}
    for name, C, chi in (("Grover", fp.GROVER, chi_g), ("Fourier", fp.FOURIER, chi_f)):
        amp = 0.9 if chi > 0 else -0.9
        for g in (amp, -amp):
            finals, wind, V0 = run_set(C, chi, 3.0, g, starts)
            results[(name, g)] = (finals, wind)
            print("%s gain 3, g %+.1f (V0 %.3e): final v %s; windings of lasting runs %s"
                  % (name, g, V0, " ".join("%+.2e" % v for v in finals), wind), flush=True)
    amp_g = 0.9 if chi_g > 0 else -0.9
    ctrl, _, V0c = run_set(fp.GROVER, chi_g, 0.5, amp_g, starts)
    print("Grover control gain 0.5, g %+.1f (V0 %.3e): final v %s" % (amp_g, V0c, " ".join("%+.2e" % v for v in ctrl)), flush=True)

    def hand_ok(name, chi):
        amp = 0.9 if chi > 0 else -0.9
        lasting = [v for v in results[(name, amp)][0] if abs(v) > 1e-3]
        return (len(lasting) >= 8 and 2 <= sum(v > 0 for v in lasting) <= 8
                and all(abs(v) < 1e-4 for v in results[(name, -amp)][0]))

    wind_g = results[("Grover", amp_g)][1]
    checks = [
        ("H0 direct iteration reproduces the diagnostic", h0),
        ("H1 Grover: lasting chance-chosen hand for the amplifying sign only", hand_ok("Grover", chi_g)),
        ("H2 Fourier: the same", hand_ok("Fourier", chi_f)),
        ("H3 Grover control (gain 0.5): all die", all(abs(v) < 1e-4 for v in ctrl)),
        ("H4 Grover: nonzero winding in at least half the lasting runs", len(wind_g) > 0 and 2 * sum(w != 0 for w in wind_g) >= len(wind_g)),
        ("H5 mirror one step to 1e-15", h5_err < 1e-15),
    ]
    print("\nExpected results:")
    for name, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", name))
    return checks[0][1] and checks[5][1]


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
