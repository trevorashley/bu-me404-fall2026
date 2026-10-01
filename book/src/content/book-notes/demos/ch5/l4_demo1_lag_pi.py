"""Lag and PI design: fivefold ramp-error improvement, Type 2 PI, and the slow tails."""
import numpy as np
from scipy import signal
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    controllers = {"P": ([1], [1]), "lag, z=.05": ([1, .05], [1, .01]),
                   "lag, z=.01": ([1, .01], [1, .002]), "PI, z=.01": ([1, .01], [1, 0])}
    systems = {name: dk.closed_loop(num, np.polymul(den, [1, 1, 0]))
               for name, (num, den) in controllers.items()}
    t = np.linspace(0, 1000, 100001)
    traces = dk.response_table(systems, t)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for name, y in traces.items():
        axes[0].plot(t, y, label=name)
        nc, dc = controllers[name]
        # E/R=S; ramp error from a ramp input. No numerical differentiation.
        char = systems[name].den
        sens = signal.TransferFunction(np.polymul(dc, [1, 1, 0]), char)
        _, e, _ = signal.lsim(sens, U=t, T=t)
        axes[1].plot(t, e, label=name)
        gs = signal.TransferFunction(dc, char)
        _, yw = signal.step(gs, T=t)
        axes[2].plot(t, yw, label=name)
    axes[0].axhspan(1-dk.SETTLING_BAND, 1+dk.SETTLING_BAND, color=dk.C["grey"], alpha=.15)
    axes[0].set(xlim=(0, 25), xlabel="time [s]", ylabel="output", title="Reference step: inspect the tail")
    axes[1].set(xlim=(0, 600), xlabel="time [s]", ylabel="tracking error", title="Unit ramp: error 1 → 0.2 → 0")
    axes[2].set(xlim=(0, 600), xlabel="time [s]", ylabel="output", title="Unit plant-input step disturbance")
    for ax in axes:
        ax.legend(fontsize=9)
    print("P: Kv=1; both lag designs: Kv=5; PI: Ka=.01, zero ramp error.")
    print("A small reference-step residue does not imply a small disturbance-step residue.")
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo1_lag_pi", args)
    fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5.5))
    gains = np.r_[0, np.geomspace(1e-7, 4, 4000)]
    for ax, name, pole in zip(axes2, ["Lag: (s+.01)/(s+.002)", "PI: (s+.01)/s"], [.002, 0]):
        den = np.polymul([1, pole], [1, 1, 0])
        dk.locus(ax, [1, .01], den, gains, xlim=(-.028, .006), ylim=(-.017, .017), title_text=name)
        roots = np.roots(np.polyadd(den, [1, .01]))
        slow = roots[np.argmin(abs(roots))]
        ax.plot(slow.real, slow.imag, "s", color="black", ms=5, zorder=6, label="slow root at K=1")
        ax.annotate(f"s = {slow.real:.6f}", xy=(slow.real, slow.imag),
                    xytext=(10, 35), textcoords="offset points", fontsize=10,
                    arrowprops={"arrowstyle": "->", "color": "black"}, zorder=7)
        ax.legend(fontsize=10, loc="lower left")
        ax.ticklabel_format(axis="both", style="sci", scilimits=(-2, -2))
    fig2.suptitle("Zoom near the origin: added poles, added zero, and the slow branch", fontsize=13)
    fig2.tight_layout()
    dk.finish(plt, fig2, "l4_demo1_lag_pi_locus", args)


if __name__ == "__main__":
    main()
