"""Root-locus gain design: damping-ray intersection, all poles at one gain, and the complete response."""
import numpy as np
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    gain = 224/27
    systems = {"motor K=1": dk.closed_loop([1], [1, 1, 0]),
               "cubic K=224/27": dk.closed_loop([1], [1, 6, 8, 0], gain),
               "exact pair response": dk.closed_loop([16/9], [1, 4/3, 0])}
    t = np.linspace(0, 20, 20001)
    traces = dk.response_table(systems, t)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    dk.locus(axes[0], [1], [1, 6, 8, 0], np.linspace(0, 80, 4000),
             xlim=(-7, 1), ylim=(-4, 4), title_text="Select ζ=0.5; then find every root")
    a = np.linspace(0, 4, 100)
    for sign in [-1, 1]:
        axes[0].plot(-a, sign*np.sqrt(3)*a, "--", color=dk.C["orange"], lw=1)
    roots = np.roots(systems["cubic K=224/27"].den)
    axes[0].plot(roots.real, roots.imag, "s", color=dk.C["red"], label="K=224/27")
    axes[0].legend(fontsize=10, loc="lower left")
    for name, y in traces.items():
        axes[1].plot(t, y, label=name)
    axes[1].axhspan(1-dk.SETTLING_BAND, 1+dk.SETTLING_BAND, color=dk.C["grey"], alpha=.15)
    axes[1].set(xlim=(0, 12), xlabel="time [s]", ylabel="output / unit step", title="Check the full transfer function")
    axes[1].legend(fontsize=10)
    print("Cubic Kv=K/8=28/27; unit-ramp steady error=27/28.")
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo1_gain_design", args)


if __name__ == "__main__":
    main()
