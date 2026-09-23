"""The 2+1 test runs (note 6, C9; expectations P0-P3 and outcomes are in note 6, fixed before any code).

Calibration first (P1): flat product stack and crowded stack (every slice the same randomly rewired torus), same totals,
at L = 10 and 14; spacetime reading must differ by >= 0.5 at both sizes, or the runs do not count (sizes revised, recorded).
Runs: L = 10 and 14, T = 16, starts 'flat' and 'crowded'. Warm-up tunes the linear counterweights (then frozen); readings
every 50 sweeps (sweep = N3 steps) on a fixed schedule, totals within a few events of ED's values (revised after the
independent review: reading at the first exact hit is biased); stop when settled (last third of slice mean-distance readings within 5
per cent, at least 300 sweeps) or at 2 hours. Checks (P0) at every reading: engine structure, every piece a layer piece,
every slice a closed surface, N22 tracking.
Readings: spacetime ball growth (A9's method, c3b.readings) on the whole spacetime graph; each slice's mean distance
against its size (log-log slope pooled over slices and both sizes: flat 2D = 0.5); the slice-size profile n(t).
"""
import json
import math
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
OUT = os.path.join(HERE, "st3_runs")
T = 16
SIZES = (28, 40)   # REVISION (recorded before any run): at 10/14 and at 20 the spacetime reading is undefined (too small across);
                   # calibration_L10_14.json and calibration_L20_28.json kept. At 28 and 40 both readings separate flat from crowded.
MIN_SWEEPS, EVERY, HOURS = 300, 50, 4.0   # REVISION: 4 h cap (a size-40 sweep is about 37 s)


def build(L, start):
    from st3 import Spacetime, random_torus_tris
    tris = None if start == "flat" else random_torus_tris(L)
    # REVISION after run 1 (st3_runs_invalid1/): the warm-up tuning of the linear counterweights overshot (mu 43-60),
    # freezing the flat runs (no event or (2,2) change could be accepted) and pushing the crowded runs about 9 per cent
    # off ED's totals. Now: no tuning (mu = 0) and a firmer quadratic hold eps = 0.1, which keeps the totals within a
    # few dozen events of ED's values; the deviation is recorded at every reading.
    return Spacetime(L, T, eps=0.1, seed=11 + L, slice_tris=tris)


def spacetime_reading(X, seed):
    from c3b import readings
    return readings(X.M.adjacency()[0], seed).get("d_H")


def slice_readings(X, seed):
    from scipy.sparse.csgraph import shortest_path
    import scipy.sparse as sp
    rng = np.random.default_rng(seed)
    sl = X.slices()
    E = X.M.edges()
    out = []
    for t, vs in sl.items():
        if len(vs) < 4:
            out.append((t, len(vs), None))
            continue
        idx = {v: i for i, v in enumerate(vs)}
        rows, cols = [], []
        for a, b in E:
            a, b = int(a), int(b)
            if a in idx and b in idx:
                rows += [idx[a], idx[b]]
                cols += [idx[b], idx[a]]
        A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(vs), len(vs)))
        src = rng.choice(len(vs), size=min(40, len(vs)), replace=False)
        d = shortest_path(A, unweighted=True, indices=src)
        out.append((t, len(vs), float(d[np.isfinite(d)].mean())))
    return out


def reading(X, seed):
    sr = slice_readings(X, seed)
    mds = [m for _, _, m in sr if m]
    return dict(spacetime=spacetime_reading(X, seed), slice_md=float(np.mean(mds)),
                profile=[n for _, n, _ in sr], slices=sr, N0=X.N0(), N22=X.N22_cur, N3=X.N3())


def calibrate():
    path = os.path.join(OUT, "calibration.json")
    if os.path.exists(path):
        return json.load(open(path))
    res = {}
    for L in SIZES:
        for start in ("flat", "crowded"):
            X = build(L, start)
            res["%s_%d" % (start, L)] = dict(check=X.check(), **reading(X, 1))
    for L in SIZES:
        res["gap_%d" % L] = res["crowded_%d" % L]["spacetime"] - res["flat_%d" % L]["spacetime"]
    res["P1"] = all(res["gap_%d" % L] >= 0.5 for L in SIZES)
    json.dump(res, open(path, "w"), indent=1)
    return res


def do_job(job):
    L, start = job
    path = os.path.join(OUT, "L%d_%s.json" % (L, start))
    t0 = time.perf_counter()
    X = build(L, start)
    rec = dict(L=L, start=start, T=T, N0s=X.N0s, N22s=X.N22s, mu0=X.mu0, mu22=X.mu22, readings=[], fails=[])
    rec["readings"].append(dict(sweep=0, **reading(X, 0)))
    sw = 0
    while True:
        for _ in range(EVERY):
            for _ in range(X.N3()):
                X.step()
            sw += 1
        # REVISION (review): read on a fixed schedule, not at the first exact hit (first-hit sampling is biased);
        # the totals sit within a few events of ED's values under the soft hold, and their deviation is recorded
        exact = X.N0() == X.N0s and X.N22_cur == X.N22s
        notes = X.check()
        if notes:
            rec["fails"].append((sw, notes[:3]))
            break
        r = reading(X, sw)
        r.update(sweep=sw, exact=exact, dN0=X.N0() - X.N0s, dN22=X.N22_cur - X.N22s, acceptance=X.acc / X.tried, hours=(time.perf_counter() - t0) / 3600)
        rec["readings"].append(r)
        json.dump(rec, open(path, "w"))
        rd = [x["slice_md"] for x in rec["readings"][1:]]
        k = max(1, len(rd) // 3)
        tail = rd[-k:]
        settled = sw >= MIN_SWEEPS and (max(tail) - min(tail)) / np.mean(tail) <= 0.05
        if settled or r["hours"] >= HOURS:
            rec["settled"] = bool(settled)
            break
    rec["done"] = True
    rec["why"] = dict(sorted(X.why.items(), key=lambda kv: -kv[1])[:12])
    json.dump(rec, open(path, "w"))
    return path


def report():
    cal = json.load(open(os.path.join(OUT, "calibration.json")))
    L_ = ["CALIBRATION (P1 %s): " % cal["P1"] + "; ".join(
        "%s_%d spacetime %.3f slice md %.3f" % (s, L, cal["%s_%d" % (s, L)]["spacetime"], cal["%s_%d" % (s, L)]["slice_md"])
        for L in SIZES for s in ("flat", "crowded")) + " | gaps %s" % [round(cal["gap_%d" % L], 3) for L in SIZES]]
    R = {}
    for L in SIZES:
        for s in ("flat", "crowded"):
            p = os.path.join(OUT, "L%d_%s.json" % (L, s))
            if os.path.exists(p):
                R[(L, s)] = json.load(open(p))
    final = {}
    for (L, s), r in R.items():
        rd = r["readings"]
        k = max(1, (len(rd) - 1) // 3)
        tail = rd[-k:]
        st = float(np.mean([x["spacetime"] for x in tail if x["spacetime"]]))
        pts = [(n, m) for x in tail for (_, n, m) in x["slices"] if m]
        final[(L, s)] = dict(spacetime=st, pts=pts, md=float(np.mean([x["slice_md"] for x in tail])))
        L_.append("L%d %-7s: spacetime %.3f -> %.3f | slice md %.3f -> %.3f | profile last %s | sweeps %d settled %s | "
                  "mu0 %.2f mu22 %.2f | acc %.3f | fails %s" % (
                      L, s, rd[0]["spacetime"], st, rd[0]["slice_md"], final[(L, s)]["md"], rd[-1]["profile"],
                      rd[-1]["sweep"], r.get("settled"), r["mu0"], r["mu22"], rd[-1].get("acceptance", 0), r["fails"]))
    if len(final) == 4:
        rates = {}
        for s in ("flat", "crowded"):
            pts = final[(SIZES[0], s)]["pts"] + final[(SIZES[1], s)]["pts"]
            x = np.log([p[0] for p in pts])
            y = np.log([p[1] for p in pts])
            rates[s] = float(np.polyfit(x, y, 1)[0])
        calflat = {L: cal["flat_%d" % L]["spacetime"] for L in SIZES}
        P2 = all(abs(final[(L, "flat")]["spacetime"] - calflat[L]) <= 0.5 and
                 abs(final[(L, "crowded")]["spacetime"] - calflat[L]) <= 0.5 for L in SIZES) and \
            all(abs(rates[s] - 0.5) <= 0.1 for s in rates)
        P3 = all(abs(final[(L, "flat")]["spacetime"] - final[(L, "crowded")]["spacetime"]) <= 0.3 for L in SIZES) and \
            abs(rates["flat"] - rates["crowded"]) <= 0.1
        L_.append("slice growth rate (flat 2D 0.5): flat start %.3f, crowded start %.3f" % (rates["flat"], rates["crowded"]))
        fails = any(r["fails"] for r in R.values())
        if fails:
            v = "a check failed - code problem"
        elif not cal["P1"]:
            v = "calibration failed (P1) - runs do not count"
        elif P2 and P3:
            v = "SPREAD-OUT from both starts: in 2+1, ED's rules give extended spacetime with nothing tuned"
        elif not P3:
            v = "starts disagree: not settled - take stock of the program"
        else:
            v = "both starts agree but not spread-out: note 5's reading wrong somewhere - take stock"
        L_.append("P2 %s P3 %s | VERDICT: %s" % (P2, P3, v))
    text = "\n".join(L_)
    open(os.path.join(HERE, "st3_run.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
        sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    cal = calibrate()
    print(json.dumps({k: v for k, v in cal.items() if k.startswith(("gap", "P1"))}), flush=True)
    if "--calibrate-only" in sys.argv:
        sys.exit(0)
    jobs = [(L, s) for L in SIZES for s in ("flat", "crowded")]
    with Pool(4) as p:
        for path in p.imap_unordered(do_job, jobs):
            print("  done", path, flush=True)
    report()
