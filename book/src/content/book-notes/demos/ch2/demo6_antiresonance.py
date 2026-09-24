"""
Demo 6  --  Antiresonance: driving a mass that refuses to move   (lecture §15)

With an undamped coupling (c2 = 0) the collocated numerator m2 s^2 + k2 has
roots exactly on the imaginary axis at +/- j*sqrt(k2/m2). Drive the system at
that frequency and the first mass -- the one the force is applied to -- comes
to a complete stop in steady state, while the second mass swings happily.

This is the operating principle of the dynamic vibration absorber.

Run:  uv run python demo6_antiresonance.py
"""

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp

import demokit as dk
from twomass import TwoMass


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    p = TwoMass(c2=0.0)                     # undamped coupling -> exact notch
    w_anti = p.antiresonance()
    poles = np.roots(p.D())

    dk.title("Demo 6 -- at the antiresonance, the driven mass stands still")
    dk.note(
        f"Undamped coupling: c2 = 0, so the zeros of X1/U sit exactly on the imaginary "
        f"axis at +/- {w_anti:g}j rad/s. The plant is still stable overall -- c1 = "
        f"{p.c1:g} bleeds energy out through the first mass -- so any transient dies "
        "and we can look at a clean steady state.")
    print("\n  plant poles:", "  ".join(dk.fmt_root(z, 3) for z in np.sort_complex(poles)))
    print(f"  all stable: {np.all(poles.real < 0)}")

    # ---------------------------------------------------------- steady state
    # For a stable plant driven by u = sin(wt), the steady-state amplitude of an
    # output is exactly |G(jw)|.  No simulation needed -- this IS what the
    # transfer function means (§8).
    def amp(G, w):
        num, den = G
        return abs(np.polyval(num, 1j * w) / np.polyval(den, 1j * w))

    dk.section("steady-state amplitude when driven by u = sin(wt), from |G(jw)|")
    rows = []
    for w in [2.0, 3.0, w_anti, 5.0, 6.0]:
        a1, a2 = amp(p.G_collocated(), w), amp(p.G_noncollocated(), w)
        tag = "  <-- antiresonance" if abs(w - w_anti) < 1e-9 else ""
        ratio = "infinite" if a1 < 1e-14 else f"{a2/a1:.1f}"
        rows.append([f"{w:.2f}", f"{a1:.3e}", f"{a2:.4f}", ratio, tag])
    dk.table(["drive w", "|x1| amplitude", "|x2| amplitude", "ratio x2/x1", ""], rows)

    a1, a2 = amp(p.G_collocated(), w_anti), amp(p.G_noncollocated(), w_anti)
    print(f"\n  |X1/U| at the antiresonance = {a1:.3e}   (an exact algebraic zero)")

    # One simulation, to watch the transient die and confirm the prediction.
    tend = 300.0
    t = np.linspace(0, tend, 12000)
    sol = solve_ivp(lambda tt, z: p.rhs(tt, z, lambda t_, z_: np.sin(w_anti * t_)),
                    (0, tend), [0, 0, 0, 0], t_eval=t, rtol=1e-10, atol=1e-12)
    y = sol.y
    tail = t > tend * 0.9
    sim1, sim2 = np.ptp(y[0][tail]) / 2, np.ptp(y[2][tail]) / 2
    dk.section("simulation check")
    dk.table(["output", "predicted |G(jw)|", "simulated amplitude"],
             [["x1", f"{a1:.3e}", f"{sim1:.3e}"],
              ["x2", f"{a2:.4f}", f"{sim2:.4f}"]])
    dk.note(
        f"x2 matches to four figures. The small residue on x1 is not a discrepancy in "
        f"the steady state -- it is the plant's own transient, which decays only as "
        f"e^(-0.027t) here and has not quite vanished after {tend:g} s. Run longer and "
        "it keeps shrinking; the steady-state value really is zero.")
    dk.note(
        f"At w = {w_anti:g} rad/s the transfer function from force to x1 is exactly zero, "
        f"so the driven mass has no steady-state motion at all, while the absorber mass "
        f"swings at {a2:.3f}. The force is still being applied "
        "every second of that. The second mass and the coupling spring return exactly "
        "the force the actuator applies, and the two cancel at m1.")

    # energy is emphatically not zero
    tail = t > t[-1] * 0.9
    ke = 0.5 * p.m2 * y[3][tail] ** 2
    pe = 0.5 * p.k2 * (y[2][tail] - y[0][tail]) ** 2
    print(f"\n  mean stored energy in the m2 branch while x1 ~ 0:  "
          f"{np.mean(ke + pe):.4f}  (kinetic + potential)")
    print("  -> 'measured output is zero' does not mean 'the system holds no energy'.")

    # ------------------------------------------------------------------ figure
    fig = plt.figure(figsize=(13.5, 7.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1], hspace=0.35, wspace=0.22)
    axS = fig.add_subplot(gs[:, 0])
    axT = fig.add_subplot(gs[0, 1])
    axB = fig.add_subplot(gs[1, 1])

    w = np.logspace(np.log10(0.5), np.log10(20), 4000)
    for (num, den), lab, col in [(p.G_collocated(), r"$X_1/U$  (driven mass)", dk.C["blue"]),
                                 (p.G_noncollocated(), r"$X_2/U$  (absorber mass)", dk.C["green"])]:
        _, h = signal.freqresp(signal.lti(num, den), w=w)
        axS.loglog(w, np.abs(h), color=col, label=lab)
    axS.axvline(w_anti, color=dk.C["red"], ls="--", lw=1.8)
    axS.annotate(f"exact null at\n$\\omega=\\sqrt{{k_2/m_2}}={w_anti:g}$ rad/s",
                 xy=(w_anti, 1e-6), xytext=(5.2, 3e-6), fontsize=11, color=dk.C["red"],
                 arrowprops=dict(arrowstyle="->", color=dk.C["red"], lw=1.4))
    axS.set_xlabel(r"drive frequency $\omega$  [rad/s]")
    axS.set_ylabel(r"$|G(j\omega)|$")
    axS.set_title("The notch goes all the way down when $c_2=0$")
    axS.legend(fontsize=11, loc="lower left")
    axS.grid(True, which="both", alpha=0.2)

    m = (t > t[-1] - 12)
    axT.plot(t[m], np.sin(w_anti * t[m]), color=dk.C["orange"], lw=2,
             label=r"applied force $u=\sin(\omega t)$")
    axT.axhline(0, color="k", lw=1)
    axT.legend(fontsize=10.5, loc="upper right")
    axT.set_title("Steady state at the antiresonance")
    axT.set_ylim(-1.4, 1.9)

    axB.plot(t[m], y[2][m], color=dk.C["green"], lw=2.2, label=r"$x_2$ (absorber)")
    axB.plot(t[m], y[0][m], color=dk.C["blue"], lw=2.8, label=r"$x_1$ (driven mass)")
    axB.axhline(0, color="k", lw=1)
    axB.set_xlabel("time  [s]")
    axB.legend(fontsize=10.5, loc="upper right")
    axB.set_title(r"$x_1$ is flat on this scale; $x_2$ is not")

    fig.suptitle("Force it, and it does not move: the collocated zero made physical",
                 fontsize=15, y=0.98)
    dk.finish(plt, fig, "demo6_antiresonance", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
