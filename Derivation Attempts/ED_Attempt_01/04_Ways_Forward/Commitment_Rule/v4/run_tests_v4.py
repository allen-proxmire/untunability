"""Runs the version 4 tests in Spec.md and reports each frozen prediction. Exit code: V4-1a, V4-1b (code checks)."""
import math
import sys

import numpy as np

from rule_v4 import PopulationV4, RuleB, explicit_average, kraus, lane_channels, mirror_perm, pure

sys.stdout.reconfigure(encoding="utf-8")
checks = {}


def report(name, ok, detail):
    checks[name] = ok
    print("%-6s %s  %s" % ("RIGHT" if ok else "WRONG", name, detail), flush=True)


# V4-1a population map
rng = np.random.default_rng(7)
n = 3 * 8
X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
rho = X @ X.conj().T
rho /= np.trace(rho)
lane, dest = lane_channels(8, 2)
p = rng.uniform(0, 0.5, len(lane))
out = kraus(rho, lane, dest, p)
tr = abs(complex(np.trace(out)) - 1)
herm = float(np.max(np.abs(out - out.conj().T)))
mineig = float(np.min(np.linalg.eigvalsh(0.5 * (out + out.conj().T))))
report("V4-1a map keeps trace, Hermitian, positive", tr < 1e-12 and herm < 1e-12 and mineig >= -1e-12,
       "trace %.1e, herm %.1e, min eig %.1e" % (tr, herm, mineig))

# V4-1b mirror
L, D, GAMMA, THETA, V0, DT, T = 24, 2, 0.3, 0.8, 0.03, 0.02, 600.0
srng = np.random.default_rng(1357)
starts = [pure(1 + 0.1 * (srng.standard_normal(3 * L) + 1j * srng.standard_normal(3 * L)) / math.sqrt(2)) for _ in range(10)]
perm = mirror_perm(L)
pa, pb = PopulationV4(L, D, GAMMA, 0.9, THETA, V0, DT), PopulationV4(L, D, GAMMA, 0.9, THETA, V0, DT)
a1, b1 = pa.step(starts[0].copy()), pb.step(starts[0][np.ix_(perm, perm)])
m1 = float(np.max(np.abs(a1[np.ix_(perm, perm)] - b1)))
a20, b20 = pa.evolve(a1, 20.0 - DT), pb.evolve(b1, 20.0 - DT)
m20 = float(np.max(np.abs(a20[np.ix_(perm, perm)] - b20)))
report("V4-1b mirror (one step)", m1 < 1e-15, "one step %.1e; t = 20 %.1e" % (m1, m20))

# V4-2, V4-3 equivalence on a small ring
Ls, Ds = 4, 2
rs = RuleB(Ls, Ds, 1.0, 0.0, THETA, V0, phase_mode="const")
Hs = rs.hamiltonian(np.full(Ls, THETA), dense=True)
lane_s, dest_s = lane_channels(Ls, Ds)
p_s = np.array([0.20, 0.35, 0.10, 0.25])
erng = np.random.default_rng(404)
psi0 = erng.normal(size=3 * Ls) + 1j * erng.normal(size=3 * Ls)
psi0 /= np.linalg.norm(psi0)
from rule_v4 import unitary  # noqa: E402
Us = unitary(Hs, DT)
rk = np.outer(psi0, psi0.conj())
for _ in range(3):
    rk = kraus(Us @ rk @ Us.conj().T, lane_s, dest_s, p_s)
r3 = explicit_average(Hs, DT, lane_s, dest_s, p_s, psi0, 3, R=3)
r2 = explicit_average(Hs, DT, lane_s, dest_s, p_s, psi0, 3, R=2)
e3, e2 = float(np.max(np.abs(r3 - rk))), float(np.max(np.abs(r2 - rk)))
report("V4-2 explicit with draws (R 3) = population map", e3 < 1e-12, "max difference %.1e" % e3)
report("V4-3 explicit without draws (R 2) = population map", e2 < 1e-12, "max difference %.1e" % e2)

# V4-4..V4-8 tuned tests
tuned_signs = [-1, -1, 1, 1, -1, -1, 1, 1, 1, 1]


def run(label, g, v0, i):
    pop = PopulationV4(L, D, GAMMA, g, THETA, v0, DT)
    r = starts[i].copy()
    Js = []
    for _ in range(6):
        r = pop.evolve(r, T / 6)
        Js.append(pop.current(r))
    w = pop.rule.final_winding(np.random.default_rng(99))
    print("%s start %d: J at t = 100..600: %s; winding %d" % (label, i, " ".join("%+.3e" % q for q in Js), w), flush=True)
    return Js[-1], w


plus = [run("g +0.9 V0 0.03", 0.9, V0, i) for i in range(10)]
minus = [run("g -0.9 V0 0.03", -0.9, V0, i) for i in range(10)]
control = [run("control g +0.9 V0 0.2", 0.9, 0.2, i) for i in range(5)]
lasting = [(i, r) for i, r in enumerate(plus) if abs(r[0]) > 1e-3]
report("V4-4 g +0.9: at least 8 of 10 lasting", len(lasting) >= 8, "%d of 10" % len(lasting))
report("V4-5 lasting |J(600)| in [0.10, 0.13]", len(lasting) > 0 and all(0.10 <= abs(r[0]) <= 0.13 for _, r in lasting),
       "values %s" % ", ".join("%.3f" % abs(r[0]) for _, r in lasting))
agree = sum(1 for i, r in enumerate(plus) if np.sign(r[0]) == tuned_signs[i])
report("V4-6 direction agrees with the tuned test in at least 8 of 10", agree >= 8, "%d of 10" % agree)
report("V4-7 nonzero winding in at least half the lasting runs", len(lasting) > 0 and 2 * sum(r[1] != 0 for _, r in lasting) >= len(lasting),
       "%d of %d" % (sum(r[1] != 0 for _, r in lasting), len(lasting)))
report("V4-8 g -0.9 and control all die (< 1e-4)", all(abs(r[0]) < 1e-4 for r in minus + control),
       "largest %.1e" % max(abs(r[0]) for r in minus + control))

code = checks["V4-1a map keeps trace, Hermitian, positive"] and checks["V4-1b mirror (one step)"]
print("\nCODE CHECKS PASS" if code else "\nCODE CHECKS FAIL")
allright = all(checks.values())
print("RECORDED RESULTS REPRODUCE (all nine right, as in run 1)" if allright else "RECORDED RESULTS DO NOT REPRODUCE")
sys.exit(0 if code and allright else 1)
