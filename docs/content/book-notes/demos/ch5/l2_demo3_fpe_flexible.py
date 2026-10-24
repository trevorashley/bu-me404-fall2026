"""FPE Section 5.3, Examples 5.8-5.10: collocated and noncollocated flexible modes, and complex multiple roots."""
import numpy as np
import kit as dk


def departure(pole, poles, zeros):
    """FPE Rule 4 at a simple pole, in degrees on (-180, 180]."""
    others = [p for p in poles if abs(p-pole) > 1e-6]
    total = sum(np.degrees(np.angle(pole-z)) for z in zeros) - sum(np.degrees(np.angle(pole-p)) for p in others) - 180
    return (total+180) % 360 - 180


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
    flex = np.polymul([1, 0.2, 0.01+6.6**2], [1, 0, 0])           # s^2 [(s+0.1)^2 + 6.6^2]
    lead_num, lead_den = [1, 1], [1, 12]

    # Example 5.8: collocated, numerator zeros at -0.1 +/- 6j.
    num = np.polymul(lead_num, [1, 0.2, 0.01+36])
    den = np.polymul(lead_den, flex)
    dk.locus(axes[0], num, den, np.r_[0, np.geomspace(0.01, 2e4, 6000)],
             xlim=(-14, 4), ylim=(-9, 9), title_text="Ex. 5.8 collocated: zeros near the flexible poles")
    pole = -0.1+6.6j
    poles, zeros = np.roots(den), np.roots(num)
    d8 = departure(pole, poles, zeros)
    axes[0].arrow(pole.real, pole.imag, 1.5*np.cos(np.deg2rad(d8)), 1.5*np.sin(np.deg2rad(d8)),
                  width=.04, color=dk.C["orange"], zorder=6)
    axes[0].text(-7.5, 7.2, rf"$\phi_{{dep}}={d8:.1f}^\circ$ (FPE: $142.6^\circ$)", fontsize=10, color=dk.C["orange"])

    # Example 5.9: noncollocated, no flexible zeros.
    num9 = lead_num
    dk.locus(axes[1], num9, den, np.r_[0, np.geomspace(0.01, 3e4, 6000)],
             xlim=(-14, 4), ylim=(-9, 9), title_text="Ex. 5.9 noncollocated: no flexible zeros")
    d9 = departure(pole, poles, np.roots(num9))
    axes[1].arrow(pole.real, pole.imag, 1.5*np.cos(np.deg2rad(d9)), 1.5*np.sin(np.deg2rad(d9)),
                  width=.04, color=dk.C["orange"], zorder=6)
    axes[1].text(-7.5, 7.2, rf"$\phi_{{dep}}={d9:.1f}^\circ$ (FPE: $-37.4^\circ$)", fontsize=10, color=dk.C["orange"])
    for angle in (45, 135, 225, 315):
        r = np.linspace(0, 14, 50)
        axes[1].plot(-2.8+r*np.cos(np.deg2rad(angle)), r*np.sin(np.deg2rad(angle)), "--", color=dk.C["grey"], lw=1)

    # Example 5.10: L = 1/(s(s+2)[(s+1)^2+4]); double roots at -1 +/- j sqrt(3/2) when K = 25/4.
    den10 = np.polymul([1, 2, 0], [1, 2, 5])
    dk.locus(axes[2], [1], den10, np.r_[np.linspace(0, 6.25, 3000), np.linspace(6.25, 80, 2500)],
             xlim=(-4.5, 2.5), ylim=(-3.5, 3.5), title_text="Ex. 5.10: $1/(s(s+2)[(s+1)^2+4])$")
    mult = [-1+1j*np.sqrt(1.5), -1-1j*np.sqrt(1.5)]
    axes[2].plot([m.real for m in mult], [m.imag for m in mult], "o", color=dk.C["orange"],
                 label=r"double roots $-1\pm1.225j$, $K=25/4$")
    axes[2].plot([-1], [0], "o", color=dk.C["red"], ms=5, label="breakaway $s=-1$, $K=4$")
    for angle in (45, 135, 225, 315):
        r = np.linspace(0, 6, 50)
        axes[2].plot(-1+r*np.cos(np.deg2rad(angle)), r*np.sin(np.deg2rad(angle)), "--", color=dk.C["grey"], lw=1)
    axes[2].legend(fontsize=9, loc="lower left")

    print(f"Example 5.8 (collocated): departure from -0.1+6.6j = {d8:.2f} deg exact; FPE's rounded vectors give 142.6 deg. Asymptote center -5.5.")
    print(f"Example 5.9 (noncollocated): departure = {d9:.2f} deg exact; FPE's rounded vectors give -37.4 deg. Asymptote center -2.8, angles +/-45, +/-135.")
    for K in (4, 6.25):
        print(f"Example 5.10 roots at K={K}:", ", ".join(dk.fmt_root(r) for r in np.roots(np.polyadd(den10, [K]))))
    print("Example 5.10: with u=(s+1)^2-1 the polynomial is u^2+5u+K; dP/ds=0 at s=-1 (K=4) and u=-5/2 (K=25/4, s=-1+/-j sqrt(3/2)).")
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo3_fpe_flexible", args)


if __name__ == "__main__":
    main()
