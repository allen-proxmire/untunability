"""Stage A report: applies note 3's exit rule (C7) to sa_runs/. Written before the results were read."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sa_runs")


def load(dim, kind, seed):
    p = os.path.join(OUT, "%dD_%s_s%d.json" % (dim, kind, seed))
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def block(dim, flat, kinds):
    L = []
    f = load(dim, flat, 0)
    rows = [(flat, 0)] + [(k, s) for k, ss in kinds for s in ss]
    L.append("%dD  %-4s %-2s %7s %7s %9s %9s %9s %10s %7s %6s %6s %5s %7s  ok" % (
        dim, "kind", "sd", "V", "m", "s", "s_dens", "s_spread", "V*ds", "a_mean", "a_sd", "deg_sd", "dmax", "meandst"))
    for k, s in rows:
        r = load(dim, k, s)
        if r is None:
            L.append("     %-4s %-2d missing" % (k, s))
            continue
        vds = r["V"] * (r["s"] - f["s"]) if f else float("nan")
        L.append("     %-4s %-2d %7d %7d %9.5f %9.5f %9.5f %10.1f %7.3f %6.3f %6.3f %5d %7.3f  %s" % (
            k, s, r["V"], r["m"], r["s"], r["s_density"], r["s_spread"], vds, r["a_mean"], r["a_sd"], r["deg_sd"],
            r["deg_max"], r["mean_distance"], all(r["ok"].values())))
    return L


def verdict():
    f = load(3, "FL", 0)
    # REVISION before results: FR equals flat (no 3-2 sites on the grid), so FRc stands in for it in the rule.
    others = {k: [load(3, k, s) for s in ss] for k, ss in (("FRc", (0,)), ("F1", (0, 1)), ("W1", (0, 1)))}
    if f is None or any(r is None for rs in others.values() for r in rs):
        return "incomplete"
    spread = max(abs(rs[0]["s"] - rs[1]["s"]) for k, rs in others.items() if len(rs) == 2)
    margin = 2 * spread
    ds = {"%s_s%d" % (k, i): r["s"] - f["s"] for k, rs in others.items() for i, r in enumerate(rs)}
    oks = all(all(r["ok"].values()) for rs in others.values() for r in rs) and all(f["ok"].values())
    lines = ["seed spread %.5f, margin (2x) %.5f; delta s vs flat: %s" % (
        spread, margin, ", ".join("%s %+.5f" % kv for kv in ds.items()))]
    if not oks:
        lines.append("VERDICT: A1 failed - code problem (recorded).")
    elif all(d < -margin for d in ds.values()):
        lines.append("VERDICT: counting leans toward flat at one tick -> stage B.")
    elif any(ds[k] > margin for k in ds if not k.startswith("FR")):
        lines.append("VERDICT: with ED's slice-to-slice step, counting leans toward small worlds -> stage B not built; "
                     "what joins one slice to the next goes to Allen on paper.")
    else:
        lines.append("VERDICT: too close -> build stage B small in 2D.")
    return "\n".join(lines)


def main():
    L = []
    a0p = os.path.join(OUT, "A0.json")
    if os.path.exists(a0p):
        a0 = json.load(open(a0p, encoding="utf-8"))
        allm = all(all(r["match"].values()) for d in ("d3", "d2") for r in a0[d])
        L.append("A0 brute-force match: %s" % allm)
        for d in ("d3", "d2"):
            for r in a0[d]:
                L.append("   %s %-5s V=%d counted %s brute %s" % (d, r["kind"], r["V"], r["counted"], r["brute"]))
    L += block(3, "FL", (("FR", (0,)), ("FRc", (0,)), ("F1", (0, 1)), ("W1", (0, 1))))
    L += block(2, "F", (("R", (0,)), ("U", (0, 1)), ("Q1", (0, 1))))
    for dim, flat, kinds in ((3, "FL", ("FR", "FRc", "F1", "W1")), (2, "F", ("R", "U", "Q1"))):
        for k in (flat,) + kinds:
            for s in (0, 1):
                r = load(dim, k, s)
                if r:
                    L.append("   %dD %s s%d totals %s (%.0f s)" % (dim, k, s, r["totals"], r["seconds"]))
    L.append(verdict())
    text = "\n".join(L)
    open(os.path.join(HERE, "sa_count.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
