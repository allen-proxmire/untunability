"""Check C246: horizon-set births (RD42) against DESI DR2 BAO + Union3 supernovae + the Planck CMB shift parameter R.

Data:
  BAO: DESI DR2, 13 values and covariance (as in bao_distance_test.py, C220); one free scale c/(H0 r_d).
  SNe: Union3 compressed (22 binned magnitudes with 22 x 22 covariance), files checks/data/union3_lcparam_full.txt and
       union3_mag_covmat.txt, downloaded verbatim 2026-09-14 from the Cobaya sn_data release (Rubin et al., Union3/UNITY1.5,
       arXiv:2311.12098); m = 5 log10((1 + z) D_M) + offset, offset marginalized analytically.
  CMB: shift parameter R = sqrt(Omega_m) * int_0^z* dz / E(z) = 1.7502 +- 0.0046 (Planck 2018 TT,TE,EE+lowE, LambdaCDM
       distance prior; Chen, Huang, Wang, JCAP 02 (2019) 028, Table I). z* from their Eqs. 8-10 with omega_b = 0.02236;
       radiation Omega_r = Omega_m / (1 + z_eq), z_eq = 2.5e4 Omega_m h^2 (T_CMB/2.7)^-4, T_CMB = 2.7255 K (their Eq. 5 text).
       h = 0.674 is fixed (it enters only through z* and radiation). l_A is not used (it needs the sound horizon).
Models (flat):
  REF  constant dark energy: E^2 = Omega_m a^-3 + Omega_r a^-4 + (1 - Omega_m - Omega_r).
  HDE  future-event-horizon holographic dark energy, with radiation: x = ln a,
       dOmega_de/dx = Omega_de [ (1 - Omega_de)(1 + 2 sqrt(Omega_de)/c) + Omega_rad(a) ],
       Omega_rad(a) = (1 - Omega_de) Omega_r a^-4 / (Omega_m a^-3 + Omega_r a^-4),
       E^2 = (Omega_m a^-3 + Omega_r a^-4) / (1 - Omega_de),  Omega_de(1) = 1 - Omega_m - Omega_r.
       (From dOmega/dx = Omega(-3w(1 - Omega) + Omega_rad) with Li's w = -1/3 - 2 sqrt(Omega)/(3c).)
Grid: Omega_m 0.24-0.40 (step 0.002), c 0.30-2.00 (step 0.01).

Caveats: CMB compressed to R only, taken from a LambdaCDM-derived prior; h fixed; Union3 compressed nodes; no
perturbations; the ED reading is an interpretation of a known model.

Predictions frozen before the first run (2026-09-14):
  P0  (code) REF with Omega_m 0.315 gives R between 1.73 and 1.77; the HDE equation equals Omega(-3w(1 - Omega) + Omega_rad).
  P1  REF combined best chi^2 (36 data points) between 25 and 50.
  P2  REF best Omega_m between 0.29 and 0.33.
  P3  HDE best c between 0.5 and 1.5.
  P4  HDE best chi^2 within 6 of REF's.
  P5  HDE best Omega_m is higher than its BAO-only value 0.272 (C242).
  P6  Delta AIC (HDE - REF, one extra number) is positive: not preferred. (Low confidence: Union3 alone hints at evolving dark energy.)

Changes after freezing (2026-09-14):
  Run 1 (hde_combined_test_run1.txt): P0, P1, P2, P3, P5, P6 RIGHT; P4 WRONG. REF best chi^2 40.058 at Omega_m 0.310
  (BAO 12.41, SN 27.05, CMB R 0.60); HDE best chi^2 72.810 at Omega_m 0.306, c 0.67 (BAO 30.95, SN 34.51, CMB R 7.34),
  w today -1.162; Delta chi^2 +32.75, Delta AIC +34.75. The original verdicts stand and are still printed. The exit
  code now checks that these recorded results reproduce, so the test can run in run_checks.
"""
import math
import sys
from pathlib import Path

import numpy as np

H = 0.674
T_CMB = 2.7255
OMB = 0.02236
R_OBS, R_ERR = 1.7502, 0.0046

Z = np.array([0.295, 0.510, 0.510, 0.706, 0.706, 0.934, 0.934, 1.321, 1.321, 1.484, 1.484, 2.33, 2.33])
KIND = ["DV", "DM", "DH", "DM", "DH", "DM", "DH", "DM", "DH", "DM", "DH", "DH", "DM"]
BAO = np.array([7.94167639, 13.58758434, 21.86294686, 17.35069094, 19.45534918, 21.57563956, 17.64149464,
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
BINV = np.linalg.inv(COV)

here = Path(__file__).resolve().parent / "data"
lc = [l.split() for l in (here / "union3_lcparam_full.txt").read_text().splitlines() if l and not l.startswith("#")]
SN_Z = np.array([float(r[1]) for r in lc])
SN_M = np.array([float(r[4]) for r in lc])
v = np.loadtxt(here / "union3_mag_covmat.txt").ravel()
SNINV = np.linalg.inv(v[1:].reshape(int(v[0]), int(v[0])))
ONES = np.ones(len(SN_Z))


def z_star(om):
    wm = om * H * H
    g1 = 0.0738 * OMB ** -0.238 / (1 + 39.5 * OMB ** 0.763)
    g2 = 0.560 / (1 + 21.1 * OMB ** 1.81)
    return 1048 * (1 + 0.00124 * OMB ** -0.738) * (1 + g1 * wm ** g2)


def omega_r(om):
    z_eq = 2.5e4 * om * H * H * (T_CMB / 2.7) ** -4
    return om / (1 + z_eq)


N = 14000
X = np.linspace(0.0, math.log(1 / 1300.0), N)
A = np.exp(X)


def hde_E(om, cs):
    orad = omega_r(om)
    cs = np.asarray(cs, dtype=float)
    y = np.full(len(cs), 1.0 - om - orad)
    out = np.empty((len(cs), N))
    out[:, 0] = y
    base = om * A ** -3 + orad * A ** -4

    def f(o, k_idx_frac):
        a = k_idx_frac
        rad = (1 - o) * orad * a ** -4 / (om * a ** -3 + orad * a ** -4)
        return o * ((1 - o) * (1 + 2 * np.sqrt(np.clip(o, 0, 1)) / cs) + rad)

    for k in range(1, N):
        h = X[k] - X[k - 1]
        a0, a1 = A[k - 1], A[k]
        am = math.exp(0.5 * (X[k] + X[k - 1]))
        k1 = f(y, a0); k2 = f(y + 0.5 * h * k1, am); k3 = f(y + 0.5 * h * k2, am); k4 = f(y + h * k3, a1)
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        out[:, k] = y
    return np.sqrt(base[None, :] / (1 - out))


def ref_E(om):
    orad = omega_r(om)
    return np.sqrt(om * A ** -3 + orad * A ** -4 + 1 - om - orad)[None, :]


def observables(E, om):
    """Returns BAO vectors (M,13), SN distance moduli without offset (M,22), R (M,)."""
    integrand = 1.0 / (A * E)
    dx = -np.diff(X)
    cum = np.concatenate([np.zeros((E.shape[0], 1)), np.cumsum(0.5 * (integrand[:, 1:] + integrand[:, :-1]) * dx, axis=1)], axis=1)

    def at(z):
        xz = math.log(1 / (1 + z))
        j = int(np.searchsorted(-X, -xz))
        t = (X[j - 1] - xz) / (X[j - 1] - X[j])
        return cum[:, j - 1] * (1 - t) + cum[:, j] * t, E[:, j - 1] * (1 - t) + E[:, j] * t

    bao = np.empty((E.shape[0], 13))
    for k, (z, kind) in enumerate(zip(Z, KIND)):
        dm, Ez = at(z)
        dh = 1 / Ez
        bao[:, k] = dm if kind == "DM" else dh if kind == "DH" else (z * dm * dm * dh) ** (1 / 3)
    sn = np.empty((E.shape[0], len(SN_Z)))
    for k, z in enumerate(SN_Z):
        dm, _ = at(z)
        sn[:, k] = 5 * np.log10((1 + z) * dm)
    dm_star, _ = at(z_star(om))
    return bao, sn, math.sqrt(om) * dm_star


def chi2(bao, sn, R):
    num = bao @ BINV @ BAO
    den = np.einsum("ij,jk,ik->i", bao, BINV, bao)
    c_bao = float(BAO @ BINV @ BAO) - num ** 2 / den
    d = SN_M[None, :] - sn
    c_sn = np.einsum("ij,jk,ik->i", d, SNINV, d) - (d @ SNINV @ ONES) ** 2 / (ONES @ SNINV @ ONES)
    c_cmb = ((R - R_OBS) / R_ERR) ** 2
    return c_bao + c_sn + c_cmb, c_bao, c_sn, c_cmb


def main():
    _, _, R_planck = observables(ref_E(0.315), 0.315)
    o = np.linspace(0.05, 0.95, 19)
    worst = 0.0
    for cc in (0.5, 1.0):
        rad = 0.2 * (1 - o)
        lhs = o * ((1 - o) * (1 + 2 * np.sqrt(o) / cc) + rad)
        w = -1 / 3 - (2 / (3 * cc)) * np.sqrt(o)
        worst = max(worst, float(np.max(np.abs(lhs - o * (-3 * w * (1 - o) + rad)))))
    print("P0: REF R at Omega_m 0.315 = %.4f (z* %.1f); HDE equation identity error %.1e" % (R_planck[0], z_star(0.315), worst))

    oms = np.arange(0.24, 0.4001, 0.002)
    cs = np.arange(0.30, 2.0001, 0.01)
    ref_best = (np.inf,)
    for om in oms:
        tot, cb, cs_, cc = chi2(*observables(ref_E(om), om))
        if tot[0] < ref_best[0]:
            ref_best = (float(tot[0]), float(om), float(cb[0]), float(cs_[0]), float(cc[0]))
    print("REF best: chi^2 %.3f at Omega_m %.3f (BAO %.2f, SN %.2f, CMB R %.2f)" % ref_best)
    hde_best = (np.inf,)
    for om in oms:
        tot, cb, cs_, cc = chi2(*observables(hde_E(om, cs), om))
        j = int(np.argmin(tot))
        if tot[j] < hde_best[0]:
            hde_best = (float(tot[j]), float(om), float(cs[j]), float(cb[j]), float(cs_[j]), float(cc[j]))
    chi_h, om_h, c_h = hde_best[:3]
    orad = omega_r(om_h)
    w0 = -1 / 3 - (2 / (3 * c_h)) * math.sqrt(1 - om_h - orad)
    print("HDE best: chi^2 %.3f at Omega_m %.3f, c %.2f (BAO %.2f, SN %.2f, CMB R %.2f); w today %.3f" % (hde_best + (w0,)))
    d = chi_h - ref_best[0]
    print("Delta chi^2 (HDE - REF) %.3f; Delta AIC %.3f" % (d, d + 2))
    if c_h in (cs[0], cs[-1]) or om_h in (oms[0], oms[-1]):
        print("note: HDE best fit at the edge of the grid")

    checks = [
        ("P0 REF R at 0.315 in [1.73, 1.77] and HDE equation identity", 1.73 <= R_planck[0] <= 1.77 and worst < 1e-12),
        ("P1 REF combined chi^2 between 25 and 50", 25 <= ref_best[0] <= 50),
        ("P2 REF best Omega_m between 0.29 and 0.33", 0.29 <= ref_best[1] <= 0.33),
        ("P3 HDE best c between 0.5 and 1.5", 0.5 <= c_h <= 1.5),
        ("P4 HDE chi^2 within 6 of REF", abs(d) < 6),
        ("P5 HDE best Omega_m above 0.272", om_h > 0.272),
        ("P6 Delta AIC positive (HDE not preferred)", d + 2 > 0),
    ]
    print("\nOriginal frozen predictions (first-run verdicts are the record: P4 was WRONG):")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))

    recorded = [
        ("R1 REF chi^2 40.058 at Omega_m 0.310", abs(ref_best[0] - 40.058) < 0.001 and abs(ref_best[1] - 0.310) < 1e-9),
        ("R2 HDE chi^2 72.810 at Omega_m 0.306, c 0.67, w today -1.162",
         abs(chi_h - 72.810) < 0.001 and abs(om_h - 0.306) < 1e-9 and abs(c_h - 0.67) < 1e-9 and abs(w0 + 1.162) < 0.001),
        ("R3 P0 code checks still hold", 1.73 <= R_planck[0] <= 1.77 and worst < 1e-12),
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
