"""
Demo 1  --  The s-plane picture                                  (lecture §10)

Every location in the complex plane corresponds to one shape of motion.  This
script draws the board from §10: a set of pole locations on the left, and the
time response e^{st} each one produces on the right, colour-matched.

Run:  uv run python demo1_splane_modes.py
"""

import numpy as np

import demokit as dk

# Each entry: (s value, label, colour, lecture example, label offset in points)
MODES = [
    (-2.5 + 0j,   "s = -2.5",      dk.C["blue"],   "thermal body, small RC (§5)",            (8, 10)),
    (-0.35 + 0j,  "s = -0.35",     dk.C["sky"],    "thermal body, large RC (§5)",            (10, -20)),
    (-0.6 + 8.0j, "s = -0.6 + 8j", dk.C["green"],  "underdamped spring-mass-damper (§7.4)", (-135, 4)),
    (0.0 + 5.0j,  "s = 5j",        dk.C["orange"], "undamped spring-mass, c = 0 (§7.3)",     (12, 6)),
    (0.30 + 8.0j, "s = 0.30 + 8j", dk.C["purple"], "unstable flutter / too much loop gain",  (14, 4)),
    (0.50 + 0j,   "s = +0.50",     dk.C["red"],    "upright pendulum (§9.2)",                (8, 10)),
]


def response(s: complex, t: np.ndarray) -> np.ndarray:
    """Real motion produced by the mode e^{st}.

    A real pole gives e^{st} directly.  A complex pole never appears alone: it
    arrives with its conjugate, and the physical motion is the sum of the pair,
    2*Re{e^{st}} = 2 e^{sigma t} cos(omega t).  This is the §7.5 point.
    """
    if abs(s.imag) < 1e-12:
        return np.exp(s.real * t)
    return 2.0 * np.real(np.exp(s * t))


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("Demo 1 -- the s-plane: where a pole sits decides how the system moves")
    dk.note(
        "s = sigma + j*omega carries two independent pieces of information. The real "
        "part sigma sets the envelope e^{sigma t} -- growth or decay. The imaginary "
        "part omega sets the ringing. Read the table below, then look at the figure: "
        "the left panel is where each pole sits, the right panel is what it does.")

    rows = []
    for s, label, _, origin, _off in MODES:
        sigma, omega = s.real, s.imag
        envelope = "decays" if sigma < -1e-12 else ("grows" if sigma > 1e-12 else "constant")
        ringing = "yes" if abs(omega) > 1e-12 else "no"
        tau = f"{1/abs(sigma):.2f} s" if abs(sigma) > 1e-12 else "--"
        rows.append([label, f"{sigma:+.2f}", f"{omega:.2f}", envelope, ringing, tau, origin])

    dk.section("pole location -> motion")
    dk.table(["pole", "sigma", "omega", "envelope", "rings?", "|1/sigma|", "lecture example"], rows)

    dk.note(
        "The particular rates above are chosen so that every trace is legible on one "
        "common 4-second window; what matters is the shape, not the numbers. "
        "Note the two thermal rows. Same shape of motion, different speed: moving the "
        "pole from -5 to -0.5 multiplies the time constant by ten. 'Faster' literally "
        "means 'further left'. And the only row that grows is the only row in the "
        "right half plane.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.2),
                                   gridspec_kw={"width_ratios": [1, 1.25]})

    dk.splane(axL, poles=[], xlim=(-6.2, 3.6), ylim=(-10.5, 10.5),
              title_text="Where the pole sits")

    for s, label, color, _, off in MODES:
        conj = [s] if abs(s.imag) < 1e-12 else [s, np.conj(s)]
        axL.plot([z.real for z in conj], [z.imag for z in conj], "x",
                 ms=14, mew=3.2, color=color, zorder=3)
        axL.annotate(label, (s.real, s.imag), textcoords="offset points",
                     xytext=off, fontsize=10.5, color=color, weight="bold")

    # Each mode is normalised by its own peak over the window, so every curve
    # fits its lane.  A decaying mode therefore starts at full height and
    # shrinks; a growing mode starts small and fills the lane by the end.
    t = np.linspace(0, 4, 2000)
    LANE = 2.4
    for k, (s, label, color, _, _off) in enumerate(MODES):
        y = response(s, t)
        y = y / np.max(np.abs(y))
        axR.axhline(LANE * k, color=color, lw=0.7, alpha=0.35)
        axR.plot(t, y + LANE * k, color=color, label=label)

    axR.set_yticks([LANE * k for k in range(len(MODES))])
    axR.set_yticklabels([m[1] for m in MODES], fontsize=10.5)
    axR.set_xlabel("time  [s]")
    axR.set_title("What it does  (each curve scaled to its own lane)")
    axR.set_ylim(-1.6, LANE * (len(MODES) - 1) + 1.6)
    axR.grid(axis="x", alpha=0.25)
    axR.grid(axis="y", visible=False)

    fig.suptitle("The s-plane: one picture behind every stability statement in the course",
                 fontsize=15, y=0.99)
    fig.tight_layout()
    dk.finish(plt, fig, "demo1_splane_modes", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
