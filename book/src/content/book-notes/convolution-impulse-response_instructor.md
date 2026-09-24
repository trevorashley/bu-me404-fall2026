# Dynamic Response I — Convolution, Transfer Functions, and the Laplace Toolkit
## FPE 8th ed., Section 3.1

**Audience:** Fourth-year undergraduate mechanical engineering (ME 404), after Chapter 2 modeling

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., §3.1. Numbered examples follow the book; §10.3 groups the initial-value examples before the Final Value Theorem for teaching purposes. Clarifications and classroom checks supplement the source.

**Prerequisite:** the earlier lecture [From Physical Models to the Laplace Transform](modeling-and-dynamics_instructor.md). That lecture arrived at $e^{st}$, the characteristic polynomial, poles as natural rates, and zeros as blocked transmission, all from physical models. This one supplies the machinery the textbook builds on top of it: superposition, convolution, the transform table, partial fractions, and the Final Value Theorem. Cross-references to it are written *(0.0.8 §n)*, meaning section n of that lecture.

**Duration:** 75 minutes. See §3 for the route and for what to prepare as slides.

**Math rendering:** `$ ... $` inline and `$$ ... $$` display, as in [From Physical Models to the Laplace Transform](modeling-and-dynamics_instructor.md).

**Book figures:** figure numbers refer to the source chapter at

```text
references/documents/Franklin, Powell, Emami-Naeimi - 8th Ed./3 - Dynamic Response.pdf
```

Page cues below use the PDF viewer's 1-based page numbers (202 pages). Project the figures directly from this PDF; extracted image files are not supplied. **[beyond the book]** Classroom checks and teaching prompts are instructor additions. Demo paths are relative to `demos/`; the demonstration index lists the scripts.

**Notation used throughout (the book's, with one warning):**

| Symbol | Meaning |
|---|---|
| $1(t)$ | unit step: $0$ for $t<0$, $1$ for $t\ge0$ |
| $\delta(t)$ | unit impulse, defined by Eqs. (3.9)–(3.11) |
| $h(t)$ | unit impulse response |
| $H(s)$, $G(s)$ | transfer function; $H(s)=\mathcal L\{h(t)\}$ |
| $u(t),\ y(t)$ | input and output signals; $U(s),\ Y(s)$ their transforms |
| $s=\sigma_1+j\omega$ | the transform variable, §3.1.3 |
| $*$ | convolution |
| $\mathcal L$ | the one-sided ($\mathcal L_-$) transform, lower limit $0^-$ |

> **Warning about $\sigma$, worth stating out loud in §6 below.** In §3.1 the book writes $s=\sigma_1+j\omega$, so $\sigma_1$ is the real part of $s$. In §3.3 it writes a stable pole as $s=-\sigma\pm j\omega_d$ with $\sigma=\zeta\omega_n>0$, so there $\sigma$ is *minus* the real part. Both conventions appear in this chapter and in the next lecture. Say which one is on the board.

---

# Part 0 — Planning

## 1. Teaching strategy

Students arrive having seen $x=Ae^{st}$ turn differential equations into algebra. The question this lecture answers is the one that follows immediately:

> **Why is that one substitution enough? What is it about linear time-invariant systems that makes a single exponential test tell us everything?**

The book's answer is in its first two sentences of §3.1, and the whole lecture is an unpacking of them:

1. A linear system obeys **superposition**.
2. The response of an LTI system is the **convolution** of the input with the unit impulse response.

From (2) it follows in one line that an exponential input gives an exponential output scaled by $H(s)$. Convolution is therefore not a detour on the way to transforms. It is the reason transforms work.

Three moments are worth protecting:

1. **§6** — the convolution integral collapses to a multiplication, $Y(s)=H(s)U(s)$. This is the payoff for the whole first half.
2. **§7** — the frequency response is read off $H(j\omega)$, and the transient that the frequency response does not describe is visible beside it.
3. **§11–§12** — the Final Value Theorem, and the example where applying it without checking gives a confident wrong answer.

A framing line for the lecture:

> **Everything today is one identity seen from four sides: $y=h*u$ in time, $Y=HU$ in $s$, $AM\cos(\omega t+\varphi)$ at a single frequency, and a table lookup at the end.**

---

## 2. Learning objectives

By the end of this lecture students should be able to:

1. Test a differential equation for linearity and time invariance, as in Examples 3.1 and 3.2, and say what each property buys.
2. Build the convolution integral from a train of short pulses, and state the sifting property of the impulse.
3. Compute the impulse response of a first-order system by integrating across $t=0$ (Example 3.3).
4. Derive $y(t)=H(s)e^{st}$ for an exponential input, and give the three equivalent definitions of the transfer function: exponential gain, ratio of transforms at zero initial conditions, and transform of the impulse response.
5. Write down a transfer function by inspection from a constant-coefficient ODE (Eq. 3.26).
6. Obtain amplitude ratio and phase from $H(j\omega)$, and separate the steady-state sinusoid from the switch-on transient (Examples 3.6, 3.7).
7. State the $\mathcal L_-$ definition, explain the $0^-$ lower limit, and derive the transforms of the step, ramp, impulse and sinusoid.
8. Apply the transform properties of §3.1.4, especially differentiation, integration, time delay and convolution.
9. Expand a rational $Y(s)$ with distinct poles by the cover-up method and invert it from the table (Example 3.11).
10. Apply the Final Value Theorem, state its hypothesis, and identify cases where it fails (Examples 3.12–3.14).
11. Solve an initial-value problem by transform, splitting the answer into zero-input and zero-state parts (Examples 3.15–3.17).
12. Define poles and zeros of a rational transfer function, count zeros at infinity, and explain why a pole-zero cancellation deserves suspicion.

---

## 3. Suggested lecture flow (75 minutes)

| Time | Topic | Section |
|---:|---|---|
| 0–5 min | Where we are; the two properties that make §3.1 work | §4 |
| 5–20 min | Superposition, time invariance, impulse response, convolution | §4–§5 |
| 20–30 min | Convolution $\rightarrow$ transfer function; three definitions; RC example | §6 |
| 30–40 min | Frequency response; transient versus steady state | §7 |
| 40–50 min | The $\mathcal L_-$ transform, four transform pairs, the properties table | §8–§9 |
| 50–60 min | Partial fractions by cover-up; the five-step procedure | §10 |
| 60–68 min | Final Value Theorem, DC gain, and the trap | §11 |
| 68–75 min | Poles and zeros; computer tools; closing | §12–§14 |

**Prepare as slides:** the convolution build-up figures (Figs. 3.1 and 3.2), the frequency-response plots (Figs. 3.4 and 3.5), the transform-pair and properties tables, and the satellite pulse figures (Figs. 3.7 and 3.8). Derive on the board only: the pulse-train limit, the exponential-input calculation, the cover-up method, and the Final Value Theorem statement.

**Core route:** teach Example 3.11 in §10.2 and assign §10.3 (Examples 3.15–3.17) as follow-up. Keep §11 and §12 intact. The twelve objectives describe the lecture plus that follow-up, not twelve separate live derivations.

### Runnable demonstrations

Four Python demos live in `demos/ch3/`. They import `demos/demokit.py` through `ch3/kit.py`. The Python environment needs NumPy, SciPy, and Matplotlib.

```
cd demos
uv run python ch3/l1_demo1_convolution.py          # one demo
uv run python ch3/l1_demo1_convolution.py --show   # interactive window
uv run python ch3/run_all.py                       # every chapter-3 figure (runtime depends on the machine)
```

**Run Demo 1 and Demo 2 live.** The first shows a sum of weighted, shifted impulse responses converging to the convolution integral; the second shows the transient that the frequency response leaves out. Demos 3 and 4 work as prepared figures.


### Teaching scope

Use the demos for the selected live examples; the accompanying checks also work on the board. For a 75-minute session, select the protected examples in §1; assign the remaining worked examples and optional computations as follow-up reading. Do not try to present every figure and derivation live.

---

# Part I — The lecture

## 4. Opening: the two properties that everything rests on

### Instructor script

> Last time we asked what exponential motions a physical system allows, and we got poles. Today I want to ask why that question was enough.
>
> The book opens Section 3.1 with two statements about linear time-invariant systems. Everything in the chapter follows from them.
>
> First: **superposition**. If I know the response to $u_1$ and the response to $u_2$, I know the response to any combination $\alpha_1u_1+\alpha_2u_2$.
>
> Second: **convolution**. The response to *any* input is the input convolved with the response to a single impulse.
>
> Put them together and you get something remarkable: the ideal impulse response determines every response from rest within the LTI model. In an experiment, keep the pulse small enough that the model remains linear.

### 4.1 Superposition (Example 3.1)

**Standing assumption:** transfer functions and convolution describe the **zero-state** response of a causal LTI system. With nonzero initial conditions, add the zero-input response. Superposition holds for input/initial-state pairs; fixing the same nonzero initial state for every input generally gives an affine, rather than linear, input-output map.

Take the first-order system

$$
\dot y+ky=u .
$$

Let $u=\alpha_1u_1+\alpha_2u_2$ and try $y=\alpha_1y_1+\alpha_2y_2$. Substituting,

$$
\alpha_1\dot y_1+\alpha_2\dot y_2+k(\alpha_1y_1+\alpha_2y_2)=\alpha_1u_1+\alpha_2u_2,
$$

which regroups as

$$
\boxed{
\alpha_1\left(\dot y_1+ky_1-u_1\right)+\alpha_2\left(\dot y_2+ky_2-u_2\right)=0 .
\tag{3.1}
}
$$

If $y_1$ solves the equation with input $u_1$ and $y_2$ with $u_2$, both brackets vanish and the combination is a solution.

#### Ask the class

> Where in that argument did we use the fact that $k$ is constant?

Nowhere. Superposition survives a time-varying $k(t)$. That is the point of the next example.

### 4.2 Time invariance (Example 3.2)

Now allow $k=k(t)$, delay the input by $\tau$, and ask whether the output is simply delayed too. Let $y_1$ solve the original equation,

$$
\dot y_1(t)+k(t)y_1(t)=u_1(t),
\tag{3.2}
$$

and assume the response to $u_2(t)=u_1(t-\tau)$ is $y_2(t)=y_1(t-\tau)$. By the chain rule, $\dot y_2(t)=\dot y_1(t-\tau)$, so substituting into $\dot y_2+k(t)y_2=u_1(t-\tau)$ gives

$$
\dot y_1(t-\tau)+k(t)y_1(t-\tau)=u_1(t-\tau).
$$

With $\eta=t-\tau$, so that $t=\eta+\tau$,

$$
\frac{dy_1(\eta)}{d\eta}+k(\eta+\tau)y_1(\eta)=u_1(\eta).
\tag{3.3}
$$

Eq. (3.2) evaluated at time $\eta$ says $dy_1/d\eta+k(\eta)y_1(\eta)=u_1(\eta)$. Subtracting it from Eq. (3.3):

$$
\left[k(\eta+\tau)-k(\eta)\right]y_1(\eta)=0 .
$$

For a nonzero response, invariance under **every** time shift $\tau$ therefore requires

$$
\boxed{k(\eta+\tau)=k(\eta)=k,\quad\text{a constant.}}
$$

So: **linearity gives superposition; constant coefficients give shift invariance.** Both are needed for what follows.

---

## 5. The impulse response and the convolution integral

### 5.1 Chopping the input into pulses

> **[ FIG 3.1 ]** — PDF p. 10, PDF p. 10, PDF p. 10, PDF p. 11
> **[ FIG 3.2 ]** — PDF p. 11
>
> **Show:** the four panels of Fig. 3.1 in order — one pulse and its response; the same pulse delayed; two pulses added; four pulses added. Then Fig. 3.2, a general signal drawn as a staircase of pulses.
> **Say:** "Panel (a) is one experiment. Panel (b) is time invariance. Panels (c) and (d) are superposition. There is no third idea coming."

Define the unit-area pulse

$$
p_\Delta(t)=
\begin{cases}
\dfrac1\Delta, & 0\le t\le\Delta\\[4pt]
0,&\text{elsewhere}
\end{cases}
\tag{3.4}
$$

and let $h_\Delta(t)$ be the system's response to it. Scaling by $\Delta u(k\Delta)$ and shifting by $k\Delta$, superposition gives the total response

$$
\boxed{
y_\Delta(t)=\sum_{k=0}^{\infty}\Delta\,u(k\Delta)\,h_\Delta(t-k\Delta)
\tag{3.5}
}
$$

Here $y_\Delta$ is the exact response to the staircase approximation of the input, not yet the exact response to $u$. Now let $\Delta\to0$. The pulse becomes taller and narrower at constant area; its impulse limit is a distributional limit, not pointwise convergence to an ordinary function:

$$
\lim_{\Delta\to0}p_\Delta(t)=\delta(t),
\qquad
\lim_{\Delta\to0}h_\Delta(t)=h(t),
\tag{3.6, 3.7}
$$

and the sum becomes an integral:

$$
\boxed{
y(t)=\int_0^\infty u(\tau)h(t-\tau)\,d\tau
\tag{3.8}
}
$$

> **[ DEMO 1 ]** — `ch3/l1_demo1_convolution.py` *(live, ~20 s)*
>
> **Teaching check [beyond the book]:** Demo 1 uses $\Delta\,u(k\Delta)h(t-k\Delta)$, an impulse-quadrature approximation to convolution. At finite $\Delta$, this differs from the exact finite-pulse response $h_\Delta$ in Eq. (3.5). Compare it with the ODE solution. Halve the pulse width and check convergence; first-order error scaling is an asymptotic expectation, not an exact halving at every step.

![Weighted impulse responses converging to the response of a first-order system](demos/ch3/figures/l1_demo1_convolution.svg)

### 5.2 The impulse and its sifting property

Dirac's definition:

$$
\delta(t)=0\ \ (t\ne0),
\qquad
\int_{-\infty}^{\infty}\delta(t)\,dt=1 .
\tag{3.9, 3.10}
$$

The property that does the work:

$$
\boxed{
\int_{-\infty}^{\infty}f(\tau)\delta(t-\tau)\,d\tau=f(t)
\tag{3.11}
}
$$

#### Instructor script

> The book's motivation for this is a baseball. The bat is in contact with the ball for a millisecond or so, and during that millisecond the ball deforms, the bat flexes, and the contact mechanics are genuinely complicated. None of that matters for the trajectory. What matters is the momentum delivered.
>
> An impulse is the mathematical version of that summary: something intense and brief, described only by the area under it.
>
> And read Eq. (3.11) backwards. It says any signal *is* a sum of impulses. So if I know the response to one impulse, superposition gives me the rest.

### 5.3 Example 3.3: the impulse response by integrating across zero

Take $\dot y+ky=\delta(t)$ with $y(0^-)=0$. Integrate from just before zero to just after:

$$
\int_{0^-}^{0^+}\dot y\,dt+k\int_{0^-}^{0^+}y\,dt=\int_{0^-}^{0^+}\delta(t)\,dt .
$$

The middle term is the integral of a bounded function over a vanishing interval, so it is zero. The rest gives

$$
y(0^+)-y(0^-)=1
\qquad\Longrightarrow\qquad
y(0^+)=1 .
$$

For $t>0$ the equation is homogeneous, $\dot y+ky=0$. Substituting $y=Ae^{st}$ gives $(s+k)Ae^{st}=0$, so $s=-k$. Then $y(0^+)=A=1$ — exactly the argument of the earlier lecture *(0.0.8 §5.2)*. Since $y=0$ for $t<0$, the result is

$$
\boxed{
h(t)=e^{-kt}1(t)
}
$$

#### Ask the class

> The impulse did not change the shape of the response. What did it change?

The initial condition. **An impulse can set an initial state.** For this first-order system, its subsequent motion is a free response. In a higher-order system one input impulse excites a particular combination of states, not every possible initial state. Direct feedthrough can also put an impulse in the output at $t=0$.

### 5.4 Causality and the limits of integration

For a time-invariant system the general input gives

$$
y(t)=\int_{-\infty}^{\infty}u(\tau)h(t-\tau)\,d\tau
=\int_{-\infty}^{\infty}h(\tau)u(t-\tau)\,d\tau .
\tag{3.12, 3.13}
$$

If $h(\tau)\ne0$ for $\tau<0$, the response can begin before the input does. Such systems are called **non-causal**. For a causal system, $h(t)=0$ for $t<0$. With an input that also vanishes before zero and zero initial state, this gives

$$
\boxed{
y(t)=\int_0^t u(\tau)h(t-\tau)\,d\tau
\tag{3.15}
}
$$

---

## 6. From convolution to the transfer function

### 6.1 The one-line consequence

Put $u(t)=e^{st}$ into Eq. (3.13):

$$
y(t)=\int_{-\infty}^{\infty}h(\tau)e^{s(t-\tau)}\,d\tau
=e^{st}\underbrace{\int_{-\infty}^{\infty}h(\tau)e^{-s\tau}\,d\tau}_{\textstyle H(s)} .
$$

Therefore

$$
\boxed{
u(t)=e^{st}
\quad\Longrightarrow\quad
y(t)=H(s)e^{st},
\qquad
H(s)=\int_{-\infty}^{\infty}h(\tau)e^{-s\tau}\,d\tau
\tag{3.17, 3.18}
}
$$

### Instructor script

> Look at what just happened. The exponential came out of the integral untouched, because shifting an exponential only rescales it: $e^{s(t-\tau)}=e^{st}e^{-s\tau}$.
>
> So an exponential in gives the same exponential out, multiplied by a complex number. Not a different frequency, not a different shape. One number.
>
> That number is the transfer function, and the integral defining it is the Laplace transform of the impulse response.
>
> Two footnotes the book is careful about, and so should we be. This input has been running since $t=-\infty$, so there are no initial conditions and no transient — Eq. (3.17) is the steady-state, particular solution. And the integral does not converge for every $s$.

**Qualification:** the convolution eigenfunction statement holds where the integral converges. Algebraic substitution also gives a particular solution when $s$ is not a pole, but it need not be an attracting steady state. At a pole, the trial form fails and resonance introduces factors such as $te^{st}$. For an exponential switched on at zero, include the switch-on transient.

### 6.2 Example 3.4

For $\dot y+ky=u=e^{st}$, assume $y=H(s)e^{st}$, so $\dot y=sH(s)e^{st}$ and

$$
sH(s)e^{st}+kH(s)e^{st}=e^{st}
\qquad\Longrightarrow\qquad
\boxed{H(s)=\frac1{s+k}} .
$$

Note what was *not* required: the integral in Eq. (3.18) was never evaluated. Substituting the assumed exponential form into the differential equation is enough, which is exactly the procedure of the earlier lecture *(0.0.8 §8)*.

### 6.3 Three definitions of the same object

Write them side by side on the board and insist they are one thing.

$$
\boxed{
\begin{array}{ll}
\textbf{1. Exponential gain} & u=e^{st}\ \Rightarrow\ y=H(s)e^{st}\\[4pt]
\textbf{2. Ratio of transforms} & \dfrac{Y(s)}{U(s)}=H(s)\ \ \text{with all initial conditions zero}\\[8pt]
\textbf{3. Transform of }h & H(s)=\mathcal L\{h(t)\}
\end{array}}
$$

Definition 3 follows because $\mathcal L\{\delta\}=1$: feed in an impulse and $Y(s)=H(s)\cdot1$.

For causal inputs from rest, taking the transform of the convolution gives $Y=HU$ directly (property 7 in §9). Definition 1 uses the convergence/particular-solution qualification above; it does not say every switched exponential produces only one exponential.

### 6.4 Writing a transfer function by inspection

For

$$
\frac{d^3y}{dt^3}+a_1\ddot y+a_2\dot y+a_3y=b_1\ddot u+b_2\dot u+b_3u ,
\tag{3.24}
$$

transform with zero initial conditions — each $d/dt$ becomes an $s$ — to get

$$
(s^3+a_1s^2+a_2s+a_3)Y(s)=(b_1s^2+b_2s+b_3)U(s),
$$

so

$$
\boxed{
H(s)=\frac{b_1s^2+b_2s+b_3}{s^3+a_1s^2+a_2s+a_3}=\frac{b(s)}{a(s)}
\tag{3.26}
}
$$

**The left side of the ODE becomes the denominator; the right side becomes the numerator.** In this ODE form, derivatives of the *input* are what produce zeros. More generally, zeros also depend on which output is measured, as Example 3.19 in §13 shows. That is a sentence to repeat in the next lecture when zeros start moving the response around.

### 6.5 Example 3.5: the RC circuit

> **[ FIG 3.3 ]** — PDF p. 24 *(slide: the circuit)*

With $u$ the source voltage and $y$ the capacitor voltage, Kirchhoff's voltage law around the loop is $u=Ri+y$. The capacitor current is $i=C\dot y$, so

$$
RC\dot y+y=u .
$$

Transform using property 5 of §9, $\mathcal L\{\dot y\}=sY(s)-y(0^-)$, with $y(0^-)=0$:

$$
RC\,sY(s)+Y(s)=U(s)
\quad\Longrightarrow\quad
(RCs+1)Y(s)=U(s)
\qquad\Longrightarrow\qquad
\boxed{H(s)=\frac{1}{RCs+1}}
$$

To invert, divide the numerator and denominator by $RC$ so the denominator has leading coefficient 1:

$$
H(s)=\frac{1/(RC)}{s+1/(RC)} .
$$

Since $\mathcal L\{e^{-at}1(t)\}=1/(s+a)$, which is the step transform with the frequency shift of property 4, the impulse response is

$$
h(t)=\frac1{RC}e^{-t/(RC)}1(t) .
$$

This is the same first-order lag as the thermal body of the earlier lecture *(0.0.8 §5.4)*, with $\tau=RC$ again. Say so — students should leave with one first-order system in their heads, not three.

---

## 7. Frequency response

### 7.1 Two exponentials make a cosine

Euler's relation splits a cosine into exponentials, and each one is a case of Eq. (3.17):

$$
A\cos\omega t=\frac A2\left(e^{j\omega t}+e^{-j\omega t}\right)
\quad\Longrightarrow\quad
y(t)=\frac A2\left[H(j\omega)e^{j\omega t}+H(-j\omega)e^{-j\omega t}\right].
\tag{3.27}
$$

For a real system, write $H(j\omega)=M(\omega)e^{j\varphi(\omega)}$. The two terms are conjugates, so their sum is real. For an input applied since $t=-\infty$, or for a stable system once the switch-on transient has decayed, the output is

$$
\boxed{
y(t)=AM\cos(\omega t+\varphi),
\qquad
M=|H(j\omega)|,
\qquad
\varphi=\angle H(j\omega)
\tag{3.28}
}
$$

This is the conjugate-pair argument of *(0.0.8 §7.5)* used for a second purpose: there it recovered real free motion, here it recovers a real forced response.

### 7.2 Examples 3.6 and 3.7

**Example 3.6.** For $H(s)=1/(s+k)$, set $s=j\omega$:

$$
H(j\omega)=\frac1{k+j\omega} .
$$

The magnitude of a quotient is the quotient of the magnitudes, and its angle is the difference of the angles. The numerator is $1$, with magnitude $1$ and angle $0$. The denominator has magnitude $\sqrt{k^2+\omega^2}$ and angle $\tan^{-1}(\omega/k)$, since $k>0$ puts it in the right half plane. Therefore

$$
M=|H(j\omega)|=\frac1{\sqrt{\omega^2+k^2}},
\qquad
\varphi=\angle H(j\omega)=0-\tan^{-1}(\omega/k)=-\tan^{-1}(\omega/k) .
$$

Equivalently, multiply by the conjugate: $H(j\omega)=\dfrac{k-j\omega}{k^2+\omega^2}$. The real part is positive and the imaginary part is negative, so the phase lies between $0$ and $-90^\circ$. With $k=1$, the book plots these two curves:

> **[ FIG 3.4 ]** — PDF p. 28 *(slide: magnitude and phase, log-log and semi-log)*
>
> **Say:** "Plotted on logarithmic axes this way, these are Bode plots, and Chapter 6 is about reading them. For now, notice only that a single complex-valued function of $\omega$ carries both curves."

**Example 3.7.** Now, with $k=1$, switch the input on at $t=0$: $u(t)=\sin(10t)1(t)$, with the system at rest. From the table in §8.2, $U(s)=10/(s^2+100)$, so

$$
Y(s)=H(s)U(s)=\frac{1}{s+1}\cdot\frac{10}{s^2+100}=\frac{10}{(s+1)(s^2+100)} .
$$

*Step 1: set up the expansion.* The quadratic has complex roots $\pm10j$. To keep the arithmetic real, give it a first-order numerator:

$$
\frac{10}{(s+1)(s^2+100)}=\frac{A}{s+1}+\frac{Bs+C}{s^2+100} .
$$

*Step 2: cover-up for the real pole.*

$$
A=\left.\frac{10}{s^2+100}\right|_{s=-1}=\frac{10}{101} .
$$

*Step 3: match coefficients for $B$ and $C$.* Multiply through by $(s+1)(s^2+100)$:

$$
10=A(s^2+100)+(Bs+C)(s+1)=(A+B)s^2+(B+C)s+(100A+C) .
$$

$$
s^2:\ A+B=0\ \Rightarrow\ B=-\frac{10}{101};
\qquad
s^0:\ 100A+C=10\ \Rightarrow\ C=10-\frac{1000}{101}=\frac{10}{101};
\qquad
s^1:\ B+C=0\ \checkmark
$$

The $s^1$ equation is left over as a check. Hence

$$
Y(s)=\frac{10}{101}\left[\frac{1}{s+1}-\frac{s}{s^2+100}+\frac1{10}\cdot\frac{10}{s^2+100}\right].
$$

*Step 4: invert term by term.* Use $e^{-t}\leftrightarrow1/(s+1)$, $\cos10t\leftrightarrow s/(s^2+100)$ (derived in §8.2), and $\sin10t\leftrightarrow10/(s^2+100)$:

$$
y(t)=\frac{10}{101}e^{-t}+\frac{1}{101}\left(\sin10t-10\cos10t\right),\qquad t\ge0 .
$$

*Step 5: combine the sinusoids.* Write $a\sin\theta+b\cos\theta=\sqrt{a^2+b^2}\,\sin(\theta+\varphi)$ with $\cos\varphi=a/\sqrt{a^2+b^2}$ and $\sin\varphi=b/\sqrt{a^2+b^2}$. Here $a=1$ and $b=-10$. The amplitude is $\sqrt{101}/101=1/\sqrt{101}$. Also $\cos\varphi>0$ and $\sin\varphi<0$, so $\varphi$ is in the fourth quadrant and $\varphi=-\tan^{-1}(10)$:

$$
\boxed{
y(t)=\underbrace{\tfrac{10}{101}e^{-t}}_{\text{transient}}
+\underbrace{\tfrac{1}{\sqrt{101}}\sin(10t+\varphi)}_{\text{steady state}}},
\qquad
\varphi=-\tan^{-1}(10)\approx-84.29^\circ .
$$

The steady-state part matches Eq. (3.28): $M(10)=1/\sqrt{101}$ and $\varphi(10)=-\tan^{-1}10$, from Example 3.6 with $\omega=10$ and $k=1$.

**Source correction [beyond the book]:** Example 3.7 on PDF p. 32 prints $-8.42^\circ$; the correct phase is $-84.29^\circ$, consistent with the book's subsequent approximately $84.2^\circ$ lag.

> **[ DEMO 2 ]** — `ch3/l1_demo2_frequency_response.py` *(live, ~15 s)*
>
> **Teaching check [beyond the book]:** For $u(t)=\sin(10t)1(t)$, predict amplitude $1/\sqrt{101}=0.099504$ and phase $-\tan^{-1}(10)=-84.29^\circ$. Verify the complete expression gives $y(0)=0$. The transient coefficient is $10/101$; it is absent from the steady-state frequency-response calculation.

![Simulated sinusoidal response split into transient and steady state, the output phase lag, and the magnitude and phase of H(jw)](demos/ch3/figures/l1_demo2_frequency_response.svg)

> **[ FIG 3.5 ]** — PDF p. 33 (a), PDF p. 34 (b) *(slide)*
>
> **Point at:** panel (b), where the phase lag is measured off the plot as $10\,\delta t=1.47$ rad $=84.2^\circ$. That is how you would measure it in a lab, with no model at all.

#### Ask the class

> Both the amplitude ratio and the phase can be measured experimentally with a signal generator and an oscilloscope. What does that let you do that a model does not?

Identify a system you have not modeled. That is Section 3.7, and it is why the frequency response matters even to people who never draw a Bode plot.

---

## 8. The $\mathcal L_-$ transform and four transform pairs

### 8.1 The definition and why the lower limit is $0^-$

$$
\boxed{
F(s)\triangleq\int_{0^-}^{\infty}f(t)e^{-st}\,dt,
\qquad
s=\sigma_1+j\omega
\tag{3.32}
}
$$

Three remarks, briefly:

- **Why one-sided.** Eq. (3.30) integrates from $-\infty$; Eq. (3.32) starts at $t=0^-$. In control we switch things on, and we want initial conditions to appear in the algebra.
- **Why $0^-$ and not $0^+$.** Mainly so that an impulse at the origin is inside the interval; that is Example 3.9. It also makes the differentiation rule use $f(0^-)$, the initial conditions known *before* the input arrives (property 5 in §9). The book notes that the $\mathcal L_+$ version "is sometimes used in other applications." *(Same convention as 0.0.8 §18.)*
- **Convergence.** The factor $e^{-\sigma_1 t}$ is a built-in convergence aid: if $f$ grows no faster than exponentially, the integral converges for $\sigma_1$ large enough.

The inversion integral

$$
f(t)=\frac1{2\pi j}\int_{\sigma_c-j\infty}^{\sigma_c+j\infty}F(s)e^{st}\,ds
\tag{3.33}
$$

exists, and the book's comment on it is the honest one: *in practice this relation is seldom used.* Show it, point at the $e^{st}$ inside it, and move to the table.

### 8.2 Four pairs, derived not quoted (Examples 3.8–3.10)

| $f(t)$, $t\ge0$ | $F(s)$ | Region |
|---|---|---|
| $a\,1(t)$ | $a/s$ | $\Re(s)>0$ |
| $b\,t\,1(t)$ | $b/s^2$ | $\Re(s)>0$ |
| $\delta(t)$ | $1$ | all $s$ |
| $\sin\omega t\,1(t)$ | $\dfrac{\omega}{s^2+\omega^2}$ | $\Re(s)>0$ |
| $\cos\omega t\,1(t)$ *[beyond the book]* | $\dfrac{s}{s^2+\omega^2}$ | $\Re(s)>0$ |

Do the step on the board in one line, the ramp by parts, the impulse by the sifting property, and the sinusoid by Euler's relation. Each one uses Eq. (3.32) directly.

**Example 3.8, step.** For $\Re(s)>0$, $e^{-st}\to0$ as $t\to\infty$, so

$$
\mathcal L\{a\,1(t)\}=\int_{0^-}^{\infty}a\,e^{-st}\,dt=a\left[-\frac{e^{-st}}{s}\right]_{0^-}^{\infty}=a\left(0+\frac1s\right)=\frac as .
$$

**Example 3.8, ramp.** Integrate by parts, $\int u\,dv=uv-\int v\,du$, with $u=t$ and $dv=e^{-st}dt$. Then $du=dt$ and $v=-e^{-st}/s$:

$$
\mathcal L\{b\,t\,1(t)\}=b\int_{0^-}^{\infty}t\,e^{-st}\,dt
=b\left[-\frac{t\,e^{-st}}{s}\right]_{0^-}^{\infty}+\frac bs\int_{0^-}^{\infty}e^{-st}\,dt
=0+\frac bs\cdot\frac1s=\frac b{s^2} .
$$

The boundary term vanishes at the upper limit because $te^{-\sigma_1t}\to0$ for $\sigma_1>0$, and it vanishes at the lower limit because $t=0$.

**Example 3.9, impulse.** The interval $[0^-,\infty)$ contains the impulse at $t=0$. The sifting property, Eq. (3.11), picks out $e^{-s\cdot0}=1$:

$$
\int_{0^-}^{\infty}\delta(t)e^{-st}\,dt=1 .
\tag{3.34}
$$

**Example 3.10, sinusoid.** Substitute $\sin\omega t=(e^{j\omega t}-e^{-j\omega t})/(2j)$. Each exponential integrates like the step, with $s$ replaced by $s\mp j\omega$, and converges for $\Re(s)>0$:

$$
\mathcal L\{\sin\omega t\,1(t)\}
=\frac1{2j}\int_{0^-}^{\infty}\left(e^{-(s-j\omega)t}-e^{-(s+j\omega)t}\right)dt
=\frac1{2j}\left(\frac1{s-j\omega}-\frac1{s+j\omega}\right)
=\frac1{2j}\cdot\frac{2j\omega}{s^2+\omega^2}
=\frac{\omega}{s^2+\omega^2} .
\tag{3.35}
$$

**The cosine, needed in §10.3 [beyond the book].** Either repeat the calculation with $\cos\omega t=(e^{j\omega t}+e^{-j\omega t})/2$, or use the differentiation property. Since $\cos\omega t=\frac1\omega\frac{d}{dt}\sin\omega t$ for $t>0$ and $\sin0=0$:

$$
\mathcal L\{\cos\omega t\,1(t)\}=\frac1\omega\left[s\cdot\frac{\omega}{s^2+\omega^2}-\sin 0\right]=\frac{s}{s^2+\omega^2} .
$$

#### Instructor script

> Notice the impulse is the only one of these with no restriction on $s$, and notice it is the reason we chose the $0^-$ lower limit. If we had started the integral at $0^+$ we would have got zero for the transform of the impulse *input*, and $Y=HU$ would predict no response to an impulse at all.

**A remark on the regions:** the rational expressions can be continued algebraically beyond their regions of convergence, except at poles. That continuation does not make the defining integral converge there. In particular, interpreting $H(j\omega)$ as a settled sinusoidal response requires decaying transients and no pole at the forcing frequency.

---

## 9. The properties table

Work down Table A.1 quickly. The ones that earn board time are marked.

| # | Property | Statement |
|---|---|---|
| 1 | Superposition | $\mathcal L\{\alpha f_1+\beta f_2\}=\alpha F_1+\beta F_2$ |
| 2 | **Time delay** | $\mathcal L\{f(t-\lambda)1(t-\lambda)\}=e^{-s\lambda}F(s)$ for ordinary causal $f$ and $\lambda\ge0$ |
| 3 | Time scaling | $\mathcal L\{f(at)\}=\frac1aF(s/a)$, $a>0$ |
| 4 | Shift in frequency | $\mathcal L\{e^{-at}f(t)\}=F(s+a)$ |
| 5 | **Differentiation** | $\mathcal L\{\dot f\}=sF(s)-f(0^-)$ |
| 6 | **Integration** | $\mathcal L\left\{\int_{0^-}^t f(\tau)\,d\tau\right\}=\frac1sF(s)$, zero initial integrator state |
| 7 | **Convolution** | $\mathcal L\{f_1*f_2\}=F_1F_2$ |
| 8 | Time product (optional) | $\mathcal L\{f_1f_2\}=\frac1{2\pi j}\int_{c-j\infty}^{c+j\infty}F_1(p)F_2(s-p)\,dp$, when the contour and convergence conditions permit |
| 9 | Multiplication by $t$ | $\mathcal L\{tf(t)\}=-\dfrac{d}{ds}F(s)$ |

Property 8 is a complex contour integral, not ordinary real-axis convolution in $s$; it can be left to Appendix A. Negative time scaling reverses time and is not covered by the one-sided scaling rule. Repeated differentiation gives

$$
\boxed{
\mathcal L\{\ddot f\}=s^2F(s)-sf(0^-)-\dot f(0^-)
\tag{3.42}
}
$$

and in general Eq. (3.43). The derivation was done in the earlier lecture *(0.0.8 §19)*; here, state it and use it.

#### Say out loud

> Property 7 is the whole first half of this lecture compressed into one line. Convolution in time is multiplication in $s$. Property 2 is the one that lets you handle transport delay, and Chapter 6 will need it.
>
> Property 5 and Property 6 are inverses of each other, and together they are why an integrator is $1/s$ and a differentiator is $s$.

---

## 10. Inverting: partial fractions and the standard procedure

### 10.1 The five-step procedure

The book states the whole method as five steps. Put them on a slide:

1. Find $H(s)$ — transform the equations of motion and solve the resulting algebra.
2. Transform the input, $U(s)$.
3. Multiply for zero initial state: $Y(s)=H(s)U(s)$. If the initial state is nonzero, add its response as in §10.3.
4. Expand $Y(s)$ in partial fractions.
5. Invert term by term from the table.

Then add the book's caveat that in design the inverse-transform step "is typically not carried out explicitly." In paraphrase:

> **Hand inversion is often deferred during design.** Pole-zero locations guide a candidate design; a numerical time response then checks its actual performance. Pole locations alone do not determine amplitudes or certify specifications.

That comment is the bridge to the next lecture, which is entirely about reading a response off a pole-zero pattern.

### 10.2 The cover-up method

For a strictly proper rational function with distinct poles,

$$
F(s)=\frac{C_1}{s-p_1}+\cdots+\frac{C_n}{s-p_n},
\qquad
\boxed{C_i=\left.(s-p_i)F(s)\right|_{s=p_i}}
\tag{3.51, 3.53}
$$

and each term inverts to $C_ie^{p_it}1(t)$.

**Why the cover-up rule works.** Multiply the expansion by $(s-p_i)$:

$$
(s-p_i)F(s)=C_i+(s-p_i)\sum_{k\ne i}\frac{C_k}{s-p_k} .
$$

At $s=p_i$ every other term is multiplied by zero, and only $C_i$ is left. "Cover up" the factor $(s-p_i)$ in the denominator and evaluate what remains at $s=p_i$.

**Example 3.11.** Take

$$
Y(s)=\frac{(s+2)(s+4)}{s(s+1)(s+3)}=\frac{C_1}{s}+\frac{C_2}{s+1}+\frac{C_3}{s+3} .
$$

The numerator has degree 2 and the denominator has degree 3, so $Y$ is strictly proper and no polynomial term appears. The poles $0,-1,-3$ are distinct. Cover up each factor in turn:

$$
C_1=\left.\frac{(s+2)(s+4)}{(s+1)(s+3)}\right|_{s=0}=\frac{(2)(4)}{(1)(3)}=\frac83,
$$

$$
C_2=\left.\frac{(s+2)(s+4)}{s(s+3)}\right|_{s=-1}=\frac{(1)(3)}{(-1)(2)}=-\frac32,
$$

$$
C_3=\left.\frac{(s+2)(s+4)}{s(s+1)}\right|_{s=-3}=\frac{(-1)(1)}{(-3)(-2)}=-\frac16 .
$$

Invert with $1/s\leftrightarrow1(t)$ and $1/(s+a)\leftrightarrow e^{-at}1(t)$, so

$$
\boxed{
y(t)=\frac83\,1(t)-\frac32e^{-t}1(t)-\frac16e^{-3t}1(t) .
}
$$

In Matlab this is `[r,p,k] = residue(num,den)`, and the book prints the result to show it agrees.

> **[ DEMO 3 ]** — `ch3/l1_demo3_partial_fractions_fvt.py` *(slide)*
>
> **Teaching check [beyond the book]:** Recombine the three fractions of Example 3.11 over a common denominator. Also check $y(0^+)=1$ and $y(\infty)=8/3$. These checks catch residue sign errors without a simulation.

![Partial-fraction terms for Example 3.11, a valid Final Value Theorem result for Example 3.12, and the invalid result for Example 3.13](demos/ch3/figures/l1_demo3_partial_fractions_fvt.svg)

**Repeated roots and complex pairs** are in Appendix A. Mention that a repeated root brings in $te^{pt}$ terms — the same $(A+Bt)e^{st}$ structure as the critically damped case of *(0.0.8 §7.2)* — and leave the algebra to the appendix.

### 10.3 Solving differential equations (Examples 3.15–3.17)

Three short examples, in increasing generality. If time is short, do the first and assign the others.

All three use the same recipe:

1. Transform each term. Derivatives of $y$ use Eqs. (3.41)–(3.42), which carry the initial conditions: $\mathcal L\{\dot y\}=sY-y(0^-)$ and $\mathcal L\{\ddot y\}=s^2Y-sy(0^-)-\dot y(0^-)$.
2. Collect the $Y(s)$ terms on the left and move everything else to the right.
3. Solve for $Y(s)$.
4. Expand in partial fractions.
5. Invert from the table.

In these examples, $y(0)$ and $\dot y(0)$ mean the values at $0^-$. No input impulse acts at $t=0$, so they equal the $0^+$ values.

**Example 3.15, homogeneous.** $\ddot y+y=0$, $y(0)=\alpha$, $\dot y(0)=\beta$.

*Transform.* By Eq. (3.42), $\mathcal L\{\ddot y\}=s^2Y(s)-s\,y(0)-\dot y(0)=s^2Y-\alpha s-\beta$. The right side transforms to 0:

$$
s^2Y-\alpha s-\beta+Y=0 .
$$

*Solve for $Y$.* Collect the $Y$ terms: $(s^2+1)Y=\alpha s+\beta$, so

$$
Y(s)=\frac{\alpha s+\beta}{s^2+1}=\alpha\,\frac{s}{s^2+1}+\beta\,\frac{1}{s^2+1} .
$$

*Invert.* No partial fractions are needed, because the split above already matches two table entries with $\omega=1$ (§8.2): $s/(s^2+1)\leftrightarrow\cos t$ and $1/(s^2+1)\leftrightarrow\sin t$. Hence

$$
y(t)=[\alpha\cos t+\beta\sin t]1(t).
$$

*Check.* $y(0)=\alpha$, $\dot y=-\alpha\sin t+\beta\cos t$ gives $\dot y(0)=\beta$, and $\ddot y=-\alpha\cos t-\beta\sin t=-y$, so $\ddot y+y=0$. The poles $\pm j$ give the undamped oscillator's natural frequency of 1 rad/s.

**Example 3.16, forced with initial conditions.** $\ddot y+5\dot y+4y=3$ for $t\ge0$, with $y(0)=\alpha$, $\dot y(0)=\beta$.

*Transform.* The constant forcing is the step $3\cdot1(t)$, which transforms to $3/s$. Term by term:

$$
\underbrace{s^2Y-\alpha s-\beta}_{\mathcal L\{\ddot y\}}
+5\underbrace{\left(sY-\alpha\right)}_{\mathcal L\{\dot y\}}
+4Y=\frac3s .
$$

*Collect.*

$$
(s^2+5s+4)Y=\alpha s+\beta+5\alpha+\frac3s .
$$

*Solve for $Y$.* Factor $s^2+5s+4=(s+1)(s+4)$, because the roots of $s^2+5s+4=0$ are $s=\frac{-5\pm\sqrt{25-16}}{2}=-1,\,-4$. Multiply the numerator and denominator by $s$ to clear the $3/s$:

$$
Y(s)=\frac{s(s\alpha+\beta+5\alpha)+3}{s(s+1)(s+4)} .
$$

*Expand.* The numerator has degree 2 and the denominator has degree 3, and the poles $0,-1,-4$ are distinct. Write $Y=\dfrac{C_1}{s}+\dfrac{C_2}{s+1}+\dfrac{C_3}{s+4}$ and cover up each factor:

$$
C_1=\left.\frac{s(s\alpha+\beta+5\alpha)+3}{(s+1)(s+4)}\right|_{s=0}=\frac{0+3}{(1)(4)}=\frac34,
$$

$$
C_2=\left.\frac{s(s\alpha+\beta+5\alpha)+3}{s(s+4)}\right|_{s=-1}
=\frac{(-1)(-\alpha+\beta+5\alpha)+3}{(-1)(3)}
=\frac{-(4\alpha+\beta)+3}{-3}
=\frac{4\alpha+\beta-3}{3},
$$

$$
C_3=\left.\frac{s(s\alpha+\beta+5\alpha)+3}{s(s+1)}\right|_{s=-4}
=\frac{(-4)(-4\alpha+\beta+5\alpha)+3}{(-4)(-3)}
=\frac{3-4\alpha-4\beta}{12} .
$$

*Invert.*

$$
y(t)=\frac34+\frac{\beta+4\alpha-3}{3}e^{-t}+\frac{3-4\alpha-4\beta}{12}e^{-4t},\qquad t\ge0.
$$

**Check before moving on:** at $t=0$,

$$
y(0)=\frac{9+(16\alpha+4\beta-12)+(3-4\alpha-4\beta)}{12}=\frac{12\alpha}{12}=\alpha,
$$

$$
\dot y(0)=-\frac{4\alpha+\beta-3}{3}-4\cdot\frac{3-4\alpha-4\beta}{12}=\frac{-4\alpha-\beta+3-3+4\alpha+4\beta}{3}=\beta .
$$

As $t\to\infty$, $y\to3/4$. That matches setting $\ddot y=\dot y=0$ in the ODE, $4y=3$, and it is the Final Value Theorem of §11 in advance.

**Zero-input and zero-state split.** The transformed equation separates $Y$ into two pieces. The initial conditions contribute $Y_{zi}=\dfrac{\alpha s+\beta+5\alpha}{(s+1)(s+4)}$. By cover-up, its residues are $\dfrac{-\alpha+\beta+5\alpha}{3}=\dfrac{4\alpha+\beta}{3}$ at $s=-1$ and $\dfrac{-4\alpha+\beta+5\alpha}{-3}=-\dfrac{\alpha+\beta}{3}$ at $s=-4$. The input contributes $Y_{zs}=H(s)U(s)=\dfrac{3}{s(s+1)(s+4)}$. Its residues are $\dfrac{3}{4}$ at $s=0$, $\dfrac{3}{(-1)(3)}=-1$ at $s=-1$, and $\dfrac{3}{(-4)(-3)}=\dfrac14$ at $s=-4$. Therefore

$$
y_{zi}(t)=\frac{4\alpha+\beta}{3}e^{-t}-\frac{\alpha+\beta}{3}e^{-4t},
\qquad
y_{zs}(t)=\frac34-e^{-t}+\frac14e^{-4t},
$$

and the sum reproduces the full answer term by term. The zero-state part alone satisfies $y_{zs}(0)=\dot y_{zs}(0)=0$.

In Example 3.15, the unit-step notation denotes the post-zero solution only. Example 3.16 states $t\ge0$ explicitly for the same reason. Extending a nonzero initial value as zero for $t<0$ introduces distributions when the signal is differentiated.

**Example 3.17, zero initial conditions.** $\ddot y+5\dot y+4y=2e^{-2t}1(t)$, $y(0)=\dot y(0)=0$.

*Transform.* With zero initial conditions, $\ddot y\to s^2Y$ and $\dot y\to sY$. The input transforms by the step and the frequency shift of property 4: $\mathcal L\{2e^{-2t}1(t)\}=2/(s+2)$. Then

$$
(s^2+5s+4)Y=\frac{2}{s+2}
\qquad\Longrightarrow\qquad
Y(s)=\frac{2}{(s+2)(s+1)(s+4)} .
$$

This is $Y=HU$ with $H(s)=1/[(s+1)(s+4)]$ and $U(s)=2/(s+2)$, which is step 3 of the five-step procedure in §10.1.

*Expand.* The three poles are distinct. Cover up each one:

$$
C_{-2}=\left.\frac{2}{(s+1)(s+4)}\right|_{s=-2}=\frac{2}{(-1)(2)}=-1,
\qquad
C_{-1}=\left.\frac{2}{(s+2)(s+4)}\right|_{s=-1}=\frac{2}{(1)(3)}=\frac23,
$$

$$
C_{-4}=\left.\frac{2}{(s+2)(s+1)}\right|_{s=-4}=\frac{2}{(-2)(-3)}=\frac13,
$$

so

$$
Y(s)=-\frac1{s+2}+\frac{2/3}{s+1}+\frac{1/3}{s+4}
\quad\Longrightarrow\quad
y(t)=\left(-e^{-2t}+\tfrac23e^{-t}+\tfrac13e^{-4t}\right)1(t).
$$

*Check.* $y(0)=-1+\tfrac23+\tfrac13=0$, and $\dot y(0)=2-\tfrac23-\tfrac43=0$, as zero initial conditions require. The book's Matlab `residue(2, poly([-2;-1;-4]))` returns `r = [0.3333 -1 0.6667]` for `p = [-4 -2 -1]`, which agrees.

#### Ask the class

> In Example 3.17 the input contributed the term $e^{-2t}$ and the system contributed $e^{-t}$ and $e^{-4t}$. Which of those is a pole of the transfer function?

Only the last two. **For zero initial state, the poles of $Y=HU$ come from the plant and the input, subject to cancellation; coincident poles can increase multiplicity.** The Final Value Theorem checks the poles of the resulting $sY(s)$, not just those of $H(s)$.

---

## 11. The Final Value Theorem

### 11.1 Statement

$$
\boxed{
\text{If all poles of }sY(s)\text{ are strictly in the LHP, then}
\quad
\lim_{t\to\infty}y(t)=\lim_{s\to0}sY(s)
\tag{3.54}
}
$$

#### Why it works: multiplying by $s$ differentiates

Start from something students already believe. Where a signal ends up is where it started plus everything it changed along the way:

$$
y(\infty)=y(0^-)+\int_{0^-}^{\infty}\dot y(t)\,dt .
$$

Now look at $sY(s)$. By the differentiation property (property 5 in §9), $sY(s)$ is almost exactly the transform of the derivative:

$$
sY(s)=\mathcal L\{\dot y\}+y(0^-)=y(0^-)+\int_{0^-}^{\infty}\dot y(t)\,e^{-st}\,dt .
$$

Put the two lines side by side. They differ only by the weight $e^{-st}$ inside the integral. As $s\to0$ that weight tends to 1 at every time, so the second line becomes the first:

$$
\boxed{
\lim_{s\to0}sY(s)
=y(0^-)+\underbrace{\int_{0^-}^{\infty}\dot y(t)\,dt}_{\text{total change}}
=y(\infty)
}
$$

That is the whole theorem. **$sY(s)$ is (up to the starting value) the transform of the rate of change, and at $s=0$ a transform just adds up its signal over all time.** Adding up the rate of change gives the total change, and the starting value plus the total change is the final value. The $0^-$ convention (§8.1) makes this bookkeeping exact: any jump at $t=0$, such as an impulse in $\dot y$, is counted in the integral rather than lost.

**What "$s\to0$" means in time.** The weight $e^{-st}$ with small positive $s$ is a very long, slowly fading window. It is close to 1 up to times of order $1/s$ before cutting off. Letting $s\to0$ stretches that window over the entire future. Small $s$ looks at long times, which is why a limit at $s=0$ can say anything about $t\to\infty$. The same reasoning in reverse gives the initial value theorem: as $s\to\infty$ the window shrinks onto $t=0^+$, and $\lim_{s\to\infty}sY(s)=y(0^+)$.

**Where the hypothesis comes in.** Replacing $e^{-st}$ by 1 inside the integral is legal only if the plain integral $\int_0^\infty\dot y\,dt$ settles to a finite value, that is, only if $y$ actually stops changing. The pole condition on $sY(s)$ is the checkable version of that requirement. The two failures in the examples below are exactly the two ways the total change can fail to exist:

- **Growth (Example 3.13).** For $y=-\tfrac32+\tfrac32e^{2t}$, the derivative $\dot y=3e^{2t}$ grows, so the area under it is infinite. Its transform $\int_0^\infty 3e^{2t}e^{-st}\,dt=3/(s-2)$ converges only for $\Re(s)>2$. The limit $s\to0$ walks outside the region where the integral means anything. The algebra still returns a number, $-3/2$, but no longer a statement about the signal.
- **Oscillation.** For $y=\sin t$ (poles of $sY$ at $\pm j$), $\dot y=\cos t$ and $\int_0^\infty\cos t\,dt$ never settles; its running value $\sin t_f$ keeps swinging between $-1$ and $1$. The formula gives $\lim_{s\to0}s\cdot\frac{1}{s^2+1}=0$, the *average* of the oscillation, even though $y$ has no limit.

**A one-line check to put on the board.** For $y=(1-e^{-t})1(t)$, $\dot y=e^{-t}$ and the total change is $\int_0^\infty e^{-t}\,dt=1$. In $s$: $Y=\dfrac1{s(s+1)}$, so $sY=\dfrac1{s+1}\to1$. Same number, and for the same reason.

### Instructor script

> Here is a second way to see the same theorem, and it is really just the partial-fraction expansion read backwards.
>
> Hold both views together. The derivative argument says *why* $sY(s)$ at $s=0$ is a final value. The partial-fraction argument says *which* poles let that final value exist.
>
> Expand $Y(s)$ into one term per pole. Every pole strictly in the left half plane gives a term that dies. A pole in the right half plane gives a term that grows, so there is no final value. A pair on the imaginary axis gives a sinusoid that never settles, so the limit does not exist either.
>
> That leaves exactly one way to have a nonzero constant at the end: a single pole at the origin, with everything else in the LHP. And the constant is that pole's residue — which is what $\lim_{s\to0}sY(s)$ computes.
>
> So the theorem is not a new fact. It is the cover-up method applied to one particular pole.

### 11.2 Example 3.12: used correctly

$$
Y(s)=\frac{3(s+2)}{s(s^2+2s+10)} .
$$

*Step 1: check the hypothesis.* Multiplying by $s$ cancels the pole at the origin:

$$
sY(s)=\frac{3(s+2)}{s^2+2s+10} .
$$

Its poles are the roots of $s^2+2s+10=0$:

$$
s=\frac{-2\pm\sqrt{4-40}}{2}=-1\pm3j .
$$

Both have real part $-1<0$, so they are strictly in the LHP and the theorem applies.

*Step 2: take the limit.*

$$
y(\infty)=\lim_{s\to0}sY(s)=\frac{3(0+2)}{0+0+10}=\frac{6}{10}=0.6 .
$$

**Cross-check by cover-up:** the residue of $Y$ at $s=0$ is exactly this $sY(s)|_{s=0}$. The other two terms carry $e^{-t}$ and die out, which is the argument of §11.1.

### 11.3 Example 3.13: used incorrectly

$$
Y(s)=\frac{3}{s(s-2)} .
$$

Applying the formula blindly gives

$$
\lim_{s\to0}sY(s)=\lim_{s\to0}\frac{3}{s-2}=-\frac32 .
$$

*The step that was skipped:* $sY(s)=3/(s-2)$ has a pole at $s=+2$, in the RHP, so the hypothesis fails. To see what the formula threw away, expand by cover-up:

$$
C_0=\left.\frac{3}{s-2}\right|_{s=0}=-\frac32,
\qquad
C_2=\left.\frac{3}{s}\right|_{s=2}=\frac32,
\qquad
Y(s)=\frac{-3/2}{s}+\frac{3/2}{s-2} .
$$

Inverting, the true signal is

$$
y(t)=\left(-\frac32+\frac32e^{2t}\right)1(t),
$$

which is unbounded. The formula returned the residue $C_0$, the constant term, and silently discarded the growing $C_2e^{2t}$ term.

> **[ DEMO 3, continued ]** — same script, middle and right panels
>
> **Teaching check [beyond the book]:** For Example 3.13, evaluate $y(6)=\tfrac32(e^{12}-1)\approx244131$. The formal limit $\lim_{s\to0}sY(s)=-1.5$ is only the constant term; the growing mode prevents a final value.

### 11.4 DC gain (Example 3.14)

Feed a unit step, $U=1/s$:

For a stable proper transfer function, the final value exists and

$$
\boxed{
\text{DC gain}=\lim_{s\to0}sG(s)\frac1s=\lim_{s\to0}G(s)=G(0)
\tag{3.55}
}
$$

For $G(s)=\dfrac{3(s+2)}{s^2+2s+10}$, first check stability. The poles are $-1\pm3j$, as in Example 3.12, so they are in the LHP. The step response $Y(s)=G(s)/s$ therefore satisfies the hypothesis of Eq. (3.54), and

$$
\text{DC gain}=G(0)=\frac{3(0+2)}{0+0+10}=\frac{6}{10}=0.6 .
$$

**Same arithmetic, different question.** Example 3.12 asked where a particular signal ends up; Example 3.14 asked what a system does to a constant. Point out that they produced the same number because they are the same calculation.

---

## 12. Poles and zeros (§3.1.8)

Write the two forms:

$$
H(s)=\frac{b_1s^m+\cdots+b_{m+1}}{s^n+a_1s^{n-1}+\cdots+a_n}=\frac{N(s)}{D(s)}
=K\frac{\prod_{i=1}^m(s-z_i)}{\prod_{i=1}^n(s-p_i)} .
\tag{3.56, 3.57}
$$

$K$ is the **transfer-function gain**, generally different from $H(0)$; $z_i$ are the **finite zeros**; $p_i$ are the **poles**. Define these for the reduced rational function, after cancelling common factors. Keep the full characteristic polynomial separately when checking internal modes.

$$
\boxed{H(z_i)=0}
\qquad\qquad
\boxed{|H(s)|\to\infty \text{ as } s\to p_i}
$$

Four statements to make, each in one sentence:

1. **Poles are the modes.** They set the natural, unforced behaviour — this is the content of the earlier lecture *(0.0.8 §17)*, and it is what §3.3 will develop into a picture.
2. **Zeros block transmission.** Drive with $u=u_0e^{s_0t}$ where $s_0=z_i$ and the output is identically zero, for a compatible initial state. Hence *transmission zeros*. *(The precise version, with the required initial state, is 0.0.8 §17.)*
3. **Zeros at infinity.** If $m<n$, the book counts $n-m$ zeros at infinity. Standard finite-dimensional causal state-space models have proper transfer functions ($m\le n$). Ideal differentiators and some idealised choices of physical input/output can produce improper models; these are not bounded-bandwidth realisations.
4. **Cancellation is a warning sign.** A common numerator/denominator factor disappears from the reduced transfer function. If it represents a mode of the physical realisation, that internal mode remains. The transfer function alone cannot tell whether such a hidden mode is physically present. Lecture 4 makes this distinction concrete.

### The book's tent-pole picture

Worth thirty seconds because it makes $|H|\to\infty$ concrete: plot $|H(s)|$ as a surface over the $s$-plane, and a pole is a tent pole holding the fabric up to infinity, a zero is a peg pinning it to the ground.

---

## 13. Computer tools (§3.1.9)

The book works four systems from Chapter 2 through Matlab. Show the code, run the equivalent in whatever language your students use, and spend the time on the *interpretation* instead of the syntax.

| Example | System | Transfer function | What to notice |
|---|---|---|---|
| 3.18 | Cruise control | $\dfrac{0.001}{s^2+0.05s}$ | Poles $0$ and $-0.05$, no zeros. The pole at the origin is the integration from speed to position. |
| 3.19 | DC motor, angle | $\dfrac{100}{s(s^2+10.1s+101)}$ | Poles $0$, $-5.05\pm8.6889j$. Measuring speed instead of angle cancels the pole at the origin. |
| 3.20 | $\ddot y+6\dot y+25y=9u+3\dot u$ | $\dfrac{3s+9}{s^2+6s+25}$ | Written down by inspection, per §6.4. Zero at $-3$, poles at $-3\pm4j$, gain 3. |
| 3.21 | Satellite attitude | $\dfrac{0.0002}{s^2}$ | A double pole at the origin and nothing else. |

**The pole and zero locations, by hand.** Check these before trusting the software output.

- **3.18:** $s^2+0.05s=s(s+0.05)$, so the poles are $s=0$ and $s=-0.05$. The numerator is a constant, so there are no finite zeros.
- **3.19:** $s(s^2+10.1s+101)$ gives $s=0$ together with
  $$
  s=\frac{-10.1\pm\sqrt{10.1^2-4(101)}}{2}=-5.05\pm\frac{\sqrt{102.01-404}}{2}=-5.05\pm j\frac{\sqrt{301.99}}{2}=-5.05\pm8.6889j .
  $$
- **3.20:** Transform with zero initial conditions: $(s^2+6s+25)Y=(3s+9)U$. The zero is at $3s+9=0$, so $s=-3$. The poles are $s=\frac{-6\pm\sqrt{36-100}}{2}=-3\pm4j$. In the form of Eq. (3.57), $H=3\,\dfrac{s+3}{s^2+6s+25}$, so $K=3$. By contrast, $H(0)=9/25$. This is the "$K$ is generally different from $H(0)$" remark of §12 in action.
- **3.21:** $s^2=0$ is a double pole at the origin, and the numerator is a constant.

**Example 3.19 is worth a full sentence:** with zero initial state, the speed transfer function is $s$ times the angle transfer function, so the pole at the origin cancels. A constant angular offset is invisible in the speed output: the position mode is unobservable from that measurement, though position remains a physical state.

> **[ DEMO 4 ]** — `ch3/l1_demo4_satellite_pulse.py` *(slide)*
>
> **Teaching check [beyond the book]:** For Example 3.21, use the book's moment arm $d=1$ m and inertia $I=5000$ kg·m$^2$. A 25 N pulse on $5\le t<5.1$ s supplies 2.5 N·s of force impulse, hence 2.5 N·m·s of angular impulse and a rate change of $0.0005$ rad/s ($0.02865^\circ$/s). An equal negative pulse on $6.1\le t<6.2$ s stops the drift and leaves $0.00055$ rad ($0.03151^\circ$). One pulse leaves unbounded angle; two balanced pulses leave a finite angle.
>
> *Working.* During a pulse the angular acceleration is $\ddot\theta=Fd/I=25/5000=0.005$ rad/s$^2$. Track $\theta$ and $\dot\theta$ through each phase with constant-acceleration kinematics:
>
> | Interval | Duration | $\dot\theta$ at end (rad/s) | $\Delta\theta$ (rad) | $\theta$ at end (rad) |
> |---|---|---|---|---|
> | $5\to5.1$ s, $+$pulse | 0.1 s | $0.005(0.1)=0.0005$ | $\tfrac12(0.005)(0.1)^2=0.000025$ | $0.000025$ |
> | $5.1\to6.1$ s, coast | 1.0 s | $0.0005$ | $0.0005(1.0)=0.0005$ | $0.000525$ |
> | $6.1\to6.2$ s, $-$pulse | 0.1 s | $0.0005-0.0005=0$ | $0.0005(0.1)-\tfrac12(0.005)(0.1)^2=0.000025$ | $0.00055$ |
>
> Converting, $0.0005\times180/\pi=0.02865^\circ$/s and $0.00055\times180/\pi=0.03151^\circ$. In transform terms, each pulse is a step minus a delayed step (property 2 of §9), so
>
> $$
> s^2\Theta(s)=\frac{0.005}{s}\left[\left(e^{-5s}-e^{-5.1s}\right)-\left(e^{-6.1s}-e^{-6.2s}\right)\right].
> $$
>
> The $1/s^2$ of the plant integrates the net impulse into a rate and then into an angle.

![Satellite attitude drifting after one thruster pulse and holding after a pulse and counter-pulse](demos/ch3/figures/l1_demo4_satellite_pulse.svg)

> **[ FIG 3.7, 3.8 ]** — PDF p. 63, PDF p. 64, PDF p. 65, PDF p. 65

---

## 14. Summary and closing script

$$
\boxed{
\text{LTI}
\rightarrow
\text{superposition + time invariance}
\rightarrow
y=h*u
\rightarrow
Y(s)=H(s)U(s)
}
$$

$$
\boxed{
H(s)=\mathcal L\{h\}
=\frac{Y(s)}{U(s)}\Big|_{\text{zero i.c.}}
=\text{the gain applied to }e^{st}
}
$$

$$
\boxed{
\text{poles } D(s)=0 \ \Rightarrow\ \text{the modes}
\qquad
\text{zeros } N(s)=0 \ \Rightarrow\ \text{blocked transmission}
}
$$

### Closing script

> We started with two properties: superposition and time invariance. From them, the impulse response determines every zero-state input-output response through convolution. Initial-state motion is a separate contribution.
>
> Convolution is awkward to compute, so we asked what happens for an exponential input. The exponential came straight back out, multiplied by a number. That number, as a function of $s$, is the transfer function, and the integral that defines it is the Laplace transform.
>
> After that everything was bookkeeping: a table of transform pairs, a table of properties, the cover-up method to break a rational function into pieces the table knows, and the Final Value Theorem to read off a steady state without inverting anything at all.
>
> The book then uses pole-zero locations to guide design before computing a time response to verify the result. Hand inversion teaches the link; numerical response calculations remain part of design.
>
> That is next time. We will draw the $s$-plane, put a pole on it, and learn to see the response.

---

# Part II — Materials

## 15. One-board summary

```text
   LINEAR + TIME INVARIANT
        |
        |  superposition          time invariance
        v
   y(t) = INTEGRAL h(tau) u(t-tau) d tau            <- one experiment, all inputs
        |
        |  try u = e^{st}
        v
   y(t) = H(s) e^{st},   H(s) = INTEGRAL h(tau) e^{-s tau} d tau
        |
        v
   Y(s) = H(s) U(s)      convolution  ->  multiplication
        |
        +--- H(s) = L{h(t)}                     (impulse response)
        +--- H(s) = Y(s)/U(s), zero i.c.        (ratio of transforms)
        +--- H(s) = N(s)/D(s) = K prod(s-z)/prod(s-p)

   D(s) = 0  ->  poles  ->  the modes, the natural response
   N(s) = 0  ->  zeros  ->  blocked transmission

   final value:   y(inf) = lim s Y(s)     ONLY if all poles of sY(s) are LHP
   DC gain:       G(0)
```

## 16. Discussion questions

1. Superposition held in Example 3.1 even with $k$ time varying, but time invariance did not. Which parts of today's lecture survive for a linear time-varying system, and which collapse?
2. The convolution integral needs $h(t)$ for all $t\ge0$. The transfer function is one function of $s$. Have we lost information?
3. Why does the impulse response deserve the name *natural response*? What does an impulse do to a system that an initial condition does not?
4. Eq. (3.17) describes an input that has been running since $t=-\infty$. Why does the answer still matter for a system we switch on this morning?
5. A colleague computes $\lim_{s\to0}sY(s)$ for a signal and reports the number as the steady-state value. What must you check before believing it, and what does the number mean if the check fails?
6. Example 3.19 loses a pole when the output changes from angle to speed. Is that the same kind of event as a pole-zero cancellation between a controller and a plant?

## 17. Homework and follow-up problems

Selected from the book's end-of-chapter set for §3.1.

| Problem | Topic | Why this one |
|---|---|---|
| 3.1 | Complex conjugate residues | One line of theory that halves later arithmetic. |
| 3.2, 3.3 | Transforms of elementary time functions | Fluency with the table; do a handful, not all. |
| 3.5 | Transforms involving convolution | Uses property 7 in the direction students find harder. |
| 3.6 | Transform of modified $f(t)$ | Delay, scaling and frequency shift in one problem. |
| 3.7, 3.8 | Inverse transforms | The cover-up method, including a quadratic factor. |
| 3.9 | Solving ODEs by transform | Full Examples 3.15–3.17 workflow, with initial conditions. |
| 3.10, 3.11 | Step response by convolution | Forces the time-domain integral, which is the point of §3.1.1. |
| 3.12 | Convolution with a piecewise input (Fig. 3.47) | More practice with the time-domain integral. |
| 3.13, 3.14 | Transfer functions of a field-controlled DC motor with load, and of the Fig. 2.57 motor system | Connects Chapter 2 models to today's machinery. |

**Suggested additional exercise [beyond the book]:** in Example 3.7 change the input to $\sin t\,1(t)$. Predict the amplitude, phase and transient coefficient, then check against $y(t)=(e^{-t}+\sin t-\cos t)/2$ for $t\ge0$.

*Answer key.* The frequency response gives $M(1)=1/\sqrt2\approx0.707$ and $\varphi(1)=-\tan^{-1}1=-45^\circ$. For the full solution, $Y=\dfrac{1}{(s+1)(s^2+1)}=\dfrac{A}{s+1}+\dfrac{Bs+C}{s^2+1}$:

- Cover-up gives $A=1/(1+1)=\tfrac12$.
- Matching the $s^2$ coefficients gives $A+B=0$, so $B=-\tfrac12$.
- Matching the constants gives $A+C=1$, so $C=\tfrac12$.
- The $s^1$ coefficients give $B+C=0$ as a check.

Hence $y=\tfrac12e^{-t}+\tfrac12(\sin t-\cos t)$ with transient coefficient $\tfrac12$. Also $\sin t-\cos t=\sqrt2\sin(t-45^\circ)$, which confirms the amplitude $1/\sqrt2$ and phase $-45^\circ$.

## 18. Instructor cautions

1. **Two meanings of $\sigma$.** In §3.1 the book writes $s=\sigma_1+j\omega$; in §3.3 it writes a *stable* pole as $s=-\sigma\pm j\omega_d$ with $\sigma>0$. Announce which is on the board, or half the class will read the next lecture's stability condition backwards.
2. **$H(s)$ from Eq. (3.17) is the particular solution.** The book says so in a footnote; students miss it. The complete response also contains natural modes excited by initial conditions and by the switch-on, as Example 3.7 shows.
3. **The Final Value Theorem has a hypothesis.** Teach it as a two-step operation: check the poles of $sY(s)$, then take the limit. Example 3.13 exists exactly to punish the one-step version.
4. **Pole-zero reasoning guides design; time responses verify it.** Hand partial fractions are one way to learn that reasoning. Numerical simulation is still needed to check specifications and model approximations.
5. **Convolution is commutative, and that surprises people.** $h*u=u*h$. It is worth writing both forms of Eq. (3.13) on the board.
6. **The transform of the impulse depends on the $0^-$ convention.** If a student uses a table from a signals course with a $0^+$ lower limit, their answers will differ at exactly the moments that matter.

## 19. Demonstration index

| # | Script | Section | What it settles | Use |
|---|---|---|---|---|
| 1 | `l1_demo1_convolution.py` | §5 | A sum of weighted, shifted impulse responses converges to the convolution integral (asymptotically first order), against an independent ODE solve. | **live** |
| 2 | `l1_demo2_frequency_response.py` | §7 | Amplitude and phase measured from a simulation agree closely with $H(j\omega)$; the transient is separate. | **live** |
| 3 | `l1_demo3_partial_fractions_fvt.py` | §10, §11 | Cover-up residues match `residue`; invalid use of the final-value formula returns $-1.5$ for a signal that reaches 244,131. | slide |
| 4 | `l1_demo4_satellite_pulse.py` | §13 | A double integrator drifts forever after one pulse and holds after two. | slide |

## 20. Where this lecture sits

| Lecture | Book sections | Content |
|---|---|---|
| *From Physical Models to the Laplace Transform* | — | $e^{st}$, characteristic polynomials, poles as rates, zeros and zero dynamics, from physics |
| **This lecture (L1)** | **3.1** | **Convolution, transfer functions, frequency response, transform properties, partial fractions, final value, poles and zeros** |
| L2 | 3.2, 3.3 | Block diagrams, Mason's rule, effect of pole locations |
| L3 | 3.4, 3.5 | Time-domain specifications, effects of zeros and extra poles |
| L4 | 3.6–3.9 | Stability, Routh's criterion, system identification, scaling, history |
