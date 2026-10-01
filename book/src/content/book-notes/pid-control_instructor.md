# A First Analysis of Feedback II — The Three-Term Controller: P, I, D, PI and PID
## FPE 8th ed., Sections 4.3.1 through 4.3.5

**Audience:** Fourth-year undergraduate mechanical engineering (ME 404)

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., §§4.3–4.3.5 (Eqs. 4.55–4.90, Examples 4.5–4.8). Worked examples and figure numbers are the book's. Additions of my own are marked **[beyond the book]**.

**Prerequisites:** [the basic equations of feedback](feedback-properties_instructor.md). From Chapter 3: the Final Value Theorem and partial fractions in [Convolution and transfer functions](convolution-impulse-response_instructor.md), second-order specifications in [Time-domain specifications](time-domain-specs_instructor.md), and Routh's criterion in [Stability](stability_instructor.md).

**Course order:** in this course the PID lectures come **before** system type and error constants (FPE §4.2, our [Steady-state error and system type](system-type_instructor.md)). Every steady-state result below is derived directly from the Final Value Theorem. Where the book says "Type 1" or quotes an error constant, the notes give the FVT calculation and forward-reference [Steady-state error and system type](system-type_instructor.md). Integrator windup, derivative filtering and tuning rules belong to [PID tuning and implementation](pid-tuning_instructor.md).

**Duration:** two 75-minute sessions (the schedule's "PID" and "PID (cont.)"). The split point is marked in §3 and in the text.

**Book figures:** figure numbers refer to the source chapter at

```text
references/documents/Franklin, Powell, Emami-Naeimi - 8th Ed./4 - A First Analysis of Feedback.pdf
```

Page cues use the PDF viewer's 1-based page numbers (120 pages). The figures are embedded from `book-figures/`. **[beyond the book]** Classroom checks and teaching prompts are instructor additions. Demo paths are relative to `demos/`; the demonstration index in §21 lists the scripts.

**Notation:**

| Symbol | Meaning |
|---|---|
| $G(s)$ | plant; in §§6–8 the second-order motor model $A/(s^2+a_1s+a_2)$ of Eq. (4.58) |
| $D_c(s)$ | controller (the book writes $D_{cl}$ when it sits in the forward path of Fig. 4.2) |
| $R,\ Y,\ U,\ E,\ W$ | reference, output, control, error $E=R-Y$, disturbance at the plant input |
| $k_P,\ k_I,\ k_D$ | proportional, integral and derivative gains |
| $T_I=k_P/k_I,\ T_D=k_D/k_P$ | integral (reset) time and derivative time |
| $a(s)$ | closed-loop characteristic polynomial, $1+D_cG=0$ cleared of fractions |
| $\mathcal T(s)$ | closed-loop transfer function $Y/R$ |

---

# Part 0 — Planning

## 1. Teaching strategy

[Feedback properties](feedback-properties_instructor.md) showed what feedback buys in principle: disturbance attenuation and lower sensitivity when the loop gain is large. This lecture introduces the controller that almost every mechanical engineer will actually tune. It predates root locus, Bode and state space, and was developed by trial and error.

The book's structure is simple: one term at a time, each on the same second-order plant, with the Final Value Theorem as the measuring instrument. Keep that structure. Every term gets the same three questions:

| Question | P | I | D |
|---|---|---|---|
| What does it respond to? | the error now | the accumulated error | the error's trend |
| Steady-state error to a constant $r$ or $w$? | nonzero, falls as $1/(1+k_PG(0))$ | **zero**, if $G(0)\ne0$ and $k_I\ne0$ makes the loop internally stable | says nothing: output of D is zero for constant $e$ |
| What does it do to the poles? | moves $\omega_n$, not $\sigma$ (on this plant) | adds a pole; destabilises if too large | adds damping |

The framing line:

> **Each term answers a different question about the error — how big is it, how long has it been there, and where is it going. The controller adds the three answers.**

Four moments to protect:

1. **§6.2** — proportional gain on the motor model slides the poles *vertically*. Error goes down, damping goes down, and the settling-time estimate $4.6/\sigma$ does not change at all (the exact settling time moves only a little).
2. **§7.4** — the one-line argument for why integral control gives zero error without knowing the plant: *if the control settles to a constant, $\dot u=k_Ie=0$.*
3. **§10.3** — Example 4.5's PI zero cancels the slow thermal pole. The reference response looks second order; the disturbance response still carries the 10-second tail. It is the cancellation lesson from *([Stability and Routh’s criterion §6.3](stability_instructor.md#section-6-3))* in its legal, stable form.
4. **§11.2** — three gains, three closed-loop roots: PID on a second-order plant places the poles anywhere, by matching coefficients.

---

## 2. Learning objectives

By the end of these two sessions students should be able to:

1. Write the P, I, D, PI and PID control laws in the time domain and as transfer functions, and state what signal each term responds to.
2. For proportional control of a second-order plant, derive the closed-loop characteristic equation and explain why, in the underdamped region, $k_P$ changes the natural frequency but not the envelope decay rate.
3. Use the Final Value Theorem to find the steady-state output, error and control for step references and step disturbances under P and under I control.
4. Explain why integral control gives zero steady-state error to constant references and disturbances despite plant parameter changes, provided the DC gain remains nonzero and the closed loop remains internally stable (all internal modes decay).
5. Find the range of integral gain that keeps an integral or PI loop stable, using Routh's criterion.
6. Explain why derivative control is not used alone, interpret it as prediction, and state its noise liability.
7. Compare the derivative in the forward path with the derivative on the measured output (Fig. 4.10): same poles, different zeros, and no derivative kick.
8. Work Example 4.5: compare open-loop, P and PI control of a thermal plant for offset, speed and robustness to gain error, and identify what a stable pole-zero cancellation hides.
9. Choose PID gains to place the three closed-loop roots of a second-order plant by matching coefficients.
10. Use the Final Value Theorem to find disturbance errors for P, PI, PD and PID in Examples 4.6–4.8, as a preview of system type.

---

## 3. Suggested lecture flow (2 × 75 minutes)

### Session A — "PID" (P, I and D, one term at a time)

| Time | Topic | Section |
|---:|---|---|
| 0–5 min | Where the controller sits; the three-term law; the FVT recipe | §§4–5 |
| 5–25 min | Proportional control on the motor model; Fig. 4.7 | §6 |
| 25–50 min | Integral control: history, zero error, the robustness argument, the price | §7 |
| 50–68 min | Derivative control: prediction, why never alone, where to put it (Fig. 4.10) | §8 |
| 68–75 min | Summary so far; what PI and PID must reconcile | §9 |

**Split point.** Session A ends after §9. If Session A overruns, carry §8.3 (Fig. 4.10 and the derivative kick) into Session B.

### Session B — "PID (cont.)" (combining the terms)

| Time | Topic | Section |
|---:|---|---|
| 0–5 min | Recap: three questions, three answers | §9 |
| 5–30 min | PI; Example 4.5 thermal system; the hidden slow mode | §10 |
| 30–48 min | PID; three knobs, three roots; coefficient matching | §11 |
| 48–60 min | Example 4.6: motor speed under P, PI and PID | §12 |
| 60–70 min | Disturbance errors in Examples 4.7 and 4.8, by FVT; preview of system type | §13 |
| 70–75 min | Summary table; what [Steady-state error and system type](system-type_instructor.md) and [PID tuning and implementation](pid-tuning_instructor.md) add | §§14–15 |

**Prepare as slides:** Fig. 4.2 (the loop), Fig. 4.7, 4.9, 4.10, 4.12, 4.14 and 4.16, plus the summary table in §14. Put the characteristic equations on the board: (4.60), the integral cubic, (4.77).

**If you are short of time,** compress §13 to the two boxed results and assign the algebra. Do not compress §7.4 or §10.3.

### Runnable demonstrations

```
cd demos
uv run python ch4/l2_demo1_proportional.py --show
uv run python ch4/l2_demo2_integral.py --show
uv run python ch4/l2_demo3_derivative_placement.py --show
```

**Run Demos 1, 2 and 3 live in Session A**; Demos 4 and 5 work as slides in Session B. Demo 2 is the one to linger on: three different plants, one integral gain, and the error goes to zero in every case.

### Teaching scope

Use the demos for the selected live examples; the accompanying checks also work on the board. In each session, select the protected moments in §1 and assign the remaining worked examples as follow-up reading. Do not try to present every figure and derivation live.

---

# Part I — Session A: one term at a time

## 4. Opening

### Instructor script

> Last lecture we wrote down the basic equations of feedback and saw what a large loop gain buys: disturbances shrink and the loop stops caring about the plant's exact gain. We did not say what to put in the controller box.
>
> Today we fill it. The controller in the box is older than every other method in this course. Engineers found it by trial and error in the 1920s and 1930s, and it still runs most of the loops you will ever touch — the thermostat, the cruise control, the motor drives on a lab bench, the flight controller of a hobby drone.
>
> It has three terms. Each one looks at the error and asks a different question. The proportional term asks how big the error is now. The integral term asks how long it has been there. The derivative term asks where it is heading. We will take them one at a time, on one plant, with one tool: the Final Value Theorem.

---

## 5. The three-term controller (§4.3)

### 5.1 The law

$$
\boxed{
D_c(s)=k_P+\frac{k_I}{s}+k_Ds
\tag{4.55}
}
$$

In the time domain, with $e=r-y$,

$$
u(t)=k_Pe(t)+k_I\int_{t_0}^{t}e(\tau)\,d\tau+k_D\dot e(t).
\tag{4.74}
$$

Process-control literature and most industrial controllers write the same law with one overall gain and two times:

$$
D_c(s)=k_P\left(1+\frac{1}{T_Is}+T_Ds\right),
\qquad T_I=\frac{k_P}{k_I},\quad T_D=\frac{k_D}{k_P}.
$$

**[beyond the book]** Both forms appear on data sheets and in the tuning tables in [PID tuning and implementation](pid-tuning_instructor.md); students should convert between them without thinking. $T_I$ and $T_D$ have units of time whatever the units of $k_P$.

### 5.2 Where it sits

![Fig. 4.2 — Closed-loop system with reference, control, disturbance and sensor noise](./book-figures/4-2.png)

> **[ FIG 4.2 ]** — PDF p. 4 *(slide; leave it up through §7)*

The controller acts on $E=R-Y$ and its output $U$ adds to a disturbance $W$ at the plant input. Sensor noise $V$ is set to zero in this lecture. From *([Feedback properties](feedback-properties_instructor.md))*, with $V=0$,

$$
Y=\frac{D_cG}{1+D_cG}R+\frac{G}{1+D_cG}W,
\qquad
U=\frac{D_c}{1+D_cG}R-\frac{D_cG}{1+D_cG}W .
$$

Every result in this lecture is one of these four transfer functions, evaluated at $s=0$.

### 5.3 The measuring instrument

**[beyond the book]** The recipe used throughout, in place of the system-type machinery of [Steady-state error and system type](system-type_instructor.md):

> For a step of size $r_0$ (or $w_0$), and **provided the closed loop is stable**,
> $$y(\infty)=\lim_{s\to0}s\,\mathcal T(s)\frac{r_0}{s}=\mathcal T(0)\,r_0 .$$
> For a ramp of slope $v_0$, $y(\infty)$ is not constant; compute the error instead, $e(\infty)=\lim_{s\to0}s\,\dfrac{E}{R}(s)\dfrac{v_0}{s^2}$.

The stability proviso is not decoration *([Stability and Routh’s criterion §5](stability_instructor.md#section-5))*. Each time we compute a final value below, say where the stability condition came from.

---

## 6. Proportional control (§4.3.1)

### 6.1 One knob

$$
u(t)=k_Pe(t),
\qquad
D_c(s)=k_P .
\tag{4.56–4.57}
$$

The controller has no dynamics: an amplifier with a knob. For a motor with non-negligible inductance, the plant is second order:

$$
G(s)=\frac{A}{s^2+a_1s+a_2}.
\tag{4.58}
$$

The characteristic equation $1+k_PG=0$ becomes

$$
\boxed{
s^2+a_1s+a_2+k_PA=0
\tag{4.60}
}
$$

Match it to $s^2+2\zeta\omega_ns+\omega_n^2$:

$$
\omega_n=\sqrt{a_2+k_PA},
\qquad
2\zeta\omega_n=a_1\ \ (\text{fixed}),
\qquad
\sigma=\zeta\omega_n=\frac{a_1}{2}\ \ (\text{fixed}).
$$

The knob reaches the constant term only. It sets how fast the response oscillates, not how fast its envelope decays.

This holds while the closed loop is **underdamped**, $a_2+Ak_P>a_1^2/4$; the roots are $-a_1/2\pm\sqrt{a_1^2/4-(a_2+Ak_P)}$. In the overdamped region the two real roots move with $k_P$ (for $G=1/(s^2+3s+2)$: $-1.887,\,-1.113$ at $k_P=0.1$, merging at $-1.5$ when $k_P=0.25$). The motor model, with $a_1^2/4=0.49<a_2=1$, is underdamped for every $k_P>0$. What stays fixed is the exponential **envelope** decay rate, so the settling-time *estimate* $4.6/\sigma$ does not change; the exact settling time still shifts somewhat.

### 6.2 Fig. 4.7 and the Final Value Theorem

The book's numbers: $A=1$, $a_1=1.4$, $a_2=1$, so $G(0)=1$.

![Fig. 4.7 — Proportional control: steady-state tracking error and loss of damping as gain rises](./book-figures/4-7.png)

> **[ FIG 4.7 ]** — PDF p. 38 *(slide)*

With $\mathcal T=k_PG/(1+k_PG)$, the step response settles (for every $k_P>-1$, since the quadratic then has positive coefficients) at

$$
y(\infty)=\frac{k_PG(0)}{1+k_PG(0)},
\qquad
e(\infty)=\frac{1}{1+k_PG(0)},
\qquad
u(\infty)=k_Pe(\infty).
$$

> **Teaching check [beyond the book]:**
>
> | | $k_P=1.5$ | $k_P=6$ |
> |---|---|---|
> | $a(s)$ | $s^2+1.4s+2.5$ | $s^2+1.4s+7$ |
> | $\omega_n$ | $\sqrt{2.5}=1.581$ | $\sqrt7=2.646$ |
> | $\zeta=0.7/\omega_n$ | 0.443 | 0.265 |
> | poles | $-0.7\pm1.418j$ | $-0.7\pm2.551j$ |
> | $y(\infty)=k_P/(1+k_P)$ | 0.600 | 0.857 |
> | $e(\infty)=1/(1+k_P)$ | 0.400 | 0.143 |
> | $u(\infty)=k_Pe(\infty)$ | 0.600 | 0.857 |
> | overshoot above $y(\infty)$ | 21.2% | 42.2% |
>
> *Working.* The overshoot follows from $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$: at $\zeta=0.443$, $\pi\zeta=1.392$ and $\sqrt{1-0.196}=0.897$, so $M_p=e^{-1.552}=0.212$. At $\zeta=0.265$, $e^{-0.833/0.964}=e^{-0.863}=0.422$. The measured peaks, $0.727$ at $2.22$ s and $1.219$ at $1.23$ s, match the figure. Note that $u(\infty)=y(\infty)/G(0)$: the steady control is whatever the plant needs to hold that output.

Quadrupling the gain cuts the error by a factor of 2.8, from 0.4 to 0.143, and doubles the overshoot. Better accuracy has cost damping.

#### Say out loud

> Look at the pole column. The real part is $-0.7$ in both cases. The settling-time estimate $4.6/\sigma=4.6/0.7=6.6$ s is the same for every gain. Turning the knob buys accuracy and oscillation; it buys no decay rate at all.
>
> **Teaching check [beyond the book]:** the *estimate* is fixed, not the exact settling time. Measured to within 1% of each final value, the step responses settle at 5.55 s ($k_P=1.5$) and 6.45 s ($k_P=6$). The envelope is the same; the time the oscillation last leaves the band is not.

> **[ DEMO 1 ]** — `ch4/l2_demo1_proportional.py` *(live, ~5 s)*

![Proportional control: step responses for four gains and the closed-loop poles sliding vertically along Re(s) = -0.7](demos/ch4/figures/l2_demo1_proportional.svg)

### 6.3 A step disturbance

From §5.2 with $D_c=k_P$:

$$
\frac{Y}{W}=\frac{G}{1+k_PG},
\qquad
\frac{U}{W}=-\frac{k_PG}{1+k_PG}.
$$

For a unit step $w$, $y(\infty)=G(0)/(1+k_PG(0))=1/(1+k_P)$: 0.4 at $k_P=1.5$ and 0.143 at $k_P=6$. The control settles at $-k_P/(1+k_P)$, so the plant sees $u+w=1/(1+k_P)$ and holds exactly that output. The controller has cancelled part of the disturbance and cannot cancel the rest, because to push back it needs an error.

$$
\boxed{
\text{Proportional control needs a nonzero error to produce a nonzero steady control.}
}
$$

That sentence is the whole case for integral action.

### 6.4 Beyond second order

For the underdamped all-pole second-order model used here, proportional gain leaves the poles' real part unchanged. On higher-order plants the picture is less tidy: some poles gain damping while others lose it, and for enough gain a plant of order three or more usually goes unstable. You met that already: in *([Stability and Routh’s criterion §8](stability_instructor.md#section-8))* the gain range was found with Routh. Root locus (Part IV) is the tool that draws the whole picture.

#### Ask the class

> A plant has $G(0)=1$. What proportional gain gives 1% steady-state error to a step? What do you expect the damping to be?

$1/(1+k_P)=0.01$ gives $k_P=99$. On the motor model, $\omega_n=\sqrt{100}=10$ and $\zeta=0.07$: 80% overshoot. Accuracy by gain alone is expensive.

---

## 7. Integral control (§4.3.2)

### 7.1 A controller with a memory

$$
u(t)=k_I\int_{t_0}^{t}e(\tau)\,d\tau,
\qquad
D_c(s)=\frac{k_I}{s}.
\tag{4.62–4.63}
$$

The control at time $t_1$ is $k_I$ times the net area under the error curve up to $t_1$. It depends on the whole history, not on the present value.

![Fig. 4.8 — Integral control: the control signal is proportional to the area under the error curve](./book-figures/4-8.png)

> **[ FIG 4.8 ]** — PDF p. 40 *(slide)*
>
> **Say:** "This curve is the error of the loop we are about to analyse, with $k_I=0.5$. The shaded area is the control. When the error has returned to zero, the area it left behind is still there."

The controller has infinite gain at DC: $|D_c(j\omega)|=k_I/\omega\to\infty$ as $\omega\to0$. Put that together with *([Feedback properties](feedback-properties_instructor.md))*, where large loop gain meant small error, and expect zero steady-state error.

### 7.2 Reference step (Eqs. 4.64–4.67)

Same plant, $G(0)=1$. Multiply numerator and denominator by $s$:

$$
\frac{E}{R}=\frac{1}{1+\frac{k_I}{s}G}=\frac{s}{s+k_IG},
\qquad
\frac{U}{R}=\frac{k_I}{s+k_IG},
\qquad
\frac{Y}{R}=\frac{k_IG}{s+k_IG}.
\tag{4.64–4.65}
$$

For a unit step, and provided the loop is stable,

$$
\boxed{
y(\infty)=\frac{k_IG(0)}{0+k_IG(0)}=1,
\qquad
e(\infty)=\frac{0}{0+k_IG(0)}=0,
\qquad
u(\infty)=\frac{k_I}{0+k_IG(0)}=\frac{1}{G(0)}
}
\tag{4.66–4.67}
$$

For a plant with finite, nonzero $G(0)$, the error is zero **for any nonzero $k_I$ that keeps the loop internally stable**. With P control there was always an error, whatever $k_P$ was. The steady control is the inverse DC gain of the plant — exactly the input you would have computed if you had known the plant perfectly.

### 7.3 Disturbance step (Eqs. 4.68–4.69)

$$
\frac{Y}{W}=\frac{sG}{s+k_IG},
\qquad
\frac{U}{W}=-\frac{k_IG}{s+k_IG}.
\tag{4.68}
$$

$$
\boxed{
y(\infty)=\frac{0\cdot G(0)}{0+k_IG(0)}=0,
\qquad
u(\infty)=-\frac{k_IG(0)}{0+k_IG(0)}=-1
}
\tag{4.69}
$$

The controller ends up producing exactly $-w$. The disturbance is cancelled, not attenuated.

![Fig. 4.9 — Integral control rejects a constant disturbance: (a) output](./book-figures/4-9a.png)
![Fig. 4.9 — (b) control effort settling at −1](./book-figures/4-9b.png)

> **[ FIG 4.9 ]** — PDF p. 43 *(slide)*
>
> **Teaching check [beyond the book]:** with $k_I=0.5$, the closed-loop polynomial is $s(s^2+1.4s+1)+0.5=s^3+1.4s^2+s+0.5$. Its roots are $-0.905$ and $-0.247\pm0.701j$. Check: the roots sum to $-0.905-0.494=-1.399\approx-1.4$ ✓. For the disturbance step the output peaks at $0.764$ at $t=2.71$ s and $u$ dips to $-1.229$ at $5.67$ s before settling at $-1$, as in the figure. For the reference step the error of Fig. 4.8 reaches its minimum, $-0.229$, at the same $5.67$ s. That is no coincidence: comparing (4.65) and (4.68), $U/W=-Y/R$ exactly, so the disturbance-step control is the mirror image of the reference-step output, whose peak is $1.229$.

### 7.4 Why it cannot fail (while it is stable) [beyond the book]

The FVT gives the answer. This gives the reason, in one line, and it is the moment of Session A.

Suppose the closed loop is internally stable (all internal modes decay), so every signal settles to a constant under constant inputs. Then the integrator's output $u$ settles to a constant, so its derivative goes to zero. But the integrator's derivative *is* $k_Ie$:

$$
\dot u=k_Ie\quad\Longrightarrow\quad
u\to\text{const}\ \Longrightarrow\ \dot u\to0\ \Longrightarrow\ e\to0 .
$$

Nothing in that argument mentions $A$, $a_1$, $a_2$, the size of $r$, the size of $w$, or where $w$ enters. The book calls this property **robust**: plant parameter changes do not matter, provided the loop stays stable.

**Qualification [beyond the book]:** a plant zero at the origin can cancel the controller integrator. For $G=s/(s+1)$ and $D_c=k_I/s$, with $k_I>0$, $E/R=(s+1)/(s+1+k_I)$, so a unit reference step leaves $e_{ss}=1/(1+k_I)$. The output settles, but the control ramps without bound: the loop is not internally stable. Indeed, $U/R=k_I(s+1)/[s(s+1+k_I)]$, so $\dot u\to k_I/(1+k_I)$. Before cancellation the characteristic polynomial is $s(s+1+k_I)$: the hidden mode at the origin does not decay. This is why Eqs. (4.66–4.67) require finite, nonzero $G(0)$ and why the settling argument must include the controller state.

#### Instructor script

> An integrator is a device that cannot be at rest while its input is nonzero. If the loop settles, the integrator settled; if the integrator settled, its input is zero; its input is the error. That is the whole proof.
>
> Notice what the argument needs — that the loop settles. That is the one thing integral action does not give you for free, and it is where we go next.

> **[ DEMO 2 ]** — `ch4/l2_demo2_integral.py` *(live, ~5 s)*
>
> Three plants with DC gains 1, 2/3 and 0.4, one $k_I=0.5$. All three reach zero error and all three reject the disturbance. The steady control is $a_2/A$ for each plant: 1, 1.5 and 2.5.

![Integral control on three different plants: reference step, disturbance step, and control effort](demos/ch4/figures/l2_demo2_integral.svg)

### 7.5 The price

**Stability.** The integrator adds a pole at the origin, and the loop order rises from two to three. For the motor model,

$$
a(s)=s^3+a_1s^2+a_2s+Ak_I .
$$

Routh *([Stability and Routh’s criterion §7](stability_instructor.md#section-7))*: the first column is $1,\ a_1,\ (a_1a_2-Ak_I)/a_1,\ Ak_I$, so

$$
\boxed{0<k_I<\frac{a_1a_2}{A}}
$$

For the book's numbers, $0<k_I<1.4$. At $k_I=1.4$, $a(s)=s^3+1.4s^2+s+1.4=(s+1.4)(s^2+1)$: the pair sits at $\pm j$, the plant's own undamped natural frequency.

**Speed.** At $k_I=0.5$ the dominant pair has $\sigma=0.247$, three times slower than the P loop's $0.7$. The 1% settling time is 16.5 s, against about 6 s for P. An integrator responds to area, and area takes time to accumulate.

**Ramps.** A constant error to a ramp reference remains; the book cites §4.2. We derive it in §10.2 and name it in [Steady-state error and system type](system-type_instructor.md).

**Saturation.** Every real actuator saturates. While $u$ is pinned at its limit, the integrator keeps integrating; this is *windup*, and the book sends it to Chapter 9. It is covered in [PID tuning and implementation](pid-tuning_instructor.md). Say now: **never ship integral action without anti-windup.**

---

## 8. Derivative control (§4.3.3)

### 8.1 Rate feedback

$$
u(t)=k_D\dot e(t),
\qquad
D_c(s)=k_Ds.
\tag{4.70–4.71}
$$

Also called **rate feedback**. Its purpose is damping: more stability, faster transients, less overshoot.

### 8.2 Never alone

A derivative controller has nothing to say about where the output should end up. If $e$ is constant — however large — then $u=0$.

> **Teaching check [beyond the book]:** with $D_c=k_Ds$ on the motor model, $\mathcal T=\dfrac{Ak_Ds}{s^2+(a_1+Ak_D)s+a_2}$. The loop is stable for any $k_D>-a_1/A$, and $\mathcal T(0)=0$: a step reference leaves the output at **zero** in steady state. The derivative has added damping ($a_1\to a_1+Ak_D$) and done nothing else. It must be paired with P or I.

**Anticipation [beyond the book].** Combine it with P and read the sum as a prediction:

$$
k_Pe(t)+k_D\dot e(t)=k_P\bigl[e(t)+T_D\dot e(t)\bigr]\approx k_P\,e(t+T_D).
$$

PD control is proportional control acting on a linear extrapolation of the error $T_D$ seconds ahead. When the error is falling fast, the controller eases off before the error reaches zero, which is exactly what removes overshoot. The extrapolation is only good when the error is smooth over $T_D$.

**Noise.** A differentiator's gain is $k_D\omega$, growing without bound with frequency. Sensor noise is high-frequency. The book defers the full discussion to Chapter 6; every practical derivative is filtered, $k_Ds/(\tau_fs+1)$, and choosing $\tau_f$ is part of [PID tuning and implementation](pid-tuning_instructor.md).

### 8.3 Where to put it: Fig. 4.10

![Fig. 4.10(a) — PID with the D-term in the feedback path](./book-figures/4-10a.png)
![Fig. 4.10(b) — PID with the D-term in the forward path](./book-figures/4-10b.png)

> **[ FIG 4.10 ]** — PDF p. 45 *(slide)*

In (b) the derivative acts on $e=r-y$. In (a) it acts on the measurement only, like a tachometer on the motor shaft. The loop, seen from $y$ back to $y$, is the same in both, so the **characteristic equation is identical**. The reference enters differently, so the **zeros of $Y/R$ differ**.

**A concrete pair [beyond the book].** On the motor model with $k_P=3$, $k_I=2$, $k_D=1.6$ (chosen in §11.2), both structures have

$$
a(s)=s^3+3s^2+4s+2=(s+1)(s^2+2s+2),
$$

with poles at $-1$ and $-1\pm j$. The reference transfer functions are

$$
\text{(b)}\ \ \frac{Y}{R}=\frac{1.6s^2+3s+2}{a(s)},
\qquad\qquad
\text{(a)}\ \ \frac{Y}{R}=\frac{3s+2}{a(s)}.
$$

| Structure | Zeros of $Y/R$ | Overshoot | Peak time |
|---|---|---|---|
| (b) D on error | $-0.938\pm0.609j$ | 1.5% | 2.00 s |
| (a) D on output | $-0.667$ | 16.4% | 2.50 s |

In (b), a step in $r$ is differentiated: the control contains an impulse $k_D\delta(t)$. With a realistic filter $\tau_f=0.02$ s, that becomes a spike of $k_D/\tau_f+k_P=1.6/0.02+3=83$ at $t=0^+$, against $u(0^+)=k_P=3$ in (a). This spike is the **derivative kick**; it is what (a) is designed to avoid.

#### Say out loud

> Moving the derivative changes the zeros, not the poles. In this example the kick-free version overshoots more, because it lost the numerator's $s^2$ term that was helping. So "put the derivative on the output" is a rule about the actuator, not a free improvement in the response. [PID tuning and implementation](pid-tuning_instructor.md) returns to the kick when it discusses physical realisation.

> **[ DEMO 3 ]** — `ch4/l2_demo3_derivative_placement.py` *(live, ~5 s)*

![Derivative on the error versus on the output: identical poles, different zeros, and the derivative kick in the control signal](demos/ch4/figures/l2_demo3_derivative_placement.svg)

---

## 9. End of Session A / start of Session B

### Instructor script — closing Session A

> Three terms, three questions. Proportional: how big is the error? It helps, it never finishes the job on a plant like this one with finite DC gain, and it trades damping for accuracy. Integral: how long has the error been there? It finishes the job without knowing the plant — as long as the loop stays stable, which it makes harder. Derivative: where is the error going? It adds damping and does nothing about the final value.
>
> Each term fixes something the others break. Next time we combine them and see whether the fixes add up.

> **— SPLIT POINT: end of Session A (75 min). Session B begins here. —**

### Recap to open Session B

| Term | Responds to | Steady-state effect | Dynamic effect |
|---|---|---|---|
| P | $e(t)$ | error $1/(1+k_PG(0))$ to a unit step | faster, less damped (on the second-order plant) |
| I | $\int e$ | zero error to constant $r$ and $w$, for a plant with $G(0)\ne0$, if internally stable | slower; destabilising if $k_I$ is large |
| D | $\dot e$ | none | damping; amplifies noise |

---

# Part I (continued) — Session B: combining the terms

## 10. PI control and Example 4.5 (§4.3.4)

### 10.1 The law

$$
u(t)=k_Pe(t)+k_I\int_{t_0}^{t}e(\tau)\,d\tau,
\qquad
D_c(s)=k_P+\frac{k_I}{s}=\frac{k_P\left(s+k_I/k_P\right)}{s}.
\tag{4.72–4.73}
$$

Written the second way, PI is a pole at the origin and a **zero at $-k_I/k_P=-1/T_I$**. The integrator provides the zero steady-state error of §7; the proportional term provides a faster response than integral action alone. Most practical controllers with an integral term also have a proportional term.

You have already seen a PI loop: Example 3.34 put $K+K_I/s$ around $1/[(s+1)(s+2)]$ and found its stability region with Routh *([Stability and Routh’s criterion §9](stability_instructor.md#section-9))*. The same Routh reasoning applies here.

### 10.2 Example 4.5: a thermal system

Two thermal masses coupled by conduction (Fig. 2.38 in Chapter 2):

$$
G(s)=\frac{K_o}{(\tau_1s+1)(\tau_2s+1)},
\qquad
\tau_1=1\ \text{s},\ \ \tau_2=10\ \text{s},\ \ K_o=1000 .
$$

Pulling the time constants out, $G(s)=\dfrac{100}{(s+1)(s+0.1)}$: a fast pole at $-1$ and a slow one at $-0.1$. The reference ramps at $30^\circ$C/s to $300^\circ$C, reached at $t=10$ s, and then holds. Goals: negligible overshoot, and robustness to errors in $K_o$, $\tau_1$ and $\tau_2$.

**Open loop.** Apply $u=300/K_o=0.3$.

![Fig. 4.11 — Open-loop step response of the thermal system](./book-figures/4-11.png)

> **[ FIG 4.11 ]** — PDF p. 47

It settles to 1% in $t_s=47.1$ s (confirmed by simulation: 47.11 s), set by the slow pole, with zero error — if $K_o$ is exactly 1000. A 5% gain error gives $315^\circ$C instead of 300: a 5% output error. Open loop has no defence against gain uncertainty *([Feedback properties](feedback-properties_instructor.md))*.

**P control, $k_P=0.03$.** The characteristic polynomial is $(s+1)(10s+1)+30=10s^2+11s+31$, or $s^2+1.1s+3.1$:

$$
\omega_n=\sqrt{3.1}=1.761,
\qquad
\zeta=\frac{1.1}{2(1.761)}=0.312 .
$$

The book rounds this to $\zeta=0.3$. The closed-loop DC gain is $30/31$, so the output settles at $300\times30/31=290.3^\circ$C: an offset of $300/31=9.68^\circ$C (the book's "$10^\circ$C").

![Fig. 4.12 — Closed-loop response for the P controller, nominal and ±10% gain](./book-figures/4-12.png)
![Fig. 4.13 — Control signals for the P controller](./book-figures/4-13.png)

> **[ FIG 4.12, 4.13 ]** — PDF pp. 48–49
>
> **Teaching check [beyond the book]:** with $K_o=900$ and $1100$ the offsets are $300/28=10.71$ and $300/34=8.82^\circ$C. A ±10% plant-gain change moves the offset by about ±1°C, roughly 0.3% of the setpoint, instead of by ±30°C. That is the sensitivity reduction of *([Feedback properties](feedback-properties_instructor.md))*, in numbers. The three output traces are nearly indistinguishable; the control signals (Fig. 4.13) are not, because the controller is doing the compensating.

**PI control, $k_P=0.03$, $k_I=0.003$.**

$$
D_c(s)=0.03+\frac{0.003}{s}=\frac{0.03\,(s+0.1)}{s}.
$$

The controller zero sits at $-0.1$, exactly on the slow plant pole. In the loop gain they cancel:

$$
D_cG=\frac{0.03(s+0.1)}{s}\cdot\frac{100}{(s+1)(s+0.1)}=\frac{3}{s(s+1)},
\qquad
\mathcal T(s)=\frac{3}{s^2+s+3}.
$$

The reference response is that of a standard second-order system with $\omega_n=\sqrt3=1.732$ and $\zeta=1/(2\sqrt3)=0.289$, poles $-0.5\pm1.658j$.

![Fig. 4.14 — Closed-loop response for the PI controller, nominal and ±10% gain](./book-figures/4-14.png)
![Fig. 4.15 — Control signals for the PI controller](./book-figures/4-15.png)

> **[ FIG 4.14, 4.15 ]** — PDF pp. 50–51
>
> **Teaching check [beyond the book]:** simulated 1% settling (band $300\pm3^\circ$C) is 13.44 s, matching the figure; with $K_o=900$ and $1100$ it is 13.62 s and 13.27 s. The peak is $309.9^\circ$C, a 3.3% overshoot on 300 — more than the "negligible" asked for, as the book concedes. The offset is zero for all three gains, and the steady heater command is $300/K_o$: 0.333, 0.300, 0.273. The $K_o$ error does not break the cancellation, because $K_o$ does not move the plant pole at $-0.1$; an error in $\tau_2$ would.

**During the ramp [beyond the book].** The ramp lasts 10 s, long enough to see a steady lag. With the FVT on $E/R=1/(1+D_cG)=\dfrac{s(s+1)}{s^2+s+3}$ and $R=30/s^2$:

$$
e_{\text{ramp}}=\lim_{s\to0}s\cdot\frac{s(s+1)}{s^2+s+3}\cdot\frac{30}{s^2}=\frac{30}{3}=10^\circ\text{C}.
$$

The simulation gives $9.97^\circ$C at $t=10$ s. The PI loop tracks a step with zero error and a ramp with a constant lag; P lags the ramp by about $20^\circ$C at the same instant. [Steady-state error and system type](system-type_instructor.md) calls the number 3 the velocity constant.

> **[ DEMO 4 ]** — `ch4/l2_demo4_thermal_pi.py` *(slide)*

![Example 4.5 recomputed: P and PI outputs near 300 C with ±10% plant gain, heater commands, and the PI response to a heater-input disturbance](demos/ch4/figures/l2_demo4_thermal_pi.svg)

### 10.3 What the cancellation hides [beyond the book]

This is the moment of Session B.

The reference response is second order. The system is still third order: the pole at $-0.1$ was cancelled in $D_cG$, not removed from the plant. Ask where a disturbance at the heater input goes:

$$
\frac{Y}{W}=\frac{G}{1+D_cG}
=\frac{100}{(s+1)(s+0.1)}\cdot\frac{s(s+1)}{s^2+s+3}
=\frac{100\,s}{(s+0.1)(s^2+s+3)} .
$$

The slow pole is back. For a unit step at the heater input, the FVT gives $y(\infty)=0$ — integral action still wins — but the route there is slow: the output peaks at $42.0^\circ$C at 1.79 s, is still $12.8^\circ$C at 10 s, $1.71^\circ$C at 30 s (4.1% of the peak) and $0.085^\circ$C at 60 s. The tail decays like $e^{-t/10}$, the plant's own time constant.

#### Instructor script

> In the stability lecture we cancelled an *unstable* pole and watched the hidden mode blow up. This is the legal version: the cancelled pole is stable, so nothing blows up, and the book is right to call the design good. But the mode is not gone. The reference cannot excite it; the disturbance can. When you cancel a slow pole, your tracking gets fast and your disturbance rejection stays slow.

Compare *([Stability and Routh’s criterion §6.3](stability_instructor.md#section-6-3))*, and the near-cancellation of lightly damped poles in Example 3.29 ([Time-domain specifications](time-domain-specs_instructor.md)). The rule is the same in both: the full characteristic polynomial is $(s+0.1)(s^2+s+3)$, and every one of its roots shows up in some input-output pair.

---

## 11. PID control (§4.3.5)

### 11.1 Three knobs, three roots

$$
u(t)=k_Pe(t)+k_I\int_{t_0}^{t}e(\tau)\,d\tau+k_D\dot e(t),
\qquad
D_c(s)=k_P+\frac{k_I}{s}+k_Ds.
\tag{4.74–4.75}
$$

On the motor model, $1+GD_c=0$ gives

$$
s^2+a_1s+a_2+A\left(k_P+\frac{k_I}{s}+k_Ds\right)=0,
$$

and multiplying by $s$ and collecting powers,

$$
\boxed{
s^3+(a_1+Ak_D)s^2+(a_2+Ak_P)s+Ak_I=0
\tag{4.77}
}
$$

Each gain owns one coefficient. $k_D$ sets the $s^2$ coefficient (minus the sum of the roots); $k_P$ sets the $s^1$ coefficient; $k_I$ sets the constant. Three free parameters, three roots: **in principle the roots can be put anywhere.** Without $k_D$, the $s^2$ coefficient is stuck at $a_1$ and the three roots must sum to $-a_1$, whatever $k_P$ and $k_I$ are. That is why the book says PID, not PI, is required for arbitrary dynamics on a second-order plant.

### 11.2 Coefficient matching [beyond the book]

Pick the roots you want, expand them into $s^3+\alpha_1s^2+\alpha_2s+\alpha_3$, and read off the gains:

$$
\boxed{
k_D=\frac{\alpha_1-a_1}{A},
\qquad
k_P=\frac{\alpha_2-a_2}{A},
\qquad
k_I=\frac{\alpha_3}{A}
}
$$

> **Teaching check [beyond the book]:** place the roots at $-1$ and $-1\pm j$ for $A=1$, $a_1=1.4$, $a_2=1$. First, $(s+1)^2+1=s^2+2s+2$. Then $(s+1)(s^2+2s+2)=s^3+3s^2+4s+2$. So $k_D=3-1.4=1.6$, $k_P=4-1=3$, $k_I=2$. These are the gains of Demo 3 (§8.3). The resulting step response has 1.5% overshoot with the derivative on the error. The zeros are not placed by this procedure, and they set the overshoot. Closed-loop poles are not the whole story; see the effect of zeros in [Time-domain specifications](time-domain-specs_instructor.md).

This is pole placement, done by hand. Part IV draws the same idea as a root locus, and Part VI generalises it to state feedback. Problem 4.42(b) asks for it on a real motor.

#### Ask the class

> What is the price of asking for very fast roots this way?

Large $\alpha$'s mean large gains, and large $k_D$ means large noise amplification and a large derivative kick. The algebra puts poles anywhere; the actuator and the sensor decide where you can afford them.

---

## 12. Example 4.6: PID control of motor speed

A DC motor with the parameters of Example 2.15, scaled so that time is in **milliseconds**:

$$
J_m=1.13\times10^{-2},\quad b=0.028,\quad L_a=10^{-1},\quad R_a=0.45,\quad K_t=K_e=0.067 .
\tag{4.78}
$$

With speed $\Omega$ as output, armature voltage as control and a load torque $W$,

$$
\Omega=\frac{K_t}{M(s)}V_a+\frac{L_as+R_a}{M(s)}W,
\qquad
M(s)=(J_ms+b)(L_as+R_a)+K_tK_e .
$$

**[beyond the book]** Numerically $M(s)=0.00113s^2+0.007885s+0.017089$, with open-loop poles at $-3.489\pm1.718j$ ms$^{-1}$. The controller gains are

$$
k_P=3,\qquad k_I=15,\qquad k_D=0.3,
\tag{4.79}
$$

with unused gains zero for P and PI.

![Fig. 4.16(a) — Responses of P, PI and PID control to a step disturbance torque](./book-figures/4-16a.png)
![Fig. 4.16(b) — Responses of P, PI and PID control to a step reference](./book-figures/4-16b.png)

> **[ FIG 4.16 ]** — PDF pp. 53–54 *(slide)*

**Final values under P, by FVT [beyond the book].** The denominator at $s=0$ is $bR_a+K_tK_e+K_tk_P=0.0126+0.00449+0.201=0.2181$:

$$
\Omega_r(\infty)=\frac{K_tk_P}{0.2181}=\frac{0.201}{0.2181}=0.922,
\qquad
\Omega_w(\infty)=\frac{R_a}{0.2181}=\frac{0.45}{0.2181}=2.06 .
$$

These are the two dashed P levels in Fig. 4.16. With PI or PID the integrator forces both to exactly 1 and 0 (§7.4).

> **Teaching check [beyond the book]:** closed-loop roots, in ms$^{-1}$:
>
> | Controller | Roots | $\zeta$ of the pair | peak, reference step | peak, disturbance step |
> |---|---|---|---|---|
> | P | $-3.49\pm13.45j$ | 0.251 | 1.330 | 6.10 |
> | PI | $-4.87$, $-1.06\pm13.48j$ | 0.078 | 1.755 | 5.70 |
> | PID | $-16.26$, $-4.25\pm6.05j$ | 0.575 | 1.126 | 3.16 |
>
> Two things to point at. First, the P pair has the **same real part, $-3.49$, as the open-loop poles** — exactly the vertical slide of §6.2, because $M(s)$ is second order and $k_P$ only adds to its constant term. Second, adding the integrator drags the pair toward the axis ($\zeta$ from 0.25 to 0.08): that is the extra ringing the book describes. Adding the derivative restores the damping and keeps the zero error.

> **[ DEMO 5 ]** — `ch4/l2_demo5_motor_pid.py` *(slide)*

![Example 4.6 recomputed: disturbance and reference step responses under P, PI and PID, with the closed-loop roots](demos/ch4/figures/l2_demo5_motor_pid.svg)

**Source correction [beyond the book]:** Eq. (4.79) prints $k_I=15$ sec and $k_D=0.3$ sec. The two gains cannot both carry units of seconds: relative to $k_P$, $k_I$ has units of inverse time and $k_D$ of time ($T_I=k_P/k_I$ and $T_D=k_D/k_P$ are both times). With the time scaling of footnote 5, the time unit is the millisecond: $T_I=0.2$ ms and $T_D=0.1$ ms.

---

## 13. Disturbance errors: Examples 4.7 and 4.8, by the Final Value Theorem

The book works these two examples in the language of §4.2 (system type, error constants). We have not met that language yet; the FVT gets the same numbers directly, and [Steady-state error and system type](system-type_instructor.md) will name the pattern.

### 13.1 Example 4.7: DC motor position, P and PI

![Fig. 4.6 — DC motor with unity feedback and disturbance torque](./book-figures/4-6.png)

> **[ FIG 4.6 ]** — PDF p. 33 *(the book's text says Fig. 4.4; see the source correction below)*

Plant $A/[s(\tau s+1)]$, disturbance torque entering through $B/A$ at the plant input, and a sensor gain $h$ in place of the unity feedback. With $R=0$ the error is $e=-y$. Solving the loop:

$$
\text{P:}\quad \frac{E}{W}=-\frac{B}{\tau s^2+s+Ak_Ph},
\qquad\qquad
\text{PI:}\quad \frac{E}{W}=-\frac{Bs}{\tau s^3+s^2+Ahk_Ps+Ahk_I}.
\tag{4.82}
$$

For P, a unit step torque gives

$$
\boxed{e(\infty)=-\frac{B}{Ak_Ph}}
$$

a constant offset, even though the plant contains an integrator. The plant's integrator sits after the disturbance, so it helps track the reference but does not reject a constant torque. For a constant reference $r_0$ with $W=0$, however, the stable P loop has $Y/R=Ak_P/(\tau s^2+s+Ak_Ph)\to1/h$ as $s\to0$, so $y(\infty)=r_0/h$ and the system error is $r_0(1-1/h)$. Thus $h\ne1$ makes it Type 0 for reference inputs despite the plant integrator; zero step error requires $h=1$ (see [Steady-state error and system type §11](system-type_instructor.md#section-11), where $H(0)=1$).

For PI, a unit step torque gives $e(\infty)=0$, and a unit **ramp** torque, $W=1/s^2$, gives

$$
\boxed{e(\infty)=\lim_{s\to0}s\cdot\frac{-Bs}{\tau s^3+s^2+Ahk_Ps+Ahk_I}\cdot\frac1{s^2}=-\frac{B}{Ahk_I}}
\tag{4.85}
$$

**[beyond the book]** Both finals need stability. Routh on $\tau s^3+s^2+Ahk_Ps+Ahk_I$ requires $k_P>\tau k_I$ (and all gains positive): the integral gain is limited by the proportional gain and the motor's time constant.

**Source correction [beyond the book]:** Example 4.7 says the motor is "shown in Fig. 4.4"; the motor block diagram is Fig. 4.6 (Fig. 4.4 is the ramp-response sketch). Example 4.7 repeats Example 4.4 of §4.2 with a sensor gain $h$ added. In part (a) the book gives $e_{ss}=-B/Ak_P$, dropping $h$; its own $K_{0,w}=-Ak_Ph/B$ gives $-B/(Ak_Ph)$, as above.

### 13.2 Example 4.8: satellite attitude, PD and PID

![Fig. 4.17(a) — Satellite attitude control, basic system](./book-figures/4-17a.png)
![Fig. 4.17(b) — PD control](./book-figures/4-17b.png)
![Fig. 4.17(c) — PID control](./book-figures/4-17c.png)

> **[ FIG 4.17 ]** — PDF p. 56

Plant $1/(Js^2)$, disturbance torque $W$ at its input. With $R=0$ and $e=-y$:

$$
\text{PD:}\quad \frac{E}{W}=-\frac{1}{Js^2+k_Ds+k_P},
\qquad\qquad
\text{PID:}\quad \frac{E}{W}=-\frac{s}{Js^3+k_Ds^2+k_Ps+k_I}.
\tag{4.86, 4.88}
$$

| Controller | Unit step torque | Unit ramp torque | Stability condition |
|---|---|---|---|
| PD | $e(\infty)=-1/k_P$ | unbounded | $k_P,k_D>0$ |
| PID | $e(\infty)=0$ | $e(\infty)=-1/k_I$ | $k_Dk_P>Jk_I$ (Routh) |

**[beyond the book]** Pure P is not on the list for a reason: $Js^2+k_P$ has roots at $\pm j\sqrt{k_P/J}$, so P alone leaves the satellite oscillating forever. The derivative is what makes this loop stable at all.

**Source correction [beyond the book]:** Eqs. (4.86) and (4.88) are printed without the minus sign that Eq. (4.82) carries. With $E=R-Y$ and $R=0$, $E=-Y$, so both need a leading minus; the steady error to a unit step torque under PD is $-1/k_P$, and the error to a unit ramp torque under PID is $-1/k_I$. The magnitudes in the book are right.

#### Say out loud

> The satellite with PD tracks a step command perfectly — the plant has two integrators in the path from controller to output — yet sits at a constant angle error when a constant torque pushes on it. Whether a loop has zero error depends on **which input** you ask about and **where the integrators are** relative to it. [Steady-state error and system type](system-type_instructor.md) turns that sentence into a table.

---

## 14. What each term does

**[beyond the book]** The standard summary table, with its honest caveat: these are tendencies on well-behaved plants, not theorems. Example 4.6 has already shown integral action *reducing* damping, and §6.4 said that higher-order plants break the tidy pattern.

| Increase | Rise time | Overshoot | Settling time | Steady-state error to a step | Stability margin |
|---|---|---|---|---|---|
| $k_P$ | decreases | increases | small change | decreases (never zero with P alone if $G(0)$ is finite) | usually decreases |
| $k_I$ | decreases | increases | increases | **eliminated** | decreases |
| $k_D$ | small change | decreases | decreases | no effect | usually increases (until noise and lag dominate) |

$$
\boxed{
\begin{array}{l}
\text{P: accuracy for damping.}\\
\text{I: zero constant error if internally stable and }G(0)\ne0\text{; costs speed and stability.}\\
\text{D: damping; says nothing about the final value; amplifies noise.}\\
\text{PID on a second-order plant: three gains place three roots.}
\end{array}}
$$

---

## 15. Closing script

> At the start of last session the controller box was empty. Now it has three terms, and you know what each one is for.
>
> Proportional action is the reflex: push back in proportion to the error. It helps, but on a plant with finite DC gain it needs an error to keep pushing, so it never finishes the job. The exception is a plant with its own integrator, like the motor-position loop, which finishes the job under P alone.
>
> Integral action is the memory. It keeps pushing until the error is exactly zero, and it does that without knowing anything about the plant — which is why it is in almost every process controller and motor drive. Its price is stability and speed, and, on real hardware, windup.
>
> Derivative action is the prediction. It adds damping, it cannot finish anything on its own, and it hears every bit of sensor noise.
>
> Two loose ends. We have been computing steady-state errors one example at a time. Next lecture turns that into a classification — system type — that tells you the answer by counting integrators. And we have picked gains by hand. The lecture after that shows how practising engineers tune them from a single experiment, and what to add so that an integrator survives a saturating actuator.

---

# Part II — Materials

## 16. One-board summary

```text
   THE LAW          u = kP e + kI INTEGRAL(e) + kD de/dt
                    Dc(s) = kP + kI/s + kD s  =  kP (1 + 1/(TI s) + TD s)

   ON  G = A/(s^2 + a1 s + a2)

     P     s^2 + a1 s + (a2 + A kP)         wn up, sigma = a1/2 FIXED (if underdamped)
           e(inf) = 1/(1 + kP G(0))          never zero (G(0) finite); zeta falls

     I     s^3 + a1 s^2 + a2 s + A kI       stable iff 0 < kI < a1 a2 / A
           e(inf) = 0, u(inf) = 1/G(0)       G(0) nonzero; loop internally stable
           why: u settles => du/dt = kI e = 0 => e = 0

     D     never alone: T(0) = 0             adds damping, amplifies noise
           kP e + kD e' ~ kP e(t + TD)       "anticipation"
           D on error vs D on output: same poles, different zeros, no kick

     PID   s^3 + (a1 + A kD) s^2 + (a2 + A kP) s + A kI
           three gains, three coefficients, three roots: place them anywhere

   EXAMPLE 4.5 (thermal, poles -1 and -0.1)
     P   kP = 0.03            offset 300/31 = 9.7 C, zeta = 0.31
     PI  + kI = 0.003         zero at -0.1 cancels the slow pole
                              reference: 3/(s^2 + s + 3), ts = 13.4 s
                              disturbance: 100 s / [(s + 0.1)(s^2 + s + 3)]
                              -> the 10 s tail is still there

   DISTURBANCE AT THE PLANT INPUT (R = 0, e = -y)
     motor P     e = -B/(A kP h)         PI   step 0, ramp -B/(A h kI)
     satellite PD  e = -1/kP             PID  step 0, ramp -1/kI
```

## 17. Discussion questions

1. Proportional control of the motor model cannot change the decay rate $\sigma=a_1/2$. Name a physical change to the motor that would, and say which coefficient it moves.
2. The argument in §7.4 says an integrator forces $e\to0$ whenever the loop settles. Give two ways the loop can fail to settle in practice, one linear and one nonlinear.
3. A household thermostat is an on-off device with no integrator, yet a house does not sit 2°C below the setpoint. How does it regulate? (Think about switching and hysteresis.) Does the temperature converge to zero error, or does it cycle? What would you need to add to get true zero steady-state error?
4. In Example 4.5 the PI zero was placed on the slow plant pole. What happens to the reference and disturbance responses if the true $\tau_2$ is 12 s instead of 10?
5. With the derivative on the output (Fig. 4.10a), the step response of §8.3 overshoots more than with the derivative on the error. When would you still choose (a)?
6. PID can place three roots anywhere on a second-order plant. What limits how far left you can put them?
7. The satellite of Example 4.8 tracks a step command with zero error under PD, but not a step torque. Explain the difference without equations.

## 18. Homework and follow-up problems

| Problem | Topic | Why this one |
|---|---|---|
| 4.34 | P, PD and PI to stabilise a given loop | One plant, three controllers; part (d) previews [Steady-state error and system type](system-type_instructor.md). |
| 4.35 | P for a damping target, PI for no overshoot, PID for settling time | Converts specifications into gains; stability ranges with Routh. |
| 4.36 | Liquid-level control: P, PI, PD, PID against time specifications | Same tasks on a different plant. |
| 4.37 | Process control: PI and PID against rise time, overshoot and peak time | Good practice at "which term fixes which spec". |
| 4.38 | Multiple-integrator plants $1/s^n$ | Why P fails for $n=2$ (§13.2) and what is needed beyond. |
| 4.39(d–e) | Generator speed: PD, then how to remove a disturbance error | Disturbance rejection, and the case for integral action. |
| 4.42 | DC motor speed with PI: place the closed-loop roots | Coefficient matching (§11.2) on a real motor. |
| Review Questions 4.8–4.10 | Objectives of I and D; D in the feedback path | Short written answers. |

Problems 4.40–4.41 and 4.43–4.44 are framed in system-type language; hold them for [Steady-state error and system type](system-type_instructor.md).

**Suggested additional exercise [beyond the book]:** in `l2_demo4_thermal_pi.py`, change $\tau_2$ to 12 s while keeping $k_I/k_P=0.1$. Report the new closed-loop roots and describe what happens to the reference response.

## 19. Instructor cautions

1. **State the stability proviso every time you use the FVT.** Integral action needs a nonzero plant DC gain for zero constant tracking error, and every internal mode must be stable; a cancelled mode at the origin does not qualify. State these assumptions when using the zero-error result.
2. **P control on the second-order plant moves $\omega_n$, not $\sigma$.** Students expect more gain to mean faster settling. On this plant it does not; show the pole column of §6.2.
3. **Do not let "integral removes error" become "integral removes all error."** A ramp still leaves a constant lag (§10.2), and a double-integrator disturbance defeats a single integrator. [Steady-state error and system type](system-type_instructor.md) organises this.
4. **Derivative control is never used alone,** and an unfiltered derivative is never implemented. Mention the filter now; [PID tuning and implementation](pid-tuning_instructor.md) does it properly.
5. **The Fig. 4.10 choice is about the actuator.** Moving D to the feedback path removes the kick; it does not automatically improve the output response (§8.3).
6. **A cancellation is not a removal.** Example 4.5's cancelled pole returns in the disturbance response (§10.3). This is the stable counterpart of *([Stability and Routh’s criterion §6.3](stability_instructor.md#section-6-3))*.
7. **Watch the units in Example 4.6:** time is in milliseconds, and the book's units on $k_I$ and $k_D$ are inconsistent (§12).
8. **Examples 4.7 and 4.8 lean on §4.2, which comes next in this course.** Present them with the FVT and treat the words "Type 0" and "Type 1" as previews.

## 20. Source corrections collected

1. **Example 4.6, Eq. (4.79):** $k_I=15$ and $k_D=0.3$ cannot both carry units of seconds; $T_I=k_P/k_I=0.2$ ms and $T_D=k_D/k_P=0.1$ ms in the scaled time. (§12)
2. **Example 4.7:** the motor diagram is Fig. 4.6, not Fig. 4.4; and the step-torque error is $-B/(Ak_Ph)$, not $-B/(Ak_P)$. (§13.1)
3. **Example 4.8, Eqs. (4.86) and (4.88):** missing leading minus sign; errors are $-1/k_P$ (PD, step torque) and $-1/k_I$ (PID, ramp torque). (§13.2)

Rounded values in the book that check out: Example 4.5's $\zeta=0.3$ is 0.312, and its $10^\circ$C offset is $9.68^\circ$C.

## 21. Demonstration index

| # | Script | Section | What it settles | Use |
|---|---|---|---|---|
| 1 | `l2_demo1_proportional.py` | §6.2 | Fig. 4.7 recomputed; error falls as $1/(1+k_P)$ while the poles slide vertically along $\Re s=-0.7$. | **live** |
| 2 | `l2_demo2_integral.py` | §7 | Figs. 4.8–4.9; zero error and exact disturbance cancellation for three different plants; the Routh limit $k_I<1.4$. | **live** |
| 3 | `l2_demo3_derivative_placement.py` | §8.3, §11.2 | Coefficient matching gives $k_P=3$, $k_I=2$, $k_D=1.6$; derivative on the error versus on the output: same poles, different zeros, and an 83-unit kick. | **live** |
| 4 | `l2_demo4_thermal_pi.py` | §10 | Example 4.5: open loop 47.1 s, P offset 9.68°C, PI settling 13.44 s, all at ±10% $K_o$; the 10 s tail in the disturbance response. | slide |
| 5 | `l2_demo5_motor_pid.py` | §12 | Example 4.6: Fig. 4.16 recomputed with the closed-loop roots; P's pair keeps the open-loop real part. | slide |

## 22. Where this lecture sits

| Lecture | Book sections | Content |
|---|---|---|
| [Feedback properties](feedback-properties_instructor.md) | 4.1 | The basic equations of feedback: tracking, regulation, sensitivity |
| **This lecture** | **4.3.1–4.3.5** | **P, I, D, PI and PID control actions** |
| [Steady-state error and system type](system-type_instructor.md) | 4.2 | System type, error constants, disturbance type |
| [PID tuning and implementation](pid-tuning_instructor.md) | 4.3.6, 4.4, 9.3.1 | Ziegler–Nichols tuning, feedforward, anti-windup, physical realisation |
