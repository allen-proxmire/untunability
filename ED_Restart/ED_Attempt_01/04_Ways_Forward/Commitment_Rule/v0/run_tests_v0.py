"""Run the tests frozen in Spec.md against rule_v0.py and report each one.

    python run_tests_v0.py

Prints every measured number. Exits with an error only if the *code* is broken
(tests A and B, and test D's baseline); the other outcomes are findings and are
reported, not asserted.
"""
import sys
import numpy as np
import rule_v0 as r

sys.stdout.reconfigure(encoding="utf-8")
results = {}


def report(name, ok, detail):
    results[name] = ok
    print("%-4s %s  %s" % ("PASS" if ok else "FAIL", name, detail))


# ---------------- Test A: mirror check ----------------
print("\nTest A: mirror check (T2)")
rng = np.random.default_rng(1)
L = 40
a0 = rng.normal(size=(L, 3)) + 1j * rng.normal(size=(L, 3))
M = rng.uniform(0, 0.05, size=L)
a, am = a0.copy(), r.mirror(a0)
U, Um = np.zeros(L), np.zeros(L)
thin_step, thin_step_m = None, None
for t in range(1, 51):
    a, am = r.walk_step(a), r.walk_step(am)
    U, Um = r.budget_step(U, M, 0.7), r.budget_step(Um, M[(-np.arange(L)) % L], 0.7)
    if thin_step is None and r.too_thin(a, 0.05):
        thin_step = t
    if thin_step_m is None and r.too_thin(am, 0.05):
        thin_step_m = t
err_pattern = np.max(np.abs(r.mirror(a) - am))
err_budget = np.max(np.abs(U[(-np.arange(L)) % L] - Um))
err_draw = np.max(np.abs(r.mirror(r.draw_probabilities(a)) - r.draw_probabilities(am)))
report("A1 pattern", err_pattern < 1e-12, "max error %.1e" % err_pattern)
report("A2 budget", err_budget < 1e-12, "max error %.1e" % err_budget)
report("A3 draw probabilities", err_draw < 1e-12, "max error %.1e" % err_draw)
report("A4 thin step", thin_step == thin_step_m, "original %s, mirror %s" % (thin_step, thin_step_m))

# ---------------- Test B: budget profile ----------------
print("\nTest B: budget profile around a mass (C54, T1 direction)")
L = 201
M = np.zeros(L)
M[0] = 0.1
NEIGHBOUR_AVG = np.zeros((L, L))
for u in range(L):
    NEIGHBOUR_AVG[u, (u + 1) % L] += 0.5
    NEIGHBOUR_AVG[u, (u - 1) % L] += 0.5
for q in (0.5, 0.9):
    U = r.budget_steady(M, q)
    U_exact = np.linalg.solve(np.eye(L) - q * NEIGHBOUR_AVG, M)   # cap at 1 not reached here
    match = np.max(np.abs(U - U_exact))
    report("B0 rule matches exact steady state q=%.1f" % q, match < 1e-12, "max difference %.1e" % match)
    rho = (2 / q - np.sqrt((2 / q) ** 2 - 4)) / 2
    ratios = U_exact[2:22] / U_exact[1:21]   # changed after freezing: see Spec.md
    rel = np.max(np.abs(ratios - rho) / rho)
    sym = np.max(np.abs(U[1:101] - U[::-1][:100]))
    s = r.rate(U)
    report("B1 falloff q=%.1f" % q, rel < 1e-6, "rho %.6f, max relative error %.1e" % (rho, rel))
    report("B2 symmetric q=%.1f" % q, sym < 1e-12, "max asymmetry %.1e" % sym)
    report("B3 slower at mass q=%.1f" % q, s[0] < s[100], "rate at mass %.4f, far %.4f" % (s[0], s[100]))

# ---------------- Test C: interference before a lone draw ----------------
print("\nTest C: interference before a lone draw (T4)")
L = 401
start = np.zeros((L, 3), dtype=complex)
start[L // 2, r.INTERNAL] = 1.0
tv_by_bmin = []
for b_min in (0.5, 0.3, 0.15, 0.08, 0.04):
    a = start.copy()
    P = np.abs(start) ** 2
    fired = None
    for t in range(1, 201):
        a = r.walk_step(a)
        P = r.decohered_step(P)
        if r.too_thin(a, b_min):
            fired = t
            break
    if fired is None:
        print("     observation  b_min %.2f: never too thin within 200 steps (max share %.3f)"
              % (b_min, r.shares(a).max()))
        continue
    tv = 0.5 * np.abs(r.shares(a) - P.sum(axis=1)).sum()
    tv_by_bmin.append((b_min, fired, tv))
    print("     b_min %.2f: draw at step %d, TV coherent vs decohered %.4f" % (b_min, fired, tv))
    if fired == 1:
        report("C1 no interference at step 1 (b_min %.2f)" % b_min, tv < 1e-12, "TV %.1e" % tv)
    else:
        report("C2 interference after spreading (b_min %.2f)" % b_min, tv > 1e-6, "TV %.4f" % tv)
tvs = [tv for _, _, tv in tv_by_bmin]
report("C3 more spreading, more interference", all(tvs[i + 1] >= tvs[i] - 1e-12 for i in range(len(tvs) - 1)),
       "TV in order of decreasing b_min: %s" % ", ".join("%.4f" % v for v in tvs))

# ---------------- Test D: no signalling ----------------
print("\nTest D: no signalling with an entangled pattern (T7)")
L = 16
A0 = np.zeros((L, 3, L, 3), dtype=complex)
A0[0, r.INTERNAL, 0, r.INTERNAL] = 1.0
A0[1, r.INTERNAL, 0, r.INTERNAL] = 1.0 / np.sqrt(2)
A0[1, r.INTERNAL, 1, r.INTERNAL] = 1.0 / np.sqrt(2)
A0 /= np.sqrt((np.abs(A0) ** 2).sum())
B_MIN, BOB_STEPS = 0.2, 3

# Alice idle: no spreading, no draw
A_idle = A0.copy()
# Alice spread: spread part A until it is first too thin
A_spread = A0.copy()
fired = None
for t in range(1, 101):
    A_spread = r.walk_step_part(A_spread, 0)
    if r.part_too_thin(A_spread, 0, B_MIN):
        fired = t
        break
print("     Alice's part first too thin at step %s" % fired)


def bob_after_steps_no_draw(A):
    for _ in range(BOB_STEPS):
        if r.part_too_thin(A, 1, B_MIN):
            return None
        A = r.walk_step_part(A, 1)
    return r.bob_distribution_no_draw(A)


# Bob must never get too thin himself during his steps (checked)
bob_idle = bob_after_steps_no_draw(A_idle)
bob_spread_nodraw = bob_after_steps_no_draw(A_spread)
bob_ok = bob_idle is not None and bob_spread_nodraw is not None
report("D0 Bob never too thin himself", bob_ok, "")

if fired is not None and bob_ok:
    base = np.max(np.abs(bob_idle - bob_spread_nodraw))
    report("D1 baseline, no draw", base < 1e-12, "max difference %.1e" % base)

    joint = r.bob_average_after_joint_draw(A_spread, BOB_STEPS)
    diff_joint = np.max(np.abs(joint - bob_idle))
    results["D2 joint draw"] = diff_joint < 1e-12
    print("%-4s D2 joint draw (RD5 literal)  max difference %.2e  (predicted: FAIL)"
          % ("PASS" if diff_joint < 1e-12 else "FAIL", diff_joint))

    local = r.bob_average_after_local_draw(A_spread, BOB_STEPS)
    diff_local = np.max(np.abs(local - bob_idle))
    results["D3 local draw"] = diff_local < 1e-12
    print("%-4s D3 local draw  max difference %.1e  (predicted: PASS)"
          % ("PASS" if diff_local < 1e-12 else "FAIL", diff_local))

    # D4 (added with RD22): the rule's own draw function, sampled, reproduces the exact local-draw average
    rng_d = np.random.default_rng(7)
    n_samples = 20000
    sampled = np.zeros(L)
    for _ in range(n_samples):
        drawn = r.draw_entangled(A_spread, 0, rng_d)
        for _ in range(BOB_STEPS):
            drawn = r.walk_step_part(drawn, 1)
        sampled += r.bob_distribution_no_draw(drawn)
    sampled /= n_samples
    diff_sampled = np.max(np.abs(sampled - local))
    report("D4 draw_entangled matches exact local average", diff_sampled < 0.02,
           "max difference %.4f over %d samples" % (diff_sampled, n_samples))

# ---------------- summary ----------------
print("\nSummary")
for name, ok in results.items():
    print("  %-45s %s" % (name, "PASS" if ok else "FAIL"))
code_checks = [k for k in results if k[0] in "AB" or k[:2] in ("D0", "D1", "D4")]
broken = [k for k in code_checks if not results[k]]
print("\ncode checks (A, B, D0, D1, D4): %s" % ("all pass" if not broken else "FAILED: " + ", ".join(broken)))
sys.exit(1 if broken else 0)
