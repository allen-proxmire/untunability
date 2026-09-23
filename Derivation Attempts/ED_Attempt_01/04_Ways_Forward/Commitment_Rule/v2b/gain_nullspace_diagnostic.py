"""Diagnostic after gain check run 1 (not pre-registered): does the version 2b Liouvillian (fixed phases, fixed rates)
have more than one steady state at theta = 0, which would make the theta = 0 solve ill-posed?

Small ring (L = 12, D = 3, so 36 channels and a 1,296-dimensional Liouvillian), dense eigenvalues. Counts eigenvalues
with |lambda| < 1e-9 (steady states) for theta in {0, 0.4} and Gamma in {0.3, 1, 3}, delta = 1e-3. Also reports the
spectrum of H at theta = 0 (flat bands would signal compact states that can avoid the drawn channels), the response chi
at theta = 0.4 on this ring, and, for theta = 0, the largest steady flow over a basis of the steady states."""
import numpy as np

from gain_check import liouvillian, rates
from rule_v2b import RuleB

L, D = 12, 3
for Gamma in (0.3, 1.0, 3.0):
    rule = RuleB(L, D, Gamma, 0.0, 0.0)
    for theta in (0.0, 0.4):
        Lv = liouvillian(rule, theta, rates(rule, Gamma, 1e-3)).toarray()
        w, V = np.linalg.eig(Lv)
        zero = np.where(np.abs(w) < 1e-9)[0]
        gap = np.sort(np.abs(w))[len(zero)] if len(zero) < len(w) else float("nan")
        flows = []
        for k in zero:
            rho = V[:, k].reshape((rule.n, rule.n), order="F")
            tr = np.trace(rho)
            if abs(tr) > 1e-8:
                rho = rho / tr
                rho = 0.5 * (rho + rho.conj().T)
                j = rule.currents(rho, np.full(L, theta))
                flows.append(float(np.max(np.abs(j))))
        print("Gamma %.1f theta %.1f: steady states %d; next |lambda| %.2e; largest |current| over trace-carrying steady states %s"
              % (Gamma, theta, len(zero), gap, ("%.2e" % max(flows)) if flows else "none"), flush=True)

rule = RuleB(L, D, 1.0, 0.0, 0.0)
H = rule.hamiltonian(np.zeros(L), dense=True)
ev = np.sort(np.linalg.eigvalsh(H))
vals, counts = np.unique(np.round(ev, 8), return_counts=True)
print("H at theta 0 (L 12): eigenvalues with multiplicity > 2: %s" % [(float(v), int(c)) for v, c in zip(vals, counts) if c > 2])
