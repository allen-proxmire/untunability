"""Diagnostic after fixed_point_check run 1 (not pre-registered).

Run 1 found (F3) that ED's discrete-time Grover walk with transfer meetings has a unique steady state that carries a
displacement when the Right/Left draw rates differ, and (F4) failed to find the Fourier walk's steady states at
delta != 0 because the singular-value threshold (1e-9) was too strict. Here: steady states from the eigenvalue of the
one-step map closest to 1 (a trace-preserving map always has one), for both coins:
  - how many eigenvalues lie within 1e-8 and 1e-6 of 1 (degeneracy);
  - displacement per step v at delta = +1e-3, -1e-3, 0, and chi = (v(+) - v(-)) / (2 delta);
  - v at a large asymmetry (delta = 0.5), and the winding of det(W_eff(phi) - z) for the lossy step operator
    W_eff = K0 W (K0 scales Right by sqrt(1-p_R), Left by sqrt(1-p_L) at committed loci), twist phi on the bond
    (L-1, 0), over sample points z;
  - for comparison, attempt 1's continuous-time rule gives chi = 0 at zero lane phase (A1-ledger C281, C282).
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402


def steady(E, n):
    w, V = np.linalg.eig(E)
    order = np.argsort(np.abs(w - 1))
    k = order[0]
    rho = V[:, k].reshape((n, n), order="F")
    rho = rho / np.trace(rho)
    rho = 0.5 * (rho + rho.conj().T)
    near8 = int(np.sum(np.abs(w - 1) < 1e-8))
    near6 = int(np.sum(np.abs(w - 1) < 1e-6))
    gap = float(np.sort(np.abs(w - 1))[1])
    return rho, near8, near6, gap, float(np.abs(w[k] - 1))


def lossy_step(W, L, D, Gamma, delta, phi):
    n = 3 * L
    lane, dest = lane_channels(L, D)
    half = len(lane) // 2
    scale = np.ones(n)
    scale[lane[:half]] = np.sqrt(1 - Gamma * (1 - delta))
    scale[lane[half:]] = np.sqrt(1 - Gamma * (1 + delta))
    Wt = W.copy()
    for a in range(3):
        for b in range(3):
            Wt[a, 3 * (L - 1) + b] *= np.exp(1j * phi)
            Wt[3 * (L - 1) + a, b] *= np.exp(-1j * phi)
    return scale[:, None] * Wt


def winding(W, L, D, Gamma, delta, rng):
    phis = np.linspace(0, 2 * np.pi, 401)
    eigs = np.array([np.linalg.eigvals(lossy_step(W, L, D, Gamma, delta, ph)) for ph in phis])
    flat = eigs.ravel()
    pts = [0.0] + list(rng.uniform(-1, 1, 40) + 1j * rng.uniform(-1, 1, 40))
    best = 0
    for z in pts:
        if np.min(np.abs(eigs - z)) < 1e-3:
            continue
        tot = np.sum(np.angle(eigs - z), axis=1)
        w = int(round(np.sum(np.angle(np.exp(1j * np.diff(tot)))) / (2 * np.pi)))
        best = max(best, abs(w))
    return best


def main():
    L, D, Gamma = 8, 2, 0.3
    n = 3 * L
    rng = np.random.default_rng(7)
    for name, C in (("Grover", fp.GROVER), ("Fourier", fp.FOURIER)):
        W = fp.walk_matrix(L, C)
        Cf = fp.coin_full(L, C)
        vs = {}
        for delta in (1e-3, -1e-3, 0.0, 0.5):
            rho, n8, n6, gap, dev = steady(fp.superop(W, L, D, Gamma, delta), n)
            vs[delta] = fp.displacement(rho, Cf, L)
            mineig = float(np.min(np.linalg.eigvalsh(rho)))
            print("%s delta %+.3f: eigenvalues within 1e-8 of 1: %d, within 1e-6: %d; next distance %.2e; chosen |lambda-1| %.1e; "
                  "min eig of steady state %.1e; v %+.4e" % (name, delta, n8, n6, gap, dev, mineig, vs[delta]), flush=True)
        chi = (vs[1e-3] - vs[-1e-3]) / 2e-3
        w0 = winding(W, L, D, Gamma, 0.0, rng)
        w5 = winding(W, L, D, Gamma, 0.5, rng)
        print("%s: chi %.4e; v(delta 0) %.1e; winding of lossy step: symmetric rates %d, delta 0.5 %d" % (name, chi, vs[0.0], w0, w5), flush=True)


if __name__ == "__main__":
    main()
