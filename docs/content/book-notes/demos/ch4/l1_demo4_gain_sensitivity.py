"""
L1 Demo 4  --  Feedback buys insensitivity to the plant           (FPE §4.1.4)

Plant G = A/(s + 1) whose gain A is nominally 1 but is actually anywhere from
0.5 to 1.5 (a +/-50% error).

  Open loop:  D_ol = 1 (calibrated for A = 1). Overall DC gain T_ol(0) = A,
              so the output is off by exactly the plant error: S = 1.
  Feedback:   D_cl = 99, so 1 + G D_cl = 100 at DC for the nominal plant.
              T_cl(0) = 99A/(1 + 99A); the first-order prediction is
              delta T/T = S (delta A/A) with S = 1/100.

The exact fractional change for a plant change eps = delta G/G is
eps S/(1 + T eps), which is what the table checks.

Run:  uv run python ch4/l1_demo4_gain_sensitivity.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

K = 99.0
AS = [0.5, 0.75, 1.0, 1.25, 1.5]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L1 Demo 4 -- a 50% plant error, open loop and with loop gain 99")

    T0 = K / (1 + K)
    S0 = 1 / (1 + K)
    rows = []
    for A in AS:
        eps = A - 1.0
        Tcl = K * A / (1 + K * A)
        rows.append([f"{A:g}", f"{eps:+.0%}", f"{A:.3f}", f"{Tcl:.5f}",
                     f"{(Tcl - T0) / T0:+.4%}", f"{S0 * eps:+.4%}",
                     f"{eps * S0 / (1 + T0 * eps):+.4%}"])
    dk.table(["A", "dG/G", "open-loop gain", "closed-loop gain",
              "closed dT/T", "S dG/G", "exact formula"], rows)
    dk.note("Open loop, the gain error is the plant error, one for one. Closed "
            "loop, a 10% plant change gives about 0.1% and even a 50% loss of "
            "plant gain costs only 1%. The linear estimate S dG/G is good for "
            "small changes; for a 50% drop in plant gain it is optimistic by a "
            "factor of two.")

    t = np.linspace(0, 5, 5001)
    t_fast = np.linspace(0, 0.1, 2001)
    yo, yc, uc = {}, {}, {}
    for A in AS:
        _, yo[A] = step(lti([A], [1, 1]), T=t)
        _, yc[A] = step(lti([K * A], [1, 1 + K * A]), T=t)
        _, uc[A] = step(lti([K, K], [1, 1 + K * A]), T=t_fast)
    print(f"\n  closed-loop pole for A = 1: -{1 + K:g} rad/s (open loop: -1 rad/s)")
    print(f"  control at t = 0+: open loop {1:.0f}, closed loop {uc[1.0][0]:.0f}"
          f"  -> settles at K/(1+K) = {K / (1 + K):.2f}")
    dk.note("Feedback also made the response a hundred times faster. It paid for "
            "both with an initial control effort of 99 instead of 1 -- sensitivity "
            "reduction is bought with loop gain, and loop gain is actuator effort.")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.0))
    ax0, ax1, ax2 = axes
    Agrid = np.linspace(0.4, 1.6, 200)
    ax0.plot(Agrid, Agrid, color=dk.C["red"], label=r"open loop: $A$")
    ax0.plot(Agrid, K * Agrid / (1 + K * Agrid), color=dk.C["blue"],
             label=r"feedback: $99A/(1+99A)$")
    ax0.axvspan(0.5, 1.5, color=dk.C["grey"], alpha=0.08)
    ax0.set_xlabel(r"actual plant gain $A$ (nominal 1)")
    ax0.set_ylabel("overall DC gain")
    ax0.set_title("Steady-state gain vs plant gain")
    ax0.legend(fontsize=10.5, loc="upper left")

    shades = [0.35, 0.55, 1.0, 0.55, 0.35]
    for A, a in zip(AS, shades):
        ax1.plot(t, yo[A], color=dk.C["red"], alpha=a, lw=1.8)
        ax1.plot(t, yc[A], color=dk.C["blue"], alpha=a, lw=1.8)
    ax1.plot([], [], color=dk.C["red"], label="open loop")
    ax1.plot([], [], color=dk.C["blue"], label="feedback")
    ax1.set_xlabel("time [s]")
    ax1.set_title(r"Step responses, $A=0.5\ldots1.5$")
    ax1.legend(fontsize=10.5, loc="lower right")

    for A, a in zip(AS, shades):
        ax2.plot(t_fast * 1000, uc[A], color=dk.C["blue"], alpha=a, lw=1.8)
    ax2.axhline(1, color=dk.C["red"], lw=1.8, label="open loop: $u=1$")
    ax2.set_xlabel("time [ms]")
    ax2.set_title("Control effort, first 100 ms")
    ax2.legend(fontsize=10.5)

    fig.suptitle(r"$G=A/(s+1)$: open loop $D_{ol}=1$ against feedback $D_{cl}=99$",
                 fontsize=14)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo4_gain_sensitivity", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
