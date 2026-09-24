"""
Demo 7  --  Damping moves zeros. It just cannot move them across the axis.
                                                          (lecture §27 and §33)

A rigid platform on soft mounts, actuator at offset +a, sensor at offset -b:

    m x'' + cx x' + kx x = u          J th'' + cth th' + kth th = a u
    y = x - b*th

The numerator is  A s^2 + B s + C  with
    A = J - ab*m,   B = cth - ab*cx,   C = kth - ab*kx.

A real RHP zero exists exactly when A*C < 0 -- a condition with no damping in
it. But B is full of damping, so the ZERO LOCATIONS move a great deal. The
slogan "damping moves poles, not zeros" is false.

Run:  uv run python demo7_damping_moves_zeros.py
"""

import numpy as np

import demokit as dk

M, J, KX, KTH = 1.0, 0.1, 100.0, 20.0
A_OFF, B_OFF = 0.3, 0.5
AB = A_OFF * B_OFF


def numerator(ab, cx, cth):
    return np.array([J - ab * M, cth - ab * cx, KTH - ab * KX])


def denominator(cx, cth):
    return np.polymul([M, cx, KX], [J, cth, KTH])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("Demo 7 -- geometry decides whether there is a RHP zero; damping decides where")
    dk.note(
        f"m={M:g}, J={J:g}, kx={KX:g}, k_theta={KTH:g}, a={A_OFF:g}, b={B_OFF:g}, "
        f"so ab={AB:g}. The existence test asks whether ab lies between J/m={J/M:g} "
        f"and k_theta/kx={KTH/KX:g}.  {J/M:g} < {AB:g} < {KTH/KX:g} is "
        f"{J/M < AB < KTH/KX}, so we expect one zero in the right half plane.")

    dk.section("the plant is asymptotically stable regardless (worked case: cx=2, cth=0.5)")
    poles = np.roots(denominator(2.0, 0.5))
    for z in np.sort_complex(poles):
        print(f"    pole  {dk.fmt_root(z)}")
    print(f"  all strictly stable: {np.all(poles.real < 0)}")
    zc = np.roots(numerator(AB, 2.0, 0.5))
    print(f"\n  zeros: {dk.fmt_root(np.sort_complex(zc)[1])} and "
          f"{dk.fmt_root(np.sort_complex(zc)[0])}   <- a stable plant with a RHP zero")

    # ------------------------------------------------ damping sweeps
    dk.section("sweeping the damping: the zeros move a long way")
    fams = [("c_theta = cx/10   (B < 0)", lambda c: c / 10.0, dk.C["blue"]),
            ("c_theta = cx/4    (B > 0)", lambda c: c / 4.0, dk.C["green"])]
    for name, rule, _ in fams:
        rows = []
        for cx in [0.0, 2.0, 6.0, 20.0, 60.0]:
            cth = rule(cx)
            zz = np.sort(np.roots(numerator(AB, cx, cth)).real)
            rows.append([f"{cx:.1f}", f"{cth:.2f}", f"{zz[1]:+.3f}", f"{zz[0]:+.3f}"])
        print(f"\n  {name}")
        dk.table(["cx", "c_theta", "RHP zero", "LHP zero"], rows, indent="    ")

    dk.note(
        "In the first family the RHP zero drifts toward the origin; in the second it "
        "races outward. Same geometry, same inertia, same stiffness -- only the "
        "damping distribution differs. Note which direction is bad: a zero drifting "
        "toward the origin tightens the bandwidth limit of §34, so damping can make "
        "the control problem worse while leaving every pole better damped.")

    dk.section("what damping can never do")
    prod = []
    for cx in np.linspace(0, 200, 500):
        for rule in (lambda c: c / 10.0, lambda c: c / 4.0):
            A, _, C = numerator(AB, cx, rule(cx))
            prod.append(C / A)
    print(f"  product of the zeros C/A over the whole sweep: "
          f"min {min(prod):.4f}, max {max(prod):.4f}")
    print("  It is constant and negative -- B never enters it. One zero must stay")
    print("  positive and one negative, no matter how the system is damped.")

    dk.section("sensor and actuator on the same side (ab < 0)")
    for cx, cth in [(0.0, 0.0), (2.0, 0.5)]:
        zz = np.roots(numerator(-AB, cx, cth))
        where = "on the jw axis" if np.max(np.abs(zz.real)) < 1e-12 else "in the LHP"
        print(f"    cx={cx:g}, c_theta={cth:g}:  "
              f"{'  '.join(dk.fmt_root(z, 3) for z in zz)}   -> {where}")
    dk.note(
        "Undamped they sit on the axis; damped they move into the left half plane. "
        "Both are minimum phase. Note that 'same side' is weaker than collocated: "
        "true collocation is the special case b = -a.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.2))

    dk.splane(axL, poles=[], xlim=(-50, 50), ylim=(-18, 18),
              title_text="Zero locus as the damping is increased")
    cxs = np.linspace(0, 60, 400)
    for name, rule, col in fams:
        zs = np.array([np.sort(np.roots(numerator(AB, c, rule(c))).real) for c in cxs])
        axL.plot(zs[:, 1], np.zeros_like(cxs), color=col, lw=3.5, label=name)
        axL.plot(zs[:, 0], np.zeros_like(cxs), color=col, lw=3.5)
        axL.plot(zs[-1, 1], 0, ">", ms=11, color=col, mec="k", mew=0.7)
        axL.plot(zs[-1, 0], 0, "<", ms=11, color=col, mec="k", mew=0.7)
    axL.plot([-10, 10], [0, 0], "o", ms=12, mfc="none", mew=2.6,
             color=dk.C["red"], label="undamped zeros  $\\pm10$")
    axL.legend(loc="upper left", fontsize=10)
    axL.text(25, -13, "the RHP zero never\ncrosses this line",
             ha="center", fontsize=11, color=dk.C["grey"])
    axL.annotate("", xy=(0, -9), xytext=(20, -11.5),
                 arrowprops=dict(arrowstyle="->", color=dk.C["grey"], lw=1.4))

    # right: step responses showing the inverse response survives damping
    from scipy import signal
    tt = np.linspace(0, 1.2, 3000)
    for cx, col, lab in [(0.0, dk.C["orange"], "undamped"),
                         (2.0, dk.C["blue"], r"$c_x=2$"),
                         (20.0, dk.C["green"], r"$c_x=20$")]:
        cth = cx / 4.0
        sysd = signal.lti(numerator(AB, cx, cth), denominator(cx, cth))
        _, yy = signal.step(sysd, T=tt)
        axR.plot(tt, yy / max(abs(yy)), color=col, label=lab)
    axR.axhline(0, color="k", lw=1.2)
    axR.set_xlabel("time  [s]")
    axR.set_ylabel("y(t), normalised")
    axR.set_title("Every one of them still starts by going the wrong way")
    axR.legend(fontsize=11)

    fig.suptitle("Damping relocates the zeros; only the geometry decides which side they are on",
                 fontsize=14.5, y=0.985)
    fig.tight_layout()
    dk.finish(plt, fig, "demo7_damping_moves_zeros", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
