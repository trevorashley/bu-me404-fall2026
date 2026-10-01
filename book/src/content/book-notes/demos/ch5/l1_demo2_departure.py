"""Root-locus construction: complex-pole departure, repeated poles, and a right-half-plane zero."""
import numpy as np
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    dk.locus(axes[0], [1], [1, 6, 13, 20], np.linspace(0, 100, 3000),
             xlim=(-7, 2), ylim=(-4.5, 4.5), title_text="Complex-pole departure")
    angle = np.deg2rad(180-90-np.rad2deg(np.arctan2(2, 3)))
    axes[0].arrow(-1, 2, .9*np.cos(angle), .9*np.sin(angle), width=.025, color=dk.C["orange"], zorder=6)
    dk.locus(axes[1], [1], [1, 0, 0], np.linspace(0, 16, 2000),
             xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), title_text="Double integrator: ±90°")
    dk.locus(axes[2], [-1, 1], [1, 2, 0], np.linspace(0, 12, 3000),
             xlim=(-3, 8), ylim=(-5.5, 5.5), title_text="RHP zero: (1-s) / [s(s+2)]")
    print("Departure at -1+2j: 56.3099 degrees. Repeated origin poles: +/-90 degrees.")
    print("RHP-zero model has negative leading numerator coefficient; use the full signed transfer function.")
    print("Its polynomial is s^2+(2-K)s+K, stable for 0<K<2.")
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo2_departure", args)


if __name__ == "__main__":
    main()
