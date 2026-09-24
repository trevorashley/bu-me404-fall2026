"""
Demo 3  --  Where did the j go?                                  (lecture §7.5)

Complex poles come in conjugate pairs, and for a real signal the coefficients
must be conjugates too. Then the imaginary parts cancel exactly and what is
left is e^{sigma t}(B cos wd t + C sin wd t).

This is lecture Problem 6: poles at -1 +/- 3j, x(0) = 2, x'(0) = 0.

Run:  uv run python demo3_real_from_complex.py
"""

import numpy as np
from scipy.integrate import solve_ivp

import demokit as dk

S1 = -1.0 + 3.0j          # the pole pair
X0, V0 = 2.0, 0.0         # initial conditions


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    sigma, wd = S1.real, S1.imag
    den = np.poly([S1, np.conj(S1)]).real          # s^2 + 2s + 10
    dk.title("Demo 3 -- a conjugate pair of complex modes makes one real motion")
    dk.note(
        f"Poles at s = {dk.fmt_root(S1)} and its conjugate, so the characteristic "
        f"polynomial is s^2 + {den[1]:.0f}s + {den[2]:.0f} = 0, i.e. the ODE is "
        f"x'' + {den[1]:.0f}x' + {den[2]:.0f}x = 0.")

    # Solve for the complex amplitude A1 from the initial conditions.
    #   x(t)     = A1 e^{s1 t} + conj(A1) e^{conj(s1) t} = 2 Re{A1 e^{s1 t}}
    #   x(0)     = 2 Re{A1}          = X0
    #   x'(0)    = 2 Re{A1 s1}       = V0
    a, b = np.linalg.solve(np.array([[2.0, 0.0],
                                     [2 * sigma, -2 * wd]]), np.array([X0, V0]))
    A1 = complex(a, b)

    dk.section("the complex amplitude, fixed by the initial conditions")
    print(f"  A1        = {dk.fmt_root(A1, 6)}")
    print(f"  conj(A1)  = {dk.fmt_root(np.conj(A1), 6)}")
    B, Cc = 2 * A1.real, -2 * A1.imag
    print(f"\n  so   x(t) = 2 Re[A1 e^(s1 t)] = e^({sigma:g}t) "
          f"({B:.4f} cos {wd:g}t + {Cc:.4f} sin {wd:g}t)")
    print(f"  compare the lecture's Problem 6 answer:  e^(-t)(2 cos 3t + 0.6667 sin 3t)")

    # ------------------------------------------------------- numerical check
    t = np.linspace(0, 6, 3000)
    mode1 = A1 * np.exp(S1 * t)
    mode2 = np.conj(A1) * np.exp(np.conj(S1) * t)
    total = mode1 + mode2
    closed = np.exp(sigma * t) * (B * np.cos(wd * t) + Cc * np.sin(wd * t))

    sol = solve_ivp(lambda tt, z: [z[1], -den[1] * z[1] - den[2] * z[0]],
                    (0, t[-1]), [X0, V0], t_eval=t, rtol=1e-11, atol=1e-13)

    dk.section("three independent routes to the same real motion")
    print(f"  max |Im( mode1 + mode2 )|                    = {np.max(np.abs(total.imag)):.3e}"
          "   <- the j cancels to machine precision")
    print(f"  max |sum of modes  -  closed form|           = "
          f"{np.max(np.abs(total.real - closed)):.3e}")
    print(f"  max |closed form   -  numerical ODE solve|   = "
          f"{np.max(np.abs(closed - sol.y[0])):.3e}")

    dk.note(
        "Each mode on its own is complex and has no physical meaning. Neither one is a "
        "motion the mass could perform. Only the pair is real -- and once added, the "
        "envelope e^{sigma t} comes from the real part of s and the ringing from the "
        "imaginary part, exactly as §7.4 claims.")

    # ------------------------------------------------------------------ figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 8), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 1]})

    ax1.plot(t, mode1.real, color=dk.C["blue"], lw=1.8,
             label=r"$\Re\{A_1 e^{s_1 t}\}$")
    ax1.plot(t, mode1.imag, "--", color=dk.C["blue"], lw=1.6,
             label=r"$\Im\{A_1 e^{s_1 t}\}$")
    ax1.plot(t, mode2.imag, ":", color=dk.C["red"], lw=2.4,
             label=r"$\Im\{\bar A_1 e^{\bar s_1 t}\}$  (equal and opposite)")
    ax1.axhline(0, color="k", lw=1)
    ax1.set_ylabel("individual modes")
    ax1.set_title("Each complex mode alone: an imaginary part that has to go somewhere")
    ax1.legend(fontsize=10.5, ncol=2)

    ax2.plot(t, total.real, color=dk.C["green"], lw=3.4, label="sum of the two modes")
    ax2.plot(t, closed, "--", color=dk.C["orange"], lw=2.2,
             label=rf"$e^{{{sigma:g}t}}({B:.2f}\cos {wd:g}t + {Cc:.3f}\sin {wd:g}t)$")
    ax2.plot(t[::60], sol.y[0][::60], "o", ms=5, color=dk.C["purple"],
             label="numerical solution of the ODE")
    env = np.abs(2 * A1) * np.exp(sigma * t)
    ax2.plot(t, env, color=dk.C["grey"], lw=1.2, alpha=0.8,
             label=r"envelope $\pm|2A_1|e^{\sigma t}$")
    ax2.plot(t, -env, color=dk.C["grey"], lw=1.2, alpha=0.8)
    ax2.axhline(0, color="k", lw=1)
    ax2.set_xlabel("time  [s]")
    ax2.set_ylabel("x(t)")
    ax2.set_title("Added together: a real motion, with no j anywhere in sight")
    ax2.legend(fontsize=10.5, ncol=2)

    fig.suptitle("Complex modes are bookkeeping; conjugate pairs are physics",
                 fontsize=15, y=0.995)
    fig.tight_layout()
    dk.finish(plt, fig, "demo3_real_from_complex", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
