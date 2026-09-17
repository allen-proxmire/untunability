"""Check C221: do clipped one-sided everpresent universes (RD38, RD39) fit DESI DR2 BAO distances as well as constant dark energy?

Data: DESI DR2 BAO, 13 values (DV/rd at z 0.295; DM/rd and DH/rd at z 0.510, 0.706, 0.934, 1.321, 1.484, 2.33) with
their covariance, copied verbatim from the Cobaya bao_data release files desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt
and _cov.txt (fetched 2026-09-14), which carry the DESI Collaboration DR2 Results II measurements (arXiv:2503.14738, C139).

Models (flat, Omega_m = 0.315, Omega_r = 9.1e-5, as in everpresent_onesided.py):
  REF      constant dark energy (Omega_L = 1 - Omega_m - Omega_r).
  CLIPPED  everpresent Model 1 (Das normalization, alpha = 0.012), dark energy = max(S, 0) 8 pi / V, with the
           early-volume fix from everpresent_onesided.py. 2,000 runs, seeds fixed. Today-like runs are kept
           (0.9 < H(1) < 1.1 and 0.6 < Omega_L(1) < 0.8).
For each model, E(z) = H / H0_ref, DM = int dz / E, DH = 1 / E, DV = (z DM^2 DH)^(1/3), all times one overall factor
A = c / (H0_ref r_d), fitted analytically (the only free number, the same for both models). chi^2 uses the full
covariance. Delta chi^2 = chi^2(run) - chi^2(REF).

Caveats: BAO only (no supernovae, no CMB); the sound horizon is absorbed into A, which ignores any change of r_d from
early dark energy; homogeneous toy; "clipped" is Claude's reading of "never negative"; Omega_m is fixed, not fitted.

Predictions frozen before the first run (2026-09-14):
  P0  (code) The distances computed on the simulation grid for REF agree with direct numerical integration to 1e-4.
  P1  REF chi^2 is between 8 and 30 (13 data points, 1 fitted factor).
  P2  More than half of the clipped today-like runs have Delta chi^2 > 4.
  P3  At least 5% of the clipped today-like runs have Delta chi^2 < 4.
  P4  The median Delta chi^2 of clipped today-like runs is above 9.
  P5  Runs whose dark energy changed by less than 30% since z = 1 have a lower median Delta chi^2 than runs whose dark
      energy changed by more than 100%.
  P6  The today-like share of the 2,000 clipped runs is between 4% and 11%.
"""
import math
import sys

import numpy as np

OM, OR = 0.315, 9.1e-5
A_START, STEPS, RUNS, ALPHA = 1e-6, 1400, 2000, 0.012

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


def distances_from_grid(a, E):
    """Unit-free DM, DH, DV at the data redshifts from E(a) on an ascending ln-a grid ending at a = 1."""
    lna = np.log(a)
    integrand = 1.0 / (a * E)                       # d(DM) = dlna / (a E)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lna))])
    DM_of_a = cum[-1] - cum                          # integral from a to 1
    out = np.empty(13)
    for k, (z, kind) in enumerate(zip(Z, KIND)):
        az = 1.0 / (1.0 + z)
        dm = np.interp(np.log(az), lna, DM_of_a)
        dh = 1.0 / np.interp(np.log(az), lna, E)
        out[k] = dm if kind == "DM" else dh if kind == "DH" else (z * dm * dm * dh) ** (1 / 3)
    return out


def chi2_min(f):
    A = (f @ CINV @ DATA) / (f @ CINV @ f)
    r = A * f - DATA
    return float(r @ CINV @ r), float(A)


def run(rng):
    lna = np.linspace(math.log(A_START), 0.0, STEPS + 1)
    a = np.exp(lna)
    dlna = lna[1] - lna[0]
    a_s = a[0]
    H_s = math.sqrt(OM * a_s ** -3 + OR * a_s ** -4)
    tau_s = 1.0 / (a_s * H_s)
    tau = np.zeros(STEPS + 1)
    tau[0] = tau_s

    def pre(tn):
        return (4 * math.pi / 3) * a_s ** 4 / tau_s ** 4 * (
            tn ** 3 * tau_s ** 5 / 5 - tn ** 2 * tau_s ** 6 / 2 + 3 * tn * tau_s ** 7 / 7 - tau_s ** 8 / 8)

    V_prev = pre(tau_s)
    S = ALPHA * math.sqrt(V_prev) * rng.standard_normal()
    lam = 8 * math.pi * max(S, 0.0) / V_prev
    lam_hist = np.zeros(STEPS + 1)
    lam_hist[0] = lam
    for n in range(1, STEPS + 1):
        H2 = OM * a[n] ** -3 + OR * a[n] ** -4 + lam / 3.0
        tau[n] = tau[n - 1] + dlna / (a[n] * math.sqrt(H2))
        ak = a[1: n + 1]
        wk = dlna / (ak * np.sqrt(OM * ak ** -3 + OR * ak ** -4 + lam_hist[1: n + 1] / 3.0))
        V = pre(tau[n]) + (4 * math.pi / 3) * np.sum(ak ** 4 * (tau[n] - tau[1: n + 1]) ** 3 * wk)
        dV = max(V - V_prev, 0.0)
        V_prev = V
        S = S + ALPHA * math.sqrt(dV) * rng.standard_normal()
        lam = 8 * math.pi * max(S, 0.0) / V
        lam_hist[n] = lam
    E = np.sqrt(OM * a ** -3 + OR * a ** -4 + lam_hist / 3.0)
    H1 = E[-1]
    OL = lam / (3 * H1 * H1)
    i_half = int(np.argmin(np.abs(a - 0.5)))
    change = abs(lam - lam_hist[i_half]) / lam if lam > 0 else float("inf")
    return a, E, H1, OL, change


def main():
    lna = np.linspace(math.log(A_START), 0.0, STEPS + 1)
    a = np.exp(lna)
    OL_ref = 1 - OM - OR
    E_ref = np.sqrt(OM * a ** -3 + OR * a ** -4 + OL_ref)
    f_ref = distances_from_grid(a, E_ref)
    # direct integration for P0
    zz = np.linspace(0, 2.33, 200001)
    Ez = np.sqrt(OM * (1 + zz) ** 3 + OR * (1 + zz) ** 4 + OL_ref)
    cumz = np.concatenate([[0.0], np.cumsum(0.5 * (1 / Ez[1:] + 1 / Ez[:-1]) * np.diff(zz))])
    f_dir = np.empty(13)
    for k, (z, kind) in enumerate(zip(Z, KIND)):
        dm = np.interp(z, zz, cumz)
        dh = 1 / math.sqrt(OM * (1 + z) ** 3 + OR * (1 + z) ** 4 + OL_ref)
        f_dir[k] = dm if kind == "DM" else dh if kind == "DH" else (z * dm * dm * dh) ** (1 / 3)
    p0_err = float(np.max(np.abs(f_ref / f_dir - 1)))
    chi_ref, A_ref = chi2_min(f_ref)
    print("REF (constant dark energy, Omega_m 0.315): chi^2 %.3f, fitted c/(H0 r_d) %.3f; grid vs direct max relative error %.1e"
          % (chi_ref, A_ref, p0_err))
    # context only: best-fit Omega_m for constant dark energy
    best = min((chi2_min(distances_from_grid(a, np.sqrt(om * a ** -3 + OR * a ** -4 + 1 - om - OR)))[0], om)
               for om in np.arange(0.25, 0.3801, 0.001))
    print("context: constant dark energy with Omega_m free: best chi^2 %.3f at Omega_m %.3f" % best)

    rng = np.random.default_rng(20260914)
    today = []
    for i in range(RUNS):
        a_r, E_r, H1, OL, change = run(rng)
        if 0.9 < H1 < 1.1 and 0.6 < OL < 0.8:
            chi, A = chi2_min(distances_from_grid(a_r, E_r))
            today.append((chi - chi_ref, change, chi))
        if (i + 1) % 250 == 0:
            print("  %d runs, %d today-like so far" % (i + 1, len(today)), flush=True)
    d = np.array([t[0] for t in today])
    ch = np.array([t[1] for t in today])
    share = len(today) / RUNS
    print("\nclipped today-like runs: %d of %d (%.3f)" % (len(today), RUNS, share))
    print("Delta chi^2: min %.2f, 10th pct %.2f, median %.2f, 90th pct %.2f" % (d.min(), np.percentile(d, 10), np.median(d), np.percentile(d, 90)))
    print("share Delta chi^2 < 0: %.3f, < 4: %.3f, > 25: %.3f" % (np.mean(d < 0), np.mean(d < 4), np.mean(d > 25)))
    small, large = d[ch < 0.3], d[ch > 1.0]
    print("change since z=1 < 30%%: %d runs, median Delta chi^2 %.2f; > 100%%: %d runs, median %.2f"
          % (len(small), np.median(small) if len(small) else float("nan"), len(large), np.median(large) if len(large) else float("nan")))

    checks = [
        ("P0 grid distances match direct integration to 1e-4", p0_err < 1e-4),
        ("P1 REF chi^2 between 8 and 30", 8 <= chi_ref <= 30),
        ("P2 more than half of today-like runs have Delta chi^2 > 4", np.mean(d > 4) > 0.5),
        ("P3 at least 5% have Delta chi^2 < 4", np.mean(d < 4) >= 0.05),
        ("P4 median Delta chi^2 above 9", np.median(d) > 9),
        ("P5 small-change runs fit better than large-change runs",
         len(small) > 0 and len(large) > 0 and np.median(small) < np.median(large)),
        ("P6 today-like share between 4% and 11%", 0.04 <= share <= 0.11),
    ]
    print()
    for name, passed in checks:
        print("%-6s %s" % ("RIGHT" if passed else "WRONG", name))
    print("ALL PREDICTIONS AS FROZEN" if all(p for _, p in checks) else "SOME PREDICTIONS WRONG")
    return all(p for _, p in checks)


def spot():
    """Change after freezing (2026-09-14): the full test takes several minutes, so run_checks uses this spot check.
    It rechecks the REF fit, the grid accuracy, the Omega_m-free best fit, and the today-like count after the first
    250 runs, against the recorded run-1 values (bao_distance_test_run1.txt)."""
    lna = np.linspace(math.log(A_START), 0.0, STEPS + 1)
    a = np.exp(lna)
    E_ref = np.sqrt(OM * a ** -3 + OR * a ** -4 + 1 - OM - OR)
    chi_ref, _ = chi2_min(distances_from_grid(a, E_ref))
    best = min((chi2_min(distances_from_grid(a, np.sqrt(om * a ** -3 + OR * a ** -4 + 1 - om - OR)))[0], om)
               for om in np.arange(0.25, 0.3801, 0.001))
    rng = np.random.default_rng(20260914)
    n_today = 0
    for _ in range(250):
        _, _, H1, OL, _ = run(rng)
        n_today += 0.9 < H1 < 1.1 and 0.6 < OL < 0.8
    checks = [("REF chi^2 14.308", abs(chi_ref - 14.308) < 0.001),
              ("Omega_m-free best chi^2 10.283 at 0.297", abs(best[0] - 10.283) < 0.001 and abs(best[1] - 0.297) < 0.0005),
              ("9 today-like runs in the first 250", n_today == 9)]
    ok = True
    for name, passed in checks:
        ok &= passed
        print("%-4s %s" % ("PASS" if passed else "FAIL", name))
    print("REF chi^2 %.3f, best %.3f at %.3f, today-like %d" % (chi_ref, best[0], best[1], n_today))
    return ok


if __name__ == "__main__":
    if "--spot" in sys.argv:
        sys.exit(0 if spot() else 1)
    sys.exit(0 if main() else 1)
