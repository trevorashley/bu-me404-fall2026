"""The heat exchanger of FPE Examples 2.18, 4.9 and 4.10, as a simulator.

Chapter 4 gives only measured curves for this plant. The numerical model is the
one FPE itself uses for the same heat exchanger in Example 7.42 and Problem 6.66:

    G(s) = e^{-5s} / [(10s + 1)(60s + 1)]      (time in seconds)

It reproduces the book's measured ultimate gain (K_u = 15.3) to three figures.

The loop is simulated by exact zero-order-hold discretisation of the lag part
at dt = 0.01 s, with the 5 s transport delay held in a ring buffer. A PID law
of the form u = k_P [ e + (1/T_I) \\int e dt - T_D dy_f/dt ] is used,
with the derivative acting on a filtered measurement (filter time T_D/N).
"""

from __future__ import annotations

import numpy as np
from scipy.signal import cont2discrete

TD_DELAY = 5.0
TAU1, TAU2 = 10.0, 60.0
DT = 0.01

_A = np.array([[-1 / TAU1, 0.0], [1 / TAU2, -1 / TAU2]])
_B = np.array([[1 / TAU1], [0.0]])
_C = np.array([[0.0, 1.0]])
_AD, _BD, *_ = cont2discrete((_A, _B, _C, np.zeros((1, 1))), DT)


def open_loop_step(T: float = 400.0):
    """Unit step response of the plant (the process reaction curve)."""
    t = np.arange(0.0, T, DT)
    a, b = 1 / TAU1, 1 / TAU2
    s = np.clip(t - TD_DELAY, 0.0, None)
    y = 1 - (TAU1 * np.exp(-a * s) - TAU2 * np.exp(-b * s)) / (TAU1 - TAU2)
    y[t < TD_DELAY] = 0.0
    return t, y


def closed_loop(kP: float, TI: float = np.inf, TD: float = 0.0, *, N: float = 10.0,
                T: float = 400.0, r: float = 1.0, impulse: float = 0.0):
    """Closed-loop response to a reference step r (or an input pulse of area
    `impulse` applied over the first sample, for the ultimate-gain test)."""
    n = int(round(T / DT))
    nd = int(round(TD_DELAY / DT))
    x = np.zeros((2, 1))
    buf = np.zeros(nd)
    integ = 0.0
    yf = 0.0
    y = np.zeros(n)
    u = np.zeros(n)
    Tf = TD / N if TD > 0 else 0.0
    for k in range(n):
        yk = float((_C @ x)[0, 0])
        y[k] = yk
        e = r - yk
        if np.isfinite(TI):
            integ += DT * e / TI
        if TD > 0:
            yf_new = yf + DT / (Tf + DT) * (yk - yf)   # backward-Euler first-order filter
            dy = (yf_new - yf) / DT if k > 0 else 0.0
            yf = yf_new
        else:
            dy = 0.0
        uk = kP * (e + integ - TD * dy)
        if k == 0 and impulse:
            uk += impulse / DT
        u[k] = uk
        ud = buf[k % nd]
        buf[k % nd] = uk
        x = _AD @ x + _BD * ud
    return np.arange(n) * DT, y, u


def peaks(t, y):
    """Indices of local maxima, for decay-ratio and period measurements."""
    idx = np.where((y[1:-1] > y[:-2]) & (y[1:-1] >= y[2:]))[0] + 1
    return idx


def ultimate_point():
    """Ultimate gain and period from the phase-crossover frequency."""
    from scipy.optimize import brentq
    phase = lambda w: -TD_DELAY * w - np.arctan(TAU1 * w) - np.arctan(TAU2 * w) + np.pi
    wu = brentq(phase, 1e-3, 1.0)
    mag = 1 / np.sqrt((1 + (TAU1 * wu) ** 2) * (1 + (TAU2 * wu) ** 2))
    return 1 / mag, 2 * np.pi / wu, wu
