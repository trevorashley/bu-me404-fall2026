# Chapter 4 lecture demonstrations

Runnable Python for the four-lecture series on FPE 8th ed. Chapter 4
(`feedback-properties_*`, `pid-control_*`, `system-type_*`, `pid-tuning_*`), plus the
anti-windup material of §9.3.1. Each script prints an annotated narrative to the
terminal and writes a figure to `figures/`. Lecture cues include rounded numerical
results and analytical checks.

These reuse `../ch2/demokit.py` through `kit.py`, so the palette, tables and
`--show` / `--no-save` flags behave identically. `heatx.py` is a shared
heat-exchanger model for L4 demos 1–2, not a demo itself. Figures land in
`ch4/figures/`.

## Running

```bash
cd demos
# Once, if a working scientific Python environment is not already available:
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python numpy scipy matplotlib

uv run python ch4/l2_demo1_proportional.py          # one demo
uv run python ch4/l2_demo1_proportional.py --show   # interactive window, for live use
uv run python ch4/run_all.py                        # regenerate every figure
```

## The demos

| Lecture | Script | Book section | What it shows |
|---|---|---|---|
| L1 | `l1_demo1_pendulum_stabilise.py` | §4.1.1, Eq. 4.17 | Open-loop cancellation of the pendulum's unstable pole diverges under a 0.001 input bias (11.0 at 10 s); feedback $7(s+1)/(s+3)$ places $-1\pm1.732j$ and holds the bias effect to 0.00075. |
| L1 | `l1_demo2_hidden_poles.py` | §4.1.2 exercise | The pole-placement answer $18(s^2+3s+9)/[s(s+9)]$ cancels the plant: $\mathcal T$ has no overshoot, $GS$ rings at the plant's $\zeta=0.5$, and $u(0^+)=18$ against a final value of 9. **live** |
| L1 | `l1_demo3_regulation_tradeoff.py` | §4.1.3 | $G=1/(s+1)$, $D=K$: from $K=1$ to 100 the bias error falls from 0.5 to 0.0099 while actuator noise grows from 0.10 to 4.44; simulation matches the $\lvert S\rvert$, $\lvert\mathcal T\rvert$, $\lvert DS\rvert$ predictions. |
| L1 | `l1_demo4_gain_sensitivity.py` | §4.1.4 | ±50% plant-gain error: ±50% open loop, −0.99%/+0.33% with $1+L=100$; the exact formula $\epsilon S/(1+\mathcal T\epsilon)$ matches simulation. **live** |
| L2 | `l2_demo1_proportional.py` | §4.3.1, Fig. 4.7 | Error falls as $1/(1+k_P)$ while the closed-loop poles slide vertically along $\Re s=-0.7$; settling time cannot improve with gain. **live** |
| L2 | `l2_demo2_integral.py` | §4.3.2, Figs. 4.8–4.9 | Zero error and exact disturbance cancellation on three different plants with one $k_I$; Routh limit $k_I<1.4$. **live** |
| L2 | `l2_demo3_derivative_placement.py` | §4.3.3, Fig. 4.10 | Coefficient matching gives $k_P=3,k_I=2,k_D=1.6$ (poles $-1,-1\pm j$); D on error vs on output: same poles, different zeros, an 83-unit kick with $\tau_f=0.02$ s. **live** |
| L2 | `l2_demo4_thermal_pi.py` | Ex. 4.5, Figs. 4.11–4.15 | Open loop 47.1 s; P offset 9.68 °C; PI settles in 13.44 s at ±10% $K_o$; the cancelled pole at −0.1 leaves a 10 s tail in the disturbance response. |
| L2 | `l2_demo5_motor_pid.py` | Ex. 4.6, Fig. 4.16 | Fig. 4.16 recomputed with closed-loop roots; integral action drops $\zeta$ from 0.25 to 0.08, derivative restores it to 0.58. |
| L3 | `l3_demo1_type_table.py` | §4.2.1, Table 4.1 | Type 0/1/2 loops driven by step, ramp and parabola; the nine simulated errors match the formula (diagonal 0.2000, 0.5000, 0.5000). **live** |
| L3 | `l3_demo2_pid_type.py` | §4.2.1, Eq. 4.58 plant | P and I control of $1/(s^2+1.4s+1)$ as the plant gain $A$ varies 4×: the I-control step error stays zero while every error constant moves; the I loop is stable only for $A<2.8$. |
| L3 | `l3_demo3_tachometer.py` | Ex. 4.3 | Tachometer raises $\zeta$ from 0.158 to 0.474 and $1/K_v$ from 0.1 to 0.3; a 2% position-sensor gain error makes the loop Type 0 (step error −0.0204). |
| L3 | `l3_demo4_disturbance_type.py` | Ex. 4.4 | DC motor with load torque: P is Type 1 to $R$ but Type 0 to $W$ ($e_{ss}=-0.25$); PI rejects a step torque and leaves −0.5 for a ramp torque. **live** |
| L3 | `l3_demo5_error_area.py` | §4.2, Truxal | $1/K_v$ three ways: $\lim sGD_c$, Truxal's pole–zero sum, step-error area; a Type 2 loop has zero net error area and so must overshoot (Prob. 4.28). |
| L4 | `l4_demo1_reaction_curve.py` | §4.3.6, Ex. 4.9 | Tangent construction on the heat-exchanger model ($R=1/85.9$, $L=10.6$ s vs the book's 1/90, 13 s); Z–N P/PI responses with decay ratios 0.20 and 0.27, at full and halved gains. **live** |
| L4 | `l4_demo2_ultimate_gain.py` | §4.3.6, Ex. 4.10 | $K_u=15.29$ (book 15.3), $P_u=43.6$ s (book 42 s); Table 4.3 responses; Routh gives $K_u=8$, $P_u=2\pi/\sqrt3$ for $1/(s+1)^3$. |
| L4 | `l4_demo3_antiwindup.py` | §9.3.1, Ex. 9.9 | Saturating PI loop stepped explicitly: overshoot 53% → 15% with $K_a=10$; saturation ends at 1.366 s → 0.525 s; $u_I$ peaks at exactly 2 at $t=1$; $K_a$ sweep. **live** |
| L4 | `l4_demo4_derivative_kick.py` | Fig. 4.10; AM 11.5 | Same closed-loop poles, three reference paths: kick 66 / 6 / 0, overshoot 18.9% / 31.9% / 2.9%, rise 0.47 / 0.61 / 1.32 s. **live** |
| L4 | `l4_demo5_feedforward.py` | §4.4, Ex. 4.11 | DC-gain feedforward gives zero steady error with unchanged poles ($M_p$ 21.2%, 42.2%); residual error when the model's DC gain is 20% off. |

## Source corrections and qualifications

These are identified in the lecture notes and can be checked from the models.

1. **Missing table bodies.** Tables 4.1, 4.2 and 4.3 (pp. 26, 61, 63) print only
   their captions in the supplied PDF; the notes rebuild them (Table 4.1 from
   Eq. 4.35, Z–N rows from the standard rules, confirmed by the book's arithmetic).
   Fig. 9.24 is likewise missing.
2. **§4.1.4 "loop gain of 100".** The example sets $1+GD_{cl}=100$, so the loop
   gain is 99. (`l1_demo4_gain_sensitivity.py`)
3. **§4.2.1, p. 24.** The Type 0 error grows for inputs of degree 1 or higher,
   not "higher than 1". (`l3_demo1_type_table.py`)
4. **Eq. (4.48).** The left side is $e_{ss}$, not $y_{ss}$. With $R=0$, $E=-Y$.
5. **Ex. 4.6, Eq. (4.79).** $k_I=15$ s and $k_D=0.3$ s cannot both be in seconds;
   the consistent times are $T_I=0.2$ ms and $T_D=0.1$ ms. (`l2_demo5_motor_pid.py`)
6. **Ex. 4.7.** Cites Fig. 4.4 for the motor, which is Fig. 4.6; the step-torque
   error is $-B/(Ak_Ph)$, not $-B/Ak_P$.
7. **Ex. 4.8, Eqs. (4.86), (4.88).** Missing leading minus signs: $-1/k_P$ and
   $-1/k_I$. (`l3_demo4_disturbance_type.py`)
8. **Ex. 4.9.** PI $k_P=0.9\cdot90/13=6.23$, not 6.22. The claim on p. 63 that the
   reaction-curve method "generally suggests higher gains" is contradicted by the
   book's own examples (6.92 vs 7.65 for P, 6.23 vs 6.885 for PI).
9. **Ex. 9.9.** $u_I$ peaks at 2.0 at exactly $t=1$ s, not 1.1 s; with antiwindup
   the error zero crossings are at 1.10 and 2.92 s. (`l4_demo3_antiwindup.py`)

Quarter decay equals 50% overshoot for the standard second-order pair
($\zeta=0.2155$); the book does not say so, and L4 uses it.
