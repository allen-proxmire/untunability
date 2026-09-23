"""Check C216: one-sided (ED, RD38) against two-sided (causal set) Everpresent Lambda, in a toy model.

Model (Everpresent Lambda "Model 1", Ahmed-Dodelson-Greene-Sorkin 2004, as described by Das-Nasiri-Yazdi 2023, C210):
  S_i = S_{i-1} + alpha sqrt(V_i - V_{i-1}) xi_i ,  Lambda_i = 8 pi S_i / V_i   (Planck units, G = 1)
  V(tau) = (4 pi / 3) * integral a(tau')^4 (tau - tau')^3 dtau'   (past light-cone 4-volume, conformal time)
  H^2 = Omega_m a^-3 + Omega_r a^-4 + Lambda / 3   (units of today's H0; only the first Friedmann equation)
Because delta Lambda ~ 8 pi alpha / sqrt(V) is unchanged when Lambda and V are rescaled to Hubble units, the same
alpha is used directly in Hubble units. Omega_m = 0.315, Omega_r = 9.1e-5 (Planck 2018).
Integration in ln a from a = 1e-6 to 1 in 1,400 steps. A run "crashes" if H^2 <= 0.

Variants:
  TWO      as published: S is a free random walk; Lambda takes either sign.
  CLIP     ED one-sided (a): same walk, but dark energy is max(S, 0): never negative.
  REFLECT  ED one-sided (b): the walk itself bounces off zero, S = |S_prev + kick|.
Runs: 400 per variant, alpha in {0.005, 0.012}, seeds fixed.
Measured at a = 1: completion fraction; Omega_L = Lambda / (3 H^2); H(1) (today-like if 0.9 < H < 1.1 and
0.6 < Omega_L < 0.8); dark energy change since z = 1, |Lambda(1) - Lambda(0.5)| / |Lambda(1)| for today-like runs;
early dark energy |Omega_L| at a = 1/1100 (median); share of completed TWO runs with Lambda(1) < 0.

Caveats: a homogeneous toy with no perturbations, so it cannot test the CMB properly; the light-cone volume is
integrated on the step grid; the one-sided forms are Claude's two readings of "births never negative".

Source check (before the first run): the model's structure was verified in the original paper's text (Ahmed,
Dodelson, Greene, Sorkin, PRD 69, 103523 (2004), Eqs. 3-6): rho_L = S/N with N = V, S_{i+1} = S_i + alpha xi sqrt(dN),
S_0 = 0 at an early time, V = (4 pi/3) int dt' a^3 [int dt''/a]^3 (the same as the conformal-time form above), and only
the Friedmann equation kept. That paper uses units with 8 pi G = 1. The 8 pi and the alpha values here follow
Das-Nasiri-Yazdi's Model 1 as reported by a fetched summary, not verified verbatim, so alpha is not directly comparable
between the two papers, and P1 depends on that normalization.

Predictions frozen before the first run (2026-09-14):
  P1  TWO at alpha 0.012: completion between 0.3 and 0.8 (Das et al. report about 53%).
  P2  CLIP and REFLECT: completion 1.0 at both alphas (Lambda >= 0 cannot make H^2 <= 0).
  P3  At both alphas, mean Omega_L(1) of completed runs: REFLECT > CLIP > TWO.
  P4  At alpha 0.012, the today-like share is higher for CLIP than for TWO (medium confidence).
  P5  At alpha 0.012, median early |Omega_L| at a = 1/1100 is within a factor of 3 between TWO and REFLECT
      (one-sidedness does not remove early dark energy) (medium).
  P6  At alpha 0.012, the share of completed TWO runs with Lambda(1) < 0 is between 0.2 and 0.6.

Changes after freezing (2026-09-14):
  1. Run 1 (everpresent_onesided_run1.txt) was invalid because of an integration bug: the light-cone volume started
     from zero at a = 1e-6, leaving out all earlier spacetime, so the first kicks were huge compared with H^2. Every
     TWO run crashed, within steps 2-25 (a about 1e-6; diagnosed on 20 runs). Run-1 verdicts: P2 and P4 right; P1,
     P3, P5, P6 wrong (P3, P5, P6 undefined, since no TWO run completed). The volume integral itself was checked: at
     a = 1, V H^4 = 0.034, the matter-era analytic value (4 pi/3) x B(9,4) x 16 = 0.0339.
     Fix: the radiation-era volume before a = 1e-6 is added analytically at every step, and S starts with the spread
     it would already have, alpha sqrt(V_start) xi (the same as starting the walk at a = 0, as in the 2004 paper).
     Predictions P1-P6 are unchanged.
  2. Added a second normalization, verified in the 2004 paper's text (8 pi G = 1 units): the dark-energy term in
     H^2 is S / (3 V), with alpha in {0.01, 0.02} (the values in that paper's figures). Predictions, frozen before
     it was first run:
     Q1  TWO completion at alpha 0.01 is above 0.5 and higher than at alpha 0.02 (medium).
     Q2  CLIP and REFLECT completion 1.0 at both alphas.
     Q3  Mean Omega_L(1): REFLECT > CLIP > TWO at both alphas.
     Q4  At alpha 0.02, the today-like share is higher for CLIP than for TWO (medium).
     Q5  At alpha 0.02, median early |Omega_L| at a = 1/1100 is within a factor of 3 between TWO and REFLECT (medium).
     Q6  At alpha 0.01, the share of completed TWO runs with Lambda(1) < 0 is between 0.2 and 0.6.
  3. After run 2 (everpresent_onesided_run2.txt): the Das-Nasiri-Yazdi text, quoted through an HTML fetch, gives
     S_i = S_{i-1} + alpha sqrt(V_i - V_{i-1}) xi_i / G and Lambda_i = 8 pi G S_i / V_i (matching the "DAS"
     normalization here), and "For alpha = 0.012, only 535/10000 runs successfully completed", which is 5.35%, not
     "about 53%". P1's expected range came from a misread summary; its verdict (WRONG) stands as recorded.
     Run 2 verdicts: P2, P4, Q2, Q3, Q5, Q6 right; P1, P3, P5, P6, Q1, Q4 wrong (P3, P5, P6 undefined because no DAS
     alpha 0.012 TWO run completed).
  4. Added `--spot` for run_checks (reruns two cells with their seeds and checks the recorded run-2 summaries).
"""
import math
import sys

import numpy as np

OM, OR = 0.315, 9.1e-5
A_START, STEPS, RUNS = 1e-6, 1400, 400


def run(alpha, variant, rng, factor):
    lna = np.linspace(math.log(A_START), 0.0, STEPS + 1)
    a = np.exp(lna)
    dlna = lna[1] - lna[0]
    a_s = a[0]
    H_s = math.sqrt(OM * a_s ** -3 + OR * a_s ** -4)
    tau_s = 1.0 / (a_s * H_s)  # radiation era: a proportional to tau
    tau = np.zeros(STEPS + 1)
    tau[0] = tau_s

    def pre(tn):  # light-cone volume from a = 0 to a_s, seen from conformal time tn (radiation era, a = a_s tau/tau_s)
        return (4 * math.pi / 3) * a_s ** 4 / tau_s ** 4 * (
            tn ** 3 * tau_s ** 5 / 5 - tn ** 2 * tau_s ** 6 / 2 + 3 * tn * tau_s ** 7 / 7 - tau_s ** 8 / 8)

    V_prev = pre(tau_s)
    S = alpha * math.sqrt(V_prev) * rng.standard_normal()
    if variant == "REFLECT":
        S = abs(S)
    s_eff = max(S, 0.0) if variant == "CLIP" else S
    lam = factor * s_eff / V_prev
    lam_hist = np.zeros(STEPS + 1)
    lam_hist[0] = lam
    for n in range(1, STEPS + 1):
        H2 = OM * a[n] ** -3 + OR * a[n] ** -4 + lam / 3.0
        if H2 <= 0 or OM * a[n - 1] ** -3 + OR * a[n - 1] ** -4 + lam_hist[n - 1] / 3.0 <= 0:
            return None
        tau[n] = tau[n - 1] + dlna / (a[n] * math.sqrt(H2))
        ak = a[1: n + 1]
        wk = dlna / (ak * np.sqrt(np.maximum(OM * ak ** -3 + OR * ak ** -4 + lam_hist[1: n + 1] / 3.0, 1e-300)))
        V = pre(tau[n]) + (4 * math.pi / 3) * np.sum(ak ** 4 * (tau[n] - tau[1: n + 1]) ** 3 * wk)
        dV = max(V - V_prev, 0.0)
        V_prev = V
        S = S + alpha * math.sqrt(dV) * rng.standard_normal()
        if variant == "REFLECT":
            S = abs(S)
        s_eff = max(S, 0.0) if variant == "CLIP" else S
        lam = factor * s_eff / V
        lam_hist[n] = lam
    H2_1 = OM + OR + lam / 3.0
    if H2_1 <= 0:
        return None
    i_half = int(np.argmin(np.abs(a - 0.5)))
    i_rec = int(np.argmin(np.abs(a - 1 / 1100)))
    H2_rec = OM * a[i_rec] ** -3 + OR * a[i_rec] ** -4 + lam_hist[i_rec] / 3.0
    return {"H": math.sqrt(H2_1), "OL": lam / (3 * H2_1), "lam": lam, "lam_half": lam_hist[i_half],
            "early": abs(lam_hist[i_rec] / (3 * H2_rec)), "VH4": V_prev * H2_1 ** 2}


def summarize(results):
    done = [r for r in results if r is not None]
    comp = len(done) / len(results)
    OL = np.array([r["OL"] for r in done])
    today = [r for r in done if 0.9 < r["H"] < 1.1 and 0.6 < r["OL"] < 0.8]
    change = np.median([abs(r["lam"] - r["lam_half"]) / abs(r["lam"]) for r in today]) if today else float("nan")
    early = float(np.median([r["early"] for r in done])) if done else float("nan")
    neg = float(np.mean([r["lam"] < 0 for r in done])) if done else float("nan")
    return {"completion": comp, "mean_OL": float(OL.mean()) if len(OL) else float("nan"),
            "today_share": len(today) / len(results), "n_today": len(today), "change_z1": float(change),
            "early_OL": early, "neg_share": neg}


def scan(label, factor, alphas, seed_base):
    out = {}
    for alpha in alphas:
        for k, variant in enumerate(("TWO", "CLIP", "REFLECT")):
            rng = np.random.default_rng(seed_base + int(alpha * 1e4) * 10 + k)
            s = summarize([run(alpha, variant, rng, factor) for _ in range(RUNS)])
            out[(alpha, variant)] = s
            print("%-5s alpha %.3f %-8s completion %.3f  mean Omega_L %+.3f  today-like %.3f (%d)  median change since z=1 %.3f  "
                  "median early |Omega_L| %.2e  share Lambda<0 %.3f" % (label, alpha, variant, s["completion"], s["mean_OL"],
                  s["today_share"], s["n_today"], s["change_z1"], s["early_OL"], s["neg_share"]), flush=True)
    return out


if "--spot" in sys.argv:
    # Change after freezing (2026-09-14): the full comparison takes about 7 minutes, so run_checks uses this spot
    # check. It reruns two cells with their original seeds and checks the recorded run-2 summaries reproduce.
    recorded = {("DAS", 0.005, "TWO", 8 * math.pi, 0): (0.983, -0.009, 0.435),
                ("ADGS", 0.02, "REFLECT", 1.0, 50000): (1.000, 0.028, 0.000)}
    ok = True
    for (label, alpha, variant, factor, base), (comp, mean_ol, neg) in recorded.items():
        k = ("TWO", "CLIP", "REFLECT").index(variant)
        rng = np.random.default_rng(base + int(alpha * 1e4) * 10 + k)
        s = summarize([run(alpha, variant, rng, factor) for _ in range(RUNS)])
        good = abs(s["completion"] - comp) < 0.0015 and abs(s["mean_OL"] - mean_ol) < 0.0015 and abs(s["neg_share"] - neg) < 0.0015
        ok &= good
        print("%-4s %s alpha %.3f %s: completion %.3f, mean Omega_L %+.3f, share Lambda<0 %.3f" % (
            "PASS" if good else "FAIL", label, alpha, variant, s["completion"], s["mean_OL"], s["neg_share"]))
    print("ALL PASS" if ok else "SOME FAIL")
    sys.exit(0 if ok else 1)


def ordered(out, al):
    return out[(al, "REFLECT")]["mean_OL"] > out[(al, "CLIP")]["mean_OL"] > out[(al, "TWO")]["mean_OL"]


das = scan("DAS", 8 * math.pi, (0.005, 0.012), 0)
t, c, r = das[(0.012, "TWO")], das[(0.012, "CLIP")], das[(0.012, "REFLECT")]
p_checks = [
    ("P1 TWO completion 0.3-0.8 at alpha 0.012", 0.3 <= t["completion"] <= 0.8),
    ("P2 one-sided completion 1.0", all(das[(al, v)]["completion"] == 1.0 for al in (0.005, 0.012) for v in ("CLIP", "REFLECT"))),
    ("P3 mean Omega_L: REFLECT > CLIP > TWO at both alphas", all(ordered(das, al) for al in (0.005, 0.012))),
    ("P4 today-like share CLIP > TWO at alpha 0.012", c["today_share"] > t["today_share"]),
    ("P5 early |Omega_L| within a factor of 3, TWO vs REFLECT", 1 / 3 <= r["early_OL"] / t["early_OL"] <= 3),
    ("P6 TWO share Lambda(1) < 0 between 0.2 and 0.6", 0.2 <= t["neg_share"] <= 0.6),
]

adgs = scan("ADGS", 1.0, (0.01, 0.02), 50000)
t1, t2 = adgs[(0.01, "TWO")], adgs[(0.02, "TWO")]
c2, r2 = adgs[(0.02, "CLIP")], adgs[(0.02, "REFLECT")]
q_checks = [
    ("Q1 TWO completion at 0.01 above 0.5 and above that at 0.02", t1["completion"] > 0.5 and t1["completion"] > t2["completion"]),
    ("Q2 one-sided completion 1.0", all(adgs[(al, v)]["completion"] == 1.0 for al in (0.01, 0.02) for v in ("CLIP", "REFLECT"))),
    ("Q3 mean Omega_L: REFLECT > CLIP > TWO at both alphas", all(ordered(adgs, al) for al in (0.01, 0.02))),
    ("Q4 today-like share CLIP > TWO at alpha 0.02", c2["today_share"] > t2["today_share"]),
    ("Q5 early |Omega_L| within a factor of 3, TWO vs REFLECT at 0.02", 1 / 3 <= r2["early_OL"] / t2["early_OL"] <= 3),
    ("Q6 TWO share Lambda(1) < 0 between 0.2 and 0.6 at 0.01", 0.2 <= t1["neg_share"] <= 0.6),
]
print()
for name, passed in p_checks + q_checks:
    print("%-6s %s" % ("RIGHT" if passed else "WRONG", name))
print("ALL PREDICTIONS AS FROZEN" if all(p for _, p in p_checks + q_checks) else "SOME PREDICTIONS WRONG")
sys.exit(0 if all(p for _, p in p_checks + q_checks) else 1)
