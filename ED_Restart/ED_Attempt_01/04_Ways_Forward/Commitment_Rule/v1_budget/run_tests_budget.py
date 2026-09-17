"""Run the tests frozen in Spec.md against rule_budget.py and report each one.

    python run_tests_budget.py

Exits with an error only if a code check fails (H1-H4, S1, F0); F1-F3 are reported against
the frozen predictions, F4 is reported only.
"""
import sys

import numpy as np

import rule_budget as r

sys.stdout.reconfigure(encoding="utf-8")
results = {}


def report(name, ok, detail):
    results[name] = ok
    print("%-4s %s  %s" % ("PASS" if ok else "FAIL", name, detail))


L = 400
H = r.generator(L)
rng = np.random.default_rng(3)

print("\nTest H: the construction")
Hs_rand = r.slowed(H, rng.uniform(0, 0.5, size=L), 4.0)
herm = np.max(np.abs(Hs_rand - Hs_rand.conj().T))
emin = np.linalg.eigvalsh(H + 4.0 * np.eye(3 * L)).min()
report("H1 Hermitian, all energies of H + m positive", herm < 1e-12 and emin > 0, "max asymmetry %.1e, lowest energy %.4f" % (herm, emin))
diff = np.max(np.abs(r.slowed(H, np.zeros(L), 4.0) - (H + 4.0 * np.eye(3 * L))))
report("H2 U = 0 gives H + m exactly", diff == 0.0, "max difference %.1e" % diff)
psi = rng.normal(size=3 * L) + 1j * rng.normal(size=3 * L)
psi /= np.linalg.norm(psi)
norm_err = abs(np.linalg.norm(r.evolve(Hs_rand, psi, 40.0)) - 1.0)
report("H3 amount conserved", norm_err < 1e-12, "change %.1e" % norm_err)
U_rand = rng.uniform(0, 0.3, size=L)
psi_small = rng.normal(size=3 * L) + 1j * rng.normal(size=3 * L)
psi_small /= np.linalg.norm(psi_small)
a = r.evolve(r.slowed(H, U_rand, 4.0), psi_small, 25.0)
b = r.evolve(r.slowed(H, r.mirror_profile(U_rand), 4.0), r.mirror_state(psi_small, L), 25.0)
merr = np.max(np.abs(r.mirror_state(a, L) - b))
report("H4 mirror check", merr < 1e-10, "max error %.1e" % merr)

print("\nTest S: uniform slowing is exact")
H1 = r.slowed(H, np.zeros(L), 4.0)
H07 = r.slowed(H, np.full(L, 0.3), 4.0)
serr = np.max(np.abs(r.evolve(H07, psi_small, 30.0) - r.evolve(H1, psi_small, 0.7 * 30.0)))
report("S1 slowed at t equals unslowed at 0.7 t", serr < 1e-10, "max difference %.1e" % serr)

print("\nTest F: does a pattern fall toward the mass?")
x0, xm, T = 120, 200, 40.0
u = np.arange(L)
start = np.zeros((L, 3), dtype=complex)
start[:, r.INTERNAL] = np.exp(-((u - x0) ** 2) / (2 * 6.0 ** 2))
start = start.reshape(-1) / np.linalg.norm(start)


def centre(psi):
    s = r.shares(psi, L)
    return (s * u).sum() / s.sum()


def drift(U0, m, potential_only=False):
    U = r.mass_profile(L, xm, U0)
    if potential_only:
        Hx = H + m * np.eye(3 * L) - m * np.diag(np.repeat(U, 3))
    else:
        Hx = r.slowed(H, U, m)
    return centre(r.evolve(Hx, start, T)) - centre(start)


d0 = drift(0.0, 4.0)
report("F0 no mass, no drift", abs(d0) < 1e-10, "drift %.1e" % d0)
d1 = drift(0.01, 4.0)
results["F1"] = d1 > 0
print("%-4s F1 positive amount falls toward the mass  drift %+.6f  (predicted: PASS)" % ("PASS" if d1 > 0 else "FAIL", d1))
dneg = drift(0.01, -4.0)
results["F2"] = dneg < 0
print("%-4s F2 negative amount moves away  drift %+.6f  (predicted: PASS)" % ("PASS" if dneg < 0 else "FAIL", dneg))
d2 = drift(0.02, 4.0)
ratio = d2 / d1 if d1 != 0 else float("nan")
results["F3"] = 1.8 <= ratio <= 2.2
print("%-4s F3 proportional  drift at 0.02 / drift at 0.01 = %.4f  (predicted: PASS)" % ("PASS" if results["F3"] else "FAIL", ratio))
dpot = drift(0.01, 4.0, potential_only=True)
print("     F4 potential only (hopping unslowed): drift %+.6f, ratio to F1 %.4f  (reported)" % (dpot, dpot / d1 if d1 else float("nan")))

print("\nFollow-up K/E (added after the first run; predictions written in Spec.md before running)")
dk = drift(0.01, 0.0)
print("     K1 Internal start, slowed, m = 0: drift %+.6f  (predicted +0.0049 within 20%%: %s)"
      % (dk, "RIGHT" if abs(dk - 0.0049) <= 0.2 * 0.0049 else "WRONG"))
massive = np.zeros((L, 3), dtype=complex)
g = np.exp(-((u - x0) ** 2) / (2 * 6.0 ** 2))
for K in range(3):
    massive[:, K] = g / np.sqrt(3)
massive = massive.reshape(-1) / np.linalg.norm(massive)


def drift_from(psi0, U0, m, potential_only=False):
    U = r.mass_profile(L, xm, U0)
    Hx = (H + m * np.eye(3 * L) - m * np.diag(np.repeat(U, 3))) if potential_only else r.slowed(H, U, m)
    return centre(r.evolve(Hx, psi0, T)) - centre(psi0)


e0 = drift_from(massive, 0.0, 4.0)
e1 = drift_from(massive, 0.01, 4.0, potential_only=True)
e2 = drift_from(massive, 0.01, 4.0)
e3 = drift_from(massive, 0.01, -4.0)
print("     E0 massive-like start, no mass: drift %+.1e" % e0)
print("     E1 massive-like start, potential only, m = +4: drift %+.6f  (predicted toward: %s)" % (e1, "RIGHT" if e1 > 0 else "WRONG"))
print("     E2 massive-like start, slowed, m = +4: drift %+.6f  (predicted toward and larger than E1: %s)" % (e2, "RIGHT" if e2 > max(e1, 0) else "WRONG"))
print("     E3 massive-like start, slowed, m = -4: drift %+.6f  (reported)" % e3)

print("\nTest M: RD35 (ticking slows by s, moving between loci by s^2), predictions written in Spec.md before running")
H35 = r.slowed_rd35(H, U_rand, 4.0)
herm35 = np.max(np.abs(H35 - H35.conj().T))
zero35 = np.max(np.abs(r.slowed_rd35(H, np.zeros(L), 4.0) - (H + 4.0 * np.eye(3 * L))))
norm35 = abs(np.linalg.norm(r.evolve(H35, psi_small, 40.0)) - 1.0)
a35 = r.evolve(H35, psi_small, 25.0)
b35 = r.evolve(r.slowed_rd35(H, r.mirror_profile(U_rand), 4.0), r.mirror_state(psi_small, L), 25.0)
mir35 = np.max(np.abs(r.mirror_state(a35, L) - b35))
report("M1 RD35 generator: Hermitian, U = 0 exact, amount conserved, mirror",
       herm35 < 1e-12 and zero35 == 0.0 and norm35 < 1e-12 and mir35 < 1e-10,
       "asymmetry %.1e, U=0 difference %.1e, amount change %.1e, mirror error %.1e" % (herm35, zero35, norm35, mir35))
Hhop = r.generator(L, g=0.0)
m2 = np.max(np.abs(r.evolve(r.slowed_rd35(Hhop, np.full(L, 0.3), 0.0), psi_small, 30.0)
                   - r.evolve(Hhop, psi_small, 0.49 * 30.0)))
report("M2 hops only, uniform U = 0.3: slowed at t equals unslowed at 0.49 t", m2 < 1e-10, "max difference %.1e" % m2)


def drift35(psi0, U0, m):
    U = r.mass_profile(L, xm, U0)
    return centre(r.evolve(r.slowed_rd35(H, U, m), psi0, T)) - centre(psi0)


m3 = drift35(start, 0.01, 0.0)
results["M3"] = m3 > 0 and 1.5 * dk <= m3 <= 2.5 * dk
print("%-4s M3 lingering only (Internal start, m = 0): drift %+.6f = %.3f x K1  (predicted toward, 1.5-2.5 x K1)"
      % ("PASS" if results["M3"] else "FAIL", m3, m3 / dk))
m4 = drift35(massive, 0.01, 4.0)
results["M4"] = m4 > 0 and abs(m4 - e2) <= 0.15 * e2
print("%-4s M4 massive-like, m = +4: drift %+.6f = %.3f x E2  (predicted toward, within 15%% of E2)"
      % ("PASS" if results["M4"] else "FAIL", m4, m4 / e2))
m5 = drift35(massive, 0.01, -4.0)
results["M5"] = m5 < 0
print("%-4s M5 massive-like, m = -4: drift %+.6f  (predicted away)" % ("PASS" if results["M5"] else "FAIL", m5))

print("\nTest N: RD36 (rate e^(-U); moving e^(-2U)), predictions written in Spec.md before running")
H36 = r.slowed_rd36(H, U_rand, 4.0)
herm36 = np.max(np.abs(H36 - H36.conj().T))
zero36 = np.max(np.abs(r.slowed_rd36(H, np.zeros(L), 4.0) - (H + 4.0 * np.eye(3 * L))))
norm36 = abs(np.linalg.norm(r.evolve(H36, psi_small, 40.0)) - 1.0)
a36 = r.evolve(H36, psi_small, 25.0)
b36 = r.evolve(r.slowed_rd36(H, r.mirror_profile(U_rand), 4.0), r.mirror_state(psi_small, L), 25.0)
mir36 = np.max(np.abs(r.mirror_state(a36, L) - b36))
report("N1 RD36 generator: Hermitian, U = 0 exact, amount conserved, mirror",
       herm36 < 1e-12 and zero36 == 0.0 and norm36 < 1e-12 and mir36 < 1e-10,
       "asymmetry %.1e, U=0 difference %.1e, amount change %.1e, mirror error %.1e" % (herm36, zero36, norm36, mir36))
n2 = np.max(np.abs(r.evolve(r.slowed_rd36(Hhop, np.full(L, 0.3), 0.0), psi_small, 30.0)
                   - r.evolve(Hhop, psi_small, np.exp(-0.6) * 30.0)))
report("N2 hops only, uniform U = 0.3: slowed at t equals unslowed at e^(-0.6) t", n2 < 1e-10, "max difference %.1e" % n2)
n3 = centre(r.evolve(r.slowed_rd36(H, r.mass_profile(L, xm, 0.01), 4.0), massive, T)) - centre(massive)
results["N3"] = abs(n3 - m4) <= 0.02 * abs(m4)
print("%-4s N3 massive-like, m = +4: drift %+.6f = %.4f x M4  (predicted within 2%%)" % ("PASS" if results["N3"] else "FAIL", n3, n3 / m4))

print("\nSummary")
for name, ok in results.items():
    print("  %-50s %s" % (name, "PASS" if ok else "FAIL"))
code = [k for k in results if k[:2] in ("H1", "H2", "H3", "H4", "S1", "F0")]
broken = [k for k in code if not results[k]]
print("\ncode checks (H1-H4, S1, F0): %s" % ("all pass" if not broken else "FAILED: " + ", ".join(broken)))
sys.exit(1 if broken else 0)
