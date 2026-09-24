"""
L1 Demo 4  --  A double integrator, one thruster pulse, and two    (Example 3.21)

The satellite of Example 2.3 has H(s) = d/I / s^2 = 0.0002/s^2 with d = 1 m and
I = 5000 kg m^2. Fire a 25 N thruster for 0.1 s at t = 5 s and the attitude
drifts forever, because nothing removes the angular momentum the pulse added.
Fire an equal and opposite pulse 1.1 s later and the drift stops at a new angle.

That pair of pulses is how attitude is actually commanded, and it is a pole at
the origin made visible.

Run:  uv run python ch3/l1_demo4_satellite_pulse.py
"""

import numpy as np

import kit as dk

D, I = 1.0, 5000.0
GAIN = D / I                 # 0.0002 rad/(N s^2)
F, T_ON, DUR = 25.0, 5.0, 0.1
T_OFF = 6.1
RAD2DEG = 180.0 / np.pi


def simulate(t, thrust):
    """Two integrations of the applied torque: theta'' = (d/I) u."""
    dt = t[1] - t[0]
    rate = GAIN * np.cumsum(thrust) * dt
    return np.cumsum(rate) * dt, rate


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L1 Demo 4 -- the pole at the origin, seen as a satellite that drifts")

    t = np.arange(0.0, 10.0, 0.001)
    single = np.where((t >= T_ON) & (t < T_ON + DUR), F, 0.0)
    double = single - np.where((t >= T_OFF) & (t < T_OFF + DUR), F, 0.0)

    th1, rate1 = simulate(t, single)
    th2, rate2 = simulate(t, double)

    impulse = F * DUR  # force impulse; angular impulse is D * impulse
    predicted_rate = GAIN * impulse
    predicted_angle = predicted_rate * (T_OFF - T_ON)

    dk.note(
        f"H(s) = {GAIN} / s^2. A {F:g} N thrust held for {DUR:g} s delivers an angular "
        f"impulse of {D*impulse:g} N m s, which the double integrator turns into a "
        f"constant rate: theta_dot = (d/I) * {impulse:g} = {predicted_rate:.2e} rad/s "
        f"= {predicted_rate*RAD2DEG:.4f} deg/s.")

    dk.section("single pulse: a step in rate, a ramp in angle")
    dk.table(["quantity", "predicted", "simulated"],
             [["rate after the pulse [deg/s]", f"{predicted_rate*RAD2DEG:.5f}",
               f"{rate1[-1]*RAD2DEG:.5f}"],
              ["angle at t = 10 s [deg]",
               f"{predicted_rate*(10 - T_ON - DUR/2)*RAD2DEG:.5f}",
               f"{th1[-1]*RAD2DEG:.5f}"]])

    dk.section("equal and opposite pulse 1.1 s later: rate back to zero")
    dk.table(["quantity", "predicted", "simulated"],
             [["final rate [deg/s]", "0.00000", f"{rate2[-1]*RAD2DEG:.5f}"],
              ["final angle [deg]", f"{predicted_angle*RAD2DEG:.5f}",
               f"{th2[-1]*RAD2DEG:.5f}"]])

    dk.note(
        "The second pulse cancels the momentum but not the angle. That is the whole "
        "content of a double pole at s = 0: the free motion is a constant plus a ramp, "
        "so the system remembers everything it has ever been given and returns nothing "
        "on its own. A single pulse has no finite final angle; balanced opposite "
        "pulses do have a finite final angle. Check the transform of the actual input.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 7.6), sharex=True)

    for col, (thrust, theta, title) in enumerate([
            (single, th1, "Fig. 3.7: one pulse"),
            (double, th2, "Fig. 3.8: pulse and counter-pulse")]):
        axes[0][col].plot(t, thrust, color=dk.C["orange"], lw=2.0)
        axes[0][col].set_ylabel("thrust [N]")
        axes[0][col].set_title(title)
        axes[0][col].set_ylim(-30, 30)
        axes[1][col].plot(t, theta * RAD2DEG, color=dk.C["blue"], lw=2.4)
        axes[1][col].set_ylabel(r"attitude $\theta$ [deg]")
        axes[1][col].set_xlabel("time [s]")
        axes[1][col].set_ylim(-0.005, 0.16)

    axes[1][1].axhline(predicted_angle * RAD2DEG, ls="--", color=dk.C["grey"])
    axes[1][1].text(6.4, predicted_angle * RAD2DEG + 0.006,
                    f"holds at {predicted_angle*RAD2DEG:.4f}$^\\circ$",
                    color=dk.C["grey"], fontsize=11)

    fig.suptitle("Satellite attitude: $H(s) = 0.0002/s^2$", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo4_satellite_pulse", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
