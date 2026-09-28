# A First Analysis of Feedback IV — Tuning, Realising and Feeding Forward the PID

**Student lecture notes — FPE 8th ed., Sections 4.3.6, 4.4 and 9.3.1**

The PID formula fits on one line. A PID that works on a real machine needs four more decisions: the gains, where the derivative acts, what happens at the actuator's limit, and how much of the job the reference does on its own. These notes cover Ziegler–Nichols tuning, practical realisation of the derivative and setpoint, integrator antiwindup, and feedforward.

**Prerequisites:** [L1 Feedback properties](feedback-properties_student.md), [L2 PID control](pid-control_student.md), [L3 System type](system-type_student.md), and Routh's criterion from [Stability](stability_student.md).

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., §4.3.6, §4.4, §4.5 and §9.3.1. Example, figure and equation numbers follow the textbook. The filtered derivative and setpoint weighting follow Åström & Murray, *Feedback Systems*, 2nd ed., §§11.3–11.5. Numbered sections and § references refer to these notes unless labelled as textbook sections.

## Learning objectives

After studying this lecture, you should be able to:

1. Read the slope $R$ and lag $L$ from a process reaction curve and apply the Ziegler–Nichols step-response rules (Table 4.2).
2. Show that a quarter decay ratio corresponds to $\zeta\approx0.215$ and to 50% overshoot for the standard second-order pair.
3. Describe the ultimate-sensitivity experiment, apply the rules of Table 4.3, and compute $K_u$ and $P_u$ with Routh's criterion for a delay-free plant.
4. Explain why Ziegler–Nichols settings are a starting point rather than a design, and what "detuning" means.
5. Explain derivative kick, and compare the derivative on the error with the derivative on the measured output (Fig. 4.10). Show that both give the same closed-loop poles but different zeros.
6. Write the filtered derivative $k_Ds/(1+sT_f)$ and compute the kick it produces, $k_P(1+N)$.
7. Use setpoint weighting to separate the response to the reference from the response to disturbances.
8. Explain integrator windup, trace Example 9.9 by hand, and derive the first-order lag that the antiwindup loop produces during saturation (Fig. 9.21d).
9. Design DC-gain feedforward for tracking and for a measured disturbance (Example 4.11), and compute the residual error when the model's DC gain is wrong.

## Notation and assumptions

| Symbol | Meaning |
|---|---|
| $G(s)$, $D_c(s)$ | plant and controller (compensator) |
| $R,\ Y,\ E,\ U,\ W$ | reference, output, error $R-Y$, control, disturbance |
| $k_P,\ k_I,\ k_D$ | proportional, integral and derivative gains |
| $T_I,\ T_D$ | integral (reset) time and derivative time: $D_c=k_P\left(1+\frac{1}{T_Is}+T_Ds\right)$, so $k_I=k_P/T_I$, $k_D=k_PT_D$ |
| $R,\ L$ | slope and apparent lag of the process reaction curve (§2); context separates this $R$ from the reference |
| $K_u,\ P_u$ | ultimate gain and ultimate period |
| $T_f,\ N$ | derivative filter time constant, $T_f=T_D/N$ |
| $b$ | setpoint weight on the proportional term |
| $u_c,\ u,\ u_{\max}$ | controller demand, saturated actuator output, actuator limit |
| $K_a$ | antiwindup feedback gain |

Several examples use a heat exchanger. Chapter 4 gives only its measured curves. The simulations here use $G(s)=e^{-5s}/[(10s+1)(60s+1)]$, the model the textbook gives for the same exchanger in Example 7.42 and Problem 6.66. It reproduces the measured ultimate gain of 15.3 to three figures.

---

## 1. From a formula to a controller {#section-1}

In the 1940s, process plants such as refineries and paper mills ran thousands of PID controllers, each with three adjustment knobs, and almost none had a mathematical model. Ziegler and Nichols (1942) gave operators a recipe: run one experiment on the process, read two numbers from the recorded response, and look up the knob settings in a table. That recipe is the first topic here.

The rest of the lecture deals with what the formula $k_P+k_I/s+k_Ds$ leaves out. The derivative needs a filter, and it should not differentiate a step in the setpoint. The integrator must stop charging when the actuator saturates. And a known input can be handled by feedforward, leaving feedback to correct only what the model does not predict.

---

## 2. Tuning from a step test {#section-2}

### 2.1 The process reaction curve {#section-2-1}

![Fig. 4.18 — Process reaction curve](./book-figures/4-18.png)

*Fig. 4.18 (textbook):* the process reaction curve and the tangent construction.

Many process plants respond to a step with an S-shaped curve: a flat start, a steepest point, then a slow approach to a new level. Ziegler and Nichols approximated such curves by a first-order lag with a time delay:

$$
\frac{Y(s)}{U(s)}=\frac{Ae^{-st_d}}{\tau s+1}
\tag{4.91}
$$

Two numbers are read from the curve by drawing the tangent at the inflection (steepest) point: its **slope**, the reaction rate $R=A/\tau$ (for an input step of size $\Delta u$, divide the measured slope by $\Delta u$: $R=\text{max slope}/\Delta u$), and its **intercept with the time axis**, the apparent lag $L=t_d$. The model is not meant to be literally true. It reduces the curve to two numbers: how fast the plant responds and how long it takes to start.

The lag $L$ is an *effective* delay: the delay of the fitted model, not necessarily a real dead time. The heat exchanger below has a true delay of 5 s, but the tangent construction gives $L\approx10.6$ s, because the lags make the curve start slowly too. $L$ is a rough time scale for the loop, and $1/L$ a rough bandwidth scale, not a strict limit on its response. The slope $R$ measures the plant's effective gain on the time scale of the loop. A proportional gain $k_P$ changes the output at a rate proportional to $k_PR$, so the loop gain accumulated over one lag is proportional to $k_PRL$. Holding that product fixed fixes the character of the transient, which is why every gain in Table 4.2 is a constant divided by $RL$.

### 2.2 Table 4.2: the step-response rules {#section-2-2}

The controller is written in the process-control form

$$
D_c(s)=k_P\left(1+\frac{1}{T_Is}+T_Ds\right).
\tag{4.92}
$$

Ziegler–Nichols step-response tuning, for a decay ratio of 0.25 (textbook Table 4.2):

| Controller | $k_P$ | $T_I$ | $T_D$ |
|---|---|---|---|
| P | $\dfrac{1}{RL}$ | — | — |
| PI | $\dfrac{0.9}{RL}$ | $\dfrac{L}{0.3}$ | — |
| PID | $\dfrac{1.2}{RL}$ | $2L$ | $0.5L$ |

Adding integral action lowers $k_P$ (from 1 to 0.9), because the integrator adds phase lag and reduces the stability margin. Adding derivative action raises it (to 1.2), because the derivative adds phase lead and restores some of that margin.

### 2.3 Quarter decay is 50% overshoot {#section-2-3}

![Fig. 4.19 — Quarter decay ratio](./book-figures/4-19.png)

*Fig. 4.19 (textbook):* the transient decays to a quarter of its amplitude in one period.

The rules were chosen so that the closed-loop transient decays to one quarter in one period. For the standard underdamped pair the envelope is $e^{-\zeta\omega_nt}$ and the period is $2\pi/\omega_d$, so one period's decay is

$$
e^{-2\pi\zeta/\sqrt{1-\zeta^2}}=\tfrac14
\quad\Longrightarrow\quad
\frac{\zeta}{\sqrt{1-\zeta^2}}=\frac{\ln4}{2\pi}=0.2206
\quad\Longrightarrow\quad
\zeta=\frac{0.2206}{\sqrt{1+0.2206^2}}=0.2155 .
$$

The overshoot of the standard pair is $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$, whose exponent is exactly half the one above. Therefore

$$
\boxed{M_p=\sqrt{1/4}=\tfrac12}
$$

For the standard second-order step response, quarter decay means 50% overshoot. Ziegler and Nichols tuned for fast recovery from disturbances in process plants, where setpoints change rarely; for most mechanical systems this target is too aggressive, and the gains are then reduced ("detuned").

---

## 3. Example 4.9: the heat exchanger, from a step test {#section-3}

![Fig. 4.23 — A measured process reaction curve](./book-figures/4-23.png)

*Fig. 4.23 (textbook):* the measured reaction curve of the heat exchanger.

From the curve, the textbook reads $R\simeq1/90$ per second and $L\simeq13$ s. Table 4.2 gives

$$
\text{P: } k_P=\frac{1}{RL}=\frac{90}{13}=6.92,
\qquad
\text{PI: } k_P=\frac{0.9}{RL}=6.23,\quad T_I=\frac{L}{0.3}=43.3\ \text{s}.
$$

(The textbook prints 6.22 for the PI gain; $0.9\times90/13=6.2308$.)

![Fig. 4.24(a) — Closed-loop step responses, Z–N gains](./book-figures/4-24a.png)
![Fig. 4.24(b) — Closed-loop step responses, k_P halved](./book-figures/4-24b.png)

*Fig. 4.24 (textbook):* (a) closed-loop responses with the Ziegler–Nichols gains; (b) with $k_P$ halved.

- **P leaves an offset.** The plant is Type 0 with $G(0)=1$, so the final value is $k_P/(1+k_P)=6.92/7.92=0.874$ and the error is $1/(1+k_P)=0.126$.
- **PI removes the offset** (Type 1), with more overshoot.
- **Both oscillate**, as the quarter-decay target implies.
- **Halving $k_P$** nearly removes the oscillation, and the P offset grows: the final value is $3.46/4.46=0.776$.

**Worked check:** On the model, the tangent construction gives $R=1/85.9$ and $L=10.64$ s, against the $1/90$ and 13 s read by eye from the printed curve. The true delay is only 5 s: the rest of $L$ is the lag of the two thermal time constants, appearing as extra dead time. With the textbook's gains the simulated decay ratios are 0.20 (P) and 0.27 (PI), close to one quarter, and the peaks are 1.26 and 1.58. The model's own tangent would give $k_P=8.07$ for P. The rules are sensitive to how the line is drawn, which is another reason to treat them as a starting point.

![Tangent construction on the heat-exchanger reaction curve, and closed-loop responses with Ziegler–Nichols P and PI gains, full and halved](demos/ch4/figures/l4_demo1_reaction_curve.svg)

---

## 4. Tuning at the edge of stability {#section-4}

### 4.1 The ultimate-sensitivity experiment {#section-4-1}

![Fig. 4.20 — Determination of ultimate gain and period](./book-figures/4-20.png)
![Fig. 4.21 — Neutrally stable system](./book-figures/4-21.png)

*Figs. 4.20 and 4.21 (textbook):* raise a proportional gain until the loop just oscillates.

Turn off the integral and derivative terms and raise $k_P$ until the loop sustains an oscillation. The gain is the **ultimate gain** $K_u$ and the period is the **ultimate period** $P_u$. Measure $P_u$ at the smallest amplitude possible, so that the actuator does not saturate.

**When the experiment works.** It needs a finite positive gain at which a complex pair of closed-loop poles reaches the imaginary axis. Not every plant has one. L2's model $G=1/(s^2+1.4s+1)$ gives $s^2+1.4s+1+k_P$, which is stable for every $k_P>0$, so it has no $K_u$ or $P_u$ and Table 4.3 cannot be applied to it. Many process plants with delay or multiple lags do have the required phase crossing, which is why the method suits them. Counting lags alone is not a test; review question 9 explores why.

When it does work, use textbook Table 4.3:

| Controller | $k_P$ | $T_I$ | $T_D$ |
|---|---|---|---|
| P | $0.5K_u$ | — | — |
| PI | $0.45K_u$ | $\dfrac{P_u}{1.2}$ | — |
| PID | $0.6K_u$ | $\dfrac{P_u}{2}$ | $\dfrac{P_u}{8}$ |

The P rule, "use half the gain that makes the loop oscillate", is a **gain margin of 2**, a stability margin that Chapter 6 develops properly.

### 4.2 Example 4.10: the heat exchanger again {#section-4-2}

![Fig. 4.25 — Ultimate period of heat exchanger](./book-figures/4-25.png)

*Fig. 4.25 (textbook):* sustained oscillation at the ultimate gain.

The textbook measures $K_u=15.3$ and $P_u=42$ s, so

$$
\text{P: } k_P=0.5\times15.3=7.65,
\qquad
\text{PI: } k_P=0.45\times15.3=6.885,\quad T_I=\frac{42}{1.2}=35\ \text{s}.
$$

![Fig. 4.26(a) — Closed-loop step responses, Table 4.3 gains](./book-figures/4-26a.png)
![Fig. 4.26(b) — Closed-loop step responses, k_P reduced by 50%](./book-figures/4-26b.png)

*Fig. 4.26 (textbook):* (a) closed-loop responses with the Table 4.3 gains; (b) with $k_P$ reduced by 50%.

The responses resemble those of Example 4.9. The textbook remarks that the step-response method generally gives higher gains, but its own examples show the reverse: 6.92 against 7.65 for P, and 6.23 against 6.885 for PI. The two methods agree to about 10%.

**Worked check:** The model oscillates when the phase of $G(j\omega)$ reaches $-180^\circ$: $5\omega+\tan^{-1}10\omega+\tan^{-1}60\omega=\pi$. This gives $\omega_u=0.1443$ rad/s, $K_u=1/|G(j\omega_u)|=15.29$ and $P_u=2\pi/\omega_u=43.6$ s. The period read from the plot, 42 s, is 4% short.

### 4.3 The same experiment, done by Routh {#section-4-3}

For a plant without delay, the ultimate gain is the boundary of Routh's stable range, and the ultimate frequency comes from the auxiliary polynomial ([Stability §7](stability_student.md#section-7)). Routh can also show that no such boundary exists, as for L2's second-order plant; then there is no ultimate gain to find. For $G=1/(s+1)^3$ with $D_c=K$:

$$
s^3+3s^2+3s+(1+K)=0,
\qquad
\begin{array}{c|cc}
s^3 & 1 & 3\\
s^2 & 3 & 1+K\\
s^1 & \dfrac{8-K}{3} & \\
s^0 & 1+K &
\end{array}
$$

The $s^1$ entry vanishes at $\boxed{K_u=8}$. The auxiliary polynomial $3s^2+9=0$ gives $s=\pm j\sqrt3$, so

$$
\omega_u=\sqrt3,
\qquad
\boxed{P_u=\frac{2\pi}{\sqrt3}=3.628\ \text{s}} .
$$

Check: $s^3+3s^2+3s+9=(s+3)(s^2+3)$ ✓. Table 4.3 then gives $k_P=4.8$, $T_I=1.814$ s and $T_D=0.453$ s. The resulting overshoots are 54% for P (about its final value of 0.8), 56% for PI and 41% for PID: stable, but lively.

The experiment and the calculation find the same boundary. Routh needs a model; the experiment needs only the plant, and a willingness to make it oscillate.

![Ultimate-gain oscillation of the heat exchanger, Table 4.3 responses, and Ziegler–Nichols tuning of 1/(s+1)^3 via Routh](demos/ch4/figures/l4_demo2_ultimate_gain.svg)

---

## 5. After Ziegler–Nichols {#section-5}

![Fig. 4.22 — Matlab's pidTuner GUI](./book-figures/4-22.png)

*Fig. 4.22 (textbook):* a model-based interactive tuner.

Many refinements followed (Cohen–Coon, Chien–Hrones–Reswick, Åström–Hägglund), along with model-based tools such as Matlab's `pidTuner`, which balance performance against robustness. Three points matter:

1. **Z–N is a starting point.** Both textbook examples end by reducing $k_P$ by half, and operators routinely fine-tune by hand.
2. **Z–N settings are not robust.** Åström and Murray (§11.3) note that the rules use too little process information and give loops that lack robustness. Improved rules use more information about the plant, such as its static gain or a first-order-plus-delay model, and typically give lower gains.
3. **The ultimate-gain experiment is risky** on real equipment. Relay auto-tuning, built into many commercial PID controllers, avoids it. A relay of amplitude $d$ in the loop produces a small limit cycle at about the ultimate period. If the output amplitude is $a$, then $K_u\approx4d/(\pi a)$, and the plant never runs at the stability boundary with a linear gain.

---

## 6. Realising the PID: where the derivative acts {#section-6}

### 6.1 Derivative kick {#section-6-1}

The ideal derivative $k_Ds$ acting on the error differentiates the reference. A unit step in $r$ puts an impulse $k_D\delta(t)$ into $u$, which no actuator can deliver: in practice the amplifier saturates briefly and the mechanism receives a jolt, called **derivative kick**. The textbook's remedy is to move the derivative into the feedback path.

![Fig. 4.10(a) — PID with the D-term in the feedback path](./book-figures/4-10a.png)
![Fig. 4.10(b) — PID with the D-term in the forward path](./book-figures/4-10b.png)

*Fig. 4.10 (textbook):* (a) derivative acting on the output; (b) derivative acting on the error.

With the derivative on the output,

$$
U=\Big(k_P+\frac{k_I}{s}\Big)E-k_DsY
\quad\Longrightarrow\quad
\frac{Y}{R}=\frac{G\,(k_P+k_I/s)}{1+G\,(k_P+k_I/s+k_Ds)} .
$$

The denominator is the same as for the forward-path version. **The closed-loop poles, and the responses to disturbances and noise, are unchanged. Only the zeros from $R$ to $Y$ change.** For $G=A/(s^2+a_1s+a_2)$,

$$
\frac{Y}{R}\Big|_{\text{D on error}}=\frac{A(k_Ds^2+k_Ps+k_I)}{\Delta(s)},
\qquad
\frac{Y}{R}\Big|_{\text{D on output}}=\frac{A(k_Ps+k_I)}{\Delta(s)},
$$

with $\Delta(s)=s^3+(a_1+Ak_D)s^2+(a_2+Ak_P)s+Ak_I$ (textbook Eq. 4.77).

### 6.2 The filtered derivative {#section-6-2}

In practice the derivative is always filtered:

$$
k_Ds\;\longrightarrow\;\frac{k_Ds}{1+sT_f},
\qquad
T_f=\frac{T_D}{N},
$$

with $N$ typically between 5 and 20 (Åström and Murray §11.5). The derivative's high-frequency gain is then bounded at $k_D/T_f=k_PN$, and one fast pole near $-1/T_f$ is added. With the filtered derivative on the error, a unit reference step gives

$$
u(0^+)=k_P+\frac{k_D}{T_f}=k_P(1+N),
$$

which is 66 for $k_P=6$ and $N=10$. With the derivative on the output, $u(0^+)=k_P$.

### 6.3 Setpoint weighting {#section-6-3}

More generally, let the reference enter the proportional and derivative terms with weights $b$ and $c$:

$$
u=k_P\,(b\,r-y)+k_I\!\int_0^t(r-y)\,d\tau+k_D\,(c\,\dot r-\dot y).
$$

The integral term must see the true error, or the steady state would be wrong. The choice $c=0$ is standard, and $b$ between 0 and 1 is a design choice. Åström and Murray (§11.5) write the weights as $\beta$ and $\gamma$; with $b=c=0$ the controller is sometimes called I-PD.

**Worked example:** Take $G=1/(s^2+1.4s+1)$ (textbook Eq. 4.58 with $a_1=1.4$, $a_2=A=1$), with $k_P=6$, $k_I=6$, $k_D=2$ and $N=10$. With the ideal derivative, the characteristic polynomial is $s^3+3.4s^2+7s+6$, with roots $-1.435$ and $-0.982\pm1.793j$. The filter moves these to $-1.504$ and $-1.076\pm1.776j$ and adds a pole at $-27.74$. These poles are the same for all three implementations:

| Implementation | $u(0^+)$ | overshoot | 10–90% rise | zeros $R\to Y$ |
|---|---:|---:|---:|---|
| (a) PID on error ($b=c=1$) | 66 | 18.9% | 0.47 s | $-1.409\pm0.861j$ |
| (b) D on output ($b=1$, $c=0$) | 6 | 31.9% | 0.61 s | $-1$, $-30$ |
| (c) P and D on output ($b=c=0$) | 0 | 2.9% | 1.32 s | $-30$ |

(The zero at $-30$ is the filter pole reappearing in the numerator.) Removing the kick increased the overshoot. With the filter cleared, the reference numerator changed from $(k_D+k_PT_f)s^2+(k_P+k_IT_f)s+k_I=2.2s^2+6.2s+6$ (zeros $-1.409\pm0.861j$) to $(k_Ps+k_I)(1+sT_f)$, whose slow real zero at $-k_I/k_P=-1$ sits close to the dominant poles, and a slow LHP zero adds overshoot ([Specifications and zeros](time-domain-specs_student.md)). Removing that zero as well, with $b=0$, nearly eliminates the overshoot but nearly triples the rise time. Because the feedback loop is the same in all three, a disturbance produces the same response in each. **The reference path is a design decision separate from the loop.**

![Output and control effort for three reference paths of the same PID loop](demos/ch4/figures/l4_demo4_derivative_kick.svg)

---

## 7. Integrator windup and antiwindup {#section-7}

### 7.1 What goes wrong {#section-7-1}

![Fig. 9.20 — Feedback system with actuator saturation](./book-figures/9-20.png)

*Fig. 9.20 (textbook):* a PI loop with a saturating actuator.

Every actuator has limits. While it is saturated, $u=u_{\max}$ whatever the controller demands, so **the feedback loop is open**. The integrator keeps integrating the error and the demand $u_c$ keeps growing. When the output finally reaches the setpoint, the integrator holds a large stored value that must be discharged by an error of the opposite sign, which produces a large overshoot. With the loop open, the integrator is an unstable element.

### 7.2 The antiwindup loop {#section-7-2}

![Fig. 9.21(a) — Antiwindup with a dead-zone nonlinearity](./book-figures/9-21a.png)
![Fig. 9.21(b) — Antiwindup using the actuator saturation itself](./book-figures/9-21b.png)

*Fig. 9.21(a, b) (textbook):* two equivalent antiwindup schemes for a PI controller.

Feed the difference between the demand and the actual actuator output back into the integrator through a gain $K_a$ (Fig. 9.21b):

$$
\dot u_I=k_I\big[e-K_a(u_c-u)\big],
\qquad
u_c=k_Pe+u_I,
\qquad
u=\operatorname{sat}(u_c).
$$

When the actuator is not saturated, $u_c=u$ and the extra term vanishes, so antiwindup is invisible to linear analysis. *Its purpose is to provide local feedback that stabilises the controller only when the main loop is opened by saturation.*

This scheme is widely known as **back-calculation**. Åström and Murray (§11.4) write it as $\dot u_I=k_Ie+k_{aw}(u-u_c)$, so $k_{aw}=k_IK_a$. They advise choosing $k_{aw}$ as a multiple of $k_I$: large enough to reset the integrator quickly, but not so large that measurement noise causes resets. Example 9.9's $K_a=10$ gives $k_{aw}=40$, ten times $k_I$. A simpler alternative in digital controllers is **conditional integration** (clamping): stop integrating while the actuator is saturated *and* the error would drive the integrator further into saturation. For $k_I>0$ that is the case when $(u_c-u)\,e>0$. Integration that brings the demand back inside the limits must be allowed, or an integrator that has already wound up can never unwind.

### 7.3 Example 9.9, worked by hand {#section-7-3}

Plant $G=1/s$, controller $D_c=2+4/s$ ($k_P=2$, $k_I=4$), $|u|\le1$, unit reference step.

**Without antiwindup.** At $t=0^+$, $e=1$ and $u_c=2$, so $u=1$. The plant integrates a constant, so $y=t$, $e=1-t$ and

$$
u_I(t)=4\int_0^t(1-\tau)\,d\tau=4t-2t^2 ,
$$

which reaches its maximum $u_I=2$ at exactly $t=1$, when $y$ crosses the setpoint. (The textbook reads this time as 1.1 s from its plot.) But $u_c=2(1-t)+u_I$ is still above 1. With $x=t-1$, $u_c=-2x+2-2x^2$, and saturation ends when $u_c=1$:

$$
2x^2+2x-1=0
\quad\Longrightarrow\quad
x=\frac{\sqrt3-1}{2}=0.366,
\qquad
t=1.366\ \text{s}.
$$

For 0.366 s after the output passes the target, the plant is still driven at full effort. The overshoot is 53%.

**With antiwindup, $K_a=10$.** The overshoot falls to 15%, and the actuator leaves saturation at $t=0.525$ s instead of 1.366 s. The integrator state goes negative immediately: at $t=0^+$, $u_c-u=1$, so $\dot u_I=4(1-10)<0$.

| $K_a$ | overshoot | leaves saturation | max $u_I$ | min $u$ |
|---:|---:|---:|---:|---:|
| 0 | 52.9% | 1.366 s | 2.000 | $-0.578$ |
| 1 | 17.8% | 0.762 s | 0.651 | $-0.194$ |
| 10 | 14.9% | 0.525 s | 0.547 | $-0.163$ |
| 100 | 14.9% | 0.503 s | 0.546 | $-0.163$ |

Increasing $K_a$ beyond about 10 changes little.

![Fig. 9.23(a) — Integrator antiwindup: step response](./book-figures/9-23a.png)
![Fig. 9.23(b) — Integrator antiwindup: control effort](./book-figures/9-23b.png)

*Fig. 9.23 (textbook):* step response and control effort with and without antiwindup.

![Output, actuator signal and integrator state with and without antiwindup](demos/ch4/figures/l4_demo3_antiwindup.svg)

Windup is a nonlinear effect. A linear simulation (for example `step()` on a transfer function) cannot show it; the saturation must be included in the simulation.

### 7.4 Why the integrator becomes a lag {#section-7-4}

![Fig. 9.21(c) — The antiwindup loop while saturated](./book-figures/9-21c.png)
![Fig. 9.21(d) — Equivalent first-order lag](./book-figures/9-21d.png)

*Fig. 9.21(c, d) (textbook):* during saturation the antiwindup loop turns the integrator into a lag.

While saturated, $u=u_{\max}$ is constant and only shifts the operating point. For the incremental dynamics,

$$
sU_I=k_IE-k_IK_a(k_PE+U_I)
\quad\Longrightarrow\quad
U_I=\frac{k_I(1-K_ak_P)}{s+K_ak_I}\,E,
$$

$$
\frac{U_c}{E}=k_P+\frac{k_I(1-K_ak_P)}{s+K_ak_I}=\boxed{\frac{k_Ps+k_I}{s+K_ak_I}} .
$$

The integrator's pole has moved from the origin to $-K_ak_I$, which is $-40$ in Example 9.9: a lag with time constant 0.025 s. During saturation the controller is stable and cannot run away.

---

## 8. Feedforward by plant model inversion {#section-8}

### 8.1 The idea {#section-8-1}

Integral action removes steady-state error but reduces damping. For a known input there is a cheaper alternative: compute the effort the model says is needed and apply it directly, leaving feedback to correct the difference between model and plant. The simplest version inverts only the plant's DC gain.

![Fig. 4.27(a) — Feedforward for tracking](./book-figures/4-27a.png)
![Fig. 4.27(b) — Feedforward for disturbance rejection](./book-figures/4-27b.png)

*Fig. 4.27 (textbook):* DC-gain feedforward for (a) tracking and (b) a measured disturbance.

- **Tracking:** $U=D_cE+G^{-1}(0)R$.
- **Disturbance rejection:** in Fig. 4.27(b) $W$ is an **output disturbance**, added after the plant. If it is *measured*, $U=D_cE-G^{-1}(0)W$ cancels its steady-state effect. For a disturbance at the plant *input*, as in L1–L3, direct cancellation is simply $U=D_cE-W$, with no $G^{-1}(0)$. An unmeasured disturbance can only be handled by feedback.

### 8.2 Example 4.11 {#section-8-2}

Take $G(s)=1/(s^2+1.4s+1)$, so $G^{-1}(0)=1$, with $D_c=k_P$ for $k_P=1.5$ and $6$.

**Tracking.** $Y=G\,[k_P(R-Y)+R]$, so

$$
\frac{Y}{R}=\frac{(1+k_P)G}{1+k_PG}=\frac{1+k_P}{s^2+1.4s+1+k_P},
\qquad
\frac{Y}{R}\Big|_{s=0}=1 .
$$

**Output disturbance ($R=0$).** $Y=W+G\,[-k_PY-W]$, so

$$
\frac{Y}{W}=\frac{1-G}{1+k_PG}=\frac{s^2+1.4s}{s^2+1.4s+1+k_P},
\qquad
\frac{Y}{W}\Big|_{s=0}=0 .
$$

![Fig. 4.28 — Tracking performance with feedforward](./book-figures/4-28.png)

*Fig. 4.28 (textbook):* tracking with feedforward.

![Fig. 4.29 — Constant disturbance rejection with feedforward](./book-figures/4-29.png)

*Fig. 4.29 (textbook):* disturbance rejection with feedforward.

Feedforward changes the numerator but not the denominator, so the closed-loop poles are those of the plain proportional loop.

**Worked check:** For $k_P=1.5$: $\omega_n=\sqrt{2.5}=1.581$, $\zeta=1.4/(2\times1.581)=0.443$, $M_p=21.2\%$. For $k_P=6$: $\omega_n=\sqrt7=2.646$, $\zeta=0.265$, $M_p=42.2\%$. These match the peaks of 1.21 and 1.42 in Fig. 4.28. Since $(s^2+1.4s)/\Delta=1-(1+k_P)/\Delta$, the disturbance responses start at 1 and undershoot to $-0.212$ and $-0.422$. Without feedforward the Type 0 loop leaves steady errors $1/(1+k_P)$: 0.4 and 0.143.

![Feedforward tracking and disturbance rejection compared with proportional feedback alone](demos/ch4/figures/l4_demo5_feedforward.svg)

### 8.3 When the model is wrong {#section-8-3}

The correction is only as good as the model. If the true DC gain is $G(0)$ and the model's is $\hat G(0)$, the steady tracking error is

$$
e_{ss}=\frac{1-G(0)/\hat G(0)}{1+k_PG(0)} .
$$

With a 20% error ($G(0)=1.2$, $\hat G(0)=1$): at $k_P=1.5$, $e_{ss}=-0.2/2.8=-0.071$, against $+0.357$ with feedback alone; at $k_P=6$, $-0.024$ against $+0.122$. Feedforward removes most of the error, and feedback divides the remainder by $1+k_PG(0)$, the inverse of the sensitivity $S(0)$ from [L1](feedback-properties_student.md). Feedforward does the work the model can predict; feedback corrects what it cannot. Integral action makes the residual exactly zero.

---

## 9. Digital implementation, and summary {#section-9}

Real controllers are programs. Textbook §4.5 notes that a continuous $D_c(s)$ must be converted to a difference equation (Appendix W4.5 and Chapter 8). Two ideas from this lecture carry over directly: antiwindup becomes a conditional statement on the integrator update, and the filtered derivative becomes a first-order digital filter whose time constant must be long compared with the sample period.

```text
   ZIEGLER-NICHOLS          Dc = kP (1 + 1/(TI s) + TD s)

     step test  (slope R, lag L)        ultimate gain  (Ku, Pu)
       P    kP = 1/(RL)                   P    kP = 0.5 Ku
       PI   kP = 0.9/(RL)  TI = L/0.3     PI   kP = 0.45 Ku  TI = Pu/1.2
       PID  kP = 1.2/(RL)  TI = 2L        PID  kP = 0.6 Ku   TI = Pu/2
                           TD = 0.5L                         TD = Pu/8

     target: quarter decay  <=>  zeta = 0.215  <=>  50% overshoot
             (standard 2nd-order step response)
     then detune

   REALISING THE PID          same loop, different reference path
     u = kP(b r - y) + kI INT(r - y) + kD(c r' - y')
     filtered D: kD s/(1 + s TD/N)                  kick = kP(1 + N)

   ANTIWINDUP                 saturation opens the loop
     uI' = kI [ e - Ka (uc - u) ]
     while saturated: uc/e = (kP s + kI)/(s + Ka kI)

   FEEDFORWARD
     U = Dc E + G^-1(0) R       poles unchanged, DC gain R->Y = 1
     model error: e_ss = (1 - G(0)/Ghat(0)) / (1 + kP G(0))
```

---

## Review questions

1. For a standard second-order response, quarter decay means 50% overshoot. Why was this acceptable for a 1940s refinery? Name a mechanical system where it would be unacceptable.
2. Both Ziegler–Nichols methods use only two numbers from the plant. What information do they discard, and when would that matter?
3. The ultimate-gain experiment drives the plant to the edge of instability. What could go wrong on a real machine?
4. Moving the derivative to the output removed the kick but increased the overshoot in §6.3. Explain this using zero locations.
5. Setpoint weighting changes the response to $r$ but not to $w$. Why is that a useful property?
6. Why can a linear closed-loop analysis never predict windup? What does it tell you about antiwindup?
7. Feedforward and integral action both remove steady error for a constant reference. Compare what each costs and what each depends on.
8. What would full inversion $G^{-1}(s)$ require, and why is it impossible for a plant with a time delay or an RHP zero?
9. Does having three stable lag poles guarantee a finite ultimate gain? For $G(s)=(s+0.1)^2/(s+1)^3$, derive the characteristic polynomial under proportional negative feedback and use Routh's criterion to test all $k_P>0$. The left-half-plane zeros add phase lead; how does the result differ from $G=1/(s+1)^3$? Would a real pole crossing at $\omega=0$ supply a finite oscillation period?

## Optional practice

Optional practice from FPE, 8th edition; these are study suggestions, not an assignment.

| Problem | Topic |
|---|---|
| 4.46 | Z–N tuning from a paper machine's step and impulse data |
| 4.47 | Z–N tuning for a paper-machine transfer function |
| 4.48 | Feedforward for DC motor tracking and disturbance |
| 4.27 | Cruise control: feedforward compared with feedback |
| Review Questions 4.10, 4.11 | Derivative in the feedback path; tuning rules |
| Extra | Use Routh to find $K_u$ and $P_u$ for $G=1/[s(s+1)(s+2)]$ (answer: $K_u=6$, $P_u=2\pi/\sqrt2=4.44$ s), apply Table 4.3, and simulate |

## Chapter 4 student notes

- [L1: The basic equations of control](feedback-properties_student.md)
- [L2: The three-term controller: P, I, D, PI and PID](pid-control_student.md)
- [L3: Steady-state error and system type](system-type_student.md)
- [L4: Tuning, realising and feeding forward the PID](pid-tuning_student.md)
