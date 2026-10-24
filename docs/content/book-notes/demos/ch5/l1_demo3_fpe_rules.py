"""FPE Section 5.2 examples: the Fig. 5.4 phase test at a trial point, and the Eq. (5.20) locus built rule by rule."""
import numpy as np
import kit as dk


def main():
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    # --- Left: Definition II at a trial point, FPE Eq. (5.18) and Fig. 5.4.
    zeros = np.array([-1.0])
    poles = np.array([0, -5, -2+2j, -2-2j])
    s0 = -1+2j
    ax = axes[0]
    dk.splane(ax, poles, zeros, xlim=(-6.5, 2.5), ylim=(-3.5, 3.5),
              title_text="Phase test at $s_0=-1+2j$ for $(s+1)/[s(s+5)((s+2)^2+4)]$")
    for label in list(ax.texts):
        label.remove()
    ax.plot([s0.real], [s0.imag], "s", color=dk.C["orange"], ms=8, zorder=6, label="trial point $s_0$")
    psi = [np.degrees(np.angle(s0-z)) for z in zeros]
    phi = [np.degrees(np.angle(s0-p)) for p in poles]
    for z, angle in zip(zeros, psi):
        ax.annotate("", xy=(s0.real, s0.imag), xytext=(z.real, z.imag),
                    arrowprops={"arrowstyle": "->", "color": dk.C["red"], "lw": 1.6}, zorder=5)
    for p, angle in zip(poles, phi):
        ax.annotate("", xy=(s0.real, s0.imag), xytext=(p.real, p.imag),
                    arrowprops={"arrowstyle": "->", "color": dk.C["blue"], "lw": 1.6}, zorder=5)
    ax.text(-0.9, 1.0, r"$\psi_1=90^\circ$", color=dk.C["red"], fontsize=10)
    ax.text(0.12, 0.85, r"$\phi_1=116.6^\circ$", color=dk.C["blue"], fontsize=10)
    ax.text(-1.95, 2.15, r"$\phi_3=0^\circ$", color=dk.C["blue"], fontsize=10)
    ax.text(-2.1, -0.9, r"$\phi_4=76.0^\circ$", color=dk.C["blue"], fontsize=10)
    ax.text(-4.0, 1.05, r"$\phi_2=26.6^\circ$", color=dk.C["blue"], fontsize=10)
    total = sum(psi)-sum(phi)
    ax.text(0.03, 0.04, rf"$\sum\psi_i-\sum\phi_i={total:.1f}^\circ\neq180^\circ$: not on the locus",
            transform=ax.transAxes, fontsize=10.5, color=dk.C["grey"])
    ax.set_aspect("equal", adjustable="box")
    ax.legend(fontsize=10, loc="upper left")

    # --- Right: FPE Eq. (5.20), L = 1/(s[(s+4)^2+16]), Figs. 5.6-5.9.
    num, den = [1], [1, 8, 32, 0]
    ax = axes[1]
    dk.locus(ax, num, den, np.r_[np.linspace(0, 64, 2000), np.linspace(64, 1200, 2500)],
             xlim=(-10, 4), ylim=(-7, 7), title_text="FPE Eq. (5.20): $1/(s[(s+4)^2+16])$")
    dk.gain_arrows(ax, num, den, 30, 45)
    alpha = -8/3
    for angle in [60, 180, 300]:
        r = np.linspace(0, 12, 100)
        ax.plot(alpha+r*np.cos(np.deg2rad(angle)), r*np.sin(np.deg2rad(angle)),
                "--", color=dk.C["grey"], lw=1)
    # Rule 4: departure from -4+4j at -45 degrees.
    dep = np.deg2rad(-45)
    ax.arrow(-4, 4, 1.2*np.cos(dep), 1.2*np.sin(dep), width=.03, color=dk.C["orange"], zorder=6)
    ax.text(-3.6, 4.3, r"$\phi_{dep}=-45^\circ$", fontsize=10, color=dk.C["orange"])
    # Section 5.2.3: zeta = 0.5 ray, gain K = 64 puts roots at -2 +/- 2 sqrt(3) j and -4.
    r = np.linspace(0, 9, 50)
    for sign in (1, -1):
        ax.plot(-r/2, sign*r*np.sqrt(3)/2, ":", color=dk.C["orange"], lw=1.2)
    roots64 = np.roots([1, 8, 32, 64])
    ax.plot(roots64.real, roots64.imag, "s", color=dk.C["red"], ms=7, zorder=6,
            label=r"$K=64$: $\zeta=0.5$ pair and third root $-4$")
    ax.plot([0, 0], [np.sqrt(32), -np.sqrt(32)], "o", color=dk.C["orange"], label=r"crossing: $K=256$")
    ax.legend(fontsize=9.5, loc="lower left")

    print("Trial point s0=-1+2j for (s+1)/[s(s+5)((s+2)^2+4)]:")
    print(f"  psi_1={psi[0]:.1f}; phi_1..4 from 0, -5, -2+2j, -2-2j = "
          + ", ".join(f"{x:.1f}" for x in phi) + f"; total={total:.1f} deg (FPE prints -129.2 from rounded angles)")
    print("FPE Eq. (5.20): poles 0, -4+/-4j; n-m=3.")
    print(f"  Rule 3: asymptotes 60, 180, 300 deg from alpha={alpha:.4f}; they cross jw at +/-{-alpha*np.tan(np.pi/3):.3f}j")
    print("  Rule 4: departure from -4+4j = -90 - 135 - 180 = -405 = -45 deg")
    print("  Section 5.2.3: zeta=0.5 ray meets the locus at s0=-2+2*sqrt(3)j; exact K=|s0||s0-s2||s0-s3|=64 (graphical estimate 65)")
    print("  roots at K=64:", ", ".join(dk.fmt_root(x) for x in roots64), "; Kv=K/32=2")
    print(f"  Routh crossing: K=256 at w=sqrt(32)={np.sqrt(32):.4f} rad/s")
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo3_fpe_rules", args)


if __name__ == "__main__":
    main()
