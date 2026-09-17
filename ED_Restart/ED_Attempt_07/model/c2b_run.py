"""C2b runs (note 9, C27; D10, D11, D12; IMPLEMENTATION_NOTES.md, C2b section).

Expected results, written down before the first run (note 9):
  E1  every random slice connected with mean degree in [9, 11]; grids exact
      (degree 2d). Every persistent run: largest neighbour difference < 0.3,
      rate spread < 0.01*sigma, W change < 2% between 2T/3 and T.
  E2  grids, persistent: median wobble exponent beta in [1.35, 1.65] (d = 1),
      [0.85, 1.15] (d = 2), [0.35, 0.65] (d = 3).
  E3  random slices, persistent: median beta in [1.3, 1.7], [0.8, 1.2], [0.3, 0.7].
  E4  persistent tilt ratio (tilt W/n at largest n over smallest n, median of
      seeds) > 1.5 (d = 1), in [0.8, 1.25] (d = 2), < 0.67 (d = 3), for G and R.
  E5  control, fresh each tick (G and R): median beta in [0.35, 0.65] (d = 1),
      [-0.1, 0.3] (d = 2), [-0.2, 0.15] (d = 3); tilt ratio < 0.67 in every d.
  Tilt against distance within a slice (D11): reported only, outside the exit
  rule. Expected shapes: persistent d=1 flat in r, d=2 falling slowly, d=3
  about r^-0.5; control d=1 about r^-0.5, d=2 and d=3 about r^-1.
Exit rule (note 9):
  E1-E4 as expected: "A common now needs slice dimension >= 3 without a ratio in
    ED's causal pattern; with commitment's fewest directions and whole numbers,
    three: consistent, not derived."
  E2 met, E3 not: "The floor is seen on grids but not on ED's random slices";
    take stock of road C.
  E2 not met: calibration or regime problem; check linearity and settling,
    revise and retest (recorded).
  Exponents don't separate (beta1 - beta2 < 0.3 or beta2 - beta3 < 0.3, in both
    G and R): "The floor isn't seen in ED's causal pattern"; take stock of road C.
  E5 not as expected: recorded, not blocking.
  E1 fails: code bug, fix and rerun (recorded).
Resumable: one JSON per run in c2b_runs/; finished runs are skipped.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from c2b import SIZES, SIGMA, grid_slice, random_slice, simulate

OUT = "c2b_runs"


def job_name(d, n, kind, fresh, seed):
    return f"d{d}_n{n}_{kind}_{'fresh' if fresh else 'persistent'}_s{seed}"


def do_job(job):
    d, n, kind, fresh, seed = job
    path = os.path.join(OUT, job_name(*job) + ".json")
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    sl = grid_slice(d, n) if kind == "G" else random_slice(d, n, seed)
    res = simulate(sl, seed, fresh)
    res["seconds"] = time.perf_counter() - t0
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f)
    os.replace(tmp, path)
    return path, res["seconds"]


def slope(x, y):
    x, y = np.log(np.asarray(x, float)), np.log(np.asarray(y, float))
    return float(np.polyfit(x, y, 1)[0])


def analyse():
    runs = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            r = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
            runs[(r["d"], r["n"], r["kind"], r["fresh"], r["seed"])] = r
    lines = []
    e1 = True
    e1_notes = []
    for key, r in runs.items():
        d = r["d"]
        if r["kind"] == "G" and abs(r["mean_degree"] - 2 * d) > 1e-12:
            e1 = False; e1_notes.append(f"grid degree {key}")
        if r["kind"] == "R" and not (9 <= r["mean_degree"] <= 11):
            e1 = False; e1_notes.append(f"random degree {r['mean_degree']:.2f} {key}")
        if not r["fresh"]:
            if r["max_neighbour_diff"] >= 0.3:
                e1 = False; e1_notes.append(f"max neighbour diff {r['max_neighbour_diff']:.3f} {key}")
            if r["rate_spread"] >= 0.01 * SIGMA:
                e1 = False; e1_notes.append(f"rate spread {r['rate_spread']:.2e} {key}")
            if r["W_change"] >= 0.02:
                e1 = False; e1_notes.append(f"W change {r['W_change']:.3f} {key}")
    beta, tilt_ratio, tilt_slope = {}, {}, {}
    for fresh in (False, True):
        for kind in ("G", "R"):
            for d in (1, 2, 3):
                ns = SIZES[d]
                bs, trs = [], []
                for s in range(3):
                    W = [runs[(d, n, kind, fresh, s)]["W"] for n in ns]
                    bs.append(slope(ns, W))
                    trs.append((W[-1] / ns[-1]) / (W[0] / ns[0]))
                beta[(fresh, kind, d)] = float(np.median(bs))
                tilt_ratio[(fresh, kind, d)] = float(np.median(trs))
                sls = []
                for s in range(3):
                    tr = {int(k): v for k, v in runs[(d, ns[-1], kind, fresh, s)]["tilt_r"].items()}
                    rs = sorted(tr)
                    rs = [r for r in rs if r <= ns[-1] // 4] if kind == "G" else rs[:-1]
                    if len(rs) >= 2:
                        sls.append(slope(rs, [tr[r] for r in rs]))
                tilt_slope[(fresh, kind, d)] = float(np.median(sls)) if sls else float("nan")
                redraws = [runs[(d, n, kind, fresh, s)]["redraws"] for n in ns for s in range(3)]
                extra = ""
                if not fresh:
                    md = max(runs[(d, n, kind, fresh, s)]["max_neighbour_diff"] for n in ns for s in range(3))
                    rsp = max(runs[(d, n, kind, fresh, s)]["rate_spread"] for n in ns for s in range(3))
                    wc = max(runs[(d, n, kind, fresh, s)]["W_change"] for n in ns for s in range(3))
                    extra = f"; max neighbour diff {md:.3f}, max rate spread {rsp/SIGMA:.1e} sigma, max W change {wc:.4f}"
                Wmed = [float(np.median([runs[(d, n, kind, fresh, s)]["W"] for s in range(3)])) for n in ns]
                lines.append(f"{'fresh     ' if fresh else 'persistent'} {kind} d={d}: median W {', '.join(f'{w:.4g}' for w in Wmed)} at n={ns}; "
                             f"beta {beta[(fresh, kind, d)]:.3f} (seeds {', '.join(f'{b:.3f}' for b in bs)}); tilt ratio {tilt_ratio[(fresh, kind, d)]:.3f}; "
                             f"within-slice tilt slope {tilt_slope[(fresh, kind, d)]:.3f}; redraws {sum(redraws)}{extra}")
    rng2 = {"G": {1: (1.35, 1.65), 2: (0.85, 1.15), 3: (0.35, 0.65)},
            "R": {1: (1.3, 1.7), 2: (0.8, 1.2), 3: (0.3, 0.7)}}
    inr = lambda v, ab: ab[0] <= v <= ab[1]
    e2 = all(inr(beta[(False, "G", d)], rng2["G"][d]) for d in (1, 2, 3))
    e3 = all(inr(beta[(False, "R", d)], rng2["R"][d]) for d in (1, 2, 3))
    e4 = all(tilt_ratio[(False, k, 1)] > 1.5 and 0.8 <= tilt_ratio[(False, k, 2)] <= 1.25 and tilt_ratio[(False, k, 3)] < 0.67
             for k in ("G", "R"))
    ctl = {1: (0.35, 0.65), 2: (-0.1, 0.3), 3: (-0.2, 0.15)}
    e5 = all(inr(beta[(True, k, d)], ctl[d]) and tilt_ratio[(True, k, d)] < 0.67 for k in ("G", "R") for d in (1, 2, 3))
    sep = {k: (beta[(False, k, 1)] - beta[(False, k, 2)] >= 0.3 and beta[(False, k, 2)] - beta[(False, k, 3)] >= 0.3) for k in ("G", "R")}
    for name, v in (("E1 structure and regime", e1), ("E2 grids persistent exponents", e2), ("E3 random slices persistent exponents", e3),
                    ("E4 persistent tilt ratios", e4), ("E5 fresh-each-tick control", e5)):
        lines.append(f"{name}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if e1_notes:
        lines.append("E1 notes: " + "; ".join(e1_notes[:20]))
    lines.append(f"exponents separate: G {sep['G']}, R {sep['R']}")
    if not e1:
        verdict = "E1 failed: code bug or regime problem; fix and rerun (recorded)."
    elif not e2:
        verdict = "E2 not met: calibration or regime problem; check linearity and settling, revise and retest (recorded)."
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
            for fresh in (False, True) for s in range(3)]
    jobs.sort(key=lambda j: -(j[1] ** j[0]) * (j[1] ** 2))  # longest first
    t0 = time.perf_counter()
    done = 0
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 5) as pool:
        for path, sec in pool.imap_unordered(do_job, jobs):
            done += 1
            print(f"[{done}/{len(jobs)}] {os.path.basename(path)} {sec:.0f} s (elapsed {time.perf_counter()-t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time this session {time.perf_counter()-t0:.0f} s")
    print("\n".join(lines))
    with open("c2b_run1.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
