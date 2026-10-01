"""
PID tuning and implementation Demo 4  --  Where the derivative acts: kick, filtering and setpoint weighting
                                      (FPE Fig. 4.10; AM Section 11.5)

Plant G(s) = 1/(s^2 + 1.4 s + 1)  (Eq. 4.58 with a1 = 1.4, a2 = 1, A = 1),
PID gains k_P = 6, k_I = 6, k_D = 2, derivative filtered with time constant
T_f = T_D/N, N = 10, T_D = k_D/k_P.

The controller is written in two-degree-of-freedom form,

    U = [b k_P + k_I/s + c k_D s/(1 + s T_f)] R  -  [k_P + k_I/s + k_D s/(1 + s T_f)] Y,

and four implementations of "the same" PID are compared:

    (a) b = 1, c = 1 : everything acts on the error         (Fig. 4.10b)
    (b) b = 1, c = 0 : derivative on the output only          (Fig. 4.10a)
    (c) b = 0, c = 0 : proportional and derivative on output  ("I-PD")
    (d) as (a), but with the ideal, unfiltered derivative (for the kick size)

All four have the SAME feedback path, hence the same closed-loop poles and
the same response to disturbances and noise. They differ only in the zeros
from R to Y and in the control effort after a reference step.

Run:  uv run python ch4/l4_demo4_derivative_kick.py
"""

import control as ct
import numpy as np

import kit as dk

KP, KI, KD, N = 6.0, 6.0, 2.0, 10.0
TD = KD / KP
TF = TD / N


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("PID tuning and implementation Demo 4 -- same poles, different zeros: where to put the derivative")

    s = ct.tf("s")
    G = 1 / (s**2 + 1.4 * s + 1)
    Dfilt = KD * s / (1 + s * TF)
    Cy = KP + KI / s + Dfilt

    variants = {
        "(a) PID on error":         (1.0, 1.0),
        "(b) D on output":          (1.0, 0.0),
        "(c) P and D on output":    (0.0, 0.0),
    }
    t = np.linspace(0, 10, 20001)
    runs, rows = {}, []
    den_ref = None
    for name, (b, c) in variants.items():
        Cr = b * KP + KI / s + c * Dfilt
        T = ct.minreal(Cr * G / (1 + Cy * G), verbose=False)
        UR = ct.minreal(Cr / (1 + Cy * G), verbose=False)
        ry = ct.step_response(T, t)
        ru = ct.step_response(UR, t)
        y, u = ry.outputs, ru.outputs
        runs[name] = (y, u)
        poles = np.sort_complex(T.poles())
        zeros = np.sort_complex(T.zeros())
        if den_ref is None:
            den_ref = poles
        rows.append([name, f"{u[0]:.2f}", f"{np.max(np.abs(u)):.2f}",
                     f"{100 * (y.max() - 1):.1f}%", f"{y[-1]:.4f}",
                     ", ".join(dk.fmt_root(z, 3) for z in zeros) or "none"])
    dk.table(["implementation", "u(0+)", "max |u|", "overshoot", "y(10)", "zeros R->Y"], rows)

    dk.section("closed-loop poles (identical in every case)")
    print("  " + ", ".join(dk.fmt_root(p, 3) for p in den_ref))
    ideal = np.roots([1, 1.4 + KD, 1 + KP, KI])
    print("  ideal-derivative characteristic polynomial s^3 + 3.4 s^2 + 7 s + 6 has roots")
    print("  " + ", ".join(dk.fmt_root(p, 3) for p in np.sort_complex(ideal)))
    print(f"  the fourth pole near -1/T_f = {-1 / TF:.1f} is the derivative filter's")

    dk.section("the size of the kick")
    dk.note(
        f"With the derivative on the error, a unit reference step makes u(0+) = "
        f"b k_P + k_D/T_f = k_P (1 + N) = {KP * (1 + N):.0f}. With the ideal derivative "
        "the kick is an impulse of area k_D: u(0+) is unbounded. Moving the derivative "
        f"to the output leaves u(0+) = k_P = {KP:.0f}; weighting the setpoint with b = 0 "
        "as well leaves u(0+) = 0, and only the integrator responds to the step at first.")

    dk.note(
        "Removing the kick is not free, and it is not monotone. (b) removes the "
        "derivative's complex zero pair but leaves the proportional zero at -k_I/k_P = -1, "
        "slow and close to the poles: overshoot rises from 18.9% to 31.9%. (c) removes "
        "that zero too: overshoot falls to 2.9% but the 10-90% rise time grows from "
        "0.47 s to 1.32 s. The feedback loop, the disturbance response and the noise "
        "response are the same in all three; only the reference path changed.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.4))
    colours = [dk.C["red"], dk.C["blue"], dk.C["green"]]
    for (name, (y, u)), colour in zip(runs.items(), colours):
        axL.plot(t, y, color=colour, label=name)
        axR.plot(t, u, color=colour, label=name)
    axL.axhline(1.0, ls=":", color="k", lw=1.0)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("$y$")
    axL.set_title("Output after a unit reference step")
    axL.legend(fontsize=10.5, loc="lower right")
    axR.set_yscale("symlog", linthresh=10)
    axR.set_xlim(0, 4)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("$u$  (symmetric log scale above 10)")
    axR.set_title(f"Control effort: the derivative kick ($N$ = {N:g})")
    axR.legend(fontsize=10.5, loc="upper right")
    fig.suptitle(r"PID on $1/(s^2+1.4s+1)$, $k_P$ = 6, $k_I$ = 6, $k_D$ = 2: "
                 "same loop, three reference paths", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo4_derivative_kick", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
