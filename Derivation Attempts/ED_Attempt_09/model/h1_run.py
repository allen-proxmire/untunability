"""H1: grow with the conditions only, and check the slices against the conditions (note 2; D3).

Growth keeps ED's two parts built as conditions - the conserved link budget and the ceiling of 60
neighbours - and drops the three built as local costs or vetoes: no commitment cost (alpha = 0), no
curvature cost (lambda = 0), no sync veto. This is attempt 7's setting D, never measured at size.

Readings, all calibrated on objects with a known answer before any of this ran:
  - the fitted spectral dimension and mass dimension (attempt 7's readings; flat 3.0 / 2.66-2.85)
  - the tilt for a common now (A8 f1_tilt; threshold -0.280, the two-dimensional reference)
  - Ollivier curvature, the direct reading of 'curvature bounded below' (h1_calibrate; threshold -0.250)
  - the spectral dimension at every distance (A8 p3_dscurve), seed 0 at n = 32 and 52

Expected results, written down before this run (note 2, C5):
  H1-3  structure and both budgets exact; no run dies, runs away or densifies.
  H1-4  density at flat: mean degree within 1 of the flat slice's 14.0 (A7 setting D read 14.3).
  H1-5  THE HONEST EXPECTATION: the slices do NOT meet the conditions - compact rather than flat, with
        a common now failing (tilt above -0.280) - because with every cost removed the shape is left
        to entropy. If so, H2 is isolated as the one question left.
Exit rule (note 2): slices meet the conditions -> the costs were the problem; they do not -> ED's
conditions alone don't beat the counting, H2 isolated; too small to measure -> the resolution wall.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from p3 import Slice3P                                        # noqa: E402
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING      # noqa: E402

SIZES = (24, 32, 52)
SEEDS = (0, 1)
T = 150
TETS_PER_EVENT_CAP = 20
CURVE = {32: 2000, 52: 2000}          # scale-resolved d_s: seed 0 only, walk steps
OUT = "h1_runs"
WORKERS = {24: 3, 32: 3, 52: 2}


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def do_job(job):
    n, s = job
    path = os.path.join(OUT, "n%d_s%d.json" % (n, s))
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    M = Slice3P(n)
    M.seed(s)
    V0 = M.V
    rng = np.random.default_rng(s)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - M.E
    ok = dict(structure=True, budget=True, link=True, cap=True)
    status = "survived"
    for t in range(1, T + 1):
        if M.T / max(M.V, 1) > TETS_PER_EVENT_CAP:
            status = "densified"
            break
        r, pool, kids, absd = M.tick(0.0, 0.0, pool, s_max=None, cap=CEILING)
        if M.check():
            ok["structure"] = False
            status = "structure failure"
            break
        if abs(float(M.S.b[M.vertices()].sum()) - V0) > 1e-9 * V0:
            ok["budget"] = False
        if M.E + pool != BL:
            ok["link"] = False
        if not (V0 / 10 <= r["size"] <= 10 * V0):
            status = "died" if r["size"] < V0 / 10 else "ran away"
            break
    grow_s = time.perf_counter() - t0
    res = dict(n=n, seed=s, V0=V0, status=status, ok=ok, events=M.V, links=M.E,
               events_vs_start=M.V / V0, mean_degree=2 * M.E / max(M.V, 1),
               max_degree=max(M.degree(v) for v in M.vertices()), grow_seconds=grow_s)
    if status == "survived":
        from p3_readings import slice_readings
        from f1_tilt import tilt_curve
        from h1_curvature import curvature_sample
        A = M.adjacency()[0]
        sl = slice_readings(M, s)
        res["slice"] = {k: sl[k] for k in ("d_H", "d_s", "diameter", "mean_distance", "r_lo", "r_max",
                                            "small_world", "mean_degree", "max_degree")}
        tc = [tilt_curve(A, rs) for rs in (0, 1, 2)]
        ex = [c["tilt_exponent"] for c in tc if c["tilt_exponent"] is not None]
        res["tilt"] = dict(exponent=float(np.mean(ex)) if ex else None, exponents=ex,
                           rungs=tc[0]["r"], fit_rungs=tc[0]["fit_rungs"], values=tc[0]["tilt"])
        res["curvature"] = curvature_sample(A, s)
        if s == 0 and n in CURVE:
            from p3_dscurve import d_s_curve
            res["ds_curve"] = d_s_curve(A, s, t_cap=CURVE[n])
    res["seconds"] = time.perf_counter() - t0
    dump(path, res)
    return path, res["seconds"]


def report():
    cal_t = json.load(open(os.path.join(HERE, "..", "..", "ED_Attempt_08", "model", "f1_calibrate.json"), encoding="utf-8"))
    cal_k = json.load(open("h1_calibrate.json", encoding="utf-8"))
    tt, kt = float(cal_t["_threshold"]), float(cal_k["_threshold"])
    f = lambda x, d=3: ("%.*f" % (d, x)) if isinstance(x, (int, float)) else "-"
    L = ["H1: growth with the conditions only (budget + ceiling; no costs, no veto)", "",
         "  thresholds fixed before growth: common now needs tilt <= %.3f ; curvature bounded below needs median >= %.3f" % (tt, kt),
         "  flat slice at n=24/32/52: d_s 3.05/3.02/3.01, d_H 2.66/2.74/2.85, diameter 18/24/39, mean degree 14.0", "",
         "  %-8s %-8s %7s %7s %6s %7s %7s %8s %9s %11s" % ("slice", "status", "ev/V0", "meandeg", "maxdeg",
                                                         "diam", "d_H", "d_s", "tilt", "curv med")]
    for n in SIZES:
        for s in SEEDS:
            p = os.path.join(OUT, "n%d_s%d.json" % (n, s))
            if not os.path.exists(p):
                continue
            r = json.load(open(p, encoding="utf-8"))
            sl, ti, cu = r.get("slice") or {}, r.get("tilt") or {}, r.get("curvature") or {}
            e, km = ti.get("exponent"), cu.get("median")
            L.append("  n=%-2d s%d  %-8s %7s %7s %6s %7s %7s %8s %9s %11s" % (
                n, s, r["status"][:8], f(r["events_vs_start"]), f(r["mean_degree"], 2), r["max_degree"],
                sl.get("diameter"), f(sl.get("d_H")), f(sl.get("d_s")),
                (f(e) + (" ok" if e is not None and e <= tt else " X" if e is not None else "")),
                (f(km) + (" ok" if km is not None and km >= kt else " X" if km is not None else ""))))
            if "ds_curve" in r:
                c = r["ds_curve"]
                L.append("        d_s by distance: " + "  ".join("r%.1f:%.2f" % (rr, d) for rr, d in
                                                                zip(c["radius"][::3], c["d_s"][::3])))
    text = "\n".join(L)
    with open("h1_run.txt", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.perf_counter()
    for n in SIZES:
        jobs = [(n, s) for s in SEEDS]
        with Pool(WORKERS[n]) as pool:
            for path, sec in pool.imap_unordered(do_job, jobs):
                print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec,
                                                        (time.perf_counter() - t0) / 3600), flush=True)
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
