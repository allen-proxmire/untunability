"""C3d runs (note 21, C76; D31, D32, D33; IMPLEMENTATION_NOTES.md, C3d section). T = 200 by the cost plan (C77).

Expected results, written down before the first run (note 21; low confidence except E0, E1):
  Shape at a size (median of seeds; booleans need both seeds), against FC at that size:
    crumpled: largest degree >= 3x FC's, or tetrahedra per event >= 2 x 5.699;
    hyperbolic: exponential-growth flag set;
    branched: neck strain >= 3x FC's, or d_H < 2.3, or d_s < 2.0;
    flat 3D: none of these and d_H in [2.5, 3.5] and d_s in [2.3, 3.7]; else unclassified.
  Settled: median |d_H(T) - d_H(3T/4)| <= 0.15 and median relative change of largest degree <= 20%.
  E0  calibration gate: FC classified flat 3D at both sizes; RC not flat 3D at both sizes. Checked first;
      if it fails the growth runs do not start.
  E1  every structure check exact every tick; both budgets conserved (children to 1e-9; links exactly,
      links + pool == B_L); no event over the ceiling; and either the run completes T ticks with mean size
      over T/2..T within +-10% of the start, or it stops on a recorded guard (died, ran away, densified).
  E2  S0 not flat 3D at the larger size.
  E3  S4 flat 3D at both sizes, settled.
  E4  every setting settled at both sizes.
  S1, S2, S3 reported.
Exit rule (note 21):
  E0 fails: stop before the growth runs; readings revision (recorded).
  E1 fails on structure or a budget: code bug (recorded).
  A setting that decides the verdict is unsettled: "Not settled in T ticks".
  Then: S4 flat 3D at both sizes and S0 not flat at the larger size: "With the link balance and the ceiling,
  ED's meanings grow a flat 3D slice at the sizes run: consistent, not derived; the density, the ceiling and
  the three strengths are knobs." S0 flat 3D at both sizes: "At pinned density, growth alone keeps a 3D slice
  flat." Density holds but nothing reads flat 3D: "The link balance fixes density but not shape: <shapes>."
  Anything else: recorded as it reads.
Resumable: one JSON per finished job in c3d_runs/, state saved every 10 ticks in c3d_runs/ckpt/.
"""
import json
import os
import pickle
import sys
import time
import numpy as np
from multiprocessing import Pool
from c3c import Slice3, flip_randomize, SIGMA, K
from c3d import tick, slice_readings, FLAT_LINKS_PER_EVENT, DEGREE_CAP

SIZES = (20, 24)
SETTINGS = {"S0": (0, 0, 0), "S1": (1, 0, 0), "S2": (0, 1, 0), "S3": (0, 0, 1), "S4": (1, 1, 1)}
SEEDS = (0, 1)
T = 200
CHECKS = (T // 2, (3 * T) // 4, T)
OUT = "c3d_runs"
CKPT_EVERY = 10
TETS_PER_EVENT_CAP = 20


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def do_job(job):
    if job[0] == "cal":
        _, kind, n = job
        path = os.path.join(OUT, f"cal_{kind}_n{n}.json")
        if os.path.exists(path):
            return path, 0
        t0 = time.perf_counter()
        M = Slice3(n)
        if kind == "RC":
            flip_randomize(M, 50, np.random.default_rng(7))
        res = dict(job="cal", kind=kind, n=n, structure_notes=M.check(),
                   readings=slice_readings(M, SIZES.index(n), with_walk=True))
        res["seconds"] = time.perf_counter() - t0
        dump(path, res)
        return path, res["seconds"]
    _, name, n, s = job
    path = os.path.join(OUT, f"grow_{name}_n{n}_s{s}.json")
    if os.path.exists(path):
        return path, 0
    ck = os.path.join(OUT, "ckpt", f"grow_{name}_n{n}_s{s}.pkl")
    alpha, lam, gamma = SETTINGS[name]
    if os.path.exists(ck):
        with open(ck, "rb") as f:
            st = pickle.load(f)
    else:
        M = Slice3(n)
        rng = np.random.default_rng(s)
        V0 = len(M.vt)
        BL = round(FLAT_LINKS_PER_EVENT * V0)
        st = dict(M=M, rng=rng, b={v: 1.0 for v in M.vt},
                  omega={v: 1.0 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))},
                  phi={v: 0.0 for v in M.vt}, t=0, V0=V0, BL=BL, pool=BL - len(M.val),
                  sizes=[], forced=[], refused=[], first_fail=None, budget_ok=True, link_ok=True,
                  cap_ok=True, status="survived", checkpoints={}, elapsed=0.0)
    M, rng = st["M"], st["rng"]
    seg0 = time.perf_counter()
    while st["t"] < T and st["status"] == "survived":
        if len(M.tets) / max(len(M.vt), 1) > TETS_PER_EVENT_CAP:
            st["status"] = "densified"
            break
        st["t"] += 1
        t = st["t"]
        r, st["pool"] = tick(M, st["b"], st["omega"], st["phi"], rng, alpha, lam, gamma, st["pool"])
        st["sizes"].append(r["size"])
        st["forced"].append(r["forced"])
        st["refused"].append((r["refused_budget"], r["refused_cap"], r["split_refused"]))
        notes = M.check()
        if notes:
            st["first_fail"] = [t, notes[:3]]
            st["status"] = "structure failure"
            break
        if abs(sum(st["b"].values()) - st["V0"]) > 1e-9 * st["V0"]:
            st["budget_ok"] = False
        if len(M.val) + st["pool"] != st["BL"]:
            st["link_ok"] = False
        if max(len(x) for x in M.nbrs.values()) > DEGREE_CAP:
            st["cap_ok"] = False
        if not (st["V0"] / 10 <= r["size"] <= 10 * st["V0"]):
            st["status"] = "died" if r["size"] < st["V0"] / 10 else "ran away"
            break
        if t in CHECKS:
            st["checkpoints"][str(t)] = slice_readings(M, 10 * s + SIZES.index(n), with_walk=True)
        if t % CKPT_EVERY == 0 and t < T:
            st["elapsed"] += time.perf_counter() - seg0
            seg0 = time.perf_counter()
            tmp = ck + ".tmp"
            with open(tmp, "wb") as f:
                pickle.dump(st, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, ck)
    st["elapsed"] += time.perf_counter() - seg0
    late = st["sizes"][T // 2 - 1:] if len(st["sizes"]) >= T else []
    ref = np.array(st["refused"]) if st["refused"] else np.zeros((1, 3))
    res = dict(job="grow", setting=name, alpha=alpha, lam=lam, gamma=gamma, n=n, V0=st["V0"], BL=st["BL"],
               seed=s, status=st["status"], first_structure_fail=st["first_fail"], budget_ok=st["budget_ok"],
               link_budget_ok=st["link_ok"], cap_ok=st["cap_ok"], ticks_done=st["t"],
               mean_size_late=float(np.mean(late)) if late else None,
               forced_per_tick=float(np.mean(st["forced"])) if st["forced"] else None,
               refused_budget_per_tick=float(ref[:, 0].mean()), refused_cap_per_tick=float(ref[:, 1].mean()),
               split_refused_per_tick=float(ref[:, 2].mean()),
               events=len(M.vt), tets=len(M.tets), links=len(M.val), pool=st["pool"],
               links_per_event=len(M.val) / max(len(M.vt), 1), tets_per_event=len(M.tets) / max(len(M.vt), 1),
               max_degree=max((len(x) for x in M.nbrs.values()), default=0),
               checkpoints=st["checkpoints"], seconds=st["elapsed"])
    dump(path, res)
    if os.path.exists(ck):
        os.remove(ck)
    return path, st["elapsed"]


def fin(x):
    return x is not None and np.isfinite(x)


def med(xs):
    xs = [x for x in xs if fin(x)]
    return float(np.median(xs)) if xs else float("nan")


def classify(rds, fc):
    m = lambda k: med([r.get(k) for r in rds])
    allb = lambda k: all(bool(r[k]) for r in rds)
    flags = []
    if m("max_degree") >= 3 * fc["max_degree"] or m("tets_per_event") >= 2 * 5.699:
        flags.append("crumpled")
    if allb("small_world"):
        flags.append("hyperbolic")
    dH, ds = m("d_H"), m("d_s")
    if m("neck_strain") >= 3 * fc["neck_strain"] or (fin(dH) and dH < 2.3) or (fin(ds) and ds < 2.0):
        flags.append("branched")
    if not flags and fin(dH) and 2.5 <= dH <= 3.5 and fin(ds) and 2.3 <= ds <= 3.7:
        return "flat 3D", dH, ds
    return (" + ".join(flags) if flags else "unclassified"), dH, ds


def gate():
    """Calibration gate: returns (ok, lines, FC readings per size)."""
    lines, FC, ok = [], {}, True
    for n in SIZES:
        fc = json.load(open(os.path.join(OUT, f"cal_FC_n{n}.json"), encoding="utf-8"))
        rc = json.load(open(os.path.join(OUT, f"cal_RC_n{n}.json"), encoding="utf-8"))
        FC[n] = fc["readings"]
        sf, dHf, dsf = classify([fc["readings"]], fc["readings"])
        sr, dHr, dsr = classify([rc["readings"]], fc["readings"])
        good = sf == "flat 3D" and sr != "flat 3D" and not fc["structure_notes"] and not rc["structure_notes"]
        ok = ok and good
        lines.append(f"calibration V={n**3}: FC {sf} (d_H {dHf:.3f}, d_s {dsf:.3f}, diameter {fc['readings']['diameter']:.0f}, "
                     f"max degree {fc['readings']['max_degree']}, links/event {fc['readings']['links_per_event']:.3f}); "
                     f"RC {sr} (d_H {dHr:.3f}, d_s {dsr:.3f}, diameter {rc['readings']['diameter']:.0f}, "
                     f"max degree {rc['readings']['max_degree']}, tets/event {rc['readings']['tets_per_event']:.2f}) "
                     f"-> {'ok' if good else 'NOT ok'}")
    return ok, lines, FC


def analyse():
    R = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            R[fn[:-5]] = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
    ok, lines, FC = gate()
    e0 = ok
    e1 = True
    shape, settled = {}, {}
    for name in SETTINGS:
        for n in SIZES:
            key = [f"grow_{name}_n{n}_s{s}" for s in SEEDS]
            if not all(k in R for k in key):
                shape[(name, n)], settled[(name, n)] = "not run", False
                continue
            runs = [R[k] for k in key]
            for r in runs:
                bad = r["first_structure_fail"] or not r["budget_ok"] or not r["link_budget_ok"] or not r["cap_ok"]
                if r["status"] == "survived":
                    bad = bad or r["mean_size_late"] is None or abs(r["mean_size_late"] / r["V0"] - 1) > 0.10
                elif r["status"] == "structure failure":
                    bad = True
                if bad:
                    e1 = False
            good = [r for r in runs if r["status"] == "survived" and str(T) in r["checkpoints"]]
            if len(good) < len(runs):
                sts = [r["status"] for r in runs]
                guards = [x for x in sts if x in ("densified", "died", "ran away")]
                shape[(name, n)] = guards[0] if guards else "incomplete runs"
                settled[(name, n)] = False
                lines.append(f"{name} V={n**3}: statuses {sts}; " + "; ".join(
                    f"seed {r['seed']}: {r['ticks_done']} ticks, links/event {r['links_per_event']:.3f}, "
                    f"tets/event {r['tets_per_event']:.2f}, max degree {r['max_degree']}, events {r['events']/r['V0']:.3f}x" for r in runs))
                continue
            rT = [r["checkpoints"][str(T)] for r in good]
            r3 = [r["checkpoints"][str(CHECKS[1])] for r in good]
            shp, dH, ds = classify(rT, FC[n])
            ch = [abs(a["d_H"] - b["d_H"]) for a, b in zip(rT, r3) if fin(a["d_H"]) and fin(b["d_H"])]
            dg = [abs(a["max_degree"] - b["max_degree"]) / max(b["max_degree"], 1) for a, b in zip(rT, r3)]
            settled[(name, n)] = bool(ch) and med(ch) <= 0.15 and med(dg) <= 0.20
            shape[(name, n)] = shp
            m = lambda k: med([x[k] for x in rT])
            traj = ", ".join(f"{med([r['checkpoints'][str(c)]['d_H'] for r in good]):.3f}" for c in CHECKS)
            lines.append(f"{name} V={n**3}: {shp}; d_H {dH:.3f} (at {CHECKS}: {traj}), d_s {ds:.3f}; settled {settled[(name, n)]}; "
                         f"links/event {m('links_per_event'):.3f} (flat 6.699), tets/event {m('tets_per_event'):.2f} (flat 5.699); "
                         f"mean degree {m('mean_degree'):.2f}, largest {m('max_degree'):.0f} (FC {FC[n]['max_degree']}, cap {DEGREE_CAP}); "
                         f"diameter {m('diameter'):.1f} (FC {FC[n]['diameter']:.0f}); valence mean {m('valence_mean'):.3f}, sd {m('valence_sd'):.3f}; "
                         f"neck strain {m('neck_strain'):.2f} (FC {FC[n]['neck_strain']:.2f}); "
                         f"late size/V0 {med([r['mean_size_late']/r['V0'] for r in good]):.3f}; forced/tick {med([r['forced_per_tick'] for r in good]):.1f}; "
                         f"refused budget/cap/split per tick {med([r['refused_budget_per_tick'] for r in good]):.0f}/"
                         f"{med([r['refused_cap_per_tick'] for r in good]):.0f}/{med([r['split_refused_per_tick'] for r in good]):.1f}")
    big, small = SIZES[-1], SIZES[0]
    flat = lambda nm, n: shape.get((nm, n)) == "flat 3D"
    e2 = not flat("S0", big)
    e3 = flat("S4", small) and flat("S4", big) and settled.get(("S4", small)) and settled.get(("S4", big))
    e4 = all(settled.get((nm, n)) for nm in SETTINGS for n in SIZES)
    for nm, v in (("E0 calibration gate", e0), ("E1 structure, budgets, ceiling, size", e1),
                  ("E2 S0 not flat at larger size", e2), ("E3 S4 flat at both sizes, settled", e3),
                  ("E4 all settings settled", e4)):
        lines.append(f"{nm}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if not e0:
        verdict = "E0 failed: readings revision (recorded); growth runs not started."
    elif not e1:
        verdict = "E1 failed: code bug (recorded)."
    elif flat("S4", small) and flat("S4", big) and not flat("S0", big):
        need = [f"{nm} V={n**3}" for nm in ("S4",) for n in SIZES if not settled[(nm, n)]]
        verdict = ("Not settled in T ticks (" + ", ".join(need) + ")." if need else
                   "With the link balance and the ceiling, ED's meanings grow a flat 3D slice at the sizes run: "
                   "consistent, not derived; the density, the ceiling and the three strengths are knobs.")
    elif flat("S0", small) and flat("S0", big):
        verdict = "At pinned density, growth alone keeps a 3D slice flat."
    elif all(shape[(nm, n)] != "flat 3D" for nm in SETTINGS for n in SIZES):
        verdict = "The link balance fixes density but not shape: " + ", ".join(f"{nm} {shape[(nm, big)]}" for nm in SETTINGS) + "."
    else:
        verdict = "Mixed: " + ", ".join(f"{nm} {shape[(nm, big)]}" for nm in SETTINGS) + "; recorded as it reads."
    lines.append("EXIT: " + verdict)
    return lines


def main():
    os.makedirs(os.path.join(OUT, "ckpt"), exist_ok=True)
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t0 = time.perf_counter()
    cals = [("cal", k, n) for n in SIZES for k in ("FC", "RC")]
    with Pool(min(workers, len(cals))) as pool:
        for p, sec in pool.imap_unordered(do_job, cals):
            print(f"calibration {os.path.basename(p)} {sec:.0f} s", flush=True)
    ok, lines, _ = gate()
    print("\n".join(lines), flush=True)
    if not ok:
        lines.append("EXIT: E0 failed: readings revision (recorded); growth runs not started.")
        print(lines[-1])
        open("c3d_run1.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
        return
    jobs = [("grow", nm, n, s) for n in sorted(SIZES, reverse=True) for nm in ("S4", "S0", "S1", "S2", "S3") for s in SEEDS]
    with Pool(workers) as pool:
        for i, (p, sec) in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print(f"[{i}/{len(jobs)}] {os.path.basename(p)} {sec:.0f} s (elapsed {time.perf_counter()-t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time this session {time.perf_counter()-t0:.0f} s")
    print("\n".join(lines))
    open("c3d_run1.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
