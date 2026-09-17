"""The threshold law under its exit rule (RD12; derivation in Threshold_Law.md, written before this check; coin plain Fourier, D7).

Rule as in feedback_candidates_check.py (L 24, meeting spacing 2), with the derived draw probabilities
  p_R = P3(lambda (1 - u_x)), p_L = P3(lambda (1 + u_x)), P3(mu) = 1 - e^{-mu} (1 + mu + mu^2 / 2), P3(lambda) = Gamma,
  u_x = clip(P_x / m0, -1, 1), m0 = 1, P_x += p_R n_R - p_L n_L after each step (n = lane populations at x after the walk).
Base strengths Gamma = 0.3 and 0.05. Seven starts as before. Steps 4,000 x max(1, 0.3 / Gamma), then 500 watched.
Comparison (not counted for the exit rule): the same threshold law with u_x = eps_x = (n_R - n_L) / (n_R + n_L) read each step.
Kinds as in feedback_candidates_check.py (for the derived law, steady also needs the largest momentum change per step below 1e-8).
Hands report v and the winding of the lossy step at the final rates.

Exit rule (RD12, confirmed before the derivation): if the derived law holds no hand, a hand from at least 4 of the 7 starts at
Gamma 0.3 or at Gamma 0.05, the discrete handedness line is closed as 'hosted, not made'.

Expected results, written down before the first run (2026-09-14):
  T0 harness: P3(lambda) reproduces Gamma to 1e-12; kappa(lambda) = lambda P3'(lambda) / P3(lambda) is 1.73 (to 0.01) at Gamma 0.3
     and between 2.7 and 3 at Gamma 0.05.
  T1 derived law, Gamma 0.3: no hand from any start.
  T2 derived law, Gamma 0.05: no hand from any start.
  T3 comparison (instantaneous), Gamma 0.3: no hand from any start.
  T4 comparison (instantaneous), Gamma 0.05: no hand from any start (low confidence: its steepness, about 2.8, lies between C70's
     no-hand at 2 and lasting flows at 4).
  Exit: the line is closed as 'hosted, not made'.
Exit code: 0 if it completes.
"""
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import math  # noqa: E402
import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
import robustness_check as rc  # noqa: E402
from rule_v4 import kraus, lane_channels  # noqa: E402

L, D, M0 = 24, 2, 1.0
WATCH, HIST = 500, 200
GAMMAS = (0.3, 0.05)
MODELS = ("derived", "instant")


def P3(mu):
    mu = np.asarray(mu, dtype=float)
    return 1.0 - np.exp(-mu) * (1.0 + mu + mu ** 2 / 2.0)


def lam_for(gam):
    lo, hi = 1e-9, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if P3(mid) < gam:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kappa(lam):
    return lam * (math.exp(-lam) * lam ** 2 / 2.0) / float(P3(lam))


def winding_p(W, p):
    n = 3 * L
    lane, dest = lane_channels(L, D)
    scale = np.ones(n)
    scale[lane] = np.sqrt(1 - p)
    eigs = []
    for ph in np.linspace(0, 2 * np.pi, 301):
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


def run(job):
    model, gam, k = job
    lam = lam_for(gam)
    W, Cf = fp.walk_matrix(L, rc.C), fp.coin_full(L, rc.C)
    lane, dest = lane_channels(L, D)
    x = np.arange(0, L, D)
    half = len(lane) // 2
    assert np.array_equal(lane[:half], 3 * x + fp.RI) and np.array_equal(lane[half:], 3 * x + fp.LE)
    steps = int(4000 * max(1.0, 0.3 / gam))
    rho = rc.start(L, k)
    P = np.zeros(len(x))
    vmax = change = pchange = 0.0
    p = None
    for t in range(steps + WATCH):
        w = W @ rho @ W.conj().T
        d = np.real(np.diag(w))
        nR, nL = d[3 * x + fp.RI], d[3 * x + fp.LE]
        if model == "derived":
            u = np.clip(P / M0, -1.0, 1.0)
        else:
            u = (nR - nL) / np.maximum(nR + nL, 1e-300)
        pR, pL = P3(lam * (1 - u)), P3(lam * (1 + u))
        p = np.concatenate([pR, pL])
        new = kraus(w, lane, dest, p)
        dP = pR * nR - pL * nL
        if model == "derived":
            P = P + dP
        if t >= steps:
            if t >= steps + WATCH - HIST:
                change = max(change, float(np.max(np.abs(new - rho))))
                if model == "derived":
                    pchange = max(pchange, float(np.max(np.abs(dP))))
            vmax = max(vmax, abs(fp.displacement(new, Cf, L)))
        rho = new
    v = fp.displacement(rho, Cf, L)
    idx = rc.shift_perm(L, D)
    shift_err = float(np.max(np.abs(rho[np.ix_(idx, idx)] - rho)))
    steady = change < 1e-8 and pchange < 1e-8
    if vmax < 1e-3:
        kind = "dead"
    elif not steady:
        kind = "unsteady"
    elif shift_err < 1e-8:
        kind = "hand"
    else:
        kind = "patterned"
    half_p = len(p) // 2
    asym = float(np.mean((p[half_p:] - p[:half_p]) / np.maximum(p[half_p:] + p[:half_p], 1e-300)))
    out = {"kind": kind, "v": v, "vmax": vmax, "asym": asym, "change": change, "pchange": pchange}
    if kind == "hand":
        out["winding"] = winding_p(W, p)
    return job, out


def main():
    t0 = {}
    for gam in GAMMAS:
        lam = lam_for(gam)
        t0[gam] = (lam, abs(float(P3(lam)) - gam), kappa(lam))
        print("Gamma %.2f: lambda %.6f, |P3(lambda) - Gamma| %.1e, kappa %.4f" % (gam, lam, t0[gam][1], t0[gam][2]), flush=True)
    jobs = [(m, gam, k) for m in MODELS for gam in GAMMAS for k in range(rc.NSTART)]
    with Pool(7) as pool:
        res = dict(pool.map(run, jobs))
    letter = {"hand": "H", "dead": "D", "patterned": "P", "unsteady": "U"}
    print("\nStarts in order: %s; H hand, D dead, P patterned, U unsteady" % ", ".join(rc.START_NAMES))
    found, nh = {}, {}
    for m in MODELS:
        for gam in GAMMAS:
            rs = [res[(m, gam, k)] for k in range(rc.NSTART)]
            hands = [a for a in rs if a["kind"] == "hand"]
            nh[(m, gam)] = len(hands)
            found[(m, gam)] = len(hands) >= 4
            print("%-8s Gamma %.2f: %s  hands %d; v %s; windings %s; largest |v| watched %s; final rate asymmetry %s; largest change %.0e; largest momentum change %.0e"
                  % (m, gam, "".join(letter[a["kind"]] for a in rs), len(hands), " ".join("%+.5e" % a["v"] for a in hands),
                     [a["winding"] for a in hands], " ".join("%.1e" % a["vmax"] for a in rs), " ".join("%+.3f" % a["asym"] for a in rs),
                     max(a["change"] for a in rs), max(a["pchange"] for a in rs)), flush=True)
    derived_found = found[("derived", 0.3)] or found[("derived", 0.05)]
    print("\nExit rule (RD12): derived law found at Gamma 0.3: %s; at Gamma 0.05: %s" % (found[("derived", 0.3)], found[("derived", 0.05)]))
    print("VERDICT: %s" % ("the derived law holds a hand; the line stays open" if derived_found
                            else "the derived law holds no hand; the discrete handedness line is closed as 'hosted, not made'"))
    t0ok = (all(t0[g][1] < 1e-12 for g in GAMMAS) and abs(t0[0.3][2] - 1.73) < 0.01 and 2.7 <= t0[0.05][2] <= 3.0)
    print("\nExpected results:")
    for label, ok in (("T0 harness: P3 and kappa", t0ok),
                      ("T1 derived, Gamma 0.3: no hand", nh[("derived", 0.3)] == 0),
                      ("T2 derived, Gamma 0.05: no hand", nh[("derived", 0.05)] == 0),
                      ("T3 comparison, Gamma 0.3: no hand", nh[("instant", 0.3)] == 0),
                      ("T4 comparison, Gamma 0.05: no hand", nh[("instant", 0.05)] == 0),
                      ("Exit: closed as 'hosted, not made'", not derived_found)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
