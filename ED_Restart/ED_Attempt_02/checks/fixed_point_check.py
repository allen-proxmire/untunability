"""The fixed-point question (RD5): can a symmetry, or a parameter-free choice, set ED's lane-loop phase at a value that is
neither 0 nor pi, so the standing phase is not tuned?

Background. Attempt 1's handedness needed a lane-loop phase neither 0 nor pi (A1-ledger C283, C288, C293). Three tries
to fix it by minimizing a cost landed on 0 or pi (A1-ledger C296-C303). Note 4 asked whether a symmetry's fixed point
could set it instead (the way modular flavour models get special values, C34, C39), with 120 degrees suggested (D5).

P0 (code) The discrete-time walk matrix built here reproduces ED's rule version 0 step (coin, then shift) for the Grover
   coin (A1-ledger rule_v0.walk_step).
P1 Continuous time (the rule used in attempt 1's handedness tests): among all 24 operations built from channel
   permutations (S3), the lattice mirror and complex conjugation, find those that map the family H(theta) into itself
   (same hop structure), and the lane-loop fluxes they fix.
P2 Continuous time: phases on the lane mixings cancel around the lane loop, so the coin cannot set the loop phase there.
P3 Discrete time (ED's original coin-and-shift form), two parameter-free coins: Grover (real) and the discrete Fourier
   coin F_jk = omega^(jk)/sqrt3, omega = e^(2 pi i/3), channels (Internal, Left, Right). Checks: mirror symmetry; with
   transfer meetings at every 2nd locus (Right/Left content drops into Internal with probability Gamma(1 -+ delta) per
   step, the rebuilt draw's population form, A1-ledger C293), the number of steady states and the mean displacement per
   step v; response chi = (v(+delta) - v(-delta)) / (2 delta).
P4 Only if P3 gives a nonzero response for the Fourier coin: the handedness dynamics with the Fourier coin, no phase set
   by hand, rate feedback gamma[x,R] = Gamma(1 - g tanh(v_x/V0)), gamma[x,L] = Gamma(1 + g tanh(v_x/V0)), g = +-0.9,
   V0 = |0.9 chi|/3 (loop gain 3; the steepness is the one tuned setting, labelled), L 24, 4,000 steps, 10 noisy starts.

Expected results, written down before the first run (2026-09-14):
  F0 P0: the walk matrix matches rule_v0.walk_step to 1e-12.
  F1 P1: the operations preserving the hop structure are the identity, the mirror (with Left <-> Right), conjugation and
     their product; the fluxes fixed by an operation that changes the flux are exactly 0 and pi.
  F2 P2: with random phases on all mixings, the lane-loop flux stays pi + 2 theta to 1e-12.
  F3 P3: both coins give mirror-symmetric walks (1e-12); with the Grover coin every steady state has |v| < 1e-10 for
     delta = +-1e-3 (time-reversal symmetric, no response).
  F4 P3: with the Fourier coin, |chi| > 1e-4 (a nonzero response with no phase set by hand), and v = 0 at delta = 0 to
     1e-10 (mirror symmetry).
  F5 P4 (if run): for the sign of g with g*chi > 0, at least 8 of 10 runs end with |v| > 1e-3, with between 2 and 8
     positive; for the other sign all end with |v| < 1e-4.
Exit code: F0-F4 (F5 reported).

Changes after freezing (2026-09-14):
  1. Run 1 (fixed_point_check_run1.txt): F0, F2 AS EXPECTED; F1, F3, F4 NOT AS EXPECTED; F5 not run.
     F1: eight operations passed the hop-structure test, not four: the test compared only magnitudes, and in the
     continuous-time rule the Right and Left lanes have identical magnitudes both ways, so swapping them without the
     mirror (and the mirror without the swap) also passed. The fluxes fixed by flux-changing operations were exactly
     0 and pi, as expected. Criterion error (Claude's).
     F3: both coins are mirror-symmetric, but the Grover walk's unique steady state carries a displacement (largest
     |v| 2.29e-4) when the draw rates differ: in discrete time the Right channel moves right, so unequal draw rates
     bias motion directly. The expectation carried over the continuous-time argument (zero response at zero lane
     phase), which does not apply to the coin-and-shift walk.
     F4: no singular value of (E - I) fell below 1e-9 for the Fourier walk at delta != 0, though a trace-preserving map
     always has a fixed point; the threshold was too strict (harness error, Claude's). chi was not computed.
  2. Diagnostic fixed_point_diagnostic.py (not pre-registered) uses the eigenvalue closest to 1 instead.
  3. The exit code now checks the recorded run-1 results: F0 and F2 hold, and the fixed fluxes are exactly 0 and pi.
"""
import itertools
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A1 = os.path.join(HERE, "..", "..", "ED_Attempt_01", "04_Ways_Forward", "Commitment_Rule")
for sub in ("v0", "v1_budget", "v2", "v4", "v2b"):
    sys.path.insert(0, os.path.join(A1, sub))
import rule_v0 as v0  # noqa: E402
from rule_v2 import real_rule  # noqa: E402
from rule_v4 import kraus, lane_channels  # noqa: E402

I, LE, RI = 0, 1, 2
OMEGA = np.exp(2j * np.pi / 3)
GROVER = v0.GROVER.astype(complex)
FOURIER = np.array([[OMEGA ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)


def walk_matrix(L, C):
    n = 3 * L
    W = np.zeros((n, n), dtype=complex)
    for u in range(L):
        for j in range(3):
            W[3 * u + I, 3 * u + j] += C[I, j]
            W[3 * ((u + 1) % L) + RI, 3 * u + j] += C[RI, j]
            W[3 * ((u - 1) % L) + LE, 3 * u + j] += C[LE, j]
    return W


def lane_loop_flux(H, u=0):
    L = H.shape[0] // 3
    v = (u + 1) % L
    prod = H[3 * v + RI, 3 * u + RI] * H[3 * v + LE, 3 * v + RI] * H[3 * u + LE, 3 * v + LE] * H[3 * u + RI, 3 * u + LE]
    return float(np.angle(prod))


def p1():
    L = 6
    H0 = real_rule(L, theta=0.0)
    ops = []
    for perm in itertools.permutations(range(3)):
        for m in (0, 1):
            for k in (0, 1):
                idx = np.zeros(3 * L, dtype=int)
                for u in range(L):
                    uu = (-u) % L if m else u
                    for c in range(3):
                        idx[3 * uu + perm[c]] = 3 * u + c
                ops.append(((perm, m, k), idx))
    preserving, fixed = [], set()
    thetas = np.linspace(-np.pi, np.pi, 721)[:-1]
    for (perm, m, k), idx in ops:
        Ht = H0[np.ix_(idx, idx)]
        if not np.allclose(np.abs(Ht), np.abs(H0), atol=1e-12):
            continue
        preserving.append((perm, m, k))
        changes = False
        for th in thetas:
            H = real_rule(L, theta=th)
            Hp = H[np.ix_(idx, idx)]
            if k:
                Hp = Hp.conj()
            f, fp = lane_loop_flux(H), lane_loop_flux(Hp)
            if abs(np.angle(np.exp(1j * (fp - f)))) > 1e-9:
                changes = True
        if changes:
            for th in thetas:
                H = real_rule(L, theta=th)
                Hp = H[np.ix_(idx, idx)]
                if k:
                    Hp = Hp.conj()
                f, fp = lane_loop_flux(H), lane_loop_flux(Hp)
                if abs(np.angle(np.exp(1j * (fp - f)))) < 1e-9:
                    fixed.add(round(abs(float(np.angle(np.exp(1j * f)))), 6))
    return preserving, sorted(fixed)


def p2(rng):
    L = 6
    worst = 0.0
    for th in (0.3, 0.8, 1.9):
        H = real_rule(L, theta=th).astype(complex)
        ph = rng.uniform(-np.pi, np.pi, (3, 3))
        ph = ph - ph.T
        for u in range(L):
            for a in range(3):
                for b in range(3):
                    if a != b:
                        H[3 * u + a, 3 * u + b] *= np.exp(1j * ph[a, b])
        f = lane_loop_flux(H)
        worst = max(worst, abs(np.angle(np.exp(1j * (f - (np.pi + 2 * th))))))
    return worst


def mirror_perm(L):
    idx = np.zeros(3 * L, dtype=int)
    for u in range(L):
        for c, cm in ((I, I), (LE, RI), (RI, LE)):
            idx[3 * ((-u) % L) + cm] = 3 * u + c
    return idx


def coin_full(L, C):
    return np.kron(np.eye(L), C)


def displacement(rho, Cf, L):
    r = Cf @ rho @ Cf.conj().T
    d = np.real(np.diag(r)).reshape(L, 3)
    return float(np.sum(d[:, RI] - d[:, LE]))


def superop(W, L, D, Gamma, delta):
    n = 3 * L
    lane, dest = lane_channels(L, D)
    p = np.zeros(len(lane))
    half = len(lane) // 2
    p[:half] = Gamma * (1 - delta)
    p[half:] = Gamma * (1 + delta)
    E = np.zeros((n * n, n * n), dtype=complex)
    for col in range(n * n):
        X = np.zeros(n * n, dtype=complex)
        X[col] = 1.0
        Xm = X.reshape((n, n), order="F")
        Y = kraus(W @ Xm @ W.conj().T, lane, dest, p)
        E[:, col] = Y.reshape(n * n, order="F")
    return E


def steady_states(E, n):
    A = E - np.eye(n * n)
    U, s, Vh = np.linalg.svd(A)
    null = [Vh[i].conj() for i in range(len(s)) if s[i] < 1e-9]
    return null, s


def p3(C, L=8, D=2, Gamma=0.3):
    W = walk_matrix(L, C)
    mi = mirror_perm(L)
    mirr = float(np.max(np.abs(W[np.ix_(mi, mi)] - W)))
    Cf = coin_full(L, C)
    n = 3 * L
    out = {"mirror": mirr}
    for delta in (1e-3, -1e-3, 0.0):
        E = superop(W, L, D, Gamma, delta)
        null, s = steady_states(E, n)
        vs = []
        for x in null:
            rho = x.reshape((n, n), order="F")
            tr = np.trace(rho)
            if abs(tr) < 1e-8:
                continue
            rho = rho / tr
            rho = 0.5 * (rho + rho.conj().T)
            vs.append(displacement(rho, Cf, L))
        out[delta] = (len(null), vs)
    return out


def p4(chi, L=24, D=2, Gamma=0.3, steps=4000):
    W = walk_matrix(L, FOURIER)
    Cf = coin_full(L, FOURIER)
    lane, dest = lane_channels(L, D)
    x = np.arange(0, L, D)
    V0 = abs(0.9 * chi) / 3
    rng = np.random.default_rng(1357)
    starts = []
    for _ in range(10):
        psi = 1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)
        psi /= np.linalg.norm(psi)
        starts.append(np.outer(psi, psi.conj()))
    res = {}
    for g in (0.9, -0.9):
        finals = []
        for rho0 in starts:
            rho = rho0.copy()
            for _ in range(steps):
                r = Cf @ rho @ Cf.conj().T
                dd = np.real(np.diag(r)).reshape(L, 3)
                nn = np.real(np.diag(rho)).reshape(L, 3).sum(axis=1)
                vx = (dd[x, RI] - dd[x, LE]) / np.maximum(nn[x], 1e-300)
                s = np.tanh(vx / V0)
                p = np.concatenate([Gamma * (1 - g * s), Gamma * (1 + g * s)])
                rho = kraus(W @ rho @ W.conj().T, lane, dest, p)
            finals.append(displacement(rho, Cf, L))
        res[g] = finals
        print("P4 g %+.1f (V0 %.2e): final v %s" % (g, V0, " ".join("%+.2e" % f for f in finals)), flush=True)
    return res


def main():
    rng = np.random.default_rng(55)
    L = 7
    a = rng.normal(size=(L, 3)) + 1j * rng.normal(size=(L, 3))
    W = walk_matrix(L, GROVER)
    f0 = float(np.max(np.abs((W @ a.reshape(-1)) - v0.walk_step(a).reshape(-1))))
    print("P0 walk matrix vs rule_v0.walk_step: %.1e" % f0, flush=True)

    preserving, fixed = p1()
    print("P1 structure-preserving operations (perm, mirror, conj): %s; fluxes fixed by flux-changing operations: %s" % (preserving, fixed), flush=True)
    worst2 = p2(rng)
    print("P2 lane-loop flux with random mixing phases: largest deviation from pi + 2 theta %.1e" % worst2, flush=True)

    g3 = p3(GROVER)
    print("P3 Grover: mirror error %.1e; steady states and v: +d %s; -d %s; 0 %s" % (g3["mirror"], g3[1e-3][0], g3[-1e-3][0], g3[0.0][0]), flush=True)
    print("   Grover largest |v| over steady states: %.2e" % max([abs(v) for d in (1e-3, -1e-3, 0.0) for v in g3[d][1]] + [0.0]), flush=True)
    f3 = p3(FOURIER)
    print("P3 Fourier: mirror error %.1e; steady states: +d %d, -d %d, 0 %d" % (f3["mirror"], f3[1e-3][0], f3[-1e-3][0], f3[0.0][0]), flush=True)
    uniq = f3[1e-3][0] == 1 and f3[-1e-3][0] == 1 and f3[0.0][0] == 1
    chi = (f3[1e-3][1][0] - f3[-1e-3][1][0]) / 2e-3 if uniq else float("nan")
    v_at0 = abs(f3[0.0][1][0]) if f3[0.0][1] else float("nan")
    print("   Fourier v(+d) %s, v(-d) %s, v(0) %s; chi %.4e" % (f3[1e-3][1], f3[-1e-3][1], f3[0.0][1], chi), flush=True)

    struct_ok = {tuple(p) for p in preserving} == {((0, 1, 2), 0, 0), ((0, 1, 2), 0, 1), ((0, 2, 1), 1, 0), ((0, 2, 1), 1, 1)}
    checks = [
        ("F0 walk matrix matches ED's version 0 step", f0 < 1e-12),
        ("F1 only identity, mirror, conjugation and product preserve the rule; fixed fluxes 0 and pi", struct_ok and fixed == [0.0, round(np.pi, 6)]),
        ("F2 mixing phases cancel around the lane loop", worst2 < 1e-12),
        ("F3 both coins mirror-symmetric; Grover steady states carry no displacement",
         g3["mirror"] < 1e-12 and f3["mirror"] < 1e-12 and all(abs(v) < 1e-10 for d in (1e-3, -1e-3, 0.0) for v in g3[d][1])),
        ("F4 Fourier coin: nonzero response, none at delta 0", uniq and abs(chi) > 1e-4 and v_at0 < 1e-10),
    ]
    f5 = None
    if uniq and abs(chi) > 1e-4:
        res = p4(chi)
        amp = 0.9 if chi > 0 else -0.9
        lasting = [v for v in res[amp] if abs(v) > 1e-3]
        f5 = len(lasting) >= 8 and 2 <= sum(v > 0 for v in lasting) <= 8 and all(abs(v) < 1e-4 for v in res[-amp])
    print("\nExpected results:")
    for name, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", name))
    if f5 is None:
        print("  (F5 not run: no nonzero Fourier response)")
    else:
        print("  %-16s F5 Fourier handedness dynamics: lasting hand for one sign of g" % ("AS EXPECTED" if f5 else "NOT AS EXPECTED"))
    recorded = checks[0][1] and checks[2][1] and fixed == [0.0, round(np.pi, 6)]
    print("RECORDED RESULTS REPRODUCE" if recorded else "RECORDED RESULTS DO NOT REPRODUCE")
    return recorded


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
