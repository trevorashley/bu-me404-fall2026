# From Physical Models to the Laplace Transform
## Exponential Modes, Poles, Zeros, Noncollocation, and Zero Dynamics

**Audience:** Introductory controls / differential equations / dynamic systems

**Primary goal:** Motivate the Laplace transform from physical modeling rather than introduce it as a purely formal integral transform.

**Duration:** Budget about 65 minutes for Part I, including a worked Laplace step response, when students already know basic ODEs and complex numbers. Part II is an optional 45-minute second lecture on zeros and geometry. Part III is reference material. See §3 for shorter routes and material to prepare as slides.

**Math rendering:** This document uses `$ ... $` for inline math and `$$ ... $$` for display math, which renders in GitHub-flavored Markdown, Pandoc (`--mathjax`), VS Code preview, and Obsidian. If you compile through LaTeX instead, the same delimiters pass through unchanged.

**Notation conventions used throughout:**

| Symbol | Meaning |
|---|---|
| $\tau$ | time constant (never torque) |
| $M$ | applied torque or moment |
| $m_p,\ l$ | pendulum mass and pivot-to-center-of-mass distance |
| $j$ | imaginary unit |
| $s$ | complex exponential rate: solve for it in free motion; choose it when testing a forced response |
| $s_i$ | a system-selected natural rate, located on the $s$-plane |
| $A$ | complex amplitude in $x = Ae^{st}$; local coefficient/matrix uses in §27/§32 are defined there |
| $\mathcal A(s)$ | Laplace transform of a beam angle $\alpha(t)$ |

Physical masses, inertias, capacitances, resistances, and restoring stiffnesses are positive unless stated otherwise; damping coefficients are nonnegative. Amplitudes such as $X$ and $U$ are numbers. Transforms such as $X(s)$ and $U(s)$ are introduced in §18.

---

# Part 0 — Planning

## 1. Teaching strategy

The central narrative of this lecture is:

$$
\boxed{
\text{physical law}
\rightarrow
\text{ODE}
\rightarrow
e^{st}
\rightarrow
\text{algebra in }s
\rightarrow
\text{poles and zeros}
\rightarrow
\text{Laplace transform}
}
$$

The key pedagogical idea is to introduce

$$
x(t)=Ae^{st}
$$

**before** introducing the Laplace transform.

The reason exponentials matter is simple:

$$
\frac{d}{dt}e^{st}=se^{st},
\qquad
\frac{d^2}{dt^2}e^{st}=s^2e^{st}.
$$

For exponentials, differentiation becomes multiplication.

That single observation gives students a reason to care about the variable $s$, and it prepares them for the later Laplace-transform property

$$
\mathcal L\{\dot x\}
=
sX(s)-x(0^-).
$$

A useful framing line for the lecture is:

> **We are going to keep asking the same question: what exponential motions are compatible with the physics?**

There are three moments the lecture is built around. Protect them even if you have to cut elsewhere:

1. **§8** — the forced response turns the characteristic polynomial into the *denominator of a transfer function*. This is where poles stop being a definition and become inevitable.
2. **§14** — holding the measured output at zero does not stop the system. This is where zeros become physical.
3. **§18–§20** — the Laplace transform extends the exponential calculation to signals with a transform, and a switched heater gives a complete time-response example.

---

## 2. Learning objectives

By the end of Part I, students should be able to:

1. Derive simple linear ODEs from physical principles.
2. Explain why $e^{st}$ is special for linear constant-coefficient ODEs.
3. Interpret $s=\sigma+j\omega$ in terms of growth, decay, and oscillation, and locate a given $s$ on the $s$-plane.
4. Derive characteristic equations from physical models.
5. Interpret transfer-function poles as the **natural exponential rates visible through the chosen input-output channel** (a pole is a rate, not the mode itself).
6. Reconstruct a real solution from a complex-conjugate pair of modes.
7. Compute a transfer function by driving a model with $e^{st}$, and relate its denominator to the characteristic polynomial, allowing for cancellations.
8. Predict how zeros change when the sensor is moved, and explain why the internal dynamics remain unchanged.
9. Interpret zero dynamics as internal motion consistent with zero measured output.
10. State and use $\mathcal L\{\dot x\}=sX(s)-x(0^-)$, explain the initial-condition term, and obtain the thermal step response by transforming and inverting.

Additional objectives for Part II:

11. Determine, for a given input-output geometry, whether a mechanical system has a right-half-plane zero.
12. Explain why right-half-plane zeros are associated with nonminimum-phase behavior and with bandwidth limits.
13. Distinguish an unstable pole from a right-half-plane zero, and give an example of a stable, nonminimum-phase plant.

---

## 3. Suggested lecture flow

### Part I — core lecture (about 65 minutes, with prepared algebra)

| Time | Topic | Section |
|---:|---|---|
| 0–5 min | Why exponentials? Introduce $e^{st}$ | §4 |
| 5–13 min | Thermal system: free response, then forcing $\rightarrow$ first transfer function | §5 |
| 13–24 min | Spring-mass-damper; complex $s$; recovering real solutions | §6–§7 |
| 24–30 min | Forced spring-mass-damper: the transfer function; poles = characteristic roots | §8 |
| 30–37 min | Pendulum, two linearizations, and the $s$-plane | §9–§10 |
| 37–52 min | Two-mass system: poles, zeros, zero dynamics, moving the sensor | §11–§17 |
| 52–65 min | Laplace transform, worked thermal step response, and summary | §18–§23 |

Prepare the §7.4 numerical table and §12–§13 cofactor algebra as slides/handouts. In the final block, explain the $0^-$ convention briefly, show the inversion formula without evaluating a contour, and use §21 as a comparison slide rather than another board derivation. Read the closing script over the §22 summary. For students new to ODEs or complex numbers, allow another session rather than compressing these introductions.

### Part II — optional second lecture (45 minutes)

| Time | Topic | Section |
|---:|---|---|
| 0–8 min | Ball-and-beam: underactuation and internal coordinates | §24 |
| 8–16 min | Flexible structures, noncollocation, hard-disk drives | §25–§26 |
| 16–26 min | A stable nonminimum-phase rigid body | §27 |
| 26–36 min | Quadrotor with and without a sensor offset | §28–§30 |
| 36–45 min | Zero dynamics in general; why RHP zeros limit control | §31–§34 |

### Runnable demonstrations

Eight Python demos live in `demos/`. Each one recomputes the lecture's numbers
rather than quoting them, prints a short narrative to the terminal, and writes a
figure to `demos/figures/`. Cue blocks marked **[ DEMO n ]** appear at the point
in the script where each belongs.

```
cd demos
uv run python demo5_zero_dynamics.py          # one demo
uv run python demo5_zero_dynamics.py --show   # interactive window, for live use
uv run python run_all.py                      # regenerate every figure (~18 s)
```

**Three are worth running live**, because they settle claims students are right
to doubt: **Demo 2** (§7.4, damping does not slide poles left), **Demo 5** (§14,
the sensor reads zero while the machine moves) and **Demo 8** (§29, a RHP zero as
visible unstable motion). The rest work better as prepared figures on a slide —
see §39 for the full index.

### Fitting a hard 55-minute slot

The 65-minute route already assumes prepared cofactor algebra, so do not count that preparation again as a saving. For a hard 55-minute slot, use the shorter route below and allow the remaining time for questions. If retaining the two-mass sequence in the first session is essential, plan the longer slot or assign part of the derivation as prior work; the full sequence should not depend on students having no questions.

Protect §18–§20, including the worked thermal step response. The Laplace transform is the title of the lecture.

For a first encounter with Laplace transforms, an alternative is §4–§10 followed by §18–§23 — thermal, spring-mass-damper, complex $s$, pendulum, and Laplace — with the two-mass sequence starting the next session. Budget about 50 minutes for that route. The remaining enrichment then needs additional time or selected examples; moving the two-mass material does not make it disappear from the course. The default sequence below retains all three protected moments in Part I.

---

# Part I — The core lecture

## 4. Opening: why $e^{st}$?

### Instructor script

> Today I do not want to begin with the Laplace-transform integral.
> I want to begin with physical systems.
>
> We are going to derive a few differential equations, and every time we will ask the same question:
>
> **What happens if the motion has the form**
>
> $$x(t)=Ae^{st}?$$
>
> The symbol $s$ denotes an exponential rate. In a free-motion problem it is unknown and the physics selects it. In a forced problem we choose the test rate and solve for the response amplitude. We will allow $s$ to be complex from the start:
>
> $$s=\sigma+j\omega.$$
>
> I am not going to make $s$ complex later as a trick. It is complex now. Some systems will simply happen to pick values that sit on the real axis.
>
> The systems themselves will tell us which values of $s$ are possible.

### Write on the board

$$
x(t)=Ae^{st}
$$

$$
\dot x=sAe^{st}
$$

$$
\ddot x=s^2Ae^{st}
$$

Then box:

$$
\boxed{
\frac{d}{dt}
\text{ acts like multiplication by }s
\text{ on }e^{st}
}
$$

### Ask the class

- What other familiar functions have derivatives proportional to themselves?
- Why might that be useful in a differential equation?
- What units must $s$ have?

Expected answer:

$$
[s]=\text{time}^{-1}.
$$

Follow up: $\sigma$ carries units of inverse seconds (nepers per second), and $\omega$ carries radians per second. Both halves of $s$ are rates.

---

## 5. Thermal system

Consider a lumped thermal body connected to an environment through a thermal resistance.

Let

- $T(t)$: body temperature,
- $T_a$: ambient temperature,
- $C$: thermal capacitance,
- $R$: thermal resistance,
- $q_{\text{in}}(t)$: externally supplied heat flow (used in §5.4).

A sketch:

```text
        q_in
         |
         v            thermal resistance R
       T(t) o------/\/\/\/\/\/\------o  T_a  (ambient)
         |
        ===  C   (thermal capacitance)
         |
       -----  reference
```

### 5.1 Derivation from first principles

The stored thermal energy changes at the rate

$$
C\dot T .
$$

The heat flow from the body to ambient is

$$
q=\frac{T-T_a}{R}.
$$

With no external heat input, conservation of energy gives

$$
C\dot T=-\frac{T-T_a}{R}.
$$

Define deviation from equilibrium:

$$
x(t)=T(t)-T_a.
$$

Since $T_a$ is constant,

$$
\dot x=\dot T.
$$

Therefore

$$
\boxed{
C\dot x+\frac1R x=0
}
$$

### 5.2 The free response

#### Instructor script

> We have reduced a physical thermal problem to a first-order linear differential equation.
>
> Now I am going to try a function whose derivative has exactly the same shape as the original function. I do **not** know its exponential rate yet, so I will call that unknown rate $s$.

Assume

$$
x(t)=Ae^{st}.
$$

Then

$$
\dot x=s Ae^{st}.
$$

Substitute:

$$
Cs Ae^{st}+\frac1R Ae^{st}=0.
$$

Factor:

$$
\left(Cs+\frac1R\right)Ae^{st}=0.
$$

Since $e^{st}$ is never zero, a nontrivial solution ($A \neq 0$) requires

$$
Cs+\frac1R=0.
$$

Thus

$$
\boxed{
s=-\frac1{RC}
}
$$

and therefore

$$
x(t)=Ae^{-t/(RC)}.
$$

Using $x(0)$,

$$
\boxed{
x(t)=x(0)e^{-t/(RC)}
}
$$

### 5.3 Interpretation

The differential equation

$$
C\dot x+\frac1R x=0
$$

became the algebraic equation

$$
Cs+\frac1R=0.
$$

Emphasize:

$$
\boxed{
\text{ODE}
\rightarrow
\text{algebra in an unknown rate}
}
$$

The natural value of $s$ is negative and real. Therefore the mode decays without oscillating. The system selected this rate; no input was specified.

The time constant is

$$
\tau=RC,
\qquad
s=-\frac1\tau.
$$

#### Ask the class

> If $R$ becomes larger, does the system respond faster or slower?

Expected reasoning: $\tau=RC$ increases, so $|s|=1/(RC)$ decreases, the pole moves *toward the origin*, and the response becomes slower. Keep that phrase — "toward the origin" — because §10 will turn it into a picture.

### 5.4 Adding an input: the first transfer function

So far the body has just been left alone. Now let a heater supply $q_{\text{in}}(t)$:

$$
C\dot T=q_{\text{in}}-\frac{T-T_a}{R},
$$

so in deviation coordinates

$$
\boxed{
C\dot x+\frac1R x=q_{\text{in}}
}
$$

This is a different question from the free response. We now **choose** the test-input rate $s$, instead of solving for a natural rate. For this chosen input, look for a **particular** response of the same shape:

$$
q_{\text{in}}=Qe^{st},
\qquad
x_p=Xe^{st}.
$$

Substituting and cancelling $e^{st}$,

$$
\left(Cs+\frac1R\right)X=Q,
$$

so

$$
\boxed{
\frac{X}{Q}
=
\frac{1}{Cs+\dfrac1R}
=
\frac{R}{RCs+1}
=
\frac{R}{\tau s+1}
}
$$

This ratio defines a function of the chosen test rate, away from the natural rate:

$$
\boxed{
G(s)
=
\frac{R}{\tau s+1}
}
$$

#### Instructor script

> Pause over the two roles of $s$. In the **free** problem, set the input to zero and solve for the allowed rates. In the **forced** problem, choose a test rate and solve for the response amplitude. The differential equation supplies the same polynomial in both calculations.
>
> This ratio is our first **transfer function**. Read it as: *if I push on this system with the exponential $e^{st}$, this is the complex number the system multiplies it by.*
>
> Now look at where it fails to be defined. Undefined gain here does not mean an infinite time signal; it means our same-exponential forced-response assumption has collided with a natural mode.
>
> The denominator vanishes at $s = -1/\tau$ — and that is exactly the natural rate $s$ we found in §5.2 with no input at all.
>
> That is not a coincidence, and it is going to keep happening. In the free problem, values of $s$ that kill this polynomial are values at which the system can produce an output with **no input**. Those are the natural modes. In the forced problem, choosing the same rate for a nonzero input makes the same-exponential particular-response formula fail. We will soon call those shared values poles.

Box:

$$
\boxed{
\text{denominator}=0
\iff
\text{motion is possible with no input}
}
$$

---

## 6. Spring-mass-damper

Now move to a mechanical system. The spring and damper act **in parallel**, both connecting the wall to the mass:

```text
   wall
    |
    |----/\/\/\/\----+
    |       k        |
    |               [ m ]  ----> x
    |                |
    |----[==c==]-----+
    |
```

Let

- $m$: mass,
- $c$: viscous damping coefficient,
- $k$: spring stiffness,
- $x(t)$: displacement from the unstretched-spring position.

For free motion, Newton's second law gives

$$
m\ddot x=-c\dot x-kx,
$$

therefore

$$
\boxed{
m\ddot x+c\dot x+kx=0
}
$$

### 6.1 Apply the same exponential idea

Assume

$$
x(t)=Ae^{st}.
$$

Then

$$
\dot x=sAe^{st},
\qquad
\ddot x=s^2Ae^{st}.
$$

Substitute:

$$
ms^2Ae^{st}+csAe^{st}+kAe^{st}=0.
$$

Factor:

$$
\left(ms^2+cs+k\right)Ae^{st}=0.
$$

Therefore

$$
\boxed{
ms^2+cs+k=0
}
$$

This is the **characteristic equation**.

### Instructor script

> Notice that I did exactly the same thing as in the thermal system.
>
> The thermal system produced a first-degree polynomial in $s$.
>
> This second-order mechanical system produces a second-degree polynomial in $s$.

Write side-by-side:

$$
C\dot x+\frac1R x=0
\quad\Longrightarrow\quad
Cs+\frac1R=0
$$

$$
m\ddot x+c\dot x+kx=0
\quad\Longrightarrow\quad
ms^2+cs+k=0
$$

Then say:

> The order of the differential equation has become the degree of a polynomial.

### 6.2 How many modes should we expect?

Worth one minute, because students otherwise wonder where the "extra" constants come from:

> The solution space of an $n$th-order linear ODE is $n$-dimensional — you need $n$ initial conditions to pin down a solution. Generically the characteristic polynomial has $n$ distinct roots, giving $n$ independent modes $e^{s_1t},\dots,e^{s_nt}$, and by linearity any sum of them is also a solution. So counting works out: $n$ roots, $n$ free constants, $n$ initial conditions.
>
> The word "generically" is doing real work there. §7.2 is the case where it fails.

---

## 7. Complex $s$: damping and oscillation

Solve

$$
ms^2+cs+k=0.
$$

The roots are

$$
\boxed{
s_{1,2}
=
\frac{-c\pm\sqrt{c^2-4mk}}{2m}
}
$$

For $m,k>0$ and $c\ge0$, separate the undamped boundary $c=0$ from the three positive-damping cases.

### 7.1 Overdamped: $c^2>4mk$

The roots are real and distinct. Moreover, for physical parameters $m,c,k>0$ **both roots are always negative** — this is guaranteed, not typical:

$$
\sqrt{c^2-4mk}<\sqrt{c^2}=c,
$$

so both numerators $-c\pm\sqrt{c^2-4mk}$ are negative. Hence

$$
s_1<0,
\qquad
s_2<0.
$$

The response is

$$
x(t)=A_1e^{s_1t}+A_2e^{s_2t},
$$

a sum of two decaying exponentials. No oscillation occurs.

That one-line sign argument is worth the board space: it is the first time students see stability read off the *coefficients* rather than the roots, which is the seed of Routh-style reasoning later.

### 7.2 Critically damped: $c^2=4mk$

There is a repeated root

$$
s=-\frac{c}{2m},
$$

and only one exponential — but §6.2 says we need two independent solutions. The generalized form supplies the second:

$$
x(t)=(A+Bt)e^{st}.
$$

Mention it, verify by substitution if you have the time, and move on.

**The substitution, if there is time.** The $Ae^{st}$ part solves the equation already, so check only $x=te^{st}$. Its derivatives are $\dot x=(1+st)e^{st}$ and $\ddot x=(2s+s^2t)e^{st}$. Substituting and grouping by powers of $t$:

$$
m\ddot x+c\dot x+kx=\big[\underbrace{(ms^2+cs+k)}_{=0\text{ (root)}}\,t+\underbrace{(2ms+c)}_{=0\text{ at }s=-c/2m}\big]e^{st}=0 .
$$

The first bracket vanishes because $s$ is a root. The second vanishes *only* because the root is repeated: $2ms+c$ is the derivative of the characteristic polynomial, and a repeated root is also a root of the derivative. For distinct roots the second bracket is nonzero, and $te^{st}$ is not a solution.

### 7.3 Undamped: $c=0$

The roots are purely imaginary:

$$
s=\pm j\sqrt{\frac{k}{m}}
=\pm j\omega_n .
$$

Here $\sigma=0$: neither growth nor decay, just sustained oscillation at the natural frequency $\omega_n=\sqrt{k/m}$.

This oscillatory case returns as a zero in the undamped antiresonance (§15) and for the above-CM quadrotor output (§29). The quadrotor's repeated poles at the origin are different: they can produce polynomial motion (§10).

### 7.4 Underdamped: $0<c<2\sqrt{mk}$

The roots are a complex-conjugate pair. Here $c^2-4mk<0$, so write $\sqrt{c^2-4mk}=j\sqrt{4mk-c^2}$ in the quadratic formula and split it into its real and imaginary parts:

$$
s_{1,2}=\frac{-c}{2m}\pm j\frac{\sqrt{4mk-c^2}}{2m} .
$$

Write them explicitly in terms of the physical parameters:

$$
\boxed{
s_{1,2}=\sigma\pm j\omega_d,
\qquad
\sigma=-\frac{c}{2m},
\qquad
\omega_d=\frac{\sqrt{4mk-c^2}}{2m}
}
$$

Note what each parameter does — and be careful here, because the obvious guess is wrong. Damping does **not** simply slide the poles left. Squaring and adding,

$$
\sigma^2+\omega_d^2
=
\frac{c^2}{4m^2}+\frac{4mk-c^2}{4m^2}
=
\frac km
=\omega_n^2 ,
$$

so at fixed $m$ and $k$ the pair has **constant magnitude** $\omega_n$ from zero damping through critical damping. Increasing $c$ moves the pair along the left semicircle: leftward and toward the real axis, where the roots meet at $c=2\sqrt{mk}$. Beyond critical damping, they split along the real axis: one moves farther left, while the other approaches the origin. More damping does not always mean a faster response.

Within the underdamped range, stiffness behaves differently. At fixed $m$ and $c$, increasing $k$ leaves $\sigma=-c/(2m)$ untouched and raises $\omega_d$, so the conjugate roots move vertically apart.

$$
\boxed{
\begin{array}{ll}
\text{more damping, up to critical} & \rightarrow \text{leftward toward the real axis on } |s|=\omega_n\\[3pt]
\text{more stiffness, underdamped} & \rightarrow \text{vertically away from the real axis}
\end{array}}
$$

Worth a numerical demonstration on the board, with $m=1$, $k=25$ (so $\omega_n=5$). Each row uses $\sigma=-c/2$ and $\omega_d=\sqrt{100-c^2}/2$. For example, $c=4$ gives $\omega_d=\sqrt{84}/2=4.58$, and $|s|=\sqrt{4+21}=5$:

| $c$ | $\sigma$ | $\omega_d$ | $\lvert s\rvert$ |
|---:|---:|---:|---:|
| $0$ | $0$ | $5.00$ | $5$ |
| $4$ | $-2$ | $4.58$ | $5$ |
| $8$ | $-4$ | $3.00$ | $5$ |
| $9.9$ | $-4.95$ | $0.71$ | $5$ |

That constant-radius arc is the first root locus students will ever see, and it costs nothing to show it here.

> **[ DEMO 2 ]** — `demo2_damping_pole_locus.py` *(live, ~30 s)*
>
> **Show:** the left panel — the pole pair walking around the circle $|s|=\omega_n$ as $c$ runs from 0 to critical, then splitting along the real axis.
> **Point at:** the $|s|$ column for the underdamped cases. It reads 5.0000 there; the script reports a maximum deviation of about $1.8\times10^{-15}$ across that range.
> **Say:** "Up to critical damping, both coordinates move along the circle while the magnitude stays fixed. After the roots meet, one moves back toward the origin."
> **Why live:** this pre-empts the wrong intuition before students form it, and the right panel ties each pole location to a waveform they recognise.

Now expand the exponential. With $s=\sigma+j\omega$,

$$
e^{st}
=
e^{(\sigma+j\omega)t}
=
e^{\sigma t}e^{j\omega t},
$$

and by Euler's identity

$$
e^{j\omega t}
=
\cos\omega t+j\sin\omega t.
$$

Thus a complex exponential contains two physically meaningful pieces:

$$
\boxed{
\sigma
=
\text{growth or decay rate}
}
\qquad
\boxed{
\omega
=
\text{oscillation frequency}
}
$$

### 7.5 Getting a real answer back

This is the question every student asks and most lectures skip:

> **My displacement is a real number. Where did the $j$ go?**

The answer is that complex roots of a real polynomial come in conjugate pairs, and for $x(t)$ to be real the coefficients must be conjugates too. Writing $A_2=\overline{A_1}$,

$$
x(t)=A_1e^{s_1t}+\overline{A_1}e^{\overline{s_1}t}
=2\,\Re\!\left\{A_1e^{(\sigma+j\omega_d)t}\right\},
$$

The first equality holds because a number plus its conjugate is twice its real part, and $\overline{A_1e^{s_1t}}=\overline{A_1}e^{\overline{s_1}t}$ for real $t$.

**Expand it.** Write $A_1=\alpha+j\beta$ with $\alpha,\beta$ real, and use Euler's identity:

$$
A_1e^{(\sigma+j\omega_d)t}
=e^{\sigma t}(\alpha+j\beta)(\cos\omega_dt+j\sin\omega_dt)
=e^{\sigma t}\left[(\alpha\cos\omega_dt-\beta\sin\omega_dt)+j(\beta\cos\omega_dt+\alpha\sin\omega_dt)\right].
$$

Twice the real part is $e^{\sigma t}(2\alpha\cos\omega_dt-2\beta\sin\omega_dt)$. This is the form students already know, with $B=2\alpha$ and $C=-2\beta$:

$$
\boxed{
x(t)=e^{\sigma t}
\left(
B\cos\omega_d t
+
C\sin\omega_d t
\right)
}
$$

with $B$ and $C$ real and fixed by the initial conditions. Equivalently,

$$
x(t)=Re^{\sigma t}\cos(\omega_d t+\psi),
\qquad
R=\sqrt{B^2+C^2}=2|A_1|,
\qquad
\psi=\angle A_1 ,
$$

since $2\Re\{|A_1|e^{j\psi}e^{j\omega_dt}\}=2|A_1|\cos(\omega_dt+\psi)$. Problem 6 (§37) has $A_1=1-j/3$, which gives $B=2$ and $C=2/3$.

#### Instructor script

> The imaginary parts did not disappear. They cancelled, because they always arrive in pairs.
>
> A complex mode is not a physical motion by itself. A conjugate pair is. The envelope $e^{\sigma t}$ comes from the real part of $s$, and the ringing inside it comes from the imaginary part.

> **[ DEMO 3 ]** — `demo3_real_from_complex.py` *(slide, or live if the board is going badly)*
>
> **Show:** the upper panel first — one complex mode alone, with a large imaginary part. Then the lower panel, where the pair adds to a real motion.
> **Point at:** the printed line `max |Im(mode1 + mode2)| = 0.000e+00`.
> **Numbers:** this is Problem 6. The script solves for $A_1 = 1 - j/3$ from the initial conditions and lands on $e^{-t}(2\cos 3t + \tfrac23\sin 3t)$, cross-checked against a numerical ODE solve to $5\times10^{-12}$.
> **Say:** "Neither of those complex curves is a motion the mass could perform. Only their sum is."

### Instructor script — closing §7

> The thermal system did not require us to invent a new variable.
>
> It simply selected a real natural rate.
>
> The spring-mass-damper selects complex natural rates when it oscillates.
>
> A natural rate was always allowed to be complex.
>
> The first system simply happened to live on the real axis.

---

## 8. Forcing the spring-mass-damper: the transfer function

§6–§7 described free motion: set the force to zero and solve for the natural rates $s_1,s_2$. Now repeat the forced-response calculation of §5.4: choose an input rate $s$ and solve for the response amplitude.

Include an external force:

$$
m\ddot x+c\dot x+kx=f(t).
$$

Choose a test-input rate $s$ and drive the system with that exponential. Unlike a natural rate, $s$ is chosen by us. Look for a **particular** solution of the same shape:

$$
f=Fe^{st},
\qquad
x_p=Xe^{st}.
$$

Substituting,

$$
\left(ms^2+cs+k\right)Xe^{st}=Fe^{st},
$$

and cancelling $e^{st}$,

$$
\left(ms^2+cs+k\right)X=F.
$$

Therefore

$$
\boxed{
G(s)
=
\frac{X}{F}
=
\frac{1}{ms^2+cs+k}
}
$$

### What this object is

The expression above applies for every chosen test rate $s$ that is not a natural rate.

$G(s)$ is the **complex gain the system applies to a test exponential $e^{st}$**. Feed in $e^{st}$; get out $G(s)e^{st}$ as the particular response. That is the entire content of the definition.

Three remarks, all worth making out loud:

**1. This is the particular solution only.** The complete response is

$$
x(t)=\underbrace{G(s)Fe^{st}}_{\text{forced}}
+\underbrace{A_1e^{s_1t}+A_2e^{s_2t}}_{\text{free modes from §7}},
$$

Here $s$ is the chosen test-input rate, while $s_1,s_2$ are the natural rates. The initial conditions determine $A_1,A_2$, including when the system starts from rest. This display assumes distinct roots; at critical damping use $(A+Bt)e^{s_1t}$. For positive damping the homogeneous part decays, with ringing only in the underdamped case; at zero damping it can persist.

**2. The denominator is the characteristic polynomial.** Not a similar polynomial — the *same* one, letter for letter, that came out of §6.1:

$$
\underbrace{ms^2+cs+k}_{\text{§6: free modes}}
\quad=\quad
\underbrace{ms^2+cs+k}_{\text{§8: denominator of }G(s)}
$$

Ask the class why. The answer is the box from §5.4: in the free problem, at a root of the denominator, the equation $(ms^2+cs+k)X=F$ has a nonzero solution $X$ when $F=0$. A root of the denominator is precisely a rate the system can sustain with no input — which is what a natural mode *is*. In the forced problem, choosing that same rate for a nonzero input means the ordinary same-exponential particular solution no longer exists.

$$
\boxed{
\text{poles of }G(s)
=
\text{roots of the characteristic equation}
=
\text{natural exponential rates}
}
$$

**Scope of the pole interpretation.** In these one-coordinate models, every natural rate appears as a transfer-function pole. For a general state model, a mode must be both excitable by the input and visible at the output to appear in the reduced transfer function. Common factors can cancel; §16–§17 returns to this point.

**3. A note on notation, so nothing surprises them later.** Here $X$ and $F$ are complex *amplitudes* — numbers. In §18 we will define $X(s)$ and $F(s)$ as Laplace *transforms* — functions. For zero initial conditions these give the identical ratio, which is why the same symbol $G(s)$ serves both. Say this once, now, and the transition in §20 will be uneventful.

### One free sentence with a large payoff

> Choose $s=j\omega$, away from any pole: a pure oscillation with no growth or decay. Then $G(j\omega)$ gives the sinusoidal particular response: its magnitude is the amplitude ratio and its angle is the phase shift. If the free transients decay, this is the eventual response. That is the frequency response, and it is where Bode plots come from.

---

## 9. Rotational version: the pendulum

Now convert the translational mechanical system into a rotational one.

Let

- $\theta$: pendulum angle, measured from straight down,
- $J$: rotational inertia about the pivot,
- $b$: rotational viscous damping,
- $m_p$: pendulum mass,
- $l$: distance from pivot to center of mass,
- $M$: applied torque.

The exact nonlinear equation is

$$
\boxed{
J\ddot\theta+b\dot\theta+m_pgl\sin\theta=M
}
$$

### 9.1 Linearization about the downward equilibrium

For small angles around $\theta=0$, use $\sin\theta\approx\theta$. Then

$$
\boxed{
J\ddot\theta+b\dot\theta+m_pgl\,\theta=M
}
$$

Compare with

$$
m\ddot x+c\dot x+kx=f.
$$

The correspondence is structural, not a substitution — note that the $m$ on the left below is the translational mass of §6, while $m_p$ is the pendulum mass:

$$
m\leftrightarrow J,
\qquad
c\leftrightarrow b,
\qquad
k\leftrightarrow m_pgl.
$$

Gravity is acting as a **rotational spring** of stiffness $m_pgl$.

For free motion with $\theta=Ae^{st}$,

$$
\boxed{
Js^2+bs+m_pgl=0
}
$$

#### Instructor script

> Locally, a pendulum near its downward equilibrium looks just like a rotational spring-mass-damper.
>
> The nonlinear system has become linear because we chose an operating point and considered small perturbations around it.

### 9.2 Linearization about the upright equilibrium

Now let

$$
\theta=\pi+\phi
$$

where $\phi$ is a small perturbation around upright. Since

$$
\sin(\pi+\phi)=-\sin\phi\approx-\phi,
$$

the linearized equation becomes

$$
\boxed{
J\ddot\phi+b\dot\phi-m_pgl\,\phi=M
}
$$

The rotational stiffness has changed sign. Gravity is no longer a restoring spring; it is a *destabilizing* one.

For free motion with $\phi=Ae^{st}$,

$$
\boxed{
Js^2+bs-m_pgl=0
}
$$

The product of the roots is $-m_pgl/J<0$, so the two roots are real with **opposite signs**. (The product of the roots of $a_2s^2+a_1s+a_0$ is $a_0/a_2$. A complex pair has product $|s|^2>0$, so a negative product rules out complex roots.) Explicitly,

$$
s_{1,2}=\frac{-b\pm\sqrt{b^2+4Jm_pgl}}{2J},
$$

and $\sqrt{b^2+4Jm_pgl}>b$, so the "$+$" root is strictly positive for any damping. One of them therefore lies in the right half plane:

$$
e^{st},
\qquad
\Re(s)>0 .
$$

That is a mode that grows on its own. The pendulum falls over.

---

## 10. The $s$-plane

Everything so far has been sign conditions in prose. Draw the picture once and they become locations.

### Board diagram

```text
                             Im(s) = omega
                                   ^
                                   |
          decaying                 |                growing
        oscillation   x            |            x   oscillation
          (§7.4)                   |                  (too much
                                   x  sustained         loop gain)
                                   |  oscillation
                                   |  (§7.3, c = 0)
    -----x----------x--------------+-------------x---------------> Re(s) = sigma
       fast        slow            |          upright
       decay       decay           |          pendulum
       (small RC)  (large RC)      |          (§9.2)
                                   x
                                   |
                      x            |            x
                                   |
     <---------- LHP: decay -------|------- RHP: growth ---------->
```

> **[ DEMO 1 ]** — `demo1_splane_modes.py` *(slide; project it beside the board sketch)*
>
> **Show:** both panels together. Left is where each pole sits, right is what it does, colour-matched.
> **Use it for:** the walk down the table below. Rather than describing each case, point at the pair.
> **Say:** "Farther left means faster exponential decay; off the real axis means oscillation. A right-half-plane pole gives exponential growth. Poles on the axis need a separate check."

### The three rules

$$
\boxed{
\Re(s)<0
\Rightarrow
\text{decay}
}
\qquad
\boxed{
\Re(s)>0
\Rightarrow
\text{growth}
}
\qquad
\boxed{
\Im(s)\neq0
\Rightarrow
\text{oscillation}
}
$$

### Location $\rightarrow$ motion $\rightarrow$ example

Walk down this table, sketching the little time-domain waveform beside each location on the board. This is the single highest-value board in the lecture.

| Location of $s$ | $x(t)$ looks like | Example in this lecture |
|---|---|---|
| Far left, real axis | Fast decay, no ringing | Thermal body, small $RC$ (§5) |
| Near origin, real axis | Slow decay, no ringing | Thermal body, large $RC$ (§5) |
| Upper/lower LHP pair | Decaying oscillation | Underdamped spring-mass-damper (§7.4) |
| Simple pair on the $j\omega$ axis, away from zero | Constant-amplitude free oscillation | Undamped spring-mass ($c=0$, §7.3) |
| Upper/lower RHP pair | Growing oscillation | Unstable flutter, servo with too much gain |
| Right, real axis | Pure growth, no ringing | Upright pendulum (§9.2) |
| At the origin | Constant; repeated scalar roots also allow powers of $t$ | Free mass: $m\ddot x=0$ gives $x=x_0+v_0t$ |

#### Instructor script

> For a mode, farther left means faster decay, and a nonzero imaginary part means oscillation. All state eigenvalues strictly in the LHP give asymptotic stability; a RHP eigenvalue gives exponential instability. On the imaginary axis, free motion may persist or grow polynomially — a free mass with initial velocity already shows why “no RHP pole” is not enough.

**Instructor note:** Bounded-input/bounded-output (BIBO) stability asks whether every bounded input gives a bounded zero-state output. For a reduced proper rational transfer function, it requires every pole strictly in the LHP; even the undamped oscillator can grow under resonant forcing. For state-model free motion, semisimple imaginary-axis eigenvalues permit bounded motion, while nontrivial Jordan blocks add powers of $t$. A repeated state eigenvalue by itself does not prove polynomial growth.

---

## 11. Add a second mass: flexible two-mass system

Now extend the spring-mass-damper. The wall connects to $m_1$ through $(k_1,c_1)$, and $m_1$ connects to $m_2$ through $(k_2,c_2)$. The input force $u(t)$ acts on $m_1$:

```text
   wall                 u
    |                   |
    |                   v
    |--(k1, c1)--[  m1  ]--(k2, c2)--[  m2  ]
    |                    |                |
    |                   x1 --->          x2 --->
```

The equations of motion are

$$
m_1\ddot x_1
+c_1\dot x_1+k_1x_1
+c_2(\dot x_1-\dot x_2)
+k_2(x_1-x_2)
=u
$$

and

$$
m_2\ddot x_2
+c_2(\dot x_2-\dot x_1)
+k_2(x_2-x_1)
=0.
$$

Collect terms:

$$
m_1\ddot x_1
+(c_1+c_2)\dot x_1
+(k_1+k_2)x_1
-c_2\dot x_2
-k_2x_2
=u
$$

$$
m_2\ddot x_2
+c_2\dot x_2+k_2x_2
-c_2\dot x_1-k_2x_1
=0.
$$

---

## 12. Exponential form for the two-mass system

Choose a test rate $s$, as in §8, and seek a particular response with two coordinates. Here $X_1,X_2,U$ are complex amplitudes:

$$
x_1=X_1e^{st},
\qquad
x_2=X_2e^{st},
\qquad
u=Ue^{st}.
$$

Each derivative becomes a factor of $s$: $\dot x_i\to sX_ie^{st}$ and $\ddot x_i\to s^2X_ie^{st}$. Cancel $e^{st}$ from every term of the two collected equations of §11. The first becomes $[m_1s^2+(c_1+c_2)s+(k_1+k_2)]X_1-(c_2s+k_2)X_2=U$, and the second becomes $-(c_2s+k_2)X_1+(m_2s^2+c_2s+k_2)X_2=0$. In matrix form:

$$
\begin{bmatrix}
m_1s^2+(c_1+c_2)s+(k_1+k_2)
&
-(c_2s+k_2)
\\[4pt]
-(c_2s+k_2)
&
m_2s^2+c_2s+k_2
\end{bmatrix}
\begin{bmatrix}
X_1\\
X_2
\end{bmatrix}
=
\begin{bmatrix}
U\\
0
\end{bmatrix}.
$$

Define the coupling dynamic stiffness (force per relative displacement)

$$
K_2(s)=c_2s+k_2 .
$$

Then the matrix takes a form that shows the structure clearly:

$$
\begin{bmatrix}
m_1s^2+c_1s+k_1+K_2(s)
&
-K_2(s)
\\
-K_2(s)
&
m_2s^2+K_2(s)
\end{bmatrix}
\begin{bmatrix}
X_1\\
X_2
\end{bmatrix}
=
\begin{bmatrix}
U\\
0
\end{bmatrix}.
$$

The determinant supplies an unreduced common denominator for this plant's transfer functions. If you are tight on time, quote it rather than expanding the cofactors live (§3) — the conceptual payload of this section is §14, not the algebra:

$$
\boxed{
D(s)
=
\left[
m_1s^2+(c_1+c_2)s+(k_1+k_2)
\right]
\left[
m_2s^2+c_2s+k_2
\right]
-
(c_2s+k_2)^2
}
$$

$D(s)$ is a fourth-degree polynomial for the four-state model. Its roots are the natural rates at which the plant can move with $u=0$. They are also poles of an input-output transfer function when no common numerator factor cancels them. We assume no such cancellation in the examples below; moving a sensor never changes the internal dynamics, but it can change which modes remain visible (§16–§17).

---

## 13. Collocated output: measure $x_1$

The actuator acts on $m_1$, and the sensor also measures $x_1$. This is a **collocated** input-output pair: force is applied at the same coordinate whose displacement is measured. Force and displacement are conjugate for virtual work; force and velocity are conjugate for power (§25).

Solving the $2\times2$ system by Cramer's rule, replace the first column of the matrix with the right-hand side $(U,0)^{\mathsf T}$ and divide by $D(s)$:

$$
X_1=\frac{1}{D(s)}\det\begin{bmatrix}U&-K_2(s)\\0&m_2s^2+K_2(s)\end{bmatrix}
=\frac{U\left(m_2s^2+K_2(s)\right)-0}{D(s)} .
$$

With $K_2=c_2s+k_2$, this gives

$$
\boxed{
\frac{X_1}{U}
=
\frac{
m_2s^2+c_2s+k_2
}{
D(s)
}
}
$$

The zeros satisfy

$$
\boxed{
m_2s^2+c_2s+k_2=0
}
$$

This numerator has a beautiful mechanical interpretation, which is the whole point of the next section.

---

## 14. Zero dynamics from the collocated two-mass system

Suppose the measured output is

$$
y=x_1 ,
$$

and now **impose** $x_1(t)\equiv0$ for all time. Then also

$$
\dot x_1=0,
\qquad
\ddot x_1=0.
$$

### What the second equation says

Substituting into the $m_2$ equation:

$$
m_2\ddot x_2+c_2\dot x_2+k_2x_2=0.
$$

Assume $x_2=Ae^{st}$. Then

$$
\boxed{
m_2s^2+c_2s+k_2=0
}
$$

This is exactly the numerator of $X_1/U$. The zeros are the natural exponential rates of the second mass while the first is held still.

### What the *first* equation says — do not skip this

Setting $x_1=\dot x_1=\ddot x_1=0$ in the $m_1$ equation leaves

$$
-c_2\dot x_2-k_2x_2=u,
$$

that is,

$$
\boxed{
u(t)=-\left(c_2\dot x_2+k_2x_2\right)
}
$$

Holding the output at zero is **not free**. It requires a specific, generally nonzero input — and that input is exactly the coupling force that $m_2$ feeds back into $m_1$. The actuator's entire job is to cancel it.

This matters because the formal definition of zero dynamics is *the internal motion under the input that holds $y\equiv0$*. Without the required $u$, the definition is incomplete, and the nonzero $u_0$ in the state-space condition of §32 will look unmotivated.

> **[ DEMO 5 ]** — `demo5_zero_dynamics.py` *(live — this is the strongest demonstration in the lecture)*
>
> **Show:** all three panels. Top: the sensor trace, dead flat. Middle: $x_2$ oscillating with an initial amplitude scale of 1. Bottom: the actuator force, with maximum magnitude 8. Both oscillations decay at rate $0.02\ \mathrm{s}^{-1}$; their envelope falls to about 30% after 60 s.
> **Point at:** the printed `max |x1(t)| over 60 s = 3.2e-17`. The output is zero to machine precision for a full minute while the machine is plainly in motion.
> **Then point at:** the table. The hidden motion rings at $3.99997$ rad/s and decays at $0.02000\ \mathrm{s}^{-1}$, matching the zero pair $-0.02\pm j3.99995$. These are rates of the zero dynamics, not the free plant poles.
> **Say:** "The sensor is telling the truth. It is just not telling you very much."
> **Why live:** students accept "zero output does not mean zero motion" as words. They believe it when they watch a flat line sit above a swinging mass for sixty seconds.

### Instructor script

> Here is a physical way to understand a zero.
>
> Suppose I force the measured coordinate $x_1$ to remain exactly zero. I am allowed to use the actuator to do it.
>
> Does that mean the entire system must be motionless?
>
> No.
>
> The second mass can still move — and in fact it moves exactly as if $m_1$ were bolted to the wall.
>
> The zero dynamics describe the internal motion that can occur while the measured output remains zero, together with the input required to keep it there.

Box:

$$
\boxed{
\text{zero dynamics}
=
\text{internal motion compatible with }y(t)\equiv0
}
$$

And the rule of thumb worth memorizing:

$$
\boxed{
\begin{array}{c}
\text{zeros of this collocated transfer function}\\
=\\
\text{natural rates of the subsystem with the measured coordinate pinned}
\end{array}
}
$$

For $m_2,c_2,k_2>0$, these zero dynamics are stable (both roots in the LHP), so this example is minimum phase. If $c_2=0$ the zeros sit exactly on the $j\omega$ axis, which is the boundary case — see §15 and §17.

---

## 15. Antiresonance

For the undamped coupling $c_2=0$, the zeros are

$$
s=\pm j\sqrt{\frac{k_2}{m_2}}.
$$

This is the §7.3 case, now appearing as a *zero* rather than a pole. At this driving frequency the first mass can remain stationary even while the second mass oscillates: the second mass acts as a tuned absorber, and the force it returns through $k_2$ exactly cancels the applied force.

This is an **antiresonance**, and it is the operating principle of the **dynamic vibration absorber** — and closely related to the tuned mass damper. The distinction is worth one sentence: the undamped absorber here produces an *exact* notch at a single frequency, whereas a practical tuned mass damper is deliberately damped, trading that exact zero for broader but shallower attenuation.

> **[ DEMO 6 ]** — `demo6_antiresonance.py` *(slide)*
>
> **Show:** the frequency-response panel, where the collocated notch goes to an exact null at $\omega=\sqrt{k_2/m_2}=4$ rad/s, then the time traces at right.
> **Point at:** the steady-state table. $|X_1/U|$ at the antiresonance is `0.000e+00` — an exact algebraic zero, not a small number.
> **Also:** the script reports mean stored energy of $0.0625$ in the $m_2$ branch while $x_1\approx0$, which sets up the question below before you ask it.
> **Watch out:** the simulated $x_1$ shows a residue near $4\times10^{-5}$. That is the plant's own transient, which decays only as $e^{-0.027t}$ — not a discrepancy in the steady state. The script says so.

### Ask the class

> If the measured displacement $x_1$ is zero, is the mechanical energy necessarily zero?

No.

The second mass and coupling spring can contain kinetic and potential energy even while $x_1=0$.

This is an excellent place to emphasize the distinction between:

- measured output,
- internal state,
- internal energy.

A single sensor reading gives one projection of the state, not the complete instantaneous state.

---

## 16. Move the sensor: measure $x_2$

Now keep the same physical plant and the same input $u$, but measure

$$
y=x_2 .
$$

Cramer's rule on the same matrix, now replacing the *second* column with $(U,0)^{\mathsf T}$, gives

$$
X_2=\frac{1}{D(s)}\det\begin{bmatrix}m_1s^2+c_1s+k_1+K_2(s)&U\\-K_2(s)&0\end{bmatrix}
=\frac{0-U\cdot\left(-K_2(s)\right)}{D(s)}=\frac{K_2(s)\,U}{D(s)} ,
$$

that is,

$$
\boxed{
\frac{X_2}{U}
=
\frac{
c_2s+k_2
}{
D(s)
}
}
$$

The poles are unchanged, because the physical internal dynamics are unchanged. (This holds provided no pole-zero cancellation occurs; if a numerator root coincided with a denominator root, that mode would become invisible from this output, and the transfer function would no longer tell the whole story. See §17 and §34.)

But the numerator has changed. If $c_2>0$, the single finite zero is

$$
\boxed{
s=-\frac{k_2}{c_2}
}
$$

and if $c_2=0$, there is no finite zero at all — the numerator is the constant $k_2$.

### Instructor script

> We did not change the masses.
>
> We did not change the springs.
>
> We did not change the dampers.
>
> We only changed what we chose to measure.
>
> The poles remained the same.
>
> The zeros changed completely — from a resonant pair to a single real zero, or to none at all.

> **[ DEMO 4 ]** — `demo4_sensor_moves_zeros.py` *(slide — the single best figure for this section)*
>
> **Show:** the two pole-zero maps at left, then the frequency response at right.
> **Point at:** the printed `largest discrepancy between the two pole sets: 0.00e+00`. Not "small" — identical.
> **Then:** both outputs show the two flexible resonances; only the collocated one has a pronounced notch between them. Here $c_2=0.02$, so the notch is not an exact null: $|G_1(j4)|\approx1.249\times10^{-3}$. Demo 6 uses $c_2=0$ for the exact null.
> **Worth adding out loud:** the script marks pole magnitudes near $3.03$ and $5.90$ rad/s and a zero magnitude of $4.00$. These indicate the resonances and notch approximately; with damping, they are not necessarily the exact extrema of the frequency response. The ordering recalls the exact undamped interlacing in §25.

Board statement:

$$
\boxed{
\text{poles are tied to internal dynamics}
}
$$

$$
\boxed{
\text{zeros depend strongly on the input-output pair}
}
$$

This distinction becomes extremely important in control, and Part II is essentially an extended demonstration of it.

---

## 17. Poles and zeros: definitions

Suppose

$$
G(s)=\frac{Y}{U}
=
\frac{N(s)}{D(s)},
$$

where $N$ and $D$ are **coprime** — any common factors have already been cancelled. (Without that condition the definitions below are ambiguous, and §34's warning about pole-zero cancellation has nothing to bite on.)

The poles are the roots of

$$
\boxed{
D(s)=0
}
$$

and the zeros are the roots of

$$
\boxed{
N(s)=0
}
$$

**At a pole**, a corresponding natural mode is visible at the output even with no input. A pole specifies its exponential rate.

**At a zero**, the system blocks that exponential: the $e^{zt}$ *component* of the forced response has zero amplitude at the chosen output. This is why zeros are called transmission zeros.

Be precise about what is and is not blocked, because the loose version of this statement is false. Stay inside the framework of §8: drive the system with

$$
u(t)=Ue^{zt}
$$

and look for the particular response $y_p(t)=Ye^{zt}$. Then $Y=G(z)U$, and at a zero $G(z)=0$, so

$$
Y=0
\qquad\Longrightarrow\qquad
y_p(t)\equiv0 .
$$

The *particular* response contains no $e^{zt}$ component at all. But the complete response is the particular solution plus the homogeneous one, and nothing has switched the homogeneous part off: the plant's own natural modes are still there, excited by the transient and by any nonzero initial condition. So the output need not be identically zero.

What *is* true is the stronger statement §14 already gave us and §32 will formalize: there is an input $u_0e^{zt}$ and a matching initial state $\mathbf x(0)=\mathbf x_0$ such that $\mathbf x(t)=\mathbf x_0e^{zt}$ and the output is identically zero. For a conjugate pair of zeros, combine conjugate trajectories to obtain real motion. Exact blocking requires a compatible initial state.

> At a transfer-function zero, the $e^{zt}$ component of the forced response is blocked at the chosen output. The system may nevertheless be moving internally — and the zero dynamics tell us what that hidden motion is.

### Minimum phase

**Convention for this lecture:** a proper real-rational continuous-time SISO transfer function is called **minimum phase** when its poles and finite zeros are all strictly in the LHP. We discuss pole stability and finite-zero locations separately whenever the plant is not asymptotically stable.

- A RHP zero is a **nonminimum-phase zero**, whether or not the plant has stable poles.
- A zero on the $j\omega$ axis is a boundary case and fails the strict minimum-phase condition.
- “No finite zeros” alone does not establish plant stability.

Some controls texts use “minimum phase” to describe stable zero dynamics independently of plant poles. Naming our convention avoids switching meanings between the stable platform and the quadrotor examples.

### Why the name "minimum phase"?

Relate the name to a concrete comparison:

> Compare stable causal rational systems with the same magnitude response and the same nonzero DC gain. The minimum-phase one has the least phase lag. For a real $z>0$, reflecting a zero from $-z$ to $+z$ while preserving DC gain multiplies in
> $$A_{\mathrm{ap}}(s)=\frac{z-s}{z+s},\qquad |A_{\mathrm{ap}}(j\omega)|=1.$$
> Its phase is $-2\arctan(\omega/z)$: it starts at zero and approaches $-180^\circ$ as frequency increases.

The factor is what you get by dividing the reflected plant by the original. With $G_+(s)=(z-s)R(s)$ and $G_-(s)=(z+s)R(s)$ for the same $R(s)$, both have the same DC gain $zR(0)$, and $G_+=A_{\mathrm{ap}}G_-$. At $s=j\omega$, the numerator $z-j\omega$ and denominator $z+j\omega$ are conjugates, so they have equal magnitude, which gives $|A_{\mathrm{ap}}|=1$. Their angles are $-\arctan(\omega/z)$ and $+\arctan(\omega/z)$, so the quotient's phase is $-\arctan(\omega/z)-\arctan(\omega/z)=-2\arctan(\omega/z)$.

That extra phase lag is one way to see the feedback difficulty. §34 states the associated interpolation constraint.

---

## 18. Transition to the Laplace transform

At this point, return to the observation that has appeared in every single derivation:

$$
\frac{d}{dt}e^{st}=se^{st},
\qquad
\frac{d^2}{dt^2}e^{st}=s^2e^{st}.
$$

### Instructor script

> Every time we tried an exponential, differentiation became multiplication.
>
> That converted differential equations into algebraic equations, and it worked for the thermal body, the spring-mass-damper, the pendulum, and a four-state flexible structure.
>
> But there is a limitation we have been quietly living with. Every input we allowed was itself an exponential, $Fe^{st}$. Real inputs are steps, pulses, ramps, noise.
>
> So here is the natural question:
>
> **Can we represent a general signal as a combination of exponentials, so that this property survives?**
>
> That is exactly what the Laplace transform does.

Define

$$
\boxed{
X(s)
=
\mathcal L\{x(t)\}
=
\int_{0^-}^{\infty}
x(t)e^{-st}\,dt
}
$$

where, as always,

$$
s=\sigma+j\omega .
$$

**Why $0^-$.** This unilateral-transform convention includes an impulse at $t=0$ and uses the state just before switching. For signals continuous through zero, $0^-$ and $0^+$ agree. At a jump, the derivative includes an impulse; the $0^-$ derivative rule includes that impulse, while a transform starting at $0^+$ excludes it.

### Two things to say about this integral

**1. Where does it converge?** For a piecewise-continuous signal of exponential order — $|x(t)|\le Ke^{at}$ for sufficiently large $t$ — the integral converges when $\Re(s)>a$. This is a sufficient condition for a right half-plane inside the *region of convergence*. The weight $e^{-\sigma t}$ must suppress the signal's growth: $e^{2t}$ has a transform for $\sigma>2$. Not every signal has a transform; $e^{t^2}$ grows too fast for any finite $\sigma$. The real part of $s$ still controls exponential growth and decay.

**2. Why does this answer the question we asked?** Because the transform is invertible, and the inversion formula says explicitly that the signal *is* a superposition of exponentials:

$$
x(t)=\frac{1}{2\pi j}\int_{\sigma_0-j\infty}^{\sigma_0+j\infty}X(s)\,e^{st}\,ds .
$$

Choose $\sigma_0$ inside the region of convergence: the integration runs along the vertical line $s=\sigma_0+j\omega$. For the regular signals considered here, this recovers the signal at continuity points. Do not evaluate the contour in this lecture; point to the integrand and say:

> Look at the $e^{st}$ inside the integral. Along this chosen vertical line, $X(s)$ supplies the weights for a continuous superposition of exponentials. These are test rates, not just the plant's discrete natural rates.
>
> Differentiating each exponential multiplies it by its rate. For the unilateral transform, a boundary term also carries the initial condition; let's derive it.

The same $s$ that described physical exponential modes is now the coordinate of the transformed signal.

---

## 19. Derivative property of the Laplace transform

Starting from

$$
X(s)=\int_{0^-}^{\infty} x(t)e^{-st}\,dt,
$$

consider

$$
\mathcal L\{\dot x\}
=
\int_{0^-}^{\infty}
\dot x(t)e^{-st}\,dt.
$$

For the board derivation, take $x$ continuous with a piecewise-continuous derivative and the exponential bound from §18. At jumps, the same identity uses distributional derivatives. Integrate by parts. Let

$$
u=e^{-st},
\qquad
dv=\dot x(t)\,dt,
$$

so that

$$
du=-se^{-st}dt,
\qquad
v=x(t).
$$

Therefore

$$
\mathcal L\{\dot x\}
=
\left[
x(t)e^{-st}
\right]_{0^-}^{\infty}
+
s\int_{0^-}^{\infty} x(t)e^{-st}\,dt.
$$

For $\Re(s)>a$, the exponential bound gives $x(t)e^{-st}\to0$, so the boundary term at infinity vanishes:

$$
\left[
x(t)e^{-st}
\right]_{0^-}^{\infty}
=
-x(0^-).
$$

Thus

$$
\boxed{
\mathcal L\{\dot x\}
=
sX(s)-x(0^-)
}
$$

and similarly, applying the same rule to $\dot x$ in place of $x$ (so $\ddot x$ is the derivative of $\dot x$):

$$
\mathcal L\{\ddot x\}=s\,\mathcal L\{\dot x\}-\dot x(0^-)=s\left[sX(s)-x(0^-)\right]-\dot x(0^-),
$$

so

$$
\boxed{
\mathcal L\{\ddot x\}
=
s^2X(s)-sx(0^-)-\dot x(0^-)
}
$$

### The heuristic with initial conditions

Using the $0^-$ convention from §18, the rule

$$
\frac{d}{dt}
\leftrightarrow
s
$$

that we have used since §4 survives with initial-condition terms added. Those terms account for stored initial state and vanish when that state is zero. The response to a switched input can still contain natural-mode exponentials even when it starts from rest; §20 makes that distinction concrete.

---

## 20. Revisit the spring-mass-damper with forcing

Return to

$$
m\ddot x+c\dot x+kx=f(t).
$$

Taking Laplace transforms of every term gives

$$
m
\left[
s^2X-sx(0^-)-\dot x(0^-)
\right]
+
c
\left[
sX-x(0^-)
\right]
+
kX
=
F.
$$

The initial conditions enter the algebra directly. The exponential method can also enforce them by adding homogeneous solutions, as in §5 and §7; the gain calculation alone does not.

To rearrange, keep the $X$ terms on the left and move the initial-condition terms to the right:

$$
(ms^2+cs+k)X=F+msx(0^-)+m\dot x(0^-)+cx(0^-)=F+(ms+c)x(0^-)+m\dot x(0^-) .
$$

Dividing by $ms^2+cs+k$ gives

$$
\boxed{
X(s)=
\underbrace{\frac{F(s)}{ms^2+cs+k}}_{\text{zero-state response}}
+
\underbrace{\frac{(ms+c)x(0^-)+m\dot x(0^-)}{ms^2+cs+k}}_{\text{zero-input response}}
}
$$

The zero-state response is due to the input with no initial stored state. The zero-input response is due to initial state with no applied force. This split differs from the particular-plus-homogeneous split: even the zero-state response may contain natural-mode transients.

For zero initial conditions,

$$
\left(ms^2+cs+k\right)X=F,
$$

so

$$
\boxed{
\frac{X(s)}{F(s)}
=
\frac{1}{ms^2+cs+k}
}
$$

### Instructor script

> Compare this with the board from §8.
>
> There, $X$ and $F$ were complex numbers — the amplitude of an assumed exponential input and the amplitude of the exponential response.
>
> Here, $X(s)$ and $F(s)$ are transforms of signals such as steps and pulses, provided the transforms exist.
>
> And we got the same function of $s$.
>
> That is the sense in which the Laplace transform is not a new idea. It is the $e^{st}$ substitution, extended to signals that are not exponentials, with initial conditions carried along for free.
>
> The polynomial $ms^2+cs+k$ has now appeared three times: as the characteristic equation of free motion, as the denominator of the exponential gain, and as the denominator of the transfer function. Its roots are the poles.
>
> That is not a coincidence. It is the whole point.

### 20.1 A complete payoff: switch on the heater

Return to $C\dot x+x/R=q_{\mathrm{in}}$ with $x(0^-)=0$ and $\tau=RC$. Switch the heater from zero to a constant $q_0$ at $t=0$. Unlike the earlier test exponential, this input has a switch-on time, and we want the complete response from rest.

Two transform pairs follow directly from the integral:

$$
\mathcal L\{1\}=\int_0^\infty e^{-st}\,dt=\left[-\frac{e^{-st}}{s}\right]_0^\infty=\frac1s
\quad (\Re(s)>0),
$$

$$
\mathcal L\{e^{-t/\tau}\}=\int_0^\infty e^{-(s+1/\tau)t}\,dt=\left[-\frac{e^{-(s+1/\tau)t}}{s+1/\tau}\right]_0^\infty=\frac1{s+1/\tau}
\quad (\Re(s)>-1/\tau).
$$

The second is the first with $s$ replaced by $s+1/\tau$. The upper limits vanish because the real part of the exponent is negative in each stated region.

Here the functions on the left are understood for $t\ge0$. Therefore the switched input has transform $Q(s)=q_0/s$. Apply the derivative rule to the thermal equation:

$$
\left(Cs+\frac1R\right)X(s)-Cx(0^-)=Q(s),
\qquad x(0^-)=0 .
$$

Multiply by $R$, so that $Cs+1/R$ becomes $(RCs+1)/R=(\tau s+1)/R$:

$$
X(s)=\frac{R}{\tau s+1}\cdot\frac{q_0}{s}=\frac{Rq_0}{s(\tau s+1)} .
$$

*Partial fractions.* Divide top and bottom by $\tau$ so each factor is monic: $X=\dfrac{Rq_0/\tau}{s(s+1/\tau)}$. Cover up each factor:

$$
\text{at }s=0:\ \frac{Rq_0/\tau}{1/\tau}=Rq_0,
\qquad
\text{at }s=-1/\tau:\ \frac{Rq_0/\tau}{-1/\tau}=-Rq_0 ,
$$

so

$$
X(s)=Rq_0\left(\frac1s-\frac1{s+1/\tau}\right).
$$

*Check:* $\dfrac1s-\dfrac1{s+1/\tau}=\dfrac{1/\tau}{s(s+1/\tau)}=\dfrac{1}{s(\tau s+1)}$ ✓.

Read the answer back from the two transform pairs:

$$
\boxed{x(t)=Rq_0\left(1-e^{-t/\tau}\right),\qquad t\ge0.}
$$

**Check it with the class:**
- $x(0)=Rq_0(1-1)=0$.
- $x(\infty)=Rq_0$, where the heater input balances the loss through $R$: $q_0=x/R$.
- $\dot x(0^+)=Rq_0/\tau=q_0/C$. The energy balance requires exactly this, because at $t=0^+$ nothing has yet leaked through $R$, so $C\dot x=q_0$.

After one time constant, $1-e^{-1}=0.632$, so the rise is about 63% complete.

> We transformed a switched input, solved an algebraic equation, and recovered the time response. The decaying exponential is present even though the initial state was zero: it makes the complete response start at the required temperature.

**Optional instructor follow-up:** At the natural test rate, $q_{\mathrm{in}}=q_0e^{-t/\tau}$, the same-exponential gain is undefined. The particular solution is instead $(q_0/C)t e^{-t/\tau}$. A pole marks failure of that trial form, not an infinite temperature.

To verify, substitute $x_p=(q_0/C)te^{-t/\tau}$. Then $C\dot x_p=q_0e^{-t/\tau}-(q_0/\tau)te^{-t/\tau}$, and $x_p/R=(q_0/RC)te^{-t/\tau}=(q_0/\tau)te^{-t/\tau}$. The $te^{-t/\tau}$ terms cancel, leaving $C\dot x_p+x_p/R=q_0e^{-t/\tau}$ ✓. This is the same "multiply by $t$" repair as the repeated root in §7.2.

---

## 21. Revisit the pendulum in the Laplace domain

**Comparison slide:** these are the same models as §9. Show the sign change without repeating the transform derivation, so §20.1 has time to finish.

For the downward pendulum,

$$
J\ddot\theta+b\dot\theta+m_pgl\,\theta=M .
$$

With zero initial conditions,

$$
\left(
Js^2+bs+m_pgl
\right)\Theta(s)
=
M(s),
$$

hence

$$
\boxed{
\frac{\Theta(s)}{M(s)}
=
\frac{1}{
Js^2+bs+m_pgl
}
}
$$

For the upright pendulum,

$$
J\ddot\phi+b\dot\phi-m_pgl\,\phi=M ,
$$

so

$$
\boxed{
\frac{\Phi(s)}{M(s)}
=
\frac{1}{
Js^2+bs-m_pgl
}
}
$$

Same hardware. Same transfer-function *structure*. One sign change in the constant term — and per §9.2, one pole crosses into the right half plane.

$$
\boxed{
\text{the operating point changes the effective stiffness, and therefore changes the poles}
}
$$

Point back at the $s$-plane board from §10: linearizing about the other equilibrium physically drags a pole across the imaginary axis.

---

## 22. Big-picture summary

The lecture can end with the following chain:

$$
\boxed{
\text{physics}
\rightarrow
\text{differential equation}
\rightarrow
e^{st}
\rightarrow
\text{characteristic polynomial}
}
$$

then

$$
\boxed{
s=\sigma+j\omega
}
$$

with

$$
\boxed{
\sigma
=
\text{growth/decay}
}
\qquad
\boxed{
\omega
=
\text{oscillation}
}
$$

then

$$
\boxed{
\text{Laplace transform}
\rightarrow
\text{algebraic system description}
}
$$

and finally

$$
\boxed{
G(s)=\frac{N(s)}{D(s)}
}
$$

with

$$
\boxed{
D(s)=0
\Rightarrow
\text{poles / natural modes}
}
$$

$$
\boxed{
N(s)=0
\Rightarrow
\text{zeros / input-output blocking}
}
$$

---

## 23. Suggested closing script

> We began with a hot object cooling toward room temperature.
>
> That gave us a real negative value of $s$ — and when we added a heater, that same value turned out to be where the transfer function's denominator vanished.
>
> We moved to a spring-mass-damper and discovered complex values of $s$, which naturally represented damping and oscillation, and which cancelled in conjugate pairs to give us back real motion.
>
> We forced that system and found that the characteristic polynomial had become the denominator of a transfer function. The poles were not a definition we imposed. They were the natural modes, seen from a different direction.
>
> We turned the same mechanical idea into a pendulum and saw how linearization around different equilibria moves a pole across the imaginary axis.
>
> We added another mass and discovered that a system can move internally while the measured output is zero — and that holding the output at zero costs a specific input.
>
> That gave us a physical interpretation of zeros and zero dynamics.
>
> Then we saw that changing where we measure can dramatically change the zeros while leaving the internal dynamics unchanged. In our examples, the visible poles stayed the same too.
>
> Finally, the Laplace transform let us switch on a heater and calculate its whole response from rest.
>
> So when we now write
>
> $$X(s)=\int_{0^-}^{\infty} x(t)e^{-st}\,dt,$$
>
> the variable $s$ is not a mysterious new symbol.
>
> It is the same $s$ that appeared naturally when we asked:
>
> **What exponential motions are compatible with the physics?**

---

# Part II — Enrichment: zeros, geometry, and noncollocation

This part assumes Part I. Its single theme is the §16 discovery, pushed hard:

> **The internal dynamics stay fixed when we move the sensor. The zeros depend on the input-output pair, and cancellations can change which internal modes appear as transfer-function poles.**

---

## 24. Ball-and-beam: underactuation and internal coordinates

Consider a ball rolling without slipping on a beam pivoted at its center.

```text
                       o  ball, position x along beam
                   ___/______________
      ____________/                  \
                  \        pivot O     (beam tilted by alpha)
                   \
```

Let

- $x$: ball position along the beam,
- $\alpha$: beam angle, positive when the positive-$x$ end slopes downward,
- $m$: ball mass,
- $r$: ball radius,
- $J_b$: ball rotational inertia about its own center,
- $J_{\text{beam}}$: beam inertia about the pivot,
- $M$: torque applied to the beam.

### 24.1 Ball dynamics

In the slowly rotating beam approximation used here, the no-slip relation is

$$
\omega_b=\frac{\dot x}{r},
$$

so translating the ball also spins it. The effective translational inertia is

$$
m_{\text{eff}}
=
m+\frac{J_b}{r^2}.
$$

To see where $m_{\text{eff}}$ comes from, let $F$ be the friction force from the beam on the ball, acting up the slope at the contact point. The ball's translation and its spin about its own center are then

$$
m\ddot x=mg\sin\alpha-F,
\qquad
J_b\dot\omega_b=Fr .
$$

No-slip gives $\dot\omega_b=\ddot x/r$, so $F=J_b\ddot x/r^2$. Substituting into the translation equation, $m\ddot x=mg\sin\alpha-(J_b/r^2)\ddot x$. The friction needed to spin the ball acts like extra mass.

The component of gravity along the beam is exactly $mg\sin\alpha$. Two approximations are being made in what follows, and it is worth naming them: we drop the centrifugal term $m x\dot\alpha^2$ (small when the beam rotates slowly), and we ignore the ball's effect on the beam's own dynamics. Then

$$
\left(
m+\frac{J_b}{r^2}
\right)\ddot x
=
mg\sin\alpha .
$$

For small $\alpha$, $\sin\alpha\approx\alpha$, so

$$
\boxed{
\left(
m+\frac{J_b}{r^2}
\right)\ddot x
=
mg\alpha
}
$$

For a solid sphere, $J_b=\tfrac25mr^2$, so

$$
m+\frac{J_b}{r^2}
=
m+\frac25m
=
\frac75m,
$$

and hence

$$
\boxed{
\ddot x=\frac57g\alpha
}
$$

Substituting $x=Xe^{st}$, $\alpha=Ae^{st}$ gives $s^2X=\tfrac57gA$, so

$$
\boxed{
\frac{X}{A}
=
\frac{5g}{7s^2}
}
$$

In Laplace terms with zero initial conditions, writing $\mathcal A(s)$ for the transform of $\alpha(t)$,

$$
\boxed{
\frac{X(s)}{\mathcal A(s)}
=
\frac{5g}{7s^2}
}
$$

### 24.2 What is the input, really?

This is where the model has to be pinned down, because two different systems are hiding here.

**If the beam angle is servo-controlled** — a fast inner loop drives $\alpha$ to whatever you command — then $\alpha$ *is* the input, and the plant is second order with state

$$
\mathbf{x}
=
\begin{bmatrix}
x & \dot x
\end{bmatrix}^{\mathsf T}.
$$

**If the input is a torque on the beam**, retain a beam coordinate and, under the stated approximation of neglecting the ball's back-reaction, write:

$$
J_{\text{beam}}\ddot\alpha=M .
$$

The neglected gravitational torque from the ball is proportional to $mgx$ near the centered equilibrium and is first order. Omitting it is an additional modeling assumption, not a consequence of small-angle linearization. This simplified cascade has $\mathcal A(s)/M(s)=1/(J_{\text{beam}}s^2)$, and multiplying by $X/\mathcal A=5g/(7s^2)$ gives

$$
\frac{X(s)}{M(s)}
=
\frac{5g}{7J_{\text{beam}}\,s^4}
$$

and the four-state description

$$
\mathbf{x}
=
\begin{bmatrix}
x &
\dot x &
\alpha &
\dot\alpha
\end{bmatrix}^{\mathsf T}.
$$

**This second version is the underactuated one.** State the criterion carefully, because counting states is the wrong test — a single mass pushed by a single force has two states and one input, and it is fully actuated. Underactuation compares actuators to **configuration degrees of freedom**:

$$
\boxed{
2\ \text{configuration DOFs }(x,\alpha),
\quad
1\ \text{independent actuator }(M)
\ \Rightarrow\
\text{underactuated}
}
$$

The four states arise merely because both coordinates obey second-order equations. What actually bites is that you have no way to push the ball directly: the one actuator you own reaches $x$ only *through* $\alpha$.

Say which model you are using; the two are not interchangeable, and the "underactuated" label applies only to the second. This distinction matters later, when students meet state-space systems with many states and enough actuators to be fully actuated anyway.

### Teaching point

The simplified ball-and-beam models used here do **not** produce a finite RHP zero. Its numerator is a constant.

Its pedagogical value is different:

- the actuator acts through an intermediate coordinate,
- the system is underactuated (in the torque-input version),
- multiple state variables are needed,
- one instantaneous position measurement does not specify all the state variables.

Use it as a bridge from simple transfer behavior to internal states, and as a counterexample to “underactuation requires a RHP zero,” which §28 will confirm. The integrators still prevent asymptotic stability.

---

## 25. Flexible structures and noncollocation

The two-mass system of §11 is a lumped model of a flexible structure. For a genuine flexible beam, the displacement field expands in modes:

$$
w(x,t)
=
\sum_{i=1}^\infty
\phi_i(x)q_i(t).
$$

With mass-normalized modes and damping diagonal in modal coordinates, a point force at $x_a$ and displacement measurement at $x_s$ give

$$
\boxed{
G(s)
=
\sum_i
\frac{
\phi_i(x_s)\phi_i(x_a)
}{
s^2+2\zeta_i\omega_i s+\omega_i^2
}
}
$$

The coefficient $\phi_i(x_s)\phi_i(x_a)$ is commonly called a **modal residue**. It says how strongly and with what sign a mode contributes. If either point is at a node, this coefficient is zero and the mode contributes no pole to that channel. The two-mass system is the finite-dimensional version of this modal picture; the scalar sum assumes modal damping.

### The collocated case

If $x_a=x_s$, every residue is a square:

$$
\phi_i(x_a)^2\ge0 .
$$

All residues share a sign — and this is a much stronger result than it looks. Take the undamped case first, where the statement is cleanest:

$$
G(s)=\sum_i\frac{\phi_i(x_a)^2}{s^2+\omega_i^2}.
$$

For distinct participating undamped frequencies with positive modal coefficients, the poles and zeros **interlace along the $j\omega$ axis**: between adjacent positive-frequency resonances sits exactly one antiresonance. These are the natural frequencies of the structure constrained at the measured coordinate — the §14 result again.

For this ideal passive mechanical model, collocation excludes finite RHP zeros. Undamped zeros lie on the axis; they do not satisfy §17's strict minimum-phase convention. If damping makes the constrained zero dynamics asymptotically stable, its zeros move strictly into the LHP. A stable plant with those LHP zeros is minimum phase. Under light damping, the resonance/notch ordering remains a useful picture, but exact interlacing is the undamped result.

With the usual positive force/displacement sign convention, the frequency-response phase lies between $-180^\circ$ and $0^\circ$ wherever the response is nonzero and finite.

### Two collocation results, not one

Be careful not to blur these together, because they are different theorems about different sensor choices:

$$
\boxed{
\begin{array}{ll}
\text{force in, displacement out}
&\rightarrow \text{no finite RHP zeros; undamped interlacing}\\[3pt]
\text{force in, velocity out}
&\rightarrow \text{passivity / positive-real structure}
\end{array}}
$$

The second result uses the power-conjugate pair of force and velocity. For the ideal passive mechanical model, the collocated force-to-velocity transfer function is positive real. Negative velocity feedback $u=-k_v\dot y$, $k_v>0$, adds dissipation:

$$
\dot E=-\text{existing dissipation}-k_v\dot y^2\le0.
$$

Additional passive modes do not turn this feedback into an energy source. This explains the spillover robustness. Asymptotic decay additionally requires that no undamped mode remain invisible to the damping/feedback. The guarantee assumes an ideal collocated interconnection; passive-controller extensions require the corresponding passivity and detectability conditions.

This is why control engineers fight for collocation. It is not a preference; it is a structural guarantee — provided you name which guarantee you mean.

### The noncollocated case

For $x_a\neq x_s$, the product

$$
\phi_i(x_s)\phi_i(x_a)
$$

may change sign from one mode to another, because the sensor may sit on the opposite side of a mode's node line from the actuator. Different modes then subtract at the measured output rather than adding.

The interlacing guarantee is lost. Zeros are free to move off the $j\omega$ axis, and for some actuator/sensor geometries they land in the right half plane.

Note carefully what is and is not being claimed: noncollocation *removes a guarantee*. It does not create a RHP zero by itself. See caution 4 in §38.

---

## 26. Hard-disk read head: a real engineering interpretation

A hard-disk-drive head-positioning mechanism is a useful conceptual example of a noncollocated flexible servo.

```text
          read/write head   <--- position we care about
                 o
                 |
      flexible arm/suspension
                 |
                 |
              pivot O  <--- voice-coil torque applied here
```

The actuator applies torque near the pivot. The controlled quantity is the head position at a remote point. At low frequency the arm looks almost rigid; at higher frequency, arm and suspension flexibility introduce additional modes with residues that depend on where the head sits relative to each mode shape.

A crude modeling progression is

$$
\text{rigid arm}
\rightarrow
\text{two-mass lumped model}
\rightarrow
\text{multi-mode flexible structure},
$$

which is precisely §9 $\rightarrow$ §11 $\rightarrow$ §25.

The important teaching point is **not** that every HDD model possesses a RHP zero. The important point is:

$$
\boxed{
\text{remote sensing + flexible modes}
\Rightarrow
\text{zeros become strongly geometry dependent}
}
$$

This is an excellent engineering context for discussing resonances, antiresonances, collocation, noncollocation, and bandwidth limitations. Flexible modes and the resulting servo-bandwidth limits are one of the important constraints on achievable track-following accuracy, and hence on track density — alongside disturbances, spindle runout, sensing noise, and media mechanics.

---

## 27. A stable, nonminimum-phase rigid body

A right-half-plane zero can arise without any structural flexibility at all. This example is worth doing carefully, because it is the one that demonstrates the claim in §33: **stable poles do not imply minimum phase.**

Consider a rigid platform on soft mounts, with two generalized coordinates:

- vertical translation $x$ of the center of mass,
- small rotation $\theta$ about the center of mass.

```text
        sensor                     actuator
       (at -b)                      (at +a)
          |                            | u
          v                            v
    ======#============ CM ============#======
             \                      /
             mounts: kx, cx (heave); k_theta, c_theta (pitch)
```

The actuator applies a vertical force $u$ at offset $a$ from the center of mass, producing both a force $u$ and a moment $au$. In center-of-mass coordinates the translational and rotational equations decouple:

$$
m\ddot x+c_x\dot x+k_xx=u
$$

$$
J\ddot\theta+c_\theta\dot\theta+k_\theta\theta=au
$$

(The decoupling assumes symmetric stiffness and damping distributions about the center of mass. Take $c_x,c_\theta>0$ as well as positive masses, inertia, and stiffnesses, so the plant is asymptotically stable. The undamped row below is a comparison limit.)

Now measure vertical displacement at a point a distance $b$ on the **opposite side** of the center of mass. For small $\theta$, a point at signed offset $d$ moves as $x+d\theta$, so with $d=-b$:

$$
\boxed{
y=x-b\theta
}
$$

### The transfer function

$$
\frac{X}{U}
=
\frac{1}{ms^2+c_xs+k_x},
\qquad
\frac{\Theta}{U}
=
\frac{a}{Js^2+c_\theta s+k_\theta},
$$

so

$$
\frac{Y}{U}
=
\frac{1}{ms^2+c_xs+k_x}
-
\frac{ab}{Js^2+c_\theta s+k_\theta}.
$$

Over the common denominator, the numerator is the first fraction's numerator times the second denominator, minus the second numerator times the first denominator:

$$
1\cdot(Js^2+c_\theta s+k_\theta)-ab\,(ms^2+c_xs+k_x)
=(J-abm)s^2+(c_\theta-abc_x)s+(k_\theta-abk_x) .
$$

Therefore

$$
\boxed{
\frac{Y}{U}
=
\frac{
(J-abm)s^2+(c_\theta-abc_x)s+(k_\theta-abk_x)
}{
(ms^2+c_xs+k_x)(Js^2+c_\theta s+k_\theta)
}
}
$$

All four poles are in the left half plane whenever $m,c_x,k_x,J,c_\theta,k_\theta>0$. The plant is **asymptotically stable**.

### When is there a RHP zero?

Use local symbols $A,B,C$ for the numerator coefficients:

$$
A=J-abm,\qquad B=c_\theta-abc_x,\qquad C=k_\theta-abk_x.
$$

First consider $A,C\ne0$. For numerator roots $z_1,z_2$,

$$
z_1z_2=\frac CA=\frac{k_\theta-abk_x}{J-abm}.
$$

A **negative** product forces two real roots of opposite signs. Writing $p=J/m$ and $q=k_\theta/k_x$, the factors are $A=m(p-ab)$ and $C=k_x(q-ab)$. Therefore

$$
\boxed{
\begin{gathered}
\text{one positive and one negative real numerator root}\\
\iff AC<0
\iff ab\text{ lies strictly between }J/m\text{ and }k_\theta/k_x.
\end{gathered}
}
$$

This is a sufficient condition for a RHP zero, not a necessary one: outside this interval there can be a RHP conjugate pair or even two positive real zeros. The full classification is in the instructor reference below. Because the plant poles are in the LHP, a positive numerator root cannot cancel.

**1. Damping cannot remove the RHP zero when $AC<0$, but it moves both zeros.** Damping enters $B$, and hence the root sum $-B/A$, while the negative product $C/A$ stays fixed. For every finite choice of damping there is still one positive and one negative root. This conclusion applies to the opposite-sign-root case; it is not a rule for every sensor geometry.

$$
\boxed{AC<0\ \Rightarrow\ \text{one RHP zero for every damping distribution}}
$$

Show the $AC<0$ case with $ab=0.15$ and the numbers below. The left family has $c_\theta=0.1c_x$; the right family has $c_\theta=0.25c_x$ and includes the worked case.

Each row uses the worked-case values $m=1$, $J=0.1$, $k_x=100$, $k_\theta=20$. These fix $A=0.1-0.15=-0.05$ and $C=20-15=5$, while $B=c_\theta-0.15c_x$. Dividing $As^2+Bs+C$ by $A$ gives $s^2-20Bs-100=0$, so $s=10B\pm\sqrt{100B^2+100}$. For example, $(c_x,c_\theta)=(2,0.2)$ gives $B=-0.1$ and $s=-1\pm\sqrt{101}=+9.05,\ -11.05$. The product is always $-100$:

| $c_x$ | $c_\theta$ | zeros | $c_x$ | $c_\theta$ | zeros |
|---:|---:|---|---:|---:|---|
| $0$ | $0$ | $\pm10.00$ | $0$ | $0$ | $\pm10.00$ |
| $2$ | $0.2$ | $+9.05,\ -11.05$ | $2$ | $0.5$ | $+12.20,\ -8.20$ |
| $6$ | $0.6$ | $+7.44,\ -13.44$ | $6$ | $1.5$ | $+17.66,\ -5.66$ |
| $20$ | $2.0$ | $+4.14,\ -24.14$ | $20$ | $5.0$ | $+42.36,\ -2.36$ |

The RHP zero moves a long way — and which direction it moves depends on the sign of $B$, i.e. on how the damping is distributed between the two channels. In the left-hand family it drifts *toward the origin*, which makes the plant harder to control (see §34). For this geometry, damping does not remove the RHP zero and can move it closer to the origin.

> **[ DEMO 7 ]** — `demo7_damping_moves_zeros.py` *(slide)*
>
> **Show:** the zero locus at left — two families of damping, the zeros travelling in opposite directions along the real axis, neither ever reaching the imaginary axis.
> **Point at:** the printed line `product of the zeros C/A over the whole sweep: min -100.0000, max -100.0000`. Constant across a 500-point sweep, because $B$ never enters the product.
> **Say:** "For this $AC<0$ geometry, damping moves the zero without changing its sign. The script sweeps farther than the table, to $c_x=60$: the two families reach about $+1.6$ and $+121$."
> **Right panel:** all three step responses still start by going the wrong way, however heavily damped. That is the §33 point made in one picture.

**2. If $ab<0$** — sensor and actuator on the *same* side of the center of mass — then $A>0$, $B>0$ and $C>0$, so both zeros lie in the open **left** half plane. (For the worked numbers below with $ab=-0.15$: $A=0.1+0.15=0.25$, $B=0.5+0.3=0.8$, $C=20+15=35$. Then $s^2+3.2s+140=0$ gives $s=-1.6\pm j\sqrt{140-2.56}=-1.60\pm j11.72$.) Only in the *undamped* case $B=0$ do those zeros sit exactly on the $j\omega$ axis.

Note that "same side" is weaker than collocated: the two can sit at different points and still share a sign. True collocation is the special case $b=-a$, meaning the sensor is *at* the actuator, which gives $ab=-a^2<0$. So collocation lives inside this family, and the favorable sign structure of §25 turns out to extend to a strictly larger set of geometries than collocation alone. That is worth saying out loud — collocation is sufficient for good sign structure here, not necessary.

**3. If $ab=J/m$ exactly**, then $A=0$. When $B\ne0$, the numerator is linear, with a root at $-C/B$, and the relative degree is **3**. If also $B=0$ but $C\ne0$, the relative degree is **4**. Here $B=0$ means $c_\theta=(J/m)c_x$, the mass-proportional damping condition for these coordinates; the undamped limit satisfies it too. If $A=B=C=0$, the entire output transfer function is zero and no finite relative degree is assigned. As usual, common factors must be canceled when identifying finite transfer zeros.

### A worked numerical case

Take $m=1$, $J=0.1$, $k_x=100$, $k_\theta=20$, $c_x=2$, $c_\theta=0.5$, with $a=0.3$ and $b=0.5$, so $ab=0.15$.

Check the condition: $J/m=0.1$ and $k_\theta/k_x=0.2$, and indeed $0.1<0.15<0.2$.

- **Poles:** $s^2+2s+100=0 \Rightarrow s=-1\pm j\sqrt{100-1}=-1\pm j9.95$. Also $0.1s^2+0.5s+20=0$, i.e. $s^2+5s+200=0$, gives $s=-2.5\pm j\sqrt{200-6.25}=-2.5\pm j13.92$. All four are stable.
- **Numerator:** $A=0.1-0.15(1)=-0.05$, $B=0.5-0.15(2)=0.2$, $C=20-0.15(100)=5$. So $-0.05s^2+0.2s+5=0$. Dividing by $-0.05$ gives $s^2-4s-100=0$, so $s=2\pm\sqrt{4+100}=2\pm10.198$. That is $s=-8.20$ and $\boxed{s=+12.20}$.

A stable plant with a right-half-plane zero. Put these numbers on the board; they make §33 concrete rather than assertional.

(These values are not mass-proportionally damped: $c_\theta/c_x=0.25\ne J/m=0.1$. Thus, if we move the sensor to $ab=J/m$, item 3 gives relative degree 3.)

### Physical interpretation

The actuator causes both translation and rotation. At the measured point, those two effects **subtract**.

Both translation and rotation have relative degree **two**. For a force step $u_0>0$ from rest, compare their acceleration contributions and their static displacements:

$$
\ddot y(0^+)=u_0\left(\frac1m-\frac{ab}{J}\right)=\frac{u_0A}{mJ},
\qquad
y(\infty)=u_0\left(\frac1{k_x}-\frac{ab}{k_\theta}\right)=\frac{u_0C}{k_xk_\theta}.
$$

Both formulas come straight from the two decoupled equations. At $t=0^+$ the system is at rest, so the damping and spring forces are zero. That leaves $m\ddot x=u_0$ and $J\ddot\theta=au_0$, and $\ddot y=\ddot x-b\ddot\theta$. At steady state all derivatives vanish, leaving $k_xx=u_0$ and $k_\theta\theta=au_0$, and $y=x-b\theta$. Put each over a common denominator to get the $A$ and $C$ forms. Equivalently, with $Y=(Y/U)\,u_0/s$, the initial value theorem gives $\ddot y(0^+)=\lim_{s\to\infty}s^3Y=\lim_{s\to\infty}s^2(Y/U)\,u_0=u_0A/(mJ)$, the ratio of leading coefficients. The final value theorem gives $y(\infty)=\lim_{s\to0}sY=(Y/U)(0)\,u_0=u_0C/(k_xk_\theta)$.

When $AC<0$, initial acceleration and final displacement have opposite signs. In the worked case, $\ddot y(0^+)=u_0(-0.05)/(0.1)=-0.5u_0$ and $y(\infty)=u_0(5)/(2000)=0.0025u_0$. In the worked case, $J/m<ab<k_\theta/k_x$: rotation wins initially ($A=-0.05$), translation wins at DC ($C=5$). The reverse ordering, $k_\theta/k_x<ab<J/m$, also gives inverse response, with translation winning initially and rotation at DC. The distinction is acceleration gain versus static gain, not relative degree.

This wrong-way motion is called an **inverse response**.

Important caution:

> Wrong-way initial motion is a common physical manifestation of a RHP zero, but it should not be used as the formal definition of one. The definition is in §17 and §31.

### Instructor reference: the full quadratic classification

Keep this table in the handout or use it for Problem 8; the live example above needs only the $AC<0$ row. For $A,C\ne0$:

| Condition | Roots of $As^2+Bs+C$ |
|---|---|
| $C/A<0$ | One positive and one negative real root, for every $B$ |
| $C/A>0$, $B/A>0$ | Both strictly in the LHP |
| $C/A>0$, $B/A<0$ | Both strictly in the RHP; real if $B^2-4AC\ge0$, otherwise conjugate |
| $C/A>0$, $B=0$ | A purely imaginary conjugate pair |

When $AC>0$, changing the damping distribution can change the half plane of the zeros. For the same $m,J,k_x,k_\theta$ as the worked example, but $ab=0.05$ and $c_x=2$, the coefficients are $A=0.1-0.05=0.05$, $C=20-5=15$ and $B=c_\theta-0.1$. Dividing by $A$ gives $s^2+20Bs+300=0$. For $c_\theta=0.05$ this is $s^2-s+300$, with roots $0.5\pm j\sqrt{299.75}$. For $c_\theta=0.20$ it is $s^2+2s+300$, with roots $-1\pm j\sqrt{299}$:

$$
\begin{array}{c|c|c}
c_\theta & N(s) & \text{zeros}\\ \hline
0.05 & 0.05s^2-0.05s+15 & 0.5\pm j17.3133\\
0.20 & 0.05s^2+0.10s+15 & -1\pm j17.2916
\end{array}
$$

The plant poles remain in the LHP in both cases. Damping alone removes the RHP pair. Two **real** positive zeros are also possible outside the interval: with $ab=0.05$, $c_x=100$, $c_\theta=0.05$, the numerator is $0.05s^2-4.95s+15$, with roots approximately $3.12921$ and $95.87079$. Here $B=0.05-0.05(100)=-4.95$. Dividing by $0.05$ gives $s^2-99s+300=0$, so $s=\tfrac12\left(99\pm\sqrt{9801-1200}\right)=\tfrac12(99\pm92.742)$.

For positive $c_x$ and nonzero $A,B,C$, all three coefficients share a sign exactly when $ab$ lies strictly below all three ratios $J/m$, $k_\theta/k_x$, $c_\theta/c_x$, or strictly above all three. This is the generic LHP-zero condition. Handle boundaries separately: $A=0$ is item 3 above; $C=0$ gives a numerator factor $s$ and requires the usual cancellation check. Thus the “same side of three ratios” rule is not a substitute for checking degree reductions.

---

## 28. Quadrotor: underactuation does not require a RHP zero

A planar quadrotor near hover provides a useful comparison — and a counterexample that stops a very common overgeneralization.

### Deriving the model

At hover the total thrust is $f\approx mg$, directed along the vehicle's body axis. If the vehicle pitches by a small angle $\theta$, that thrust tilts, and its horizontal component is

$$
f\sin\theta\approx mg\theta ,
$$

so the horizontal acceleration of the center of mass is

$$
\boxed{
\ddot x=g\theta
}
$$

The pitch axis is driven directly by the differential-thrust torque $M$:

$$
\boxed{
J\ddot\theta=M
}
$$

where $x$ is horizontal center-of-mass position, $\theta$ is pitch angle (positive $\theta$ tilts the thrust axis toward positive $x$), and $M$ is pitch torque. Note the structure: **you cannot push sideways directly.** You can only torque, wait for the vehicle to tilt, and let the tilted thrust push you.

### The center-of-mass channel

Assume exponential motion: $x=Xe^{st}$, $\theta=\Theta e^{st}$, $M=M_0e^{st}$. Then

$$
s^2X=g\Theta,
\qquad
Js^2\Theta=M_0 ,
$$

so

$$
\Theta=\frac{1}{Js^2}M_0
\qquad\text{and}\qquad
X=\frac{g}{Js^4}M_0 .
$$

Therefore

$$
\boxed{
\frac{X}{M}
=
\frac{g}{Js^4}
}
$$

There is **no finite transmission zero** in this channel. The numerator is a constant.

So emphasize:

$$
\boxed{
\text{underactuated}
\not\Rightarrow
\text{a RHP zero}
}
$$

**But do not oversell it.** Four poles at the origin and relative degree 4 make this a demanding control problem. The free response can grow polynomially; the plant is neither asymptotically stable nor BIBO stable. “No finite zeros” describes the zeros only, and does not make this plant minimum phase under §17's convention.

---

## 29. Quadrotor with an offset measurement point

Now measure the horizontal position of a point offset vertically from the center of mass — a downward-facing camera used for visual servoing, a landing skid, or a sensor mast.

Note that these are all **rigidly attached** points. The relation $y=x-h\theta$ describes a point bolted to the airframe. A cable-suspended payload is a genuinely different problem: the swing angle is an extra generalized coordinate with its own dynamics, and this model does not describe it.

### Which way does the offset point move?

This is the decisive question and it deserves an explicit answer rather than a hedge.

With the convention of §28 — positive $\theta$ tilts the thrust axis toward $+x$ — a body-fixed point at height $+h$ **above** the center of mass has horizontal position $x+h\theta$. It swings the same way the vehicle accelerates.

A point a distance $h$ **below** the center of mass has horizontal position

$$
\boxed{
y=x-h\theta
}
$$

It swings *opposite* to the direction the vehicle is about to accelerate. That is the case that produces the RHP zero.

### The transfer function

From §28,

$$
\frac{X}{M}
=
\frac{g}{Js^4},
\qquad
\frac{\Theta}{M}
=
\frac{1}{Js^2},
$$

so, since $Y=X-h\Theta$,

$$
\frac{Y}{M}
=
\frac{g}{Js^4}
-
\frac{h}{Js^2}
$$

and therefore, writing the second term over $Js^4$ as $hs^2/(Js^4)$,

$$
\boxed{
\frac{Y}{M}
=
\frac{g-hs^2}{Js^4}
}
$$

The zeros satisfy $g-hs^2=0$, so

$$
\boxed{
s=\pm\sqrt{\frac gh}
}
$$

and one of them lies in the right half plane:

$$
\boxed{
s=+\sqrt{\frac gh}
}
$$

This is a nonminimum-phase zero. For the point *above* the CM, the sign of the $h$ term flips: $Y/M=(g+hs^2)/(Js^4)$, and $g+hs^2=0$ gives $s^2=-g/h$, i.e. $s=\pm j\sqrt{g/h}$. Summarizing the geometry:

| Measurement point | Output | Zeros | Character |
|---|---|---|---|
| At the center of mass | $y=x$ | none (finite) | no finite zeros; four integrators |
| A distance $h$ **above** the CM | $y=x+h\theta$ | $\pm j\sqrt{g/h}$ | on the $j\omega$ axis |
| A distance $h$ **below** the CM | $y=x-h\theta$ | $\pm\sqrt{g/h}$ | **RHP zero** |

### Where that zero comes from: derive the zero dynamics directly

This is the best moment in Part II, because you can get the zero without touching the transfer function at all.

> This is the exact same trick we did with the second mass. Set the measured output to zero, and ask what the rest of the machine is still free to do.

Say it in those words. The recurrence is worth more to students than another definition — §14 pinned $x_1$ and found $m_2$ still ringing; here we pin the camera and find the airframe still pitching.

> **[ DEMO 8 ]** — `demo8_quadrotor_rhp.py` *(live — the payoff of Part II)*
>
> **Show:** the top panel first. Three outputs, one plant, one actuator; only the point below the centre of mass dips negative before recovering.
> **Point at:** the wrong-way excursion ending at $t=\sqrt{12h/g}=0.49$ s — an exact analytic result the script confirms against `scipy.signal.step` to $10^{-12}$.
> **Derivation of the crossing time.** For a torque step $M_0$ from rest, $\theta=\frac{M_0}{2J}t^2$. Integrating $\ddot x=g\theta$ twice gives $x=\frac{gM_0}{24J}t^4$. So $y=x-h\theta=\frac{M_0t^2}{2J}\left(\frac{gt^2}{12}-h\right)$. This is negative until $gt^2/12=h$, i.e. $t=\sqrt{12h/g}$. With $h=0.2$: $\sqrt{2.4/9.81}=0.4946$ s. The same formula gives $\theta=0.2446/(2\cdot0.02)=6.12$ rad for the script's unit torque.
> **Then the lower-right panel:** $\theta(t)$ under $y\equiv0$, diverging on a log scale, lying exactly on $\cosh(\sqrt{g/h}\,t)$.
> **Point at:** the three-row table. Divergence rate fitted from the simulation, $\sqrt{g/h}$, and the RHP zero of $Y/M$ all read $7.00357$.
> **Say:** "The zero is the exponential growth rate of a motion compatible with keeping this output at zero. The linear zero dynamics are unstable."
> **Model scope:** these are responses of the linearized model. The script's unit torque with $J=0.02$ gives $\theta\approx6.12$ rad at the $0.4946$ s crossing, outside the small-angle range. The crossing time is independent of nonzero step amplitude; a smaller torque scales the motion down. Likewise the growing zero-dynamics trace is physically local, not a prediction of unlimited large-angle flight. Read the script's CM label “minimum phase” as “no finite zeros,” following §17's convention.

Impose the defining condition:

$$
y(t)\equiv0
\qquad\Longrightarrow\qquad
x=h\theta .
$$

Differentiate twice: $\ddot x=h\ddot\theta$. But the physics says $\ddot x=g\theta$. Setting these equal,

$$
h\ddot\theta=g\theta
\qquad\Longrightarrow\qquad
\boxed{
\ddot\theta=\frac gh\,\theta
}
$$

with characteristic roots $s=\pm\sqrt{g/h}$ — precisely the zeros we just computed. (The required input follows from $M=J\ddot\theta=J(g/h)\theta$; it is generally nonzero along a nontrivial trajectory.)

**Look carefully at the sign.** This is

$$
\ddot\theta-\frac gh\theta=0,
\qquad\text{not}\qquad
\ddot\theta+\frac gh\theta=0 .
$$

It is an **inverted**-pendulum equation, not a hanging one. A hanging pendulum of length $h$ oscillates at $\sqrt{g/h}$; this one *diverges* at rate $\sqrt{g/h}$. Do not describe the zero as "a pendulum frequency" — the magnitude coincides, but the character is the opposite, and the whole point is that the motion grows.

A generic initial condition of these zero dynamics contains the growing exponential: holding the offset point fixed then requires increasing pitch motion. The negative-root trajectory instead decays, but any growing-mode component makes the zero dynamics unstable. The linear prediction applies while angles remain small.

$$
\boxed{
\sqrt{g/h}
=
\text{the inverted-pendulum divergence rate of the zero dynamics}
}
$$

### Put a number on it

For a camera $h=0.2\ \text{m}$ below the center of mass,

$$
z=\sqrt{\frac{9.81}{0.2}}=\sqrt{49.05}\approx 7.0\ \mathrm{s}^{-1}.
$$

For the bandwidth estimate below, $z/2\approx3.5$ rad/s, and dividing by $2\pi$ gives about $0.56$ Hz.

The design heuristic of §34 — keep crossover comfortably below the RHP zero, with $z/2$ a common illustrative target — then suggests a practical closed-loop bandwidth for that output somewhere around $3.5\ \text{rad/s}$, about $0.56\ \text{Hz}$. Treat that as an order-of-magnitude expectation, not a computed limit.

Mounting the camera *lower* makes it worse: $h$ up, $z$ down, achievable bandwidth down. That is a design consequence students can act on, and the direction of the effect is solid even though the factor of $1/2$ is not.

### Instructor script

> Moving the sensor did not change the vehicle's open-loop dynamics; the four integrators were already there.
>
> We changed the output.
>
> The center of mass and the offset point combine translation and rotation differently.
>
> That changes the zeros.
>
> In these three channels, the same four poles remain. The zeros change with the chosen output.

**Connect this to §27:** translation and rotation subtract at the sensor in both examples. The actuation paths differ. Platform force drives translation and rotation in parallel, each with relative degree two; quadrotor torque drives translation through attitude, giving relative degrees four and two. Both worked examples have real zeros, but their initial-motion arguments are different.

---

## 30. Why the offset-point quadrotor moves the wrong way first

The argument is entirely about **relative degree** — how many integrations separate the input from each contribution to the output.

The pitch torque acts immediately on angular acceleration:

$$
J\ddot\theta=M
\qquad\Rightarrow\qquad
\theta\ \text{responds after 2 integrations}.
$$

The horizontal center-of-mass motion has to wait for the attitude to develop first:

$$
\ddot x=g\theta
\qquad\Rightarrow\qquad
x\ \text{responds after 4 integrations}.
$$

But the offset point's output contains the direct geometric term $-h\theta$, which inherits the *fast* path. So in the first instants after a torque command, the $-h\theta$ term dominates completely — the $x$ term has barely started — and the measured point moves backwards. For a positive constant torque, translation later dominates in the linear model. There is no finite steady state for this open-loop integrator chain.

This explains the initial inverse response. Increasing feedback gain without accounting for that response can destabilize the loop; the RHP zero must be included in the design.

---

## 31. Zero dynamics in general

The transfer-function definition of §17 is algebraically convenient, but the physical interpretation is more revealing and generalizes to nonlinear systems.

Suppose the output is $y(t)$. Impose

$$
\boxed{
y(t)\equiv0
}
$$

**using whatever input is required to maintain it**, and ask:

> What internal motions can still occur?

Those internal motions are the **zero dynamics**. Recall §14, where the required input was $u=-(c_2\dot x_2+k_2x_2)$ and the internal motion was the free vibration of the pinned second mass.

- If all compatible internal motions decay toward equilibrium, the zero dynamics are asymptotically stable.
- A growing compatible mode makes them unstable.

For a minimal SISO continuous-time **LTI** system, an exponentially growing zero-dynamics mode corresponds to a RHP transmission zero. Simple imaginary-axis zeros give nondecaying modes; generalized modes on the axis can grow polynomially. The nonlinear definition still uses $y\equiv0$, but its stability requires analysis of the resulting nonlinear dynamics.

---

## 32. Optional: the state-space statement

For a **minimal SISO realization with a nonzero transfer function**, write

$$
\dot{\mathbf x}=A\mathbf x+B u,
\qquad
y=C\mathbf x+D u,
$$

a **transmission zero** $z$ is a value for which there exist nonzero directions $\mathbf x_0,u_0$ satisfying

$$
\begin{bmatrix}
zI-A & -B\\
C & D
\end{bmatrix}
\begin{bmatrix}
\mathbf x_0\\
u_0
\end{bmatrix}
=
0 .
$$

Equivalently,

$$
(zI-A)\mathbf x_0-Bu_0=0
\qquad\text{and}\qquad
C\mathbf x_0+Du_0=0 .
$$

### Why this is the same idea

Take the input and state to be exponentials with the *same* $s=z$ that has appeared all lecture:

$$
u(t)=u_0e^{zt},
\qquad
\mathbf x(t)=\mathbf x_0e^{zt}.
$$

Then the first equation says $\dot{\mathbf x}=A\mathbf x+Bu$ is satisfied (it is exactly $z\mathbf x_0=A\mathbf x_0+Bu_0$), and the second says

$$
y(t)=C\mathbf x_0e^{zt}+Du_0e^{zt}=0
\qquad\text{for all }t .
$$

So: the internal state evolves as $e^{zt}$, the input $u_0e^{zt}$ sustains that motion, and the output is identically zero. That is precisely §14 and §31, written in matrix form — and note that $u_0$ is generally nonzero, which is why §14's derivation of the required input mattered.

The minimality hypothesis matters: for a nonminimal realization the system-matrix condition describes invariant zeros, which need not coincide with the reduced transfer-function zeros. This section is optional; if included, connect the matrix condition to the exponential trajectory above.

---

## 33. Nonminimum phase does not mean unstable plant

This distinction is worth making explicitly, because students conflate the two constantly.

An unstable **pole** means:

> The system has a natural internal mode that grows when left alone.

A RHP **zero** means:

> The chosen input-output channel has unstable zero dynamics.

A system can therefore have stable poles *and* a RHP zero — and §27 is a fully worked example: four poles at $-1\pm j9.95$ and $-2.5\pm j13.92$, all comfortably stable, alongside a zero at $s=+12.20$.

For each underdamped platform mode, increasing its damping coefficient moves the pole pair leftward toward critical damping; beyond critical damping one real pole returns toward the origin (§7.4). Damping also moves the zeros.

In the worked platform, $AC<0$: the numerator's leading and constant coefficients have opposite signs. Their negative root product forces one positive and one negative real root for every finite damping distribution. Thus **for this geometry**, damping cannot remove the RHP zero.

$$
\boxed{AC<0:\ \text{damping moves the zeros but preserves one RHP root}}
$$

To remove that zero in this case, change $ab$, $J/m$, or $k_\theta/k_x$ — for example by moving the sensor or actuator, redistributing mass, or retuning mount stiffnesses. Outside the $AC<0$ case, damping distribution can create or remove a RHP pair, as §27's reference table shows. There is no general rule that damping affects only location while geometry alone decides existence.

$$
\boxed{
\text{stable plant poles}
\not\Rightarrow
\text{minimum-phase input-output behavior}
}
$$

The upright pendulum of §9.2 supplies the other distinction: it has an unstable pole and no finite zeros. Thus unstable poles do not require RHP zeros. Under §17's convention, we do not call that unstable plant minimum phase.

---

## 34. Why RHP zeros matter in control

A RHP zero places **fundamental** limitations on achievable closed-loop behavior — limitations no controller can design around, because they follow from the plant structure rather than from any particular design.

Conceptually:

1. The output may initially move in the wrong direction (§27, §30).
2. Aggressive tracking becomes difficult: reacting hard to the initial wrong-way motion drives the system the wrong way.
3. **Bandwidth is limited.** Crossover is normally kept comfortably below the RHP zero, with $\omega_c\lesssim z/2$ widely used as an illustrative design target. Be honest with students about the status of that factor: the genuinely fundamental statement is the interpolation constraint below, while any specific number depends on the phase margin you demand, the loop slope, the robustness targets, and whatever else is in the plant. Different texts quote different factors for exactly this reason. What is *not* negotiable is the direction of the effect — a slow RHP zero is a severe constraint, and §29's camera example makes it concrete.
4. Exact pole-zero cancellation is dangerous. Specifically: cancelling a plant RHP zero with a controller RHP pole (or a plant RHP pole with a controller RHP zero) produces a closed loop whose input-output transfer function looks fine but which is **internally unstable** — a hidden mode grows without bound and eventually saturates or breaks something. The cancelled factor does not go away; it just stops being visible from that one input-output pair. This is why §17 insisted $N$ and $D$ be coprime.
5. Fast plant inversion is fundamentally problematic: inverting a RHP zero produces a RHP pole.

### The underlying reason, in one line

For the standard negative-feedback loop with plant $G(s)$ and controller $K(s)$, define the sensitivity $S(s)=1/[1+G(s)K(s)]$. A well-posed, **internally stabilizing** loop satisfies the interpolation constraint

$$
S(z)=1
$$

at every RHP zero $z$ of the plant. Internal stability excludes canceling that zero with a controller RHP pole.

The one-line derivation: $G(z)=0$ at a zero, so $S(z)=1/[1+0\cdot K(z)]=1$. The only escape is for $K$ to have a pole at $z$, making $G(z)K(z)$ an indeterminate $0\cdot\infty$. That is exactly the forbidden RHP cancellation of item 4. Similarly, the complementary sensitivity $T=1-S$ satisfies $T(z)=0$: the closed loop inherits the plant's RHP zero.

Read that carefully: for a real RHP zero, $z>0$ is a point on the **positive real axis of the $s$-plane**, not a sinusoidal frequency. Frequency response lives on $s=j\omega$, so it is wrong to say the sensitivity is stuck at 1 "at that frequency." $S(z)=1$ is an *analytic* constraint pinning the value of $S$ at one point of the complex plane — and because $S$ is analytic, pinning it there restricts how small it can be made along the $j\omega$ axis, which is where performance is actually measured. Together with stability and the remaining plant dynamics, this constraint underlies the tracking and robustness tradeoffs measured on the imaginary axis.

A concise statement for students:

> A RHP zero means that making the output do exactly what we want may require the internal system to do something unstable.

---

# Part III — Materials

## 35. One-board summary

If you want one final board at the end of Part I, write:

$$
\boxed{
e^{st}
}
$$

$$
\dot x\rightarrow sx,
\qquad
\ddot x\rightarrow s^2x
$$

$$
\boxed{
s=\sigma+j\omega
}
$$

$$
\Re(s)<0
\Rightarrow
\text{decay}
\qquad
\Re(s)>0
\Rightarrow
\text{growth}
\qquad
\Im(s)\neq0
\Rightarrow
\text{oscillation}
$$

Then:

$$
\boxed{
G(s)=\frac{N(s)}{D(s)}
}
$$

$$
D(s)=0
\Rightarrow
\text{poles}
\qquad
N(s)=0
\Rightarrow
\text{zeros}
$$

$$
y(t)\equiv0
\Rightarrow
\text{zero dynamics}
$$

$$
\text{RHP zero}
\Rightarrow
\text{nonminimum phase}
$$

Finally:

$$
\boxed{
X(s)
=
\int_{0^-}^{\infty}
x(t)e^{-st}\,dt
}
$$

and close with:

> **The Laplace transform works because exponentials are the natural language of linear differential equations.**

---

## 36. Discussion questions

These work well as pauses during the lecture.

### Thermal system (§5)

1. Why must the thermal pole be real in this simple one-state model?
2. What physical changes move the pole closer to the origin?
3. Why does a larger thermal resistance slow the system?
4. The transfer function $R/(\tau s+1)$ blows up at $s=-1/\tau$. What is physically happening at that value of $s$?

### Spring-mass-damper (§6–§8)

1. What determines whether the roots are real or complex?
2. What does the real part of $s$ do? The imaginary part?
3. If the displacement is a real number, where did the $j$ go?
4. What would a pole in the RHP mean physically?
5. We found $G(s)=1/(ms^2+cs+k)$ by assuming a *particular* solution. What happened to the free modes?
6. Why is the denominator of $G(s)$ the same polynomial as the characteristic equation? (Answer it with the "no input" argument, not by inspection.)

### Pendulum and the $s$-plane (§9–§10)

1. Why does the same pendulum have different linear models around downward and upright equilibria?
2. What changed sign, and why does that sign change cause instability?
3. Locate both pendulum models' poles on the $s$-plane. What physically happened between the two pictures?
4. What kind of motion corresponds to a pole exactly at the origin?

### Two-mass system (§11–§16)

1. If $x_1=0$, must $x_2=0$?
2. Can internal energy exist when the measured output is zero?
3. Holding $x_1\equiv 0$ requires an input. What is that input doing, physically?
4. Why did moving the sensor change the zeros but not the poles?
5. The collocated numerator turned out to be the pinned-$m_2$ characteristic polynomial. Would you expect that pattern to generalize?

### Laplace transform (§18–§21)

1. Why do exponentials make differential equations easy?
2. What is the precise difference between $\dot x\leftrightarrow sx$ and $\mathcal L\{\dot x\}=sX-x(0^-)$?
3. When do characteristic roots appear as transfer-function poles, and what can a cancellation hide?
4. What does the region of convergence have to do with $\sigma$?
5. Looking at the inversion integral, in what sense is the Laplace transform "the same idea" as substituting $e^{st}$?
6. The heater starts from zero temperature deviation. Why does its step response still contain $e^{-t/\tau}$?

### Zeros and geometry (Part II)

1. Why is the ball-and-beam underactuated — and under which of the two models in §24.2?
2. Does underactuation automatically imply a RHP zero?
3. Why does moving the quadrotor's output point create a zero, and why does *below* the center of mass differ from *above*?
4. Why does adding damping to the rigid platform in §27 not remove the RHP zero?
5. What do §27 and §29 have in common mechanically?
6. Can a stable plant have a RHP zero? Can an unstable plant have no finite zeros?

---

## 37. Homework and follow-up problems

Answer sketches are included so the material can be used directly in section.

### Problem 1: Thermal pole placement

For $C\dot x+\frac1R x=0$, choose $R$ so that the pole is $s=-2\ \text{s}^{-1}$ for a known $C$.

> **Sketch.** $s=-1/(RC)=-2 \Rightarrow RC=\tfrac12 \Rightarrow R=1/(2C)$. Then $\tau=0.5\ \text{s}$, so the response decays to about 37% of its initial value in half a second.

### Problem 2: Damping classification

Given $m=1$, $k=25$, find the values of $c$ corresponding to overdamped, critically damped, and underdamped behavior.

> **Sketch.** $c^2-4mk=c^2-100$. Overdamped $c>10$; critically damped $c=10$; underdamped $0<c<10$. The natural frequency is $\omega_n=\sqrt{k/m}=5$ rad/s and the damping ratio is $\zeta=c/(2\sqrt{mk})=c/10$. For $c=6$: $\sigma=-3$, $\omega_d=4$, so poles at $-3\pm j4$ — on a circle of radius 5, as $|s|=\omega_n$ requires.

### Problem 3: Upright pendulum poles

Ignoring damping, show that the upright pendulum has poles $s=\pm\sqrt{m_pgl/J}$, and interpret both roots physically.

> **Sketch.** With $b=0$, $Js^2-m_pgl=0$. The positive root is the falling mode — the one you actually see. The negative root is real too: it corresponds to the single special family of initial conditions (a precise inward velocity for a given displacement) that would carry the pendulum *asymptotically* toward upright without ever reaching it. Any perturbation off that stable manifold excites the growing mode. This is why balancing requires continuous feedback rather than one perfect push.

### Problem 4: Two-mass zero

For the collocated transfer function $X_1/U=(m_2s^2+c_2s+k_2)/D(s)$, show that the zeros are exactly the natural poles of the $m_2$-subsystem when $x_1$ is constrained to zero.

> **Sketch.** Set $x_1\equiv0$ in the $m_2$ equation of §11; the coupling terms in $x_1$ drop out and leave $m_2\ddot x_2+c_2\dot x_2+k_2x_2=0$. Substituting $x_2=Ae^{st}$ gives the numerator. Physically, $x_1\equiv0$ is indistinguishable from bolting $m_2$'s spring and damper to a wall. Then find the input required to sustain this: from the $m_1$ equation, $u=-(c_2\dot x_2+k_2x_2)$.

### Problem 5: Noncollocated sensor

Derive $X_2/U=(c_2s+k_2)/D(s)$, and explain why changing the measured output changes the numerator but not the denominator.

> **Sketch.** Cramer's rule on the §12 matrix: $X_2=(-b\,U)/\det$ with $b=-(c_2s+k_2)$. The denominator is the determinant, which is a property of the matrix alone — that is, of the plant. The numerator involves which row of the solution you read off, i.e. which coordinate you measure.

### Problem 6: Recovering a real solution

A system has poles at $s=-1\pm j3$ and initial conditions $x(0)=2$, $\dot x(0)=0$. Write $x(t)$ in real form.

> **Sketch.** $x(t)=e^{-t}(B\cos 3t+C\sin 3t)$. From $x(0)=2$, $B=2$. Differentiating, $\dot x(0)=-B+3C=0$, so $C=2/3$. Hence $x(t)=e^{-t}\left(2\cos 3t+\tfrac23\sin 3t\right)$. Check that the answer contains no $j$, and identify which feature of the answer came from $\sigma$ and which from $\omega_d$.

### Problem 7: Quadrotor sensor offset

Starting from $\ddot x=g\theta$ and $J\ddot\theta=M$, with $y=x-h\theta$, derive

$$
\frac{Y}{M}=\frac{g-hs^2}{Js^4}.
$$

Find the zeros, identify the nonminimum-phase zero, and state where the measurement point is relative to the center of mass.

> **Sketch.** $X/M=g/(Js^4)$ and $\Theta/M=1/(Js^2)$; subtract $h$ times the second from the first. Zeros at $s=\pm\sqrt{g/h}$, with $s=+\sqrt{g/h}$ in the RHP. The output $y=x-h\theta$ describes a point a distance $h$ **below** the center of mass. A point *above* it ($y=x+h\theta$) yields $\pm j\sqrt{g/h}$ — on the imaginary axis, not in the RHP.

### Problem 8: When damping can and cannot remove a RHP zero

For the rigid platform of §27:

1. Show that the numerator has one strictly positive and one strictly negative real root exactly when $ab$ lies strictly between $J/m$ and $k_\theta/k_x$. Explain why damping cannot remove the RHP zero in this case.
2. With $ab=0.15$ and the worked parameters, compare zeros for $(c_x,c_\theta)=(0,0),(2,0.5),(2,0.2)$.
3. Now set $ab=0.05$ and $c_x=2$, keeping $m,J,k_x,k_\theta$ fixed. Find the zeros at $c_\theta=0.05$ and $0.20$. Does the conclusion of part 1 apply?

> **Sketch.** Write $N(s)=As^2+Bs+C$, where $A=J-abm$, $B=c_\theta-abc_x$, and $C=k_\theta-abk_x$. The product $C/A$ is negative exactly when $(J/m-ab)$ and $(k_\theta/k_x-ab)$ have opposite signs. This forces one positive and one negative real numerator root independently of $B$. Stable plant poles cannot cancel the positive root.
>
> In part 2 the zeros are $\pm10$, then $+12.20,-8.20$, then $+9.05,-11.05$. Damping changes their locations but leaves the product negative.
>
> In part 3, $A=0.05$ and $C=15$, so $AC>0$. The two choices give $B=-0.05$ and $B=0.10$, hence zeros $0.5\pm j17.3133$ and $-1\pm j17.2916$. Damping removes the RHP pair with geometry fixed. A negative root product is sufficient, not necessary, for a RHP zero.

**Optional extension:** with $ab=0.05$, $c_x=100$, and $c_\theta=0.05$, verify two positive real zeros near $3.12921$ and $95.87079$. This disproves the claim that merely saying “real RHP zero” makes the interval condition necessary.

### Problem 9: Design consequence

A quadrotor carries a camera $h=0.35\ \text{m}$ below its center of mass and must servo that camera's horizontal position. Estimate the order of magnitude of the achievable closed-loop bandwidth. What happens if the mounting is lengthened to $0.7\ \text{m}$, and what does that tell you about how to fix the problem?

> **Sketch.** The zero rate is $z=\sqrt{9.81/0.35}\approx5.3\ \mathrm{s}^{-1}$. Using the $z/2$ design target gives crossover near $2.6$ rad/s ($\approx0.42$ Hz). Doubling $h$ gives $z\approx3.7\ \mathrm{s}^{-1}$ and a target near $1.9$ rad/s — a slower loop target.
>
> Students should be able to say what is and is not solid here. The scaling $z=\sqrt{g/h}$ is exact for this model, and the direction (longer mount $\rightarrow$ slower loop) is robust. The factor of $1/2$ is a design heuristic, not a theorem, so quoting "2.6 rad/s" to two figures overstates what we know. The actionable conclusion is unaffected: the fix is geometric, not algorithmic — shorten the mount, or servo a different output.

---

## 38. Instructor cautions

1. **Do not say that $s$ starts real and later becomes complex.**
   Say that $s$ is allowed to be complex from the beginning; the thermal system simply selects a real value.

2. **Distinguish the two roles of $s$.**
   For free motion, solve for allowed rates. For a test input, choose the rate and solve for the particular-response amplitude. The ratio $X/F$ comes from this forced calculation (§8); the same characteristic polynomial supplies its denominator.

3. **Do not skip the real-solution reconstruction (§7.5).**
   Students who never see $2\Re\{Ae^{st}\}$ resolve into $e^{\sigma t}(B\cos+C\sin)$ quietly conclude that complex poles are a formal trick with no physical content.

4. **Do not imply that every noncollocated system is nonminimum phase.**
   Noncollocation removes the interlacing *guarantee* and may produce RHP zeros; it does not create them by itself.

5. **Do not imply that underactuation implies RHP zeros.**
   The quadrotor center-of-mass channel has no finite zeros, but its four integrators prevent asymptotic and BIBO stability. Use that precise description rather than calling it minimum phase (§17, §28).

6. **Do not claim that the simple ball-and-beam model has a finite RHP zero.**
   Its value in this lecture is as a bridge to internal-state thinking. Also state which of the two models in §24.2 you are using; the angle-input and torque-input versions differ in order and only the latter is underactuated.

7. **Distinguish unstable poles from RHP zeros.**
   §27 has stable poles and a zero at $s=+12.20$; the upright pendulum has an unstable pole and no finite zeros. Also distinguish exponential instability from polynomial growth at repeated axis poles (§10).

8. **Say which collocation guarantee you mean.**
   For the ideal passive mechanical model, force/displacement collocation excludes finite RHP zeros; exact interlacing concerns participating undamped modes. Force/velocity collocation gives positive-real structure. Velocity feedback adds dissipation, but asymptotic decay requires that no undamped mode escape the damping/feedback (§25).

9. **Qualify the damping claim by $AC<0$.**
   In that case the numerator retains one positive and one negative real root for every finite damping distribution. If $AC>0$, damping can move a pair between half planes. The interval condition is not necessary for a RHP zero, even a real one (§27, Problem 8).

10. **Do not call $\sqrt{g/h}$ a pendulum frequency (§29).**
    The zero dynamics give $\ddot\theta=+(g/h)\theta$ — an inverted pendulum, diverging — not $\ddot\theta=-(g/h)\theta$. The magnitude matches a hanging pendulum's frequency; the behavior is its opposite.

11. **Do not say a zero makes the output zero.**
    Driving with $u=e^{zt}$ blocks only the $e^{zt}$ *component*; the plant's own modes still appear. Identically zero output requires the matched initial state of §32.

12. **Treat inverse response as intuition, not definition.**
    Wrong-way initial motion is often associated with RHP zeros but is not itself the formal definition (§17, §31).

13. **Do not present $\omega_c\lesssim z/2$ as a theorem.**
    It is a design heuristic whose factor depends on margins and loop shape. The fundamental statement is $S(z)=1$ (§34).

14. **Do not call a real RHP zero a frequency.**
    $z>0$ is a point on the positive real axis; frequency response lives on $s=j\omega$. $S(z)=1$ is an analytic interpolation constraint, not a statement about the response at $\omega=z$ (§34).

15. **Use a consistent unilateral-transform convention.**
    The $0^-$ convention includes an impulse at switching and the state just before it. For ordinary continuous signals, writing 0 as the integration limit is harmless; jumps and impulses require the convention to be explicit (§18–§19).

16. **Do not equate "same side of the center of mass" with collocation.**
    Collocation is the special case $b=-a$. The favorable sign structure covers a larger set than collocation does (§27).

17. **Define underactuation by degrees of freedom, not states.**
    Actuators versus configuration DOFs — counting states gets it wrong (§24.2).

18. **Keep $\tau$ for the time constant and $M$ for torque.**
    This distinguishes the thermal time constant of §5/§20.1 from the applied moments in the rotational examples.

19. **Keep the transform payoff in the live lecture.**
    Finish §20.1. The switched-heater response shows what the transform adds, and demonstrates that zero initial state does not mean an absence of natural-mode transients.

20. **Keep demo captions within the model assumptions.**
    Demo 4 is damped and has a finite notch; Demo 5's hidden motion decays; Demo 8 shows the linearized model, whose large-angle trajectories are not physical predictions.

---

## 39. Demonstration index

Eight scripts in `demos/`. Each prints an annotated narrative and writes a figure
to `demos/figures/`. All eight regenerate in about 18 seconds:

```
cd demos
uv run python run_all.py
```

Every demo accepts `--show` (interactive window instead of files) and `--no-save`
(terminal narrative only).

| # | Script | Cue at | Shows | Live? |
|---|---|---|---|---|
| 1 | `demo1_splane_modes.py` | §10 | Six pole locations beside the motion each produces | slide |
| 2 | `demo2_damping_pole_locus.py` | §7.4 | Damping moves poles around the circle $\lvert s\rvert=\omega_n$ | **live** |
| 3 | `demo3_real_from_complex.py` | §7.5 | Two complex modes adding to one real motion | slide |
| 4 | `demo4_sensor_moves_zeros.py` | §16 | Identical poles, completely different zeros | slide |
| 5 | `demo5_zero_dynamics.py` | §14 | $y\equiv0$ while the system moves, and the input it costs | **live** |
| 6 | `demo6_antiresonance.py` | §15 | Drive the mass at $\sqrt{k_2/m_2}$ and it does not move | slide |
| 7 | `demo7_damping_moves_zeros.py` | §27 | For the selected $AC<0$ geometry, zeros move but retain opposite signs | slide |
| 8 | `demo8_quadrotor_rhp.py` | §29 | Inverse response, and the divergent $\ddot\theta=(g/h)\theta$ behind it | **live** |

`twomass.py` holds the shared §11 model used by demos 4–6; `demokit.py` holds the
plotting and narration helpers.

### What the demos verify

They recompute the lecture's numbers rather than reprinting them, which is the
point — several exist to settle claims a sceptical student should not take on
trust:

| Claim | Where | What the script reports |
|---|---|---|
| $\lvert s\rvert=\omega_n$ is fixed as $c$ varies | §7.4 | max deviation $1.8\times10^{-15}$ over the underdamped range |
| Conjugate modes cancel exactly | §7.5 | $\max\lvert\Im(\text{sum})\rvert = 0$; matches Problem 6 and a numerical solve to $5\times10^{-12}$ |
| Moving the sensor leaves the poles alone | §16 | largest pole discrepancy `0.00e+00` |
| $y\equiv0$ does not mean the system is still | §14 | $\max\lvert x_1\rvert\approx3.2\times10^{-17}$ over 60 s while $x_2$ oscillates with a decaying envelope |
| The hidden motion follows the *zero dynamics* | §14 | measured frequency $3.99997$ rad/s and decay $0.02000\ \mathrm{s}^{-1}$, versus zeros $-0.02\pm j3.99995$ |
| The antiresonance is an exact null | §15 | $\lvert X_1/U\rvert$ at $\omega=4$ is `0.000e+00` |
| Damping preserves opposite root signs when $AC<0$ | §27 | reproduces both damping families; product $C/A$ pinned at $-100$ across 500 points |
| The RHP zero *is* the zero-dynamics rate | §29 | $7.00357$ from three independent routes |

### Interpreting the numerical checks

Use the inline cues to distinguish exact algebra from finite-time simulation and physical-model validity. Demo 4's damped notch near 4 rad/s illustrates the ordering of resonances and attenuation; Demo 6 sets $c_2=0$ for an exact null. Demo 5 verifies both the frequency and decay rate of the hidden motion. Demo 8's agreement with the linear equations does not extend the small-angle model to large angles.

The scripts retain their original narration; when presenting them, use the corrected cue text in this document, especially Demo 8's “no finite zeros” description of the CM channel. Numerical residuals depend on the solver and environment; they are representative checks, not universal constants.

---

## 40. Revision notes — version 0.0.8

This version preserves the lecture's Parts I–III and the main worked examples. The earlier revision history remains in the unchanged `lecture_0.0.7.md`. Changes here incorporate the mathematical reviews and rebuttal:

- **§4–§8: rate notation.** Use $s$ consistently; free motion solves for it, while forcing chooses it. Amplitude ratios precede transform notation.
- **§7, §10, §31: stability.** Restrict the constant-radius locus to the range through critical damping; distinguish exponential growth, nondecaying axis modes, and possible polynomial growth.
- **§12–§17, §32: poles and zeros.** State the cancellation/minimality assumptions where needed. Keep natural rates, visible transfer poles, and zero-dynamics rates distinct.
- **§17, §25, §28–§29: terminology and collocation.** Announce the minimum-phase convention, use the DC-normalized all-pass factor, label the CM channel “no finite zeros,” and specify the assumptions behind interlacing and passive velocity feedback.
- **§18–§20: Laplace payoff.** State a sufficient exponential-order condition, identify the inversion line, distinguish zero-state/zero-input from particular/homogeneous responses, and add a complete switched-heater calculation.
- **§27, §33, Problem 8, §38: RHP-zero condition.** The interval condition characterizes opposite-sign real numerator roots. It is sufficient, not necessary, for a RHP zero. Damping immunity is restricted to $AC<0$; the reference table and homework show how damping changes half planes when $AC>0$.
- **§27, §29–§30: inverse response.** Use acceleration and static gains for the parallel platform paths, and relative degree for the quadrotor cascade. Handle numerator degree reductions explicitly.
- **Demo cues and §39.** Correct the damped-notch and decaying-amplitude descriptions; identify the quadrotor simulations as linear-model responses with local physical validity.
- **Planning and materials.** Reserve time for the thermal step response, use prepared algebra/comparison slides, and align questions, cautions, and summaries with the corrected statements.
