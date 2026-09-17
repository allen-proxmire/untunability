"""C3c runs (note 18, C67; D25, D26, D27; IMPLEMENTATION_NOTES.md, C3c section). T = 500 by the cost plan (C68).

Expected results, written down before the first run (note 18; low confidence except E0, E1):
  Shape at a size (median of seeds; booleans count only if true in both seeds), against FC at that size:
    crumpled: largest degree >= 3x FC's; hyperbolic: exponential-growth flag set; branched: neck strain
    >= 3x FC's or d_H < 2.3; flat 3D: none of these and d_H in [2.5, 3.5]; else unclassified.
  Settled: median |d_H(T) - d_H(3T/4)| <= 0.15 and median relative change of largest degree <= 20%.
  E0  FC classified flat 3D at both sizes; RC not flat 3D at both sizes.
  E1  every structure check exact every tick; budget conserved (1e-9 relative); every run survives;
      mean size over ticks T/2..T within +-10% of the start.
  E2  S0 not flat 3D at the larger size (most likely crumpled).
  E3  S1 branched at the larger size.
  E4  S3 not flat 3D at the larger size (most likely crumpled).
  E5  S4 flat 3D at both sizes, settled.
  S2, S5 reported.
Exit rule (note 18):
  E1 fails: code bug. E0 fails: readings revision. S4 or S5 unsettled at a size: "Not settled in T ticks".
  Then: S4 or S5 flat 3D at both sizes and S0 not flat 3D at the larger size: "Commitment, quadratic energy
  and sync together grow a flat 3D slice at the sizes run: consistent, not derived; alpha, lambda, gamma are
  knobs." S0 flat 3D at both sizes: "Growth alone keeps a 3D slice flat at these sizes." S4 and S5 not flat
  but each a named bad shape at the larger size: "The three pressures don't balance at unit strengths:
  <shapes>." Otherwise: "A flat 3D slice isn't grown with ED's local moves at these strengths."
  E2-E4 not as expected are findings.
Resumable: one JSON per finished job in c3c_runs/, and a state checkpoint every 50 ticks in c3c_runs/ckpt/.
"""
import json
import os
import pickle
import sys
import time
import numpy as np
from multiprocessing import Pool
from c3c import Slice3, tick, flip_randomize, slice_readings, SIGMA, K

SIZES = (16, 24)
SETTINGS = {"S0": (0, 0, 0), "S1": (1, 0, 0), "S2": (0, 1, 0), "S3": (0, 0, 1), "S4": (1, 1, 1), "S5": (1, 1, 4)}
SEEDS = (0, 1)
T = 500
CHECKS = (T // 2, (3 * T) // 4, T)
OUT = "c3c_runs"
CKPT_EVERY = 50


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def in_run_strain(M, phi):
    return float(max(abs(phi[a] - phi[b]) for a, b in M.val) / (SIGMA / K))


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
        res = dict(job="cal", kind=kind, n=n, structure_notes=M.check(), readings=slice_readings(M, 3000 + SIZES.index(n)))
        res["seconds"] = time.perf_counter() - t0
        dump(path, res)
        return path, res["seconds"]
    _, name, n, s = job
    path = os.path.join(OUT, f"grow_{name}_n{n}_s{s}.json")
    if os.path.exists(path):
        return path, 0
    ck = os.path.join(OUT, "ckpt", f"grow_{name}_n{n}_s{s}.pkl")
    alpha, lam, gamma = SETTINGS[name]
    t0 = time.perf_counter()
    if os.path.exists(ck):
        with open(ck, "rb") as f:
            st = pickle.load(f)
    else:
        M = Slice3(n)
        rng = np.random.default_rng(s)
        st = dict(M=M, rng=rng, b={v: 1.0 for v in M.vt},
                  omega={v: 1.0 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(len(M.vt)))},
                  phi={v: 0.0 for v in M.vt}, t=0, V0=len(M.vt), sizes=[], forced=[], flips=[],
                  first_fail=None, budget_ok=True, status="survived", checkpoints={}, elapsed=0.0)
    M, rng = st["M"], st["rng"]
    seg0 = time.perf_counter()
    while st["t"] < T and st["status"] == "survived":
        st["t"] += 1
        t = st["t"]
        r = tick(M, st["b"], st["omega"], st["phi"], rng, alpha, lam, gamma)
        st["sizes"].append(r["size"]); st["forced"].append(r["forced"]); st["flips"].append(r["flips_accepted"])
        notes = M.check()
        if notes:
            st["first_fail"] = [t, notes[:3]]
            st["status"] = "structure failure"
            break
        if abs(sum(st["b"].values()) - st["V0"]) > 1e-9 * st["V0"]:
            st["budget_ok"] = False
        if not (st["V0"] / 10 <= r["size"] <= 10 * st["V0"]):
            st["status"] = "died" if r["size"] < st["V0"] / 10 else "ran away"
            break
        if t in CHECKS:
            rd = slice_readings(M, 3000 + 10 * s + SIZES.index(n))
            rd["in_run_strain"] = in_run_strain(M, st["phi"])
            st["checkpoints"][str(t)] = rd
        if t % CKPT_EVERY == 0 and t < T:
            st["elapsed"] += time.perf_counter() - seg0
            seg0 = time.perf_counter()
            tmp = ck + ".tmp"
            with open(tmp, "wb") as f:
                pickle.dump(st, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, ck)
    st["elapsed"] += time.perf_counter() - seg0
    late = st["sizes"][T // 2 - 1:] if len(st["sizes"]) >= T else []
    res = dict(job="grow", setting=name, alpha=alpha, lam=lam, gamma=gamma, n=n, V0=st["V0"], seed=s, status=st["status"],
               first_structure_fail=st["first_fail"], budget_ok=st["budget_ok"],
               mean_size_late=float(np.mean(late)) if late else None, forced_per_tick=float(np.mean(st["forced"])) if st["forced"] else None,
               flips_accepted_per_tick=float(np.mean(st["flips"])) if st["flips"] else None,
               checkpoints=st["checkpoints"], seconds=st["elapsed"])
    dump(path, res)
    if os.path.exists(ck):
        os.remove(ck)
    return path, st["elapsed"]


def fin(x):
    return x is not None and np.isfinite(x)


def analyse():
    R = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            R[fn[:-5]] = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
    lines = []

    def classify(rds, fc):
        """rds: list of readings dicts (one per seed, or one for a calibration)."""
        med = lambda k: float(np.median([r[k] for r in rds if fin(r.get(k))])) if any(fin(r.get(k)) for r in rds) else float("nan")
        allb = lambda k: all(bool(r[k]) for r in rds)
        flags = []
        if med("max_degree") >= 3 * fc["max_degree"]:
            flags.append("crumpled")
        if allb("small_world"):
            flags.append("hyperbolic")
        dH = med("d_H")
        if med("neck_strain") >= 3 * fc["neck_strain"] or (fin(dH) and dH < 2.3):
            flags.append("branched")
        if not flags and fin(dH) and 2.5 <= dH <= 3.5:
            return "flat 3D", flags, dH
        return (" + ".join(flags) if flags else "unclassified"), flags, dH

    e0 = True
    FC = {}
    for n in SIZES:
        fc = R[f"cal_FC_n{n}"]["readings"]
        FC[n] = fc
        rc = R[f"cal_RC_n{n}"]["readings"]
        sf, _, dHf = classify([fc], fc)
        sr, _, dHr = classify([rc], fc)
        ok = sf == "flat 3D" and sr != "flat 3D" and not R[f"cal_FC_n{n}"]["structure_notes"] and not R[f"cal_RC_n{n}"]["structure_notes"]
        e0 = e0 and ok
        lines.append(f"calibration V={n**3}: FC {sf} (d_H {dHf:.3f}, max degree {fc['max_degree']}, neck strain {fc['neck_strain']:.2f}, "
                     f"flag {fc['small_world']}); RC {sr} (d_H {dHr:.3f}, max degree {rc['max_degree']}, neck strain {rc['neck_strain']:.2f}, "
                     f"flag {rc['small_world']}, valence sd {rc['valence_sd']:.2f}) -> {'ok' if ok else 'NOT ok'}")
    e1 = True
    shape, settled = {}, {}
    for name in SETTINGS:
        for n in SIZES:
            runs = [R[f"grow_{name}_n{n}_s{s}"] for s in SEEDS]
            for r in runs:
                if (r["status"] != "survived" or r["first_structure_fail"] or not r["budget_ok"]
                        or r["mean_size_late"] is None or abs(r["mean_size_late"] / r["V0"] - 1) > 0.10):
                    e1 = False
            ok = [r for r in runs if r["status"] == "survived" and str(T) in r["checkpoints"]]
            if len(ok) < len(runs):
                shape[(name, n)], settled[(name, n)] = "failed runs", False
                lines.append(f"{name} V={n**3}: statuses {[r['status'] for r in runs]}")
                continue
            rT = [r["checkpoints"][str(T)] for r in ok]
            r3 = [r["checkpoints"][str(CHECKS[1])] for r in ok]
            shp, flags, dH = classify(rT, FC[n])
            ch = [abs(a["d_H"] - b["d_H"]) for a, b in zip(rT, r3) if fin(a["d_H"]) and fin(b["d_H"])]
            dg = [abs(a["max_degree"] - b["max_degree"]) / b["max_degree"] for a, b in zip(rT, r3)]
            settled[(name, n)] = bool(ch) and float(np.median(ch)) <= 0.15 and float(np.median(dg)) <= 0.20
            shape[(name, n)] = shp
            m = lambda k, rr=rT: float(np.median([x[k] for x in rr]))
            traj = ", ".join(f"{np.median([r['checkpoints'][str(c)]['d_H'] for r in ok]):.3f}" for c in CHECKS)
            lines.append(f"{name} V={n**3}: {shp}; d_H {dH:.3f} (at {CHECKS}: {traj}); settled {settled[(name, n)]}; "
                         f"max degree {m('max_degree'):.0f} (FC {FC[n]['max_degree']}), mean degree {m('mean_degree'):.2f}; "
                         f"neck strain {m('neck_strain'):.2f} (FC {FC[n]['neck_strain']:.2f}); flags {[x['small_world'] for x in rT]}; "
                         f"valence mean {m('valence_mean'):.3f}, sd {m('valence_sd'):.3f}, (val-5.104)^2 {m('curv2'):.3f}; "
                         f"in-run strain {m('in_run_strain'):.1f}; late size/V0 {np.median([r['mean_size_late']/r['V0'] for r in ok]):.3f}; "
                         f"forced/tick {np.median([r['forced_per_tick'] for r in ok]):.2f}; flips/tick {np.median([r['flips_accepted_per_tick'] for r in ok]):.0f}")
    big, small = SIZES[-1], SIZES[0]
    flat = lambda nm, n: shape.get((nm, n)) == "flat 3D"
    e2 = not flat("S0", big)
    e3 = "branched" in str(shape.get(("S1", big)))
    e4 = not flat("S3", big)
    e5 = flat("S4", small) and flat("S4", big) and settled[("S4", small)] and settled[("S4", big)]
    for nm, v in (("E0 calibrations", e0), ("E1 structure, budget, survival, size", e1), ("E2 S0 not flat at larger size", e2),
                  ("E3 S1 branched at larger size", e3), ("E4 S3 not flat at larger size", e4), ("E5 S4 flat at both sizes, settled", e5)):
        lines.append(f"{nm}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if not e1:
        verdict = "E1 failed: code bug (recorded)."
    elif not e0:
        verdict = "E0 failed: readings revision (recorded)."
    elif not all(settled[(nm, n)] for nm in ("S4", "S5") for n in SIZES):
        verdict = "Not settled in T ticks (" + ", ".join(f"{nm} V={n**3}" for nm in ("S4", "S5") for n in SIZES if not settled[(nm, n)]) + ")."
    elif any(flat(nm, small) and flat(nm, big) for nm in ("S4", "S5")) and not flat("S0", big):
        which = [nm for nm in ("S4", "S5") if flat(nm, small) and flat(nm, big)]
        verdict = ("Commitment, quadratic energy and sync together grow a flat 3D slice at the sizes run: consistent, not derived; "
                   f"alpha, lambda, gamma are knobs ({', '.join(which)}).")
    elif flat("S0", small) and flat("S0", big):
        verdict = "Growth alone keeps a 3D slice flat at these sizes."
    elif all(shape[(nm, big)] not in ("flat 3D", "unclassified", "failed runs") for nm in ("S4", "S5")):
        verdict = f"The three pressures don't balance at unit strengths: S4 {shape[('S4', big)]}, S5 {shape[('S5', big)]}."
    else:
        verdict = "A flat 3D slice isn't grown with ED's local moves at these strengths."
    lines.append("EXIT: " + verdict)
    return lines


def main():
    os.makedirs(os.path.join(OUT, "ckpt"), exist_ok=True)
    jobs = [("cal", k, n) for n in SIZES for k in ("FC", "RC")]
    order = ("S4", "S5", "S1", "S2", "S3", "S0")
    jobs += [("grow", nm, n, s) for n in sorted(SIZES, reverse=True) for nm in order for s in SEEDS]
    t0 = time.perf_counter()
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as pool:
        for i, (p, sec) in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print(f"[{i}/{len(jobs)}] {os.path.basename(p)} {sec:.0f} s (elapsed {time.perf_counter()-t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time this session {time.perf_counter()-t0:.0f} s")
    print("\n".join(lines))
    open("c3c_run1.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
