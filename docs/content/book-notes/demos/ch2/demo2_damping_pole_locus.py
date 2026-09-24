"""
Demo 2  --  What damping actually does to the poles              (lecture §7.4)

The intuitive guess is that damping "slides the poles left". It does not. For
m x'' + c x' + k x = 0 with m and k fixed,

    sigma^2 + omega_d^2 = k/m = omega_n^2,

so the underdamped pair has CONSTANT MAGNITUDE. Increasing c walks it around a
circle of radius omega_n -- leftward AND toward the real axis -- until the two
roots collide on the real axis at c = 2*sqrt(mk) and split apart.

This script proves it numerically and draws the arc.

Run:  uv run python demo2_damping_pole_locus.py
"""

import numpy as np

import demokit as dk

M, K = 1.0, 25.0                  # the lecture's parameters: omega_n = 5 rad/s
C_CRIT = 2.0 * np.sqrt(M * K)     # = 10.0


def poles(c: float) -> np.ndarray:
    return np.roots([M, c, K])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    wn = np.sqrt(K / M)
    dk.title("Demo 2 -- damping moves the poles along a circle, not along a line")
    dk.note(
        f"System: m = {M:g}, k = {K:g}, so the natural frequency is "
        f"omega_n = sqrt(k/m) = {wn:g} rad/s and the critical damping is "
        f"c_crit = 2*sqrt(mk) = {C_CRIT:g}.")

    # ------------------------------------------------- the lecture's table
    dk.section("underdamped: the pair keeps constant magnitude (this is §7.4's table)")
    rows = []
    for c in [0.0, 2.0, 4.0, 6.0, 8.0, 9.9]:
        p = poles(c)
        sigma, wd = p[0].real, abs(p[0].imag)
        rows.append([f"{c:.1f}", f"{sigma:+.3f}", f"{wd:.3f}",
                     f"{np.hypot(sigma, wd):.4f}", f"{c/C_CRIT:.3f}"])
    dk.table(["c", "sigma", "omega_d", "|s|", "zeta"], rows)

    dk.note(
        "Read the |s| column: it never moves. Damping changes BOTH coordinates of the "
        "pole -- sigma becomes more negative and omega_d shrinks -- in exactly the way "
        "that keeps sigma^2 + omega_d^2 fixed at k/m. The pair slides around the arc "
        "and reaches the real axis precisely when zeta = 1.")

    err = max(abs(np.hypot(poles(c)[0].real, poles(c)[0].imag) - wn)
              for c in np.linspace(0, C_CRIT * 0.999, 400))
    print(f"\n  max deviation of |s| from omega_n over 0 <= c < c_crit:  {err:.2e}")

    # ------------------------------------------------- overdamped branch
    dk.section("overdamped: the roots leave the circle and separate on the real axis")
    rows = []
    for c in [10.0, 11.0, 14.0, 26.0]:
        p = np.sort_complex(poles(c))
        rows.append([f"{c:.1f}", f"{p[0].real:+.3f}", f"{p[1].real:+.3f}",
                     f"{abs(p[0]):.3f}", f"{abs(p[1]):.3f}",
                     f"{(p[0]*p[1]).real:.3f}"])
    dk.table(["c", "s1", "s2", "|s1|", "|s2|", "s1*s2"], rows)
    dk.note(
        "Past critical damping the magnitudes split, but their PRODUCT stays at "
        f"k/m = {K/M:g} -- that is what the constant term of the characteristic "
        "polynomial pins down. One root races off to the left while the other creeps "
        "toward the origin, which is why a heavily overdamped system is slow.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.2),
                                   gridspec_kw={"width_ratios": [1, 1.15]})

    dk.splane(axL, poles=[], xlim=(-13.5, 3.5), ylim=(-8.2, 8.2),
              title_text=r"Pole locus as $c$ increases from 0")
    axL.set_aspect("equal")   # so that a circle looks like a circle

    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 400)
    axL.plot(wn * np.cos(th), wn * np.sin(th), "--", color=dk.C["grey"],
             lw=1.6, label=rf"circle $|s|=\omega_n={wn:g}$")

    cs_under = np.linspace(0, C_CRIT * 0.9995, 300)
    pu = np.array([poles(c) for c in cs_under])
    axL.plot(pu[:, 0].real, pu[:, 0].imag, color=dk.C["blue"], lw=3, label="underdamped")
    axL.plot(pu[:, 1].real, pu[:, 1].imag, color=dk.C["blue"], lw=3)

    cs_over = np.linspace(C_CRIT * 1.0005, 26, 300)
    po = np.array([poles(c) for c in cs_over])
    axL.plot(po[:, 0].real, po[:, 0].imag, color=dk.C["red"], lw=3, label="overdamped")
    axL.plot(po[:, 1].real, po[:, 1].imag, color=dk.C["red"], lw=3)

    for c, mark in [(0.0, "o"), (4.0, "o"), (8.0, "o"), (C_CRIT, "s")]:
        p = poles(c)
        axL.plot(p.real, p.imag, mark, ms=9, color=dk.C["orange"],
                 mec="k", mew=0.8, zorder=5)
        off = {0.0: (-12, 12), 4.0: (10, 6), 8.0: (10, 6), C_CRIT: (8, 10)}[c]
        axL.annotate(f"c={c:g}", (p[0].real, p[0].imag), textcoords="offset points",
                     xytext=off, fontsize=10, weight="bold")
    axL.annotate("overdamped branch\ncontinues to -25",
                 xy=(-13.0, 0), xytext=(-12.5, 2.4), fontsize=9.5,
                 color=dk.C["red"], ha="left",
                 arrowprops=dict(arrowstyle="->", color=dk.C["red"], lw=1.2))
    axL.legend(loc="lower left", fontsize=9.5)

    # right panel: the motion each damping produces
    t = np.linspace(0, 4, 1600)
    for c, color in [(0.0, dk.C["orange"]), (2.0, dk.C["green"]),
                     (6.0, dk.C["blue"]), (10.0, dk.C["purple"]), (26.0, dk.C["red"])]:
        p = poles(c)
        if abs(p[0] - p[1]) < 1e-9:                      # critically damped
            y = (1 + 5 * t) * np.exp(p[0].real * t)
        else:                                            # x(0)=1, x'(0)=0
            a1 = -p[1] / (p[0] - p[1])
            a2 = p[0] / (p[0] - p[1])
            y = np.real(a1 * np.exp(p[0] * t) + a2 * np.exp(p[1] * t))
        axR.plot(t, y, color=color, label=f"c = {c:g}  (ζ = {c/C_CRIT:.2f})")

    axR.axhline(0, color="k", lw=1)
    axR.set_xlabel("time  [s]")
    axR.set_ylabel("x(t)   released from x(0)=1")
    axR.set_title("The same information, in the time domain")
    axR.legend(fontsize=10.5)

    fig.suptitle(r"Increasing $c$ moves the poles leftward AND toward the real axis",
                 fontsize=15, y=0.99)
    fig.tight_layout()
    dk.finish(plt, fig, "demo2_damping_pole_locus", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
