"""Moving committed matter that gives back its motion: model (ii), under its exit rule (RD14, RD15; rules M1-M5 in
Moving_Committed_Matter.md, written before this code; coin plain Fourier, D7).

State: walker rho (3L x 3L); committed amount c_x and momentum P_x at every locus. One step:
  1. rho <- W rho W^dagger (fair coin, then shift).
  2. n_R, n_L: lane populations at each locus.
  3. u_x = clip(P_x / c_x, -1, 1) (0 where c_x <= 1e-12); mu_R = lam (c_x / m0)(1 - u_x), mu_L = lam (c_x / m0)(1 + u_x);
     p = P3(mu), P3(mu) = 1 - e^{-mu} (1 + mu + mu^2 / 2), P3(lam) = Gamma.                                            (M2)
  4. Lane channels scaled by sqrt(1 - p); caught amount p n released: share 1 - |u_x| into Internal at x, share |u_x| into
     Right at x + 1 (u_x > 0) or Left at x - 1 (u_x < 0).                                                               (M3)
  5. P_x += (p_R n_R - p_L n_L) - u_x (p_R n_R + p_L n_L).                                                              (M4)
  6. Share |u_x| of c_x and of P_x moves one locus in the direction of u_x (u_x from step 3).                          (M5)
Start: c_x = m0 at even loci, 0 at odd; P = 0; walker starts as in robustness_check.py.
Steps: 4,000 x max(1, L / 24) x max(1, 0.3 / Gamma) x m0, then 500 watched.

Kinds: dead (largest |v| watched below 1e-3, v the coin-output displacement as before); unsteady (over the last 200 steps the
largest change per step of rho, P or c is at least 1e-8); hand (steady, and rho, c and P unchanged by a shift of 2 loci to 1e-8);
patterned (steady, not shift-invariant). Hands report v, the released current (sum of caught amount times u), and the winding of
the lossy step at the final catch probabilities.

Exit rule (RD14, confirmed RD15): 'found' on a ring means a hand with winding 1 from at least 4 of the 7 starts at Gamma 0.3 or
0.05, with m0 = 1. The line ends, recorded as 'moving matter doesn't make a hand either', if (a) not found on ring 24, or (b) found
on ring 24 but not on ring 36. The m0 = 10 runs (ring 24) are a reported check, not part of the verdict.

Harness: `python moving_matter_check.py --h0` runs only M0.

Expected results, written down before the first run (2026-09-15):
  M0 harness: with carrying (M3's moved share, M4's give-back term) and moving (M5) switched off, the model reproduces note 7's
     derived law step for step for 50 steps from start 0 at Gamma 0.3, to 1e-12.
  M1 ring 24, m0 1: no hand from any start at either Gamma. (Reasoning, C76: carrying back motion halves the old route's strength,
     and the released current feeds the lane imbalance only weakly, since the fair coin spreads released stuff evenly on the next
     step; the loop gain stays below 1.)
  M2 ring 36, m0 1: no hand from any start at either Gamma.
  M3 ring 24, m0 10: no hand from any start at either Gamma.
  Exit: the line ends ('moving matter doesn't make a hand either').
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
from threshold_law_check import P3, lam_for  # noqa: E402

WATCH, HIST = 500, 200
SETTINGS = [(24, 1.0), (36, 1.0), (24, 10.0)]
GAMMAS = (0.3, 0.05)


class Model:
    def __init__(self, L, gam, m0, carry=True, move=True):
        self.L, self.m0, self.carry, self.move = L, m0, carry, move
        self.lam = lam_for(gam)
        self.W, self.Cf = fp.walk_matrix(L, rc.C), fp.coin_full(L, rc.C)
        self.lane, _ = lane_channels(L, 1)
        xs = np.arange(L)
        assert np.array_equal(self.lane[:L], 3 * xs + fp.RI) and np.array_equal(self.lane[L:], 3 * xs + fp.LE)
        self.c = np.where(xs % 2 == 0, m0, 0.0)
        self.P = np.zeros(L)

    def velocity(self):
        u = np.zeros(self.L)
        ok = self.c > 1e-12
        u[ok] = self.P[ok] / self.c[ok]
        return np.clip(u, -1.0, 1.0)

    def step(self, rho):
        L = self.L
        xs = np.arange(L)
        w = self.W @ rho @ self.W.conj().T
        d = np.real(np.diag(w))
        nR, nL = d[3 * xs + fp.RI], d[3 * xs + fp.LE]
        u = self.velocity()
        dens = self.c / self.m0
        pR, pL = P3(self.lam * dens * (1 - u)), P3(self.lam * dens * (1 + u))
        p = np.concatenate([pR, pL])
        n = 3 * L
        scale = np.ones(n)
        scale[self.lane] = np.sqrt(1 - p)
        out = scale[:, None] * w * scale[None, :]
        caught = pR * nR + pL * nL
        share = np.abs(u) if self.carry else np.zeros(L)
        add = np.zeros(n)
        np.add.at(add, 3 * xs + fp.I, (1 - share) * caught)
        right = u > 0
        np.add.at(add, 3 * ((xs[right] + 1) % L) + fp.RI, share[right] * caught[right])
        left = u < 0
        np.add.at(add, 3 * ((xs[left] - 1) % L) + fp.LE, share[left] * caught[left])
        out[np.diag_indices(n)] += add
        dP = (pR * nR - pL * nL) - (u * caught if self.carry else 0.0)
        P = self.P + dP
        c = self.c
        if self.move:
            f = np.abs(u)
            mc, mP = f * c, f * P
            c = c - mc
            P = P - mP
            np.add.at(c, (xs[right] + 1) % L, mc[right])
            np.add.at(P, (xs[right] + 1) % L, mP[right])
            np.add.at(c, (xs[left] - 1) % L, mc[left])
            np.add.at(P, (xs[left] - 1) % L, mP[left])
        released = float(np.sum(share * caught * np.sign(u)))
        self.c, self.P = c, P
        return out, p, released


def closed_step(rho, W, lam, P, L):
    lane, dest = lane_channels(L, 2)
    x = np.arange(0, L, 2)
    w = W @ rho @ W.conj().T
    d = np.real(np.diag(w))
    nR, nL = d[3 * x + fp.RI], d[3 * x + fp.LE]
    u = np.clip(P / 1.0, -1.0, 1.0)
    pR, pL = P3(lam * (1 - u)), P3(lam * (1 + u))
    new = kraus(w, lane, dest, np.concatenate([pR, pL]))
    return new, P + (pR * nR - pL * nL)


def h0():
    L, gam = 24, 0.3
    m = Model(L, gam, 1.0, carry=False, move=False)
    rho_a = rc.start(L, 0)
    rho_b = rho_a.copy()
    Pb = np.zeros(L // 2)
    worst = 0.0
    for _ in range(50):
        rho_a, _, _ = m.step(rho_a)
        rho_b, Pb = closed_step(rho_b, m.W, m.lam, Pb, L)
        worst = max(worst, float(np.max(np.abs(rho_a - rho_b))), float(np.max(np.abs(m.P[0::2] - Pb))), float(np.max(np.abs(m.P[1::2]))))
    return worst


def winding_lanes(W, L, lane, p):
    n = 3 * L
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
    L, m0, gam, k = job
    m = Model(L, gam, m0)
    steps = int(4000 * max(1.0, L / 24) * max(1.0, 0.3 / gam) * m0)
    rho = rc.start(L, k)
    vmax = change = 0.0
    p = None
    released = 0.0
    for t in range(steps + WATCH):
        c_old, P_old = m.c.copy(), m.P.copy()
        new, p, released = m.step(rho)
        if t >= steps:
            if t >= steps + WATCH - HIST:
                change = max(change, float(np.max(np.abs(new - rho))), float(np.max(np.abs(m.c - c_old))), float(np.max(np.abs(m.P - P_old))))
            vmax = max(vmax, abs(fp.displacement(new, m.Cf, L)))
        rho = new
    v = fp.displacement(rho, m.Cf, L)
    idx = rc.shift_perm(L, 2)
    shift_err = max(float(np.max(np.abs(rho[np.ix_(idx, idx)] - rho))), float(np.max(np.abs(np.roll(m.c, 2) - m.c))),
                    float(np.max(np.abs(np.roll(m.P, 2) - m.P))))
    if vmax < 1e-3:
        kind = "dead"
    elif change >= 1e-8:
        kind = "unsteady"
    elif shift_err < 1e-8:
        kind = "hand"
    else:
        kind = "patterned"
    out = {"kind": kind, "v": v, "vmax": vmax, "change": change, "released": released,
           "u_mean": float(np.mean(m.velocity())), "c_spread": float(np.ptp(m.c))}
    if kind == "hand":
        out["winding"] = winding_lanes(m.W, L, m.lane, p)
    return job, out


def main():
    worst = h0()
    m0ok = worst < 1e-12
    print("M0 harness: carrying and moving off vs note 7's derived law, 50 steps: largest difference %.1e" % worst, flush=True)
    if "--h0" in sys.argv:
        return 0
    jobs = [(L, m0, gam, k) for L, m0 in SETTINGS for gam in GAMMAS for k in range(rc.NSTART)]
    jobs.sort(key=lambda j: -j[0] * j[1] / j[2])
    with Pool(7) as pool:
        res = dict(pool.imap_unordered(run, jobs))
    letter = {"hand": "H", "dead": "D", "patterned": "P", "unsteady": "U"}
    print("\nStarts in order: %s; H hand, D dead, P patterned, U unsteady" % ", ".join(rc.START_NAMES))
    found, nh = {}, {}
    for L, m0 in SETTINGS:
        for gam in GAMMAS:
            rs = [res[(L, m0, gam, k)] for k in range(rc.NSTART)]
            hands = [a for a in rs if a["kind"] == "hand"]
            good = [a for a in hands if a["winding"] == 1]
            nh[(L, m0, gam)] = len(hands)
            found[(L, m0, gam)] = len(good) >= 4
            print("ring %d m0 %4.1f Gamma %.2f: %s  hands %d (winding 1: %d); v %s; windings %s; largest |v| watched %s; mean matter velocity %s; "
                  "released current %s; matter amount spread %s; largest change %.0e"
                  % (L, m0, gam, "".join(letter[a["kind"]] for a in rs), len(hands), len(good), " ".join("%+.5e" % a["v"] for a in hands),
                     [a["winding"] for a in hands], " ".join("%.1e" % a["vmax"] for a in rs), " ".join("%+.3f" % a["u_mean"] for a in rs),
                     " ".join("%+.1e" % a["released"] for a in rs), " ".join("%.1e" % a["c_spread"] for a in rs), max(a["change"] for a in rs)), flush=True)
    f24 = found[(24, 1.0, 0.3)] or found[(24, 1.0, 0.05)]
    f36 = found[(36, 1.0, 0.3)] or found[(36, 1.0, 0.05)]
    ends = (not f24) or (f24 and not f36)
    print("\nExit rule (RD14): found on ring 24: %s; found on ring 36: %s" % (f24, f36))
    print("VERDICT: %s" % ("the line ENDS: moving matter doesn't make a hand either" if ends
                            else "the line does not end: a hand is made, conditional on the fair coin and model (ii)'s assumptions"))
    print("\nExpected results:")
    for label, ok in (("M0 harness reproduces note 7's derived law", m0ok),
                      ("M1 ring 24, m0 1: no hand", nh[(24, 1.0, 0.3)] + nh[(24, 1.0, 0.05)] == 0),
                      ("M2 ring 36, m0 1: no hand", nh[(36, 1.0, 0.3)] + nh[(36, 1.0, 0.05)] == 0),
                      ("M3 ring 24, m0 10: no hand", nh[(24, 10.0, 0.3)] + nh[(24, 10.0, 0.05)] == 0),
                      ("Exit: the line ends", ends)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
