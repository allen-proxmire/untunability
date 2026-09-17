"""Apply note 13's expected results and exit rule to the M2 runs (scoring fixed in IMPLEMENTATION_NOTES.md before any run).

Usage: python m2_analyze.py LARGEST
"""
import glob
import itertools
import json
import sys
import numpy as np


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


def fin(x):
    return x is not None and isinstance(x, (int, float)) and np.isfinite(x)


def cp_ok(c):
    return (fin(c.get("d_H")) and 2.6 <= c["d_H"] <= 3.4 and fin(c.get("d_s")) and 2.6 <= c["d_s"] <= 3.4
            and fin(c.get("d_w")) and 1.8 <= c["d_w"] <= 2.2 and fin(c.get("R5")) and c["R5"] <= 0.3
            and fin(c.get("beta")) and 0.55 <= c["beta"] <= 0.78 and not c.get("small_world"))


def at_rest(r):
    if r is None or r["stalled"] or len(r["checkpoints"]) < 5:
        return False
    cps = r["checkpoints"]
    if not all(cp_ok(c) for c in cps):
        return False
    for key in ("d_H", "d_s", "d_w"):
        v = [c[key] for c in cps]
        if max(v) - min(v) > 0.2:
            return False
    return True


def some_cp(r):
    return r is not None and not r["stalled"] and any(cp_ok(c) for c in r["checkpoints"])


def majority(vals, n):
    return sum(bool(v) for v in vals) * 2 > n


def main():
    largest = int(sys.argv[1])
    R = load()
    lines = [f"runs loaded: {len(R)}"]
    SCAN = list(itertools.product((1, 3, 10, 30), (0.5, 1.0, 2.0), (8, 12, 16), (-0.2, -0.1, 0.0)))

    def runs(kind, K, c, k, kap, N, seeds):
        return [R.get((kind, K, float(c), k, kap if kind == "constrained" else None, N, s)) for s in seeds]

    from run_m2_plan import jobs as plan_jobs
    expected = plan_jobs(largest)
    have = {(j["kind"], j["K"], float(j["c"]), j["k_max"],
             (None if not np.isfinite(j["kappa_min"]) else round(float(j["kappa_min"]), 1)), j["N"], j["seed"]) for j in expected}
    missing_jobs = [k for k in have if k not in R]
    lines.append(f"planned jobs: {len(expected)}; missing: {len(missing_jobs)}")
    if missing_jobs:
        lines.append("INCOMPLETE: no expected-result verdicts and no exit verdict until every planned job has a saved result.")
        out = "\n".join(lines)
        print(out)
        with open("m2_verdict.txt", "w", encoding="utf-8") as f:
            f.write(out + "\n")
        return

    # central setting
    central = {}
    for N in (1000, 4000, largest):
        rs = runs("constrained", 10, 1.0, 12, -0.1, N, range(5))
        central[N] = majority([at_rest(r) for r in rs], 5)
        lines.append(f"central constrained N={N}: at rest in {sum(at_rest(r) for r in rs)}/5 seeds -> {'PASS' if central[N] else 'fail'}; stalled {sum(bool(r and r['stalled']) for r in rs)}/5")

    # scan settings
    passes, somes, stall_set, e4, e8c, e8k = 0, 0, 0, 0, 0, 0
    kinds_ctrl = {}
    for K, c, k, kap in SCAN:
        rs = runs("constrained", K, c, k, kap, 4000, range(3))
        cs = runs("control", K, c, k, None, 4000, range(3))
        p = majority([at_rest(r) for r in rs], 3)
        passes += p
        somes += majority([some_cp(r) for r in rs], 3)
        stall_set += majority([bool(r and r["stalled"]) for r in rs], 3)

        def mean_dev(group):
            v = [abs(cp["d_w"] - 2) for r in group if r and not r["stalled"] for cp in r["checkpoints"] if fin(cp.get("d_w"))]
            return np.mean(v) if v else np.inf
        e4 += mean_dev(rs) < mean_dev(cs)

        def grew(group):
            return majority([bool(r and len(r["r10_growth"]) == 4 and r["r10_growth"][3] > r["r10_growth"][0]) for r in group], 3)
        e8k += grew(rs)
        e8c += grew(cs)
    n = len(SCAN)
    frac = passes / n
    lines.append(f"scan constrained settings at rest (majority of 3 seeds): {passes}/{n} = {frac:.3f}")
    lines.append(f"scan constrained settings meeting criteria at some checkpoint (majority): {somes}/{n}")

    # control, E3 and E6
    e3 = 0
    for K, c, k, kap in SCAN:
        cs = runs("control", K, c, k, None, 4000, range(3))

        def e3run(r):
            return (r is not None and not r["stalled"] and len(r["checkpoints"]) == 5 and
                    all(cp.get("small_world") or (fin(cp.get("d_H")) and 2.0 <= cp["d_H"] <= 2.7 and fin(cp.get("d_w")) and cp["d_w"] > 2.2)
                        for cp in r["checkpoints"]))
        e3 += majority([e3run(r) for r in cs], 3)
    ctrl_stalls = sum(bool(r["stalled"]) for key, r in R.items() if key[0] == "control")

    def sync_rest(r):
        return r is not None and not r["stalled"] and len(r["checkpoints"]) == 5 and all(cp["R7"] >= 0.9 for cp in r["checkpoints"])
    e6 = all(majority([sync_rest(r) for r in runs(kind, 30, c, k, kap, 4000, range(3))], 3)
             for kind in ("constrained", "control") for K, c, k, kap in SCAN if K == 30)

    # E1, E2
    e1 = True
    for r in R.values():
        for cp in r["checkpoints"]:
            if abs(cp["stuck_share"] - (1 - 2 / cp["mean_degree"] + 1 / (2 * cp["E"]))) > 1e-12:
                e1 = False
    leaks = {kind: [x for s in range(5) for x in (R.get((kind, 10, 1.0, 12, -0.1 if kind == "constrained" else None, 1000, s)) or {}).get("leakage", [])]
             for kind in ("constrained", "control")}
    pooled = leaks["constrained"] + leaks["control"]
    e2_mean = float(np.mean(pooled)) if pooled else float("nan")

    res = {
        "E1 stuck share formula": e1,
        f"E2 mean leakage per rewire in [1e-4, 1e-2] (pooled {e2_mean:.3e}; constrained {np.mean(leaks['constrained']) if leaks['constrained'] else float('nan'):.3e}, control {np.mean(leaks['control']) if leaks['control'] else float('nan'):.3e})": (1e-4 <= e2_mean <= 1e-2),
        f"E3 control: small world or d_H in [2.0,2.7] with d_w > 2.2 at rest in >= half of settings ({e3}/{n})": e3 * 2 >= n,
        f"E4 constrained d_w closer to 2 than control in >= half ({e4}/{n})": e4 * 2 >= n,
        f"E5 constrained fails smooth three at rest in >= half ({n - passes}/{n})": (n - passes) * 2 >= n,
        "E6 sync R7 >= 0.9 at rest at K/sigma = 30, both kinds": e6,
        f"E7 constrained stalls in fewer than half of settings ({stall_set}/{n}) and control in none ({ctrl_stalls} control runs stalled)": (stall_set * 2 < n and ctrl_stalls == 0),
        f"E8 distance grows 25%->100% in >= half of settings, constrained ({e8k}/{n}) and control ({e8c}/{n})": (e8k * 2 >= n and e8c * 2 >= n),
    }
    for k, v in res.items():
        lines.append(f"{k}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")

    if all(central.values()) and frac >= 0.75:
        x = "X1: model result: M2 grows a smooth, direction-free, three-dimensional pattern that stays that way (conditional; not a derivation; knobs counted)"
    elif 0.25 <= frac < 0.75:
        x = "X2: three in a region of the knobs (recorded as tuning)"
    elif frac < 0.25 and somes / n >= 0.25:
        x = "X3: three at a moment, not at rest"
    else:
        x = "X4: births inside relations, with ED's other rules as read, don't grow a smooth three"
    lines.append("EXIT: " + x)
    out = "\n".join(lines)
    print(out)
    with open("m2_verdict.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
