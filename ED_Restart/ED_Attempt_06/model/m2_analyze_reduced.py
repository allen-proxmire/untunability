"""Scoring for the reduced M2 plan (Allen D17; rules fixed before the reduced plan ran).

Differences from m2_analyze.py, all forced by the reduced scope:
  * the scan is the 36 settings at floor -0.2 only;
  * sizes are 1,000 and 4,000; there is no 16,000 run, so note 13's X1
    (which needs the central setting at rest at all three sizes) CANNOT be
    reached, and is reported as unreachable rather than failed;
  * verdicts are labelled R-X1..R-X4 for the -0.2 region at these sizes;
  * the constrained scan at floors -0.1 and 0 is not run; it is recorded
    separately as rings (C73, C75), not scored here.
Everything else (per-run criteria, majority of seeds, E1-E8 forms) is as fixed
in IMPLEMENTATION_NOTES.md before any M2 reading.
"""
import glob
import itertools
import json
import numpy as np
from m2_analyze import at_rest, some_cp, majority, fin
from run_m2_plan_reduced import jobs as plan_jobs


def load():
    R = {}
    for p in glob.glob("m2_runs/*.json"):
        with open(p, encoding="utf-8") as f:
            r = json.load(f)
        j = r["job"]
        kap = j["kappa_min"]
        kap = None if (isinstance(kap, str) or kap is None or not np.isfinite(float(kap))) else round(float(kap), 1)
        R[(j["kind"], j["K"], float(j["c"]), j["k_max"], kap, j["N"], j["seed"])] = r
    return R


def main():
    R = load()
    lines = ["reduced M2 plan (D17): scan at floor -0.2, sizes 1,000 and 4,000"]
    expected = plan_jobs()
    have = {(j["kind"], j["K"], float(j["c"]), j["k_max"],
             (None if not np.isfinite(j["kappa_min"]) else round(float(j["kappa_min"]), 1)), j["N"], j["seed"]) for j in expected}
    missing = [k for k in have if k not in R]
    lines.append(f"planned jobs: {len(expected)}; missing: {len(missing)}")
    if missing:
        lines.append("INCOMPLETE: no verdicts until every planned job has a saved result.")
        out = "\n".join(lines)
        print(out)
        with open("m2_verdict_reduced.txt", "w", encoding="utf-8") as f:
            f.write(out + "\n")
        return

    SET = list(itertools.product((1, 3, 10, 30), (0.5, 1.0, 2.0), (8, 12, 16)))

    def runs(kind, K, c, k, N, seeds, kap):
        return [R.get((kind, K, float(c), k, kap if kind == "constrained" else None, N, s)) for s in seeds]

    central = {}
    for N in (1000, 4000):
        rs = runs("constrained", 10, 1.0, 12, N, range(5), -0.1)
        central[N] = majority([at_rest(r) for r in rs], 5)
        lines.append(f"central constrained (floor -0.1) N={N}: at rest {sum(at_rest(r) for r in rs)}/5 -> {'PASS' if central[N] else 'fail'}; "
                     f"stalled {sum(bool(r and r['stalled']) for r in rs)}/5; mean degree "
                     f"{np.mean([r['relations']*2/r['loci'] for r in rs if r]):.2f}")

    passes = somes = stalls = e4 = e8k = e8c = e3 = 0
    for K, c, k in SET:
        rs = runs("constrained", K, c, k, 4000, range(3), -0.2)
        cs = runs("control", K, c, k, 4000, range(3), None)
        passes += majority([at_rest(r) for r in rs], 3)
        somes += majority([some_cp(r) for r in rs], 3)
        stalls += majority([bool(r and r["stalled"]) for r in rs], 3)

        def dev(group):
            v = [abs(cp["d_w"] - 2) for r in group if r and not r["stalled"] for cp in r["checkpoints"] if fin(cp.get("d_w"))]
            return np.mean(v) if v else np.inf
        e4 += dev(rs) < dev(cs)

        def grew(group):
            return majority([bool(r and len(r["r10_growth"]) == 4 and r["r10_growth"][3] > r["r10_growth"][0]) for r in group], 3)
        e8k += grew(rs)
        e8c += grew(cs)

        def e3run(r):
            return (r is not None and not r["stalled"] and len(r["checkpoints"]) == 5 and
                    all(cp.get("small_world") or (fin(cp.get("d_H")) and 2.0 <= cp["d_H"] <= 2.7 and fin(cp.get("d_w")) and cp["d_w"] > 2.2)
                        for cp in r["checkpoints"]))
        e3 += majority([e3run(r) for r in cs], 3)

    n = len(SET)
    frac = passes / n
    lines.append(f"scan at floor -0.2, settings at rest (majority of 3 seeds): {passes}/{n} = {frac:.3f}")
    lines.append(f"settings meeting the criteria at some checkpoint: {somes}/{n}")
    lines.append(f"settings stalling: {stalls}/{n}")

    def sync_rest(r):
        return r is not None and not r["stalled"] and len(r["checkpoints"]) == 5 and all(cp["R7"] >= 0.9 for cp in r["checkpoints"])
    e6 = all(majority([sync_rest(r) for r in runs(kind, 30, c, k, 4000, range(3), -0.2)], 3)
             for kind in ("constrained", "control") for K, c, k in SET if K == 30)

    e1 = all(abs(cp["stuck_share"] - (1 - 2 / cp["mean_degree"] + 1 / (2 * cp["E"]))) <= 1e-12
             for r in R.values() for cp in r["checkpoints"])
    leaks = {kind: [x for s in range(5)
                    for x in (R.get((kind, 10, 1.0, 12, -0.1 if kind == "constrained" else None, 1000, s)) or {}).get("leakage", [])]
             for kind in ("constrained", "control")}
    pooled = leaks["constrained"] + leaks["control"]
    e2 = float(np.mean(pooled)) if pooled else float("nan")
    ctrl_stalls = sum(bool(r["stalled"]) for key, r in R.items() if key[0] == "control")

    res = {
        "E1 stuck share formula": e1,
        f"E2 mean leakage per rewire in [1e-4, 1e-2] (pooled {e2:.3e})": (1e-4 <= e2 <= 1e-2),
        f"E3 control small world or d_H in [2.0,2.7] with d_w > 2.2, >= half ({e3}/{n})": e3 * 2 >= n,
        f"E4 constrained (-0.2) d_w closer to 2 than control, >= half ({e4}/{n})": e4 * 2 >= n,
        f"E5 constrained (-0.2) fails smooth three at rest, >= half ({n - passes}/{n})": (n - passes) * 2 >= n,
        "E6 sync R7 >= 0.9 at rest at K/sigma = 30, both kinds": e6,
        f"E7 constrained (-0.2) stalls in fewer than half ({stalls}/{n}); control none ({ctrl_stalls})": (stalls * 2 < n and ctrl_stalls == 0),
        f"E8 distance grows 25%->100%, >= half: constrained ({e8k}/{n}), control ({e8c}/{n})": (e8k * 2 >= n and e8c * 2 >= n),
    }
    for k, v in res.items():
        lines.append(f"{k}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")

    lines.append("note 13's X1 is unreachable in the reduced plan: it requires the central setting at rest at all three sizes, and 16,000 was dropped.")
    if all(central.values()) and frac >= 0.75:
        x = "R-X1: at 1,000 and 4,000, the floor -0.2 region grows a smooth, direction-free, three-dimensional pattern that stays that way (largest size untested; reduced plan; not a derivation; knobs counted)"
    elif 0.25 <= frac < 0.75:
        x = "R-X2: three in a region of the knobs within the floor -0.2 scan (recorded as tuning)"
    elif frac < 0.25 and somes / n >= 0.25:
        x = "R-X3: three at a moment, not at rest"
    else:
        x = "R-X4: with the floor at -0.2, births inside relations and ED's other rules as read don't grow a smooth three at these sizes"
    lines.append("EXIT (reduced): " + x)
    lines.append("floors -0.1 and 0 were not run: recorded as rings on C73's arithmetic and the measured runs in C71, C75.")
    out = "\n".join(lines)
    print(out)
    with open("m2_verdict_reduced.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
