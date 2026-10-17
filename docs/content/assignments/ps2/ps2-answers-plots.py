"""Generate the figures and numerical checks for the PS2 answer key.

Requires Python 3, NumPy, SciPy, and Matplotlib. Run from any directory:
    python ps2-answers-plots.py

NumPy (np) supplies arrays and element-by-element mathematical operations;
1j is the imaginary unit, ** means exponentiation, and np.real takes the
real part. SciPy supplies quadrature, transfer-function simulation, and a
scalar root finder. Matplotlib supplies plotting commands.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save figures without opening graphical windows.
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.signal import TransferFunction, step


OUT = Path(__file__).resolve().parent / "ps2-answers-figures"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def sawtooth(t):
    """Period 2, with the jump value chosen as -1."""
    return np.mod(t + 1, 2) - 1


def trapezoid(t):
    """Period 6; even about the time origin shown in the problem."""
    r = np.mod(t + 3, 6) - 3
    return np.clip(2 - np.abs(r), 0, 1)


def saw_coefficient(k):
    return 0.0 if k == 0 else 1j * (-1.0)**k / (np.pi * k)


def trapezoid_coefficient(k):
    if k == 0:
        return 0.5
    if k % 2 == 0:
        return 0.0
    return 3 * (np.cos(k*np.pi/3) - np.cos(2*k*np.pi/3)) / (np.pi*k)**2


def output_coefficient(k):
    return saw_coefficient(k) / (1 + 0.5j*k*np.pi)


def fourier_sum(t, N, period, coefficient):
    """Pair conjugate terms: c0 + 2 Re(sum from k=1 to N)."""
    result = np.full_like(t, np.real(coefficient(0)), dtype=float)
    for k in range(1, N + 1):  # Python's range excludes its upper endpoint.
        result += 2*np.real(coefficient(k)*np.exp(1j*k*2*np.pi*t/period))
    return result


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def reconstructions():
    for name, period, original, coefficient in [
        ("sawtooth", 2, sawtooth, saw_coefficient),
        ("trapezoid", 6, trapezoid, trapezoid_coefficient),
    ]:
        t = np.linspace(-period, period, 12001)
        fig, axes = plt.subplots(3, 1, figsize=(8.2, 7.2),
                                 sharex=True, layout="constrained")
        for ax, N in zip(axes, [3, 10, 50]):
            ax.plot(t, original(t), color="0.25", lw=1.5, label="Original")
            ax.plot(t, fourier_sum(t, N, period, coefficient),
                    color="#176ca4", lw=1.3, label=f"N = {N}")
            ax.set_ylabel("Signal x(t)")
            ax.grid(alpha=0.2)
            ax.legend(loc="upper right", ncol=2)
        axes[-1].set_xlabel("Time t (problem time units)")
        axes[-1].set_xlim(-period, period)
        save(fig, f"part-1-{name}.png")

    t = np.linspace(-2, 2, 12001)
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.5), layout="constrained")
    axes[0].plot(t, sawtooth(t), color="0.35", label="Input x(t)")
    axes[0].plot(t, fourier_sum(t, 50, 2, output_coefficient),
                 color="#176ca4", label="Steady-state output, N = 50")
    axes[0].set(xlabel="Time t (s)", ylabel="Voltage (V)", xlim=(-2, 2))
    axes[0].legend(loc="upper right")
    k = np.arange(1, 11)
    # Small horizontal offsets make both stems at each harmonic visible.
    axes[1].stem(k - .08, [abs(saw_coefficient(n)) for n in k],
                 linefmt="C0-", markerfmt="C0o", basefmt=" ", label=r"$|c_k|$")
    axes[1].stem(k + .08, [abs(output_coefficient(n)) for n in k],
                 linefmt="C1-", markerfmt="C1s", basefmt=" ", label=r"$|d_k|$")
    axes[1].set(xlabel="Harmonic index k", ylabel="Individual coefficient magnitude (V)",
                xticks=k)
    axes[1].legend()
    for ax in axes:
        ax.grid(alpha=0.2)
    save(fig, "part-1-rc.png")


def convolution_figure():
    t = np.linspace(-1, 5, 601)
    fig, ax = plt.subplots(figsize=(7.8, 3), layout="constrained")
    ax.plot(t, np.clip(t, 0, 2), lw=2)
    ax.plot([0, 2], [0, 2], "ko")
    ax.annotate("(0, 0)", (0, 0), xytext=(8, 12), textcoords="offset points")
    ax.annotate("(2, 2)", (2, 2), xytext=(-40, -22), textcoords="offset points")
    ax.axhline(2, color="0.5", ls=":", label="Final value = 2")
    ax.set(xlabel="Time t", ylabel="Step response y(t)", xlim=(-1, 5), ylim=(-.2, 2.4))
    ax.grid(alpha=.2)
    ax.legend(loc="lower right")
    save(fig, "part-3-step.png")


def design_figures():
    K, a = 76.25, 95.0
    wn = np.sqrt(25*a + 100*K)
    sigma = (a + 25)/2
    zeta = sigma/wn
    wd = np.sqrt(wn**2 - sigma**2)
    y_final = 100*K/wn**2
    tolerance = 0.01  # Explicitly use the required 1% criterion.
    envelope_time = -np.log(tolerance*np.sqrt(1-zeta**2))/sigma
    system = TransferFunction([100*K], [1, a+25, 25*a+100*K])
    t = np.linspace(0, .3, 30001)  # 10 microseconds; beyond the envelope time.
    t, y = step(system, T=t)

    def exact_response(time):
        return y_final*(1 - np.exp(-sigma*time)*(
            np.cos(wd*time) + sigma/wd*np.sin(wd*time)))

    np.testing.assert_allclose(y, exact_response(t), atol=2e-11, rtol=2e-11)
    outside = np.flatnonzero(np.abs(y-y_final) > tolerance*abs(y_final))
    last = outside[-1]
    assert last < len(t)-1 and t[-1] > envelope_time
    # Refine the last sampled band crossing with the exact response.
    ts = brentq(lambda time: abs(exact_response(time)-y_final)
                - tolerance*abs(y_final), t[last], t[last+1], xtol=1e-14)
    peak_index = np.argmax(y)
    measured_overshoot = 100*(y[peak_index]-y_final)/abs(y_final)
    tp = np.pi/wd
    peak = exact_response(tp)
    predicted_overshoot = 100*np.exp(-sigma*np.pi/wd)
    assert measured_overshoot <= 25 and ts <= .1
    assert abs(measured_overshoot-predicted_overshoot) < 1e-5
    # The second and all later extrema are already inside the 1% band.
    assert np.exp(-2*sigma*np.pi/wd) < tolerance
    assert np.all(np.abs(y[last+1:]-y_final) <= tolerance*abs(y_final))
    print(f"K={K:g}, a={a:g}; poles={np.roots(system.den)}")
    print(f"Final={y_final:.8f}; peak={peak:.8f} at {tp:.8f} s")
    print(f"Overshoot: measured={measured_overshoot:.6f}%, predicted={predicted_overshoot:.6f}%")
    print(f"1% settling: grid bracket=[{t[last]:.8f}, {t[last+1]:.8f}] s")
    print(f"Refined={ts:.10f} s; estimate={4.6/sigma:.8f} s; envelope={envelope_time:.8f} s")

    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.6), layout="constrained")
    for ax in axes:
        ax.plot(t, y, color="#176ca4", lw=1.8, label="Output y(t)")
        ax.axhline(1, color="0.3", ls="--", label="Unit reference")
        ax.axhline(y_final, color="#b85a13", ls="--", label="Final output = 0.7625")
        ax.axhspan(.99*y_final, 1.01*y_final, color="#40a874", alpha=.2, label="1% band")
        ax.axvline(ts, color="#7952a5", ls=":", label=f"Settling: {ts:.5f} s")
        ax.grid(alpha=.2)
        ax.set(xlabel="Time t (s)", ylabel="Output y(t)")
    axes[0].plot(tp, peak, "o", color="#b32733", label=f"Peak = {peak:.5f}")
    axes[0].set(xlim=(0, .3), ylim=(0, 1.08), title="Complete transient from rest")
    axes[0].legend(loc="lower right", ncol=2, fontsize=9)
    axes[1].set(xlim=(.05, .12), ylim=(.748, .783), title="Detail of the final band crossing")
    save(fig, "part-5-response.png")

    zmin = np.log(4)/np.hypot(np.pi, np.log(4))
    slope = np.sqrt(1-zmin**2)/zmin
    re = np.linspace(-180, 0, 1000)
    fig, ax = plt.subplots(figsize=(7.8, 6.5), layout="constrained")
    bound = -slope*re
    ax.fill_between(re, -bound, bound, where=re <= -46,
                    color="#40a874", alpha=.2, label="Approximate design region")
    ax.plot(re, bound, color="#176ca4", label="Exact 25% overshoot boundary")
    ax.plot(re, -bound, color="#176ca4")
    ax.axvline(-46, color="#b85a13", ls="--", label="Approximate settling boundary: Re(s) = -46")
    ax.axhline(0, color="0.4", lw=.8)
    ax.axvline(0, color="0.4", lw=.8)
    ax.plot([-sigma, -sigma], [wd, -wd], "x", color="#b32733", ms=10,
            mew=2, label="Selected poles: -60 +/- 80j")
    ax.set(xlim=(-180, 12), ylim=(-120, 120), xlabel="Re(s) (1/s)", ylabel="Im(s) (rad/s)")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=.2)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.02), fontsize=9)
    save(fig, "part-5-region.png")


def check_fourier_coefficients():
    """Compare formulas to numerical integration of the original waveforms."""
    for original, coefficient, period, points in [
        (sawtooth, saw_coefficient, 2, [-1, 1]),
        (trapezoid, trapezoid_coefficient, 6, [-3, -2, -1, 1, 2, 3]),
    ]:
        for k in range(-12, 13):
            f = lambda time: original(time)*np.exp(-1j*k*2*np.pi*time/period)/period
            value = sum(quad(lambda time: np.real(f(time)), lo, hi, epsabs=1e-12)[0]
                        + 1j*quad(lambda time: np.imag(f(time)), lo, hi, epsabs=1e-12)[0]
                        for lo, hi in zip(points[:-1], points[1:]))
            np.testing.assert_allclose(value, coefficient(k), atol=1e-12)
            np.testing.assert_allclose(coefficient(-k), np.conj(coefficient(k)), atol=1e-14)
    # Independent piecewise ODE solution for the periodic RC output.
    t = np.linspace(-2, 2, 12001)
    r = sawtooth(t)
    exact = r - .5 + 2*np.exp(-2*(r+1))/(1-np.exp(-4))
    error = np.max(np.abs(fourier_sum(t, 50, 2, output_coefficient)-exact))
    assert error < .009  # Finite-series error is largest near the slope jumps.
    print(f"Fourier coefficients verified by quadrature; RC N=50 max error={error:.6g} V")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    check_fourier_coefficients()
    reconstructions()
    convolution_figure()
    design_figures()
