"""Lag and PI design extensions: Franklin lead-lag, notch detuning, and rate feedback."""
import numpy as np
from scipy import signal
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    lead_num, lead_den = [91, 182], [1, 14, 13, 0]
    systems = {"lead": dk.closed_loop(lead_num, lead_den),
               "lead-lag": dk.closed_loop(np.polymul(lead_num, [1, .05]),
                                          np.polymul(lead_den, [1, .01]))}
    t = np.linspace(0, 300, 60001)
    traces = dk.response_table(systems, t)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for name, y in traces.items():
        axes[0].plot(t, y, label=name)
    axes[0].set(xlim=(0, 3), xlabel="time [s]", ylabel="output", title="FPE §5.4.2: Kv 14 → 70")
    axes[0].legend(fontsize=10)
    omega = np.linspace(5, 15, 2000)
    sn = 1j*omega
    notch = (sn**2+.6*sn+100)/(sn**2+6*sn+100)
    axes[1].plot(omega, abs(notch), color=dk.C["blue"])
    for w in [8, 10, 12]:
        value = abs(((1j*w)**2+.6j*w+100)/((1j*w)**2+6j*w+100))
        axes[1].plot(w, value, "o", color=dk.C["orange"])
        print(f"Notch magnitude at {w} rad/s: {value:.4f}")
    axes[1].set(xlabel="sinusoidal frequency [rad/s]", ylabel="amplitude ratio", title="Notch: attenuation depends on tuning")
    short = np.linspace(0, 5, 10001)
    for name, numerator in [("forward PD", [3, 8]), ("rate feedback", [8])]:
        _, y = signal.step(signal.TransferFunction(numerator, [1, 4, 8]), T=short)
        axes[2].plot(short, y, label=name)
    axes[2].set(xlabel="time [s]", ylabel="output", title="Same characteristic polynomial")
    axes[2].legend(fontsize=10)
    print("The notch plot is a filter illustration, not a validated flexible-plant control design.")
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo2_extensions", args)


if __name__ == "__main__":
    main()
