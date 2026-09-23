"""Dispersion check (road J's named risk, C20). Arithmetic on representative hop rules; not a model of ED.

Question: do waves in discrete hop rules built from ED's decided meanings travel slower than light at short wavelengths? (Husain and Louko,
C18: any such dip, f = omega/|k| < 1 somewhere, leaks into low-energy detectors.)

Rules (set before running, 2026-09-15; ED has no decided three-dimensional hop rule, so these are representative):
  Decided meanings used: one locus per tick is the top speed (A4 note 13); light does not turn (A4 D27, R4-Q2); mass is turning
  (A4 C74, the checkerboard / zigzag picture). Lattice units: one grain, one tick; c = 1 is the low-wavelength speed.
  R1 (1D light): a two-state relation pointer, right-movers hop right, left-movers hop left, no turning. U(k) = diag(e^{-ik}, e^{ik}).
  R2 (1D matter): a turn by angle theta each tick, then the same hop: U(k) = diag(e^{-ik}, e^{ik}) . [[cos t, -sin t], [sin t, cos t]],
     with theta = pi/4 (a fair turn).
  R3 (3D light): the simplest no-turn rule with one hop along each axis per tick, the hop direction along axis i set by the pointer's
     state along i: U(k) = exp(-i kx sx) exp(-i ky sy) exp(-i kz sz), sx, sy, sz the Pauli matrices. Close in form to the Weyl walks of
     Bisio, D'Ariano and Perinotti.
  Speeds: phase speed f = omega/|k| (Husain and Louko's f); group speed |d omega/d k|.

Expected results, written down before the first run (2026-09-15):
  E1 R1: omega = |k| exactly for all k in (-pi, pi): max |f - 1| < 1e-12. Light in 1D has no slow short waves.
  E2 R2: cos omega = cos(theta) cos(k); maximum group speed over k equals cos(theta) = 0.70711 (to 1e-4); gap omega(0) = theta = 0.78540
     (to 1e-9). Matter travels below c: that is mass, not the Husain-Louko effect.
  E3 R3: its eigenphases are +-omega with cos omega = cos kx cos ky cos kz - sin kx sin ky sin kz, to 1e-12 on 2000 random k.
  E4 R3 along an axis, k = (s, 0, 0) for s in (0, pi): f = 1 exactly (max |f - 1| < 1e-12).
  E5 R3 at |k| = 0.01: f - 1 = +0.001925 along (1,1,1)/sqrt3 and -0.001925 along (1,1,-1)/sqrt3, each within 3%: the deviation is linear
     in |k|, of size |k|/(3 sqrt3), faster than light in some directions and slower in others.
  E6 R3 at |k| = 0.5: along (1,1,-1)/sqrt3, f within 0.85 and 0.92 (slower than light); along (1,1,1)/sqrt3, f within 1.05 and 1.10.
  E7 R3 averaged over 200,000 random directions (as a randomly oriented pattern would average them): mean f within 0.985 and 0.995 at
     |k| = 0.5, and within 0.9980 and 0.9990 at |k| = 0.2 (about 1 - 0.038 |k|^2): slower than light on average.
Exit code: 0 if it completes.
"""
import math
import sys

import numpy as np

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)


def expm_pauli(a, s):
    return math.cos(a) * I2 - 1j * math.sin(a) * s


def omega_from_unitary(U):
    ev = np.linalg.eigvals(U)
    return np.abs(np.angle(ev))


def r3_omega(kvec):
    kx, ky, kz = kvec
    U = expm_pauli(kx, SX) @ expm_pauli(ky, SY) @ expm_pauli(kz, SZ)
    w = omega_from_unitary(U)
    return float(np.max(w)), U


def r3_cos_formula(kvec):
    kx, ky, kz = kvec
    return math.cos(kx) * math.cos(ky) * math.cos(kz) - math.sin(kx) * math.sin(ky) * math.sin(kz)


def main():
    rng = np.random.default_rng(20260915)

    ks = np.linspace(-math.pi + 1e-3, math.pi - 1e-3, 4001)
    worst1 = 0.0
    for k in ks:
        if abs(k) < 1e-9:
            continue
        U = np.diag([np.exp(-1j * k), np.exp(1j * k)])
        w = omega_from_unitary(U)
        worst1 = max(worst1, float(np.max(np.abs(w / abs(k) - 1))))
    print("E1 1D light: max |f - 1| = %.2e" % worst1)

    theta = math.pi / 4
    C = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]], complex)
    kk = np.linspace(0, math.pi, 200001)
    om = np.arccos(np.clip(math.cos(theta) * np.cos(kk), -1, 1))
    vg = np.abs(np.gradient(om, kk))
    U0 = np.diag([1.0, 1.0]).astype(complex) @ C
    gap = float(np.min(omega_from_unitary(U0)))
    formula_ok = True
    for k in np.linspace(0.1, 3.0, 30):
        U = np.diag([np.exp(-1j * k), np.exp(1j * k)]) @ C
        formula_ok &= abs(math.cos(float(np.max(omega_from_unitary(U)))) - math.cos(theta) * math.cos(k)) < 1e-12
    print("E2 1D matter (theta = pi/4): max group speed %.5f, gap %.5f, formula holds %s" % (float(vg.max()), gap, formula_ok))

    worst3 = 0.0
    for _ in range(2000):
        kv = rng.uniform(-math.pi, math.pi, 3)
        w, _ = r3_omega(kv)
        worst3 = max(worst3, abs(math.cos(w) - r3_cos_formula(kv)))
    print("E3 3D rule dispersion formula: max |cos omega - formula| = %.2e" % worst3)

    worst4 = 0.0
    for s in np.linspace(0.01, math.pi - 0.01, 500):
        w, _ = r3_omega((s, 0.0, 0.0))
        worst4 = max(worst4, abs(w / s - 1))
    print("E4 3D rule along an axis: max |f - 1| = %.2e" % worst4)

    def f_along(direction, K):
        d = np.array(direction, float)
        d /= np.linalg.norm(d)
        w, _ = r3_omega(K * d)
        return w / K

    fp, fm = f_along((1, 1, 1), 0.01), f_along((1, 1, -1), 0.01)
    target = 0.01 / (3 * math.sqrt(3))
    print("E5 |k| = 0.01: f - 1 along (1,1,1) = %+.6f, along (1,1,-1) = %+.6f (target +-%.6f)" % (fp - 1, fm - 1, target))

    fm5, fp5 = f_along((1, 1, -1), 0.5), f_along((1, 1, 1), 0.5)
    print("E6 |k| = 0.5: f along (1,1,-1) = %.4f, along (1,1,1) = %.4f" % (fm5, fp5))

    dirs = rng.standard_normal((200000, 3))
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    means = {}
    for K in (0.5, 0.2):
        kv = K * dirs
        c = np.cos(kv[:, 0]) * np.cos(kv[:, 1]) * np.cos(kv[:, 2]) - np.sin(kv[:, 0]) * np.sin(kv[:, 1]) * np.sin(kv[:, 2])
        w = np.arccos(np.clip(c, -1, 1))
        means[K] = float(np.mean(w / K))
    print("E7 direction-averaged f: |k| = 0.5 -> %.5f, |k| = 0.2 -> %.6f" % (means[0.5], means[0.2]))

    checks = (
        ("E1 1D light has f = 1 exactly", worst1 < 1e-12),
        ("E2 1D matter: max group speed cos(theta), gap theta", abs(float(vg.max()) - math.cos(theta)) < 1e-4 and abs(gap - theta) < 1e-9 and formula_ok),
        ("E3 3D rule dispersion formula", worst3 < 1e-12),
        ("E4 3D rule exact along axes", worst4 < 1e-12),
        ("E5 linear direction-dependent deviation |k|/(3 sqrt3)", abs((fp - 1) / target - 1) < 0.03 and abs((fm - 1) / (-target) - 1) < 0.03),
        ("E6 at |k| = 0.5 slow along (1,1,-1), fast along (1,1,1)", 0.85 <= fm5 <= 0.92 and 1.05 <= fp5 <= 1.10),
        ("E7 direction-averaged f below 1", 0.985 <= means[0.5] <= 0.995 and 0.9980 <= means[0.2] <= 0.9990),
    )
    print("\nExpected results:")
    for label, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
