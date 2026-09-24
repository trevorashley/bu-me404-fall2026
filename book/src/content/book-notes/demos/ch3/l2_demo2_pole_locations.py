"""
L2 Demo 2  --  Fig. 3.16, recomputed                              (FPE §3.3)

Fig. 3.16 is the picture the book asks you to commit to memory: where a pole
sits in the s-plane and what motion that produces. Here every one of those
little waveforms is computed from its pole rather than drawn by hand, and the
first-order time-constant percentages of Fig. 3.14(b) are computed too.

Run:  uv run python ch3/l2_demo2_pole_locations.py
"""

import numpy as np

import kit as dk

# (pole, label) -- a conjugate pair is entered by its upper member.
CASES = [
    (-3.0 + 0.0j,  "fast real"),
    (-0.6 + 0.0j,  "slow real"),
    (-1.0 + 3.0j,  "decaying oscillation"),
    (0.0 + 3.0j,   "sustained oscillation"),
    (0.6 + 3.0j,   "growing oscillation"),
    (0.6 + 0.0j,   "pure growth"),
    (0.0 + 0.0j,   "integrator"),
]


def mode(t, p):
    """Real natural motion belonging to a pole (a conjugate pair if complex)."""
    if abs(p.imag) < 1e-12:
        return np.exp(p.real * t)
    return np.exp(p.real * t) * np.cos(p.imag * t)


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L2 Demo 2 -- pole location decides the shape of the natural response")

    dk.section("what each pole does")
    rows = []
    for p, label in CASES:
        real_part = p.real
        if real_part < 0:
            fate = f"decays, tau = {1/abs(real_part):.2f} s"
        elif real_part > 0:
            fate = f"grows, doubles every {np.log(2)/real_part:.2f} s"
        else:
            fate = "neither decays nor grows"
        rows.append([dk.fmt_root(p, 2), label,
                     f"{real_part:+.2f}", f"{abs(p.imag):.2f}", fate])
    dk.table(["pole", "name", "Re(p) [1/s]", "omega_d [rad/s]", "behaviour"], rows)

    dk.note(
        "For these simple modes, the real part decides decay or growth; the imaginary part decides "
        "whether the motion rings. 'Fast' and 'slow' are statements about distance "
        "from the imaginary axis, not about frequency -- the pole at -3 and the pole "
        "at -0.6 both produce pure exponentials, one five times quicker.")

    dk.section("Fig. 3.14(b): the first-order percentages, computed")
    dk.table(["t / tau", "1 - e^{-t/tau}"],
             [[f"{n}", f"{100*(1 - np.exp(-n)):.1f}%"] for n in range(1, 6)])
    print("\n  the 63% at one time constant and 'settled by five' both come "
          "from this column")

    # -------------------------------------------------- decay-rate comparison
    dk.section("how much faster is 'farther left'?")
    t_check = 1.0
    rows = []
    for real_part in [-0.6, -1.0, -2.0, -3.0]:
        rows.append([f"{real_part:+.1f}", f"{np.exp(real_part*t_check):.4f}",
                     f"{4.6/abs(real_part):.2f}"])
    dk.table(["pole", "e^{Re(p) t} at t = 1 s", "4.6/|Re(p)| [s]"], rows)

    # ------------------------------------------------------------------ figure
    # Laid out like Fig. 3.16: columns are LHP / jw axis / RHP, the top row is a
    # complex pair and the bottom row a real pole. Every curve is computed.
    t = np.linspace(0, 6, 1200)
    panels = [
        [(-1.0 + 3.0j, "decaying oscillation"), (0.0 + 3.0j, "sustained oscillation"),
         (0.6 + 3.0j, "growing oscillation")],
        [(-3.0 + 0.0j, "fast decay"), (0.0 + 0.0j, "constant (integrator)"),
         (0.6 + 0.0j, "pure growth")],
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13.6, 7.0), sharex=True)
    # each panel keeps its own vertical scale: a growing mode would otherwise
    # flatten every stable trace into a line
    col_titles = ["LHP:  $\\Re(s) < 0$", "$j\\omega$ axis:  $\\Re(s) = 0$",
                  "RHP:  $\\Re(s) > 0$"]

    for r, row in enumerate(panels):
        for c, (p_, label) in enumerate(row):
            ax = axes[r][c]
            colour = dk.C["blue"] if p_.real < 0 else (
                dk.C["grey"] if p_.real == 0 else dk.C["red"])
            ax.plot(t, mode(t, p_), color=colour, lw=2.2)
            if r == 1 and c == 0:      # show the slow pole beside the fast one
                ax.plot(t, mode(t, -0.6 + 0j), color=dk.C["sky"], lw=2.0,
                        label="$s=-0.6$ (slow)")
                ax.plot([], [], color=dk.C["blue"], label="$s=-3$ (fast)")
                ax.legend(fontsize=9.5, loc="upper right")
            ax.axhline(0, color="k", lw=0.8)
            y = mode(t, p_)
            span = max(1.2, 1.15 * float(np.max(np.abs(y))))
            ax.set_ylim(-span, span)
            note = ""
            if p_.real > 0:
                note = f"   (reaches {np.max(np.abs(y)):.0f}$\\times$)"
            ax.set_title(f"{label}{note}\n$s = {dk.fmt_root(p_, 1)}$", fontsize=11)
            if r == 0:
                ax.text(0.5, 1.34, col_titles[c], transform=ax.transAxes,
                        ha="center", fontsize=13, color=dk.C["grey"])
            if r == 1:
                ax.set_xlabel("time [s]")
            if c == 0:
                ax.set_ylabel("natural response")

            # a thumbnail s-plane in the corner, so the pole and its motion sit together
            inset = ax.inset_axes([0.03, 0.04, 0.20, 0.30])
            inset.axhline(0, color="k", lw=0.6)
            inset.axvline(0, color="k", lw=1.1)
            pts = [p_] if abs(p_.imag) < 1e-12 else [p_, np.conj(p_)]
            inset.plot([z.real for z in pts], [z.imag for z in pts], "x",
                       ms=7, mew=2.0, color=colour)
            inset.set_xlim(-4, 2)
            inset.set_ylim(-4.5, 4.5)
            inset.set_xticks([])
            inset.set_yticks([])
            inset.grid(False)

    fig.suptitle("Fig. 3.16 recomputed: pole location decides the shape of the motion",
                 fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    dk.finish(plt, fig, "l2_demo2_pole_locations", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
