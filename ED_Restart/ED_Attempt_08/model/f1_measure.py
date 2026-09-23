"""Road F: measure the tilt on E4's grown slices (D13, D15; note 10).

The slices re-grow exactly - the port's generator is seeded - so these are E4's own slices, not new
ones. Each is placed on the calibration ladder fixed in f1_calibrate.py before any of this ran:

    d=1 -0.013    d=2 -0.280    d=3 -0.627

F1-2, fixed first: a grown slice SUPPORTS a common now if its tilt exponent is at or below the
two-dimensional reference of -0.280; it FAILS if it sits above that, toward one dimension.

Expected results, written down before this run:
  F1-3  the veto slices (sync condition on) sit ABOVE the d=2 reference - they do not support a
        common now - and the controls (sync off) sit at or below it. This is C42's claim, that the
        per-move veto destroys the condition it enforces, and it is what road F exists to test.
  F1-4  every slice yields at least three fitted rungs. If not, the ladder is too short and the
        answer is "not measurable", which is road E's resolution wall again rather than a result.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from p3 import Slice3P
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING
from f1_tilt import tilt_curve

T = 150
F = 0.45
OUT = "f1_runs"
JOBS = [(24, 0, True), (32, 0, True), (52, 0, True), (32, 0, False), (52, 0, False)]


def do_job(job):
    n, seed, use_sync = job
    tag = "n%d_s%d_%s" % (n, seed, "veto" if use_sync else "ctrl")
    path = os.path.join(OUT, tag + ".json")
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    base = json.load(open(os.path.join("e4_runs", "cal_FC_n%d_r0.json" % n), encoding="utf-8"))["strain_median"]
    s_max = F * base if use_sync else None
    M = Slice3P(n)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    pool = round(FLAT_LINKS_PER_EVENT * V0) - M.E
    for t in range(T):
        r, pool, kids, absd = M.tick(1.0, 1.0, pool, s_max=s_max, cap=CEILING)
    ref = json.load(open(os.path.join("e4_runs", "grow_n%d_s%d%s.json"
                                      % (n, seed, "" if use_sync else "_ctrl")), encoding="utf-8"))
    same = (M.V == ref["events"] and M.E == ref["links"])
    A = M.adjacency()[0]
    curves = [tilt_curve(A, s) for s in (0, 1, 2)]
    exps = [c["tilt_exponent"] for c in curves if c["tilt_exponent"] is not None]
    res = dict(n=n, seed=seed, sync=use_sync, matches_run=bool(same), V=M.V, E=M.E,
               rungs=curves[0]["r"], fit_rungs=curves[0]["fit_rungs"], pairs=curves[0]["pairs"],
               tilt=curves[0]["tilt"], exponents=exps,
               exponent=float(np.mean(exps)) if exps else None,
               run_d_s=(ref.get("slice") or {}).get("d_s"),
               run_diameter=(ref.get("slice") or {}).get("diameter"),
               seconds=time.perf_counter() - t0)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, default=str)
    os.replace(tmp, path)
    return path, res["seconds"]


def report():
    cal = json.load(open("f1_calibrate.json", encoding="utf-8"))
    scale, thr = cal["_scale"], float(cal["_threshold"])
    L = ["Road F: the tilt on E4's grown slices", "",
         "  the scale:  d=1 %.3f   d=2 %.3f   d=3 %.3f   | threshold %.3f"
         % (scale["ring (d=1)"], scale["square torus (d=2)"], scale["cube torus (d=3)"], thr), "",
         "  %-16s %8s %9s %10s %9s %8s %s" % ("slice", "V", "run d_s", "exponent", "vs d=2", "rungs", "common now?")]
    for n, seed, use_sync in JOBS:
        p = os.path.join(OUT, "n%d_s%d_%s.json" % (n, seed, "veto" if use_sync else "ctrl"))
        if not os.path.exists(p):
            continue
        r = json.load(open(p, encoding="utf-8"))
        e = r["exponent"]
        if e is None:
            L.append("  %-16s %8d %9s %10s %9s %8s %s"
                     % ("n=%d %s" % (n, "veto" if use_sync else "ctrl"), r["V"],
                        "%.3f" % r["run_d_s"] if r["run_d_s"] else "-", "-", "-",
                        len(r["fit_rungs"]), "NOT MEASURABLE (ladder too short)"))
            continue
        L.append("  %-16s %8d %9s %10.3f %+9.3f %8d %s"
                 % ("n=%d %s" % (n, "veto" if use_sync else "ctrl"), r["V"],
                    "%.3f" % r["run_d_s"] if r["run_d_s"] else "-", e, e - thr,
                    len(r["fit_rungs"]),
                    "SUPPORTS" if e <= thr else "FAILS"))
        if not r["matches_run"]:
            L.append("      (re-grown slice does not match E4's run)")
    text = "\n".join(L)
    with open("f1_measure.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return text


def main(workers):
    os.makedirs(OUT, exist_ok=True)
    t0 = time.perf_counter()
    with Pool(workers) as pool:
        for path, sec in pool.imap_unordered(do_job, JOBS):
            print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec,
                                                    (time.perf_counter() - t0) / 3600), flush=True)
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 3))
