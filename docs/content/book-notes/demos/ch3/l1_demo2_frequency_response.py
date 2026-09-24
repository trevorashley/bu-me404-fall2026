"""
L1 Demo 2  --  Frequency response, transient and steady state    (Examples 3.6, 3.7)

For H(s) = 1/(s + 1) the book claims that a sinusoid in gives a sinusoid out,
same frequency, amplitude scaled by |H(j w)| and phase shifted by arg H(j w).
Example 3.7 drives it with sin(10 t) 1(t) and reports an amplitude of
1/sqrt(101) = 0.0995 and a lag of 84.2 degrees, on top of a decaying transient
(10/101) e^-t that the frequency-response formula alone does not predict.

This script simulates the switched-on sinusoid from rest and measures both.

Run:  uv run python ch3/l1_demo2_frequency_response.py
"""

import numpy as np
from scipy.integrate import solve_ivp

import kit as dk

K = 1.0
W = 10.0          # input frequency, rad/s (Example 3.7)


def H(s):
    return 1.0 / (s + K)


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L1 Demo 2 -- amplitude ratio and phase, measured rather than quoted")

    M = abs(H(1j * W))
    phi = np.angle(H(1j * W))
    dk.note(
        f"H(s) = 1/(s + {K:g}). At w = {W:g} rad/s the transfer function evaluates to "
        f"H(j{W:g}) = {H(1j*W).real:+.6f} {H(1j*W).imag:+.6f}j, so the predicted "
        f"amplitude ratio is M = {M:.6f} = 1/sqrt({1 + W**2:.0f}) and the predicted "
        f"phase is {np.degrees(phi):.2f} degrees.")

    dk.section("the frequency-response table (this is Fig. 3.4, three rows of it)")
    rows = []
    for w in [0.01, 0.1, 1.0, 10.0, 100.0]:
        Hj = H(1j * w)
        rows.append([f"{w:g}", f"{abs(Hj):.6f}",
                     f"{np.degrees(np.angle(Hj)):+.2f}",
                     f"{-np.degrees(np.arctan2(w, K)):+.2f}"])
    dk.table(["w [rad/s]", "|H(jw)|", "arg H(jw) [deg]", "-atan(w/k) [deg]"], rows)

    # ------------------------------------------------ simulate from rest
    t = np.linspace(0.0, 10.0, 40001)
    sol = solve_ivp(lambda tt, y: np.sin(W * tt) - K * y[0], (0.0, t[-1]), [0.0],
                    t_eval=t, rtol=1e-11, atol=1e-13, max_step=0.002)
    y = sol.y[0]

    y_transient = (W / (K**2 + W**2)) * np.exp(-K * t)
    y_steady = M * np.sin(W * t + phi)
    y_closed = y_transient + y_steady

    dk.section("the closed form of Example 3.7 against the simulation")
    print(f"\n  max |simulated - (transient + steady state)| = "
          f"{np.max(np.abs(y - y_closed)):.3e}")

    # measure the steady-state amplitude and lag after the transient has gone
    late = t > 8.0
    t_late, y_late = t[late], y[late]
    amp_measured = 0.5 * (y_late.max() - y_late.min())

    def last_up_crossing(time, sig):
        i = np.where((sig[:-1] < 0) & (sig[1:] >= 0))[0][-1]
        frac = -sig[i] / (sig[i + 1] - sig[i])
        return time[i] + frac * (time[i + 1] - time[i])

    dt_lag = last_up_crossing(t_late, y_late) - last_up_crossing(t_late, np.sin(W * t_late))
    lag_deg = -np.degrees(dt_lag * W)

    dk.table(["quantity", "predicted", "measured"],
             [["steady-state amplitude", f"{M:.6f}", f"{amp_measured:.6f}"],
              ["phase shift [deg]", f"{np.degrees(phi):+.2f}", f"{lag_deg:+.2f}"],
              ["transient coefficient", f"{W/(K**2+W**2):.6f}",
               f"{y_transient[0]:.6f}"]])

    dk.note(
        "The steady-state numbers come straight off H(j w). The transient does not: "
        "it is there because the sinusoid was switched on at t = 0 with the system at "
        "rest, and it decays at the rate set by the pole at s = -1. Frequency response "
        "describes what is left after that.")

    # ------------------------------------------------------------------ figure
    fig = plt.figure(figsize=(13.5, 8.0))
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    ax1.plot(t, y, color="k", lw=2.6, alpha=0.4, label="$y$ (simulated)")
    ax1.plot(t, y_transient, color=dk.C["red"], lw=1.8,
             label=r"$y_1 = \frac{10}{101}e^{-t}$ (transient)")
    ax1.plot(t, y_steady, color=dk.C["blue"], lw=1.6,
             label=r"$y_2 = \frac{1}{\sqrt{101}}\sin(10t+\varphi)$")
    ax1.set_xlim(0, 2.5)
    ax1.set_xlabel("time [s]")
    ax1.set_ylabel("output")
    ax1.set_title("Fig. 3.5(a): transient + steady state")
    ax1.legend(loc="upper right", fontsize=10)

    ax2.plot(t, np.sin(W * t), color=dk.C["grey"], lw=1.6, label="input $\\sin 10t$")
    ax2.plot(t, y / M, color=dk.C["blue"], lw=2.0,
             label="output, rescaled by $1/M$")
    ax2.set_xlim(8.0, 9.2)
    ax2.set_xlabel("time [s]")
    ax2.set_title(f"Fig. 3.5(b): output lags by {abs(lag_deg):.1f}$^\\circ$")
    ax2.legend(loc="upper right", fontsize=10)

    w = np.logspace(-2, 2, 400)
    ax3.loglog(w, np.abs(H(1j * w)), color=dk.C["blue"])
    ax3.plot([W], [M], "o", color=dk.C["red"], ms=9)
    ax3.set_xlabel("$\\omega$ [rad/s]")
    ax3.set_ylabel("$|H(j\\omega)|$")
    ax3.set_title("Fig. 3.4: magnitude")

    ax4.semilogx(w, np.degrees(np.angle(H(1j * w))), color=dk.C["blue"])
    ax4.plot([W], [np.degrees(phi)], "o", color=dk.C["red"], ms=9)
    ax4.set_xlabel("$\\omega$ [rad/s]")
    ax4.set_ylabel("phase [deg]")
    ax4.set_title("Fig. 3.4: phase")

    fig.suptitle("Sinusoid in, sinusoid out -- plus a transient nobody ordered",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo2_frequency_response", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
