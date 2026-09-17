"""What are the lasting states of the discrete hand test? (RD6; follows C43)

Same rule and settings as discrete_hand_test.py (L 24, transfer meetings at every 2nd locus, Gamma 0.3, rate feedback on
the local displacement, loop gain 3, the 10 noisy starts), for four sets: Fourier g +0.9, Fourier g -0.9, Grover g -0.9,
Grover g +0.9. Each run goes 4,000 steps, then 2,000 more steps are watched.

Measured per run:
  steadiness: the largest change of the state per step over the last 200 steps; if it isn't steady, the smallest period
    P <= 200 with max |rho(t+P) - rho(t)| < 1e-9 at the end, or 'irregular';
  displacement v at the end, and its spread over the last 2,000 steps;
  spatial pattern: per-locus amount on committed and uncommitted loci (spread within each set), and the number of sign
    changes of the local displacement density around the ring (0 means uniform direction);
  a position-free fingerprint: the sorted eigenvalues of rho (unchanged by translation and mirror).

Expected results, written down before the first run (2026-09-14):
  L1 Fourier g +0.9: all 10 runs steady (largest change per step < 1e-10), the local displacement has no sign changes
     around the ring, each locus type (committed, uncommitted) has amounts equal to 1e-8, and all 10 fingerprints agree to
     1e-8 (one state and its mirror image).
  L2 Grover g -0.9: at least 5 of 10 runs are not steady.
  L3 Fourier g -0.9: at least 5 of 10 runs are not steady.
  L4 Grover g +0.9: all 10 runs steady with |v| < 1e-4.
Exit code: none of these is a code property; the script reports and exits 0 if it completes.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
from discrete_hand_test import D, GAMMA, step  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402

L, STEPS, WATCH, HIST = 24, 4000, 2000, 200
CHI = {"Grover": 2.2926e-01, "Fourier": 1.6515e-01}


def starts():
    rng = np.random.default_rng(1357)
    out = []
    for _ in range(10):
        psi = 1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)
        psi /= np.linalg.norm(psi)
        out.append(np.outer(psi, psi.conj()))
    return out


def analyse(name, C, g, rho0):
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    V0 = abs(0.9 * CHI[name]) / 3
    rho = rho0.copy()
    for _ in range(STEPS):
        rho, _ = step(rho, W, Cf, lane, dest, L, g, V0)
    hist, vs, changes = [], [], []
    for t in range(WATCH):
        new, _ = step(rho, W, Cf, lane, dest, L, g, V0)
        if t >= WATCH - HIST:
            changes.append(float(np.max(np.abs(new - rho))))
            hist.append(new)
        rho = new
        vs.append(fp.displacement(rho, Cf, L))
    steady = max(changes) < 1e-10
    period = None
    if not steady:
        for P in range(1, HIST):
            if float(np.max(np.abs(hist[-1] - hist[-1 - P]))) < 1e-9:
                period = P
                break
    r = Cf @ rho @ Cf.conj().T
    dd = np.real(np.diag(r)).reshape(L, 3)
    dens = dd[:, fp.RI] - dd[:, fp.LE]
    signs = np.sign(dens[np.abs(dens) > 1e-12])
    sign_changes = int(np.sum(signs != np.roll(signs, 1))) if len(signs) else 0
    amounts = np.real(np.diag(rho)).reshape(L, 3).sum(axis=1)
    spread_c = float(np.ptp(amounts[0::D]))
    spread_u = float(np.ptp(amounts[1::D]))
    fingerprint = np.sort(np.real(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))))[::-1][:12]
    return {"steady": steady, "maxchange": max(changes), "period": period, "v": vs[-1],
            "vspread": float(np.ptp(vs)), "sign_changes": sign_changes, "spread_c": spread_c, "spread_u": spread_u,
            "fp": fingerprint}


def main():
    st = starts()
    sets = [("Fourier", fp.FOURIER, 0.9), ("Fourier", fp.FOURIER, -0.9), ("Grover", fp.GROVER, -0.9), ("Grover", fp.GROVER, 0.9)]
    results = {}
    for name, C, g in sets:
        rs = []
        for i, rho0 in enumerate(st):
            a = analyse(name, C, g, rho0)
            rs.append(a)
            kind = "steady" if a["steady"] else ("period %d" % a["period"] if a["period"] else "irregular")
            print("%s g %+.1f start %d: %s (largest change %.1e); v %+.4e (spread over last 2,000 steps %.1e); "
                  "sign changes %d; amount spread committed %.1e, uncommitted %.1e"
                  % (name, g, i, kind, a["maxchange"], a["v"], a["vspread"], a["sign_changes"], a["spread_c"], a["spread_u"]), flush=True)
        fps = np.array([a["fp"] for a in rs])
        fp_spread = float(np.max(np.ptp(fps, axis=0)))
        print("%s g %+.1f: fingerprint spread across runs %.1e" % (name, g, fp_spread), flush=True)
        results[(name, g)] = (rs, fp_spread)

    rsF, fpF = results[("Fourier", 0.9)]
    l1 = all(a["steady"] and a["sign_changes"] == 0 and a["spread_c"] < 1e-8 and a["spread_u"] < 1e-8 for a in rsF) and fpF < 1e-8
    l2 = sum(not a["steady"] for a in results[("Grover", -0.9)][0]) >= 5
    l3 = sum(not a["steady"] for a in results[("Fourier", -0.9)][0]) >= 5
    l4 = all(a["steady"] and abs(a["v"]) < 1e-4 for a in results[("Grover", 0.9)][0])
    print("\nExpected results:")
    for name, ok in (("L1 Fourier g +0.9: steady, uniform, one state and its mirror", l1),
                     ("L2 Grover g -0.9: at least 5 of 10 not steady", l2),
                     ("L3 Fourier g -0.9: at least 5 of 10 not steady", l3),
                     ("L4 Grover g +0.9: steady at zero flow", l4)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", name))
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
