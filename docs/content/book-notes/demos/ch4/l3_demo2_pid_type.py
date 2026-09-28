"""
L3 Demo 2  --  The PID examples of L2, re-read in the language of type
                                          (FPE §4.3.1-4.3.2 plant; §4.2.1 ideas)

The plant of FPE Eq. (4.58) with a1 = 1.4, a2 = 1 and a gain A that is allowed
to drift:

    G(s) = A / (s^2 + 1.4 s + 1).

Proportional control, D_c = k_P, gives a Type 0 loop with K_p = k_P A: the step
error 1/(1 + k_P A) is never zero and moves whenever A moves.

Integral control, D_c = k_I / s, gives a Type 1 loop with K_v = k_I A: the step
error is exactly zero for every A that keeps the loop stable, while the ramp
error 1/(k_I A) moves with A. That is the book's claim that type is robust and
error constants are not.

Run:  uv run python ch4/l3_demo2_pid_type.py
"""

import numpy as np
from scipy.signal import lsim, lti

import kit as dk

A_NOM = 1.0
A_VALUES = [0.5, 1.0, 2.0]
KP, KI = 6.0, 0.5


def plant(A):
    return [A], [1.0, 1.4, 1.0]


def loops(A):
    n, d = plant(A)
    return {
        "P": (np.polymul([KP], n), d),                       # Type 0
        "I": (np.polymul([KI], n), np.polymul([1.0, 0.0], d)),  # Type 1
    }


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 2 -- P and I control of the L2 plant, read as Type 0 and Type 1")

    dk.section("the book's P-control gains (Fig. 4.7), A = 1")
    rows = []
    for kp in [1.5, 6.0]:
        rows.append([f"{kp:g}", "0", f"K_p = {kp:g}", f"{1/(1+kp):.4f}"])
    dk.table(["k_P", "type", "error constant", "step e_ss = 1/(1+K_p)"], rows)

    dk.section(f"plant gain A drifts: P (k_P = {KP:g}) against I (k_I = {KI:g})")
    t = np.linspace(0, 80, 16001)
    runs = {}
    rows = []
    for A in A_VALUES:
        L = loops(A)
        for name, (num, den) in L.items():
            char = np.polyadd(den, num)
            roots = np.roots(char)
            S = lti(den, char)
            _, e_step, _ = lsim(S, np.ones_like(t), t)
            _, e_ramp, _ = lsim(S, t, t)
            runs[(name, A)] = (e_step, e_ramp)
            if name == "P":
                pred_step, pred_ramp = 1 / (1 + KP * A), "grows"
            else:
                pred_step, pred_ramp = 0.0, f"{1/(KI*A):.4f}"
            rows.append([f"{A:g}", name, f"{pred_step:.4f}", f"{e_step[-1]:.4f}",
                         pred_ramp, f"{e_ramp[-1]:.4f}",
                         f"{max(roots.real):+.3f}"])
    dk.table(["A", "D_c", "step: table", "step: sim", "ramp: table",
              "ramp: sim (t=80)", "max Re(pole)"], rows)

    dk.note(
        "With the integrator the step error is zero at every A: the zero comes "
        "from the pole of D_c G at s = 0, and no parameter change removes it. The "
        "velocity constant K_v = k_I A, and with it the ramp error, scales with A. "
        "Under P control even the step error depends on A. Integral action is "
        "limited by stability, not by type: the Routh condition for "
        "s^3 + 1.4 s^2 + s + k_I A is 1.4 > k_I A, i.e. A < 2.8 here, and the "
        "A = 2 loop is already lightly damped.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.6))
    colours = {0.5: dk.C["orange"], 1.0: dk.C["blue"], 2.0: dk.C["green"]}
    for A in A_VALUES:
        axL.plot(t, runs[("P", A)][0], color=colours[A], ls="--",
                 label=f"P, A = {A:g}")
        axL.plot(t, runs[("I", A)][0], color=colours[A], label=f"I, A = {A:g}")
        axR.plot(t, runs[("I", A)][1], color=colours[A], label=f"I, A = {A:g}")
        axR.axhline(1 / (KI * A), color=colours[A], ls=":", lw=1.2)
    axL.axhline(0, color="k", lw=0.8)
    axL.set_xlim(0, 40)
    axL.set_ylim(-0.75, 1.05)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("step error $e(t)$")
    axL.set_title(f"Step: P (dashed, $k_P={KP:g}$) keeps an error; I does not")
    axL.legend(fontsize=10, ncol=2)
    axR.axhline(0, color="k", lw=0.8)
    axR.set_xlim(0, 80)
    axR.set_ylim(-0.5, 6)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("ramp error $e(t)$")
    axR.set_title(rf"Ramp under I control: $e_{{ss}}=1/(k_I A)$")
    axR.legend(fontsize=10)
    fig.suptitle(r"$G=A/(s^2+1.4s+1)$: type survives a change in $A$; the error constant does not",
                 fontsize=14)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo2_pid_type", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
