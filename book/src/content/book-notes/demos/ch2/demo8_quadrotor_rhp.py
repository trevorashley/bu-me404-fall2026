"""
Demo 8  --  The quadrotor's right-half-plane zero          (lecture §29 and §30)

Planar quadrotor near hover:   x'' = g*theta,   J*theta'' = M.

Measure the horizontal position of a point a distance h from the centre of
mass. A point ABOVE the CM moves as x + h*theta; a point BELOW moves as
x - h*theta. Only the second gives a right-half-plane zero.

Setting y == 0 forces x = h*theta, hence h*theta'' = g*theta, i.e.

    theta'' = (g/h) * theta

which is an INVERTED pendulum equation -- it diverges at rate sqrt(g/h). That
is where the zero comes from, and why it is not a "pendulum frequency".

Run:  uv run python demo8_quadrotor_rhp.py
"""

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp

import demokit as dk

G, JJ, H = 9.81, 0.02, 0.20


def tf(h_signed):
    """Y/M for y = x + h_signed*theta.  Numerator (g + h_signed s^2)/J s^4."""
    return np.array([h_signed, 0.0, G]), np.array([JJ, 0, 0, 0, 0])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    z = np.sqrt(G / H)
    dk.title("Demo 8 -- move the sensor below the centre of mass and the zero goes unstable")
    dk.note(
        f"g = {G} m/s^2, J = {JJ} kg m^2, offset h = {H} m. The three measurement "
        "choices below share identical dynamics and an identical actuator. They differ "
        "only in which point on the airframe we decide to call the output.")

    dk.section("same plant, three outputs")
    rows = []
    for label, hs in [("at the centre of mass  (y = x)", 0.0),
                      (f"h={H} m ABOVE the CM   (y = x + h th)", +H),
                      (f"h={H} m BELOW the CM   (y = x - h th)", -H)]:
        num, den = tf(hs)
        zz = np.roots(num) if abs(hs) > 0 else np.array([])
        pp = np.roots(den)
        zs = "  none (finite)" if not len(zz) else "  ".join(dk.fmt_root(q, 3) for q in zz)
        kind = ("minimum phase" if not len(zz) else
                ("on the jw axis" if np.max(np.abs(zz.real)) < 1e-9 else "NONMINIMUM PHASE"))
        rows.append([label, f"{len(pp)} poles at 0", zs, kind])
    dk.table(["output", "poles", "zeros", "character"], rows)

    print(f"\n  the RHP zero sits at  z = sqrt(g/h) = {z:.4f} rad/s")

    # ------------------------------------- analytic step response, verified
    dk.section("step response of the point below the CM (analytic vs simulated)")
    dk.note(
        "With Y/M = (g - h s^2)/(J s^4), a unit step in torque gives, exactly, "
        "y(t) = (g t^4/24 - h t^2/2)/J. The t^2 term is negative and dominates early; "
        "the t^4 term is positive and takes over later. That is the inverse response.")
    t = np.linspace(0, 1.2, 4000)
    y_exact = (G * t ** 4 / 24 - H * t ** 2 / 2) / JJ
    _, y_sim = signal.step(signal.lti(*tf(-H)), T=t)
    print(f"  max |analytic - scipy.signal.step| = {np.max(np.abs(y_exact - y_sim)):.3e}")

    t_min = np.sqrt(6 * H / G)
    t_cross = np.sqrt(12 * H / G)
    y_min = -1.5 * H ** 2 / (G * JJ)
    print(f"\n  most-wrong-way point   t = sqrt(6h/g)  = {t_min:.4f} s,  y = {y_min:.4f} m")
    print(f"  returns through zero   t = sqrt(12h/g) = {t_cross:.4f} s")
    print(f"  simulated minimum      t = {t[np.argmin(y_sim)]:.4f} s,  "
          f"y = {np.min(y_sim):.4f} m")

    # --------------------------------------- the zero dynamics, integrated
    dk.section("the zero dynamics: hold y at zero and watch what the airframe must do")
    th0 = 0.01
    sol = solve_ivp(lambda tt, s_: [s_[1], (G / H) * s_[0]], (0, 1.6), [th0, 0.0],
                    t_eval=np.linspace(0, 1.6, 2000), rtol=1e-11, atol=1e-13)
    tz, th = sol.t, sol.y[0]
    fit = np.polyfit(tz[tz > 1.0], np.log(th[tz > 1.0]), 1)[0]
    dk.table(["quantity", "value"],
             [["divergence rate fitted from the simulation", f"{fit:.5f} 1/s"],
              ["sqrt(g/h)", f"{z:.5f} 1/s"],
              ["RHP zero of Y/M", f"{max(np.roots(tf(-H)[0]).real):.5f}"]])
    dk.note(
        "All three are the same number. Note the sign of the zero-dynamics equation: "
        "theta'' = +(g/h) theta diverges, whereas a hanging pendulum obeys "
        "theta'' = -(g/h) theta and oscillates. The magnitudes coincide, the behaviour "
        "is opposite. To keep that camera perfectly still the vehicle would have to "
        "pitch over faster and faster -- unstable zero dynamics, made visible.")

    # ------------------------------------------------------------------ figure
    fig = plt.figure(figsize=(13.5, 7.4))
    gs = fig.add_gridspec(2, 2, hspace=0.36, wspace=0.24)
    axA = fig.add_subplot(gs[0, :])
    axB = fig.add_subplot(gs[1, 0])
    axC = fig.add_subplot(gs[1, 1])

    for hs, col, lab in [(+H, dk.C["green"], rf"above the CM:  $y=x+{H:g}\theta$"),
                         (0.0, dk.C["blue"],  r"at the CM:  $y=x$"),
                         (-H, dk.C["red"],   rf"below the CM:  $y=x-{H:g}\theta$")]:
        num, den = tf(hs)
        _, yy = signal.step(signal.lti(num, den), T=t)
        axA.plot(t, yy, color=col, lw=2.6, label=lab)
    axA.axhline(0, color="k", lw=1.2)
    axA.axvline(t_cross, color=dk.C["grey"], ls=":", lw=1.5)
    axA.annotate(f"wrong way until\n$t=\\sqrt{{12h/g}}={t_cross:.2f}$ s",
                 xy=(t_min, y_min), xytext=(0.60, -0.42), fontsize=11,
                 color=dk.C["red"],
                 arrowprops=dict(arrowstyle="->", color=dk.C["red"], lw=1.4))
    axA.set_xlabel("time  [s]")
    axA.set_ylabel("y(t)  [m]")
    axA.set_title("Unit step in pitch torque, first 0.85 s: only the point below "
                  "the CM reverses\n(all three curves keep rising after this window)",
                  fontsize=13.5)
    axA.legend(fontsize=11, loc="upper left")
    axA.set_ylim(-0.5, 1.15)
    axA.set_xlim(0, 0.85)

    dk.splane(axB, poles=np.roots(tf(-H)[1]), zeros=np.roots(tf(-H)[0]),
              xlim=(-9, 9), ylim=(-9, 9),
              title_text="Below the CM: a zero at $+\\sqrt{g/h}$")
    axB.set_aspect("equal")
    axB.annotate(f"$z=+{z:.2f}$", xy=(z, 0), xytext=(z - 1.4, 3.0),
                 fontsize=12, color=dk.C["red"], weight="bold")
    axB.annotate("4 poles\nat the origin", xy=(0, 0), xytext=(-8.2, 4.2),
                 fontsize=10.5, color=dk.C["blue"])

    axC.semilogy(tz, th, color=dk.C["red"], lw=2.6, label=r"$\theta(t)$ with $y\equiv 0$")
    axC.semilogy(tz, th0 * np.cosh(z * tz), "--", color=dk.C["grey"], lw=1.8,
                 label=rf"$\theta_0\cosh(\sqrt{{g/h}}\,t)$")
    axC.set_xlabel("time  [s]")
    axC.set_ylabel(r"pitch angle $\theta$  [rad]")
    axC.set_title("The zero dynamics diverge (log scale)")
    axC.legend(fontsize=10.5, loc="lower right")

    fig.suptitle("A right-half-plane zero is a visible, unstable internal motion",
                 fontsize=15, y=0.985)
    dk.finish(plt, fig, "demo8_quadrotor_rhp", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
