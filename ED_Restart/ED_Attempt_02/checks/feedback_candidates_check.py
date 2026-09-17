"""Does an ED-native feedback hold the hand? (RD11; follows C62-C64; reasoning in C69; coin plain Fourier, D7)

So far the draw rates followed the local flow through a chosen law, Gamma (1 -+ g tanh(v / V0)), with a chosen steepness (C65).
Candidate from ED's own pieces (C69): meetings pass motion into committed matter, committed matter keeps the momentum it receives,
and the chance of a meeting scales with the relative velocity of lane amplitude and committed matter.

Rule as in robustness_check.py at the current values (L 24, meeting spacing 2, Gamma 0.3), except the draw probabilities:
  K1 kinematic, integrated (the candidate): each committed locus holds momentum P_x (starting at 0) and a fixed rest amount m0 = 1;
     its velocity u_x = clip(P_x / m0, -1, 1); p_R = Gamma (1 - u_x), p_L = Gamma (1 + u_x); after each step P_x gains the
     expected captured Right amount minus the captured Left amount (p_R n_R - p_L n_L, with n the lane populations at x after the
     walk). Its steady states need p_R n_R = p_L n_L, i.e. u_x = eps_x = (n_R - n_L) / (n_R + n_L), with no free steepness.
  K2 instantaneous, strength kappa: p_R = Gamma (1 - s_x), p_L = Gamma (1 + s_x), s_x = clip(kappa eps_x, -1, 1), eps_x read after
     the walk each step. kappa = 1 is the candidate's steady-state law; kappa = 2, 4, 8 show how much stronger a hand needs.
Seven starts as before; 4,000 steps, then 500 watched. Kinds as in robustness_check.py (dead, unsteady, hand = steady and unchanged by
a shift of 2 loci, patterned); for K1 'steady' also needs the largest change of P per step below 1e-8. Hands report v and winding.
'Found' as in RD10: a hand from at least 4 of the 7 starts.

Expected results, written down before the first run (2026-09-14):
  F1 K1 (the ED-native candidate): no hand from any start.
  F2 K2 at kappa = 1: no hand from any start.
  F3 K2: found at kappa = 4 or 8, not at 2.
  F4 every hand has winding 1.
Exit code: 0 if it completes.
"""
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
import robustness_check as rc  # noqa: E402
from rule_v4 import kraus, lane_channels  # noqa: E402

L, D, GAM, M0 = 24, 2, 0.3, 1.0
STEPS, WATCH, HIST = 4000, 500, 200
MODELS = [("K1", None)] + [("K2", k) for k in (1.0, 2.0, 4.0, 8.0)]


def run(job):
    model, kappa, k = job
    W, Cf = fp.walk_matrix(L, rc.C), fp.coin_full(L, rc.C)
    lane, dest = lane_channels(L, D)
    x = np.arange(0, L, D)
    half = len(lane) // 2
    assert np.array_equal(lane[:half], 3 * x + fp.RI) and np.array_equal(lane[half:], 3 * x + fp.LE)
    rho = rc.start(L, k)
    P = np.zeros(len(x))
    vmax = change = pchange = 0.0
    s = np.zeros(len(x))
    for t in range(STEPS + WATCH):
        w = W @ rho @ W.conj().T
        d = np.real(np.diag(w))
        nR, nL = d[3 * x + fp.RI], d[3 * x + fp.LE]
        if model == "K1":
            s = np.clip(P / M0, -1.0, 1.0)
        else:
            eps = (nR - nL) / np.maximum(nR + nL, 1e-300)
            s = np.clip(kappa * eps, -1.0, 1.0)
        pR, pL = GAM * (1 - s), GAM * (1 + s)
        new = kraus(w, lane, dest, np.concatenate([pR, pL]))
        if model == "K1":
            dP = pR * nR - pL * nL
            P = P + dP
        if t >= STEPS:
            if t >= STEPS + WATCH - HIST:
                change = max(change, float(np.max(np.abs(new - rho))))
                if model == "K1":
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
    out = {"kind": kind, "v": v, "change": change, "pchange": pchange, "s_mean": float(np.mean(s)), "s_spread": float(np.ptp(s))}
    if kind == "hand":
        c = dict(rc.BASE, g=1.0)
        out["winding"] = rc.winding(W, c, s)
    return job, out


def main():
    jobs = [(m, kap, k) for m, kap in MODELS for k in range(rc.NSTART)]
    with Pool(7) as pool:
        res = dict(pool.map(run, jobs))
    letter = {"hand": "H", "dead": "D", "patterned": "P", "unsteady": "U"}
    found, windings_ok = {}, True
    print("Starts in order: %s; H hand, D dead, P patterned, U unsteady" % ", ".join(rc.START_NAMES))
    for m, kap in MODELS:
        rs = [res[(m, kap, k)] for k in range(rc.NSTART)]
        hands = [a for a in rs if a["kind"] == "hand"]
        found[(m, kap)] = len(hands) >= 4
        if any(a["winding"] != 1 for a in hands):
            windings_ok = False
        label = "K1 kinematic integrated" if m == "K1" else "K2 instantaneous kappa %.0f" % kap
        print("%-28s %s  hands %d; v %s; windings %s; final rate asymmetry s mean %s; largest change %.0e; largest momentum change %.0e"
              % (label, "".join(letter[a["kind"]] for a in rs), len(hands), " ".join("%+.5e" % a["v"] for a in hands),
                 [a["winding"] for a in hands], " ".join("%+.3f" % a["s_mean"] for a in rs), max(a["change"] for a in rs),
                 max(a["pchange"] for a in rs)), flush=True)
    anyhand = lambda m, kap: any(res[(m, kap, k)]["kind"] == "hand" for k in range(rc.NSTART))
    f1 = not anyhand("K1", None)
    f2 = not anyhand("K2", 1.0)
    f3 = (found[("K2", 4.0)] or found[("K2", 8.0)]) and not found[("K2", 2.0)]
    print("\nExpected results:")
    for label, ok in (("F1 K1 ED-native candidate: no hand", f1), ("F2 K2 kappa 1: no hand", f2),
                      ("F3 K2 found at kappa 4 or 8, not 2", f3), ("F4 every hand has winding 1", windings_ok)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
