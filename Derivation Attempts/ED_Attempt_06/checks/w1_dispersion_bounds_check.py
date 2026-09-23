"""Road W part 1: arithmetic check of the on-paper dispersion bounds (note 2, C4).

Arithmetic only. No model or simulation of ED: the formulas below are the
direction-averaged dispersion of a second-order spreading rule whose hops
point every way, (i) all hops one length l ("shell"), (ii) hops spread evenly
inside a reach r ("ball"), in continuous time and with one-tick (leapfrog)
time steps. Units: hop length or reach = 1, long-wave speed c = 1, x = k*reach.

  continuous:  w_c(x)^2 = A * (1 - g(x)),  g = sinc (shell) or 3 j1(x)/x (ball),
               A = 6 (shell) or 10 (ball), chosen so that w_c ~ x for small x.
  one tick:    (2/tau)^2 sin^2(w tau / 2) = w_c^2,  s = c tau / reach.
  f = w / x  (phase speed over long-wave speed).

Expected results, written down before the first run:
  B1  Continuous time: f < 1 for every x in (0, 60], shell and ball.
      Small-x fit of 1 - f^2 = a x^2 gives a = 1/20 (shell), 1/28 (ball),
      each within 2%.
  B2  General inequality behind B1: 1 - cos y < y^2 / 2 for every y != 0
      (checked on y in [-60, 60] excluding 0).
  B3  One tick, lowest order: 1 - f^2 ~ x^2 (a - s^2/12); the cancel point
      s^2 = 12a is 0.6000 (shell), 0.4286 (ball).
      Stability needs s^2 * A * max(1 - g) <= 4: max(1 - g) = 1.2172 (shell),
      1.0862 (ball), so s^2 <= 0.5477 (shell), 0.3683 (ball), each within 0.002.
      Stability limit is below the cancel point in both cases.
  B4  One tick at the stability limit (and at half of it): f < 1 for every
      x in (0, 60], shell and ball.
"""
import numpy as np

x = np.linspace(1e-3, 60, 600001)


def g_shell(x):
    return np.sin(x) / x


def g_ball(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x**3


cases = {"shell": (g_shell, 6.0, 1 / 20), "ball": (g_ball, 10.0, 1 / 28)}
ok_all = True


def report(name, ok, detail):
    global ok_all
    ok_all &= ok
    print(f"{name}: {'AS EXPECTED' if ok else 'NOT AS EXPECTED'}  {detail}")


# B1
for label, (g, A, a) in cases.items():
    wc2 = A * (1 - g(x))
    f2 = wc2 / x**2
    xs = np.linspace(1e-3, 0.05, 200)
    fit = np.polyfit(xs**2, 1 - A * (1 - g(xs)) / xs**2, 1)[0]
    ok = f2.max() < 1 and abs(fit - a) / a < 0.02
    report(f"B1 {label}", ok, f"max f^2 = {f2.max():.6f}, fitted a = {fit:.5f} (1/{1/fit:.2f})")

# B2
y = np.concatenate([np.linspace(-60, -1e-3, 300000), np.linspace(1e-3, 60, 300000)])
report("B2", bool(np.all(1 - np.cos(y) < y**2 / 2)), f"min of y^2/2 - (1 - cos y) = {np.min(y**2/2 - (1-np.cos(y))):.3e}")

# B3 and B4
xx = np.linspace(1e-3, 20, 2000001)
for label, (g, A, a) in cases.items():
    m = (1 - g(xx)).max()
    s2_stab = 4 / (A * m)
    s2_cancel = 12 * a
    exp_m, exp_stab = {"shell": (1.2172, 0.5477), "ball": (1.0862, 0.3683)}[label]
    ok = abs(m - exp_m) < 0.002 and abs(s2_stab - exp_stab) < 0.002 and s2_stab < s2_cancel
    report(f"B3 {label}", ok, f"max(1-g) = {m:.4f}, s^2 stability = {s2_stab:.4f}, s^2 cancel = {s2_cancel:.4f}")
    worst = []
    for s2 in (s2_stab, s2_stab / 2):
        tau = np.sqrt(s2)
        z = np.clip(tau * np.sqrt(A * (1 - g(x))) / 2, 0, 1)
        f = (2 / tau) * np.arcsin(z) / x
        worst.append(f.max())
    report(f"B4 {label}", max(worst) < 1, f"max f at limit = {worst[0]:.6f}, at half = {worst[1]:.6f}")

print("ALL AS EXPECTED" if ok_all else "SOME NOT AS EXPECTED")
