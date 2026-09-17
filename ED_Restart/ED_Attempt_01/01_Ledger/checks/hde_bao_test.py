"""Check C240: horizon-set births (holographic dark energy with the future event horizon) against DESI DR2 BAO.

Allen's 'flow meets boundary' thought (D14, C235) as an ED birth rule: the birth-driven dark energy density is set by
the future event horizon L, rho_de = 3 c^2 M_P^2 / L^2 (Li 2004, C157), with c an order-1 number replacing the tiny
constant birth chance (C211). In a flat universe with matter (radiation neglected; it changes E(z) by about 0.1% at
z = 2.33), with x = ln a:
  dOmega_de/dx = Omega_de (1 - Omega_de) (1 + 2 sqrt(Omega_de) / c)
  w_de = -1/3 - (2 / (3 c)) sqrt(Omega_de)
  E(a)^2 = Omega_m a^-3 / (1 - Omega_de(a)),  Omega_de(a = 1) = 1 - Omega_m
Data: DESI DR2 BAO, 13 values and covariance, the same as bao_distance_test.py (C220). One overall factor
c/(H0 r_d) fitted analytically in every case. Reference: flat constant dark energy (Omega_m free), also without
radiation. Grid: Omega_m 0.25-0.40 (step 0.002); c 0.30-2.00 (step 0.01).

Caveats: BAO only; radiation neglected in both models; r_d absorbed into the fitted factor; the ED reading (births set
by the horizon) is an interpretation of a known model, not a derivation.

Predictions frozen before the first run (2026-09-14):
  P0  (code) w at Omega_de = 0.73, c = 1 is -0.903 within 0.005 (Li 2004 quotes -0.90), and with c = 1e6 the HDE
      distances equal constant dark energy to 1e-4 relative.
  P1  Constant dark energy, radiation neglected: best chi^2 between 9 and 12.
  P2  HDE best-fit c lies between 0.5 and 1.5.
  P3  HDE best chi^2 is within 4 of constant dark energy's best chi^2 (comparable, as in Huang-Liu-Shao 2026, C227).
  P4  w today at the HDE best fit is between -1.1 and -0.85.

Changes after freezing (2026-09-14):
  Run 1 (hde_bao_test_run1.txt): P1-P4 RIGHT; P0 WRONG on its second half. The w formula gave -0.9029 (as Li quotes),
  but c = 1e6 differed from constant dark energy by 22%. That was Claude's wrong premise, not a code error: as c grows,
  holographic dark energy tends to w = -1/3, not w = -1, so it does not contain constant dark energy as a limit. The
  code was checked another way: the Omega_de equation used is exactly dOmega/dx = -3 w Omega (1 - Omega) with Li's w
  (the general flat matter-plus-dark-energy relation). The original verdicts stand. The exit code now checks that
  consistency and that the recorded run-1 results reproduce (constant best chi^2 10.275 at Omega_m 0.298; HDE best
  10.045 at Omega_m 0.272, c 0.93, w today -0.945).
"""
import math
import sys

import numpy as np

Z = np.array([0.295, 0.510, 0.510, 0.706, 0.706, 0.934, 0.934, 1.321, 1.321, 1.484, 1.484, 2.33, 2.33])
KIND = ["DV", "DM", "DH", "DM", "DH", "DM", "DH", "DM", "DH", "DM", "DH", "DH", "DM"]
DATA = np.array([7.94167639, 13.58758434, 21.86294686, 17.35069094, 19.45534918, 21.57563956, 17.64149464,
                 27.60085612, 14.17602155, 30.51190063, 12.81699964, 8.631545674846294, 38.988973961958784])
COV = np.zeros((13, 13))
COV[0, 0] = 5.78998687e-03
for (i, j), (vi, cij, vj) in {(1, 2): (2.83473742e-02, -3.26062007e-02, 1.83928040e-01),
                              (3, 4): (3.23752442e-02, -2.37445646e-02, 1.11469198e-01),
                              (5, 6): (2.61732816e-02, -1.12938006e-02, 4.04183878e-02),
                              (7, 8): (1.05336516e-01, -2.90308418e-02, 5.04233092e-02),
                              (9, 10): (5.83020277e-01, -1.95215562e-01, 2.68336193e-01),
                              (11, 12): (1.02136194e-02, -2.31395216e-02, 2.82685779e-01)}.items():
    COV[i, i], COV[i, j], COV[j, i], COV[j, j] = vi, cij, cij, vj
CINV = np.linalg.inv(COV)

N = 6000
X = np.linspace(0.0, math.log(1 / (1 + 2.33)) - 0.01, N)  # from a = 1 back past z = 2.33 (descending x)
A = np.exp(X)


def omega_de_history(om, cs):
    """RK4 in x for many c at once, starting from Omega_de(a=1) = 1 - om. Returns array (len(cs), N)."""
    cs = np.asarray(cs, dtype=float)
    out = np.empty((len(cs), N))
    y = np.full(len(cs), 1.0 - om)
    out[:, 0] = y
    f = lambda o: o * (1 - o) * (1 + 2 * np.sqrt(np.clip(o, 0, 1)) / cs)
    for k in range(1, N):
        h = X[k] - X[k - 1]
        k1 = f(y); k2 = f(y + 0.5 * h * k1); k3 = f(y + 0.5 * h * k2); k4 = f(y + h * k3)
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        out[:, k] = y
    return out


def distances(E):
    """E: array (M, N) on the descending x grid. Returns unit-free model vectors (M, 13)."""
    integrand = 1.0 / (A * E)                                   # d(DM)/d(-x)
    dx = -np.diff(X)
    cum = np.concatenate([np.zeros((E.shape[0], 1)), np.cumsum(0.5 * (integrand[:, 1:] + integrand[:, :-1]) * dx, axis=1)], axis=1)
    out = np.empty((E.shape[0], 13))
    for k, (z, kind) in enumerate(zip(Z, KIND)):
        xz = math.log(1 / (1 + z))
        j = int(np.searchsorted(-X, -xz))                       # first index with X <= xz
        t = (X[j - 1] - xz) / (X[j - 1] - X[j])
        dm = cum[:, j - 1] * (1 - t) + cum[:, j] * t
        Ez = E[:, j - 1] * (1 - t) + E[:, j] * t
        dh = 1.0 / Ez
        out[:, k] = dm if kind == "DM" else dh if kind == "DH" else (z * dm * dm * dh) ** (1 / 3)
    return out


def chi2_min(F):
    num = F @ CINV @ DATA
    den = np.einsum("ij,jk,ik->i", F, CINV, F)
    return float(DATA @ CINV @ DATA) - num ** 2 / den


def lcdm_E(om):
    return np.sqrt(om * A ** -3 + 1 - om)[None, :]


def main():
    w_li = -1 / 3 - (2 / 3) * math.sqrt(0.73)
    E_big = np.sqrt(0.315 * A ** -3 / (1 - omega_de_history(0.315, [1e6])))
    p0b = float(np.max(np.abs(distances(E_big) / distances(lcdm_E(0.315)) - 1)))
    print("P0: w(Omega 0.73, c 1) = %.4f; c = 1e6 vs constant dark energy max relative difference %.1e" % (w_li, p0b))

    oms = np.arange(0.25, 0.4001, 0.002)
    cs = np.arange(0.30, 2.0001, 0.01)
    lcdm = np.array([chi2_min(distances(lcdm_E(om)))[0] for om in oms])
    i_l = int(np.argmin(lcdm))
    print("constant dark energy (no radiation): best chi^2 %.3f at Omega_m %.3f" % (lcdm[i_l], oms[i_l]))

    best = (np.inf, None, None)
    for om in oms:
        od = omega_de_history(om, cs)
        E = np.sqrt(om * A[None, :] ** -3 / (1 - od))
        chi = chi2_min(distances(E))
        j = int(np.argmin(chi))
        if chi[j] < best[0]:
            best = (float(chi[j]), float(om), float(cs[j]))
    chi_h, om_h, c_h = best
    w0 = -1 / 3 - (2 / (3 * c_h)) * math.sqrt(1 - om_h)
    print("HDE (future event horizon): best chi^2 %.3f at Omega_m %.3f, c %.2f; w today %.3f" % (chi_h, om_h, c_h, w0))
    print("Delta chi^2 (HDE - constant) %.3f; Delta AIC (one extra parameter) %.3f" % (chi_h - lcdm[i_l], chi_h - lcdm[i_l] + 2))
    at_edge = c_h in (cs[0], cs[-1]) or om_h in (oms[0], oms[-1])
    if at_edge:
        print("note: best fit is at the edge of the grid")

    checks = [
        ("P0 w formula matches Li's -0.90 and c -> infinity gives constant dark energy", abs(w_li + 0.903) < 0.005 and p0b < 1e-4),
        ("P1 constant dark energy best chi^2 between 9 and 12", 9 <= lcdm[i_l] <= 12),
        ("P2 HDE best-fit c between 0.5 and 1.5", 0.5 <= c_h <= 1.5),
        ("P3 HDE best chi^2 within 4 of constant dark energy", abs(chi_h - lcdm[i_l]) < 4),
        ("P4 w today between -1.1 and -0.85", -1.1 <= w0 <= -0.85),
    ]
    print("\nOriginal frozen predictions (first-run verdicts are the record: P0 was WRONG on its second half):")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))

    # after freezing: consistency of the Omega_de equation with Li's w, and reproduction of the recorded results
    o = np.linspace(0.05, 0.95, 19)
    worst = 0.0
    for cc in (0.5, 0.93, 2.0):
        lhs = o * (1 - o) * (1 + 2 * np.sqrt(o) / cc)
        w = -1 / 3 - (2 / (3 * cc)) * np.sqrt(o)
        worst = max(worst, float(np.max(np.abs(lhs - (-3 * w * o * (1 - o))))))
    recorded = [
        ("R0 Omega_de equation equals -3 w Omega (1 - Omega)", worst < 1e-12),
        ("R1 constant dark energy best chi^2 10.275 at Omega_m 0.298", abs(lcdm[i_l] - 10.275) < 0.001 and abs(oms[i_l] - 0.298) < 1e-9),
        ("R2 HDE best chi^2 10.045 at Omega_m 0.272, c 0.93, w today -0.945",
         abs(chi_h - 10.045) < 0.001 and abs(om_h - 0.272) < 1e-9 and abs(c_h - 0.93) < 1e-9 and abs(w0 + 0.945) < 0.001),
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
