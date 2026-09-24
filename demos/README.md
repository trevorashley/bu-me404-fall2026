# Lecture demonstrations

Runnable Python for *From Physical Models to the Laplace Transform*. Each script
prints an annotated narrative to the terminal and writes a figure to `figures/`.
The numbers are the lecture's numbers, computed rather than quoted — several
demos exist specifically to settle claims students are right to be sceptical of.

## Setup

The environment is already built (`.venv`, Python 3.13, numpy/scipy/matplotlib/control).
To rebuild it from scratch:

```bash
uv venv --python 3.13
uv pip install -e .
```

## Running

```bash
uv run python demo1_splane_modes.py       # or: .venv/bin/python demo1_splane_modes.py
uv run python run_all.py                  # regenerate every figure (~20 s total)
```

Two flags on every demo:

| flag | effect |
|---|---|
| `--show` | open an interactive window instead of writing files (good for live use) |
| `--no-save` | print the terminal narrative only |

## The demos

| # | Script | Section | What it shows |
|---|---|---|---|
| 1 | `demo1_splane_modes.py` | §10 | The s-plane board: six pole locations beside the motion each one produces. |
| 2 | `demo2_damping_pole_locus.py` | §7.4 | Damping moves the poles **around a circle of radius ωₙ**, not leftward along a line. |
| 3 | `demo3_real_from_complex.py` | §7.5 | Where the *j* goes. Two complex modes, three independent routes, one real motion. |
| 4 | `demo4_sensor_moves_zeros.py` | §13, §16 | Same plant, two sensors: identical poles to 0.00e+00, completely different zeros. |
| 5 | `demo5_zero_dynamics.py` | §14 | Holding y ≡ 0 while the system keeps moving — and the input it costs. |
| 6 | `demo6_antiresonance.py` | §15 | Drive the mass at √(k₂/m₂) and it does not move. |
| 7 | `demo7_damping_moves_zeros.py` | §27, §33 | Damping moves zeros a *long* way, but can never push one across the axis. |
| 8 | `demo8_quadrotor_rhp.py` | §29, §30 | Inverse response, and the unstable zero dynamics θ̈ = (g/h)θ behind it. |

`twomass.py` holds the shared §11 two-mass model (demos 4–6); `demokit.py` holds
plotting and narration helpers.

## Suggested use in lecture

Three of these earn their keep as live demos:

- **Demo 5** is the strongest. The sensor reads `3e-17` for a full minute while the
  second mass swings through a displacement of 1 and the actuator works at amplitude 8.
  It makes "zero output ≠ zero motion" impossible to disbelieve.
- **Demo 2** pre-empts the wrong intuition about damping before students form it.
- **Demo 8** shows a right-half-plane zero as a *visible unstable motion* rather than
  an algebraic sign condition.

Demos 4, 6 and 7 work well as figures on a slide; demos 1 and 3 are worth running
only if the corresponding board is going badly.

## Verification built into the scripts

Rather than assert the lecture's numbers, each script recomputes them:

- Demo 2 confirms |s| = ωₙ to 1.8e-15 across the whole underdamped range.
- Demo 3 gets A₁ = 1 − j/3 and reproduces Problem 6's closed form, cross-checked
  against a numerical ODE solve (agreement 4.7e-12).
- Demo 4 finds the two pole sets identical to 0.00e+00.
- Demo 5 measures the hidden motion's frequency as 3.99997 rad/s against the zero
  at 3.99995 rad/s.
- Demo 7 reproduces both §27 damping tables exactly, and shows the product of the
  zeros pinned at −100 across a 500-point sweep.
- Demo 8 matches the analytic step response `(g t⁴/24 − h t²/2)/J` to 1e-12, and
  gets √(g/h) = 7.00357 from three independent routes.
