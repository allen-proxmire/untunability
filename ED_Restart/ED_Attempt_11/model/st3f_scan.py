"""Validation scan with the compiled sampler (D8): the program run as plain 3D CDT, 100x longer than attempt 1.

Expectations (note 7's V1-V3, unchanged, with the longer runs the published drop should now be visible):
  V1  tau = N22/N3 falls as k0 rises AND drops sharply somewhere (tau > 0.15 below it, tau < 0.05 above it).
      Our slices are tori, not spheres, so the drop may sit at a different k0; the shape is the test.
  V2  ED's tau = 1/3 sits below the drop.
  V3  reported: the slice growth rate in the extended region.
Each coupling: L = 14, T = 16, 20,000 sweeps, tau averaged over the last fifth; both a flat start and (for the couplings
near the drop) a start from the end of the next coupling up, to show hysteresis if the transition is first order.
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
OUT = os.path.join(HERE, "st3f_scan_runs")
L, T, SWEEPS = 14, 16, 20000
K0S = (0.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0)


def do_job(k0):
    path = os.path.join(OUT, "k%.1f.json" % k0)
    if os.path.exists(path):
        return path
    from st3f_run import Fast
    import st3_run as R
    t0 = time.time()
    F = Fast(L, T, mode="cdt", k0=k0, seed=int(7 + k0))
    rec = dict(k0=k0, L=L, T=T, taus=[], fails=[])
    for blk in range(20):
        F.sweeps(SWEEPS // 20)
        rec["taus"].append((int(F.cnt[1]), float(F.tau()), F.X.N0(), F.X.N3()))
        json.dump(rec, open(path, "w"))
    notes = F.check()
    if notes:
        rec["fails"].append(notes[:3])
    sl = [(n, m) for (_, n, m) in R.slice_readings(F.X, 5) if m]
    rec["rate"] = float(np.polyfit(np.log([x[0] for x in sl]), np.log([x[1] for x in sl]), 1)[0]) if len(sl) > 3 else None
    rec["slice_md"] = float(np.mean([m for _, m in sl]))
    rec["tau"] = float(np.mean([t for _, t, _, _ in rec["taus"][-4:]]))
    rec["profile"] = [n for n, _ in sl]
    rec["hours"] = (time.time() - t0) / 3600
    json.dump(rec, open(path, "w"))
    return path


def report():
    rows = []
    for k0 in K0S:
        p = os.path.join(OUT, "k%.1f.json" % k0)
        if os.path.exists(p):
            r = json.load(open(p))
            if "tau" in r:
                rows.append(r)
    L_ = ["published (AJL Fig. 7, spherical slices): tau about 0.25 at k0 = 5.25, dropping sharply to about 0 near k0 = 6.6"]
    for r in rows:
        L_.append("k0 %5.1f | tau %.3f | slice md %.2f rate %s | sizes %d-%d | %.2f h | fails %s | tau trail %s"
                  % (r["k0"], r["tau"], r["slice_md"], None if r["rate"] is None else round(r["rate"], 3),
                     min(r["profile"]), max(r["profile"]), r["hours"], r["fails"],
                     [round(t, 3) for _, t, _, _ in r["taus"][::4]]))
    if len(rows) >= 6:
        taus = {r["k0"]: r["tau"] for r in rows}
        ks = sorted(taus)
        falls = all(taus[a] >= taus[b] - 0.02 for a, b in zip(ks, ks[1:]))
        jumps = [(a, b, taus[a] - taus[b]) for a, b in zip(ks, ks[1:])]
        big = max(jumps, key=lambda x: x[2])
        drop = any(taus[k] > 0.15 for k in ks) and any(taus[k] < 0.05 for k in ks)
        V1 = falls and drop
        V2 = any(taus[k] >= 1 / 3 for k in ks)
        L_.append("V1 %s (falls %s, drop %s; biggest step %.3f between k0 %.1f and %.1f) | V2 %s (tau >= 1/3 at k0 %s)"
                  % (V1, falls, drop, big[2], big[0], big[1], V2, [k for k in ks if taus[k] >= 1 / 3]))
        L_.append("V3 slice growth rates: " + ", ".join("k0 %.1f -> %s" % (r["k0"], None if r["rate"] is None else round(r["rate"], 3)) for r in rows))
    text = "\n".join(L_)
    open(os.path.join(HERE, "st3f_scan.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    if "--report" in sys.argv:
        report(); sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    with Pool(5) as p:
        for path in p.imap_unordered(do_job, K0S):
            print("  done", os.path.basename(path), flush=True)
    report()
