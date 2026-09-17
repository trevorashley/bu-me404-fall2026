"""
L1 Demo 1  --  Superposition builds the convolution integral      (FPE 3.1.1)

The book's Figs. 3.1 and 3.2 are a claim, not a proof: chop the input into short
pulses, add up one shifted impulse response per pulse, and in the limit you get

    y(t) = integral_0^t u(tau) h(t - tau) d tau.

This script carries out that sum for the first-order system of Examples 3.1-3.3,

    y' + k y = u,      h(t) = e^{-k t} 1(t),

with a deliberately un-elementary input, and watches the pulse sum converge to
the exact response as the pulse width Delta shrinks.

Run:  uv run python ch3/l1_demo1_convolution.py
"""

import numpy as np
from scipy.integrate import solve_ivp

import kit as dk

K = 1.0                     # the k of y' + k y = u
T_END = 8.0


def u(t):
    """A composite bounded causal input, rather than a single table entry."""
    t = np.asarray(t, dtype=float)
    return np.where(t < 0.0, 0.0,
                    0.6 + np.exp(-0.30 * t) * np.sin(2.0 * t) + 0.25 * (t > 3.0))


def h(t):
    """Impulse response of the first-order system (Example 3.3)."""
    t = np.asarray(t, dtype=float)
    return np.where(t < 0.0, 0.0, np.exp(-K * t))


def exact(t_eval):
    """Ground truth: integrate the ODE itself, never touching convolution."""
    sol = solve_ivp(lambda t, y: u(t) - K * y[0], (0.0, T_END), [0.0],
                    t_eval=t_eval, rtol=1e-10, atol=1e-12, max_step=0.005)
    return sol.y[0]


def pulse_sum(t_eval, delta):
    """Impulse-quadrature approximation to Eq. (3.8), using h, not h_Delta.

    At finite Delta this is not the exact rectangular-pulse response of Eq. (3.5).
    """
    centres = np.arange(0.0, T_END + delta, delta)
    contributions = delta * u(centres)[None, :] * h(t_eval[:, None] - centres[None, :])
    return contributions.sum(axis=1)


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    t = np.linspace(0.0, T_END, 1601)
    y_exact = exact(t)

    dk.title("L1 Demo 1 -- a sum of pulse responses becomes the convolution integral")
    dk.note(
        "The system is y' + k y = u with k = 1, whose impulse response is h(t) = e^-t. "
        "The input is a decaying sinusoid on a constant offset with a step added at "
        "t = 3 s -- a composite input to exercise convolution. The reference answer "
        "comes from integrating the differential equation directly, so the pulse sum "
        "has nothing to lean on.")

    dk.section("shrinking the pulse width")
    rows = []
    prev = None
    for delta in [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]:
        err = float(np.max(np.abs(pulse_sum(t, delta) - y_exact)))
        ratio = "" if prev is None else f"{prev / err:.2f}"
        rows.append([f"{delta:.5f}", f"{err:.3e}", ratio])
        prev = err
    dk.table(["Delta", "max |pulse sum - exact|", "error ratio"], rows)

    dk.note(
        "For sufficiently small Delta, halving Delta approximately halves the error. "
        "That is the first-order convergence a rectangle rule on the convolution integral should "
        "give. This uses weighted impulses, not exact finite-width pulse responses: "
        "the shapes are shifted copies of the known impulse response.")

    dk.section("the same statement in the frequency domain")
    dk.note(
        "Convolution in time is multiplication of transforms, Y(s) = H(s) U(s). "
        "Checking one value: for a unit step, U(s) = 1/s and H(s) = 1/(s+1), so "
        "Y(s) = 1/(s(s+1)) and y(t) = 1 - e^-t. The final value theorem gives "
        "lim s Y(s) = 1 as s -> 0, and the simulated step response below agrees.")
    t_step = np.linspace(0, 12, 2001)
    step_sol = solve_ivp(lambda tt, y: 1.0 - K * y[0], (0, 12), [0.0],
                         t_eval=t_step, rtol=1e-10, atol=1e-12)
    print(f"\n  simulated step response at t = 12 s : {step_sol.y[0][-1]:.6f}")
    print(f"  final value theorem prediction      : {1.0:.6f}")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.0))

    delta_show = 0.5
    centres = np.arange(0.0, T_END + delta_show, delta_show)
    axL.step(np.append(centres, T_END + delta_show), np.append(u(centres), u(T_END)),
             where="post", color=dk.C["grey"], lw=1.6,
             label=f"pulse approximation, $\\Delta$ = {delta_show}")
    axL.plot(t, u(t), color=dk.C["blue"], lw=2.4, label="input $u(t)$")
    for c in centres[::2]:
        axL.plot(t, delta_show * u(np.array([c]))[0] * h(t - c),
                 color=dk.C["orange"], lw=1.0, alpha=0.75)
    axL.plot([], [], color=dk.C["orange"], lw=1.0,
             label=r"individual responses $\Delta\,u(k\Delta)\,h(t-k\Delta)$")
    axL.set_xlabel("time [s]")
    axL.set_ylabel("input and pulse responses")
    axL.set_title("Fig. 3.2 idea: chop the input, respond to each piece")
    axL.legend(loc="upper right", fontsize=10.5)

    axR.plot(t, y_exact, color="k", lw=3.0, alpha=0.35, label="exact (ODE solve)")
    for delta, colour in [(1.0, dk.C["red"]), (0.25, dk.C["orange"]),
                          (0.0625, dk.C["green"])]:
        axR.plot(t, pulse_sum(t, delta), color=colour, lw=1.8,
                 label=f"pulse sum, $\\Delta$ = {delta}")
    axR.set_xlabel("time [s]")
    axR.set_ylabel("output $y(t)$")
    axR.set_title("The sum converges to the convolution integral")
    axR.legend(loc="lower right", fontsize=10.5)

    fig.suptitle("Superposition + time invariance = convolution   (FPE §3.1.1)",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo1_convolution", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
