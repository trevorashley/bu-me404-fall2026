"""Root-locus construction: motor breakaway and cubic imaginary-axis crossing. Use --show live."""
import numpy as np
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    dk.locus(axes[0], [1], [1, 1, 0], np.r_[np.linspace(0, 1, 1500), np.linspace(1, 12, 1500)],
             xlim=(-4, 3), ylim=(-3.5, 3.5), title_text="Motor: 1 / [s(s+1)]")
    dk.gain_arrows(axes[0], [1], [1, 1, 0], 2, 3.2)
    axes[0].plot([-.5], [0], "o", color=dk.C["orange"], label="breakaway: K=0.25")
    axes[0].axvline(-.5, color=dk.C["grey"], ls="--", lw=1)
    axes[0].legend(fontsize=10, loc="lower left")
    dk.locus(axes[1], [1], [1, 6, 8, 0], np.r_[np.linspace(0, 60, 2500), np.linspace(60, 500, 1500)],
             xlim=(-10, 4), ylim=(-7, 7), title_text="Cubic: 1 / [s(s+2)(s+4)]")
    dk.gain_arrows(axes[1], [1], [1, 6, 8, 0], 15, 25)
    for angle in [60, 180, 300]:
        r = np.linspace(0, 12, 100)
        axes[1].plot(-2+r*np.cos(np.deg2rad(angle)), r*np.sin(np.deg2rad(angle)),
                     "--", color=dk.C["grey"], lw=1)
    axes[1].plot([0, 0], [np.sqrt(8), -np.sqrt(8)], "o", color=dk.C["orange"], label="crossing: K=48")
    axes[1].legend(fontsize=10, loc="lower left")
    print("Motor: s=-0.5 +/- sqrt(0.25-K). Cubic: stable precisely for 0<K<48.")
    sb = -2+2*np.sqrt(3)/3
    print(f"Cubic positive-gain breakaway: s={sb:.6f}, K={-sb*(sb+2)*(sb+4):.6f}")
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo1_motor_cubic", args)


if __name__ == "__main__":
    main()
