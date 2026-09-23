"""Tier 3 comparison, against attempt 7's own per-seed values rather than the note's rounded ones.

SYMMETRIC CRITERION, declared 2026-09-19 while attempt 7's six extra seeds were still running and
before any of their values had been seen (zero of six finished at the time of writing).

The original criterion - both of attempt 7's two values inside the port's eight-seed min-max - is
wrong now that both sides have eight seeds, and it was too strict even then: the min-max of eight
samples does not cover a population, so a fresh draw lands outside it about a fifth of the time. It
duly failed on merges and splits per tick by 0.19 and 0.12 in about 8,065, which is 0.002 per cent,
with the two ranges overlapping 94 and 99 per cent.

With eight seeds on each side, a quantity passes when BOTH:
  (a) the two eight-seed ranges overlap; and
  (b) the two means differ by less than the pooled seed-to-seed standard deviation.
A Mann-Whitney U p-value is printed for the record and is NOT part of the gate.
Tier 3 passes when every quantity passes, in both settings, with all runs structurally clean.


Attempt 7 has two seeds per setting at n = 24 (its `c3g_runs/grow_*_n24_*.json`); the port has eight.
The test of note 2's tier 3 is whether each attempt 7 value falls inside the port's seed-to-seed
range. Both ranges are printed, so a near miss is visible rather than hidden behind a verdict.
"""
import glob
import json
import os
import numpy as np

A7DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ED_Attempt_07", "model", "c3g_runs")
EXTRA = "a7_extra_runs"    # six more seeds of attempt 7's own code, run from attempt 8 (D4)
PORTDIR = "p3_tier3_runs"
KEYS = ("links_per_event", "tets_per_event", "diameter", "spacetime_d_H", "refused_sync_per_tick",
        "merges_per_tick", "splits_per_tick", "forced_or_split_refused")


def a7_rows(setting):
    out = []
    files = sorted(glob.glob(os.path.join(A7DIR, "grow_%s_n24_*.json" % setting)))
    files += sorted(glob.glob(os.path.join(EXTRA, "grow_%s_n24_s*.json" % setting)))
    for f in files:
        r = json.load(open(f, encoding="utf-8"))
        ck = (r.get("checkpoints") or {}).get("150") or {}
        st = r.get("spacetime") or {}
        out.append(dict(links_per_event=r["links_per_event"], tets_per_event=r["tets_per_event"],
                        diameter=ck.get("diameter"), spacetime_d_H=st.get("d_H"),
                        refused_sync_per_tick=r["refused_sync_per_tick"],
                        merges_per_tick=r["merges_per_tick"], splits_per_tick=r["splits_per_tick"],
                        forced_or_split_refused=r["split_refused_per_tick"], events=r["events"]))
    return out


def port_rows(setting):
    out = []
    for f in sorted(glob.glob(os.path.join(PORTDIR, "grow_%s_s*.json" % setting))):
        r = json.load(open(f, encoding="utf-8"))
        sl = r.get("slice") or {}
        st = r.get("spacetime") or {}
        out.append(dict(links_per_event=r["links_per_event"], tets_per_event=r["tets_per_event"],
                        diameter=sl.get("diameter"), spacetime_d_H=st.get("d_H"),
                        refused_sync_per_tick=r["refused_sync_per_tick"],
                        merges_per_tick=r["merges_per_tick"], splits_per_tick=r["splits_per_tick"],
                        forced_or_split_refused=r["split_refused_per_tick"], events=r["events"],
                        status=r["status"], ok=all(r["ok"].values())))
    return out


def rng(rows, k):
    v = [float(r[k]) for r in rows if isinstance(r.get(k), (int, float))]
    return (min(v), max(v), float(np.mean(v)), len(v)) if v else None


def main():
    lines = []
    verdict = True
    for setting in ("A", "B"):
        p = port_rows(setting)
        a = a7_rows(setting)
        if not p:
            continue
        bad = [r for r in p if not r["ok"] or r["status"] != "survived"]
        lines.append("setting %s: port %d seeds, attempt 7 %d seeds" % (setting, len(p), len(a)))
        lines.append("  T1 structure/budgets/ceiling/flips, all seeds survived: %s"
                     % ("clean" if not bad else "FAILED in %d run(s)" % len(bad)))
        if bad:
            verdict = False
        lines.append("  %-24s %-28s %-28s %s" % ("", "port (%d seeds)" % len(p), "attempt 7 (%d seeds)" % len(a), "tier 3"))
        for k in KEYS:
            rp, ra = rng(p, k), rng(a, k)
            if rp is None or ra is None:
                lines.append("  %-24s %s" % (k, "no values"))
                continue
            vp = [float(r[k]) for r in p if isinstance(r.get(k), (int, float))]
            va = [float(r[k]) for r in a if isinstance(r.get(k), (int, float))]
            if len(va) >= 8:
                overlap = min(rp[1], ra[1]) >= max(rp[0], ra[0])
                sd = float(np.sqrt((np.var(vp, ddof=1) + np.var(va, ddof=1)) / 2.0)) if len(vp) > 1 else 0.0
                close = abs(rp[2] - ra[2]) < sd if sd > 0 else (rp[2] == ra[2])
                ok = overlap and close
                try:
                    from scipy.stats import mannwhitneyu
                    pv = float(mannwhitneyu(vp, va, alternative="two-sided").pvalue)
                except Exception:
                    pv = float("nan")
                lines.append("  %-24s %8.2f - %-8.2f (m %8.2f)  %8.2f - %-8.2f (m %8.2f)  overlap %s, "
                             "|dmean| %.3f vs sd %.3f, U p=%.3f  %s"
                             % (k, rp[0], rp[1], rp[2], ra[0], ra[1], ra[2], "yes" if overlap else "NO",
                                abs(rp[2] - ra[2]), sd, pv, "pass" if ok else "FAIL"))
            else:
                ok = all(rp[0] <= x <= rp[1] for x in (ra[0], ra[1]))
                lines.append("  %-24s %8.2f - %-8.2f (m %6.2f)  %8.2f - %-8.2f  %s (2-seed criterion)"
                             % (k, rp[0], rp[1], rp[2], ra[0], ra[1], "inside" if ok else "OUTSIDE"))
            if not ok:
                verdict = False
    lines.append("")
    lines.append("TIER 3: %s" % ("PASS" if verdict else "NOT PASSED - see the OUTSIDE rows"))
    text = "\n".join(lines)
    print(text)
    with open("p3_tier3_report.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
