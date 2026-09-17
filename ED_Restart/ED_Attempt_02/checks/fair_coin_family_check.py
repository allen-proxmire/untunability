"""The fair-coin family: do all phase-dressed equivalents of the Fourier coin hold the hand? (RD8; follows C52-C54)

A fair three-channel coin (unitary, every entry of size 1/sqrt 3) is D1 P1 F P2 D2 for diagonal phases D and permutations P
(Haagerup, C53). Not all of these act alike in ED's walk. What doesn't change the physics:
  a global phase;
  conjugating the coin by site-independent channel phases Q (C -> Q C Q^dagger; the shift, the transfer meetings and the
    feedback's readout are unchanged, since they only see phases through |amplitude|^2 or as overall phases of Kraus operators);
  a momentum gauge on the ring: C -> diag(1, e^{-ik}, e^{ik}) C with k a multiple of 2 pi / L.
Algebra (checked in Q1): every fair coin reduces under the first two to diag(1, e^{ia}, e^{ib}) F or diag(1, e^{ia}, e^{ib}) F*,
and by the momentum gauge only a + b matters, up to a flux a - b modulo 2 pi / L. The space mirror maps (a, b) to (b, a), so the
coins with a = b are exactly mirror-symmetric. Complex conjugation of the whole dynamics maps the F* family at phase phi = a + b
to the F family at -phi.

Coins run (Left phase a, Right phase b; phi = a + b):
  family A: diag(1, e^{i phi/2}, e^{i phi/2}) F for phi = 0, 30, ..., 330 degrees (12 coins, mirror-symmetric);
  family B: diag(1, e^{i phi/2}, e^{i phi/2}) F* for phi = 0, 90, 120, 210 degrees (4 coins, mirror-symmetric);
  controls: family A at phi = 0 and 120 degrees with a - b = 7.5 degrees (half the ring's flux quantum; not mirror-symmetric).
Rule and settings as steepness_range_check.py (L 24, transfer meetings at every 2nd locus, Gamma 0.3), with one common
steepness V0 = 0.9 x 0.16515 / 3 for every coin (the Fourier coin's gain-3 value), both feedback signs g = +0.9 and -0.9,
starts 0-2, 4,000 steps then 500 watched. Kinds as in steepness_range_check.py (dead, hand, patterned, unsteady). For each coin
the response chi (from the L 8 steady state at rate differences +-1e-3) and the loop gain 0.9 |chi| / V0 are reported.
A coin 'holds a hand' if, for at least one sign, all 3 starts are hands.

Expected results, written down before the first run (2026-09-14):
  Q1 200 of 200 random fully-dressed fair coins reduce to diag(phases) F or diag(phases) F* under a global phase and channel-phase
     conjugation (the elementwise ratio to F or F* has rank 1 to 1e-10).
  Q2 family A at phi = 0 (the undressed Fourier coin) reproduces C45: hands for g = +0.9 with |v| = 0.24271 (to 1e-5).
  Q3 fairness alone is not enough: at least one of the 16 mirror-symmetric coins does not hold a hand.
  Q4 family B at phi gives the same kinds as family A at -phi for each sign (compared as sets over the 3 starts, since the
     starts are not conjugated), and the same |v| for hands (to 1e-6).
  Q5 in the two controls, wherever all 3 starts are hands, all 3 go the same way.
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
from discrete_hand_test import D, iterate_steady, step, winding_at  # noqa: E402
from lasting_states_check import L, starts  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402

STEPS, WATCH, HIST, NSTART = 4000, 500, 200, 3
V0 = 0.9 * 1.6515e-01 / 3
F = fp.FOURIER
P12 = np.eye(3)[[fp.I, fp.RI, fp.LE]]
COINS = ([("A", phi, 0.0) for phi in range(0, 360, 30)] + [("B", phi, 0.0) for phi in (0, 90, 120, 210)]
         + [("A", 0, 7.5), ("A", 120, 7.5)])


def coin(key):
    fam, phi, asym = key
    a, b = np.radians(phi / 2 + asym / 2), np.radians(phi / 2 - asym / 2)
    ph = np.ones(3, dtype=complex)
    ph[fp.LE], ph[fp.RI] = np.exp(1j * a), np.exp(1j * b)
    return np.diag(ph) @ (F if fam == "A" else F.conj())


def reduces(C):
    best = np.inf
    for B in (F, F.conj()):
        sv = np.linalg.svd(C / B, compute_uv=False)
        best = min(best, sv[1] / sv[0])
    return best


def work(job):
    if job[0] == "chi":
        C = coin(job[1])
        return job, (iterate_steady(C, 1e-3) - iterate_steady(C, -1e-3)) / 2e-3
    _, key, g, i = job
    C = coin(key)
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
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
    if vmax < 1e-3:
        kind = "dead"
    elif change >= 1e-8:
        kind = "unsteady"
    elif uniform:
        kind = "hand"
    else:
        kind = "patterned"
    out = {"kind": kind, "v": v, "vmax": vmax, "change": change}
    if kind == "hand":
        out["winding"] = winding_at(W, L, s, g)
    return job, out


def mirror_error(C):
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    mi = fp.mirror_perm(L)
    r0 = starts()[0]
    a1, _ = step(r0, W, Cf, lane, dest, L, 0.9, V0)
    a2, _ = step(r0[np.ix_(mi, mi)], W, Cf, lane, dest, L, 0.9, V0)
    return float(np.max(np.abs(a1[np.ix_(mi, mi)] - a2)))


def main():
    rng = np.random.default_rng(2468)
    worst = 0.0
    for _ in range(200):
        P1, P2 = np.eye(3)[rng.permutation(3)], np.eye(3)[rng.permutation(3)]
        D1, D2 = np.diag(np.exp(2j * np.pi * rng.random(3))), np.diag(np.exp(2j * np.pi * rng.random(3)))
        worst = max(worst, reduces(D1 @ P1 @ F @ P2 @ D2))
    q1 = worst < 1e-10
    print("Q1 worst second-to-first singular value ratio over 200 random fair coins: %.1e" % worst, flush=True)

    mirror = {key: mirror_error(coin(key)) for key in COINS}
    jobs = [("chi", key) for key in COINS] + [("run", key, g, i) for key in COINS for g in (0.9, -0.9) for i in range(NSTART)]
    res = {}
    with Pool(7) as pool:
        for job, out in pool.imap_unordered(work, jobs):
            res[job] = out
            if job[0] == "run":
                print("done %s phi %3d asym %.1f g %+.1f start %d: %s" % (job[1] + (job[2], job[3], out["kind"])), flush=True)

    print("\nBy coin:")
    holds = {}
    for key in COINS:
        chi = res[("chi", key)]
        line = "%s phi %3d asym %.1f: mirror one step %.1e, chi %+.4e, loop gain %.2f" % (key + (mirror[key], chi, 0.9 * abs(chi) / V0))
        holds[key] = False
        for g in (0.9, -0.9):
            rs = [res[("run", key, g, i)] for i in range(NSTART)]
            if all(a["kind"] == "hand" for a in rs):
                holds[key] = True
            line += "; g %+.1f: %s v %s windings %s" % (g, [a["kind"] for a in rs], " ".join("%+.5e" % a["v"] for a in rs),
                                                        [a.get("winding") for a in rs])
        print(line, flush=True)

    r = res[("run", ("A", 0, 0.0), 0.9, 0)]
    q2 = all(res[("run", ("A", 0, 0.0), 0.9, i)]["kind"] == "hand" and abs(abs(res[("run", ("A", 0, 0.0), 0.9, i)]["v"]) - 0.24271) < 1e-5
             for i in range(NSTART))
    symmetric = [key for key in COINS if key[2] == 0.0]
    q3 = not all(holds[key] for key in symmetric)
    q4 = True
    for phi in (0, 90, 120, 210):
        for g in (0.9, -0.9):
            bs = [res[("run", ("B", phi, 0.0), g, i)] for i in range(NSTART)]
            as_ = [res[("run", ("A", (-phi) % 360, 0.0), g, i)] for i in range(NSTART)]
            if sorted(x["kind"] for x in bs) != sorted(x["kind"] for x in as_):
                q4 = False
            hb = sorted(abs(x["v"]) for x in bs if x["kind"] == "hand")
            ha = sorted(abs(x["v"]) for x in as_ if x["kind"] == "hand")
            if len(hb) == len(ha) and any(abs(p - q) > 1e-6 for p, q in zip(hb, ha)):
                q4 = False
    q5 = True
    for key in (("A", 0, 7.5), ("A", 120, 7.5)):
        for g in (0.9, -0.9):
            rs = [res[("run", key, g, i)] for i in range(NSTART)]
            if all(a["kind"] == "hand" for a in rs) and len({np.sign(a["v"]) for a in rs}) > 1:
                q5 = False
    print("\nMirror-symmetric coins holding a hand: %d of %d (%s)"
          % (sum(holds[k] for k in symmetric), len(symmetric), ", ".join("%s%d" % (k[0], k[1]) for k in symmetric if holds[k])))
    print("\nExpected results:")
    for label, ok in (("Q1 every fair coin reduces to phases times F or F*", q1),
                      ("Q2 undressed Fourier coin reproduces C45", q2),
                      ("Q3 at least one mirror-symmetric fair coin holds no hand", q3),
                      ("Q4 family B at phi matches family A at -phi", q4),
                      ("Q5 controls: hands all go the same way", q5)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
