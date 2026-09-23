"""ED's 2+1 runs, judged against the extended phase itself (C17's correction), with the compiled sampler.

C12's rule asked ED's slices to read like flat surfaces (growth rate 0.5). C17 showed that a KNOWN extended spacetime
reads 0.22-0.29 on that measure, so the target was wrong. Here ED is compared with two references measured at the same
sizes with the same readings:
  EXT  plain CDT at k0 = 3.2 - the coupling where the published-style scan gives tau near ED's own 1/3, inside the
       extended phase (C17: the drop sits between k0 = 5 and 6)
  COL  plain CDT at k0 = 8 - above the drop, the collapsed phase
and ED itself from two starts (flat product stack; crowded stack of rewired slices), with its three totals held.

Expectations, written before this run:
  E0  no check failures below the drop (the engine's check cannot run in the collapsed phase, C17)
  E1  EXT and COL differ clearly: slice growth rate and the spread of slice sizes
  E2  ED's readings (both starts) match EXT within 0.08 on the slice growth rate and within 0.5 on the spacetime reading
  E3  ED's two starts agree with each other within the same tolerances
Outcome: E2 and E3 -> 'in 2+1, ED's conserved totals give what the extended phase gives, with nothing tuned'.
E2 failing toward COL -> ED's point behaves like the collapsed phase. Starts disagreeing -> still not settled.
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
OUT = os.path.join(HERE, "st3f_ed_runs")
T, SWEEPS, BLOCKS = 16, 20000, 20
SIZES = (20, 28)
JOBS = [(L, k) for L in SIZES for k in ("ed_flat", "ed_crowded", "ext", "col")]


def do_job(job):
    L, kind = job
    path = os.path.join(OUT, "L%d_%s.json" % (L, kind))
    if os.path.exists(path) and json.load(open(path)).get("done"):
        return path
    from st3f_run import Fast
    from st3 import random_torus_tris
    import st3_run as R
    t0 = time.time()
    if kind.startswith("ed"):
        tris = None if kind.endswith("flat") else random_torus_tris(L)
        F = Fast(L, T, mode="ed", eps=0.1, seed=31 + L, slice_tris=tris)
    else:
        F = Fast(L, T, mode="cdt", k0=(3.2 if kind == "ext" else 8.0), seed=41 + L)
    rec = dict(L=L, kind=kind, T=T, trail=[], fails=[])
    for b in range(BLOCKS):
        F.sweeps(SWEEPS // BLOCKS)
        sl = [(n, m) for (_, n, m) in R.slice_readings(F.X, b) if m]
        rate = float(np.polyfit(np.log([x[0] for x in sl]), np.log([x[1] for x in sl]), 1)[0]) if len(sl) > 3 else None
        rec["trail"].append(dict(block=b, tau=float(F.tau()), N0=F.X.N0(), N3=F.X.N3(), rate=rate,
                                 md=float(np.mean([m for _, m in sl])), sizes=[n for n, _ in sl],
                                 hours=(time.time() - t0) / 3600))
        json.dump(rec, open(path, "w"))
    notes = F.check()
    if notes:
        rec["fails"].append(notes[:2])
    rec["spacetime"] = R.spacetime_reading(F.X, 9)
    rec["done"] = True
    json.dump(rec, open(path, "w"))
    return path


def report():
    R_ = {}
    for L, k in JOBS:
        p = os.path.join(OUT, "L%d_%s.json" % (L, k))
        if os.path.exists(p):
            R_[(L, k)] = json.load(open(p))
    L_ = []
    tail = {}
    for (L, k), r in sorted(R_.items()):
        t = r["trail"][-4:]
        tail[(L, k)] = dict(rate=float(np.mean([x["rate"] for x in t if x["rate"]])),
                            md=float(np.mean([x["md"] for x in t])), tau=float(np.mean([x["tau"] for x in t])),
                            st=r.get("spacetime"))
        L_.append("L%d %-11s tau %.3f | slice rate %.3f md %.2f | sizes %d-%d | spacetime %s | blocks %d | fails %s"
                  % (L, k, tail[(L, k)]["tau"], tail[(L, k)]["rate"], tail[(L, k)]["md"],
                     min(t[-1]["sizes"]), max(t[-1]["sizes"]),
                     None if r.get("spacetime") is None else round(r["spacetime"], 3), len(r["trail"]), r["fails"]))
    if len(R_) == len(JOBS):
        ok2 = ok3 = True
        for L in SIZES:
            e = tail[(L, "ext")]
            for s in ("ed_flat", "ed_crowded"):
                d = tail[(L, s)]
                ok2 &= abs(d["rate"] - e["rate"]) <= 0.08 and (d["st"] is None or e["st"] is None
                                                               or abs(d["st"] - e["st"]) <= 0.5)
            a, b = tail[(L, "ed_flat")], tail[(L, "ed_crowded")]
            ok3 &= abs(a["rate"] - b["rate"]) <= 0.08 and (a["st"] is None or b["st"] is None or abs(a["st"] - b["st"]) <= 0.5)
        L_.append("E2 (ED matches the extended phase) %s | E3 (ED's starts agree) %s" % (ok2, ok3))
        L_.append("VERDICT: " + ("in 2+1, ED's conserved totals give what the extended phase gives, with nothing tuned"
                                 if ok2 and ok3 else
                                 "ED's starts disagree - still not settled" if not ok3 else
                                 "ED does not match the extended phase - reported as it reads"))
    text = "\n".join(L_)
    open(os.path.join(HERE, "st3f_ed.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    if "--report" in sys.argv:
        report(); sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for path in p.imap_unordered(do_job, JOBS):
            print("  done", os.path.basename(path), flush=True)
    report()
