"""The decisive test: does a pattern with NO dimension acquire one when participation becomes thick?

Road T showed that in the thick regime, read with ED's own instrument (paper 10 S3.5, the number of independent
participation directions available at scale), a pattern grown from a cubic torus reads exactly 3 and one grown from
a ring reads exactly 1. But three went in and three came out: that is preservation, not selection.

This runs the same growth from a RANDOM WEB - an object ED's instrument reads as having NO definite number of
directions at all - and asks whether thickness gives it one.

  If it stays undefined       ED's rules carry a dimension but do not make one. The persistence story, confirmed
                              with ED's own instrument in ED's own regime, and the project's answer.
  If it becomes definite      ED's rules SELECT a number of directions from a pattern that had none. That is the
                              thing this project has been looking for since attempt 5, and the value it picks is
                              then the question.

ROBUSTNESS, fixed before the run (the instrument is new and Allen's caveat that these are early definitions is
recorded): a reading counts as DEFINITE only if
  - the group of lowest modes is the same size at all three clustering tolerances (0.15, 0.25, 0.40), AND
  - the group size is even (directions come in pairs, one per direction), AND
  - the gap ratio - the next mode above the group, divided by the top of the group - is at least 1.5.
Anything else is reported as no definite reading, whatever number the bare calculation returns.

EXPECTATIONS, fixed before running:
  W1  the web start, thickened, gives a DEFINITE number of directions            about 35%
  W2  if it does, that number is 3                                               about 20%
  W3  the controls behave: ring reads 1, cubic torus reads 3                     high
  W4  reported: gap ratios and tolerance agreement for every run
"""
import io
import json
import os
import sys
import time
import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse.csgraph import connected_components

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for rel in (("..", "..", "ED_Attempt_12", "model"), ("..", "..", "ED_Attempt_11", "model"),
            ("..", "..", "ED_Attempt_08", "model")):
    sys.path.insert(0, os.path.join(HERE, *rel))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402
import g_grad as G                                          # noqa: E402
import t_thick as T                                         # noqa: E402
import ed_readings as E                                     # noqa: E402

OUT = os.path.join(HERE, "e_runs")
STARTS = ("web", "grid3D", "ring")
THICK = (12, 25, 50)
SEEDS = (1, 2, 3)
TOLS = (0.15, 0.25, 0.40)
GROW = 4.0


def giant(A):
    k, lab = connected_components(A, directed=False)
    if k == 1:
        return A, 1.0
    b = np.bincount(lab)
    i = np.flatnonzero(lab == b.argmax())
    return A[i][:, i], float(b.max()) / A.shape[0]


def directions_robust(A, nmodes=30):
    """ED's reading, with the robustness rule applied. Returns (reading or None, detail)."""
    Lap = E.laplacian(A)
    try:
        vals = eigsh(Lap, k=min(nmodes, A.shape[0] - 2), sigma=-1e-6, which="LM",
                     return_eigenvectors=False, maxiter=5000)
    except Exception:
        return None, {"why": "modes could not be computed"}
    vals = np.sort(np.real(vals))
    vals = vals[vals > 1e-8]
    if len(vals) < 6:
        return None, {"why": "too few modes"}
    groups, gaps = [], []
    for tol in TOLS:
        g = int(np.sum(vals <= vals[0] * (1.0 + tol)))
        groups.append(g)
        gaps.append(float(vals[g] / vals[g - 1]) if g < len(vals) else float("inf"))
    same = len(set(groups)) == 1
    g = groups[0]
    gap = gaps[1]
    ok = same and g % 2 == 0 and gap >= 1.5
    detail = {"groups": groups, "gap_ratio": round(gap, 3), "same_at_all_tolerances": same,
              "even": g % 2 == 0, "modes": [round(float(v), 6) for v in vals[:8]]}
    return (g / 2.0 if ok else None), detail


def grow_thick(name, rho, seed, grow=GROW):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng),
          "web": lambda: N1.rand_regular(2000, rng)}[name]()
    adj = P.to_adj(A0)
    omega = rng.normal(0, 1, len(adj))
    omega -= omega.mean()
    sp_pass = G.SIGMA_PASS * float(omega.std())
    while len(adj) < grow * A0.shape[0]:
        adj, omega = T.inherit_thick(adj, omega, rng, rho, sp_pass)
        omega = G.diffuse(adj, omega, G.ALPHA)
        omega -= omega.mean()
    return P.to_A(adj)


def main():
    os.makedirs(OUT, exist_ok=True)
    res, lines = [], []
    for name in STARTS:
        for rho in THICK:
            for seed in SEEDS:
                t0 = time.time()
                A, frac = giant(grow_thick(name, rho, seed))
                d, detail = directions_robust(A)
                ball = P.read(A)["d_H"]
                r = dict(start=name, rho=rho, seed=seed, n=A.shape[0], whole=round(frac, 3),
                         directions=d, ball=ball, secs=round(time.time() - t0, 1), **detail)
                res.append(r)
                lines.append("%-6s thickness %2d seed %d | n %5d | ED DIRECTIONS %s | groups at three tolerances %s"
                             " | gap ratio %s | ball growth %s"
                             % (name, rho, seed, A.shape[0], d, detail.get("groups"), detail.get("gap_ratio"), ball))
                print(lines[-1], flush=True)
                json.dump(res, open(os.path.join(OUT, "web.json"), "w"), indent=1, default=str)
    webs = [r for r in res if r["start"] == "web"]
    w1 = any(r["directions"] is not None for r in webs)
    vals = [r["directions"] for r in webs if r["directions"] is not None]
    w2 = bool(vals) and all(abs(v - 3.0) < 0.01 for v in vals)
    ctrl_ring = [r["directions"] for r in res if r["start"] == "ring"]
    ctrl_grid = [r["directions"] for r in res if r["start"] == "grid3D"]
    w3 = all(v == 1.0 for v in ctrl_ring if v is not None) and all(v == 3.0 for v in ctrl_grid if v is not None)
    lines.append("")
    lines.append("W1 (a web start acquires a definite number of directions) %s   values %s" % (w1, vals))
    lines.append("W2 (and that number is 3) %s" % w2)
    lines.append("W3 (controls: ring reads 1, cubic torus reads 3) %s   ring %s | cubic torus %s"
                 % (w3, ctrl_ring, ctrl_grid))
    if not w1:
        lines.append("** The web start keeps NO definite number of directions. ED's rules carry a dimension; they do "
                     "not make one. That is the project's answer, measured with ED's own instrument in ED's own "
                     "regime. **")
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "w_web.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
