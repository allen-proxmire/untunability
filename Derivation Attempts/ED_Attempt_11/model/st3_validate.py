"""Validation of the 2+1 program against published 3D CDT (note 7 option (a); the primes lesson: show the instrument sees
the known answer first).

The program is run as plain 3D CDT: weight exp(k0 N0 - k3 N3) with the total volume held near a target, which is what
Ambjorn-Jurkiewicz-Loll (hep-th/0011276) simulate. Their order parameter is tau = N22/N3. Their published behaviour
(their Fig. 7, spherical slices, T = 64): tau falls as k0 rises, about 0.25 at k0 = 5.25, and drops sharply to near zero
at k0 about 6.6 (a first-order transition); below the transition the spacetime is extended, above it the slices decouple.

Expected results, written down before this run:
  V1  tau falls as k0 rises, and drops sharply (tau > 0.15 at k0 = 4 and 5; tau < 0.05 at k0 = 8) - the published shape.
      Our slices are tori, not spheres, so the transition may sit at a different k0; the SHAPE is the test, not the place.
  V2  ED's value tau = 1/3 sits below the transition (at a k0 lower than where the drop happens).
  V3  reported, no expectation: in the extended region (k0 = 4, 5), what our slice reading says - the growth rate of
      distance across a slice with its size. If it reads like our 'crowded' runs (about 0.1 rather than 0.5), then a
      crumpled slice is what the extended phase looks like in our readings, and note 7's third reading holds.
Failure: if tau does not fall with k0 or shows no drop, the program does not reproduce published CDT and the 2+1 runs
cannot be trusted (recorded).
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
OUT = os.path.join(HERE, os.environ.get("OUTDIR", "st3_validate_runs"))
L, T, SWEEPS = 14, 16, int(os.environ.get("SWEEPS", "200"))
K0S = tuple(float(x) for x in os.environ.get("K0S", "0,2,4,5,6,7,8").split(","))
# ATTEMPT 2 (recorded): run 1 (200 sweeps, k0 = 0..8) gave tau falling from 0.465 to 0.263 with NO sharp drop, and tau
# was still falling at every k0 at the last reading - not equilibrated. Attempt 2 runs longer (1,000 sweeps) and higher
# (k0 = 8..14), where the drop should be if the program is right. Run 1 is kept in st3_validate_runs/ and st3_validate_run1.txt.


def do_job(k0):
    path = os.path.join(OUT, "k%.1f.json" % k0)
    if os.path.exists(path):
        return path
    from st3 import Spacetime
    import st3_run as R
    t0 = time.perf_counter()
    X = Spacetime(L, T, seed=5).as_cdt(k0)
    rec = dict(k0=k0, L=L, T=T, N3s=X.N3s, taus=[], readings=[], fails=[])
    for sw in range(1, SWEEPS + 1):
        for _ in range(X.N3()):
            X.step()
        if sw % 20 == 0:
            n3 = X.N3()
            rec["taus"].append((sw, X.N22_cur / n3, X.N0(), n3))
            if X.check():
                rec["fails"].append((sw, X.check()[:2]))
                break
            json.dump(rec, open(path, "w"))
    rec["final"] = R.reading(X, 3)
    rec["tau"] = float(np.mean([t for _, t, _, _ in rec["taus"][-5:]]))
    rec["hours"] = (time.perf_counter() - t0) / 3600
    json.dump(rec, open(path, "w"))
    return path


def report():
    rows = []
    for k0 in K0S:
        p = os.path.join(OUT, "k%.1f.json" % k0)
        if not os.path.exists(p):
            continue
        r = json.load(open(p))
        f = r.get("final", {})
        sl = [(n, m) for (_, n, m) in f.get("slices", []) if m]
        rate = float(np.polyfit(np.log([x[0] for x in sl]), np.log([x[1] for x in sl]), 1)[0]) if len(sl) > 3 else None
        prof = f.get("profile", [])
        rows.append(dict(k0=k0, tau=r.get("tau"), N0=f.get("N0"), N3=f.get("N3"), spacetime=f.get("spacetime"),
                         slice_md=f.get("slice_md"), rate=rate, prof_min=min(prof) if prof else None,
                         prof_max=max(prof) if prof else None, fails=r["fails"], taus=[round(t, 3) for _, t, _, _ in r["taus"]]))
    L_ = ["published 3D CDT (AJL Fig. 7, spherical slices): tau about 0.25 at k0 = 5.25, dropping sharply to about 0 near k0 = 6.6"]
    for r in rows:
        L_.append("k0 %4.1f | tau %.3f | N0 %s N3 %s | spacetime %s | slice md %s rate %s | slice sizes %s-%s | fails %s"
                  % (r["k0"], r["tau"] or float("nan"), r["N0"], r["N3"],
                     None if r["spacetime"] is None else round(r["spacetime"], 3),
                     None if r["slice_md"] is None else round(r["slice_md"], 2),
                     None if r["rate"] is None else round(r["rate"], 3), r["prof_min"], r["prof_max"], r["fails"]))
        L_.append("    tau by sweep: %s" % r["taus"])
    if len(rows) >= 5:
        taus = {r["k0"]: r["tau"] for r in rows}
        falls = all(taus[a] >= taus[b] - 0.02 for a, b in zip(K0S, K0S[1:]) if a in taus and b in taus)
        V1 = falls and taus.get(4.0, 0) > 0.15 and taus.get(5.0, 0) > 0.15 and taus.get(8.0, 1) < 0.05
        below = [k for k in K0S if taus.get(k, 0) >= 1 / 3]
        V2 = bool(below)
        L_.append("V1 (published shape) %s | V2 (ED's tau = 1/3 below the drop) %s: couplings with tau >= 1/3: %s" % (V1, V2, below))
        L_.append("V3 slice growth rate in the extended region: " + ", ".join(
            "k0 %.1f -> %s" % (r["k0"], None if r["rate"] is None else round(r["rate"], 3)) for r in rows if r["k0"] <= 5))
    text = "\n".join(L_)
    open(os.path.join(HERE, os.environ.get("TXT", "st3_validate.txt")), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
        sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for path in p.imap_unordered(do_job, K0S):
            print("  done", os.path.basename(path), flush=True)
    report()
