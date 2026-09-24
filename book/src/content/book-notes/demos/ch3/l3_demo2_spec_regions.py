"""
L3 Demo 2  --  Turning specifications into a region of the s-plane
                                                            (Example 3.27)

The requirement is t_r <= 0.6 s, M_p <= 10%, t_s <= 3 s. Section 3.4 converts
each one into a constraint on where a second-order pole pair may sit:

    omega_n >= 1.8/0.6 = 3 rad/s        a circle
    zeta    >= 0.6      (M_p <= 10%)    a wedge
    sigma   >= 4.6/3    = 1.53 1/s      a vertical line

This script draws the region and then tests it: pole pairs are sampled inside
and just outside, their step responses are simulated, and the specifications
are measured. The region is a guide, and the test says how good a guide.

Run:  uv run python ch3/l3_demo2_spec_regions.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

TR_MAX, MP_MAX, TS_MAX = 0.6, 0.10, 3.0
WN_MIN = 1.8 / TR_MAX
ZETA_MIN = float(np.sqrt(np.log(MP_MAX)**2 / (np.pi**2 + np.log(MP_MAX)**2)))
SIGMA_MIN = 4.6 / TS_MAX


def measure(zeta, wn):
    t = np.linspace(0, max(8.0, 20.0 / (zeta * wn)), 60000)
    _, y = step(lti([wn**2], [1.0, 2 * zeta * wn, wn**2]), T=t)
    tr = t[np.argmax(y >= 0.9)] - t[np.argmax(y >= 0.1)]
    mp = max(0.0, y.max() - 1.0)
    outside = np.where(np.abs(y - 1.0) > 0.01)[0]
    ts = t[outside[-1] + 1] if len(outside) and outside[-1] + 1 < len(t) else (np.inf if len(outside) else 0.0)
    return tr, mp, ts


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 2 -- specifications become a region, and the region is tested")

    dk.table(["specification", "requirement", "becomes", "value"],
             [["rise time", f"t_r <= {TR_MAX} s", "omega_n >= 1.8/t_r",
               f"{WN_MIN:.2f} rad/s"],
              ["overshoot", f"M_p <= {100*MP_MAX:.0f}%", "zeta >= zeta(M_p)",
               f"{ZETA_MIN:.3f}"],
              ["settling", f"t_s <= {TS_MAX} s", "sigma >= 4.6/t_s",
               f"{SIGMA_MIN:.2f} 1/s"]])
    dk.note(
        "The damping bound is exact: invert M_p = exp(-pi zeta / sqrt(1 - zeta^2)) at "
        f"10% and you get zeta = {ZETA_MIN:.3f}, which the book reads off Fig. 3.24 as "
        "0.6. Note also that any pair meeting both the omega_n and zeta bounds already "
        f"has sigma = zeta*omega_n >= {ZETA_MIN*WN_MIN:.2f}, comfortably past "
        f"{SIGMA_MIN:.2f}: the settling requirement is not the binding one here.")

    dk.section("sampled pole pairs, specifications measured from the response")
    trials = [("inside, comfortably", 0.70, 5.0),
              ("inside, on the omega_n circle", 0.70, 3.0),
              ("inside, on the zeta wedge", ZETA_MIN, 4.0),
              ("outside: too little damping", 0.45, 5.0),
              ("outside: too slow", 0.70, 2.0)]
    rows = []
    for label, z, wn in trials:
        tr, mp, ts = measure(z, wn)
        ok = (tr <= TR_MAX) and (mp <= MP_MAX + 1e-9) and (ts <= TS_MAX)
        rows.append([label, f"{z:.3f}", f"{wn:.2f}", f"{tr:.3f}",
                     f"{100*mp:.1f}%", f"{ts:.2f}", "yes" if ok else "NO"])
    dk.table(["pole pair", "zeta", "omega_n", "t_r [s]", "M_p", "t_s [s]",
              "meets spec?"], rows)

    dk.note(
        "The boundary rows are the interesting ones, and one of them fails. A pair "
        "sitting exactly on the omega_n = 3 circle at zeta = 0.7 has a measured rise "
        "time of 0.71 s against a 0.6 s requirement, because omega_n t_r is 2.13 at "
        "that damping rather than the 1.8 the rule assumes. The overshoot bound, "
        "which came from an exact formula, is met to the digit. Region first, "
        "simulation second -- Section 3.4 says so, and this is what it means.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 6.2),
                                   gridspec_kw={"width_ratios": [1.05, 1]})

    lim = 7.0
    axL.axhline(0, color="k", lw=1.0)
    axL.axvline(0, color="k", lw=1.6)

    # allowed set: |s| >= wn_min, Re(s) <= -sigma_min, angle within the zeta wedge
    xs = np.linspace(-lim, 0.5, 900)
    ys = np.linspace(-lim, lim, 900)
    X, Y = np.meshgrid(xs, ys)
    R = np.hypot(X, Y)
    with np.errstate(invalid="ignore", divide="ignore"):
        Z = np.where(R > 0, -X / R, 0.0)          # zeta = -Re(s)/|s|
    allowed = (R >= WN_MIN) & (-X >= SIGMA_MIN) & (Z >= ZETA_MIN) & (X < 0)
    axL.contourf(X, Y, allowed.astype(float), levels=[0.5, 1.5],
                 colors=[dk.C["green"]], alpha=0.22)

    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 300)
    axL.plot(WN_MIN * np.cos(th), WN_MIN * np.sin(th), color=dk.C["blue"], lw=2.0,
             label=f"$\\omega_n = {WN_MIN:.0f}$ rad/s  (rise time)")
    axL.axvline(-SIGMA_MIN, color=dk.C["red"], lw=2.0,
                label=f"$\\sigma = {SIGMA_MIN:.2f}$ 1/s  (settling)")
    ang = np.arcsin(ZETA_MIN)
    for sgn in (1, -1):
        axL.plot([0, -2 * lim * np.sin(ang)], [0, sgn * 2 * lim * np.cos(ang)],
                 color=dk.C["orange"], lw=2.0,
                 label=(f"$\\zeta = {ZETA_MIN:.2f}$  (overshoot)" if sgn == 1 else None))

    for label, z, wn in trials:
        p = wn * (-z + 1j * np.sqrt(1 - z**2))
        tr, mp, ts = measure(z, wn)
        ok = (tr <= TR_MAX) and (mp <= MP_MAX + 1e-9) and (ts <= TS_MAX)
        axL.plot([p.real, p.real], [p.imag, -p.imag], "x", ms=12, mew=3,
                 color=dk.C["green"] if ok else dk.C["red"])

    axL.set_xlim(-lim, 1.0)
    axL.set_ylim(-lim, lim)
    axL.set_xlabel(r"$\Re(s)$")
    axL.set_ylabel(r"$\Im(s)$")
    axL.set_title("Fig. 3.26: the shaded wedge is where the poles may sit")
    axL.legend(fontsize=9.5, loc="lower left")

    t = np.linspace(0, 4, 4000)
    for label, z, wn in trials:
        _, y = step(lti([wn**2], [1.0, 2 * z * wn, wn**2]), T=t)
        tr, mp, ts = measure(z, wn)
        ok = (tr <= TR_MAX) and (mp <= MP_MAX + 1e-9) and (ts <= TS_MAX)
        axR.plot(t, y, lw=2.0, color=dk.C["green"] if ok else dk.C["red"],
                 alpha=0.9 if ok else 0.75,
                 label=f"{label} ({'meets' if ok else 'fails'})")
    axR.axhline(1.10, ls="--", color=dk.C["grey"], lw=1.2)
    axR.text(2.6, 1.115, "10% overshoot limit", fontsize=10, color=dk.C["grey"])
    axR.set_xlabel("time [s]")
    axR.set_ylabel("step response")
    axR.set_title("The same five pole pairs, simulated")
    axR.legend(fontsize=9, loc="lower right")

    fig.suptitle("Example 3.27: specifications drawn in the s-plane, then verified",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo2_spec_regions", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
