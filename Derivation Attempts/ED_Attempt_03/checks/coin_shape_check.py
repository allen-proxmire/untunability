"""ED bootstrap, part 2: checks of note 3's paper picture (RD4; expected results E1-E5 written in ED_Bootstrap_Coins.md before
any computation, copied here unchanged).

Channels in order Internal (0), Left (1), Right (2). A coin C is a 3 x 3 unitary; its odds table is P = |C|^2 (entrywise).
Mirror symmetry: C commutes with the Left-Right swap. Mirror-symmetric odds tables have x = P[I, L] and y = P[L, L].
Chain-link test (C14): for each pair of rows i, j the lengths sqrt(P[i, k] P[j, k]), k = 0, 1, 2, form a triangle; the slack of a
pair is (sum of the two shorter lengths) - (longest), and a table passes if every slack is >= -1e-12.
Fair family (A2-ledger C55): A(phi) = diag(1, e^{i phi/2}, e^{i phi/2}) F, B(phi) = diag(1, e^{i phi/2}, e^{i phi/2}) F*,
F_jk = omega^{jk} / sqrt 3. Equivalence (A2): overall phase, conjugation by channel phases, momentum gauge
C -> diag(1, e^{-ik}, e^{ik}) C with k = 2 pi m / 24.

Expected results, as written in note 3 before any computation (2026-09-15):
  E1 20,000 random mirror-symmetric unitary coins: every odds table passes both chain-link conditions and lies in the four-sided
     slice; none falls outside; samples come within 0.01 of the chain-link boundary.
  E2 Grover's odds (4/9, 1/9): both link conditions hold with equality, to 1e-12.
  E3 The fair point (1/3, 1/3): its link triangles are equilateral and the angles closing them are 120 degrees, to 1e-12.
  E4 C = I + beta J, beta = e^{+-i150 deg} / sqrt 3: unitary, fair and mirror-symmetric to 1e-12; equivalent (overall phase,
     channel phases, ring momentum gauge) to the fair family at phi = 120 degrees or its conjugate.
  E5 The channels-alike line: coins exist for exactly x <= 4/9.
Exit code: 0 if it completes.
"""
import sys

import numpy as np

I, LE, RI = 0, 1, 2
OMEGA = np.exp(2j * np.pi / 3)
F = np.array([[OMEGA ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)
SWAP = np.eye(3)[[I, RI, LE]]
J = np.ones((3, 3))


def slacks(P):
    out = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        L = np.sort(np.sqrt(np.clip(P[i] * P[j], 0, None)))
        out.append(L[0] + L[1] - L[2])
    return np.array(out)


def in_slice(x, y, tol=1e-12):
    return -tol <= x <= 0.5 + tol and -tol <= y <= 1 - x + tol


def random_mirror_coin(rng):
    Bm = np.array([[1, 0, 0], [0, 1 / np.sqrt(2), 1 / np.sqrt(2)], [0, 1 / np.sqrt(2), -1 / np.sqrt(2)]]).T
    Z = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    Q, R = np.linalg.qr(Z)
    U2 = Q * (np.diag(R) / np.abs(np.diag(R)))
    blk = np.zeros((3, 3), dtype=complex)
    blk[:2, :2] = U2
    blk[2, 2] = np.exp(2j * np.pi * rng.random())
    return Bm @ blk @ Bm.conj().T


def family(name, phi_deg):
    d = np.ones(3, dtype=complex)
    d[LE] = d[RI] = np.exp(1j * np.radians(phi_deg) / 2)
    return np.diag(d) @ (F if name == "A" else F.conj())


def equivalent(C, T, tol=1e-9):
    for m in range(24):
        k = 2 * np.pi * m / 24
        Tm = np.diag([1, np.exp(-1j * k), np.exp(1j * k)]) @ T
        M = C / Tm
        th = M[0, 0]
        N = M / th
        if np.max(np.abs(np.abs(M) - 1)) > tol:
            return None
        if np.max(np.abs(np.diag(N) - 1)) > tol:
            continue
        if all(abs(N[j, kk] - N[j, 0] * N[0, kk]) < tol for j in range(3) for kk in range(3)):
            return m
    return None


def main():
    rng = np.random.default_rng(3141)
    worst_unit = worst_mirror = worst_bist = 0.0
    fails_link = fails_slice = 0
    min_slack = np.inf
    for _ in range(20000):
        C = random_mirror_coin(rng)
        worst_unit = max(worst_unit, float(np.max(np.abs(C.conj().T @ C - np.eye(3)))))
        worst_mirror = max(worst_mirror, float(np.max(np.abs(SWAP @ C @ SWAP - C))))
        P = np.abs(C) ** 2
        worst_bist = max(worst_bist, float(np.max(np.abs(P.sum(0) - 1))), float(np.max(np.abs(P.sum(1) - 1))))
        s = slacks(P)
        fails_link += int(np.min(s) < -1e-12)
        x, y = P[I, LE], P[LE, LE]
        fails_slice += int(not in_slice(x, y))
        min_slack = min(min_slack, float(np.min(s)))
    e1 = fails_link == 0 and fails_slice == 0 and min_slack < 0.01
    print("E1 20,000 random mirror-symmetric coins: unitarity %.1e, mirror %.1e, row/column sums %.1e; chain-link failures %d; outside slice %d; smallest slack %.2e"
          % (worst_unit, worst_mirror, worst_bist, fails_link, fails_slice, min_slack), flush=True)

    G = (2 / 3) * J - np.eye(3)
    PG = np.abs(G) ** 2
    sG = slacks(PG)
    e2 = abs(PG[I, LE] - 4 / 9) < 1e-12 and abs(PG[LE, LE] - 1 / 9) < 1e-12 and np.max(np.abs(sG)) < 1e-12
    print("E2 Grover odds (x, y) = (%.12f, %.12f); link slacks %s" % (PG[I, LE], PG[LE, LE], " ".join("%.1e" % v for v in sG)), flush=True)

    PF = np.abs(F) ** 2
    e3 = True
    for i, j in ((0, 1), (0, 2), (1, 2)):
        terms = F[i] * F[j].conj()
        lengths = np.abs(terms)
        angles = sorted(np.degrees(np.angle(terms[(q + 1) % 3] / terms[q])) % 360 for q in range(3))
        ok = np.max(np.abs(lengths - 1 / 3)) < 1e-12 and abs(np.sum(terms)) < 1e-12 and all(min(abs(a - 120), abs(a - 240)) < 1e-9 for a in angles)
        e3 = e3 and ok
        print("E3 fair rows %d,%d: lengths %s, sum of terms %.1e, turning angles %s" % (i, j, " ".join("%.12f" % v for v in lengths), abs(np.sum(terms)),
                                                                                   " ".join("%.9f" % a for a in angles)), flush=True)
    e3 = e3 and np.max(np.abs(PF - 1 / 3)) < 1e-12

    e4 = True
    for sign in (+1, -1):
        beta = np.exp(sign * 1j * np.radians(150)) / np.sqrt(3)
        C = np.eye(3) + beta * J
        unit = float(np.max(np.abs(C.conj().T @ C - np.eye(3))))
        fair = float(np.max(np.abs(np.abs(C) ** 2 - 1 / 3)))
        mirror = float(np.max(np.abs(SWAP @ C @ SWAP - C)))
        ratio = C[I, I] ** 2 / (C[LE, LE] * C[RI, RI])
        matches = []
        for name in ("A", "B"):
            for phi in range(360):
                m = equivalent(C, family(name, phi))
                if m is not None:
                    matches.append((name, phi, m))
        ok = unit < 1e-12 and fair < 1e-12 and mirror < 1e-12 and any(mt[1] in (120, 240) for mt in matches)
        e4 = e4 and ok
        print("E4 beta sign %+d: unitarity %.1e, fairness %.1e, mirror %.1e; C_II^2/(C_LL C_RR) = %.6f%+.6fi; equivalent to (family, phi, momentum m): %s"
              % (sign, unit, fair, mirror, ratio.real, ratio.imag, matches), flush=True)

    xs = np.linspace(0, 0.5, 2001)
    ok_link = np.array([np.min(slacks(np.array([[1 - 2 * x, x, x], [x, 1 - 2 * x, x], [x, x, 1 - 2 * x]]))) >= -1e-12 for x in xs])
    thetas = np.linspace(0, np.pi, 20001)
    reach = (2 - 2 * np.cos(thetas)) / 9
    e5 = bool(np.all(ok_link[xs <= 4 / 9 + 1e-12]) and not np.any(ok_link[xs > 4 / 9 + 1e-9]) and abs(reach.max() - 4 / 9) < 1e-12)
    print("E5 channels-alike line: chain-link passes for x up to %.6f; channels-alike coins I + (e^{i theta} - 1) J/3 reach x from %.3f to %.12f"
          % (xs[ok_link].max(), reach.min(), reach.max()), flush=True)

    print("\nExpected results:")
    for label, ok in (("E1 random mirror-symmetric coins fill the chain-link region only", e1), ("E2 Grover on the boundary", e2),
                      ("E3 fair point: equilateral triangles, 120 degrees", e3), ("E4 fair channels-alike coins at phi 120 or conjugate", e4),
                      ("E5 channels-alike coins exist exactly for x <= 4/9", e5)):
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
