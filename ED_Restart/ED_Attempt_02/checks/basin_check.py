"""Basin check: does 'no hand' mean 'cannot hold one'? (RD9; follows C55-C57)

Coins: the 12 fair coins diag(1, e^{i phi/2}, e^{i phi/2}) F, phi = 0, 30, ..., 330 degrees (fair_coin_family_check.coin, family A),
and the Grover coin. Rule and settings as before (L 24, transfer meetings at every 2nd locus, Gamma 0.3, rate feedback on the local
displacement). The steepness is set per coin so that every coin has the same loop gain: V0 = 0.9 |chi| / gain, gain 3 and 10,
with chi from the L 8 steady state at rate differences +-1e-3. Both feedback signs g = +0.9 and -0.9.

Seven starts, the same for every coin:
  near-uniform   psi = 1 + 0.1 xi (start 0 of the earlier checks);
  staggered      (-1)^x times the near-uniform start;
  wave pi/2      e^{i pi x / 2} times the near-uniform start;
  wave 2pi/3     e^{i 2 pi x / 3} times the near-uniform start;
  random pure 1  fully random complex amplitudes (seed 97531);
  random pure 2  fully random complex amplitudes (seed 86420);
  random mixed   A A^dagger / trace, A a random complex Gaussian matrix (seed 75319).
Each run: 4,000 steps, then 500 watched. Kinds as before: dead (largest |v| watched below 1e-3), unsteady (largest change per step
over the last 200 steps at least 1e-8), hand (steady, no sign changes of the local displacement, amounts equal within each locus
type to 1e-8), patterned (steady, not uniform). Hands also report v and winding.

Expected results, written down before the first run (2026-09-14):
  B1 the plain Fourier coin (phi = 0), g = +0.9: a hand from all 7 starts at both gains.
  B2 fair coins, g = +0.9: at phi = 240 and 270 degrees no hand from any start at either gain; at each of the other 10 phases a hand
     from at least one start at one gain or more.
  B3 the Grover coin: no hand from any start, either sign, either gain.
  B4 fair coins, g = -0.9: no hands.
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
from fair_coin_family_check import coin as fair_coin  # noqa: E402
from lasting_states_check import L, starts as old_starts  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402

STEPS, WATCH, HIST = 4000, 500, 200
COINS = ["F%d" % phi for phi in range(0, 360, 30)] + ["Grover"]
GAINS = (3.0, 10.0)
SIGNS = (0.9, -0.9)
START_NAMES = ("near-uniform", "staggered", "wave pi/2", "wave 2pi/3", "random pure 1", "random pure 2", "random mixed")


def coin(name):
    return fp.GROVER if name == "Grover" else fair_coin(("A", int(name[1:]), 0.0))


def start(k):
    base = old_starts()[0]
    x = np.repeat(np.arange(L), 3)
    if k == 0:
        return base
    if k in (1, 2, 3):
        q = (np.pi, np.pi / 2, 2 * np.pi / 3)[k - 1]
        ph = np.exp(1j * q * x)
        return ph[:, None] * base * ph.conj()[None, :]
    if k in (4, 5):
        rng = np.random.default_rng((97531, 86420)[k - 4])
        psi = rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)
        psi /= np.linalg.norm(psi)
        return np.outer(psi, psi.conj())
    rng = np.random.default_rng(75319)
    A = rng.standard_normal((3 * L, 3 * L)) + 1j * rng.standard_normal((3 * L, 3 * L))
    rho = A @ A.conj().T
    return rho / np.trace(rho).real


def work(job):
    if job[0] == "chi":
        C = coin(job[1])
        return job, (iterate_steady(C, 1e-3) - iterate_steady(C, -1e-3)) / 2e-3
    _, name, chi, gain, g, k = job
    C = coin(name)
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    V0 = 0.9 * abs(chi) / gain
    rho = start(k)
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
    out = {"kind": kind, "v": v}
    if kind == "hand":
        out["winding"] = winding_at(W, L, s, g)
    return (job[0], name, gain, g, k), out


def main():
    res = {}
    with Pool(7) as pool:
        chi = dict((job[1], val) for job, val in pool.map(work, [("chi", name) for name in COINS]))
        for name in COINS:
            print("%s: chi %+.5e" % (name, chi[name]), flush=True)
        jobs = [("run", name, chi[name], gain, g, k) for name in COINS for gain in GAINS for g in SIGNS for k in range(len(START_NAMES))]
        for key, out in pool.imap_unordered(work, jobs):
            res[key[1:]] = out
            print("done %s gain %.0f g %+.1f %s: %s" % (key[1], key[2], key[3], START_NAMES[key[4]], out["kind"]), flush=True)

    print("\nBy coin (starts in order: %s; H hand, D dead, P patterned, U unsteady):" % ", ".join(START_NAMES))
    letter = {"hand": "H", "dead": "D", "patterned": "P", "unsteady": "U"}
    anyhand = {}
    for name in COINS:
        for gain in GAINS:
            for g in SIGNS:
                rs = [res[(name, gain, g, k)] for k in range(len(START_NAMES))]
                hands = [a for a in rs if a["kind"] == "hand"]
                anyhand[(name, gain, g)] = len(hands)
                print("%-6s gain %4.1f g %+.1f: %s  hands %d; v %s; windings %s"
                      % (name, gain, g, "".join(letter[a["kind"]] for a in rs), len(hands),
                         " ".join("%+.5e" % a["v"] for a in hands), [a["winding"] for a in hands]), flush=True)

    fair = [n for n in COINS if n != "Grover"]
    b1 = all(anyhand[("F0", gain, 0.9)] == len(START_NAMES) for gain in GAINS)
    holds = {n: any(anyhand[(n, gain, 0.9)] > 0 for gain in GAINS) for n in fair}
    b2 = (not holds["F240"] and not holds["F270"]) and all(holds[n] for n in fair if n not in ("F240", "F270"))
    b3 = all(anyhand[("Grover", gain, g)] == 0 for gain in GAINS for g in SIGNS)
    b4 = all(anyhand[(n, gain, -0.9)] == 0 for n in fair for gain in GAINS)
    print("\nFair coins holding a hand from some start (g +0.9): %s" % ", ".join(n for n in fair if holds[n]))
    print("\nExpected results:")
    for label, ok in (("B1 plain Fourier: hand from all 7 starts at both gains", b1),
                      ("B2 fair coins: none at 240 and 270, some at each other phase", b2),
                      ("B3 Grover: no hand anywhere", b3),
                      ("B4 fair coins, g -0.9: no hands", b4)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
