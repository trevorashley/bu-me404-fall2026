"""
PID control Demo 1  --  Proportional control: one knob, and what it cannot reach
                                                        (Section 4.3.1, Fig. 4.7)

The plant is the second-order motor model of Eq. (4.58),

    G(s) = A / (s^2 + a1 s + a2),    A = 1, a1 = 1.4, a2 = 1,

under unity feedback with D_c = k_P. The closed-loop characteristic
polynomial is s^2 + a1 s + (a2 + k_P A): the gain sets the constant term only.
Every closed-loop pole therefore keeps the real part -a1/2 = -0.7 while the
gain slides it up the s-plane. Steady-state error falls as 1/(1 + k_P) and
damping falls with it.

Run:  uv run python ch4/l2_demo1_proportional.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

A, A1, A2 = 1.0, 1.4, 1.0
GAINS = [0.5, 1.5, 6.0, 20.0]


def closed_loop(kP):
    return lti([kP * A], [1.0, A1, A2 + kP * A])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("PID control Demo 1 -- proportional control of G = 1/(s^2 + 1.4 s + 1)")

    dk.note(
        "Closed loop: s^2 + 1.4 s + (1 + k_P). The gain appears only in the constant "
        "term, so omega_n = sqrt(1 + k_P) rises and zeta = 0.7/omega_n falls. The real "
        "part of the poles is pinned at -0.7 whatever k_P is.")

    dk.section("error, damping and overshoot against gain")
    t = np.linspace(0, 10, 5001)
    rows, traces = [], {}
    for kP in GAINS:
        sys = closed_loop(kP)
        _, y = step(sys, T=t)
        traces[kP] = y
        wn = np.sqrt(A2 + kP * A)
        zeta = A1 / (2 * wn)
        yss = kP * A / (A2 + kP * A)
        overshoot = 100 * (y.max() - yss) / yss
        poles = np.roots([1.0, A1, A2 + kP * A])
        rows.append([f"{kP:g}", f"{yss:.4f}", f"{1 - yss:.4f}", f"{wn:.3f}",
                     f"{zeta:.3f}", f"{overshoot:.1f}%",
                     dk.fmt_root(poles[0], 3)])
    dk.table(["k_P", "y(inf)", "e(inf)", "omega_n", "zeta", "overshoot",
              "pole"], rows)

    dk.note(
        "Fig. 4.7 shows k_P = 1.5 and 6: final values 0.6 and 0.857, peaks 0.727 and "
        "1.219. Quadrupling the gain cuts the error from 0.4 to 0.143 but doubles the "
        "overshoot. The 1% settling estimate 4.6/sigma = 4.6/0.7 = 6.6 s cannot be "
        "improved by any k_P, because sigma does not depend on it.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.6))
    colours = [dk.C["sky"], dk.C["blue"], dk.C["orange"], dk.C["red"]]
    for kP, c in zip(GAINS, colours):
        axL.plot(t, traces[kP], color=c, label=f"$k_P$ = {kP:g}")
        yss = kP / (1 + kP)
        axL.axhline(yss, color=c, ls=":", lw=1.2)
    axL.axhline(1.0, color="k", ls="--", lw=1.0, label="$r$ = 1")
    axL.set_xlabel("time [s]")
    axL.set_ylabel("$y(t)$")
    axL.set_title("Step responses (dotted: final values)")
    axL.legend(fontsize=10.5, loc="lower right")

    kk = np.linspace(0, 25, 400)
    locus = np.array([np.roots([1.0, A1, A2 + k * A]) for k in kk])
    dk.splane(axR, xlim=(-2.0, 0.6), ylim=(-5.2, 5.2))
    axR.plot(locus[:, 0].real, locus[:, 0].imag, color=dk.C["grey"], lw=1.2)
    axR.plot(locus[:, 1].real, locus[:, 1].imag, color=dk.C["grey"], lw=1.2)
    for kP, c in zip(GAINS, colours):
        p = np.roots([1.0, A1, A2 + kP * A])
        axR.plot(p.real, p.imag, "x", ms=12, mew=3, color=c)
    axR.axvline(-0.7, color=dk.C["red"], ls=":", lw=1.2)
    axR.text(-0.68, -4.8, r"$\Re(s)=-a_1/2$", color=dk.C["red"], fontsize=10.5)
    axR.set_title("Closed-loop poles as $k_P$ rises")

    fig.suptitle("Proportional control: less error, less damping", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo1_proportional", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
