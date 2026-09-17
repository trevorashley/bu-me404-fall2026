"""
L3 Demo 4  --  An extra pole, and a real nonminimum-phase aeroplane
                                                (Eq. 3.82, Example 3.30)

Two loose ends of Section 3.5, both checked numerically.

  1. An extra LHP pole at -alpha zeta omega_n slows the rise and can alter settling time (Figs. 3.36-3.38).
  2. The Boeing 747 altitude response to the elevator,

         h(s)/delta_e(s) = 30 (s - 6) / [ s (s^2 + 4s + 13) ],

     has a zero at s = +6 and an integrator. Pull the stick back and the
     aeroplane briefly descends before it climbs. The second-order estimates of
     Section 3.4 are then applied to a system that is neither second order nor
     zero-free, and the errors are reported.

Run:  uv run python ch3/l3_demo4_extra_pole_aircraft.py
"""

import numpy as np
from scipy.signal import impulse, lti, step

import kit as dk

ZETA = 0.5


def with_extra_pole(alpha, zeta=ZETA):
    """Eq. (3.82) with omega_n = 1: a second-order pair plus a real pole."""
    p = alpha * zeta                       # extra pole at -alpha*zeta
    den = np.polymul([1.0 / p, 1.0], [1.0, 2 * zeta, 1.0])
    return lti([1.0], den)


def rise_time(sys, t):
    _, y = step(sys, T=t)
    yf = float(np.polyval(sys.num, 0) / np.polyval(sys.den, 0))
    return t[np.argmax(y >= 0.9 * yf)] - t[np.argmax(y >= 0.1 * yf)], y


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 4 -- an extra pole slows things down; a RHP zero reverses them")

    # ------------------------------------------------------- extra pole
    dk.section("Fig. 3.38: normalised rise time versus the extra pole's distance")
    t = np.linspace(0, 40, 20000)
    tr0, y0 = rise_time(lti([1.0], [1.0, 2 * ZETA, 1.0]), t)
    rows = []
    for alpha in [0.5, 1.0, 2.0, 4.0, 10.0]:
        tr, _ = rise_time(with_extra_pole(alpha), t)
        rows.append([f"{alpha:g}", f"{-alpha*ZETA:+.2f}", f"{tr:.3f}",
                     f"{tr/tr0:.2f}x"])
    dk.table(["alpha", "extra pole", "omega_n t_r", "versus no extra pole"], rows)
    print(f"\n  second-order reference: omega_n t_r = {tr0:.3f}")
    dk.note(
        "In this standard family, an extra real pole slows the rise, and it matters once it comes within a "
        "factor of about four of the real part of the complex pair -- the same "
        "factor-of-four rule the book gives for zeros. Far away, its effect diminishes: at "
        "alpha = 10 the rise time is within a few percent of the pure second-order "
        "value.")

    # ------------------------------------------------------- the 747
    dk.section("Example 3.30: Boeing 747 altitude, impulsive elevator")
    t2 = np.linspace(0, 10, 40000)
    # delta_e = -1 (stick back, elevator up by the sign convention of Fig. 10.30)
    sys = lti([-30.0, 180.0], [1.0, 4.0, 13.0, 0.0])
    _, h = impulse(sys, T=t2)

    wn, zeta = np.sqrt(13.0), 2.0 / np.sqrt(13.0)
    hf = 180.0 / 13.0
    print(f"\n  final value theorem: h(inf) = 30*(-6)*(-1)/13 = {hf:.4f}")
    print(f"  simulated h(10 s)                          = {h[-1]:.4f}")

    undershoot = h.min()
    t_cross = t2[np.argmax(h > 0)]
    hn = h / hf
    tr = t2[np.argmax(hn >= 0.9)] - t2[np.argmax(hn >= 0.1)]
    mp = hn.max() - 1.0
    outside = np.where(np.abs(hn - 1.0) > 0.01)[0]
    ts = t2[outside[-1] + 1]

    dk.table(["quantity", "second-order estimate", "measured", "source of the estimate"],
             [["omega_n [rad/s]", f"{wn:.3f}", "--", "sqrt(13)"],
              ["zeta", f"{zeta:.3f}", "--", "2 zeta wn = 4"],
              ["t_r [s]", f"{1.8/wn:.3f}", f"{tr:.3f}", "1.8/omega_n"],
              ["M_p", f"{100*np.exp(-zeta*np.pi/np.sqrt(1-zeta**2)):.1f}%",
               f"{100*mp:.1f}%", "Eq. (3.72)"],
              ["t_s [s]", f"{4.6/2.0:.2f}", f"{ts:.2f}", "4.6/sigma"]])

    print(f"\n  worst undershoot        : {undershoot:.3f} (the aeroplane descends first)")
    print(f"  time to regain altitude : {t_cross:.3f} s")

    dk.note(
        "The estimates land within about 15% of the measurements even though this "
        "plant has three poles, a right half-plane zero and an integrator. Its scaled "
        "impulse response equals the step response of a second-order pair with "
        "a RHP zero, which explains why these estimates are useful here. The one thing they do not predict is "
        "the sign of the first quarter second: the elevator deflection pushes the tail "
        "down and the whole aircraft sinks before the increased wing angle of attack "
        "converts into lift. That initial dip is the RHP zero at s = +6, and no "
        "amount of control gain removes it.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.2))

    for alpha, colour in [(0.5, dk.C["red"]), (1.0, dk.C["orange"]),
                          (2.0, dk.C["green"]), (100.0, dk.C["blue"])]:
        sysa = with_extra_pole(alpha) if alpha < 50 else lti([1.0], [1.0, 2 * ZETA, 1.0])
        _, y = step(sysa, T=t)
        lbl = "no extra pole" if alpha > 50 else f"$\\alpha$ = {alpha:g}"
        axes[0].plot(t, y, color=colour, lw=2.0, label=lbl)
    axes[0].axhline(1.0, ls=":", color="k", lw=1.0)
    axes[0].set_xlim(0, 20)
    axes[0].set_xlabel(r"normalised time $\omega_n t$")
    axes[0].set_title(f"Fig. 3.36: extra pole, $\\zeta$ = {ZETA}")
    axes[0].legend(fontsize=10)

    aa = np.linspace(0.4, 8.0, 40)
    trs = [rise_time(with_extra_pole(a), t)[0] for a in aa]
    axes[1].plot(aa, trs, color=dk.C["blue"], lw=2.4)
    axes[1].axhline(tr0, ls="--", color=dk.C["grey"], label="no extra pole")
    axes[1].set_xlabel(r"$\alpha$  (extra pole at $-\alpha\zeta\omega_n$)")
    axes[1].set_ylabel(r"$\omega_n t_r$")
    axes[1].set_title("Fig. 3.38: rise time versus the extra pole")
    axes[1].legend(fontsize=10)

    axes[2].plot(t2, h, color=dk.C["blue"], lw=2.4)
    axes[2].axhline(hf, ls="--", color=dk.C["red"],
                    label=f"final value {hf:.1f} (FVT)")
    axes[2].axhline(0, color="k", lw=0.8)
    axes[2].annotate(f"undershoot {undershoot:.2f}",
                     (t2[np.argmin(h)], undershoot), textcoords="offset points",
                     xytext=(18, -6), fontsize=10.5, color=dk.C["grey"],
                     arrowprops=dict(arrowstyle="->", color=dk.C["grey"]))
    axes[2].set_xlim(0, 6)
    axes[2].set_xlabel("time [s]")
    axes[2].set_ylabel("altitude [ft]")
    axes[2].set_title("Fig. 3.35: pull back, go down, then climb")
    axes[2].legend(fontsize=10, loc="lower right")

    fig.suptitle("Beyond the pure second order: an extra pole and a RHP zero",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo4_extra_pole_aircraft", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
