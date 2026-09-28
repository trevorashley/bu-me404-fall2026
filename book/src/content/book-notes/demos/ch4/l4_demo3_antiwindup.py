"""
L4 Demo 3  --  Integrator windup, and the anti-windup loop that cures it
                                                  (FPE Section 9.3.1, Example 9.9)

Plant G(s) = 1/s, PI controller D_c(s) = 2 + 4/s, unity feedback, actuator
limited to |u| <= 1, unit reference step. The anti-windup is the scheme of
Fig. 9.21(b): the difference between the controller's demand u_c and the
saturated actuator output u is fed back through K_a into the integrator input,

    du_I/dt = k_I [ e - K_a (u_c - u) ],      u_c = k_P e + u_I,  u = sat(u_c).

While the actuator is not saturated, u_c = u and the extra term is zero: the
anti-windup loop is invisible to linear analysis.

The loop is simulated by explicit time stepping (dt = 1e-5 s), because the
saturation is nonlinear and a transfer function cannot represent it.

Run:  uv run python ch4/l4_demo3_antiwindup.py
"""

import numpy as np

import kit as dk

KP, KI, UMAX = 2.0, 4.0, 1.0
DT, TEND = 1e-5, 10.0


def simulate(Ka: float):
    n = int(round(TEND / DT))
    t = np.arange(n) * DT
    y = np.zeros(n)
    u = np.zeros(n)
    uc_log = np.zeros(n)
    uI_log = np.zeros(n)
    yk, uI = 0.0, 0.0
    for k in range(n):
        e = 1.0 - yk
        uc = KP * e + uI
        uk = min(max(uc, -UMAX), UMAX)
        y[k], u[k], uc_log[k], uI_log[k] = yk, uk, uc, uI
        uI += DT * KI * (e - Ka * (uc - uk))
        yk += DT * uk                       # plant 1/s
    return t, y, u, uc_log, uI_log


def last_saturated(t, u):
    idx = np.where(np.abs(u) >= UMAX - 1e-12)[0]
    return t[idx[-1]] if len(idx) else float("nan")


def error_zero_crossings(t, y):
    e = 1.0 - y
    s = np.sign(e)
    idx = np.where(s[1:] * s[:-1] < 0)[0]
    return t[idx + 1]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 3 -- windup: the integrator keeps charging while the actuator is pinned")

    runs = {}
    rows = []
    for Ka in [0.0, 1.0, 10.0, 100.0]:
        t, y, u, uc, uI = simulate(Ka)
        runs[Ka] = (t, y, u, uc, uI)
        zc = error_zero_crossings(t, y)
        rows.append([f"{Ka:g}", f"{100 * (y.max() - 1):.1f}%", f"{t[np.argmax(y)]:.2f}",
                     f"{last_saturated(t, u):.3f}", f"{zc[0]:.3f}", f"{zc[1]:.3f}",
                     f"{uI.max():.3f}", f"{u.min():+.3f}"])
    dk.table(["K_a", "overshoot", "t_peak", "leaves sat.", "1st e=0", "2nd e=0",
              "max u_I", "min u"], rows)

    dk.section("the no-anti-windup case, by hand")
    dk.note(
        "At t=0 the error is 1 and u_c = 2 + 0 > 1, so u = 1 and y = t: a ramp. The "
        "error 1 - t reaches zero at exactly t = 1 s, and by then the integrator holds "
        "u_I = 4 * integral_0^1 (1 - tau) d tau = 2. With y still climbing, u_c = "
        "2(1-t) + 2 - 2(t-1)^2 stays above 1 until 2x^2 + 2x - 1 = 0 with x = t - 1, "
        "i.e. t = 1 + (sqrt(3) - 1)/2 = 1.366 s. The plant is at full throttle for "
        "0.366 s after the output has already passed the target. That is windup.")
    print(f"\n  exact: leaves saturation at t = {1 + (np.sqrt(3) - 1) / 2:.4f} s")

    dk.section("what the anti-windup loop looks like while saturated")
    dk.note(
        "With u held at u_max, Fig. 9.21(c) reduces to u_c/e = (k_P s + k_I)/(s + K_a k_I) "
        "= (2s + 4)/(s + 40) for K_a = 10: the integrator has become a first-order lag "
        "with time constant 1/(K_a k_I) = 0.025 s, which cannot run away. Larger K_a "
        "helps with diminishing returns; K_a = 0 is the pure integrator again.")

    # ------------------------------------------------------------------ figure
    fig, axs = plt.subplots(1, 3, figsize=(16.5, 5.2))
    for Ka, colour, lab in [(0.0, dk.C["red"], "without anti-windup"),
                            (10.0, dk.C["blue"], "with anti-windup, $K_a$ = 10")]:
        t, y, u, uc, uI = runs[Ka]
        axs[0].plot(t, y, color=colour, label=lab)
        axs[1].plot(t, u, color=colour, label=lab)
        axs[2].plot(t, uI, color=colour, label=r"$u_I$, " + lab.split(",")[0])
    axs[0].axhline(1.0, ls=":", color="k", lw=1.0)
    axs[0].set_title("Output (cf. Fig. 9.23a)")
    axs[0].set_ylabel("$y$")
    axs[1].axhline(UMAX, ls="--", color=dk.C["grey"], lw=1.0)
    axs[1].axhline(-UMAX, ls="--", color=dk.C["grey"], lw=1.0)
    axs[1].set_title("Actuator output $u$ (cf. Fig. 9.23b)")
    axs[1].set_ylabel("$u$")
    axs[2].axvline(1.0, ls=":", color=dk.C["grey"], lw=1.0)
    axs[2].set_title("Integrator state $u_I$")
    axs[2].set_ylabel("$u_I$")
    for ax, loc in zip(axs, ["upper right", "center right", "upper right"]):
        ax.set_xlabel("time [s]")
        ax.set_xlim(0, 8)
        ax.legend(fontsize=10.5, loc=loc)
    fig.suptitle("Example 9.9: PI control of $1/s$ with $|u|\\leq 1$", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo3_antiwindup", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
