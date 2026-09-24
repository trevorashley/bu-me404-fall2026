# Addendum A: Signals Built from Exponentials

**Student lecture notes — Fourier series, periodic forcing, and the road to $e^{-\sigma t}$**

A transfer function tells us how a linear system responds to an exponential input. Superposition extends that result to sums of exponentials. Fourier series let us build a square wave from those sums; separating repeated pulses leads to a Fourier integral. A step then shows why the Laplace transform needs the weight $e^{-\sigma t}$.

**Prerequisites:** Exponential trial solutions, complex-conjugate pairs, and the spring-mass-damper transfer function from [Lecture 1, §4.5](modeling-and-dynamics-poles_student.md#section-4-5) and [§5](modeling-and-dynamics-poles_student.md#section-5), together with elementary integration.

**Where this fits:** Read this addendum before [Lecture 1, §15: Transition to the Laplace transform](modeling-and-dynamics-poles_student.md#section-15). It develops the signal representation used there and prepares for the switched-heater calculation in [Lecture 1, §17.1](modeling-and-dynamics-poles_student.md#section-17-1).

## Learning objectives

After studying this addendum, you should be able to:

1. Use linearity and constant coefficients to find particular responses to finite sums of exponentials, away from poles.
2. Obtain a real sinusoidal response from $G(j\omega)$ and interpret its magnitude and phase.
3. Derive the Fourier coefficients of a square wave and reconstruct it using complex exponentials or real sines.
4. Predict a stable spring-mass-damper's periodic steady-state response harmonic by harmonic, including amplification near resonance.
5. Explain Fourier-series convergence at a jump and the Gibbs phenomenon.
6. Distinguish finite narrow pulses from the ideal impulse limit.
7. Explain the two limits from a periodic pulse train to an isolated pulse and then to a step.
8. Derive the step transform $1/s$, state its region of convergence, and explain the role of $e^{-\sigma t}$ in transformation and reconstruction.
9. Choose harmonic sums for periodic steady state or transform pairs and partial fractions for rational switched-input problems.

## Notation and assumptions

| Symbol | Meaning |
|---|---|
| $j$ | imaginary unit |
| $s=\sigma+j\omega$ | complex exponential rate |
| $u(t)$ | input signal; a force in the spring-mass-damper example |
| $x_p(t)$, $x_{ss}(t)$ | particular response and periodic steady-state response |
| $T$ | repetition period, not temperature |
| $\omega_0=2\pi/T$ | fundamental angular frequency |
| $n\omega_0$ | frequency of harmonic $n$; distinct from natural frequency $\omega_n$ |
| $U_n$, $X_n$ | complex Fourier coefficients of the input and response |
| $N$ | highest harmonic retained in a partial sum |
| $L$ | duration of an isolated pulse |
| $\varepsilon$ | width of a narrow, unit-area pulse |
| $U(s)$, $X(s)$ | Laplace transforms, introduced in [§6](#section-6) |
| $h(t)$ | causal impulse response |

We use $n$ for harmonic indices, $k$ for stiffness, and $c$ for damping. Unless an undamped case is explicitly stated, the spring-mass-damper has $m>0$, $k>0$, and $c>0$, so its natural modes decay. **LTI** means linear and time invariant; **zero-state response** means the response to an input with the system initially at rest.

The coefficients $U_n$ and $X_n$ are amplitudes of individual complex harmonics. Transform values such as $U(\sigma+j\omega)$ instead supply weights in a continuous reconstruction integral; they are not amplitudes of isolated frequencies.

---

## 1. From one exponential to a general input {#section-1}

In [Lecture 1, §5](modeling-and-dynamics-poles_student.md#section-5), the forced model

$$
m\ddot x+c\dot x+kx=u(t)
$$

gave the particular response

$$
u(t)=Fe^{st}
\quad\Longrightarrow\quad
x_p(t)=G(s)Fe^{st},
\qquad G(s)=\frac{1}{ms^2+cs+k},
$$

provided $s$ is not a pole. Differentiation preserves the exponential's shape, so the differential equation becomes an algebraic amplitude calculation.

Real inputs also include steps, pulses, and repeated switching. To use the same calculation for these inputs, we need to answer two questions:

1. Can we build the input from exponentials?
2. If we can, does adding their separate responses give the response to the complete input?

Linearity answers the second question. Fourier series and the Laplace transform answer the first, with convergence conditions that we will develop along the way.

## 2. Superposition, and two exponentials make a cosine {#section-2}

### 2.1 Many exponentials in, many exponentials out {#section-2-1}

The spring-mass-damper $m\ddot x+c\dot x+kx=f$ is **linear**: if $x_1$ is a response to $f_1$ and $x_2$ is a response to $f_2$, then $\alpha x_1+\beta x_2$ is a response to $\alpha f_1+\beta f_2$. The coefficients $m,c,k$ are **constant**, and that is what lets [Lecture 1, §5](modeling-and-dynamics-poles_student.md#section-5) cancel $e^{st}$ from both sides.

Combine the two properties with [Lecture 1, §5](modeling-and-dynamics-poles_student.md#section-5)'s result, one exponential at a time:

$$
\boxed{
u(t)=\sum_n U_n\,e^{s_nt}
\quad\Longrightarrow\quad
x_p(t)=\sum_n G(s_n)\,U_n\,e^{s_nt}
}
$$

Each exponential passes through on its own and is multiplied by the value of $G$ at its own rate. Nothing mixes. This holds directly for finite sums provided no $s_n$ lands exactly on a pole. Extending it to an infinite series requires convergence. For the square wave and the stable spring-mass-damper with $m>0$, $k>0$, $c>0$, it gives the periodic steady-state response. The complete response also includes the homogeneous terms needed to meet the initial conditions.

#### Check your understanding

> Suppose the spring were nonlinear, with a force $kx+k_3x^3$. Drive it with $\cos\omega t$. Why can't one amplitude-independent LTI transfer function describe its full response?

**Answer:** $\cos^3\omega t=\tfrac34\cos\omega t+\tfrac14\cos3\omega t$. To show this with exponentials, write $\theta=\omega t$ and cube Euler's form with the binomial theorem:

$$
\cos^3\theta=\left(\frac{e^{j\theta}+e^{-j\theta}}2\right)^3
=\frac{e^{3j\theta}+3e^{j\theta}+3e^{-j\theta}+e^{-3j\theta}}8
=\frac{2\cos3\theta+6\cos\theta}8 .
$$

Multiplying exponentials *adds* their rates, so $e^{j\theta}\cdot e^{j\theta}\cdot e^{j\theta}$ produces $e^{3j\theta}$. A frequency that was never in the input appears in the output. The exponentials no longer pass through separately, so no single complex number per frequency can describe the system. Linearity is what keeps them apart. A transfer function can still describe a specified linearization about an operating point.

### 2.2 Two exponentials make a cosine {#section-2-2}

This is the smallest case of the box above. Euler's identity splits a cosine into a conjugate pair:

$$
A\cos\omega t=\frac A2e^{j\omega t}+\frac A2e^{-j\omega t}.
$$

Each term passes through $G$ separately:

$$
x_p(t)=\frac A2G(j\omega)e^{j\omega t}+\frac A2G(-j\omega)e^{-j\omega t}.
$$

For a real model, $G(-j\omega)=\overline{G(j\omega)}$. $G$ is a ratio of polynomials with real coefficients, and conjugating $s$ in such a polynomial conjugates its value. For example, $G(-j\omega)=1/(k-m\omega^2-jc\omega)$, which is the conjugate of $G(j\omega)=1/(k-m\omega^2+jc\omega)$.

The two terms are therefore conjugates, and their sum is real. This is the [Lecture 1, §4.5](modeling-and-dynamics-poles_student.md#section-4-5) argument again, now applied to a forced response. The sum is twice the real part of the first term: $x_p=\Re\{AG(j\omega)e^{j\omega t}\}$. Write $G(j\omega)=|G(j\omega)|e^{j\angle G(j\omega)}$. Then $AG(j\omega)e^{j\omega t}=A|G(j\omega)|e^{j(\omega t+\angle G(j\omega))}$, whose real part is the cosine below:

$$
\boxed{
A\cos\omega t
\quad\Longrightarrow\quad
x_p(t)=A\,|G(j\omega)|\cos\!\big(\omega t+\angle G(j\omega)\big)
}
$$

The same holds with $\sin$ in place of $\cos$. Magnitude is the amplitude ratio, and angle is the phase shift. For a stable system, this particular response is the sinusoidal steady state after the natural modes have decayed.

## 3. A square wave is a sum of exponentials {#section-3}

### 3.1 The signal {#section-3-1}

Take a force that switches between $0$ and $1$ N:

$$
u(t)=
\begin{cases}
1, & 0<t<T/2\\
0, & T/2<t<T
\end{cases}
\qquad\text{repeated with period }T.
$$

Physically, this is a step that switches off, waits, and switches on again. In [§6](#section-6) we will vary the pulse duration and repetition period separately to reach a single pulse and then a step.

### 3.2 The Fourier-series representation {#section-3-2}

The complex exponentials that repeat with period $T$ satisfy $e^{j\omega T}=1$, so $\omega=n\omega_0$ for integer $n$. For the piecewise-smooth periodic signals considered here, these harmonics give the Fourier-series representation:

$$
\boxed{
u(t)=\sum_{n=-\infty}^{\infty}U_n\,e^{jn\omega_0t},
\qquad
\omega_0=\frac{2\pi}{T}
}
$$

### 3.3 Finding the amplitudes by projection {#section-3-3}

The harmonics are orthogonal over one period:

$$
\frac1T\int_0^Te^{jn\omega_0t}\,e^{-jl\omega_0t}\,dt=
\begin{cases}1,&n=l\\0,&n\neq l\end{cases}
$$

When $n\neq l$, the integrand turns a whole number of times around the unit circle and averages to zero. Explicitly, with $p=n-l\neq0$ and $\omega_0T=2\pi$,

$$
\frac1T\int_0^Te^{jp\omega_0t}\,dt=\frac{e^{jp\omega_0T}-1}{jp\omega_0T}=\frac{e^{j2\pi p}-1}{j2\pi p}=0,
$$

while for $p=0$ the integrand is 1 and the average is 1. Multiply the series by $e^{-jl\omega_0t}$ and average over a period. Every term except $n=l$ vanishes:

$$
\boxed{
U_n=\frac1T\int_0^Tu(t)\,e^{-jn\omega_0t}\,dt
}
$$

Read this as *how much of $e^{jn\omega_0t}$ the signal contains*.

For the square wave, the integral runs only over the "on" half. For $n\ne0$, use $\omega_0T=2\pi$:

$$
U_n=\frac1T\int_0^{T/2}e^{-jn\omega_0t}\,dt
=\frac1T\left[\frac{e^{-jn\omega_0t}}{-jn\omega_0}\right]_0^{T/2}
=\frac{1-e^{-jn\omega_0T/2}}{jn\omega_0T}
=\frac{1-e^{-jn\pi}}{jn\omega_0T}
=\frac{1-(-1)^n}{j2\pi n}.
$$

Here $\omega_0T/2=\pi$, $e^{-jn\pi}=(-1)^n$, and $\omega_0T=2\pi$ in the denominator. The numerator $1-(-1)^n$ is 2 for odd $n$ and 0 for even $n$.

Compute the mean separately: $U_0=(1/T)\int_0^{T/2}1\,dt=1/2$. Thus

$$
\boxed{
U_0=\tfrac12,
\qquad
U_n=\frac{1}{j\pi n}\ \ (n\text{ odd}),
\qquad
U_n=0\ \ (n\text{ even},\ n\neq0)
}
$$

$U_0$ is the average force, $\tfrac12$ N. The even harmonics vanish because the "on" and "off" halves are the same length.

### 3.4 Back to real form {#section-3-4}

Pair positive $n$ with $-n$ exactly as in [§2.2](#section-2-2). For positive odd $n$, $U_{-n}=1/(j\pi(-n))=-U_n$, so

$$
U_ne^{jn\omega_0t}+U_{-n}e^{-jn\omega_0t}
=\frac{1}{j\pi n}\left(e^{jn\omega_0t}-e^{-jn\omega_0t}\right)
=\frac{1}{j\pi n}\cdot2j\sin n\omega_0t
=\frac{2}{\pi n}\sin n\omega_0t ,
$$

using $e^{j\theta}-e^{-j\theta}=2j\sin\theta$. Therefore

$$
\boxed{
u(t)=\frac12+\frac2\pi\left(\sin\omega_0t+\frac13\sin3\omega_0t+\frac15\sin5\omega_0t+\cdots\right)
}
$$

### 3.5 Convergence and the Gibbs phenomenon {#section-3-5}

Near a jump, the partial sums overshoot. Adding harmonics narrows the oscillations, but the overshoot approaches about 8.949% of the jump and does not tend to zero. At the jump itself the series converges to the midpoint. Demo 9 reports peaks of $1.1366$, $1.0912$ and $1.0895$ for $N=1$, $9$ and $199$. This is the **Gibbs phenomenon**. For this 0/1 square wave, the series gives $1/2$ at every switching instant, regardless of which endpoint value we assign to the input.

**What "well-behaved" means.** The series converges to $u(t)$ wherever $u$ is continuous, and to the midpoint of each jump, when three conditions hold over one period: $u$ is absolutely integrable, has finitely many maxima and minima, and has finitely many finite jumps. These **Dirichlet conditions** are sufficient for the piecewise-smooth periodic waveforms used here; they are not necessary conditions for every Fourier representation. Ideal impulses require a generalized interpretation ([§5](#section-5)).

## 4. Driving the spring-mass-damper with a square wave {#section-4}

### 4.1 The response, harmonic by harmonic {#section-4-1}

Apply superposition from [§2.1](#section-2-1) to the series. Each harmonic's amplitude is multiplied by $G$ at its own frequency:

$$
X_n=G(jn\omega_0)\,U_n,
\qquad
G(s)=\frac1{ms^2+cs+k}.
$$

In real form: the $n=0$ term is $G(0)U_0=G(0)/2$. For positive odd $n$, pair $X_n$ with $X_{-n}=\overline{X_n}$ as in [§2.2](#section-2-2). Write $U_n=\frac{1}{\pi n}e^{-j\pi/2}$ and $G(jn\omega_0)=|G|e^{j\angle G}$. Then

$$
X_ne^{jn\omega_0t}+X_{-n}e^{-jn\omega_0t}
=2\Re\{X_ne^{jn\omega_0t}\}
=\frac{2}{\pi n}|G|\cos\!\left(n\omega_0t+\angle G-\tfrac\pi2\right)
=\frac{2}{\pi n}|G|\sin\!\left(n\omega_0t+\angle G\right).
$$

Summing,

$$
\boxed{
x_{ss}(t)=\frac{G(0)}2+\sum_{n=1,3,5,\ldots}\frac2{\pi n}\,\big|G(jn\omega_0)\big|\sin\!\big(n\omega_0t+\angle G(jn\omega_0)\big)
}
$$

The subscript "ss" means steady state. As in [Lecture 1, §5](modeling-and-dynamics-poles_student.md#section-5), the complete response adds the free modes, and they decay here because $m>0$, $k>0$ and $c>0$.

### 4.2 Numbers that make the point {#section-4-2}

Use $m=1$ kg, $c=1$ N·s/m, $k=25$ N/m. Then:
- $\omega_n=\sqrt{k/m}=5$ rad/s;
- $\zeta=c/(2\sqrt{mk})=1/10=0.1$;
- the roots of $s^2+s+25$ give poles at $-0.5\pm j\sqrt{25-0.25}=-0.5\pm j4.975$.

Pick the period so that the **third** harmonic lands on the natural frequency: $3\omega_0=5$ gives $\omega_0=5/3$ rad/s, and $T=2\pi/\omega_0=3.770$ s.

**How each row is computed.** At $s=j\omega$, $G(j\omega)=\dfrac{1}{(k-m\omega^2)+jc\omega}$. So $|G|=1/\sqrt{(k-m\omega^2)^2+c^2\omega^2}$ and $\angle G=-\operatorname{atan2}(c\omega,\ k-m\omega^2)$. The force amplitude is $2/(\pi n)$, and the motion amplitude is the product.
- *$n=1$:* $\omega=1.667$, $k-m\omega^2=25-2.778=22.222$, $c\omega=1.667$. So $|G|=1/\sqrt{493.83+2.78}=0.04487$, $\angle G=-\arctan(1.667/22.222)=-4.3^\circ$, and the motion amplitude is $0.6366\times0.04487=0.02857$.
- *$n=3$:* $\omega=5$, $k-m\omega^2=0$, so $G=1/(j5)$. Then $|G|=0.2$ and $\angle G=-90^\circ$, giving $0.2122\times0.2=0.04244$.
- *$n=5$:* $k-m\omega^2=25-69.44=-44.44$ is negative, so the phase passes $-90^\circ$ toward $-180^\circ$.

| Harmonic $n$ | $n\omega_0$ [rad/s] | force amplitude [N] | $\lvert G\rvert$ [m/N] | $\angle G$ | motion amplitude [m] |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0.5000 | 0.04000 | $0^\circ$ | 0.02000 |
| 1 | 1.667 | 0.6366 | 0.04487 | $-4.3^\circ$ | 0.02857 |
| 3 | 5.000 | 0.2122 | 0.20000 | $-90.0^\circ$ | **0.04244** |
| 5 | 8.333 | 0.1273 | 0.02211 | $-169.4^\circ$ | 0.00282 |
| 7 | 11.667 | 0.0909 | 0.00895 | $-174.0^\circ$ | 0.00081 |
| 9 | 15.000 | 0.0707 | 0.00499 | $-175.7^\circ$ | 0.00035 |

For positive odd $n$, $|U_n|=1/(\pi n)$ is one complex coefficient; the real sine amplitude in the table is $2|U_n|$. For $n=0$ the amplitude column holds the mean value. The mean displacement $G(0)/2=0.02$ m is the static spring deflection under the mean force of $0.5$ N: $0.5/k=0.02$ m.

Two features of the table explain the output:

1. **The input's harmonics fall off as $1/n$.** The third harmonic of the force is one third the size of the fundamental.
2. **The output's third harmonic is 1.49 times its fundamental** ($0.04244/0.02857=1.486$). The third harmonic lies near the resonance peak. At $3\omega_0=\omega_n$, the gain is exactly $1/(c\omega_n)=0.2$ m/N. The third harmonic is the largest component, but the fundamental remains substantial: the output still has fundamental frequency $\omega_0$ and period $T$.

For this force-to-displacement transfer function, $|G(j\omega)|^{-2}=(k-m\omega^2)^2+c^2\omega^2$. Its minimum gives, for $0<\zeta<1/\sqrt2$,

$$
\omega_r=\omega_n\sqrt{1-2\zeta^2},\qquad
|G(j\omega_r)|=\frac1{c\omega_n\sqrt{1-\zeta^2}}.
$$

**Derivation.** Let $w=\omega^2$ and $f(w)=(k-mw)^2+c^2w$. Setting $f'(w)=-2m(k-mw)+c^2=0$ gives $w=\dfrac km-\dfrac{c^2}{2m^2}$. With $c=2\zeta\omega_nm$, this is $w=\omega_n^2-2\zeta^2\omega_n^2$, so $\omega_r=\omega_n\sqrt{1-2\zeta^2}$. This requires $1-2\zeta^2>0$, i.e. $\zeta<1/\sqrt2$; otherwise the minimum of $f$ is at $\omega=0$ and there is no peak. At the minimum, $k-mw=c^2/(2m)$, so

$$
f=\frac{c^4}{4m^2}+c^2\left(\frac km-\frac{c^2}{2m^2}\right)=\frac{c^2k}{m}-\frac{c^4}{4m^2}=c^2\omega_n^2\left(1-\frac{c^2}{4mk}\right)=c^2\omega_n^2(1-\zeta^2),
$$

and $|G(j\omega_r)|=1/\sqrt f$.

Here $\omega_r=5\sqrt{0.98}=4.94975$ rad/s and the peak is $1/(1\cdot5\sqrt{0.99})=0.201008$ m/N. The peak frequency, natural frequency $5$ rad/s, and imaginary part of the poles $4.97494$ rad/s are distinct.

Above the resonance, $|G|$ falls as roughly $1/(m\omega^2)$, so the output's harmonics fall as roughly $1/n^3$: a $1/n$ force coefficient times a $1/n^2$ gain. These absolutely summable displacement coefficients give a smooth reconstruction: displacement and velocity are continuous. Acceleration jumps when the force switches, so its Fourier reconstruction can still exhibit Gibbs oscillations.

#### Check your understanding

> Keep the same plant, but make the damping zero and leave $\omega_0=5/3$. Which harmonic prevents a bounded periodic steady state?

**Answer:** The nonresonant harmonics retain sinusoidal particular solutions, with gains changed by removing damping. In the real sine series the third harmonic is resonant (both $n=+3$ and $n=-3$ in the complex series). Its equation is

$$
\ddot x+25x=\frac{2}{3\pi}\sin5t,\qquad
\boxed{x_{p,3}(t)=-\frac{t}{15\pi}\cos5t.}
$$

The forcing amplitude is the $n=3$ sine coefficient, $2/(3\pi)$. Indeed, $(D^2+25)(t\cos5t)=-10\sin5t$. To see this:
- $\frac{d}{dt}(t\cos5t)=\cos5t-5t\sin5t$.
- $\frac{d^2}{dt^2}(t\cos5t)=-5\sin5t-5\sin5t-25t\cos5t=-10\sin5t-25t\cos5t$.
- Adding $25t\cos5t$ leaves $-10\sin5t$.
- Similarly, $(D^2+25)(t\sin5t)=10\cos5t$.

With the trial $t(a\cos5t+b\sin5t)$, matching $-10a\sin5t+10b\cos5t=\frac{2}{3\pi}\sin5t$ gives $a=-\frac{1}{15\pi}$ and $b=0$. The same-exponential trial fails because $G(j5)$ is undefined. The resonant response grows without bound; there is no bounded periodic steady state, and homogeneous oscillations no longer decay.

## 5. Narrow pulses and the ideal impulse limit {#section-5}

Replace the square wave with a train of pulses of width $\varepsilon<T$ and height $1/\varepsilon$, each of unit area, arriving every $T$ seconds. Projection gives

$$
U_n=\frac1T\int_0^\varepsilon\frac1\varepsilon e^{-jn\omega_0t}\,dt
=\frac1T e^{-jn\omega_0\varepsilon/2}
\operatorname{sinc}\!\left(\frac{n\omega_0\varepsilon}{2}\right),
\qquad \operatorname{sinc}(z)=\frac{\sin z}{z},\quad \operatorname{sinc}(0)=1.
$$

**Derivation.** Let $x=n\omega_0\varepsilon/2$. The integral is $\dfrac{1}{T\varepsilon}\cdot\dfrac{1-e^{-j2x}}{jn\omega_0}$. Factor out the midpoint phase: $1-e^{-j2x}=e^{-jx}(e^{jx}-e^{-jx})=e^{-jx}\cdot2j\sin x$. Then

$$
U_n=\frac{1}{T\varepsilon}\cdot\frac{2j\sin x}{jn\omega_0}\,e^{-jx}
=\frac1T\cdot\frac{\sin x}{n\omega_0\varepsilon/2}\,e^{-jx}
=\frac1Te^{-jx}\operatorname{sinc}x .
$$

The phase $e^{-jx}$ is the delay to the pulse's centre at $t=\varepsilon/2$. For $n=0$, $U_0=\frac1T\int_0^\varepsilon\frac1\varepsilon\,dt=\frac1T$ directly.

For **each fixed $n$**, $x\to0$ and $\operatorname{sinc}x\to1$, so $U_n\to1/T$ as $\varepsilon\to0$. For a finite pulse, the coefficients are approximately $1/T$ only when $|n\omega_0\varepsilon|\ll1$; higher-frequency coefficients decay and have zeros. The limit is not uniform over all harmonics.

The ideal unit-impulse train has coefficients $1/T$ at every harmonic. Its Fourier series represents a distribution, not an ordinary pointwise-convergent function.

For our stable plant, the periodic response to this ideal train has coefficients

$$
X_n=\frac{G(jn\omega_0)}{T}.
$$

A **single** unit impulse applied from rest produces the impulse response $h(t)$. Its Laplace transform is $G(s)$; for this stable plant, its Fourier transform is $G(j\omega)$. The impulse response characterizes the system's zero-state input-output behavior, a connection developed further in [§7](#section-7).

## 6. From a finite pulse to a step: why $e^{-\sigma t}$ {#section-6}

### 6.1 From a sum to an integral: keep pulse duration fixed {#section-6-1}

Stretching the 50%-duty square wave does approach a step at each fixed nonzero time, but its coefficients $U_0=1/2$ and $U_n=1/(j\pi n)$ for odd $n$ do **not** shrink with $T$. That limit alone cannot justify turning its Fourier series into an ordinary Fourier integral.

Instead, let $p_L(t)=1$ on $0<t<L$ and zero elsewhere. Hold $L$ fixed and repeat the pulse with period $T>L$, calling the periodic signal $p_{L,T}$. Its coefficients are

$$
P_{n,T}=\frac1T\int_0^L e^{-jn\omega_0t}\,dt
=\frac1T P_L(jn\omega_0),\qquad \omega_0=\frac{2\pi}{T},
$$

where

$$
P_L(j\omega)=\int_0^Le^{-j\omega t}\,dt=\frac{1-e^{-j\omega L}}{j\omega}\quad(\omega\ne0),
\qquad P_L(0)=L.
$$

The integral over one period only sees the pulse, because $p_{L,T}=0$ on $L<t<T$. So the coefficient is $1/T$ times the isolated pulse's integral evaluated at the harmonic frequency.

Now $TP_{n,T}$ samples one fixed function of frequency. Increasing $T$ separates pulses without changing their shape. With $\Delta\omega=2\pi/T$, write $1/T=\Delta\omega/(2\pi)$ in $p_{L,T}=\sum_nP_{n,T}e^{jn\omega_0t}$. The series is

$$
p_{L,T}(t)=\frac1{2\pi}\sum_{n=-\infty}^{\infty}
P_L(jn\Delta\omega)e^{jn\Delta\omega t}\,\Delta\omega.
$$

On a finite frequency interval this has the form of a Riemann sum. Fourier inversion for this piecewise-smooth, integrable pulse gives the corresponding isolated-pulse representation:

$$
\boxed{
p_L(t)=\frac1{2\pi}\lim_{\Omega\to\infty}
\int_{-\Omega}^{\Omega}P_L(j\omega)e^{j\omega t}\,d\omega
}
$$

The inverse is a **symmetric improper integral**: it gives the pulse at continuity points and $1/2$ at either jump. The Riemann-sum picture motivates the formula; passing to unbounded frequencies requires the Fourier inversion theorem, not just shrinking harmonic spacing.

More generally, for suitable integrable signals,

$$
U(j\omega)=\int_{-\infty}^{\infty}u(t)e^{-j\omega t}\,dt,
\qquad
u(t)=\frac1{2\pi}\lim_{\Omega\to\infty}
\int_{-\Omega}^{\Omega}U(j\omega)e^{j\omega t}\,d\omega,
$$

with sufficient regularity such as piecewise smoothness and the same midpoint convention. Only **after isolating the pulse** do we let $L\to\infty$ to obtain a step. This second limit is the problem to examine next.

### 6.2 Why the step's ordinary Fourier integral fails {#section-6-2}

Now try the step itself, $u(t)=1$ for $t\ge0$:

$$
U(j\omega)=\int_0^\infty e^{-j\omega t}\,dt
=\lim_{t_f\to\infty}\frac{1-e^{-j\omega t_f}}{j\omega},\qquad \omega\ne0.
$$

The limit does not exist. As $t_f$ grows, the partial integral runs around a circle of radius $1/|\omega|$ centred on $1/(j\omega)$, forever. To see the circle, write the partial integral as $\dfrac1{j\omega}-\dfrac{e^{-j\omega t_f}}{j\omega}$: a fixed centre plus a term of constant magnitude $1/|\omega|$ whose angle keeps turning. [Practice Problem 4](#practice-problems-with-answers) works through this. At $\omega=0$, the partial integral equals $t_f$ and diverges linearly.

**Why it fails.** The step never decays, so there is always more signal to integrate, and $e^{-j\omega t}$ keeps turning. A ramp and a growing exponential such as $e^{2t}$ also fail to have ordinary Fourier transforms defined by this integral.

**Fourier series and Fourier integrals have different convergence questions.** A Fourier coefficient integrates over one finite period; even a constant signal has a Fourier series. Here the problem is an ordinary integral over an infinite time interval. A step also has a generalized Fourier transform, but that requires distribution theory and is outside this addendum.

### 6.3 The fix: weight by $e^{-\sigma t}$ {#section-6-3}

Multiply by a decaying exponential before transforming. This weight is chosen for convergence; it is not the plant's decay rate. For a pulse of duration $L$, as $L\to\infty$,

$$
\int_0^L e^{-(\sigma+j\omega)t}\,dt=\frac{1-e^{-(\sigma+j\omega)L}}{\sigma+j\omega}\;\longrightarrow\;\frac1{\sigma+j\omega},\qquad \sigma>0.
$$

The limit exists because $|e^{-(\sigma+j\omega)L}|=e^{-\sigma L}|e^{-j\omega L}|=e^{-\sigma L}\to0$. The turning factor still turns, but the decaying factor shrinks the circle to a point. Thus any $\sigma>0$ makes the step integral converge:

$$
\int_0^\infty e^{-\sigma t}e^{-j\omega t}\,dt
=\int_0^\infty e^{-(\sigma+j\omega)t}\,dt
=\frac1{\sigma+j\omega}.
$$

Name the combination $s=\sigma+j\omega$:

$$
\boxed{
\int_0^\infty1\cdot e^{-st}\,dt=\frac1s,
\qquad\Re(s)>0
}
$$

This is the pair used in [Lecture 1, §17.1](modeling-and-dynamics-poles_student.md#section-17-1) to switch on the heater.

### 6.4 The weight comes back out {#section-6-4}

For the ordinary signals here, define the **causal extension** $u(t)=0$ for $t<0$, and its Laplace transform

$$
U(s)=\int_0^\infty u(t)e^{-st}\,dt.
$$

Choose $\sigma$ so that $u(t)e^{-\sigma t}$ is absolutely integrable, and assume sufficient regularity for Fourier inversion, such as piecewise smoothness. Its Fourier transform is then $U(\sigma+j\omega)$, because

$$
\int_{-\infty}^{\infty}\left[u(t)e^{-\sigma t}\right]e^{-j\omega t}\,dt=\int_0^\infty u(t)e^{-(\sigma+j\omega)t}\,dt=U(\sigma+j\omega),
$$

using $u=0$ for $t<0$. Apply the Fourier inversion of [§6.1](#section-6-1) to the weighted signal, so at continuity points

$$
u(t)e^{-\sigma t}=\frac1{2\pi}\lim_{\Omega\to\infty}
\int_{-\Omega}^{\Omega}U(\sigma+j\omega)e^{j\omega t}\,d\omega.
$$

Undo the weight by multiplying both sides by $e^{+\sigma t}$. Since $\sigma$ is fixed, it can go inside the integral, where $e^{\sigma t}e^{j\omega t}=e^{(\sigma+j\omega)t}=e^{st}$. Now change variables to $s=\sigma+j\omega$. On the vertical line $\sigma$ is constant, so $ds=j\,d\omega$, i.e. $d\omega=ds/j$. The limits $\omega=\pm\Omega$ become $s=\sigma\pm j\Omega$, and the prefactor becomes $\frac1{2\pi}\cdot\frac1j$:

$$
\boxed{
u(t)=\frac1{2\pi j}\lim_{\Omega\to\infty}
\int_{\sigma-j\Omega}^{\sigma+j\Omega}U(s)e^{st}\,ds
}
$$

This is the inversion formula in [Lecture 1, §15](modeling-and-dynamics-poles_student.md#section-15), interpreted by symmetric frequency truncation. At a jump it recovers the midpoint of the two one-sided limits; the step's value at zero is therefore $1/2$ under inversion, regardless of its assigned endpoint value.

The vertical line contains exponentials $e^{(\sigma+j\omega)t}$: the transform uses $e^{-\sigma t}$, while reconstruction uses $e^{+\sigma t}$. A step requires $\sigma>0$; sufficiently decaying signals can allow $\sigma=0$ or negative $\sigma$.

To pass this representation through a causal LTI system using convolution, choose the line in a **common convergence region** for the input and the system's causal impulse response, with sufficient convergence to interchange the integrals. Avoiding isolated poles alone is not enough. For our stable plant and a step, any $\sigma>0$ lies in both regions.

### 6.5 The other standard inputs {#section-6-5}

The same weight handles the rest of the familiar inputs:

Here $1(t)$ denotes the causal unit step: zero for $t<0$ and one for $t>0$.

| Input | Convergence or idealization | Transform |
|---|---|---|
| Impulse $\delta(t)$ | A single ideal impulse has a flat transform; no decay weight is needed. | $1$ for every $s$ |
| Step $1(t)$ | The signal never decays | $1/s$, $\ \Re(s)>0$ |
| Ramp $t\,1(t)$ | The signal grows without bound | $1/s^2$, $\ \Re(s)>0$ |
| $e^{2t}\,1(t)$ | The signal grows exponentially | $1/(s-2)$, $\ \Re(s)>2$ |

For the impulse row, use the $0^-$ convention of [Lecture 1, §15](modeling-and-dynamics-poles_student.md#section-15): $\mathcal L\{\delta(t)\}=\int_{0^-}^\infty\delta(t)e^{-st}\,dt=1$, including the impulse at zero. For ordinary signals, writing 0 as the lower limit has the same effect.

The region of convergence makes the requirement precise: the weight must suppress the signal's growth. For example, $e^{2t}e^{-\sigma t}=e^{-(\sigma-2)t}$ decays only when $\sigma>2$.

The ramp is [Practice Problem 5](#practice-problems-with-answers). For the exponential, $\int_0^\infty e^{2t}e^{-st}\,dt=\int_0^\infty e^{-(s-2)t}\,dt=\dfrac1{s-2}$. This is the step result with $s$ replaced by $s-2$, so it needs $\Re(s-2)>0$, i.e. $\Re(s)>2$. In general, a signal growing like $e^{at}$ needs $\sigma>a$.

## 7. Two ways to take a signal apart {#section-7}

There are two complementary ways to build a signal and compute its response:

| | Build from impulses | Build from exponentials |
|---|---|---|
| Building block | a shifted impulse $\delta(t-\tau)$ | an exponential $e^{st}$ |
| What the system returns | $h(t-\tau)$, a different shape | $G(s)e^{st}$ as a particular response, away from poles |
| How the pieces combine | convolution, an integral over time | multiplication by $G(s)$, one frequency at a time |

Both describe the same LTI system, with the convergence conditions of [§6.4](#section-6-4) when using inverse integrals. The exponential entry is a particular response: switching an exponential on at zero generally also produces natural-mode transients, even from rest. Convolution with $h$ gives the complete zero-state response; nonzero initial conditions add a zero-input response. Scaling exponentials is what makes the transform algebra simple.

For a causal system initially at rest, convolution gives

$$
x(t)=\int_0^t h(t-\tau)u(\tau)\,d\tau,
\qquad
\boxed{X(s)=G(s)U(s)}.
$$

The product formula holds where the transforms and convolution converge. For example, a unit step applied to our spring-mass-damper from rest gives

$$
X(s)=\frac{1}{s(ms^2+cs+k)}.
$$

Partial fractions and transform pairs recover the complete switched response, including the transient. Nonzero initial conditions contribute additional terms, as shown in [Lecture 1, §17](modeling-and-dynamics-poles_student.md#section-17).

**Choose the computation to suit the input.** Use harmonic sums for a periodic steady state. Use transform pairs and partial fractions when a switched input gives a rational transform. The exponential representation explains why the same transfer function serves both calculations.

---

## 8. Quick reference {#section-8}

| Task | Formula or condition |
|---|---|
| Finite exponential input | $u=\sum_n U_ne^{s_nt}$ gives $x_p=\sum_nG(s_n)U_ne^{s_nt}$, away from poles |
| Sinusoidal response | $A\cos\omega t$ gives $A\lvert G(j\omega)\rvert\cos(\omega t+\angle G(j\omega))$ as a particular response |
| Periodic input | $u=\sum_{n=-\infty}^{\infty}U_ne^{jn\omega_0t}$, with $\omega_0=2\pi/T$ |
| Fourier coefficient | $U_n=(1/T)\int_0^T u(t)e^{-jn\omega_0t}\,dt$ |
| Stable plant's periodic response | $X_n=G(jn\omega_0)U_n$, with appropriate convergence |
| Laplace transform | $U(s)=\int_{0^-}^{\infty}u(t)e^{-st}\,dt$ |
| Unit step | $U(s)=1/s$, $\Re(s)>0$ |
| Complete zero-state response | $X(s)=G(s)U(s)$ in a common convergence region |

A Fourier series recovers the midpoint at a jump, and its partial sums exhibit Gibbs oscillations nearby. A periodic response computed from harmonics is the steady state; an input switched on at zero generally also excites natural-mode transients. The choice of transform weight $\sigma$ ensures convergence and does not specify the plant's physical decay rate.

---

## Review questions and answers

**1. Which two model properties let exponentials pass through independently?**

**Answer:** Constant coefficients make an exponential trial retain its shape under the differential operator. Linearity lets us add and scale the separate particular responses. The simple gain formula also requires that the input rates avoid poles.

**2. How could nonzero even harmonics appear in the square wave?**

**Answer:** Change the duty cycle from one half. If the force is 1 on $0<t<DT$ and 0 for the rest of the period, then $U_0=D$ and $U_n=(1-e^{-j2\pi nD})/(j2\pi n)$ for $n\ne0$. Nonzero even harmonics generally appear; each produces an output coefficient $G(jn\omega_0)U_n$, so one near resonance may be strongly amplified.

**3. A triangle wave is the integral of a square wave with its mean removed. How do its harmonic amplitudes decay?**

**Answer:** Integration divides each nonzero coefficient by $jn\omega_0$. The square wave's $1/n$ decay therefore becomes $1/n^2$ for the triangle wave. Its smoother shape has smaller high-frequency components, so fewer harmonics are needed for a useful approximation.

**4. Why does the displacement contain much less of the high harmonics than the force?**

**Answer:** At high frequency, the inertia term dominates: $G(j\omega)\approx-1/(m\omega^2)$. Multiplying the square wave's $1/n$ coefficients by this $1/n^2$ gain gives displacement coefficients of order $1/n^3$. Displacement and velocity remain continuous even though the force and acceleration jump.

**5. If the third harmonic is largest in the output, has the fundamental frequency changed?**

**Answer:** No. In the worked example, the first harmonic remains nonzero, so the output's fundamental frequency is still $\omega_0$ and its period is still $T$. The largest component happens to be the third harmonic.

**6. Why does adding harmonics not remove the square wave's overshoot?**

**Answer:** Gibbs overshoot approaches about 8.949% of the jump. More harmonics make the oscillations narrower, while the peak overshoot persists. At the jump itself, the series converges to the midpoint.

**7. What does the ratio between the step transform $1/s$ and the impulse transform 1 tell us?**

**Answer:** A causal step is the time integral of an impulse. Integration from rest contributes a factor $1/s$ in the transform domain. Consequently the step response is the time integral of the impulse response.

**8. If a signal's region of convergence is $\Re(s)>2$, can its transform integral be evaluated at $s=j\omega$?**

**Answer:** No. The imaginary axis lies outside that region, so setting $s=j\omega$ is not justified by the defining integral. For $e^{2t}1(t)$, the rational expression $1/(s-2)$ has finite values on the imaginary axis, but those values are an analytic continuation, not values of a convergent Fourier integral of the signal.

**9. Why do we first increase $T$ at fixed pulse duration $L$, and only afterward let $L$ grow?**

**Answer:** Increasing $T$ at fixed $L$ separates identical pulses and gives coefficients $P_{n,T}=P_L(jn\omega_0)/T$, which form a frequency Riemann sum. Lengthening the isolated pulse then approaches a step and exposes the failure of ordinary Fourier convergence. Stretching a 50%-duty square wave changes pulse width and spacing together, leaving its indexed coefficients unchanged; that alone does not justify the same sum-to-integral argument.

**10. Does choosing $\sigma=0.5$ mean the system has a pole at $-0.5$?**

**Answer:** No. The transform weight is chosen to make the integral converge. The plant's poles are fixed by its dynamics. For the step, any $\sigma>0$ works; using the inverse integral through a system also requires a line in a common convergence region for the input and the causal impulse response.

---

## Practice problems with answers {#practice-problems-with-answers}

**Problem 1 — a symmetric square wave.** Let $v(t)=\pm1$, with $+1$ on the first half period. Write $v$ in terms of the 0/1 square wave $u$ of [§3](#section-3), and use the result to find the $V_n$ without integrating.

**Answer:** $v=2u-1$, so $V_0=0$, $V_n=2/(j\pi n)$ for odd $n$, and $V_n=0$ for even $n\neq0$. The coefficients are linear in the signal. Scaling by 2 doubles every $U_n$, and subtracting the constant 1 changes only the $n=0$ coefficient: $V_0=2(\tfrac12)-1=0$.

**Problem 2 — move the resonance.** Using the plant of [§4.2](#section-4-2), set $\omega_0=5$ rad/s so that the *fundamental* sits on $\omega_n$. Find the motion amplitudes of harmonics 1, 3 and 5, and compare with the table in [§4.2](#section-4-2).

**Answer:** $0.1273$, $0.00106$ and $0.00021$ m. The working uses $|G(j\omega)|=1/\sqrt{(25-\omega^2)^2+\omega^2}$:
- $n=1$, $\omega=5$: $|G|=1/5=0.2$, and $0.6366\times0.2=0.1273$.
- $n=3$, $\omega=15$: $|G|=1/\sqrt{200^2+15^2}=1/200.56=0.00499$, and $0.2122\times0.00499=0.00106$.
- $n=5$, $\omega=25$: $|G|=1/\sqrt{600^2+25^2}=1/600.5=0.00167$, and $0.1273\times0.00167=0.00021$.

The fundamental now dominates by a factor of about 120 ($0.1273/0.00106$). Close to the resonance, the output is nearly a pure sinusoid at the forcing frequency, however square the force.

**Problem 3 — undamped periodic forcing.** Set $c=0$ in [§4.2](#section-4-2), keeping $\omega_0=5/3$. Show that every term of the formal harmonic particular-response sum in real sine form is still defined except one. Find the particular solution for that term and explain why no bounded periodic steady state exists.

**Answer:** Only the real third harmonic fails (indices $\pm3$ in the complex series). For $\ddot x+25x=2\sin5t/(3\pi)$, the trial $t(a\cos5t+b\sin5t)$ gives $a=-1/(15\pi)$ and $b=0$, hence $x_{p,3}=-t\cos5t/(15\pi)$. Its envelope grows linearly. Other harmonics retain sinusoidal particular solutions with changed gains, while homogeneous oscillations do not decay.

**Problem 4 — the circle.** For real $\omega\ne0$, show that $I(t_f)=\int_0^{t_f}e^{-j\omega t}\,dt$ satisfies $\big|I(t_f)-1/(j\omega)\big|=1/|\omega|$ for every $t_f$. Then show that $\int_0^{t_f}e^{-st}\,dt\to1/s$ when $\Re(s)>0$.

**Answer:** $I-1/(j\omega)=-e^{-j\omega t_f}/(j\omega)$, whose magnitude is $1/|\omega|$. At $\omega=0$, $I(t_f)=t_f$ diverges linearly. With $\Re(s)=\sigma>0$, $|e^{-st_f}|=e^{-\sigma t_f}\to0$.

**Problem 5 — the ramp.** Compute $\int_0^\infty t\,e^{-st}\,dt$ by parts, stating exactly where $\Re(s)>0$ is used.

**Answer:** $1/s^2$. The condition is used in the boundary term $\big[-t\,e^{-st}/s\big]_0^\infty$, which vanishes when $t\,e^{-\sigma t}\to0$, and in the remaining integral $\int_0^\infty e^{-st}\,dt=1/s$, whose convergence also requires $\Re(s)>0$.

**Problem 6 — a nonlinear spring.** A mass on a spring with force $kx+k_3x^3$ is driven by $F\cos\omega t$. Assume a small response $x\approx X\cos\omega t$ and substitute. Identify the term that no single-frequency response can balance.

**Answer:** $k_3X^3\cos^3\omega t$ contains $\tfrac14k_3X^3\cos3\omega t$. A third harmonic is forced, so no single amplitude-independent LTI transfer function describes the full nonlinear model. A specified linearization can have a transfer function.

---

## Optional computational example

The accompanying [demo9_square_wave_harmonics.py](demos/demo9_square_wave_harmonics.py) recomputes the numerical results and compares a harmonic reconstruction with direct integration of the equation of motion. From the directory containing these notes:

```sh
cd demos
uv run python demo9_square_wave_harmonics.py
```

Use `--show` for an interactive plot or `--no-save` to skip writing figures. The default run saves PNG and SVG figures in `demos/figures/`.

| Panel | What to examine |
|---|---|
| (a) Square-wave reconstruction | Partial sums through harmonics 1, 3, 9, and 49 approach the square wave; the oscillations narrow near each jump. The terminal also compares projected coefficients with their analytical values. |
| (b) Harmonic gains | The third motion harmonic exceeds the fundamental by about 1.49. The gain curve is normalized by its DC value; force and motion harmonics are each normalized by their own fundamental amplitudes. These are dimensionless quantities with different references. |
| (c) Response comparison | Direct ODE integration from rest approaches the harmonic steady state. The comparison uses the last two of 20 periods and retains harmonics through $n=399$. |
| (d) Transform convergence | At $\omega=2$ rad/s, the unweighted step integral circles forever. With $\sigma=0.5$, it approaches $1/(0.5+2j)=(0.5-2j)/4.25=0.1176-0.4706j$; by $t_f=40$ s the remaining error factor is $e^{-20}\approx2\times10^{-9}$. |

The supplied example reports a maximum sampled displacement discrepancy of about $9.3\times10^{-8}$ m against a peak-to-peak motion of about $0.135$ m. At the comparison window's start, the transient envelope has been reduced by $e^{-0.5(18T)}=e^{-0.5\times67.86}=e^{-33.93}\approx1.8\times10^{-15}$; this is a dimensionless reduction factor, not a displacement error. The discrepancy includes numerical integration and Fourier truncation errors and varies with the numerical environment. Agreement between the two calculations illustrates superposition; it does not replace the convergence argument.
