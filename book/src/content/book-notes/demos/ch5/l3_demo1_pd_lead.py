"""Lead and PD design: exact PD and lead design for -2 +/- 2j; pole targets versus actual response."""
import numpy as np
from scipy import signal
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    pd = dk.closed_loop([3, 8], [1, 1, 0])
    lead = dk.closed_loop([20, 40], [1, 9, 8, 0])
    systems = {"P: K=8": dk.closed_loop([8], [1, 1, 0]),
               "PD: 3s+8": pd, "lead: 20(s+2)/(s+8)": lead,
               "rate feedback: no reference zero": signal.TransferFunction([8], [1, 4, 8])}
    t = np.linspace(0, 20, 40001)
    traces = dk.response_table(systems, t)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    dk.locus(axes[0], [1, 8/3], [1, 1, 0], np.linspace(0, 15, 3000),
             xlim=(-9, 1), ylim=(-5, 5), title_text="PD locus: K(s+8/3)")
    dk.locus(axes[1], [1, 2], [1, 9, 8, 0], np.linspace(0, 90, 4000),
             xlim=(-9, 1), ylim=(-5, 5), title_text="Lead locus: K(s+2)/(s+8)")
    dk.gain_arrows(axes[0], [1, 8/3], [1, 1, 0], 4, 5.5)
    dk.gain_arrows(axes[1], [1, 2], [1, 9, 8, 0], 27, 35)
    for ax, system in zip(axes[:2], [pd, lead]):
        roots = np.roots(system.den)
        ax.plot(roots.real, roots.imag, "s", color=dk.C["orange"])
    for name, y in traces.items():
        axes[2].plot(t, y, label=name)
    axes[2].set(xlim=(0, 5), xlabel="time [s]", ylabel="output / unit step", title="Same target pair, different responses")
    axes[2].legend(fontsize=8.5)
    print("Lead: u(0+)=20 for a unit reference step. Ideal forward-path PD demands an impulse of area 3.")
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo1_pd_lead", args)


if __name__ == "__main__":
    main()
