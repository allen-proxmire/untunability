"""Scoring for the strong-sync M2 runs (Allen D20). A PARTIAL result, not note 13's verdict.

Per-run criteria and the majority-of-seeds rule are as fixed before any M2
reading (m2_analyze.py). Reports, for K/sigma = 30 at 4,000 loci:
  * floor -0.2: settings (of 9) smooth three at rest; settings meeting the
    criteria at some checkpoint; stalls; mean readings;
  * control: small-world share; mean readings;
  * for context, the weak-sync (K/sigma = 1) floor -0.2 runs already saved.
Labels: "strong sync: smooth three in k of 9 settings" or "strong sync: no
setting reaches smooth three at rest". No X1/R-X verdict is given.
"""
import glob
import itertools
import json
import statistics as st
import numpy as np
from m2_analyze import at_rest, some_cp, majority, fin
from run_m2_plan_k30 import jobs as plan_jobs
from run_m2 import job_name


def main():
    R = {}
    for p in glob.glob("m2_runs/*.json"):
        with open(p, encoding="utf-8") as f:
            r = json.load(f)
        R[r["name"]] = r
    missing = [job_name(j) for j in plan_jobs() if job_name(j) not in R]
    lines = [f"strong-sync plan (D20): planned 54, missing {len(missing)}"]
    if missing:
        lines.append("INCOMPLETE: no summary until every planned job has a saved result.")
    else:
        passes = somes = stalls = 0
        for c, k in itertools.product((0.5, 1.0, 2.0), (8, 12, 16)):
            rs = [R[job_name(dict(kind="constrained", K=30, c=c, k_max=k, kappa_min=-0.2, N=4000, seed=s))] for s in range(3)]
            passes += majority([at_rest(r) for r in rs], 3)
            somes += majority([some_cp(r) for r in rs], 3)
            stalls += majority([r["stalled"] for r in rs], 3)
        lines.append(f"floor -0.2 at K/sigma=30: settings smooth three at rest {passes}/9; at some checkpoint {somes}/9; stalled {stalls}/9")

        def summary(kind, K):
            rows = [r for r in R.values() if r["job"]["kind"] == kind and r["job"]["K"] == K and r["job"]["N"] == 4000
                    and (kind == "control" or r["job"]["kappa_min"] == -0.2)]
            last = [r["checkpoints"][-1] for r in rows if r["checkpoints"]]
            def m(key):
                v = [x[key] for x in last if fin(x.get(key))]
                return f"{st.mean(v):.2f}" if v else "undefined"
            sw = sum(bool(x.get("small_world")) for x in last)
            return (f"{kind} K/sigma={K}: n={len(rows)}, mean degree {st.mean(r['relations']*2/r['loci'] for r in rows):.2f}, "
                    f"d_H {m('d_H')}, d_s {m('d_s')}, d_w {m('d_w')}, beta {m('beta')}, small world {sw}/{len(last)}")
        lines.append(summary("constrained", 30))
        lines.append(summary("control", 30))
        lines.append("context: " + summary("constrained", 1))
        label = (f"strong sync: smooth three at rest in {passes} of 9 settings" if passes
                 else "strong sync: no setting reaches smooth three at rest")
        lines.append("RESULT (partial, D20): " + label)
    out = "\n".join(lines)
    print(out)
    with open("m2_verdict_k30.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
