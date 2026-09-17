"""C3b runs (note 16, C61; D22, D23, D24; IMPLEMENTATION_NOTES.md, C3b section incl. ball-growth readings).

Expected results, written down before the first run (note 16):
  E1  every stand-in connected; F degree exactly 6; FR mean degree in [13, 15]; B exactly one link per
      tree edge; H exactly 6-regular and simple; Cr mean degree within +-10% of sqrt(N).
  E2  sync: neck tilt ratio (pooled RMS over seeds of the largest single-link tick difference, largest
      size over smallest) >= 3 for B, <= 1.5 for F, FR, H, Cr.
  E3  commitment: degree ratio (mean degree, largest size over smallest) >= 3 for Cr, <= 1.2 for F, FR, B, H.
  E4  curvature proxy: exponential-growth flag (readings v2 small_world, majority of seeds) at the largest
      size true for H, false for F, FR, B; Cr reported (a flag allowed).
  Extra flags on other bad shapes are allowed and reported (C3b-Q4).
Exit rule (note 16):
  E1 fails: code or construction bug (recorded).
  No meaning misses its own shape (sync-B, commitment-Cr, curvature-H) and none flags F or FR:
    "Each bad 3D shape is flagged by one existing ED meaning, and a flat 3D slice by none: consistent,
    not derived." Then spec 3D growth (C3c).
  A meaning misses its shape: "<meaning> doesn't flag <shape>"; take stock of road C3.
  A meaning flags F or FR: "<meaning> flags a flat 3D slice"; take stock of road C3.
Resumable: one JSON per job in c3b_runs/.
"""
import json
import math
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from c3b import KINDS, SIZES, MAKERS, connected, sync_steady_state, readings, degree_stats

SEEDS = (0, 1, 2)
OUT = "c3b_runs"


def do_job(job):
    kind, N, s = job
    path = os.path.join(OUT, f"{kind}_N{N}_s{s}.json")
    if os.path.exists(path):
        return path
    t0 = time.perf_counter()
    A, info = MAKERS[kind](N, s)
    sync = sync_steady_state(A, s)
    res = dict(kind=kind, N=int(A.shape[0]), seed=s, connected=bool(connected(A)), redraws=info["redraws"],
               degrees=degree_stats(A), links=int(A.nnz // 2), sync=sync, readings=readings(A, s))
    if kind == "B":
        nb = 64
        necks = info["necks"]
        rows, cols = A.nonzero()
        inter = int(np.sum((rows < cols) & (rows // nb != cols // nb)))
        res["tree_edges"], res["blocks"], res["inter_block_links"] = info["tree_edges"], info["blocks"], inter
        res["necks_present"] = bool(all(A[x, y] == 1 for x, y in necks))
        u, v = sync["argmax_edge"]
        res["max_on_neck"] = bool(u // nb != v // nb)
    res["seconds"] = time.perf_counter() - t0
    with open(path, "w", encoding="utf-8") as f:
        json.dump(res, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    return path


def analyse():
    R = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            r = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
            R[(r["kind"], r["N"], r["seed"])] = r
    lines = []
    e1, notes = True, []
    for (k, N, s), r in R.items():
        d = r["degrees"]
        ok = r["connected"]
        if k == "F":
            ok &= d["min_degree"] == 6 and d["max_degree"] == 6
        elif k == "FR":
            ok &= 13 <= d["mean_degree"] <= 15
        elif k == "B":
            ok &= r["tree_edges"] == r["blocks"] - 1 and r["inter_block_links"] == r["tree_edges"] and r["necks_present"]
        elif k == "H":
            ok &= d["min_degree"] == 6 and d["max_degree"] == 6 and r["links"] == 3 * N
        elif k == "Cr":
            ok &= abs(d["mean_degree"] / math.sqrt(N) - 1) <= 0.10
        ok &= r["sync"]["residual"] < 1e-8
        if not ok:
            e1 = False
            notes.append(f"{k} N={N} s={s}")
    tilt, degr, flag = {}, {}, {}
    for k in KINDS:
        ns = SIZES[k]
        pooled = [math.sqrt(np.mean([R[(k, N, s)]["sync"]["max_link_diff"] ** 2 for s in SEEDS])) for N in ns]
        Wp = [math.sqrt(np.mean([R[(k, N, s)]["sync"]["W"] ** 2 for s in SEEDS])) for N in ns]
        md = [float(np.mean([R[(k, N, s)]["degrees"]["mean_degree"] for s in SEEDS])) for N in ns]
        tilt[k] = pooled[-1] / pooled[0]
        degr[k] = md[-1] / md[0]
        flags = [R[(k, ns[-1], s)]["readings"]["small_world"] for s in SEEDS]
        flag[k] = sum(flags) >= 2
        wexp = float(np.polyfit(np.log(ns), np.log(Wp), 1)[0])
        dH = [R[(k, ns[-1], s)]["readings"]["d_H"] for s in SEEDS]
        line = (f"{k}: pooled largest link difference {', '.join(f'{x:.3f}' for x in pooled)} at N={ns} -> neck tilt ratio {tilt[k]:.2f}; "
                f"pooled wobble {', '.join(f'{x:.3f}' for x in Wp)} (exponent in N {wexp:.3f}); mean degree {', '.join(f'{x:.2f}' for x in md)} "
                f"-> ratio {degr[k]:.2f}; max degree at largest {max(R[(k, ns[-1], s)]['degrees']['max_degree'] for s in SEEDS)}; "
                f"exponential-growth flag at largest {flags} -> {flag[k]}; d_H at largest {dH}")
        if k == "B":
            share = [sum(R[(k, N, s)]["max_on_neck"] for s in SEEDS) for N in ns]
            line += f"; largest difference on a neck link (seeds of 3) {share}"
        lines.append(line)
    e2 = tilt["B"] >= 3 and all(tilt[k] <= 1.5 for k in ("F", "FR", "H", "Cr"))
    e3 = degr["Cr"] >= 3 and all(degr[k] <= 1.2 for k in ("F", "FR", "B", "H"))
    e4 = flag["H"] and not any(flag[k] for k in ("F", "FR", "B"))
    for name, v in (("E1 construction", e1), ("E2 sync", e2), ("E3 commitment", e3), ("E4 curvature proxy", e4)):
        lines.append(f"{name}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if notes:
        lines.append("E1 notes: " + "; ".join(notes))
    sig = {"sync": {k: tilt[k] > 1.5 if k != "B" else tilt[k] >= 3 for k in KINDS},
           "commitment": {k: degr[k] > 1.2 if k != "Cr" else degr[k] >= 3 for k in KINDS},
           "curvature": {k: flag[k] for k in KINDS}}
    own = {"sync": "B", "commitment": "Cr", "curvature": "H"}
    names = {"B": "branched", "Cr": "crumpled", "H": "hyperbolic"}
    misses = [f"{m} doesn't flag {names[own[m]]}" for m in own if not sig[m][own[m]]]
    flat_flags = [f"{m} flags a flat 3D slice ({k})" for m in own for k in ("F", "FR") if sig[m][k]]
    extra = [f"{m} also flags {names[k]}" for m in own for k in ("B", "Cr", "H") if k != own[m] and sig[m][k]]
    lines.append("extra flags on other bad shapes (allowed): " + ("; ".join(extra) if extra else "none"))
    if not e1:
        verdict = "E1 failed: code or construction bug (recorded)."
    elif not misses and not flat_flags:
        verdict = ("PASS: Each bad 3D shape is flagged by one existing ED meaning, and a flat 3D slice by none: "
                   "consistent, not derived. Then spec 3D growth (C3c).")
    else:
        verdict = "; ".join(misses + flat_flags) + ". Take stock of road C3."
    lines.append("EXIT: " + verdict)
    return lines


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [(k, N, s) for k in KINDS for N in SIZES[k] for s in SEEDS]
    t0 = time.perf_counter()
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as pool:
        for i, p in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print(f"[{i}/{len(jobs)}] {os.path.basename(p)} (elapsed {time.perf_counter()-t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time {time.perf_counter()-t0:.0f} s")
    print("\n".join(lines))
    open("c3b_run1.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
