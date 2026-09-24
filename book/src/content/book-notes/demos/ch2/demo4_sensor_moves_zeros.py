"""
Demo 4  --  Move the sensor: the zeros change, the poles do not
                                                          (lecture §13 and §16)

Same masses, same springs, same dampers, same actuator. The only change is
which coordinate we choose to measure. The denominator D(s) is the determinant
of the system matrix -- a property of the plant -- so the poles cannot move.
The numerator depends on which row of the solution we read off, so the zeros
change completely.

Run:  uv run python demo4_sensor_moves_zeros.py
"""

import numpy as np
from scipy import signal

import demokit as dk
from twomass import TwoMass


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    p = TwoMass()

    n1, d1 = p.G_collocated()          # X1/U -- sensor on m1 (collocated)
    n2, d2 = p.G_noncollocated()       # X2/U -- sensor on m2 (noncollocated)

    poles1, poles2 = np.roots(d1), np.roots(d2)
    zeros1, zeros2 = np.roots(n1), np.roots(n2)

    dk.title("Demo 4 -- the poles belong to the plant, the zeros belong to the sensor")
    dk.note(
        f"Parameters: m1={p.m1:g}, m2={p.m2:g}, k1={p.k1:g}, k2={p.k2:g}, "
        f"c1={p.c1:g}, c2={p.c2:g}. The force u acts on m1 in both cases.")

    dk.section("poles  (roots of D(s), identical for both outputs)")
    dk.table(["X1/U poles", "X2/U poles", "difference"],
             [[dk.fmt_root(a), dk.fmt_root(b), f"{abs(a-b):.2e}"]
              for a, b in zip(np.sort_complex(poles1), np.sort_complex(poles2))])
    print(f"\n  largest discrepancy between the two pole sets: "
          f"{np.max(np.abs(np.sort_complex(poles1) - np.sort_complex(poles2))):.2e}")

    dk.section("zeros  (roots of N(s), completely different)")
    print(f"  collocated    X1/U :  numerator m2 s^2 + c2 s + k2")
    for z in np.sort_complex(zeros1):
        print(f"                        {dk.fmt_root(z)}")
    print(f"\n  noncollocated X2/U :  numerator c2 s + k2")
    for z in np.sort_complex(zeros2):
        print(f"                        {dk.fmt_root(z)}")

    wres = np.sort(np.abs(poles1[poles1.imag > 0]))
    wanti = abs(zeros1[zeros1.imag > 0][0])
    dk.note(
        f"Look at the ordering. The two resonances are at {wres[0]:.2f} and "
        f"{wres[1]:.2f} rad/s, and the collocated antiresonance falls at "
        f"{wanti:.2f} rad/s -- strictly between them. That is the interlacing property "
        "of §25, and it is why the collocated pair is guaranteed minimum phase. Move "
        "the sensor to m2 and the interlacing is gone: the only zero left is at "
        f"{zeros2[0].real:.0f} rad/s, far outside the band of interest.")

    # ------------------------------------------------------------------ figure
    fig = plt.figure(figsize=(13.5, 7.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.3], hspace=0.32, wspace=0.24)
    axA = fig.add_subplot(gs[0, 0])
    axB = fig.add_subplot(gs[1, 0])
    axM = fig.add_subplot(gs[:, 1])

    lim = 7.0
    for ax, zz, name, col in [(axA, zeros1, r"collocated:  $X_1/U$", dk.C["blue"]),
                              (axB, zeros2, r"noncollocated:  $X_2/U$", dk.C["green"])]:
        dk.splane(ax, poles=poles1, zeros=zz[np.abs(zz) < 50],
                  xlim=(-lim, lim), ylim=(-lim, lim), pole_color=col,
                  title_text=name)
        ax.set_aspect("equal")
        if not np.any(np.abs(zz) < 50):
            ax.text(0.5, 0.16, "no zero in this band\n(the only zero is at $s=-400$)",
                    transform=ax.transAxes, ha="center", va="center", fontsize=10,
                    color=dk.C["red"],
                    bbox=dict(fc="white", ec=dk.C["red"], alpha=0.9, lw=1.0, pad=4))

    w = np.logspace(np.log10(0.3), np.log10(40), 3000)
    for num, den, lab, col in [(n1, d1, r"$X_1/U$  (sensor on $m_1$, collocated)", dk.C["blue"]),
                               (n2, d2, r"$X_2/U$  (sensor on $m_2$, noncollocated)", dk.C["green"])]:
        _, h = signal.freqresp(signal.lti(num, den), w=w)
        axM.loglog(w, np.abs(h), color=col, label=lab)

    for wr in wres:
        axM.axvline(wr, color=dk.C["grey"], ls=":", lw=1.4)
    axM.axvline(wanti, color=dk.C["red"], ls="--", lw=1.8)
    axM.annotate(f"antiresonance\n{wanti:.2f} rad/s\n(zero of $X_1/U$ only)",
                 xy=(wanti, 3e-4), xytext=(9, 4e-4), fontsize=10.5, color=dk.C["red"],
                 arrowprops=dict(arrowstyle="->", color=dk.C["red"], lw=1.4))
    for wr in wres:
        axM.annotate(f"pole {wr:.2f}", xy=(wr, 2e-5), xytext=(wr * 1.04, 2.2e-5),
                     fontsize=10, color=dk.C["grey"], rotation=90, va="bottom")

    axM.set_xlabel(r"frequency $\omega$  [rad/s]")
    axM.set_ylabel(r"$|G(j\omega)|$")
    axM.set_title("Same two resonant peaks. Only one output has the notch.")
    axM.legend(fontsize=11, loc="lower left")
    axM.grid(True, which="both", alpha=0.2)

    fig.suptitle("We changed nothing but the sensor location", fontsize=15, y=0.98)
    dk.finish(plt, fig, "demo4_sensor_moves_zeros", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
