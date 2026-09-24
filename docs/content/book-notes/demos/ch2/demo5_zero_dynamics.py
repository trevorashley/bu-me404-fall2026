"""
Demo 5  --  Zero dynamics: holding the output at zero            (lecture §14)

Force the measured coordinate x1 to stay exactly zero. Is the system then
motionless? No. The second mass keeps ringing, and it rings at exactly the
roots of the numerator of X1/U -- which is the definition of a zero.

Holding the output at zero is not free. It takes a specific input,

    u(t) = -( c2 x2' + k2 x2 ),

which is precisely the coupling force m2 feeds back into m1. The actuator's
entire job is to cancel it.

Run:  uv run python demo5_zero_dynamics.py
"""

import numpy as np
from scipy.integrate import solve_ivp

import demokit as dk
from twomass import TwoMass


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    p = TwoMass()

    zeros = np.roots(p.A22())
    dk.title("Demo 5 -- the system moves while the measured output stays at zero")

    # The control law that holds y = x1 identically at zero.
    def u_hold(t, z):
        _, _, x2, v2 = z
        return -(p.c2 * v2 + p.k2 * x2)

    t = np.linspace(0, 60, 12000)
    z0 = [0.0, 0.0, 1.0, 0.0]           # x1 = 0 already; give m2 a displacement
    sol = solve_ivp(lambda tt, z: p.rhs(tt, z, u_hold), (0, t[-1]), z0,
                    t_eval=t, rtol=1e-12, atol=1e-14)
    x1, v1, x2, v2 = sol.y
    u = np.array([u_hold(tt, z) for tt, z in zip(t, sol.y.T)])

    dk.section("did the measured output stay at zero?")
    print(f"  max |x1(t)| over 60 s      = {np.max(np.abs(x1)):.3e}   (integration noise only)")
    print(f"  max |x2(t)| over 60 s      = {np.max(np.abs(x2)):.4f}")
    print(f"  max |u(t)|  over 60 s      = {np.max(np.abs(u)):.4f}")
    dk.note(
        "The sensor reads zero to machine precision for the whole minute, "
        "while the second mass swings through a displacement of order 1 and the "
        "actuator works continuously to keep it invisible. A sensor sees one "
        "projection of the state. It does not see the state.")

    # ------------------------------- the hidden motion IS the zero dynamics
    dk.section("what frequency and decay rate is the hidden motion?")
    peaks = [i for i in range(1, len(t) - 1)
             if x2[i] > x2[i - 1] and x2[i] > x2[i + 1] and x2[i] > 0]
    period = np.mean(np.diff(t[peaks]))
    w_meas = 2 * np.pi / period
    logdec = np.polyfit(t[peaks], np.log(x2[peaks]), 1)[0]
    dk.table(["quantity", "measured from the simulation", "root of m2 s^2 + c2 s + k2"],
             [["frequency  [rad/s]", f"{w_meas:.5f}", f"{abs(zeros[0].imag):.5f}"],
              ["decay rate [1/s]",   f"{logdec:+.5f}", f"{zeros[0].real:+.5f}"]])
    dk.note(
        "The hidden motion rings at the numerator roots -- the ZEROS of X1/U -- not at "
        "the poles of the plant. That is the whole content of §14: the zero dynamics "
        "are the natural modes of the subsystem left over when the measured coordinate "
        "is pinned. Here that is m2 hanging off a spring and damper anchored to a "
        "stationary m1.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 9), sharex=True)
    tmax = 40
    m = t <= tmax

    axes[0].plot(t[m], x1[m], color=dk.C["blue"], lw=2.5)
    axes[0].set_ylabel(r"$y = x_1$")
    axes[0].set_title(r"The measured output: identically zero, by construction")
    axes[0].set_ylim(-1.05, 1.05)
    axes[0].axhline(0, color="k", lw=1)
    axes[0].text(0.99, 0.9, f"max |x1| = {np.max(np.abs(x1)):.1e}",
                 transform=axes[0].transAxes, ha="right", fontsize=11,
                 color=dk.C["blue"])

    axes[1].plot(t[m], x2[m], color=dk.C["green"], lw=2.2, label=r"$x_2(t)$")
    env = np.exp(zeros[0].real * t[m])
    axes[1].plot(t[m], env, "--", color=dk.C["grey"], lw=1.4,
                 label=rf"$e^{{{zeros[0].real:+.3f}t}}$  (from the zero)")
    axes[1].plot(t[m], -env, "--", color=dk.C["grey"], lw=1.4)
    axes[1].axhline(0, color="k", lw=1)
    axes[1].set_ylabel(r"$x_2$")
    axes[1].set_title("Meanwhile the second mass is moving: this is the zero dynamics")
    axes[1].legend(fontsize=10.5, loc="upper right")

    axes[2].plot(t[m], u[m], color=dk.C["red"], lw=2.2)
    axes[2].axhline(0, color="k", lw=1)
    axes[2].set_ylabel(r"$u(t)$")
    axes[2].set_xlabel("time  [s]")
    axes[2].set_title(r"Holding $y\equiv 0$ is not free: $u=-(c_2\dot x_2+k_2x_2)$")

    fig.suptitle("Zero output does not mean zero motion, and does not mean zero effort",
                 fontsize=15, y=0.995)
    fig.tight_layout()
    dk.finish(plt, fig, "demo5_zero_dynamics", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
