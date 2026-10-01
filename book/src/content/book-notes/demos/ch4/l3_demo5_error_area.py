"""
Steady-state error and system type Demo 5  --  K_v from the closed loop: error area and Truxal's formula
                                   (FPE §4.2.1 Eq. 4.45; Truxal, Appendix W4.2.2.1)
                                                           [beyond the book]

For a stable loop with T(0) = 1, the step error e(t) has Laplace transform
[1 - T(s)]/s, so its total area is

    integral_0^inf e dt = lim_{s->0} [1 - T(s)]/s = 1/K_v.

Type 1: the area between the reference step and the response equals the ramp
error 1/K_v. Type 2: 1/K_v = 0, the net area is zero, and because e(0+) = 1 > 0
the error must go negative -- a Type 2 step response always overshoots (FPE
Problem 4.28).

Truxal's formula gives the same number from closed-loop poles p_i and zeros z_j:

    1/K_v = sum 1/(-p_i) - sum 1/(-z_j),

and sum 1/(-p_i) = a_{n-1}/a_n, the ratio of the last two coefficients of the
closed-loop denominator. Checked on three loops, including the PI loop of
Example 3.34 at K = 10, K_I = 5.

Run:  uv run python ch4/l3_demo5_error_area.py
"""

import numpy as np
from scipy.integrate import trapezoid
from scipy.signal import lsim, lti

import kit as dk

# name: loop numerator, loop denominator, direct K_v
LOOPS = {
    "Type 1: 2/[s(0.5s+1)]": ([2.0], [0.5, 1.0, 0.0], 2.0),
    "Type 2: 2(s+1)/[s^2(0.2s+1)]": ([2.0, 2.0], [0.2, 1.0, 0.0, 0.0], np.inf),
    "Ex. 3.34 PI: (10s+5)/[s(s+1)(s+2)]": ([10.0, 5.0], [1.0, 3.0, 2.0, 0.0], 2.5),
}


def truxal(num, den):
    cl_den = np.polyadd(den, num)
    poles, zeros = np.roots(cl_den), np.roots(num)
    sp = float(np.sum(1 / -poles).real)
    sz = float(np.sum(1 / -zeros).real) if len(zeros) else 0.0
    return poles, zeros, sp, sz, cl_den


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("Steady-state error and system type Demo 5 -- the velocity constant read from the closed loop")

    t = np.linspace(0, 60, 60001)
    rows, runs = [], {}
    for name, (num, den, kv) in LOOPS.items():
        poles, zeros, sp, sz, cl = truxal(num, den)
        inv_kv = sp - sz
        _, e, _ = lsim(lti(np.polysub(cl, num), cl), np.ones_like(t), t)
        runs[name] = e
        area = trapezoid(e, t)
        rows.append([name, f"{cl[-2]/cl[-1]:.4f}", f"{sp:.4f}", f"{sz:.4f}",
                     f"{inv_kv:.4f}", "0" if np.isinf(kv) else f"{1/kv:.4f}",
                     f"{area:.4f}", f"{e.min():+.4f}"])
    dk.table(["loop", "a_{n-1}/a_n", "sum 1/(-p)", "sum 1/(-z)", "Truxal 1/K_v",
              "direct 1/K_v", "area of e", "min e"], rows)

    dk.note(
        "Three ways to the same number: lim s L(s), Truxal's pole-zero sum, and the "
        "area under the step error. In the PI loop the slow pole at -0.462 and the "
        "zero at -0.5 almost cancel in the response, yet they contribute "
        "2.166 - 2.000 = 0.166 of the total 0.400 in 1/K_v -- over 40%. A slow "
        "pole-zero pair near the origin barely shows in the step response and can "
        "still move K_v a lot; Chapter 5's lag compensator is built on that fact.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.6))
    names = list(LOOPS)
    for name, colour in [(names[0], dk.C["blue"]), (names[1], dk.C["green"])]:
        e = runs[name]
        axL.plot(t, e, color=colour, label=name)
        axL.fill_between(t, e, 0, color=colour, alpha=0.18)
    axL.axhline(0, color="k", lw=0.8)
    axL.set_xlim(0, 6)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("step error $e(t)$")
    axL.set_title(r"Area under $e$: $1/K_v=0.5$ (Type 1), $0$ (Type 2)")
    axL.legend(fontsize=10.5)

    num, den, _ = LOOPS[names[2]]
    poles, zeros, *_ = truxal(num, den)
    dk.splane(axR, poles, zeros, xlim=(-2.0, 0.5), ylim=(-3.6, 3.6),
              label_poles="closed-loop poles", label_zeros="closed-loop zero",
              title_text=r"Ex. 3.34 PI loop: $1/K_v = 2.4 - 2.0 = 0.4$")
    for p in poles:
        axR.annotate(f"{1/-p.real if abs(p.imag) < 1e-9 else (1/-p).real:.3f}",
                     (p.real, p.imag), textcoords="offset points", xytext=(8, 8),
                     fontsize=10.5, color=dk.C["blue"])
    axR.annotate("2.000", (zeros[0].real, 0), textcoords="offset points",
                 xytext=(-6, -22), fontsize=10.5, color=dk.C["red"])
    axR.legend(fontsize=10, loc="lower left")
    fig.suptitle("The velocity constant from the closed loop [beyond the book]", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo5_error_area", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
