"""
L2 Demo 3  --  Reading a response off the poles              (Examples 3.25, 3.26)

Two transfer functions with the same numerator and almost the same denominator:

    H(s) = (2s + 1)/(s^2 + 3s + 2)     poles at -1 and -2      (Example 3.25)
    H(s) = (2s + 1)/(s^2 + 2s + 5)     poles at -1 +/- 2j      (Example 3.26)

The first is a sum of two decaying exponentials; the second rings inside an
envelope. Both closed forms are checked here against a numerical impulse
response, and the standard second-order parameters (zeta, omega_n, sigma,
omega_d) are computed from the coefficients rather than looked up.

Run:  uv run python ch3/l2_demo3_second_order.py
"""

import numpy as np
from scipy.signal import impulse, lti, step

import kit as dk


def second_order_params(den):
    """(zeta, omega_n, sigma, omega_d) from s^2 + 2 zeta wn s + wn^2."""
    _, a1, a2 = den
    wn = np.sqrt(a2)
    zeta = a1 / (2 * wn)
    sigma = zeta * wn
    wd = wn * np.sqrt(max(0.0, 1 - zeta**2))
    return zeta, wn, sigma, wd


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L2 Demo 3 -- the poles set the shapes, the zero sets the weights")

    # ---------------------------------------------------------- Example 3.25
    dk.section("Example 3.25: real poles at -1 and -2, zero at -0.5")
    t = np.linspace(0, 6, 1500)
    sys1 = lti([2.0, 1.0], [1.0, 3.0, 2.0])
    _, h1 = impulse(sys1, T=t)

    r_m1 = (2 * (-1) + 1) / (-1 + 2)          # cover-up at s = -1
    r_m2 = (2 * (-2) + 1) / (-2 + 1)          # cover-up at s = -2
    h1_closed = r_m1 * np.exp(-t) + r_m2 * np.exp(-2 * t)

    dk.table(["pole", "residue by cover-up", "term"],
             [["-1", f"{r_m1:+.4f}", f"{r_m1:+.0f} e^-t"],
              ["-2", f"{r_m2:+.4f}", f"{r_m2:+.0f} e^-2t"]])
    print(f"\n  max |closed form - numerical impulse response| = "
          f"{np.max(np.abs(h1 - h1_closed)):.2e}")

    cross = t[np.argmin(np.abs(np.abs(r_m1 * np.exp(-t)) - np.abs(r_m2 * np.exp(-2 * t))))]
    dk.note(
        f"The fast term 3e^-2t dominates early and the slow term -e^-t takes over "
        f"later; the two are equal in size at t = {cross:.2f} s. The poles decided that "
        "there would be an e^-t and an e^-2t at all. The zero at -0.5 decided how much "
        "of each -- and it sits near neither pole, so neither residue is small.")

    # ---------------------------------------------------------- Example 3.26
    dk.section("Example 3.26: the same numerator over s^2 + 2s + 5")
    sys2 = lti([2.0, 1.0], [1.0, 2.0, 5.0])
    _, h2 = impulse(sys2, T=t)
    zeta, wn, sigma, wd = second_order_params([1.0, 2.0, 5.0])

    dk.table(["quantity", "value", "from"],
             [["omega_n [rad/s]", f"{wn:.4f}", "sqrt(5)"],
              ["zeta", f"{zeta:.4f}", "2 zeta wn = 2"],
              ["sigma [1/s]", f"{sigma:.4f}", "zeta wn"],
              ["omega_d [rad/s]", f"{wd:.4f}", "wn sqrt(1 - zeta^2)"],
              ["pole angle [deg]", f"{np.degrees(np.arcsin(zeta)):.2f}",
               "theta = asin(zeta), Fig. 3.18"]])

    h2_closed = 2 * np.exp(-t) * np.cos(2 * t) - 0.5 * np.exp(-t) * np.sin(2 * t)
    print(f"\n  max |closed form - numerical impulse response| = "
          f"{np.max(np.abs(h2 - h2_closed)):.2e}")
    amp = np.hypot(2.0, 0.5)
    print(f"  envelope: +/- {amp:.4f} e^-t, so |h(t)| is below 0.01 by "
          f"t = {np.log(100*amp)/sigma:.2f} s")

    dk.note(
        "Both systems have the same numerator, so the difference in the plots is "
        "entirely a matter of where the poles are. Moving the pair off the real axis "
        "converted a sum of two decays into one decaying oscillation at omega_d = 2 "
        "rad/s inside an e^-t envelope.")

    # ------------------------------------------------- the zeta family, Fig 3.19
    dk.section("Fig. 3.19(b): the step response family, overshoot computed")
    rows = []
    tn = np.linspace(0, 12, 2400)
    for z in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        sysz = lti([1.0], [1.0, 2 * z, 1.0])       # wn = 1
        _, y = step(sysz, T=tn)
        mp_meas = max(0.0, y.max() - 1.0)
        mp_form = np.exp(-z * np.pi / np.sqrt(1 - z**2)) if z < 1 else 0.0
        rows.append([f"{z:.1f}", f"{100*mp_meas:.2f}%", f"{100*mp_form:.2f}%"])
    dk.table(["zeta", "overshoot measured", "exp(-pi zeta/sqrt(1-zeta^2))"], rows)

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.2))

    axes[0].plot(t, h1, color="k", lw=3.0, alpha=0.3, label="$h(t)$")
    axes[0].plot(t, r_m2 * np.exp(-2 * t), color=dk.C["orange"], lw=1.8,
                 label=r"$3e^{-2t}$ (fast pole)")
    axes[0].plot(t, r_m1 * np.exp(-t), color=dk.C["blue"], lw=1.8,
                 label=r"$-e^{-t}$ (slow pole)")
    axes[0].axhline(0, color="k", lw=0.8)
    axes[0].set_xlim(0, 4)
    axes[0].set_xlabel("time [s]")
    axes[0].set_title("Example 3.25: fast term first, slow term last")
    axes[0].legend(fontsize=10)

    axes[1].plot(t, h2, color=dk.C["blue"], lw=2.4, label="$h(t)$")
    axes[1].plot(t, amp * np.exp(-sigma * t), "--", color=dk.C["red"], lw=1.4,
                 label=r"$\pm\sqrt{2^2+0.5^2}\,e^{-\sigma t}$")
    axes[1].plot(t, -amp * np.exp(-sigma * t), "--", color=dk.C["red"], lw=1.4)
    axes[1].axhline(0, color="k", lw=0.8)
    axes[1].set_xlim(0, 5)
    axes[1].set_xlabel("time [s]")
    axes[1].set_title(f"Example 3.26: $\\zeta$ = {zeta:.3f}, $\\omega_d$ = {wd:.1f} rad/s")
    axes[1].legend(fontsize=10)

    for z, colour in zip([0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
                         [dk.C["purple"], dk.C["red"], dk.C["orange"],
                          dk.C["green"], dk.C["sky"], dk.C["blue"]]):
        sysz = lti([1.0], [1.0, 2 * z, 1.0])
        _, y = step(sysz, T=tn)
        axes[2].plot(tn, y, color=colour, lw=1.8, label=f"$\\zeta$ = {z:g}")
    axes[2].axhline(1.0, color="k", lw=0.8, ls=":")
    axes[2].set_xlabel(r"normalised time $\omega_n t$")
    axes[2].set_title("Fig. 3.19(b): step response versus damping")
    axes[2].legend(fontsize=9.5, ncol=2)

    fig.suptitle("Poles decide the shapes; the numerator decides the mixture",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo3_second_order", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
