"""
PID control Demo 3  --  Where the derivative goes: same poles, different zeros
                                                       (Section 4.3.3, Fig. 4.10)

PID around G(s) = 1/(s^2 + 1.4 s + 1). The characteristic polynomial is

    s^3 + (1.4 + k_D) s^2 + (1 + k_P) s + k_I,                       (Eq. 4.77)

so the gains k_D = 1.6, k_P = 3, k_I = 2 put the closed-loop roots exactly at
-1 and -1 +/- j, i.e. (s + 1)(s^2 + 2 s + 2) = s^3 + 3 s^2 + 4 s + 2.

Fig. 4.10(b), D on the error:   Y/R = (k_D s^2 + k_P s + k_I) / a(s)
Fig. 4.10(a), D on the output:  Y/R = (k_P s + k_I) / a(s)

Identical poles; the zeros differ. With the derivative on the error a step in
r is differentiated, so u(t) contains an impulse k_D delta(t). An ideal
derivative cannot be built; here it is approximated by k_D s / (tau_f s + 1)
with tau_f = 0.02 s, which turns the impulse into a spike of height about
k_D / tau_f. Filtering the derivative is taken up properly in PID tuning and implementation.

Run:  uv run python ch4/l2_demo3_derivative_placement.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

A1, A2 = 1.4, 1.0
KP, KI, KD = 3.0, 2.0, 1.6
TAU_F = 0.02


def pid_gains_for(target_roots):
    """Coefficient matching for G = 1/(s^2 + a1 s + a2) under PID."""
    alpha = np.real(np.poly(target_roots))       # [1, alpha1, alpha2, alpha3]
    return alpha[2] - A2, alpha[3], alpha[1] - A1   # k_P, k_I, k_D


def simulate(d_on_error: bool, t):
    """Filtered-derivative loop, built as polynomials in s.

    Plant  : Y = U / (s^2 + a1 s + a2)
    PI part: (k_P s + k_I)/s acting on e = r - y
    D part : k_D s/(tau s + 1) acting on e (Fig. 4.10b) or on -y (Fig. 4.10a)
    """
    P = np.array([1.0, A1, A2])
    Fd = np.array([TAU_F, 1.0])
    # controller over the common denominator s (tau s + 1)
    den_c = np.polymul([1.0, 0.0], Fd)
    num_pi = np.polymul([KP, KI], Fd)
    num_d = np.array([KD, 0.0, 0.0])
    num_fb = np.polyadd(num_pi, num_d)                   # acts on -y in both cases
    num_ref = num_fb if d_on_error else num_pi           # acts on r
    char = np.polyadd(np.polymul(den_c, P), num_fb)
    Y = lti(num_ref, char)
    U = lti(np.polymul(num_ref, P), char)
    _, y = step(Y, T=t)
    _, u = step(U, T=t)
    return y, u, char


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("PID control Demo 3 -- derivative on the error or on the output")

    dk.section("choosing the three gains by matching coefficients")
    target = [-1.0, -1.0 + 1.0j, -1.0 - 1.0j]
    kP, kI, kD = pid_gains_for(target)
    print(f"  target polynomial {np.real(np.poly(target))}")
    print(f"  k_P = {kP:.4f}, k_I = {kI:.4f}, k_D = {kD:.4f}")
    char = [1.0, A1 + KD, A2 + KP, KI]
    print("  check, roots of s^3 + 3 s^2 + 4 s + 2:",
          ", ".join(dk.fmt_root(z, 4) for z in np.sort_complex(np.roots(char))))

    dk.section("ideal derivative: the two reference transfer functions")
    rows = []
    for name, num in [("D on error  (4.10b)", [KD, KP, KI]),
                      ("D on output (4.10a)", [KP, KI])]:
        t = np.linspace(0, 10, 20001)
        _, y = step(lti(num, char), T=t)
        zeros = np.roots(num)
        rows.append([name, ", ".join(dk.fmt_root(z, 3) for z in zeros),
                     f"{100 * (y.max() - 1):.1f}%", f"{t[y.argmax()]:.2f}"])
    dk.table(["structure", "zeros of Y/R", "overshoot", "t_p [s]"], rows)

    dk.section(f"control effort with a filtered derivative, tau_f = {TAU_F} s")
    t = np.linspace(0, 10, 20001)
    res = {}
    rows = []
    for name, flag in [("D on error", True), ("D on output", False)]:
        y, u, cp = simulate(flag, t)
        res[name] = (y, u)
        rows.append([name, f"{u.max():.2f}", f"{u[0]:.2f}",
                     f"{100 * (y.max() - 1):.1f}%", f"{u[-1]:.4f}"])
    dk.table(["structure", "max u", "u(0+)", "overshoot", "u(10)"], rows)
    print(f"\n  filtered roots (D on error): "
          + ", ".join(dk.fmt_root(z, 3) for z in np.sort_complex(np.roots(cp))))

    dk.note(
        "Both loops settle with u -> a2 = 1, the inverse DC gain. With the derivative on "
        "the error, the reference step produces a spike near k_D/tau_f = 80, the "
        "'derivative kick'. Moving the derivative to the measured output removes the "
        "kick and leaves the closed-loop poles alone, but it also removes the "
        "numerator's s^2 term. In this example that costs overshoot, so the choice is "
        "about the actuator as much as about the response.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.4))
    for (name, (y, u)), c in zip(res.items(), [dk.C["blue"], dk.C["orange"]]):
        axL.plot(t, y, color=c, label=name)
        axR.plot(t, u, color=c, label=name)
    axL.axhline(1.0, color="k", ls="--", lw=1.0)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("$y(t)$")
    axL.set_title("Output: same poles, different zeros")
    axL.legend(fontsize=10.5, loc="lower right")
    y_err, u_err = res["D on error"]
    axR.set_ylim(-0.5, 6.0)
    axR.annotate(f"kick: peak {u_err.max():.0f}", xy=(0.0, 6.0), xytext=(1.2, 5.0),
                 arrowprops=dict(arrowstyle="->", color=dk.C["blue"]),
                 color=dk.C["blue"], fontsize=11)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("$u(t)$  (axis clipped)")
    axR.set_title(rf"Control: the derivative kick ($\tau_f$ = {TAU_F} s)")
    axR.legend(fontsize=10.5)
    fig.suptitle(r"PID with $k_P$ = 3, $k_I$ = 2, $k_D$ = 1.6: poles at $-1$, $-1\pm j$",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo3_derivative_placement", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
