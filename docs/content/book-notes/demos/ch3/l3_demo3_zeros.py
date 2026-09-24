"""
L3 Demo 3  --  What a zero does to a step response     (FPE §3.5, Example 3.28)

Section 3.5 makes a mechanical claim about zeros. Write the normalised system

    H(s) = [ s/(alpha zeta) + 1 ] / [ s^2 + 2 zeta s + 1 ]           (Eq. 3.80)

as the sum of the zero-free system H0 and a second term that is 1/(alpha zeta)
times s H0 -- that is, times the DERIVATIVE of the zero-free step response:

    y(t) = y0(t) + (1/(alpha zeta)) y0'(t).

Adding a derivative bump lifts the early response, so a LHP zero raises the
overshoot and quickens the rise. Flip the zero into the RHP and the same bump
is SUBTRACTED, so the response starts out backwards. This script computes both
decompositions and the overshoot curve of Fig. 3.29, then reproduces the pole-
zero cancellations of Example 3.28.

Run:  uv run python ch3/l3_demo3_zeros.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

ZETA = 0.5


def normalised(alpha, zeta=ZETA):
    """Eq. (3.80) with omega_n = 1; alpha < 0 puts the zero in the RHP."""
    return lti([1.0 / (alpha * zeta), 1.0], [1.0, 2 * zeta, 1.0])


def step_of(sys, t):
    _, y = step(sys, T=t)
    return y


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 3 -- a zero adds a derivative to the response")

    t = np.linspace(0, 12, 6000)
    y0 = step_of(lti([1.0], [1.0, 2 * ZETA, 1.0]), t)
    y0dot = np.gradient(y0, t)

    dk.section("the decomposition y = y0 + (1/alpha zeta) * y0'   (Eq. 3.81)")
    rows = []
    for alpha in [10.0, 4.0, 2.0, 1.0, 0.5]:
        y = step_of(normalised(alpha), t)
        y_sum = y0 + y0dot / (alpha * ZETA)
        rows.append([f"{alpha:.1f}", f"{-alpha*ZETA:+.2f}",
                     f"{100*(y.max()-1):.1f}%",
                     f"{np.max(np.abs(y - y_sum)):.2e}"])
    dk.table(["alpha", "zero location", "overshoot", "|y - (y0 + y0'/(alpha zeta))|"],
             rows)
    dk.note(
        "The last column is the point: the response with a zero really is the "
        "zero-free response plus a scaled copy of its own derivative. Small alpha "
        "means the zero is close to the poles, the derivative term is weighted "
        "heavily, and the overshoot climbs.")

    dk.section("Fig. 3.29: overshoot versus normalised zero location")
    rows = []
    for alpha in [0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 10.0, 100.0]:
        y = step_of(normalised(alpha), t)
        rows.append([f"{alpha:g}", f"{100*(y.max()-1):.1f}%"])
    dk.table(["alpha", "M_p"], rows)
    print(f"\n  zero-free reference (alpha -> infinity): "
          f"{100*(y0.max()-1):.1f}%")
    print("  distance reduces the effect; factor four is a heuristic, not an error bound")

    dk.section("the RHP mirror image: alpha < 0")
    rows = []
    for alpha in [-1.0, -2.0, -4.0]:
        y = step_of(normalised(alpha), t)
        undershoot = y.min()
        t_cross = t[np.argmax(y > 0)] if (y < 0).any() else 0.0
        rows.append([f"{alpha:.1f}", f"{-alpha*ZETA:+.2f}", f"{undershoot:+.3f}",
                     f"{t_cross:.2f}", f"{100*(y.max()-1):.1f}%"])
    dk.table(["alpha", "zero location", "worst undershoot", "time to cross zero [s]",
              "M_p"], rows)
    dk.note(
        "A right half-plane zero subtracts the derivative bump instead of adding it, "
        "so the response starts backwards and only then climbs. Read the overshoot "
        "column carefully, because the book's one-line summary is easy to "
        "over-generalise: against the LHP zero at the same distance the RHP zero does "
        "depress the overshoot (20.9% at alpha = -2 versus 29.8% at alpha = +2), but "
        "against the zero-free system it still raises it (16.3%). What a RHP zero "
        "reliably does is the undershoot and the sluggishness, not a smaller peak.")

    # ------------------------------------------------------- Example 3.28
    dk.section("Example 3.28: H(s) = (24/z)(s+z)/[(s+4)(s+6)], z = 1..6")
    t2 = np.linspace(0, 2.5, 4000)
    rows = []
    for z in [1, 2, 3, 4, 5, 6]:
        y = step_of(lti([24.0 / z, 24.0], [1.0, 10.0, 24.0]), t2)
        c4 = 12.0 / z - 3.0        # coefficient of e^-4t
        c6 = 2.0 - 12.0 / z        # coefficient of e^-6t
        rows.append([f"{z}", f"{c4:+.3f}", f"{c6:+.3f}",
                     f"{100*max(0.0, y.max()-1):.2f}%"])
    dk.table(["zero at -z", "coeff of e^-4t", "coeff of e^-6t", "overshoot"], rows)
    dk.note(
        "At z = 4 and z = 6 the zero lands exactly on a pole, that mode's coefficient "
        "is exactly zero, and the response is first order -- a physical realisation may retain the "
        "mode even though this transfer function no longer shows it. At z = 5, with the "
        "zero between the two poles, both coefficients are negative: the response "
        "approaches its final value from below and never overshoots at all. Below "
        "z = 4 the zero is nearer the origin than either pole, the coefficients grow "
        "and take opposite signs, and the overshoot runs away -- 108% at z = 1.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.2))

    for alpha, colour in [(0.5, dk.C["red"]), (1.0, dk.C["orange"]),
                          (2.0, dk.C["green"]), (100.0, dk.C["blue"])]:
        lbl = r"no zero" if alpha == 100.0 else f"$\\alpha$ = {alpha:g}"
        trace = y0 if alpha == 100.0 else step_of(normalised(alpha), t)
        axes[0].plot(t, trace, color=colour, lw=2.0, label=lbl)
    axes[0].axhline(1.0, ls=":", color="k", lw=1.0)
    axes[0].set_xlim(0, 12)
    axes[0].set_xlabel(r"normalised time $\omega_n t$")
    axes[0].set_title(f"Fig. 3.27: LHP zero, $\\zeta$ = {ZETA}")
    axes[0].legend(fontsize=10)

    aa = np.concatenate([np.linspace(0.4, 1.0, 25), np.linspace(1.0, 8.0, 40)])
    mps = [100 * (step_of(normalised(a), t).max() - 1) for a in aa]
    axes[1].plot(aa, mps, color=dk.C["blue"], lw=2.4)
    axes[1].axhline(100 * (y0.max() - 1), ls="--", color=dk.C["grey"],
                    label="no zero")
    axes[1].axvline(1.0, ls=":", color=dk.C["red"])
    axes[1].text(1.1, 5, r"$\alpha=1$: zero on $\Re$(pole)", fontsize=10,
                 color=dk.C["red"])
    axes[1].set_xlabel(r"$\alpha$  (zero at $-\alpha\zeta\omega_n$)")
    axes[1].set_ylabel("$M_p$ [%]")
    axes[1].set_title("Fig. 3.29: overshoot versus zero location")
    axes[1].legend(fontsize=10)

    y_rhp = step_of(normalised(-2.0), t)
    axes[2].plot(t, y0, color=dk.C["grey"], lw=1.6, label="no zero, $y_0$")
    axes[2].plot(t, y0dot / (2.0 * ZETA), color=dk.C["orange"], lw=1.6,
                 label=r"derivative term $y_0'/(\alpha\zeta)$")
    axes[2].plot(t, step_of(normalised(2.0), t), color=dk.C["green"], lw=2.2,
                 label=r"LHP zero: $y_0 + y_0'/(\alpha\zeta)$")
    axes[2].plot(t, y_rhp, color=dk.C["red"], lw=2.2,
                 label=r"RHP zero: $y_0 - y_0'/(|\alpha|\zeta)$")
    axes[2].axhline(0, color="k", lw=0.8)
    axes[2].set_xlim(0, 12)
    axes[2].set_xlabel(r"normalised time $\omega_n t$")
    axes[2].set_title("Figs. 3.30 and 3.31: add the bump, or subtract it")
    axes[2].legend(fontsize=9.5, loc="lower right")

    fig.suptitle("Zeros do not move the poles; they reweight what the poles produce",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo3_zeros", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
