"""Lead and PD design: recompute FPE 7th/8th ed. Example 5.11, including its design iteration."""
import numpy as np
from scipy import signal
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    systems = {"initial: K=70, p=10": dk.closed_loop([70, 140], [1, 11, 10, 0]),
               "revised: K=91, p=13": dk.closed_loop([91, 182], [1, 14, 13, 0])}
    t = np.linspace(0, 8, 32001)
    traces = dk.response_table(systems, t)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for name, y in traces.items():
        axes[0].plot(t, y, label=name)
    axes[0].axhline(1.2, color=dk.C["red"], ls="--", lw=1, label="20% overshoot limit")
    axes[0].set(xlim=(0, 2), xlabel="time [s]", ylabel="output / unit step", title="Franklin Example 5.11")
    axes[0].legend(fontsize=10)
    for name, (k, p) in zip(systems, [(70, 10), (91, 13)]):
        den = [1, p+1, p+k, 2*k]
        # U/R = D_c/(1+D_c G), including the finite direct term.
        ur = signal.TransferFunction(np.polymul([k, 2*k], [1, 1, 0]), den)
        _, u = signal.step(ur, T=t)
        axes[1].plot(t, u, label=name)
    axes[1].set(xlim=(0, 1.5), xlabel="time [s]", ylabel="normalized actuator command", title="Faster damping costs initial effort")
    axes[1].legend(fontsize=10)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo2_franklin", args)


if __name__ == "__main__":
    main()
