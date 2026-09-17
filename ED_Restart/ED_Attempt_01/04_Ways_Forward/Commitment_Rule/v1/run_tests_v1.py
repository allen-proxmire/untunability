"""Run the tests frozen in Spec.md against rule_v1.py and report each one.

    python run_tests_v1.py

Prints every measured number. Exits with an error only if a *code* check fails
(U1, L1, M1, M2, E4, F0); the other outcomes are reported against the frozen predictions.
"""
import sys

import numpy as np

import rule_v1 as r

sys.stdout.reconfigure(encoding="utf-8")
results = {}


def report(name, ok, detail):
    results[name] = ok
    print("%-4s %s  %s" % ("PASS" if ok else "FAIL", name, detail))


I, LE, RI = r.INTERNAL, r.LEFT, r.RIGHT
LS, LM = 31, 8
X1, X2 = 13, 17
NS = 8
PHIS = (0.0, np.pi / 2, np.pi)


def random_pattern(rng, L):
    a = rng.normal(size=(L, 3)) + 1j * rng.normal(size=(L, 3))
    return a / np.sqrt((np.abs(a) ** 2).sum())


def system_start(phi):
    a = np.zeros((LS, 3), dtype=complex)
    a[X1, I] = 1 / np.sqrt(2)
    a[X2, I] = np.exp(1j * phi) / np.sqrt(2)
    return a


def marker_theta(theta):
    m = np.zeros((LM, 3), dtype=complex)
    m[0, I] = np.cos(theta)
    m[0, LE] = np.sin(theta)
    return m


def meeting(x, op):
    return lambda A: r.meet(A, x, op)


def marker_step(A):
    return r.walk_step_part(A, 1)


def branches(phi, m, pre, detect=False, post=()):
    """Per detector outcome: (probability, system screen after NS steps). One branch if no detector."""
    A = r.joint(system_start(phi), m)
    for f in pre:
        A = f(A)
    bs = r.detector_outcomes(A, 1) if detect else [(1.0, A)]
    out = []
    for w, B in bs:
        for f in post:
            B = f(B)
        for _ in range(NS):
            B = r.walk_step_part(B, 0)
        s = r.part_shares(B, 0)
        out.append((w, s / s.sum()))
    return out


def average_screen(bs):
    return sum(w * s for w, s in bs)


def visibility(P):
    """P = screens at phi = 0, pi/2, pi. Screen = a + Re(c e^{i phi}); V = |c| / a where a > 1e-9."""
    a = (P[0] + P[2]) / 2
    re = (P[0] - P[2]) / 2
    im = a - P[1]
    V = np.zeros_like(a)
    ok = a > 1e-9
    V[ok] = np.sqrt(re[ok] ** 2 + im[ok] ** 2) / a[ok]
    return V


def run_case(m, pre, detect=False, post=()):
    bs = [branches(phi, m, pre, detect, post) for phi in PHIS]
    return bs, visibility([average_screen(b) for b in bs])


def mirror_joint(A):
    ps = (-np.arange(A.shape[0])) % A.shape[0]
    pm = (-np.arange(A.shape[2])) % A.shape[2]
    ch = [I, RI, LE]
    return A[ps][:, ch][:, :, pm][:, :, :, ch]


rng = np.random.default_rng(11)

# ---------------- U1 ----------------
print("\nTest U1: meetings conserve the amount")
A = r.joint(random_pattern(rng, LS), random_pattern(rng, LM))
err = 0.0
for op in (r.swap_lanes, r.walk_step):
    for x in (0, 5, 30):
        B = r.meet(A, x, op)
        err = max(err, abs((np.abs(B) ** 2).sum() - (np.abs(A) ** 2).sum()))
report("U1 meet conserves the amount", err < 1e-12, "max change %.1e" % err)

# ---------------- L1 ----------------
print("\nTest L1: no spontaneous draws (RD26)")
a = random_pattern(rng, LS)
m1 = np.zeros((LM, 3), dtype=complex)
m1[0, I] = 1.0
A, draws = r.run(r.joint(a, m1), [("walk", 0)] * 200, rng)
b = a.copy()
for _ in range(200):
    b = r.walk_step(b)
err = np.max(np.abs(A - r.joint(b, m1)))
report("L1 lone pattern never draws", draws == 0 and err < 1e-12, "draws %d, max difference %.1e" % (draws, err))

# ---------------- M ----------------
print("\nTest M: mirror check (T2)")
a, m = random_pattern(rng, LS), random_pattern(rng, LM)
x, xm = 9, (-9) % LS
events = [("meet", x, r.swap_lanes)] + [("walk", 0), ("walk", 1)] * 5 + [("meet", x, r.walk_step)]
events_m = [("meet", xm, r.swap_lanes)] + [("walk", 0), ("walk", 1)] * 5 + [("meet", xm, r.walk_step)]
A, _ = r.run(r.joint(a, m), events, rng)
Am, _ = r.run(r.joint(r.mirror(a), r.mirror(m)), events_m, rng)
err = np.max(np.abs(mirror_joint(A) - Am))
report("M1 joint pattern matches mirror", err < 1e-12, "max error %.1e" % err)
avg = sum(w * r.part_shares(B, 0) for w, B in r.detector_outcomes(A, 1))
avg_m = sum(w * r.part_shares(B, 0) for w, B in r.detector_outcomes(Am, 1))
err = np.max(np.abs(avg[(-np.arange(LS)) % LS] - avg_m))
report("M2 detector-averaged screen matches mirror", err < 1e-12, "max error %.1e" % err)

# ---------------- E ----------------
print("\nTest E: a partial mark gives partial fringes (C109, C110)")
_, V0 = run_case(marker_theta(0.0), [])
print("     largest V0 (no meeting): %.4f" % V0.max())
cases = [("theta %.4f, lane swap" % t, marker_theta(t), r.swap_lanes)
         for t in (0.0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2)]
for seed in (21, 22):
    cases.append(("random marker %d, spreading step" % seed, random_pattern(np.random.default_rng(seed), LM), r.walk_step))
e1 = e2 = e3 = 0.0
print("     %-34s %8s %6s %8s %9s %9s %9s" % ("case", "overlap", "D", "max V", "E1 err", "D2+V2", "E3 diff"))
for label, m, op in cases:
    ov = abs(np.vdot(m, op(m)))
    bs, V = run_case(m, [meeting(X1, op)])
    err1 = np.max(np.abs(V - ov * V0))
    D2 = max(0.0, 1 - ov ** 2)
    dv = D2 + np.max(V) ** 2
    bsd, _ = run_case(m, [meeting(X1, op)], detect=True)
    err3 = max(np.max(np.abs(average_screen(bs[j]) - average_screen(bsd[j]))) for j in range(3))
    e1, e2, e3 = max(e1, err1), max(e2, dv), max(e3, err3)
    print("     %-34s %8.4f %6.4f %8.4f %9.1e %9.6f %9.1e" % (label, ov, np.sqrt(D2), V.max(), err1, dv, err3))
report("E1 V = |overlap| x V0 at every locus", e1 < 1e-10, "max error %.1e" % e1)
report("E2 D^2 + V^2 <= 1", e2 <= 1 + 1e-12, "largest D^2 + V^2 = %.12f" % e2)
report("E3 detector on marker leaves the system's screen unchanged", e3 < 1e-12, "max difference %.1e" % e3)

m = marker_theta(np.pi / 4)
A = r.meet(r.joint(system_start(0.0), m), X1, r.swap_lanes)
exact = average_screen(branches(0.0, m, [meeting(X1, r.swap_lanes)], detect=True))
rng_s = np.random.default_rng(7)
n_samples = 20000
sampled = np.zeros(LS)
for _ in range(n_samples):
    B = r.draw_local(A, 1, rng_s)
    for _ in range(NS):
        B = r.walk_step_part(B, 0)
    s = r.part_shares(B, 0)
    sampled += s / s.sum()
sampled /= n_samples
err = np.max(np.abs(sampled - exact))
report("E4 sampled draw matches exact average", err < 0.02, "max difference %.4f over %d samples" % (err, n_samples))

# ---------------- F ----------------
print("\nTest F: eraser (C111)")
m = marker_theta(np.pi / 2)
pre = [meeting(X1, r.swap_lanes), marker_step, marker_step, marker_step]
bs, Vavg = run_case(m, pre, detect=True)
same_len = len(set(len(b) for b in bs)) == 1
wdiff = max(abs(bs[j][k][0] - bs[0][k][0]) for j in range(3) for k in range(len(bs[0]))) if same_len else np.inf
report("F0 outcomes and probabilities same for every phase", same_len and wdiff < 1e-12,
       "%d outcomes, max probability difference %.1e" % (len(bs[0]), wdiff))
report("F1 no fringes overall", Vavg.max() < 1e-12, "largest average V %.1e" % Vavg.max())
best, best_w, best_k = 0.0, 0.0, None
for k in range(len(bs[0])):
    w = bs[0][k][0]
    if w <= 0.01:
        continue
    Vk = visibility([bs[j][k][1] for j in range(3)])
    if Vk.max() > best:
        best, best_w, best_k = Vk.max(), w, k
report("F2 fringes return in a sorted outcome", best > 0.5 * V0.max(),
       "best sorted V %.4f (outcome probability %.4f) vs 0.5 x largest V0 = %.4f" % (best, best_w, 0.5 * V0.max()))
bs_nd, _ = run_case(m, pre, detect=False)
err = max(np.max(np.abs(average_screen(bs[j]) - average_screen(bs_nd[j]))) for j in range(3))
report("F3 sorted screens add up to the undetected screen", err < 1e-12, "max difference %.1e" % err)

# ---------------- G ----------------
print("\nTest G: meetings without a mark; marks brought back or not (C107)")
m = random_pattern(np.random.default_rng(31), LM)
pre = [meeting(X1, r.walk_step), meeting(X2, r.walk_step)]
_, Vg = run_case(m, pre)
_, Vgd = run_case(m, pre, detect=True)
err = max(np.max(np.abs(Vg - V0)), np.max(np.abs(Vgd - V0)))
report("G1 meeting both paths alike leaves fringes", err < 1e-10, "max difference from V0 %.1e (with and without detector)" % err)

m = marker_theta(np.pi / 2)
_, Vmark = run_case(m, [meeting(X1, r.swap_lanes)])
_, Vback = run_case(m, [meeting(X1, r.swap_lanes), meeting(X1, r.swap_lanes)])
err = np.max(np.abs(Vback - V0))
report("G2 mark undone before a draw: fringes back", err < 1e-12,
       "V with mark %.1e; after undoing, max difference from V0 %.1e" % (Vmark.max(), err))
_, Vafter = run_case(m, [meeting(X1, r.swap_lanes)], detect=True, post=[meeting(X1, r.swap_lanes)])
report("G3 'undone' after a draw: no fringes", Vafter.max() < 1e-12, "largest average V %.1e" % Vafter.max())

# ---------------- summary ----------------
print("\nSummary")
for name, ok in results.items():
    print("  %-60s %s" % (name, "PASS" if ok else "FAIL"))
code_checks = [k for k in results if k[:2] in ("U1", "L1", "M1", "M2", "E4", "F0")]
broken = [k for k in code_checks if not results[k]]
print("\ncode checks (U1, L1, M1, M2, E4, F0): %s" % ("all pass" if not broken else "FAILED: " + ", ".join(broken)))
sys.exit(1 if broken else 0)
