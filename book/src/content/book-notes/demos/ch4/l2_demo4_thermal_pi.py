"""
L2 Demo 4  --  PI control of a thermal system        (Example 4.5, Figs. 4.11-4.15)

Two thermal masses: G(s) = K_o / [(tau1 s + 1)(tau2 s + 1)] with tau1 = 1 s,
tau2 = 10 s, K_o = 1000. The reference ramps at 30 C/s to 300 C at t = 10 s
and then holds. Three strategies, each also run with K_o changed by +/-10%:

  open loop  u = 0.3 (the inverse DC gain times 300)
  P          k_P = 0.03
  PI         k_P = 0.03, k_I = 0.003   -> controller zero at -0.1

The PI zero cancels the slow plant pole at -0.1 in the reference response.
The cancelled mode is still there: a step disturbance at the heater input
excites it, and it decays with the plant's own 10 s time constant.

Run:  uv run python ch4/l2_demo4_thermal_pi.py
"""

import numpy as np
from scipy.signal import lsim, lti, step

import kit as dk

TAU1, TAU2, KO = 1.0, 10.0, 1000.0
KP, KI = 0.03, 0.003


def plant_den():
    return np.polymul([TAU1, 1.0], [TAU2, 1.0])


def loops(Ko, kP, kI):
    """Return (Y/R, U/R, Y/W) for D_c = kP + kI/s, unity feedback."""
    P = plant_den()
    num_c = [kP, kI] if kI else [kP]
    den_c = [1.0, 0.0] if kI else [1.0]
    char = np.polyadd(np.polymul(den_c, P), Ko * np.array(num_c, dtype=float))
    YR = lti(Ko * np.array(num_c, dtype=float), char)
    UR = lti(np.polymul(num_c, P), char)
    YW = lti(Ko * np.array(den_c, dtype=float), char)
    return YR, UR, YW, char


def settle(t, y, target, band):
    out = np.nonzero(np.abs(y - target) > band)[0]
    if out[-1] == len(t) - 1:
        return None
    return t[out[-1] + 1]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L2 Demo 4 -- Example 4.5: open loop, P and PI on a thermal plant")

    t = np.linspace(0, 70, 70001)
    _, y_ol = step(lti([KO], plant_den()), T=t)
    y_ol *= 0.3
    ts_ol = settle(t, y_ol, 300.0, 3.0)
    dk.section("open loop, input step of 0.3")
    print(f"  1% settling time: {ts_ol:.2f} s   (Fig. 4.11: 47.1 s)")
    print(f"  with K_o 5% high, final value {1.05 * 300:.0f} C: the error is the gain error")

    tr = np.linspace(0, 30, 30001)
    r = np.minimum(30.0 * tr, 300.0)
    results = {}
    dk.section("ramp to 300 C, nominal and +/-10% K_o")
    rows = []
    for name, kI in [("P", 0.0), ("PI", KI)]:
        for Ko in [0.9 * KO, KO, 1.1 * KO]:
            YR, UR, _, char = loops(Ko, KP, kI)
            _, y, _ = lsim(YR, r, tr)
            _, u, _ = lsim(UR, r, tr)
            results[(name, Ko)] = (y, u)
            ts = settle(tr, y, 300.0, 3.0)
            rows.append([name, f"{Ko:.0f}", f"{y[-1]:.2f}", f"{300 - y[-1]:+.2f}",
                         f"{y.max():.2f}", "never" if ts is None else f"{ts:.2f}",
                         f"{u[-1]:.4f}",
                         ", ".join(dk.fmt_root(z, 3) for z in np.sort_complex(np.roots(char)))])
    dk.table(["ctrl", "K_o", "y(30)", "300-y", "max y", "t_s(1%)", "u(30)", "closed-loop roots"],
             rows)

    YR, _, _, char = loops(KO, KP, 0.0)
    p = np.roots(char)[0]
    print(f"\n  P loop: omega_n = {abs(p):.3f}, zeta = {-p.real / abs(p):.3f}"
          f"   (book: zeta = 0.3); offset 300/31 = {300 / 31:.2f} C")
    dk.note("The P loop's DC gain is 30/31, so the output stops 9.68 C short. The PI loop "
            "has no offset at any of the three plant gains. Its settling time, 13.44 s, "
            "matches Fig. 4.14.")

    dk.section("what the cancellation hides: unit step at the heater input")
    td = np.linspace(0, 80, 80001)
    _, _, YW, char = loops(KO, KP, KI)
    _, yw = step(YW, T=td)
    k = yw.argmax()
    print(f"  Y/W poles: " + ", ".join(dk.fmt_root(z, 3) for z in np.roots(char)))
    print(f"  peak {yw[k]:.2f} C at t = {td[k]:.2f} s")
    for tt in [10, 30, 60]:
        print(f"  y({tt:>2d} s) = {yw[int(tt * 1000)]:.3f} C   "
              f"({100 * yw[int(tt * 1000)] / yw[k]:.1f}% of peak)")
    dk.note("The disturbance response keeps the pole at -0.1: the tail decays like "
            "exp(-t/10), the plant's own slow mode, even though the reference response "
            "looks second order. A cancelled stable pole is legal; it is not gone.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(16.0, 5.2))
    ax = axes[0]
    ax.plot(tr, r, color="k", lw=1.2, ls="--", label="$r$")
    for name, c in [("P", dk.C["orange"]), ("PI", dk.C["blue"])]:
        for Ko, ls in [(0.9 * KO, ":"), (KO, "-"), (1.1 * KO, "-.")]:
            ax.plot(tr, results[(name, Ko)][0], color=c, ls=ls, lw=1.8,
                    label=f"{name}" if Ko == KO else None)
    ax.axhspan(297, 303, color=dk.C["green"], alpha=0.15)
    ax.set_ylim(250, 320)
    ax.set_xlim(5, 30)
    ax.set_title("Output near 300 C (Figs. 4.12, 4.14)")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("$y$ [C]")
    ax.legend(fontsize=10.5, loc="lower right")

    ax = axes[1]
    for name, c in [("P", dk.C["orange"]), ("PI", dk.C["blue"])]:
        for Ko, ls in [(0.9 * KO, ":"), (KO, "-"), (1.1 * KO, "-.")]:
            ax.plot(tr, results[(name, Ko)][1], color=c, ls=ls, lw=1.6,
                    label=f"{name}, $K_o$ = {Ko:.0f}")
    ax.set_title("Heater command (Figs. 4.13, 4.15)")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("$u$")
    ax.legend(fontsize=8.5, ncol=2, loc="lower right")

    ax = axes[2]
    ax.plot(td, yw, color=dk.C["blue"])
    ax.plot(td, yw[k] * np.exp(-(td - td[k]) / 10.0), color=dk.C["red"], ls=":",
            label=r"$\propto e^{-t/10}$")
    ax.set_title("PI: unit step at heater input")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("$y$ [C]")
    ax.legend(fontsize=10.5)

    fig.suptitle("Example 4.5: P leaves an offset, PI removes it; the slow mode "
                 "stays in the disturbance path", fontsize=14)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo4_thermal_pi", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
