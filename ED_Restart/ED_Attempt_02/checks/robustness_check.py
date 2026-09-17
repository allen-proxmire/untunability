"""Robustness of the hand under the confirmed exit rule (RD10; coin fixed: plain Fourier, D7; results conditional on the coin).

Rule as in basin_check.py (coin-and-shift walk, transfer meetings at committed loci carrying lane amplitude into Internal, draw
rates following the local displacement), with each setting varied one at a time from the current values:
  ring size L          12, 24*, 36
  meeting spacing D    2*, 3
  draw strength Gamma  0.1, 0.3*, 0.6
  feedback amplitude g 0.3, 0.6, 0.9*
  feedback form        smooth tanh*, clipped straight line (clip(u, -1, 1))
(* current value). Draw rates: Gamma (1 - g s) on Right lanes and Gamma (1 + g s) on Left lanes, s = form(v_x / V0).
Steepness is set so the loop gain g |chi| / V0 is 3 or 10 at every setting, with chi from the steady state at rate differences
+-1e-3 on that setting's own L, D and Gamma. Seven starts as in basin_check.py, built for each ring size by the same
recipe (at L 24 they are identical to basin_check.py's). Steps: 4,000 x max(1, L / 24) x max(1, 0.3 / Gamma), then 500 watched.

Kinds (thresholds fixed before running): dead (largest |v| watched below 1e-3); unsteady (largest change per step over the last
200 steps at least 1e-8); hand (steady, and unchanged by a shift of D loci to 1e-8, so uniform at the meeting spacing); patterned
(steady, not shift-invariant). Hands report v and the winding of the lossy step at the final rates.

Exit rule (RD10, confirmed before running): a hand is 'found' at a value if it forms from at least 4 of the 7 starts at loop gain 3
or at loop gain 10. The discrete handedness line ends if (a) for any one setting it is found at the current value and at no other
tested value, or (b) it is not found at L 36.

Expected results, written down before the first run (2026-09-14):
  R0 harness: chi at L 8 with the current D and Gamma equals 0.16515 to 1e-5 (reproduces C42); at the current values, hands from
     7 of 7 starts at both gains, |v| within 1e-3 of 0.24271 (gain 3) and 0.24288 (gain 10) (chi now comes from L 24, so the
     steepness differs slightly from C58's).
  R1 found at L 12, 24 and 36.
  R2 found at D 2 and 3.
  R3 found at Gamma 0.1, 0.3 and 0.6.
  R4 found at g 0.3, 0.6 and 0.9.
  R5 found with both forms.
  R6 every hand has winding 1.
  Exit: the line does not end.
Exit code: 0 if it completes (the exit-rule verdict is printed, not returned).

Change before the first run (after a smoke test, no robustness results seen): chi was first taken at L 12 for every setting, but
the smoke test gave 0.16915 at L 12 against 0.16515 at L 8, so chi depends on the ring size; it is now taken on each setting's own
ring, and R0 was adjusted to match.
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
from rule_v4 import kraus, lane_channels  # noqa: E402

C = fp.FOURIER
BASE = {"L": 24, "D": 2, "Gamma": 0.3, "g": 0.9, "form": "tanh"}
VALUES = {"L": (12, 24, 36), "D": (2, 3), "Gamma": (0.1, 0.3, 0.6), "g": (0.3, 0.6, 0.9), "form": ("tanh", "clip")}
GAINS = (3.0, 10.0)
NSTART, WATCH, HIST, L_CHI = 7, 500, 200, 12
START_NAMES = ("near-uniform", "staggered", "wave pi/2", "wave 2pi/3", "random pure 1", "random pure 2", "random mixed")


def configs():
    out = [dict(BASE)]
    for key, vals in VALUES.items():
        for val in vals:
            if val != BASE[key]:
                c = dict(BASE)
                c[key] = val
                out.append(c)
    return out


def ckey(c):
    return (c["L"], c["D"], c["Gamma"], c["g"], c["form"])


def start(L, k):
    rng = np.random.default_rng(1357)
    psi = 1 + 0.1 * (rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)) / math.sqrt(2)
    psi /= np.linalg.norm(psi)
    base = np.outer(psi, psi.conj())
    x = np.repeat(np.arange(L), 3)
    if k == 0:
        return base
    if k in (1, 2, 3):
        ph = np.exp(1j * (np.pi, np.pi / 2, 2 * np.pi / 3)[k - 1] * x)
        return ph[:, None] * base * ph.conj()[None, :]
    if k in (4, 5):
        rng = np.random.default_rng((97531, 86420)[k - 4])
        v = rng.standard_normal(3 * L) + 1j * rng.standard_normal(3 * L)
        v /= np.linalg.norm(v)
        return np.outer(v, v.conj())
    rng = np.random.default_rng(75319)
    A = rng.standard_normal((3 * L, 3 * L)) + 1j * rng.standard_normal((3 * L, 3 * L))
    rho = A @ A.conj().T
    return rho / np.trace(rho).real


def rates(L, D, Gam, g, s):
    return np.concatenate([Gam * (1 - g * s), Gam * (1 + g * s)])


def step(rho, W, Cf, lane, dest, c, V0):
    L, D = c["L"], c["D"]
    x = np.arange(0, L, D)
    r = Cf @ rho @ Cf.conj().T
    dd = np.real(np.diag(r)).reshape(L, 3)
    nn = np.real(np.diag(rho)).reshape(L, 3).sum(axis=1)
    u = (dd[x, fp.RI] - dd[x, fp.LE]) / np.maximum(nn[x], 1e-300) / V0
    s = np.tanh(u) if c["form"] == "tanh" else np.clip(u, -1.0, 1.0)
    return kraus(W @ rho @ W.conj().T, lane, dest, rates(L, D, c["Gamma"], c["g"], s)), s


def chi_for(L, D, Gam):
    n = 3 * L
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    half = len(lane) // 2
    vals = []
    for delta in (1e-3, -1e-3):
        p = np.concatenate([np.full(half, Gam * (1 - delta)), np.full(half, Gam * (1 + delta))])
        rho = np.eye(n, dtype=complex) / n
        for _ in range(int(20000 * max(1.0, 0.3 / Gam))):
            new = kraus(W @ rho @ W.conj().T, lane, dest, p)
            if np.max(np.abs(new - rho)) < 1e-14:
                rho = new
                break
            rho = new
        vals.append(fp.displacement(rho, Cf, L))
    return (vals[0] - vals[1]) / 2e-3


def winding(W, c, s):
    L, D = c["L"], c["D"]
    n = 3 * L
    lane, dest = lane_channels(L, D)
    half = len(lane) // 2
    p = rates(L, D, c["Gamma"], c["g"], s)
    scale = np.ones(n)
    scale[lane[:half]] = np.sqrt(1 - p[:half])
    scale[lane[half:]] = np.sqrt(1 - p[half:])
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


def shift_perm(L, t):
    idx = np.zeros(3 * L, dtype=int)
    for u in range(L):
        for ch in range(3):
            idx[3 * ((u + t) % L) + ch] = 3 * u + ch
    return idx


def work(job):
    if job[0] == "chi":
        return job, chi_for(job[1], job[2], job[3])
    _, c, chi, gain, k = job
    L, D = c["L"], c["D"]
    W, Cf = fp.walk_matrix(L, C), fp.coin_full(L, C)
    lane, dest = lane_channels(L, D)
    V0 = c["g"] * abs(chi) / gain
    steps = int(4000 * max(1.0, L / 24) * max(1.0, 0.3 / c["Gamma"]))
    rho = start(L, k)
    for _ in range(steps):
        rho, s = step(rho, W, Cf, lane, dest, c, V0)
    vmax, change = 0.0, 0.0
    for t in range(WATCH):
        new, s = step(rho, W, Cf, lane, dest, c, V0)
        if t >= WATCH - HIST:
            change = max(change, float(np.max(np.abs(new - rho))))
        rho = new
        vmax = max(vmax, abs(fp.displacement(rho, Cf, L)))
    v = fp.displacement(rho, Cf, L)
    idx = shift_perm(L, D)
    shift_err = float(np.max(np.abs(rho[np.ix_(idx, idx)] - rho)))
    if vmax < 1e-3:
        kind = "dead"
    elif change >= 1e-8:
        kind = "unsteady"
    elif shift_err < 1e-8:
        kind = "hand"
    else:
        kind = "patterned"
    out = {"kind": kind, "v": v, "change": change, "shift_err": shift_err}
    if kind == "hand":
        out["winding"] = winding(W, c, s)
    return ("run", ckey(c), gain, k), out


def main():
    cs = configs()
    chis_needed = sorted({(c["L"], c["D"], c["Gamma"]) for c in cs} | {(8, 2, 0.3)})
    with Pool(7) as pool:
        chi = {job[1:]: val for job, val in pool.map(work, [("chi",) + t for t in chis_needed])}
        for (L, D, G), val in sorted(chi.items()):
            print("chi at L %d, D %d, Gamma %.1f: %+.5e" % (L, D, G, val), flush=True)
        jobs = [("run", c, chi[(c["L"], c["D"], c["Gamma"])], gain, k) for c in cs for gain in GAINS for k in range(NSTART)]
        jobs.sort(key=lambda j: -j[1]["L"] / j[1]["Gamma"])
        res = {}
        for key, out in pool.imap_unordered(work, jobs):
            res[key[1:]] = out
            print("done L %d D %d Gamma %.1f g %.1f %s gain %.0f %s: %s" % (key[1] + (key[2], START_NAMES[key[3]], out["kind"])), flush=True)

    letter = {"hand": "H", "dead": "D", "patterned": "P", "unsteady": "U"}
    found, windings_ok = {}, True
    print("\nBy setting (starts in order: %s; H hand, D dead, P patterned, U unsteady):" % ", ".join(START_NAMES))
    for c in cs:
        k = ckey(c)
        nh = {}
        for gain in GAINS:
            rs = [res[(k, gain, i)] for i in range(NSTART)]
            hands = [a for a in rs if a["kind"] == "hand"]
            nh[gain] = len(hands)
            if any(a["winding"] != 1 for a in hands):
                windings_ok = False
            print("L %d D %d Gamma %.1f g %.1f %-5s gain %4.1f: %s  hands %d; v %s; windings %s; largest change %.0e; largest shift error %.0e"
                  % (k + (gain, "".join(letter[a["kind"]] for a in rs), len(hands), " ".join("%+.5e" % a["v"] for a in hands),
                     [a["winding"] for a in hands], max(a["change"] for a in rs), max(a["shift_err"] for a in rs))), flush=True)
        found[k] = any(nh[g] >= 4 for g in GAINS)

    def found_at(key, val):
        c = dict(BASE)
        c[key] = val
        return found[ckey(c)]

    base_rs3 = [res[(ckey(BASE), 3.0, i)] for i in range(NSTART)]
    base_rs10 = [res[(ckey(BASE), 10.0, i)] for i in range(NSTART)]
    r0 = (abs(chi[(8, 2, 0.3)] - 0.16515) < 1e-5
          and all(a["kind"] == "hand" and abs(abs(a["v"]) - 0.24271) < 1e-3 for a in base_rs3)
          and all(a["kind"] == "hand" and abs(abs(a["v"]) - 0.24288) < 1e-3 for a in base_rs10))
    print("\nFound (hand from at least 4 of 7 starts at gain 3 or 10):")
    for key, vals in VALUES.items():
        print("  %-6s %s" % (key, "  ".join("%s: %s" % (val, "found" if found_at(key, val) else "NOT found") for val in vals)))
    rule_a = [key for key, vals in VALUES.items()
              if found_at(key, BASE[key]) and not any(found_at(key, val) for val in vals if val != BASE[key])]
    rule_b = not found_at("L", 36)
    print("\nExit rule (RD10): (a) settings where the hand is found only at the current value: %s; (b) not found at L 36: %s"
          % (rule_a if rule_a else "none", rule_b))
    print("VERDICT: %s" % ("the discrete handedness line ENDS" if (rule_a or rule_b) else "the discrete handedness line does not end"))

    print("\nExpected results:")
    for label, ok in (("R0 harness: chi and the current values reproduce C58", r0),
                      ("R1 found at L 12, 24, 36", all(found_at("L", v) for v in VALUES["L"])),
                      ("R2 found at D 2, 3", all(found_at("D", v) for v in VALUES["D"])),
                      ("R3 found at Gamma 0.1, 0.3, 0.6", all(found_at("Gamma", v) for v in VALUES["Gamma"])),
                      ("R4 found at g 0.3, 0.6, 0.9", all(found_at("g", v) for v in VALUES["g"])),
                      ("R5 found with both forms", all(found_at("form", v) for v in VALUES["form"])),
                      ("R6 every hand has winding 1", windings_ok),
                      ("Exit: the line does not end", not (rule_a or rule_b))):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
