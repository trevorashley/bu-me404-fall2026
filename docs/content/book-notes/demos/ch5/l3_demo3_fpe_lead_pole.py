"""FPE Section 5.4.1, Figs. 5.22-5.23: the motor with P and PD K(s+2), then lead (s+2)/(s+p) with p = 20 and 10."""
import numpy as np
import kit as dk


def roots_vs_gain(num, den, gains):
    return np.array([np.roots(np.polyadd(den, k*np.asarray(num, dtype=float))) for k in gains])


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))

    # Fig. 5.22: proportional (vertical line at -1/2) versus PD K(s+2) (circle centered on the zero).
    ax = axes[0]
    dk.splane(ax, [0, -1], [-2], xlim=(-4.5, 1), ylim=(-3, 3), title_text="FPE Fig. 5.22: $D_c=K$ and $D_c=K(s+2)$")
    for label in list(ax.texts):
        label.remove()
    rp = roots_vs_gain([1], [1, 1, 0], np.linspace(0, 9, 500))
    ax.plot(rp.real.ravel(), rp.imag.ravel(), ".", color=dk.C["blue"], ms=1.8, alpha=.6, label="P: roots as $K$ increases")
    rpd = roots_vs_gain([1, 2], [1, 1, 0], np.r_[np.linspace(0, 6, 900), np.linspace(6, 60, 300)])
    ax.plot(rpd.real.ravel(), rpd.imag.ravel(), ".", color=dk.C["orange"], ms=1.8, alpha=.6, label="PD $K(s+2)$: circle $|s+2|=\\sqrt{2}$")
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(2*np.cos(theta), 2*np.sin(theta), "--", color=dk.C["grey"], lw=1.2, label="$\\omega_n=2$")
    sel = {"P, $K=4$: $\\zeta=0.25$": np.roots([1, 1, 4]), "PD, $K=2$: $\\zeta=0.75$": np.roots([1, 3, 4])}
    for (name, r), color in zip(sel.items(), [dk.C["blue"], dk.C["orange"]]):
        ax.plot(r.real, r.imag, "s", color=color, ms=7, label=name, zorder=6)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(fontsize=8.5, loc="lower left")

    # Fig. 5.23: PD K(s+2) against lead K(s+2)/(s+p), p = 20 and p = 10.
    ax = axes[1]
    dk.splane(ax, [0, -1], [-2], xlim=(-12, 1), ylim=(-6.5, 6.5), title_text="FPE Fig. 5.23: $K(s+2)/(s+p)$")
    for label in list(ax.texts):
        label.remove()
    cases = [("PD $K(s+2)$", [1, 1, 0], None, dk.C["orange"], np.linspace(0, 60, 900)),
             ("lead, $p=20$", [1, 21, 20, 0], -20, dk.C["green"], np.linspace(0, 900, 1400)),
             ("lead, $p=10$", [1, 11, 10, 0], -10, dk.C["purple"], np.linspace(0, 450, 1400))]
    for name, den, pole, color, gains in cases:
        r = roots_vs_gain([1, 2], den, gains)
        ax.plot(r.real.ravel(), r.imag.ravel(), ".", color=color, ms=1.6, alpha=.55, label=name)
        if pole is not None:
            ax.plot([pole], [0], "x", ms=12, mew=2.6, color=color)
            ax.axvline((1-abs(pole))/2, color=color, ls=":", lw=1)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(fontsize=9, loc="lower left")

    print("Fig. 5.22: at wn = 2, proportional control needs K = 4 and gives zeta = 1/4;")
    print("           PD K(s+2) needs K = 2 and gives s^2+3s+4, zeta = 3/4, roots", np.roots([1, 3, 4]))
    print("Fig. 5.23: lead asymptote centres (0-1-p+2)/2 = -9.5 (p=20) and -4.5 (p=10);")
    print("           for small K the lead loci follow the PD circle; the pole lowers the damping later.")
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo3_fpe_lead_pole", args)


if __name__ == "__main__":
    main()
