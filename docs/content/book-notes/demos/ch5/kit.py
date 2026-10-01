"""Chapter 5 plotting style and numerical helpers; coefficients descend in s."""
from pathlib import Path
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch2"))
import demokit
from demokit import *  # noqa: F401,F403

demokit.FIGDIR = Path(__file__).parent / "figures"
SETTLING_BAND = 0.01  # Course/FPE convention; relative to the final value.


def closed_loop(num, den, gain=1.0):
    """Negative unity feedback, without cancelling poles and zeros."""
    num = gain * np.asarray(num, dtype=float)
    return signal.TransferFunction(num, np.polyadd(den, num))


def locus(ax, num, den, gains, *, xlim, ylim, title_text):
    """Plot all roots as dots: no arbitrary connection across repeated roots."""
    poles = np.roots(den)
    zeros = np.roots(num)
    splane(ax, poles, zeros, xlim=xlim, ylim=ylim, title_text=title_text)
    # The equal-aspect s-plane can be narrow; omit the generic corner labels
    # rather than allowing "LHP" and "RHP" to overlap above the origin.
    for label in list(ax.texts):
        label.remove()
    roots = np.array([np.roots(np.polyadd(den, k*np.asarray(num))) for k in gains])
    ax.plot(roots.real.ravel(), roots.imag.ravel(), ".", color=C["blue"], ms=1.6,
            alpha=0.5, label="roots as K increases")
    ax.set_aspect("equal", adjustable="box")
    return roots


def gain_arrows(ax, num, den, k1, k2):
    """Arrows between nearby, matched roots away from multiple-root points."""
    from scipy.optimize import linear_sum_assignment
    r1 = np.roots(np.polyadd(den, k1*np.asarray(num)))
    r2 = np.roots(np.polyadd(den, k2*np.asarray(num)))
    rows, columns = linear_sum_assignment(abs(r1[:, None]-r2[None, :]))
    for i, j in zip(rows, columns):
        ax.annotate("", xy=(r2[j].real, r2[j].imag),
                    xytext=(r1[i].real, r1[i].imag),
                    arrowprops={"arrowstyle": "->", "color": C["blue"], "lw": 2},
                    zorder=5)


def metrics(system, t, eps=SETTLING_BAND):
    """Sampled 10-90% rise, peak overshoot, and last settling-band entry (1% by default).

    An unsettled final sample raises an error instead of reporting a false
    settling time. These demos also choose horizons from their slowest poles.
    """
    if np.max(np.roots(system.den).real) >= 0:
        raise ValueError("Transient metrics require a stable closed loop")
    _, y = signal.step(system, T=t)
    final = system.num[-1] / system.den[-1]
    yn = y / final
    t10 = t[np.flatnonzero(yn >= .1)[0]]
    t90 = t[np.flatnonzero(yn >= .9)[0]]
    outside = np.flatnonzero(abs(yn-1) > eps)
    if len(outside) and outside[-1] == len(t)-1:
        raise ValueError("Increase the simulation horizon")
    settling = t[outside[-1]+1] if len(outside) else 0
    return y, [100*max(0, yn.max()-1), t90-t10, settling]


def response_table(systems, t):
    rows = []
    traces = {}
    for name, system in systems.items():
        y, numbers = metrics(system, t)
        traces[name] = y
        rows.append([name, *(f"{x:.4f}" for x in numbers)])
        print(name, "poles:", ", ".join(fmt_root(p) for p in np.roots(system.den)))
    table(["design", "overshoot [%]", "rise 10-90% [s]", "settling 1% [s]"], rows)
    return traces
