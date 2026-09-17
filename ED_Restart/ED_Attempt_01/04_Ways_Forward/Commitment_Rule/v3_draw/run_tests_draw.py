"""Runs the tests frozen in Spec.md against rule_draw.py. Exit code: D1a, D1b, D7 (code checks)."""
import itertools
import sys
from pathlib import Path

import numpy as np

import rule_draw as d

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v1"))
import rule_v1 as r1  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
I = d.INTERNAL
LS, NS = 31, 8
PHIS = (0.0, np.pi / 2, np.pi)
results = {}


def report(name, ok, detail):
    results[name] = ok
    print("%-6s %s  %s" % ("RIGHT" if ok else "WRONG", name, detail), flush=True)


def visibility(P):
    a = (P[0] + P[2]) / 2
    re = (P[0] - P[2]) / 2
    im = a - P[1]
    V = np.zeros_like(a)
    ok = a > 1e-9
    V[ok] = np.sqrt(re[ok] ** 2 + im[ok] ** 2) / a[ok]
    return V, ok


def system(phi, amps=((13, 1 / np.sqrt(2)), (17, None))):
    a = np.zeros((LS, 3), dtype=complex)
    for x, v in amps:
        a[x, I] = v if v is not None else np.exp(1j * phi) / np.sqrt(2)
    return a


def norm_screen(s):
    return s / s.sum()


def ratio_ok(V, V0, target, okmask, tol=1e-8):
    m = okmask & (V0 > 1e-6)
    return bool(np.all(np.abs(V[m] / V0[m] - target) < tol)), float(np.max(np.abs(V[m] / V0[m] - target))) if m.any() else 0.0


def screens_for(events, F, r_star=d.R_STAR, amps_fn=None):
    """For each phi: the run's branches (probability, pattern, drawn)."""
    out = []
    for phi in PHIS:
        a = amps_fn(phi) if amps_fn else system(phi)
        br, marks, worst = d.run(d.start(a, F), events, r_star)
        out.append((br, worst))
    return out


def averaged_V(runs):
    P = []
    for br, _ in runs:
        P.append(norm_screen(sum(p * d.screen(b, NS) / d.amount(b) for p, b, _ in br)))
    return visibility(P)


rng = np.random.default_rng(2026)

# V0
V0, ok0 = visibility([norm_screen(d.screen(d.start(system(phi), 1), NS)) for phi in PHIS])
print("V0: max %.4f over %d loci" % (float(V0.max()), int(ok0.sum())))

# D1a
a = rng.normal(size=(LS, 3)) + 1j * rng.normal(size=(LS, 3))
psi = d.start(a / np.linalg.norm(a), 3)
psi[..., 1, 0, 1] = 0.3 * psi[..., 0, 0, 0]
psi /= np.sqrt(d.amount(psi))
err = abs(d.amount(d.walk(psi)) - 1)
for loci, f, th in (([5], 0, 0.7), ([0, 30], 2, 1.3), ([12, 13, 14], 1, np.pi / 2)):
    err = max(err, abs(d.amount(d.meet(psi, loci, f, th)[0]) - 1))
report("D1a amount conserved (walk, meet)", err < 1e-12, "max change %.1e" % err)

# D1b mirror
a = rng.normal(size=(LS, 3)) + 1j * rng.normal(size=(LS, 3))
a /= np.linalg.norm(a)
ev = [("meet", [9], 0, 0.7)] + [("walk",)] * 5 + [("meet", [9, 10], 1, 1.2), ("walk",), ("walk",)]
evm = [("meet", [(-9) % LS], 0, 0.7)] + [("walk",)] * 5 + [("meet", [(-9) % LS, (-10) % LS], 1, 1.2), ("walk",), ("walk",)]
b1, _, _ = d.run(d.start(a, 2), ev)
b2, _, _ = d.run(d.start(r1.mirror(a), 2), evm)
err = float(np.max(np.abs(d.mirror(b1[0][1]) - b2[0][1])))
report("D1b mirror", len(b1) == 1 and len(b2) == 1 and err < 1e-12, "max error %.1e" % err)

# D2 no mark
runs = screens_for([], 1)
V, okm = averaged_V(runs)
good, dev = ratio_ok(V, V0, 1.0, okm)
report("D2 no mark: V/V0 = 1, no draw", good and all(len(br) == 1 for br, _ in runs), "max deviation %.1e" % dev)

# D3 Englert
allgood, devs = True, []
for th in (np.pi / 6, np.pi / 4, np.pi / 3):
    runs = screens_for([("meet", [13], 0, th)], 1)
    V, okm = averaged_V(runs)
    good, dev = ratio_ok(V, V0, abs(np.cos(th)), okm)
    allgood &= good and all(len(br) == 1 for br, _ in runs)
    devs.append(dev)
report("D3 partial mark: V/V0 = |cos theta|, no draw", allgood, "max deviations %s" % ", ".join("%.1e" % x for x in devs))

# D4 eraser, one full mark
runs = screens_for([("meet", [13], 0, np.pi / 2)], 1)
V, okm = averaged_V(runs)
unc = float(V[okm].max())
cond_good, cond_dev = True, []
for s in (+1, -1):
    P = []
    for br, _ in runs:
        _, kept = d.erase(br[0][1], [0], [s])
        P.append(norm_screen(d.screen(kept, NS)))
    Vc, okc = visibility(P)
    good, dev = ratio_ok(Vc, V0, 1.0, okc)
    cond_good &= good
    cond_dev.append(dev)
report("D4 eraser: unconditioned V ~ 0; conditioned V/V0 = 1; no draw",
       unc < 1e-10 and cond_good and all(len(br) == 1 for br, _ in runs),
       "unconditioned max %.1e; conditioned deviations %s" % (unc, ", ".join("%.1e" % x for x in cond_dev)))

# D5 redundant mark
amp5 = lambda phi: system(phi, ((13, np.cos(0.4)), (17, None)))


def amp5(phi):
    a = np.zeros((LS, 3), dtype=complex)
    a[13, I] = np.cos(0.4)
    a[17, I] = np.exp(1j * phi) * np.sin(0.4)
    return a


ev5 = [("meet", [13], f, np.pi / 2) for f in range(3)]
runs = screens_for(ev5, 3, amps_fn=amp5)
probs_ok, conf, worst = True, 0.0, 0.0
for br, w in runs:
    worst = max(worst, w)
    pm = {("MARKED" if b[13, I].reshape(-1)[-1] != 0 else "UNMARKED"): p for p, b, _ in br}
    marked = [p for p, b, _ in br if (np.abs(b[13]) ** 2).sum() > 1e-12]
    unmarked = [p for p, b, _ in br if (np.abs(b[17]) ** 2).sum() > 1e-12]
    probs_ok &= len(br) == 2 and abs(marked[0] - np.cos(0.4) ** 2) < 1e-12 and abs(unmarked[0] - np.sin(0.4) ** 2) < 1e-12
    for p, b, _ in br:
        on13 = float((np.abs(b[13]) ** 2).sum())
        on17 = float((np.abs(b[17]) ** 2).sum())
        conf = max(conf, min(on13, on17))
V, okm = averaged_V(runs)
report("D5 redundant mark: draw, Born weights, confined, V ~ 0",
       probs_ok and worst < 1e-12 and conf < 1e-15 and float(V[okm].max()) < 1e-10,
       "probabilities ok %s; disagreeing weight %.1e; other-path amount %.1e; averaged V max %.1e" % (probs_ok, worst, conf, float(V[okm].max())))

# D6 fixes only what the mark distinguishes
def amp6(psi_phase):
    a = np.zeros((LS, 3), dtype=complex)
    a[12, I] = 0.5
    a[14, I] = 0.5 * np.exp(1j * psi_phase)
    a[17, I] = 1 / np.sqrt(2)
    return a


ev6 = [("meet", [12, 13, 14], f, np.pi / 2) for f in range(3)]
P, Pref = [], []
for ph in PHIS:
    br, _, _ = d.run(d.start(amp6(ph), 3), ev6)
    marked = [b for p, b, _ in br if (np.abs(b[12]) ** 2).sum() + (np.abs(b[14]) ** 2).sum() > 1e-12][0]
    P.append(norm_screen(d.screen(marked, NS)))
    lone = np.zeros((LS, 3), dtype=complex)
    lone[12, I] = 1 / np.sqrt(2)
    lone[14, I] = np.exp(1j * ph) / np.sqrt(2)
    Pref.append(norm_screen(d.screen(d.start(lone, 1), NS)))
Vm, okm = visibility(P)
Vr, okr = visibility(Pref)
good, dev = ratio_ok(Vm, Vr, 1.0, okm & okr)
v1max = 0.0
for ph in PHIS:
    A = r1.joint(amp6(ph), np.array([[1.0, 0, 0]], dtype=complex))
    for w, B in r1.detector_outcomes(A, 0):
        pass
# version 1 contrast: inner visibility per outcome at loci 12 or 14 (screens must match outcome across phases)
outs = []
for ph in PHIS:
    A = r1.joint(amp6(ph), np.array([[1.0, 0, 0]], dtype=complex))
    o = {}
    for w, B in r1.detector_outcomes(A, 0):
        u = int(np.argmax((np.abs(B) ** 2).sum(axis=(1, 2, 3))))
        if u in (12, 14):
            for _ in range(NS):
                B = r1.walk_step_part(B, 0)
            s = r1.part_shares(B, 0)
            o[u] = s / s.sum()
    outs.append(o)
for u in (12, 14):
    Vv, okv = visibility([o[u] for o in outs])
    v1max = max(v1max, float(Vv[okv].max()))
report("D6 draw keeps coherence inside the record", good, "max deviation %.1e; version 1 detector contrast: inner V max %.1e" % (dev, v1max))

# D7 no signalling
F7 = 4  # fragments 0-2 written, axis 3 is partner B
a7 = np.zeros((LS, 3) + (2,) * F7, dtype=complex)
a7[(13, I, 0, 0, 0, 0)] = 1 / np.sqrt(2)
a7[(17, I, 0, 0, 0, 1)] = np.exp(0.3j) / np.sqrt(2)
a7[(14, I, 0, 0, 0, 1)] = 0.2
a7 /= np.sqrt(d.amount(a7))
br, _, _ = d.run(a7, ev5)
rhoB = sum(p * d.reduced(b, 2 + 3) / d.amount(b) for p, b, _ in br)
brn, _, _ = d.run(a7, ev5, r_star=99)
rhoB0 = d.reduced(brn[0][1], 5)
rhoBi = d.reduced(a7, 5)
err = float(max(np.max(np.abs(rhoB - rhoB0)), np.max(np.abs(rhoB - rhoBi))))
report("D7 partner's reduced state unchanged by the draw", len(br) == 2 and err < 1e-12, "draw branches %d; max difference %.1e" % (len(br), err))

# D8 threshold
for R, label in ((2, "D8a two full marks: no draw; joint eraser restores V/V0 = 1"),
                 (3, "D8b three full marks: draw; joint eraser V ~ 0 (stand-in's limit)")):
    ev8 = [("meet", [13], f, np.pi / 2) for f in range(R)]
    runs = screens_for(ev8, R)
    Vu, oku = averaged_V(runs)
    worst_ratio, maxV = 0.0, 0.0
    good_all = True
    for signs in itertools.product((1, -1), repeat=R):
        P = []
        for br, _ in runs:
            tot = 0.0
            acc = np.zeros(LS)
            for p, b, _ in br:
                w, kept = d.erase(b, list(range(R)), signs)
                if w > 0:
                    acc += p * w * norm_screen(d.screen(kept, NS))
                    tot += p * w
            P.append(acc / tot)
        Vc, okc = visibility(P)
        maxV = max(maxV, float(Vc[okc].max()))
        if R == 2:
            good, dev = ratio_ok(Vc, V0, 1.0, okc)
            good_all &= good
            worst_ratio = max(worst_ratio, dev)
    ndraw = max(len(br) for br, _ in runs)
    if R == 2:
        report(label, ndraw == 1 and float(Vu[oku].max()) < 1e-10 and good_all,
               "branches %d; unconditioned V max %.1e; conditioned deviation %.1e" % (ndraw, float(Vu[oku].max()), worst_ratio))
    else:
        report(label, ndraw == 2 and maxV < 1e-10, "branches %d; conditioned V max %.1e" % (ndraw, maxV))

code = results["D1a amount conserved (walk, meet)"] and results["D1b mirror"] and results["D7 partner's reduced state unchanged by the draw"]
print("\nCODE CHECKS PASS" if code else "\nCODE CHECKS FAIL")
allright = all(results.values())
print("RECORDED RESULTS REPRODUCE (all ten right, as in run 2)" if allright else "RECORDED RESULTS DO NOT REPRODUCE")
sys.exit(0 if code and allright else 1)
