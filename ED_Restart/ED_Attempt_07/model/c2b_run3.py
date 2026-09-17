"""C2b run 3: revise and retest (note 10, C36; D14).

Revisions (recorded), on top of run 2's (sigma = 0.0005, 10 seeds):
  (i)   E2-E4 (and the separation check) read with the pooled measure: exponent
        beta = slope of ln sqrt(mean over seeds of W^2) against ln n; tilt ratio
        from the same pooled W. Wobbles add as squares (C35).
  (ii)  E1's random-slice degree range is 10 +- 3*sqrt(20/N).
  (iii) Random-slice seed 1000*(seed + 1) + redraw (redraw < 1000), so no two
        seeds share a slice; duplicates are still reported.
Fresh seeds 13-22. Everything else unchanged from note 9: sizes, update, K,
readings, the E2-E5 ranges, E5's measure (median of per-seed slopes), the exit
rule, the tilt reading (reported only). The per-seed median measure is reported
alongside.

Expected results, written down before the first run:
  E1  every random slice connected with mean degree in 10 +- 3*sqrt(20/N);
      grids exact (degree 2d). Every persistent run: largest neighbour
      difference < 0.3, rate spread < 0.01*sigma, W change < 2% between 2T/3 and T.
  E2  grids, persistent: pooled beta in [1.35, 1.65] (d = 1), [0.85, 1.15]
      (d = 2), [0.35, 0.65] (d = 3).
  E3  random slices, persistent: pooled beta in [1.3, 1.7], [0.8, 1.2], [0.3, 0.7].
  E4  persistent pooled tilt ratio (largest n over smallest n) > 1.5 (d = 1),
      in [0.8, 1.25] (d = 2), < 0.67 (d = 3), for G and R.
  E5  control, fresh each tick (G and R): median per-seed beta in [0.35, 0.65]
      (d = 1), [-0.1, 0.3] (d = 2), [-0.2, 0.15] (d = 3); tilt ratio < 0.67 in
      every d.
  Tilt against distance within a slice (D11): reported only. Expected shapes:
  persistent d=1 flat in r, d=2 falling slowly, d=3 about r^-0.5; control d=1
  about r^-0.5, d=2 and d=3 about r^-1.
Exit rule (note 9, with the revised readings):
  E1-E4 as expected: "A common now needs slice dimension >= 3 without a ratio in
    ED's causal pattern; with commitment's fewest directions and whole numbers,
    three: consistent, not derived."
  E2 met, E3 not: "The floor is seen on grids but not on ED's random slices";
    take stock of road C.
  E2 not met: calibration or regime problem (recorded).
  Pooled exponents don't separate (gaps < 0.3 in both G and R): "The floor
    isn't seen in ED's causal pattern"; take stock of road C.
  E1-E3 met, E4 not: not covered; recorded, back to Allen.
  E5 not as expected: recorded, not blocking.
  E1 fails: code bug or regime problem (recorded).
Resumable: one JSON per run in c2b_runs3/; finished runs are skipped.
"""
import json
import math
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from c2b import SIZES, grid_slice, random_slice, simulate

SIGMA = 0.0005
SEEDS = list(range(13, 23))
OUT = "c2b_runs3"


def job_name(d, n, kind, fresh, seed):
    return f"d{d}_n{n}_{kind}_{'fresh' if fresh else 'persistent'}_s{seed}"


def do_job(job):
    d, n, kind, fresh, seed = job
    path = os.path.join(OUT, job_name(*job) + ".json")
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    sl = grid_slice(d, n) if kind == "G" else random_slice(d, n, seed, max_redraws=1000, scheme="v2")
    res = simulate(sl, seed, fresh, sigma=SIGMA)
    res["slice_seed"] = None if kind == "G" else 1000 * (seed + 1) + sl["redraws"]
    res["seconds"] = time.perf_counter() - t0
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f)
    os.replace(tmp, path)
    return path, res["seconds"]


def slope(x, y):
    return float(np.polyfit(np.log(np.asarray(x, float)), np.log(np.asarray(y, float)), 1)[0])


def analyse():
    runs = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            r = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
            runs[(r["d"], r["n"], r["kind"], r["fresh"], r["seed"])] = r
    lines, e1_notes = [], []
    e1 = True
    for key, r in runs.items():
        d, N = r["d"], r["N"]
        if r["kind"] == "G" and abs(r["mean_degree"] - 2 * d) > 1e-12:
            e1 = False; e1_notes.append(f"grid degree {key}")
        if r["kind"] == "R" and abs(r["mean_degree"] - 10) > 3 * math.sqrt(20 / N):
            e1 = False; e1_notes.append(f"random degree {r['mean_degree']:.2f} (limit +-{3*math.sqrt(20/N):.2f}) {key}")
        if not r["fresh"]:
            if r["max_neighbour_diff"] >= 0.3:
                e1 = False; e1_notes.append(f"max neighbour diff {r['max_neighbour_diff']:.3f} {key}")
            if r["rate_spread"] >= 0.01 * SIGMA:
                e1 = False; e1_notes.append(f"rate spread {r['rate_spread']:.2e} {key}")
            if r["W_change"] >= 0.02:
                e1 = False; e1_notes.append(f"W change {r['W_change']:.3f} {key}")
    pb, ptr, mb, mtr, tslope = {}, {}, {}, {}, {}
    for fresh in (False, True):
        for kind in ("G", "R"):
            for d in (1, 2, 3):
                ns = SIZES[d]
                Wp = [math.sqrt(np.mean([runs[(d, n, kind, fresh, s)]["W"] ** 2 for s in SEEDS])) for n in ns]
                k = (fresh, kind, d)
                pb[k] = slope(ns, Wp)
                ptr[k] = (Wp[-1] / ns[-1]) / (Wp[0] / ns[0])
                bs, trs = [], []
                for s in SEEDS:
                    W = [runs[(d, n, kind, fresh, s)]["W"] for n in ns]
                    bs.append(slope(ns, W))
                    trs.append((W[-1] / ns[-1]) / (W[0] / ns[0]))
                mb[k], mtr[k] = float(np.median(bs)), float(np.median(trs))
                sls = []
                for s in SEEDS:
                    tr = {int(a): v for a, v in runs[(d, ns[-1], kind, fresh, s)]["tilt_r"].items()}
                    rs = sorted(tr)
                    rs = [a for a in rs if a <= ns[-1] // 4] if kind == "G" else rs[:-1]
                    if len(rs) >= 2:
                        sls.append(slope(rs, [tr[a] for a in rs]))
                tslope[k] = float(np.median(sls)) if sls else float("nan")
                redraws = sum(runs[(d, n, kind, fresh, s)]["redraws"] for n in ns for s in SEEDS)
                extra = ""
                if not fresh:
                    md = max(runs[(d, n, kind, fresh, s)]["max_neighbour_diff"] for n in ns for s in SEEDS)
                    rsp = max(runs[(d, n, kind, fresh, s)]["rate_spread"] for n in ns for s in SEEDS)
                    wc = max(runs[(d, n, kind, fresh, s)]["W_change"] for n in ns for s in SEEDS)
                    extra = f"; max neighbour diff {md:.3f}, max rate spread {rsp/SIGMA:.1e} sigma, max W change {wc:.4f}"
                lines.append(f"{'fresh     ' if fresh else 'persistent'} {kind} d={d}: pooled W {', '.join(f'{w:.4g}' for w in Wp)} at n={ns}; "
                             f"pooled beta {pb[k]:.3f}, pooled tilt ratio {ptr[k]:.3f}; median per-seed beta {mb[k]:.3f} "
                             f"(sd {np.std(bs, ddof=1):.3f}), median tilt ratio {mtr[k]:.3f}; within-slice tilt slope {tslope[k]:.3f}; redraws {redraws}{extra}")
    inr = lambda v, ab: ab[0] <= v <= ab[1]
    rg = {"G": {1: (1.35, 1.65), 2: (0.85, 1.15), 3: (0.35, 0.65)}, "R": {1: (1.3, 1.7), 2: (0.8, 1.2), 3: (0.3, 0.7)}}
    e2 = all(inr(pb[(False, "G", d)], rg["G"][d]) for d in (1, 2, 3))
    e3 = all(inr(pb[(False, "R", d)], rg["R"][d]) for d in (1, 2, 3))
    e4 = all(ptr[(False, k, 1)] > 1.5 and 0.8 <= ptr[(False, k, 2)] <= 1.25 and ptr[(False, k, 3)] < 0.67 for k in ("G", "R"))
    ctl = {1: (0.35, 0.65), 2: (-0.1, 0.3), 3: (-0.2, 0.15)}
    e5 = all(inr(mb[(True, k, d)], ctl[d]) and mtr[(True, k, d)] < 0.67 for k in ("G", "R") for d in (1, 2, 3))
    sep = {k: (pb[(False, k, 1)] - pb[(False, k, 2)] >= 0.3 and pb[(False, k, 2)] - pb[(False, k, 3)] >= 0.3) for k in ("G", "R")}
    ss = {}
    for rr in runs.values():
        if rr.get("slice_seed") is not None:
            ss.setdefault((rr["d"], rr["n"], rr["slice_seed"]), set()).add(rr["seed"])
    dup = {str(k): sorted(v) for k, v in ss.items() if len(v) > 1}
    for name, v in (("E1 structure and regime", e1), ("E2 grids persistent pooled exponents", e2),
                    ("E3 random slices persistent pooled exponents", e3), ("E4 persistent pooled tilt ratios", e4),
                    ("E5 fresh-each-tick control", e5)):
        lines.append(f"{name}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if e1_notes:
        lines.append("E1 notes: " + "; ".join(e1_notes[:20]))
    lines.append(f"random-slice seed duplicates at the same (d, n): {dup if dup else 'none'}")
    lines.append(f"pooled exponents separate: G {sep['G']}, R {sep['R']}")
    if not e1:
        verdict = "E1 failed: code bug or regime problem (recorded)."
    elif not e2:
        verdict = "E2 not met: calibration or regime problem (recorded)."
    elif not sep["G"] and not sep["R"]:
        verdict = "The floor isn't seen in ED's causal pattern; take stock of road C."
    elif not e3:
        verdict = "The floor is seen on grids but not on ED's random slices; take stock of road C."
    elif e4:
        verdict = ("PASS: A common now needs slice dimension >= 3 without a ratio in ED's causal pattern; "
                   "with commitment's fewest directions and whole numbers, three: consistent, not derived.")
    else:
        verdict = "E1-E3 met but E4 not: not covered by the exit rule; recorded, back to Allen."
    lines.append("EXIT: " + verdict + (" (E5 not as expected: recorded, not blocking.)" if not e5 else ""))
    return lines


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [(d, n, kind, fresh, s) for d in (1, 2, 3) for n in SIZES[d] for kind in ("G", "R")
            for fresh in (False, True) for s in SEEDS]
    jobs.sort(key=lambda j: -(j[1] ** j[0]) * (j[1] ** 2))
    t0 = time.perf_counter()
    done = 0
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as pool:
        for path, sec in pool.imap_unordered(do_job, jobs):
            done += 1
            print(f"[{done}/{len(jobs)}] {os.path.basename(path)} {sec:.0f} s (elapsed {time.perf_counter()-t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time this session {time.perf_counter()-t0:.0f} s")
    print("\n".join(lines))
    with open("c2b_run3.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
