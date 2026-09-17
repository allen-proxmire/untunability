"""Does the Fourier hand hold across steepness, and does the Grover coin form a uniform hand anywhere? (RD7; follows C45-C47)

Same rule as discrete_hand_test.py and lasting_states_check.py (L 24, transfer meetings at every 2nd locus, Gamma 0.3, rate
feedback on the local displacement), at loop gains 1.5, 2, 3, 5, 10 (V0 = |0.9 chi| / gain), for three sets: Fourier g +0.9,
Grover g +0.9, Grover g -0.9. Starts 0-5 of the same 10 noisy starts. Each run: 6,000 steps, then 1,000 watched.

Each run is sorted into one kind (thresholds fixed before running):
  dead:      the largest |v| over the watched steps is below 1e-3;
  hand:      not dead, largest change of the state per step over the last 200 steps below 1e-8, no sign changes of the local
             displacement around the ring, amounts equal within each locus type to 1e-8;
  patterned: not dead, steady (as above), but not uniform;
  unsteady:  not dead and not steady.
For hand runs: v, the winding of the lossy step at the final rates, and the fingerprint (largest 12 eigenvalues of rho); the
fingerprint spread is taken over hand runs within each setting.

Expected results, written down before the first run (2026-09-14):
  S1 Fourier g +0.9: all 6 runs are hands at every one of the five gains, with winding 1, fingerprints agreeing to 1e-8 within
     each gain, and |v| not decreasing as the gain increases.
  S2 Grover g +0.9: all runs dead at every gain.
  S3 Grover g -0.9: no run is a hand at any gain.
Exit code: none of these is a code property; the script reports and exits 0 if it completes.
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
from discrete_hand_test import D, step, winding_at  # noqa: E402
from lasting_states_check import CHI, L, starts  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402

STEPS, WATCH, HIST = 6000, 1000, 200
GAINS = (1.5, 2.0, 3.0, 5.0, 10.0)
SETS = (("Fourier", 0.9), ("Grover", 0.9), ("Grover", -0.9))
NSTART = 6


def run(job):
    name, g, gain, i = job
    C = fp.FOURIER if name == "Fourier" else fp.GROVER
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    V0 = abs(0.9 * CHI[name]) / gain
    rho = starts()[i]
    for _ in range(STEPS):
        rho, s = step(rho, W, Cf, lane, dest, L, g, V0)
    vmax, change = 0.0, 0.0
    for t in range(WATCH):
        new, s = step(rho, W, Cf, lane, dest, L, g, V0)
        if t >= WATCH - HIST:
            change = max(change, float(np.max(np.abs(new - rho))))
        rho = new
        vmax = max(vmax, abs(fp.displacement(rho, Cf, L)))
    v = fp.displacement(rho, Cf, L)
    r = Cf @ rho @ Cf.conj().T
    dd = np.real(np.diag(r)).reshape(L, 3)
    dens = dd[:, fp.RI] - dd[:, fp.LE]
    signs = np.sign(dens[np.abs(dens) > 1e-12])
    sign_changes = int(np.sum(signs != np.roll(signs, 1))) if len(signs) else 0
    amounts = np.real(np.diag(rho)).reshape(L, 3).sum(axis=1)
    uniform = sign_changes == 0 and np.ptp(amounts[0::D]) < 1e-8 and np.ptp(amounts[1::D]) < 1e-8
    steady = change < 1e-8
    if vmax < 1e-3:
        kind = "dead"
    elif not steady:
        kind = "unsteady"
    elif uniform:
        kind = "hand"
    else:
        kind = "patterned"
    out = {"job": job, "kind": kind, "v": v, "vmax": vmax, "change": change, "sign_changes": sign_changes,
           "amount_spread": float(max(np.ptp(amounts[0::D]), np.ptp(amounts[1::D])))}
    if kind == "hand":
        out["winding"] = winding_at(W, L, s, g)
        out["fp"] = np.sort(np.real(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))))[::-1][:12]
    return out


def main():
    jobs = [(name, g, gain, i) for name, g in SETS for gain in GAINS for i in range(NSTART)]
    results = {}
    with Pool(7) as pool:
        for a in pool.imap_unordered(run, jobs):
            name, g, gain, i = a["job"]
            results[a["job"]] = a
            print("done %s g %+.1f gain %4.1f start %d: %s" % (name, g, gain, i, a["kind"]), flush=True)

    print("\nBy setting:")
    summary = {}
    for name, g in SETS:
        for gain in GAINS:
            rs = [results[(name, g, gain, i)] for i in range(NSTART)]
            kinds = [a["kind"] for a in rs]
            hands = [a for a in rs if a["kind"] == "hand"]
            fps = float(np.max(np.ptp(np.array([a["fp"] for a in hands]), axis=0))) if len(hands) > 1 else float("nan")
            summary[(name, g, gain)] = (kinds, hands, fps)
            print("%s g %+.1f gain %4.1f: kinds %s; v %s; largest |v| watched %s; change %s; sign changes %s; amount spread %s; "
                  "windings of hands %s; fingerprint spread of hands %.1e"
                  % (name, g, gain, kinds, " ".join("%+.4e" % a["v"] for a in rs), " ".join("%.1e" % a["vmax"] for a in rs),
                     " ".join("%.0e" % a["change"] for a in rs), [a["sign_changes"] for a in rs],
                     " ".join("%.0e" % a["amount_spread"] for a in rs), [a["winding"] for a in hands], fps), flush=True)

    s1 = True
    last = 0.0
    for gain in GAINS:
        kinds, hands, fps = summary[("Fourier", 0.9, gain)]
        if len(hands) != NSTART or any(a["winding"] != 1 for a in hands) or not fps < 1e-8:
            s1 = False
            continue
        vmean = float(np.mean([abs(a["v"]) for a in hands]))
        if vmean < last - 1e-9:
            s1 = False
        last = vmean
    s2 = all(k == "dead" for gain in GAINS for k in summary[("Grover", 0.9, gain)][0])
    s3 = all(k != "hand" for gain in GAINS for k in summary[("Grover", -0.9, gain)][0])
    print("\nExpected results:")
    for label, ok in (("S1 Fourier g +0.9: hands at every gain, winding 1, one state and its mirror, |v| not decreasing", s1),
                      ("S2 Grover g +0.9: dead at every gain", s2),
                      ("S3 Grover g -0.9: no hand at any gain", s3)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
