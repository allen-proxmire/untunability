"""Check C44: a localized wave spreads at a rate set by hbar/m.

For a free wave with |psi(x, 0)|^2 of standard deviation s0,
    s(t) = s0 * sqrt(1 + (hbar * t / (2 * m * s0**2))**2).
The script evolves the wave exactly in Fourier space and compares the measured
width with this formula for several masses. Heavier things spread less between
ticks, so the next draw lands closer to the last one.
"""
import sys
import numpy as np

HBAR = 1.0
n, length = 8192, 400.0
x = (np.arange(n) - n // 2) * (length / n)
k = 2 * np.pi * np.fft.fftfreq(n, d=length / n)


def width(psi):
    p = np.abs(psi) ** 2
    p /= p.sum()
    mean = (x * p).sum()
    return np.sqrt(((x - mean) ** 2 * p).sum())


ok = True
s0 = 1.0
psi0 = np.exp(-x ** 2 / (4 * s0 ** 2)).astype(complex)
for m in (0.5, 1.0, 4.0):
    for t in (1.0, 5.0, 20.0):
        psi = np.fft.ifft(np.fft.fft(psi0) * np.exp(-1j * HBAR * k ** 2 * t / (2 * m)))
        predicted = s0 * np.sqrt(1 + (HBAR * t / (2 * m * s0 ** 2)) ** 2)
        measured = width(psi)
        err = abs(measured - predicted) / predicted
        ok &= err < 1e-3
        print("m %.1f  t %5.1f  predicted %.4f  measured %.4f" % (m, t, predicted, measured))

print("C44 holds" if ok else "C44 FAILED")
sys.exit(0 if ok else 1)
