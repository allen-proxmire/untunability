"""C3a runs (note 13 with its revision before any run; D19, D20; IMPLEMENTATION_NOTES.md, C3a section).

Expected results, written down before the first run (note 13, sizes revised by D20):
  "Flat at a size" = median over seeds of slice d_H and d_s at T both in [1.7, 2.3], and settled
  (median |d_H(T) - d_H(3T/4)| <= 0.15).
  E0  calibrations at every size: F (flat grid torus) d_H and d_s in [1.7, 2.3]; R (torus randomized
      by 200 sweeps of uniform edge flips) d_H > 2.6.
  E1  every structure check exact in every run; budget conserved (1e-9 relative); every run survives;
      mean size over ticks T/2..T within +-10% of L*.
  E2  rule U not flat at the largest size, 25,600 (d_H > 2.3, or d_s outside [1.7, 2.3], or D > 2.4).
      Low confidence.
  E3  rule Q2 flat at all three sizes, and D in [1.7, 2.4]. Low confidence.
  E4  every Q setting settled at every size.
  Q0.5, Q1: reported, no expected value. Spacetime readings (1,600, ticks T-100..T): reported only.
  Global D = 1 / slope of ln(median mean eccentricity) against ln L* over the three sizes.
Exit rule (note 13, D20):
  E1 fails: code bug (recorded). E0 fails: readings or sizes revision (recorded).
  Then, ignoring settling, the tentative verdict in order:
    U flat at all sizes with D in [1.7, 2.4]: "Growth alone keeps a surface flat."
    else some Q flat at all sizes with D in [1.7, 2.4]: "Quadratic energy keeps a grown surface flat
      at the sizes run: consistent, not derived; lambda a knob." Then 3D on paper.
    else some Q flat at the smallest size (1,600) but not the largest: "Flat up to a crossover, as in
      equilibrium; 2D not reached at large scales." Then 3D on paper.
    else: "Growing a flat 2D slice is not reached with ED's local moves." Take stock.
  If any setting that decides the tentative verdict is unsettled at a size it uses: "Not settled in
  T ticks" (revise T, recorded).
  E2-E4 not as expected are findings; the verdict follows the table.
Resumable: one JSON per job in c3a_runs/.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from c3a import (Torus, grow_tick, flip_randomize, slice_readings, mean_eccentricity, degree_stats,
                 slice_edges, build_spacetime)
from readings_v2 import all_readings

SIZES = (40, 80, 160)
RULES = (None, 0.5, 1.0, 2.0)
SEEDS = (0, 1, 2)
T = 1000
CHECKS = (250, 500, 750, 1000)
OUT = "c3a_runs"


def rname(lam):
    return "U" if lam is None else f"Q{lam:g}"


def job_path(job):
    if job[0] == "cal":
        return os.path.join(OUT, f"cal_{job[1]}_n{job[2]}.json")
    _, lam, n, s = job
    return os.path.join(OUT, f"grow_{rname(lam)}_n{n}_s{s}.json")


def to_json(o):
    if hasattr(o, "item"):
        return o.item()
    return str(o)


def do_job(job):
    path = job_path(job)
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    if job[0] == "cal":
        _, kind, n = job
        M = Torus(n)
        if kind == "R":
            flip_randomize(M, 200, np.random.default_rng(7))
        res = dict(job="cal", kind=kind, n=n, structure_notes=M.check(),
                   readings=slice_readings(M, 3000 + SIZES.index(n)),
                   eccentricity=mean_eccentricity(M, 3000 + SIZES.index(n)), degrees=degree_stats(M))
    else:
        _, lam, n, s = job
        Ls = n * n
        M = Torus(n)
        b = {v: 1.0 for v in M.ring}
        rng = np.random.default_rng(s)
        sizes, forced = [], []
        first_fail, budget_ok, status = None, True, "survived"
        checkpoints, snaps = {}, []
        for t in range(1, T + 1):
            rec = {} if (n == SIZES[0] and t > T - 100) else None
            e = slice_edges(M) if rec is not None else None
            r = grow_tick(M, b, rng, lam, record=rec)
            if rec is not None:
                snaps.append((e, rec))
            sizes.append(r["size"])
            forced.append(r["forced"])
            if first_fail is None:
                notes = M.check()
                if notes:
                    first_fail = [t, notes[:3]]
            if abs(sum(b.values()) - Ls) > 1e-9 * Ls:
                budget_ok = False
            if not (Ls / 10 <= r["size"] <= 10 * Ls):
                status = "died" if r["size"] < Ls / 10 else "ran away"
                break
            if t in CHECKS:
                checkpoints[str(t)] = dict(readings=slice_readings(M, 3000 + 10 * s + SIZES.index(n)),
                                           degrees=degree_stats(M))
        res = dict(job="grow", rule=rname(lam), n=n, Lstar=Ls, seed=s, status=status,
                   first_structure_fail=first_fail, budget_ok=budget_ok,
                   mean_size_late=float(np.mean(sizes[T // 2 - 1:])) if status == "survived" else None,
                   forced_per_tick=float(np.mean(forced)), checkpoints=checkpoints)
        if status == "survived":
            res["eccentricity"] = mean_eccentricity(M, 3000 + 10 * s + SIZES.index(n))
            if snaps:
                snaps.append((slice_edges(M), {"children": {}, "absorbed": {}}))
                A = build_spacetime(snaps)
                rr = all_readings(A, np.random.default_rng(4000 + s))
                res["spacetime"] = {k: (float(rr[k]) if rr.get(k) is not None else None)
                                    for k in ("d_H", "d_s", "d_w", "N")}
    res["seconds"] = time.perf_counter() - t0
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, default=to_json)
    os.replace(tmp, path)
    return path, res["seconds"]


def fin(x):
    return x is not None and np.isfinite(x)


def med(xs):
    xs = [x for x in xs if fin(x)]
    return float(np.median(xs)) if xs else float("nan")


def analyse():
    R = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            R[fn[:-5]] = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
    lines = []
    inr = lambda x, a, b: fin(x) and a <= x <= b
    e0 = True
    for n in SIZES:
        F, Rr = R[f"cal_F_n{n}"], R[f"cal_R_n{n}"]
        okF = inr(F["readings"]["d_H"], 1.7, 2.3) and inr(F["readings"]["d_s"], 1.7, 2.3) and not F["structure_notes"]
        okR = fin(Rr["readings"]["d_H"]) and Rr["readings"]["d_H"] > 2.6 and not Rr["structure_notes"]
        e0 = e0 and okF and okR
        lines.append(f"calibration L*={n*n}: F d_H {F['readings']['d_H']}, d_s {F['readings']['d_s']} ({'ok' if okF else 'NOT ok'}); "
                     f"R d_H {Rr['readings']['d_H']}, d_s {Rr['readings']['d_s']}, degree sd {Rr['degrees']['deg_sd']:.2f} "
                     f"({'ok' if okR else 'NOT ok'}); eccentricity F {F['eccentricity']:.2f}, R {Rr['eccentricity']:.2f}")
    e1 = True
    flat, settled, D = {}, {}, {}
    for lam in RULES:
        rn = rname(lam)
        ecc = []
        for n in SIZES:
            runs = [R[f"grow_{rn}_n{n}_s{s}"] for s in SEEDS]
            for r in runs:
                if (r["first_structure_fail"] or not r["budget_ok"] or r["status"] != "survived"
                        or abs(r["mean_size_late"] / r["Lstar"] - 1) > 0.10):
                    e1 = False
            ok = [r for r in runs if r["status"] == "survived"]
            dH = [r["checkpoints"]["1000"]["readings"]["d_H"] for r in ok]
            ds = [r["checkpoints"]["1000"]["readings"]["d_s"] for r in ok]
            dH3 = [r["checkpoints"]["750"]["readings"]["d_H"] for r in ok]
            mdH, mds = med(dH), med(ds)
            sett = med([abs(a - b) for a, b in zip(dH, dH3) if fin(a) and fin(b)])
            settled[(rn, n)] = fin(sett) and sett <= 0.15
            flat[(rn, n)] = len(ok) == len(runs) and inr(mdH, 1.7, 2.3) and inr(mds, 1.7, 2.3)
            e = med([r.get("eccentricity") for r in ok])
            ecc.append(e)
            traj = ", ".join(f"{med([r['checkpoints'][str(c)]['readings']['d_H'] for r in ok if str(c) in r['checkpoints']]):.3f}"
                             for c in CHECKS)
            c2 = med([r["checkpoints"]["1000"]["degrees"]["curv2"] for r in ok])
            dmax = max(r["checkpoints"]["1000"]["degrees"]["deg_max"] for r in ok) if ok else None
            line = (f"{rn} L*={n*n}: survived {len(ok)}/3; median d_H {mdH:.3f}, d_s {mds:.3f} at T "
                    f"(d_H at 250/500/750/1000: {traj}); settle change {sett:.3f} "
                    f"({'settled' if settled[(rn, n)] else 'NOT settled'}); flat {flat[(rn, n)]}; "
                    f"mean (deg-6)^2 {c2:.2f}, max degree {dmax}; forced keeps/tick {med([r['forced_per_tick'] for r in ok]):.2f}; "
                    f"late size/L* {med([r['mean_size_late'] / r['Lstar'] for r in ok]):.3f}; eccentricity {e:.2f}")
            if n == SIZES[0]:
                line += (f"; spacetime d_H {med([r['spacetime']['d_H'] for r in ok if 'spacetime' in r]):.3f}, "
                         f"d_s {med([r['spacetime']['d_s'] for r in ok if 'spacetime' in r]):.3f}")
            lines.append(line)
        if all(fin(x) for x in ecc):
            sl = float(np.polyfit(np.log([n * n for n in SIZES]), np.log(ecc), 1)[0])
            D[rn] = 1.0 / sl if sl > 0 else float("inf")
        else:
            D[rn] = float("nan")
        lines.append(f"{rn}: global D {D[rn]:.3f}")
    inD = lambda rn: inr(D[rn], 1.7, 2.4)
    Qs = [rname(l) for l in RULES[1:]]
    e2 = not (flat[("U", SIZES[-1])] and settled[("U", SIZES[-1])] and inD("U"))
    e3 = all(flat[("Q2", n)] and settled[("Q2", n)] for n in SIZES) and inD("Q2")
    e4 = all(settled[(q, n)] for q in Qs for n in SIZES)
    for name, v in (("E0 calibrations", e0), ("E1 structure, budget, survival, size", e1),
                    ("E2 U not flat at largest size", e2), ("E3 Q2 flat at all sizes with D in range", e3),
                    ("E4 all Q settled", e4)):
        lines.append(f"{name}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if not e1:
        verdict = "E1 failed: code bug (recorded)."
    elif not e0:
        verdict = "E0 failed: readings or sizes revision (recorded)."
    else:
        if all(flat[("U", n)] for n in SIZES) and inD("U"):
            tent, deciders = "Growth alone keeps a surface flat.", [("U", n) for n in SIZES]
        elif any(all(flat[(q, n)] for n in SIZES) and inD(q) for q in Qs):
            qs = [q for q in Qs if all(flat[(q, n)] for n in SIZES) and inD(q)]
            tent = ("Quadratic energy keeps a grown surface flat at the sizes run: consistent, not derived; "
                    f"lambda a knob (flat: {', '.join(qs)}). Then 3D on paper.")
            deciders = [(q, n) for q in qs for n in SIZES]
        elif any(flat[(q, SIZES[0])] and not flat[(q, SIZES[-1])] for q in Qs):
            qs = [q for q in Qs if flat[(q, SIZES[0])] and not flat[(q, SIZES[-1])]]
            tent = f"Flat up to a crossover, as in equilibrium; 2D not reached at large scales ({', '.join(qs)}). Then 3D on paper."
            deciders = [(q, n) for q in qs for n in SIZES]
        else:
            tent = "Growing a flat 2D slice is not reached with ED's local moves. Take stock."
            deciders = [(rname(l), n) for l in RULES for n in SIZES]
        unsettled = [f"{a} L*={n*n}" for (a, n) in deciders if not settled[(a, n)]]
        verdict = (f"Not settled in T ticks (unsettled: {', '.join(unsettled)}); tentative verdict was: {tent}"
                   if unsettled else tent)
    lines.append("EXIT: " + verdict)
    return lines


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [("cal", k, n) for n in SIZES for k in ("F", "R")]
    jobs += [("grow", lam, n, s) for n in sorted(SIZES, reverse=True) for lam in reversed(RULES) for s in SEEDS]
    t0 = time.perf_counter()
    done = 0
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as pool:
        for path, sec in pool.imap_unordered(do_job, jobs):
            done += 1
            print(f"[{done}/{len(jobs)}] {os.path.basename(path)} {sec:.0f} s (elapsed {time.perf_counter() - t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time this session {time.perf_counter() - t0:.0f} s")
    print("\n".join(lines))
    with open("c3a_run1.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
