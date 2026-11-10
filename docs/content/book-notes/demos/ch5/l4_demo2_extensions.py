"""Lag and PI design extensions: Franklin lead-lag, notch detuning, rate feedback, and FPE's notch on the flexible plant."""
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
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    axes = axes.ravel()
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
    # FPE Section 5.4.3, Eqs. (5.74)-(5.76): the lead-lag design on the flexible plant, with and without the notch.
    # Loop numerator and denominator: plant 2500/[s(s+1)(s^2+s+2500)] times 91(s+2)(s+0.05)/[(s+13)(s+0.01)].
    loop_num = 2500*91*np.polymul([1, 2], [1, .05])
    loop_den = np.polymul(np.polymul([1, 1, 0], [1, 1, 2500]), np.polymul([1, 13], [1, .01]))
    notch_num, notch_den = [1, .8, 3600], np.polymul([1, 60], [1, 60])
    fpe = {"lead-lag on flexible plant": dk.closed_loop(loop_num, loop_den),
           "with notch (5.76)": dk.closed_loop(np.polymul(loop_num, notch_num), np.polymul(loop_den, notch_den))}
    tf = np.linspace(0, 8, 160001)
    fpe_traces = dk.response_table(fpe, tf)
    for name, y in fpe_traces.items():
        axes[3].plot(tf, y, label=name)
    axes[3].set(xlim=(0, 2), xlabel="time [s]", ylabel="output", title="FPE §5.4.3: 50 rad/s flexible mode")
    axes[3].legend(fontsize=10)
    print("The 10 rad/s notch plot is a filter illustration; the fourth panel is FPE's own Eq. (5.74)-(5.76) design.")
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo2_extensions", args)


if __name__ == "__main__":
    main()
