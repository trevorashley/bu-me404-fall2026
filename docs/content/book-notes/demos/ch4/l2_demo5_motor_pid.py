"""
PID control Demo 5  --  P, PI and PID on a DC motor's speed       (Example 4.6, Fig. 4.16)

Armature-controlled DC motor, speed output, parameters of Eq. (4.78), with
J_m and L_a scaled so that time is in milliseconds:

    (J s + b) Omega = K_t I + W,     (L_a s + R_a) I = V_a - K_e Omega.

Then Omega = G_v V_a + G_w W with the shared denominator
M(s) = (J s + b)(L_a s + R_a) + K_t K_e, G_v = K_t / M and G_w = (L_a s + R_a) / M.
The controller drives V_a from e = r - omega with gains from Eq. (4.79):
k_P = 3, k_I = 15, k_D = 0.3 (unused gains zero).

Run:  uv run python ch4/l2_demo5_motor_pid.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

J, B, LA, RA, KT, KE = 1.13e-2, 0.028, 0.1, 0.45, 0.067, 0.067
GAINS = {"P": (3.0, 0.0, 0.0), "PI": (3.0, 15.0, 0.0), "PID": (3.0, 15.0, 0.3)}


def M():
    return np.polyadd(np.polymul([J, B], [LA, RA]), [KT * KE])


def loops(kP, kI, kD):
    """Characteristic polynomial and the R->Y, W->Y transfer functions."""
    num_c = np.trim_zeros(np.array([kD, kP, kI]), "f")   # D_c = (kD s^2 + kP s + kI)/s
    den_c = np.array([1.0, 0.0])
    if kI == 0 and kD == 0:                 # pure P: no controller state
        num_c, den_c = np.array([kP]), np.array([1.0])
    char = np.polyadd(np.polymul(den_c, M()), KT * num_c)
    YR = lti(KT * num_c, char)
    YW = lti(np.polymul(den_c, [LA, RA]), char)
    return char, YR, YW


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("PID control Demo 5 -- Example 4.6: motor speed under P, PI and PID")

    ol = np.roots(M())
    print("  open-loop poles (1/ms): " + ", ".join(dk.fmt_root(z, 3) for z in ol))

    t = np.linspace(0, 6, 12001)
    rows, traces = [], {}
    for name, g in GAINS.items():
        char, YR, YW = loops(*g)
        _, yr = step(YR, T=t)
        _, yw = step(YW, T=t)
        traces[name] = (yr, yw)
        roots = np.sort_complex(np.roots(char))
        pair = [z for z in roots if z.imag > 1e-9][0]
        rows.append([name, ", ".join(dk.fmt_root(z, 2) for z in roots),
                     f"{-pair.real / abs(pair):.3f}",
                     f"{yr[-1]:.4f}", f"{yr.max():.3f}",
                     f"{yw[-1]:+.4f}", f"{yw.max():.3f}"])
    dk.table(["ctrl", "closed-loop roots [1/ms]", "zeta(pair)", "y_r(6)", "max y_r",
              "y_w(6)", "max y_w"], rows)

    den0 = B * RA + KT * KE
    print(f"\n  P, from the Final Value Theorem: reference {3 * KT / (den0 + 3 * KT):.4f}, "
          f"disturbance {RA / (den0 + 3 * KT):.4f}")
    dk.note(
        "P leaves errors in both responses. Adding the integral removes them but drags "
        "a complex pair toward the imaginary axis (zeta falls from 0.25 to 0.08), which "
        "is the extra ringing in Fig. 4.16. Adding the derivative moves that pair to "
        "zeta = 0.58 and keeps the zero steady-state error.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(16.0, 5.2))
    colours = {"P": dk.C["orange"], "PI": dk.C["blue"], "PID": dk.C["green"]}
    for name, (yr, yw) in traces.items():
        axes[0].plot(t, yw, color=colours[name], label=name)
        axes[1].plot(t, yr, color=colours[name], label=name)
    axes[0].axhline(0, color="k", lw=1.0)
    axes[0].set_title("(a) unit step disturbance torque")
    axes[1].axhline(1, color="k", ls="--", lw=1.0)
    axes[1].set_title("(b) unit step reference")
    for ax in axes[:2]:
        ax.set_xlabel("time [ms]")
        ax.set_ylabel("speed")
        ax.legend(fontsize=10.5)
    ax = axes[2]
    dk.splane(ax, xlim=(-18, 2), ylim=(-16, 16), title_text="Closed-loop roots [1/ms]")
    for name, g in GAINS.items():
        char, _, _ = loops(*g)
        r = np.roots(char)
        ax.plot(r.real, r.imag, "x", ms=12, mew=3, color=colours[name], label=name)
    ax.plot(ol.real, ol.imag, "+", ms=12, mew=2, color=dk.C["grey"], label="open loop")
    ax.set_xlabel(r"$\Re(s)$   [1/ms]")
    ax.set_ylabel(r"$\Im(s)$   [rad/ms]")
    ax.legend(fontsize=10, loc="lower left")
    fig.suptitle("Example 4.6: integral removes the offset, derivative restores the damping",
                 fontsize=14)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo5_motor_pid", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
