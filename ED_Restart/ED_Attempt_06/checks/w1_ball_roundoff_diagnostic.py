"""Follow-up diagnostic for w1_dispersion_bounds_check.py (NOT pre-registered).

Run 1 gave B1 ball and B4 ball NOT AS EXPECTED (max f^2 = 1.0029, fitted
a = 1/27.08). Those verdicts stand. This script only asks where the excess
sits and whether it survives a numerically stable form of the same formula.
Stable form: power series of 1 - g(x) for x < 1, closed form above.
  shell: f_c^2 = 6 * sum_{n>=1} (-1)^(n+1) x^(2n-2) / (2n+1)!
  ball:  f_c^2 = sum_{n>=2} (-1)^n 60 n x^(2n-4) / (2n+1)!
"""
from math import factorial
import numpy as np

x = np.linspace(1e-3, 60, 600001)


def fc2_naive(label, x):
    if label == "shell":
        return 6 * (1 - np.sin(x) / x) / x**2
    return 10 * (1 - 3 * (np.sin(x) - x * np.cos(x)) / x**3) / x**2


def fc2_stable(label, x):
    out = fc2_naive(label, x)
    s = x < 1
    xs = x[s]
    if label == "shell":
        ser = sum((-1) ** (n + 1) * 6 * xs ** (2 * n - 2) / factorial(2 * n + 1) for n in range(1, 14))
    else:
        ser = sum((-1) ** n * 60 * n * xs ** (2 * n - 4) / factorial(2 * n + 1) for n in range(2, 15))
    out[s] = ser
    return out


for label, A, s2 in (("shell", 6.0, 0.5477), ("ball", 10.0, 0.3683)):
    naive = fc2_naive(label, x)
    i = int(np.argmax(naive))
    stable = fc2_stable(label, x)
    xs = np.linspace(1e-3, 0.05, 200)
    fit = np.polyfit(xs**2, 1 - fc2_stable(label, xs), 1)[0]
    print(f"{label}: naive max f^2 = {naive.max():.6f} at x = {x[i]:.4f}; "
          f"stable max f^2 = {stable.max():.12f} at x = {x[int(np.argmax(stable))]:.4f}; stable fit a = 1/{1/fit:.3f}")
    for ss in (s2, s2 / 2):
        tau = np.sqrt(ss)
        z = np.clip(tau * x * np.sqrt(stable) / 2, 0, 1)
        f = (2 / tau) * np.arcsin(z) / x
        print(f"   one tick s^2 = {ss:.4f}: stable max f = {f.max():.12f} at x = {x[int(np.argmax(f))]:.4f}")
