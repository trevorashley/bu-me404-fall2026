"""
L3 Demo 3  --  A sensor in the loop: tachometer feedback (Example 4.3)
                                                     (FPE §4.2.1, Eqs. 4.39-4.45)

Position servo G = 1/[s(s+1)] (tau = 1), proportional gain k_P = 10, and a
sensor H(s) = 1 + k_t s that adds a tachometer signal to the position signal.
The book's result: the loop is Type 1 with K_v = k_P / (1 + k_t k_P). The
tachometer buys damping and pays for it in velocity constant:

    k_t = 0     s^2 +  s + 10    zeta = 0.158    K_v = 10      ramp error 0.1
    k_t = 0.2   s^2 + 3s + 10    zeta = 0.474    K_v = 3.33    ramp error 0.3

A third case [beyond the book]: the same k_t = 0.2 loop with a position sensor
whose DC gain is 0.98 instead of 1. The loop still contains an integrator, but
T(0) = 1/H(0) = 1/0.98, so the step error is 1 - 1/0.98 = -0.0204 and the ramp
error grows. With a sensor in the loop, type is decided by 1 - T, not by
counting integrators.

Run:  uv run python ch4/l3_demo3_tachometer.py
"""

import numpy as np
from scipy.signal import lsim, lti

import kit as dk

TAU, KP = 1.0, 10.0
G_NUM, G_DEN = [1.0], [TAU, 1.0, 0.0]


def closed_loop(kt, h0=1.0):
    """T = D G / (1 + D G H) with D = k_P and H = h0 (1 + k_t s)."""
    H = np.polymul([h0], [kt, 1.0])
    num = np.polymul([KP], G_NUM)
    den = np.polyadd(G_DEN, np.polymul(num, H))
    return num, den


CASES = [
    ("k_t = 0", 0.0, 1.0, dk.C["red"]),
    ("k_t = 0.2", 0.2, 1.0, dk.C["blue"]),
    ("k_t = 0.2, H(0) = 0.98", 0.2, 0.98, dk.C["purple"]),
]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 3 -- tachometer feedback: damping bought with velocity constant")
    dk.note(
        "With a sensor in the loop the system error is E = R - Y = [1 - T(s)] R, "
        "Eq. (4.42). The error constants must be computed from 1 - T, Eq. (4.45), "
        "because the signal the controller sees, R - H Y, is not the system error.")

    t = np.linspace(0, 20, 20001)
    rows, runs = [], {}
    for label, kt, h0, _ in CASES:
        num, den = closed_loop(kt, h0)
        # 1 - T = (den - num)/den
        E = lti(np.polysub(den, num), den)
        _, e_step, _ = lsim(E, np.ones_like(t), t)
        _, e_ramp, _ = lsim(E, t, t)
        _, y_step, _ = lsim(lti(num, den), np.ones_like(t), t)
        runs[label] = (e_step, e_ramp, y_step)
        roots = np.roots(den)
        wn = np.sqrt(den[2] / den[0])
        zeta = den[1] / den[0] / (2 * wn)
        T0 = num[-1] / den[-1]
        if h0 == 1.0:
            kv = KP / (1 + kt * KP)
            ramp_pred = f"{1/kv:.4f}"
            kv_txt = f"{kv:.4f}"
        else:
            ramp_pred, kv_txt = "grows", "(Type 0)"
        rows.append([label, ", ".join(dk.fmt_root(r, 3) for r in np.sort_complex(roots)),
                     f"{zeta:.3f}", f"{T0:.4f}", f"{1 - T0:+.4f} | {e_step[-1]:+.4f}",
                     kv_txt, f"{ramp_pred} | {e_ramp[-1]:.4f}"])
    dk.table(["case", "closed-loop poles", "zeta", "T(0)", "step e_ss: table | sim",
              "K_v", "ramp e_ss: table | sim(20 s)"], rows)

    dk.note(
        "Adding k_t triples the damping ratio and triples the ramp error: "
        "K_v = k_P/(1 + k_t k_P) = 10/3. The tachometer term vanishes at s = 0, so "
        "H(0) = 1 is preserved and the loop stays Type 1. A 2% calibration error in "
        "the position sensor destroys that: the output settles to 1/0.98 of the "
        "reference, and the ramp error drifts at 1 - 1/0.98 = -0.0204 per unit of "
        "ramp: slowly, but without bound.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.6))
    for label, _, _, colour in CASES:
        e_step, e_ramp, y_step = runs[label]
        ls = ":" if "0.98" in label else "-"
        axL.plot(t, y_step, color=colour, ls=ls, label=label)
        axR.plot(t, e_ramp, color=colour, ls=ls, label=label)
    axL.axhline(1.0, color="k", lw=0.8)
    axL.set_xlim(0, 10)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("step response $y(t)$")
    axL.set_title("Step: the tachometer damps the response")
    axL.legend(fontsize=10.5, loc="lower right")
    axR.axhline(0.1, color=dk.C["red"], ls="--", lw=1.0)
    axR.axhline(0.3, color=dk.C["blue"], ls="--", lw=1.0)
    axR.set_xlim(0, 20)
    axR.set_ylim(-0.5, 0.8)
    axR.axhline(0, color="k", lw=0.8)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("ramp error $e(t)=r-y$")
    axR.set_title(r"Ramp: $1/K_v$ rises from 0.1 to 0.3")
    axR.legend(fontsize=10.5, loc="upper left")
    fig.suptitle(r"Example 4.3: $G=1/[s(s+1)]$, $k_P=10$, $H=1+k_t s$", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo3_tachometer", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
