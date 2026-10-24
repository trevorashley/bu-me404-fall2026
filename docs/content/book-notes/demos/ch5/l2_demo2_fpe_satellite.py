"""FPE Section 5.3, Examples 5.3-5.7: the double-integrator satellite with PD, then lead with the pole at 12, 9, and 4."""
import numpy as np
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.8))

    # Example 5.3: PD, L = (s+1)/s^2. Circle centred on the zero, break-in at -2 when K = 4.
    dk.locus(axes[0], [1, 1], [1, 0, 0], np.r_[np.linspace(0, 4, 2500), np.linspace(4, 60, 1500)],
             xlim=(-4, 1.5), ylim=(-2.5, 2.5), title_text="Ex. 5.3 PD: $(s+1)/s^2$")
    axes[0].plot([-2], [0], "o", color=dk.C["orange"], label="break-in: $s=-2$, $K=4$")
    axes[0].legend(fontsize=9, loc="lower left")

    # Examples 5.4-5.6: lead, L = (s+1)/(s^2 (s+p)).
    cases = [(12, "Ex. 5.4 lead, $p=12$", (-14, 2), (-6, 6)),
             (9, "Ex. 5.6 transition, $p=9$", (-10, 2), (-5, 5)),
             (4, "Ex. 5.5 lead, $p=4$", (-6, 2), (-5, 5))]
    for ax, (p, name, xlim, ylim) in zip(axes[1:], cases):
        den = [1, p, 0, 0]
        dk.locus(ax, [1, 1], den, np.r_[np.linspace(0, 60, 3000), np.linspace(60, 600, 1500)],
                 xlim=xlim, ylim=ylim, title_text=name)
        alpha = (1-p)/2
        ax.axvline(alpha, color=dk.C["grey"], ls="--", lw=1)
        # Real-axis multiple roots: s(2s^2+(3+p)s+2p)=0, real only when (p-1)(p-9) >= 0.
        disc = (3+p)**2-16*p
        if disc >= 0:
            pts = np.roots([2, 3+p, 2*p])
            gains = [-x*x*(x+p)/(x+1) for x in pts]
            label = (f"triple root $s={pts[0].real:.0f}$ ($K={gains[0].real:.0f}$)" if disc == 0 else
                     ", ".join(f"$s={x.real:.3f}$ ($K={k.real:.1f}$)" for x, k in zip(pts, gains)))
            ax.plot(pts.real, pts.imag, "o", color=dk.C["orange"], label=label)
            ax.legend(fontsize=8.5, loc="lower left")
        print(f"p={p}: asymptote center {alpha}; discriminant (p-1)(p-9)={disc}; "
              + ("multiple roots at " + ", ".join(f"{x.real:.4f} (K={k.real:.4f})" for x, k in zip(pts, gains))
                 if disc >= 0 else "no real-axis multiple roots"))
    print("Example 5.3: K = 2(1-cos(theta)) on the circle |s+1|=1; break-in at s=-2 with K=4 since s^2+4(s+1)=(s+2)^2.")
    print("Example 5.6: at p=9 the real-axis multiple root is triple, s^2(s+9)+27(s+1)=(s+3)^3.")
    print("Example 5.7 conclusion: a pole moving in from the far left pushes the locus branches to the right.")
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo2_fpe_satellite", args)


if __name__ == "__main__":
    main()
