"""
L4 Demo 2  --  Ziegler-Nichols by the ultimate-sensitivity method
                                                  (Example 4.10, and Routh)

Turn the integral and derivative terms off, raise k_P until the loop just
oscillates, and record the ultimate gain K_u and period P_u. Then (FPE Table 4.3):

    P   : k_P = 0.5 K_u
    PI  : k_P = 0.45 K_u,  T_I = P_u/1.2
    PID : k_P = 0.6 K_u,   T_I = P_u/2,  T_D = P_u/8

Part 1 does this for the heat exchanger model e^{-5s}/[(10s+1)(60s+1)]; the
book measured K_u = 15.3 and P_u = 42 s. Part 2 does it for a delay-free plant
1/(s+1)^3, where the experiment is exactly Routh's imaginary-axis crossing of
Chapter 3 and can be done with a pencil.

Run:  uv run python ch4/l4_demo2_ultimate_gain.py
"""

import numpy as np
from scipy.signal import lti, step

import heatx as hx
import kit as dk


def pid_tf(kP, TI, TD):
    """Ideal PID k_P(1 + 1/(T_I s) + T_D s) as (num, den)."""
    if not np.isfinite(TI):
        return np.array([kP * TD, kP]) if TD else np.array([kP]), np.array([1.0])
    return kP * np.array([TI * TD, TI, 1.0]), np.array([TI, 0.0])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 2 -- the ultimate gain: push the loop to the edge, then back off")

    # --------------------------------------------------------- heat exchanger
    dk.section("part 1: the heat exchanger (Example 4.10)")
    Ku, Pu, wu = hx.ultimate_point()
    print(f"  phase-crossover frequency  w_u = {wu:.5f} rad/s")
    print(f"  ultimate gain              K_u = {Ku:.3f}     (book, measured: 15.3)")
    print(f"  ultimate period            P_u = {Pu:.2f} s   (book, measured: 42 s)")

    # the experiment itself: a small pulse into the loop at k_P = K_u
    tt, yK, _ = hx.closed_loop(Ku, T=240.0, r=0.0, impulse=1.0)
    pk = hx.peaks(tt, yK)
    per = np.diff(tt[pk])
    print(f"  simulated at k_P = K_u: peak spacing {per.mean():.2f} s, "
          f"peak heights {yK[pk[0]]:.5f} -> {yK[pk[-1]]:.5f} (neither growing nor decaying)")

    dk.note(
        "The model gives K_u = 15.29, matching the book's 15.3; its period is 43.6 s "
        "against the book's 42 s read from a plot, a 4% difference. Tuning below "
        "uses the book's measured values, so the gains match the book exactly.")

    rows, runs = [], {}
    laws = [("P (book)", 0.5 * 15.3, np.inf, 0.0),
            ("PI (book)", 0.45 * 15.3, 42 / 1.2, 0.0),
            ("PID [beyond]", 0.6 * 15.3, 42 / 2, 42 / 8)]
    for name, kP, TI, TD in laws:
        t, y, u = hx.closed_loop(kP, TI, TD, N=10.0, T=400.0)
        runs[name] = (t, y, u)
        rows.append([name, f"{kP:.3f}", "--" if not np.isfinite(TI) else f"{TI:.2f}",
                     f"{TD:.2f}" if TD else "--", f"{y.max():.3f}",
                     f"{y[-1]:.4f}"])
    dk.table(["law", "k_P", "T_I [s]", "T_D [s]", "peak y", "y(400 s)"], rows)
    dk.note(
        "Table 4.3 on the book's measurements: k_P = 7.65 for P, and k_P = 6.885 with "
        "T_I = 35 s for PI -- exactly the book's numbers. The PID row, which the book "
        "does not simulate, uses a derivative on the measured output with a filter "
        "time T_D/10. All three overshoot heavily; the rules aim at quarter decay.")

    # --------------------------------------------------------- Routh link
    dk.section("part 2: the same experiment done by Routh, for 1/(s+1)^3")
    dk.note(
        "Characteristic equation with a pure gain K: (s+1)^3 + K = "
        "s^3 + 3s^2 + 3s + (1+K). Routh's s^1 entry is [3*3 - (1+K)]/3 = (8-K)/3, "
        "so K_u = 8. At K_u the s^2 row gives the auxiliary polynomial "
        "3s^2 + 9 = 0, so w_u = sqrt(3) and P_u = 2 pi / sqrt(3).")
    Ku3 = 8.0
    roots = np.roots([1, 3, 3, 1 + Ku3])
    wu3 = float(np.max(roots.imag))
    Pu3 = 2 * np.pi / wu3
    print(f"  roots at K = 8        : " + ", ".join(dk.fmt_root(r) for r in np.sort_complex(roots)))
    print(f"  w_u = {wu3:.5f} rad/s = sqrt(3) = {np.sqrt(3):.5f};  P_u = {Pu3:.4f} s")

    G3 = (np.array([1.0]), np.array([1.0, 3.0, 3.0, 1.0]))
    t3 = np.linspace(0, 40, 8001)
    rows, runs3 = [], {}
    for name, kP, TI, TD in [("P", 0.5 * Ku3, np.inf, 0.0),
                             ("PI", 0.45 * Ku3, Pu3 / 1.2, 0.0),
                             ("PID", 0.6 * Ku3, Pu3 / 2, Pu3 / 8)]:
        nD, dD = pid_tf(kP, TI, TD)
        L_num = np.polymul(nD, G3[0])
        L_den = np.polymul(dD, G3[1])
        cl_den = np.polyadd(L_den, L_num)
        _, y = step(lti(L_num, cl_den), T=t3)
        runs3[name] = y
        cl_roots = np.sort_complex(np.roots(cl_den))
        yfin = L_num[-1] / cl_den[-1]
        rows.append([name, f"{kP:.3f}", "--" if not np.isfinite(TI) else f"{TI:.4f}",
                     f"{TD:.4f}" if TD else "--", f"{100 * (y.max() / yfin - 1):.1f}%",
                     f"{yfin:.4f}", f"{max(cl_roots.real):+.4f}"])
    dk.table(["law", "k_P", "T_I", "T_D", "overshoot", "final y", "max Re(pole)"], rows)
    dk.note(
        "The PID row here uses the ideal derivative on the error, as in Table 4.3; "
        "its overshoot is typical of Ziegler-Nichols settings. Every closed loop is "
        "stable, which is all the rules promise; the designer then detunes.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axM, axR) = plt.subplots(1, 3, figsize=(16.5, 5.4))
    axL.plot(tt, yK, color=dk.C["blue"])
    for j in pk[:2]:
        axL.axvline(tt[j], color=dk.C["grey"], ls=":", lw=1.0)
    axL.annotate("", xy=(tt[pk[1]], yK[pk[0]] * 1.12), xytext=(tt[pk[0]], yK[pk[0]] * 1.12),
                 arrowprops=dict(arrowstyle="<->"))
    axL.text(0.5 * (tt[pk[0]] + tt[pk[1]]), yK[pk[0]] * 1.17, f"$P_u$ = {Pu:.1f} s",
             ha="center", fontsize=11.5)
    axL.set_ylim(-1.35 * yK.max(), 1.35 * yK.max())
    axL.set_xlabel("time [s]")
    axL.set_ylabel("output after a small pulse")
    axL.set_title(f"$k_P=K_u$ = {Ku:.2f}: neutral (cf. Fig. 4.25)")

    for (name, colour) in [("P (book)", dk.C["orange"]), ("PI (book)", dk.C["blue"]),
                           ("PID [beyond]", dk.C["green"])]:
        t, y, _ = runs[name]
        axM.plot(t, y, color=colour, label=name.replace(" [beyond]", ", filtered D"))
    axM.axhline(1.0, ls=":", color="k", lw=1.0)
    axM.set_xlim(0, 400)
    axM.set_xlabel("time [s]")
    axM.set_ylabel("output")
    axM.set_title("Heat exchanger, Table 4.3 gains (cf. Fig. 4.26)")
    axM.legend(fontsize=10.5)

    for name, colour in [("P", dk.C["orange"]), ("PI", dk.C["blue"]), ("PID", dk.C["green"])]:
        axR.plot(t3, runs3[name], color=colour, label=name)
    axR.axhline(1.0, ls=":", color="k", lw=1.0)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("output")
    axR.set_title(r"$1/(s+1)^3$: $K_u=8$, $P_u=2\pi/\sqrt{3}$ by Routh")
    axR.legend(fontsize=10.5)

    fig.suptitle("Ultimate-sensitivity tuning: find the edge of stability, then back off",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo2_ultimate_gain", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
