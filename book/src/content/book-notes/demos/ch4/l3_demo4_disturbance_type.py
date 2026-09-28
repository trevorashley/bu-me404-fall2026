"""
L3 Demo 4  --  Type with respect to a disturbance (Example 4.4)
                                                     (FPE §4.2.2, Eqs. 4.46-4.54)

The DC motor of Fig. 4.6: plant A/[s(tau s + 1)], a load torque W entering
through B/A at the plant input, unity feedback. Numbers chosen here
[beyond the book]: A = 2, B = 1, tau = 0.5, k_P = 2, k_I = 1.

    P:   T_w = -B / [s(tau s+1) + A k_P]                    Type 0 to W
         unit-step torque   ->  e_ss = -B/(A k_P) = -0.25
    PI:  T_w = -B s / [s^2(tau s+1) + A(k_P s + k_I)]       Type 1 to W
         unit-step torque   ->  e_ss = 0
         unit-ramp torque   ->  e_ss = -B/(A k_I) = -0.5

The same P loop is Type 1 to the reference (K_v = A k_P = 4), and the PI loop is
Type 2 to the reference (K_a = A k_I = 2). The integrator in the plant counts for
the reference but not for a disturbance that enters upstream of it.

Run:  uv run python ch4/l3_demo4_disturbance_type.py
"""

import numpy as np
from scipy.signal import lsim, lti

import kit as dk

A, B, TAU, KP, KI = 2.0, 1.0, 0.5, 2.0, 1.0
PLANT_DEN = [TAU, 1.0, 0.0]          # s(tau s + 1)


def disturbance_to_error(ctrl):
    """E/W = -(B/A) G / (1 + D G), G = A/[s(tau s+1)], as (num, den)."""
    if ctrl == "P":
        return [-B], np.polyadd(PLANT_DEN, [A * KP])
    # PI: multiply through by s
    return [-B, 0.0], np.polyadd(np.polymul([1.0, 0.0], PLANT_DEN), [A * KP, A * KI])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 4 -- a load torque on a DC motor: which integrator counts?")
    dk.note(
        "With R = 0, E = -Y, and E/W = T_w(s) = s^n T_o,w(s). A step torque leaves "
        "e_ss = T_w(0); a ramp torque leaves lim T_w(s)/s. Type to W is the number "
        "of zeros of T_w at s = 0, which is the number of controller integrators "
        "upstream of the disturbance entry point.")

    t = np.linspace(0, 25, 12501)
    runs, rows = {}, []
    for ctrl in ["P", "PI"]:
        num, den = disturbance_to_error(ctrl)
        Tw = lti(num, den)
        _, e_step, _ = lsim(Tw, np.ones_like(t), t)
        _, e_ramp, _ = lsim(Tw, t, t)
        runs[ctrl] = (e_step, e_ramp)
        roots = np.roots(den)
        if ctrl == "P":
            pred = (-B / (A * KP), "grows")
            ref = f"Type 1, K_v = {A*KP:g}"
        else:
            pred = (0.0, f"{-B/(A*KI):+.4f}")
            ref = f"Type 2, K_a = {A*KI:g}"
        rows.append([ctrl, ", ".join(dk.fmt_root(r, 3) for r in np.sort_complex(roots)),
                     f"{pred[0]:+.4f} | {e_step[-1]:+.4f}",
                     f"{pred[1]} | {e_ramp[-1]:+.4f}", ref])
    dk.table(["D_c", "closed-loop poles", "step W: table | sim",
              "ramp W: table | sim(25 s)", "to the reference"], rows)

    dk.note(
        "Same loop, two types. Under P control the plant's integrator makes the "
        "loop Type 1 for the reference, but a constant torque still leaves a "
        "constant position error: the motor must be displaced by B/(A k_P) so that "
        "the proportional term can push back. The PI integrator sits upstream of "
        "the torque, so it builds the cancelling torque without needing an error.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.6))
    axL.plot(t, runs["P"][0], color=dk.C["red"], label=r"P: $e_{ss}=-B/(Ak_P)=-0.25$")
    axL.plot(t, runs["PI"][0], color=dk.C["blue"], label=r"PI: $e_{ss}=0$")
    axL.axhline(-0.25, color=dk.C["red"], ls="--", lw=1.0)
    axL.axhline(0, color="k", lw=0.8)
    axL.set_xlim(0, 12)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("error $e=-y$")
    axL.set_title("Unit-step load torque")
    axL.legend(fontsize=11, loc="lower right")

    axR.plot(t, runs["P"][1], color=dk.C["red"], label="P: grows")
    axR.plot(t, runs["PI"][1], color=dk.C["blue"], label=r"PI: $e_{ss}=-B/(Ak_I)=-0.5$")
    axR.axhline(-0.5, color=dk.C["blue"], ls="--", lw=1.0)
    axR.axhline(0, color="k", lw=0.8)
    axR.set_ylim(-3, 0.3)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("error $e=-y$")
    axR.set_title("Unit-ramp load torque")
    axR.legend(fontsize=11, loc="lower left")
    fig.suptitle(r"Example 4.4 with $A=2$, $B=1$, $\tau=0.5$, $k_P=2$, $k_I=1$", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo4_disturbance_type", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
