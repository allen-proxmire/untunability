"""Check C263: with local feedback, does a mirror-symmetric irreversible rule form domains of opposite hand, does one
seed take over, and does a saturated hand block an opposite seed? (RD44, G46; follows C248, C251)

Rule (a toy, not ED's full rule): one lane of complex amplitudes psi_x on a ring of L = 512 loci,
d psi / dt = -i (H psi), (H psi)_x = t_f[x-1] psi_{x-1} + t_b[x] psi_{x+1}, bond b joining loci b and b+1,
renormalized each step (the hops below don't depend on overall scale, so this only rescales). Hops on each bond come
from the local current only (no global sum, unlike C248):
  v_b = 2 Im(psi_b* psi_{b+1}) / (|psi_b|^2 + |psi_{b+1}|^2)      (between -1 and 1; e^{ikx} gives sin k)
  vbar = v smoothed by NB = 8 passes of the (1/4, 1/2, 1/4) neighbour average
  t_f[b] = 1 - g tanh(vbar_b / V0),  t_b[b] = 1 + g tanh(vbar_b / V0),  g = 0.5, V0 = 0.05.
Mirror x -> -x sends v_b -> -v_{-b-1} and swaps t_f and t_b, so the rule has no built-in hand.
Local hand of bond b: sign(t_b - t_f) where |t_b - t_f| > 0.1, else unhanded. A domain is a maximal run of
same-hand bonds around the ring, skipping unhanded bonds. RK4, dt = 0.02, hops held fixed within a step.

Linear theory (derived before freezing). About the uniform state, write psi = e^{-2it}(1 + u + i w). To first order
v_b = w_{b+1} - w_b, and for a wave of wavenumber k, with s = 4 sin^2(k/2), S = cos^(2 NB)(k/2), G = g / V0:
  du/dt = -s w,  dw/dt = s u + G S s w,
so the growth rate is lambda(k) = (G S s + Re sqrt((G S s)^2 - 4 s^2)) / 2 > 0 for every k in (0, pi): the uniform
state is linearly unstable (unlike C251, where the global current cancels at first order). lambda_max is about 1.6 at
k about 0.7 (wavelength about 9 loci), so noise should break into short domains quickly.

Runs:
  A  20 noise starts, psi = 1 + 1e-3 xi (xi complex unit Gaussian), to t = 400 (snapshot at t = 50).
  B  10 runs: noise 1e-3 plus one seed, 0.5 exp(-((x - L/2)/32)^2) e^{i 0.3 x} (hand +1 inside it), to t = 400.
  C  the seed with noise 1e-9.   D  the seed with no noise (round-off only).
  E  5 runs: a fully handed background e^{i k0 x}, k0 = 2 pi 24 / L (hand +1, saturated), plus an opposite seed
     0.5 exp(-((x - L/2)/32)^2) e^{-i 0.3 x} and noise 1e-3, to t = 400.
  G  growth check: noise 1e-12, slope of ln rms(t_b - t_f) between t = 6 and t = 12.
  M  mirror check: the mirror image of one A start, evolved to t = 5.

Known context: spontaneous choice of direction with domains and reversals in one-dimensional flocking (Czirok,
Barabasi, Vicsek 1999; O'Loan and Evans 1999; C262); nonlinear non-Hermitian nonreciprocity (C245).

Predictions frozen before the first run (2026-09-14):
  P0  G: the measured growth rate is within 30% of the linear theory's lambda_max.
  P1  M: mirror image of the evolved state matches the evolved mirror image to 1e-9, and the hands are mirrored.
  P2  An exactly uniform start stays exactly uniform with no handed bonds at t = 400.
  P3  A at t = 50: every run has at least 10 domains.
  P4  A at t = 400: at least 15 of 20 runs still have 2 or more domains (no single hand takes the ring).
  P5  A at t = 400: among all handed bonds of all runs, the share with hand +1 is between 0.4 and 0.6.
  P6  B: in at least 8 of 10 runs, the seed's hand (+1) covers under 50% of bonds at t = 400.
  P7  C: the seed's hand covers under 50% of bonds at t = 400.
  P8  D: the seed's hand covers under 90% of bonds at t = 400.
  P9  E: in at least 4 of 5 runs, the background hand (+1) covers at least 90% of bonds at t = 400.
Exit code: P1 and P2 (code properties); the rest are reported.

Changes after freezing (2026-09-14):
  1. Run 1 (handedness_local_toy_run1.txt): P0, P1, P2, P9 RIGHT; P3-P8 WRONG. Linear theory confirmed (growth 1.568
     measured against 1.623). Noise starts merge: 1-6 domains by t = 50 and one hand over the whole ring by t = 400 in
     all 20 runs (+1 in 7, -1 in 13). One seed's hand took the whole ring in all 10 noisy runs, with noise 1e-9, and with
     no noise. A saturated hand kept the whole ring against an opposite seed in all 5 runs.
  2. Claude's design errors: P3's snapshot (t = 50) came long after the instability saturates (about t = 5), so it
     measured merging, not first domains; P5 pooled bonds, but each run ends with one hand, so the effective sample is
     20 runs, and 7 of 20 is within chance (two-sided binomial p about 0.26).
  3. The exit code now checks P1, P2 and that the recorded run-1 results reproduce.
  4. Diagnostic handedness_local_diagnostic.py (not pre-registered): domains over time, and a ring 8 times longer.
  5. Diagnostic result (C267): at t = 5 there are about 102 domains per 512 loci (P3 would have held at that time);
     on a ring of 4,096 the seed's hand covers about half until late, so run 1's seed wins (P6-P8 wrong) were a small-ring effect.
"""
import math
import sys

import numpy as np

L, G_FB, V0, NB, DT = 512, 0.5, 0.05, 8, 0.02
X = np.arange(L)


def hops(psi):
    a = np.roll(psi, -1)
    den = np.abs(psi) ** 2 + np.abs(a) ** 2
    v = np.divide(2 * np.imag(np.conj(psi) * a), den, out=np.zeros(L), where=den > 0)
    for _ in range(NB):
        v = 0.25 * np.roll(v, 1) + 0.5 * v + 0.25 * np.roll(v, -1)
    d = G_FB * np.tanh(v / V0)
    return 1 - d, 1 + d


def step(psi):
    tf, tb = hops(psi)
    tfp = np.roll(tf, 1)

    def rhs(p):
        return -1j * (tfp * np.roll(p, 1) + tb * np.roll(p, -1))

    k1 = rhs(psi); k2 = rhs(psi + 0.5 * DT * k1); k3 = rhs(psi + 0.5 * DT * k2); k4 = rhs(psi + DT * k3)
    psi = psi + DT * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return psi / np.linalg.norm(psi)


def evolve(psi, t_end, snapshots=()):
    psi = psi / np.linalg.norm(psi)
    snaps = {}
    n = int(round(t_end / DT))
    marks = {int(round(t / DT)): t for t in snapshots}
    for i in range(1, n + 1):
        psi = step(psi)
        if i in marks:
            snaps[marks[i]] = psi.copy()
    return psi, snaps


def hands(psi):
    tf, tb = hops(psi)
    d = tb - tf
    return np.where(np.abs(d) > 0.1, np.sign(d), 0).astype(int)


def domains(h):
    nz = h[h != 0]
    if len(nz) == 0:
        return 0
    changes = int(np.sum(nz != np.roll(nz, 1)))
    return max(changes, 1)


def noise(rng, eps):
    return eps * (rng.standard_normal(L) + 1j * rng.standard_normal(L)) / math.sqrt(2)


def bump():
    return np.exp(-((X - L / 2) / 32.0) ** 2)


def mirror(psi):
    return psi[(-X) % L]


def lambda_theory():
    k = np.linspace(1e-4, math.pi - 1e-4, 20001)
    s = 4 * np.sin(k / 2) ** 2
    a = (G_FB / V0) * np.cos(k / 2) ** (2 * NB) * s
    lam = (a + np.real(np.sqrt((a ** 2 - 4 * s ** 2).astype(complex)))) / 2
    i = int(np.argmax(lam))
    return float(lam[i]), float(k[i])


def main():
    lam, kmax = lambda_theory()
    rng = np.random.default_rng(99)
    psi = 1 + noise(rng, 1e-12)
    psi = psi / np.linalg.norm(psi)
    rms = {}
    for i in range(1, int(round(12 / DT)) + 1):
        psi = step(psi)
        if i in (int(round(6 / DT)), int(round(12 / DT))):
            tf, tb = hops(psi)
            rms[i] = float(np.sqrt(np.mean((tb - tf) ** 2)))
    i6, i12 = int(round(6 / DT)), int(round(12 / DT))
    lam_meas = math.log(rms[i12] / rms[i6]) / 6.0
    print("G: linear theory lambda_max %.3f at k %.3f; measured %.3f (rms t_b - t_f %.2e -> %.2e)" % (lam, kmax, lam_meas, rms[i6], rms[i12]))

    rng = np.random.default_rng(2026)
    s0 = 1 + noise(rng, 1e-3)
    e1, _ = evolve(s0.copy(), 5.0)
    e2, _ = evolve(mirror(s0), 5.0)
    merr = float(np.max(np.abs(mirror(e1) - e2)))
    h1, h2 = hands(e1), hands(e2)
    hmirror = bool(np.all(h2 == -h1[(-X - 1) % L]))
    print("M: mirror error %.1e; hands mirrored: %s; handed bonds %d" % (merr, hmirror, int(np.sum(h1 != 0))))

    eu, _ = evolve(np.ones(L, dtype=complex), 400.0)
    uni_ok = bool(np.max(np.abs(eu - eu[0])) == 0 and np.all(hands(eu) == 0))
    print("uniform start: exactly uniform at t = 400: %s" % uni_ok)

    rng = np.random.default_rng(12345)
    d50, d400, plus, handed, plus_runs = [], [], 0, 0, []
    for r in range(20):
        end, snaps = evolve(1 + noise(rng, 1e-3), 400.0, snapshots=(50.0,))
        h50, h = hands(snaps[50.0]), hands(end)
        d50.append(domains(h50)); d400.append(domains(h))
        if int(np.sum(h == 1)) == L:
            plus_runs.append(r)
        plus += int(np.sum(h == 1)); handed += int(np.sum(h != 0))
        print("A run %2d: domains t50 %3d, t400 %3d; +1 %3d, -1 %3d, unhanded %3d" % (r, d50[-1], d400[-1], np.sum(h == 1), np.sum(h == -1), np.sum(h == 0)))
    share_plus = plus / handed if handed else float("nan")

    rng = np.random.default_rng(54321)
    cover_b = []
    for r in range(10):
        end, _ = evolve(1 + 0.5 * bump() * np.exp(1j * 0.3 * X) + noise(rng, 1e-3), 400.0)
        h = hands(end)
        cover_b.append(float(np.mean(h == 1)))
        print("B run %d: seed hand covers %.3f; domains %d" % (r, cover_b[-1], domains(h)))
    rng = np.random.default_rng(777)
    end, _ = evolve(1 + 0.5 * bump() * np.exp(1j * 0.3 * X) + noise(rng, 1e-9), 400.0)
    cover_c = float(np.mean(hands(end) == 1))
    print("C: seed hand covers %.3f; domains %d" % (cover_c, domains(hands(end))))
    end, _ = evolve(1 + 0.5 * bump() * np.exp(1j * 0.3 * X), 400.0)
    cover_d = float(np.mean(hands(end) == 1))
    print("D: seed hand covers %.3f; domains %d" % (cover_d, domains(hands(end))))

    rng = np.random.default_rng(31415)
    k0 = 2 * math.pi * 24 / L
    cover_e = []
    for r in range(5):
        start = np.exp(1j * k0 * X) + 0.5 * bump() * np.exp(-1j * 0.3 * X) + noise(rng, 1e-3)
        h0 = hands(start / np.linalg.norm(start))
        end, _ = evolve(start, 400.0)
        h = hands(end)
        cover_e.append(float(np.mean(h == 1)))
        print("E run %d: background hand covers %.3f at start, %.3f at t = 400; domains %d" % (r, float(np.mean(h0 == 1)), cover_e[-1], domains(h)))

    checks = [
        ("P0 growth rate within 30% of linear theory", abs(lam_meas / lam - 1) <= 0.3),
        ("P1 mirror check", merr < 1e-9 and hmirror),
        ("P2 exactly uniform start stays uniform and unhanded", uni_ok),
        ("P3 A t = 50: every run at least 10 domains", min(d50) >= 10),
        ("P4 A t = 400: at least 15 of 20 runs with 2+ domains", sum(d >= 2 for d in d400) >= 15),
        ("P5 A t = 400: share +1 among handed bonds in [0.4, 0.6]", 0.4 <= share_plus <= 0.6),
        ("P6 B: seed hand under 50% in at least 8 of 10", sum(c < 0.5 for c in cover_b) >= 8),
        ("P7 C: seed hand under 50%", cover_c < 0.5),
        ("P8 D: seed hand under 90%", cover_d < 0.9),
        ("P9 E: background hand at least 90% in at least 4 of 5", sum(c >= 0.9 for c in cover_e) >= 4),
    ]
    print("\nA: share +1 among handed bonds %.3f; domains t50 min %d median %.0f; t400 min %d median %.0f"
          % (share_plus, min(d50), np.median(d50), min(d400), np.median(d400)))
    print("\nFrozen predictions:")
    for name, passed in checks:
        print("  %-6s %s" % ("RIGHT" if passed else "WRONG", name))
    recorded = [
        ("P1, P2 code properties", checks[1][1] and checks[2][1]),
        ("run-1 A reproduces (domains t50, one domain at t400 in all, +1 in runs 0 4 6 7 10 17 18)",
         d50 == [6, 2, 2, 4, 4, 2, 4, 4, 2, 2, 2, 4, 4, 6, 2, 2, 1, 4, 4, 2] and d400 == [1] * 20
         and plus_runs == [0, 4, 6, 7, 10, 17, 18]),
        ("run-1 B, C, D, E coverage reproduces (all 1.000)",
         all(c == 1.0 for c in cover_b) and cover_c == 1.0 and cover_d == 1.0 and all(c == 1.0 for c in cover_e)),
    ]
    ok = True
    print("\nRecorded results reproduce:")
    for name, passed in recorded:
        ok &= passed
        print("%-4s %s" % ("PASS" if passed else "FAIL", name))
    print("ALL PASS" if ok else "SOME FAIL")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
