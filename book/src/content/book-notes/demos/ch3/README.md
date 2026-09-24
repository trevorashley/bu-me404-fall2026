# Chapter 3 lecture demonstrations

Runnable Python for the four-lecture series on FPE 8th ed. Chapter 3
(`book/src/content/lectures/lecture_ch3_L1..L4`). Each script prints an annotated narrative to the
terminal and writes a figure to `figures/`. Lecture cues include rounded numerical
results and analytical checks. Floating-point discrepancies and sampled crossing
times can vary slightly with the numerical environment.

These reuse `../demokit.py` (written for the physical-models lecture), so the palette,
tables and `--show` / `--no-save` flags behave identically. Figures land in
`ch3/figures/` rather than `../figures/`.

## Running

```bash
cd demos
# Once, if a working scientific Python environment is not already available:
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python numpy scipy matplotlib

uv run python ch3/l1_demo1_convolution.py          # one demo
uv run python ch3/l1_demo1_convolution.py --show   # interactive window, for live use
uv run python ch3/run_all.py                       # regenerate every figure
```

## The demos

| Lecture | Script | Book section | What it shows |
|---|---|---|---|
| L1 | `l1_demo1_convolution.py` | §3.1.1 | Weighted impulses approximate the convolution integral at first order, checked against an independent ODE solve. At finite width this is not the exact finite-pulse response. **live** |
| L1 | `l1_demo2_frequency_response.py` | Ex. 3.6, 3.7 | Amplitude ratio and phase measured from a simulation match $H(j\omega)$ to five decimals; the switch-on transient is separate. **live** |
| L1 | `l1_demo3_partial_fractions_fvt.py` | Ex. 3.11–3.14 | Cover-up residues against `scipy.signal.residue`; the Final Value Theorem applied where it holds and where it does not. |
| L1 | `l1_demo4_satellite_pulse.py` | Ex. 3.21 | A double integrator drifts forever after one thruster pulse and holds after a counter-pulse. |
| L2 | `l2_demo1_block_reduction.py` | Ex. 3.22–3.24 | The reduced transfer function of Fig. 3.12 agrees with the diagram solved as a linear system at 2000 random points in the $s$-plane. **live** |
| L2 | `l2_demo2_pole_locations.py` | §3.3, Fig. 3.16 | Fig. 3.16 recomputed: pole location beside the motion it produces, plus the first-order time-constant percentages. **live** |
| L2 | `l2_demo3_second_order.py` | Ex. 3.25, 3.26 | Closed-form impulse responses checked against numerical ones; $\zeta$, $\omega_n$, $\sigma$, $\omega_d$ from the coefficients; the overshoot family. |
| L3 | `l3_demo1_step_specs.py` | §3.4 | Exact peak formulas, the rise-time fit, and the approximate settling rule compared with the full envelope bound. |
| L3 | `l3_demo2_spec_regions.py` | Ex. 3.27 | The specification region, and a pole pair sitting on its boundary that fails the specification. **live** |
| L3 | `l3_demo3_zeros.py` | §3.5, Ex. 3.28 | The identity $y=y_0+\dot y_0/(\alpha\zeta)$; overshoot versus zero location; the exact cancellations of Example 3.28. |
| L3 | `l3_demo4_extra_pole_aircraft.py` | Eq. 3.82, Ex. 3.30 | Extra-pole rise times matching Fig. 3.38; the Boeing 747's undershoot and its final value. **live** |
| L4 | `l4_demo1_routh.py` | Ex. 3.32 | The Routh array built from coefficients; sign-change count checked against a root finder. **live** |
| L4 | `l4_demo2_gain_range.py` | Ex. 3.33 | The imaginary-axis crossing found by sweeping roots is $K=7.5000$, exactly Routh's symbolic answer. |
| L4 | `l4_demo3_pi_region.py` | Ex. 3.34 | Routh's two inequalities against closed-loop roots at 40,401 gain pairs: zero disagreements. |
| L4 | `l4_demo4_bibo_internal.py` | §3.6.1–3.6.2 | Bounded input with unbounded output, and a stable transfer function hiding an internally unstable system. **live** |

## Source corrections and qualifications

These are identified in the lecture notes and can be checked from the models.

1. **Example 3.32's root footnote.** The book prints $+0.7797\pm0.7488j$; the
   roots are $+0.6797\pm0.7488j$. The coefficient of $s^5$ is 4, so the six
   roots must sum to $-4$, which settles it. The conclusion — two right
   half-plane roots — is unaffected. (`l4_demo1_routh.py`)
2. **"A zero in the RHP will depress the overshoot."** True against a left
   half-plane zero at the same distance (20.9% versus 29.8% at $|\alpha|=2$),
   false against the zero-free system (16.3%). In this standard family the
   RHP zero produces an initial inverse response. (`l3_demo3_zeros.py`)
3. **Example 3.34, $K=10$, $K_I=5$.** Roots of $s^3+3s^2+12s+5$ are
   approximately $-0.462,-1.269\pm3.036j$, rather than the book's imaginary
   part near 3.3. (`l4_demo3_pi_region.py`)
4. **Settling time.** $4.6/\sigma$ is an estimate, not a guaranteed 1% bound.
   For the standard underdamped pair the full envelope bound is
   $-\ln(0.01\sqrt{1-\zeta^2})/\sigma$. (`l3_demo1_step_specs.py`)

The PI grid checks the full cubic with the integrator state retained. At
$K_I=0$, distinguish that neutral state from a controller implemented as a
pure proportional gain. Routh zero rows are marked as special cases rather
than counted as ordinary positive-column tests.
