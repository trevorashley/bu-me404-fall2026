# From Physical Models to the Laplace Transform

**Student lecture notes — exponential modes, poles, and zeros**

Physical laws lead to differential equations. Exponential trial solutions turn those equations into algebra in $s$, revealing natural rates and transfer functions. The Laplace transform extends this calculation to switched inputs and carries initial conditions into the algebra.

**Prerequisites:** Basic ordinary differential equations, complex numbers, and elementary matrix algebra.

**Next lecture:** [Zeros, Geometry, and Noncollocation](modeling-and-dynamics-zeroes_student.md).

## Learning objectives

After studying this lecture, you should be able to:

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

## Notation and assumptions

**Notation conventions used throughout:**

| Symbol | Meaning |
|---|---|
| $\tau$ | time constant (never torque) |
| $M$ | applied torque or moment |
| $m_p,\ l$ | pendulum mass and pivot-to-center-of-mass distance |
| $j$ | imaginary unit |
| $s$ | complex exponential rate: solve for it in free motion; choose it when testing a forced response |
| $s_i$ | a system-selected natural rate, located on the $s$-plane |
| $A$ | complex amplitude in $x = Ae^{st}$; local coefficient/matrix uses in [Lecture 2, §4](modeling-and-dynamics-zeroes_student.md#section-4)/[Lecture 2, §9](modeling-and-dynamics-zeroes_student.md#section-9) are defined there |
| $\mathcal A(s)$ | Laplace transform of a beam angle $\alpha(t)$ |

Physical masses, inertias, capacitances, resistances, and restoring stiffnesses are positive unless stated otherwise; damping coefficients are nonnegative. Amplitudes such as $X$ and $U$ are numbers. Transforms such as $X(s)$ and $U(s)$ are introduced in [§15](#section-15).

---

## 1. Opening: why $e^{st}$? {#section-1}

Physical modeling leads to differential equations. A useful question is:

**What motions of the form $x(t)=Ae^{st}$ are compatible with the physics?**

The symbol $s$ denotes an exponential rate. In free motion, the physics selects the allowed rates. In a forced problem, we choose a test-input rate and solve for the response amplitude. The rate is allowed to be complex from the beginning:

$$ s=\sigma+j\omega.  $$

Some systems select real rates; others select complex-conjugate pairs. The same derivative identities apply in either case.

$$ x(t)=Ae^{st} $$

$$ \dot{x}=sAe^{st} $$

$$ \ddot{x}=s^2Ae^{st} $$

$$\boxed{ \frac{d}{dt} \text{ acts like multiplication by }s \text{ on }e^{st} } $$

### Check your understanding

**Why are exponentials useful here?** Their derivatives are proportional to themselves, so substitution turns derivatives into algebraic factors. For $a>0$, $a^t=e^{t\ln a}$ has this property; constants are the zero-rate case.

**What units must $s$ have?** The exponent $st$ must be dimensionless, so the units must be inverse time.

$\sigma$ carries units of inverse seconds (nepers per second), and $\omega$ carries radians per second. Both halves of $s$ are rates.

---

## 2. Thermal system {#section-2}

Consider a lumped thermal body connected to an environment through a thermal resistance.

Let

- $T(t)$: body temperature,
- $T_a$: ambient temperature,
- $C$: thermal capacitance,
- $R$: thermal resistance,
- $q_{\mathrm{in}}(t)$ : externally supplied heat flow (used in [§2.4](#section-2-4)).

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

### 2.1 Derivation from first principles {#section-2-1}

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

### 2.2 The free response {#section-2-2}

We have reduced a physical thermal problem to a first-order linear differential equation.

Try a function whose derivative has the same shape as the original function. Its unknown natural rate is $s$.

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

### 2.3 Interpretation {#section-2-3}

The differential equation

$$
C\dot x+\frac1R x=0
$$

became the algebraic equation

$$
Cs+\frac1R=0.
$$

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

#### Check your understanding

If $R$ becomes larger, does the system respond faster or slower?

**Answer:** $\tau=RC$ increases, so $|s|=1/(RC)$ decreases, the pole moves *toward the origin*, and the response becomes slower. This movement is shown on the $s$-plane in [§7](#section-7).

### 2.4 Adding an input: the first transfer function {#section-2-4}

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

The two roles of $s$ are distinct. In the **free** problem, set the input to zero and solve for the allowed rates. In the **forced** problem, choose a test rate and solve for the response amplitude. The differential equation supplies the same polynomial in both calculations.

This ratio is the **transfer function**: the complex gain relating the exponential input amplitude to its particular-response amplitude.

The gain fails to be defined at the natural rate. Undefined gain here does not mean an infinite time signal; it means our same-exponential forced-response assumption has collided with a natural mode.

The denominator vanishes at $s = -1/\tau$ — and that is exactly the natural rate $s$ we found in [§2.2](#section-2-2) with no input at all.

That is not a coincidence, and it is going to keep happening. In the free problem, values of $s$ that kill this polynomial are values at which the system can produce an output with **no input**. Those are the natural modes. In the forced problem, choosing the same rate for a nonzero input makes the same-exponential particular-response formula fail. We will soon call those shared values poles.

$$
\boxed{
\text{denominator}=0
\iff
\text{motion is possible with no input}
}
$$

---

## 3. Spring-mass-damper {#section-3}

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

### 3.1 Apply the same exponential idea {#section-3-1}

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

The same substitution applies to both systems.

The thermal system produced a first-degree polynomial in $s$.

This second-order mechanical system produces a second-degree polynomial in $s$.

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

The order of the differential equation has become the degree of a polynomial.

### 3.2 How many modes should we expect? {#section-3-2}

The solution space of an $n$th-order homogeneous linear ODE is $n$-dimensional — you need $n$ initial conditions to pin down a solution. Generically the characteristic polynomial has $n$ distinct roots, giving $n$ independent modes $e^{s_1t},\dots,e^{s_nt}$, and by linearity any sum of them is also a solution. So counting works out: $n$ roots, $n$ free constants, $n$ initial conditions.

Repeated roots require generalized modes, as in [§4.2](#section-4-2).

---

## 4. Complex $s$: damping and oscillation {#section-4}

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

### 4.1 Overdamped: $c^2>4mk$ {#section-4-1}

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

This sign argument lets us infer stability directly from the coefficients.

### 4.2 Critically damped: $c^2=4mk$ {#section-4-2}

There is a repeated root

$$
s=-\frac{c}{2m},
$$

and only one exponential — but [§3.2](#section-3-2) says we need two independent solutions. The generalized form supplies the second:

$$
x(t)=(A+Bt)e^{st}.
$$

To verify the generalized solution, let $x=(A+Bt)e^{st}$. Then

$$
\dot x=[B+s(A+Bt)]e^{st},\qquad
\ddot x=[2sB+s^2(A+Bt)]e^{st}.
$$

Substitution gives $[ (ms^2+cs+k)(A+Bt)+(2ms+c)B ]e^{st}=0$, because both $ms^2+cs+k=0$ and $2ms+c=0$ at the repeated root.

**Why the repeated root matters.** The $Ae^{st}$ part solves the equation already, so the new piece to check is $x=te^{st}$. Its derivatives are $\dot x=(1+st)e^{st}$ and $\ddot x=(2s+s^2t)e^{st}$. Substituting and grouping by powers of $t$:

$$
m\ddot x+c\dot x+kx=\big[\underbrace{(ms^2+cs+k)}_{=0\text{ (root)}}\,t+\underbrace{(2ms+c)}_{=0\text{ at }s=-c/2m}\big]e^{st}=0 .
$$

The first bracket vanishes because $s$ is a root. The second vanishes *only* because the root is repeated: $2ms+c$ is the derivative of the characteristic polynomial, and a repeated root is also a root of the derivative. For distinct roots the second bracket is nonzero, and $te^{st}$ is not a solution.

### 4.3 Undamped: $c=0$ {#section-4-3}

The roots are purely imaginary:

$$
s=\pm j\sqrt{\frac{k}{m}}
=\pm j\omega_n .
$$

Here $\sigma=0$: neither growth nor decay, just sustained oscillation at the natural frequency $\omega_n=\sqrt{k/m}$.

This oscillatory case returns as a zero in the undamped antiresonance ([§12](#section-12)) and for the above-CM quadrotor output ([Lecture 2, §6](modeling-and-dynamics-zeroes_student.md#section-6)). The quadrotor's repeated poles at the origin are different: they can produce polynomial motion ([§7](#section-7)).

### 4.4 Underdamped: $0<c<2\sqrt{mk}$ {#section-4-4}

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

The parameters affect both coordinates of the pole. Damping does **not** simply slide the poles left. Squaring and adding,

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

For a numerical example, take $m=1$, $k=25$ (so $\omega_n=5$). Each row uses $\sigma=-c/2$ and $\omega_d=\sqrt{100-c^2}/2$. For example, $c=4$ gives $\omega_d=\sqrt{84}/2=4.58$, and $|s|=\sqrt{4+21}=5$:

| $c$ | $\sigma$ | $\omega_d$ | $\lvert s\rvert$ |
|---:|---:|---:|---:|
| $0$ | $0$ | $5.00$ | $5$ |
| $4$ | $-2$ | $4.58$ | $5$ |
| $8$ | $-4$ | $3.00$ | $5$ |
| $9.9$ | $-4.95$ | $0.71$ | $5$ |

This arc is a root locus: a path traced by roots as a parameter varies.

![How damping changes pole locations and time responses for fixed mass and stiffness.](demos/figures/demo2_damping_pole_locus.png)

**Numerical check.** The figure’s leftward-motion title applies up to critical damping. In that range, the pole magnitudes remain $\omega_n$; the accompanying calculation gives a maximum deviation of about $1.8\times10^{-15}$. Beyond critical damping, one real pole moves toward the origin.

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

### 4.5 Getting a real answer back {#section-4-5}

**My displacement is a real number. Where did the $j$ go?**

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

Twice the real part is $e^{\sigma t}(2\alpha\cos\omega_dt-2\beta\sin\omega_dt)$. This is a real form, with $B=2\alpha$ and $C=-2\beta$:

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

since $2\Re\{|A_1|e^{j\psi}e^{j\omega_dt}\}=2|A_1|\cos(\omega_dt+\psi)$. In the worked example below, $A_1=1-j/3$, which gives $B=2$ and $C=2/3$.

The imaginary parts did not disappear. They cancelled, because they always arrive in pairs.

A complex mode is not a physical motion by itself. A conjugate pair is. The envelope $e^{\sigma t}$ comes from the real part of $s$, and the ringing inside it comes from the imaginary part.

#### Worked example: initial conditions and conjugate modes

For $s=-1\pm j3$, $x(0)=2$, and $\dot x(0)=0$, write

$$
x(t)=e^{-t}(B\cos 3t+C\sin 3t).
$$

The first condition gives $B=2$. Differentiating and evaluating at zero gives $-B+3C=0$, so $C=2/3$. Therefore

$$
\boxed{x(t)=e^{-t}\left(2\cos 3t+\frac23\sin 3t\right).}
$$

Equivalently, $A_1=1-j/3$ and $A_2=1+j/3$. Their imaginary contributions cancel. A numerical ODE solution agrees to about $5\times10^{-12}$.

![A conjugate pair of complex modes combines to give a real displacement.](demos/figures/demo3_real_from_complex.png)

The thermal system did not require us to invent a new variable.

It simply selected a real natural rate.

The spring-mass-damper selects complex natural rates when it oscillates.

A natural rate was always allowed to be complex.

The first system simply happened to live on the real axis.

---

## 5. Forcing the spring-mass-damper: the transfer function {#section-5}

[§3](#section-3)–[§4](#section-4) described free motion: set the force to zero and solve for the natural rates $s_1,s_2$. Now repeat the forced-response calculation of [§2.4](#section-2-4): choose an input rate $s$ and solve for the response amplitude.

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

Three distinctions matter:

**1. This is the particular solution only.** The complete response is

$$
x(t)=\underbrace{G(s)Fe^{st}}_{\text{forced}}
+\underbrace{A_1e^{s_1t}+A_2e^{s_2t}}_{\text{free modes from §4}},
$$

Here $s$ is the chosen test-input rate, while $s_1,s_2$ are the natural rates. The initial conditions determine $A_1,A_2$, including when the system starts from rest. This display assumes distinct roots; at critical damping use $(A+Bt)e^{s_1t}$. For positive damping the homogeneous part decays, with ringing only in the underdamped case; at zero damping it can persist.

**2. The denominator is the characteristic polynomial.** Not a similar polynomial — the *same* one, letter for letter, that came out of [§3.1](#section-3-1):

$$
\underbrace{ms^2+cs+k}_{\text{§3: free modes}}
\quad=\quad
\underbrace{ms^2+cs+k}_{\text{§5: denominator of }G(s)}
$$

The reason follows from [§2.4](#section-2-4): in the free problem, at a root of the denominator, the equation $(ms^2+cs+k)X=F$ has a nonzero solution $X$ when $F=0$. A root of the denominator is precisely a rate the system can sustain with no input — which is what a natural mode *is*. In the forced problem, choosing that same rate for a nonzero input means the ordinary same-exponential particular solution no longer exists.

$$
\boxed{
\text{poles of }G(s)
=
\text{roots of the characteristic equation}
=
\text{natural exponential rates}
}
$$

**Scope of the pole interpretation.** In these one-coordinate models, every natural rate appears as a transfer-function pole. For a general state model, a mode must be both excitable by the input and visible at the output to appear in the reduced transfer function. Common factors can cancel; [§13](#section-13)–[§14](#section-14) returns to this point.

**3. Amplitudes and transforms.** Here $X$ and $F$ are complex *amplitudes* — numbers. In [§15](#section-15) we will define $X(s)$ and $F(s)$ as Laplace *transforms* — functions. For zero initial conditions these give the identical ratio, which is why the same symbol $G(s)$ serves both.

### Frequency response

Choose $s=j\omega$, away from any pole: a pure oscillation with no growth or decay. Then $G(j\omega)$ gives the sinusoidal particular response: its magnitude is the amplitude ratio and its angle is the phase shift. If the free transients decay, this is the eventual response. That is the frequency response, and it is where Bode plots come from.

---

## 6. Rotational version: the pendulum {#section-6}

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

### 6.1 Linearization about the downward equilibrium {#section-6-1}

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

The correspondence is structural, not a substitution — note that the $m$ on the left below is the translational mass of [§3](#section-3), while $m_p$ is the pendulum mass:

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

Locally, a pendulum near its downward equilibrium looks just like a rotational spring-mass-damper.

The nonlinear system has become linear because we chose an operating point and considered small perturbations around it.

### 6.2 Linearization about the upright equilibrium {#section-6-2}

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

## 7. The $s$-plane {#section-7}

The $s$-plane represents exponential rates geometrically: the horizontal axis is $\sigma=\Re(s)$ and the vertical axis is $\omega=\Im(s)$.

### Pole-location diagram

```text
                             Im(s) = omega
                                   ^
                                   |
          decaying                 |                growing
        oscillation   x            |            x   oscillation
          (§4.4)                   |                  (too much
                                   x  sustained         loop gain)
                                   |  oscillation
                                   |  (§4.3, c = 0)
    -----x----------x--------------+-------------x---------------> Re(s) = sigma
       fast        slow            |          upright
       decay       decay           |          pendulum
       (small RC)  (large RC)      |          (§6.2)
                                   x
                                   |
                      x            |            x
                                   |
     <---------- LHP: decay -------|------- RHP: growth ---------->
```

![Pole locations and their corresponding time responses.](demos/figures/demo1_splane_modes.png)

**Reading the figure.** Farther left means faster exponential decay; a nonzero imaginary part produces oscillation. Right-half-plane rates produce growth. Axis modes require the separate stability checks below.

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

| Location of $s$ | $x(t)$ looks like | Example in this lecture |
|---|---|---|
| Far left, real axis | Fast decay, no ringing | Thermal body, small $RC$ ([§2](#section-2)) |
| Near origin, real axis | Slow decay, no ringing | Thermal body, large $RC$ ([§2](#section-2)) |
| Upper/lower LHP pair | Decaying oscillation | Underdamped spring-mass-damper ([§4.4](#section-4-4)) |
| Simple pair on the $j\omega$ axis, away from zero | Constant-amplitude free oscillation | Undamped spring-mass ($c=0$, [§4.3](#section-4-3)) |
| Upper/lower RHP pair | Growing oscillation | Unstable flutter, servo with too much gain |
| Right, real axis | Pure growth, no ringing | Upright pendulum ([§6.2](#section-6-2)) |
| At the origin | Constant; repeated scalar roots also allow powers of $t$ | Free mass: $m\ddot x=0$ gives $x=x_0+v_0t$ |

For a mode, farther left means faster decay, and a nonzero imaginary part means oscillation. All state eigenvalues strictly in the LHP give asymptotic stability; a RHP eigenvalue gives exponential instability. On the imaginary axis, free motion may persist or grow polynomially — a free mass with initial velocity already shows why “no RHP pole” is not enough.

**Stability distinction:** Bounded-input/bounded-output (BIBO) stability asks whether every bounded input gives a bounded zero-state output. For a reduced proper rational transfer function, it requires every pole strictly in the LHP; even the undamped oscillator can grow under resonant forcing. For state-model free motion, semisimple imaginary-axis eigenvalues permit bounded motion, while nontrivial Jordan blocks add powers of $t$. A repeated state eigenvalue by itself does not prove polynomial growth.

---

## 8. Add a second mass: flexible two-mass system {#section-8}

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

**Parameters for the numerical examples.** Unless a different value is stated, the two-mass figures use $m_1=1\ \mathrm{kg}$, $m_2=0.5\ \mathrm{kg}$, $k_1=20\ \mathrm{N/m}$, $k_2=8\ \mathrm{N/m}$, $c_1=0.20\ \mathrm{N\,s/m}$, and $c_2=0.02\ \mathrm{N\,s/m}$. The exact antiresonance example sets $c_2=0$ and uses a sinusoidal force of amplitude $1\ \mathrm{N}$.

---

## 9. Exponential form for the two-mass system {#section-9}

Choose a test rate $s$, as in [§5](#section-5), and seek a particular response with two coordinates. Here $X_1,X_2,U$ are complex amplitudes:

$$
x_1=X_1e^{st},
\qquad
x_2=X_2e^{st},
\qquad
u=Ue^{st}.
$$

Each derivative becomes a factor of $s$: $\dot x_i\to sX_ie^{st}$ and $\ddot x_i\to s^2X_ie^{st}$. Cancel $e^{st}$ from every term of the two collected equations of [§8](#section-8). The first becomes $[m_1s^2+(c_1+c_2)s+(k_1+k_2)]X_1-(c_2s+k_2)X_2=U$, and the second becomes $-(c_2s+k_2)X_1+(m_2s^2+c_2s+k_2)X_2=0$. In matrix form:

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

The determinant supplies an unreduced common denominator for this plant's transfer functions:

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

$D(s)$ is a fourth-degree polynomial for the four-state model. Its roots are the natural rates at which the plant can move with $u=0$. They are also poles of an input-output transfer function when no common numerator factor cancels them. We assume no such cancellation in the examples below; moving a sensor never changes the internal dynamics, but it can change which modes remain visible ([§13](#section-13)–[§14](#section-14)).

---

## 10. Collocated output: measure $x_1$ {#section-10}

The actuator acts on $m_1$, and the sensor also measures $x_1$. This is a **collocated** input-output pair: force is applied at the same coordinate whose displacement is measured. Force and displacement are conjugate for virtual work; force and velocity are conjugate for power ([Lecture 2, §2](modeling-and-dynamics-zeroes_student.md#section-2)).

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

The next section derives the mechanical interpretation of this numerator.

---

## 11. Zero dynamics from the collocated two-mass system {#section-11}

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

### The required input from the first equation

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

Zero dynamics are *the internal motion under the input that holds $y\equiv0$*. Both the internal motion and its required input belong to this description; [Lecture 2, §9](modeling-and-dynamics-zeroes_student.md#section-9) gives the state-space form.

![Zero measured displacement while the second mass moves and the actuator cancels its coupling force.](demos/figures/demo5_zero_dynamics.png)

**Numerical example.** The second mass starts with displacement $1\ \mathrm{m}$ and zero velocity. The actuator force has maximum magnitude $8\ \mathrm{N}$. The hidden motion and force have envelopes decaying at $0.02\ \mathrm{s}^{-1}$, reaching about 30% of their initial envelope after 60 seconds. Meanwhile, the computed maximum $|x_1|$ is about $3.2\times10^{-17}$. The measured oscillation rate $3.99997\ \mathrm{rad/s}$ and decay rate $0.02000\ \mathrm{s}^{-1}$ agree with the zero pair $-0.02\pm j3.99995$. These are zero-dynamics rates, rather than the free plant poles.

Here is a physical way to understand a zero.

Use the actuator to hold the measured coordinate $x_1$ exactly at zero.

Does that mean the entire system must be motionless?

No.

The second mass can still move — and in fact it moves exactly as if $m_1$ were bolted to the wall.

The zero dynamics describe the internal motion that can occur while the measured output remains zero, together with the input required to keep it there.

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

For $m_2,c_2,k_2>0$, these zero dynamics are stable (both roots in the LHP), so this example is minimum phase. If $c_2=0$ the zeros sit exactly on the $j\omega$ axis, which is the boundary case — see [§12](#section-12) and [§14](#section-14).

---

## 12. Antiresonance {#section-12}

For the undamped coupling $c_2=0$, the zeros are

$$
s=\pm j\sqrt{\frac{k_2}{m_2}}.
$$

This is the [§4.3](#section-4-3) case, now appearing as a *zero* rather than a pole. At this driving frequency the first mass can remain stationary even while the second mass oscillates: the second mass acts as a tuned absorber, and the force it returns through $k_2$ exactly cancels the applied force.

This is an **antiresonance**, and it is the operating principle of the **dynamic vibration absorber** — and closely related to the tuned mass damper. The distinction is that the undamped absorber here produces an *exact* notch at a single frequency, whereas a practical tuned mass damper is deliberately damped, trading that exact zero for broader but shallower attenuation.

![Exact undamped antiresonance and the corresponding mass motions.](demos/figures/demo6_antiresonance.png)

**Numerical example.** With $c_2=0$ and $\sqrt{k_2/m_2}=4\ \mathrm{rad/s}$, the steady-state gain $|X_1/U|$ is exactly zero. The second mass and spring still store energy; the example has mean stored energy $0.0625\ \mathrm{J}$. A finite-time simulation can retain a small $x_1$ transient (about $4\times10^{-5}$ here), because the plant's natural transient decays only as $e^{-0.027t}$. That residual does not change the exact steady-state null.

### Check your understanding

If the measured displacement $x_1$ is zero, is the mechanical energy necessarily zero?

No.

The second mass and coupling spring can contain kinetic and potential energy even while $x_1=0$.

Distinguish between:

- measured output,
- internal state,
- internal energy.

A single sensor reading gives one projection of the state, not the complete instantaneous state.

---

## 13. Move the sensor: measure $x_2$ {#section-13}

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

The poles are unchanged, because the physical internal dynamics are unchanged. (This holds provided no pole-zero cancellation occurs; if a numerator root coincided with a denominator root, that mode would become invisible from this output, and the transfer function would no longer tell the whole story. See [§14](#section-14) and [Lecture 2, §11](modeling-and-dynamics-zeroes_student.md#section-11).)

But the numerator has changed. If $c_2>0$, the single finite zero is

$$
\boxed{
s=-\frac{k_2}{c_2}
}
$$

and if $c_2=0$, there is no finite zero at all — the numerator is the constant $k_2$.

We did not change the masses.

We did not change the springs.

We did not change the dampers.

We only changed what we chose to measure.

The poles remained the same.

The zeros changed completely — from a resonant pair to a single real zero, or to none at all.

![Moving the sensor changes the zeros and frequency response while preserving the poles in this example.](demos/figures/demo4_sensor_moves_zeros.png)

**Damped numerical example.** Both outputs show two flexible resonances; only the collocated output has a pronounced notch between them. With $c_2=0.02$, the notch is finite: $|G_1(j4)|\approx1.249\times10^{-3}$. Pole magnitudes near $3.03$ and $5.90\ \mathrm{rad/s}$ surround a zero magnitude near $4.00\ \mathrm{s}^{-1}$. With damping, these magnitudes need not equal the exact frequencies of the response extrema. The two computed pole sets are identical.

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

Lecture 2 develops the control consequences of this distinction.

---

## 14. Poles and zeros: definitions {#section-14}

Suppose

$$
G(s)=\frac{Y}{U}
=
\frac{N(s)}{D(s)},
$$

where $N$ and $D$ are **coprime** — any common factors have already been cancelled. A canceled factor can hide an internal mode, as discussed in [Lecture 2, §11](modeling-and-dynamics-zeroes_student.md#section-11).

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

Within the particular-response framework of [§5](#section-5), drive the system with

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

What *is* true is the stronger statement [§11](#section-11) already gave us and [Lecture 2, §9](modeling-and-dynamics-zeroes_student.md#section-9) will formalize: there is an input $u_0e^{zt}$ and a matching initial state $\mathbf x(0)=\mathbf x_0$ such that $\mathbf x(t)=\mathbf x_0e^{zt}$ and the output is identically zero. For a conjugate pair of zeros, combine conjugate trajectories to obtain real motion. Exact blocking requires a compatible initial state.

At a transfer-function zero, the $e^{zt}$ component of the forced response is blocked at the chosen output. The system may nevertheless be moving internally — and the zero dynamics tell us what that hidden motion is.

### Minimum phase

**Convention for this lecture:** a proper real-rational continuous-time SISO transfer function is called **minimum phase** when its poles and finite zeros are all strictly in the LHP. We discuss pole stability and finite-zero locations separately whenever the plant is not asymptotically stable.

- A RHP zero is a **nonminimum-phase zero**, whether or not the plant has stable poles.
- A zero on the $j\omega$ axis is a boundary case and fails the strict minimum-phase condition.
- “No finite zeros” alone does not establish plant stability.

Some controls texts use “minimum phase” to describe stable zero dynamics independently of plant poles. Naming our convention avoids switching meanings between the stable platform and the quadrotor examples.

### Why the name "minimum phase"?

Compare stable causal rational systems with the same magnitude response and the same nonzero DC gain. The minimum-phase one has the least phase lag. For a real $z>0$, reflecting a zero from $-z$ to $+z$ while preserving DC gain multiplies in
$$A_{\mathrm{ap}}(s)=\frac{z-s}{z+s},\qquad |A_{\mathrm{ap}}(j\omega)|=1.$$
Its phase is $-2\arctan(\omega/z)$: it starts at zero and approaches $-180^\circ$ as frequency increases.

The factor is what you get by dividing the reflected plant by the original. With $G_+(s)=(z-s)R(s)$ and $G_-(s)=(z+s)R(s)$ for the same $R(s)$, both have the same DC gain $zR(0)$, and $G_+=A_{\mathrm{ap}}G_-$. At $s=j\omega$, the numerator $z-j\omega$ and denominator $z+j\omega$ are conjugates, so they have equal magnitude, which gives $|A_{\mathrm{ap}}|=1$. Their angles are $-\arctan(\omega/z)$ and $+\arctan(\omega/z)$, so the quotient's phase is $-\arctan(\omega/z)-\arctan(\omega/z)=-2\arctan(\omega/z)$.

That extra phase lag is one way to see the feedback difficulty. [Lecture 2, §11](modeling-and-dynamics-zeroes_student.md#section-11) states the associated interpolation constraint.

---

## 15. Transition to the Laplace transform {#section-15}

The common observation behind the derivations is:

$$
\frac{d}{dt}e^{st}=se^{st},
\qquad
\frac{d^2}{dt^2}e^{st}=s^2e^{st}.
$$

Every time we tried an exponential, differentiation became multiplication.

That converted differential equations into algebraic equations, and it worked for the thermal body, the spring-mass-damper, the pendulum, and a four-state flexible structure.

The exponential gain calculation assumes an exponential input, $Fe^{st}$. Other inputs include steps, pulses, and ramps.

So here is the natural question:

**Can we represent a general signal as a combination of exponentials, so that this property survives?**

That is exactly what the Laplace transform does.

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

### Convergence and reconstruction

**1. Where does it converge?** For a piecewise-continuous signal of exponential order — $|x(t)|\le Ke^{at}$ for sufficiently large $t$ — the integral converges when $\Re(s)>a$. This is a sufficient condition for a right half-plane inside the *region of convergence*. The weight $e^{-\sigma t}$ must suppress the signal's growth: $e^{2t}$ has a transform for $\sigma>2$. Not every signal has a transform; $e^{t^2}$ grows too fast for any finite $\sigma$. The real part of $s$ still controls exponential growth and decay.

**2. Why does this answer the question we asked?** Because the transform is invertible, and the inversion formula says explicitly that the signal *is* a superposition of exponentials:

$$
x(t)=\frac{1}{2\pi j}\int_{\sigma_0-j\infty}^{\sigma_0+j\infty}X(s)\,e^{st}\,ds .
$$

Choose $\sigma_0$ inside the region of convergence: the integration runs along the vertical line $s=\sigma_0+j\omega$. For the regular signals considered here, this recovers the signal at continuity points. The integrand explains the connection to exponential testing:

The integral contains $e^{st}$. Along this chosen vertical line, $X(s)$ supplies the weights for a continuous superposition of exponentials. These are test rates, not just the plant's discrete natural rates.

Differentiating each exponential multiplies it by its rate. For the unilateral transform, a boundary term also carries the initial condition; let's derive it.

The same $s$ that described physical exponential modes is now the coordinate of the transformed signal.

---

## 16. Derivative property of the Laplace transform {#section-16}

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

For this derivation, take $x$ continuous with a piecewise-continuous derivative and the exponential bound from [§15](#section-15). At jumps, the same identity uses distributional derivatives. Integrate by parts. Let

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

Using the $0^-$ convention from [§15](#section-15), the rule

$$
\frac{d}{dt}
\leftrightarrow
s
$$

that we have used since [§1](#section-1) survives with initial-condition terms added. Those terms account for stored initial state and vanish when that state is zero. The response to a switched input can still contain natural-mode exponentials even when it starts from rest; [§17](#section-17) makes that distinction concrete.

---

## 17. Revisit the spring-mass-damper with forcing {#section-17}

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

The initial conditions enter the algebra directly. The exponential method can also enforce them by adding homogeneous solutions, as in [§2](#section-2) and [§4](#section-4); the gain calculation alone does not.

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

Compare this result with [§5](#section-5).

There, $X$ and $F$ were complex numbers — the amplitude of an assumed exponential input and the amplitude of the exponential response.

Here, $X(s)$ and $F(s)$ are transforms of signals such as steps and pulses, provided the transforms exist.

And we got the same function of $s$.

That is the sense in which the Laplace transform is not a new idea. It is the $e^{st}$ substitution, extended to signals that are not exponentials, with initial conditions carried along for free.

The polynomial $ms^2+cs+k$ has now appeared three times: as the characteristic equation of free motion, as the denominator of the exponential gain, and as the denominator of the transfer function. Its roots are the poles.

That is not a coincidence. It is the whole point.

### 17.1 A complete payoff: switch on the heater {#section-17-1}

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

**Check:**
- $x(0)=Rq_0(1-1)=0$.
- $x(\infty)=Rq_0$, where the heater input balances the loss through $R$: $q_0=x/R$.
- $\dot x(0^+)=Rq_0/\tau=q_0/C$. The energy balance requires exactly this, because at $t=0^+$ nothing has yet leaked through $R$, so $C\dot x=q_0$.

After one time constant, $1-e^{-1}=0.632$, so the rise is about 63% complete.

We transformed a switched input, solved an algebraic equation, and recovered the time response. The decaying exponential is present even though the initial state was zero: it makes the complete response start at the required temperature.

**Forcing at the natural rate:** At the natural test rate, $q_{\mathrm{in}}=q_0e^{-t/\tau}$, the same-exponential gain is undefined. The particular solution is instead $(q_0/C)t e^{-t/\tau}$. A pole marks failure of that trial form, not an infinite temperature.

To verify, substitute $x_p=(q_0/C)te^{-t/\tau}$. Then $C\dot x_p=q_0e^{-t/\tau}-(q_0/\tau)te^{-t/\tau}$, and $x_p/R=(q_0/RC)te^{-t/\tau}=(q_0/\tau)te^{-t/\tau}$. The $te^{-t/\tau}$ terms cancel, leaving $C\dot x_p+x_p/R=q_0e^{-t/\tau}$ ✓. This is the same "multiply by $t$" repair as the repeated root in [§4.2](#section-4-2).

---

## 18. Revisit the pendulum in the Laplace domain {#section-18}

Apply the derivative rule to the two linearized models from [§6](#section-6).

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

Same hardware. Same transfer-function *structure*. One sign change in the constant term — and per [§6.2](#section-6-2), one pole crosses into the right half plane.

$$
\boxed{
\text{the operating point changes the effective stiffness, and therefore changes the poles}
}
$$

On the $s$-plane ([§7](#section-7)), the upright linearization has one positive real pole, corresponding to a growing mode.

---

## 19. Big-picture summary {#section-19}

The main chain of ideas is:

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
\text{poles / visible natural rates}
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

## 20. Connecting the examples {#section-20}

We began with a hot object cooling toward room temperature.

That gave us a real negative value of $s$ — and when we added a heater, that same value turned out to be where the transfer function's denominator vanished.

We moved to a spring-mass-damper and discovered complex values of $s$, which naturally represented damping and oscillation, and which cancelled in conjugate pairs to give us back real motion.

We forced that system and found that the characteristic polynomial had become the denominator of a transfer function. The poles were not a definition we imposed. They specified natural exponential rates visible in the input-output response.

We turned the same mechanical idea into a pendulum and saw how linearization around different equilibria moves a pole across the imaginary axis.

We added another mass and discovered that a system can move internally while the measured output is zero — and that holding the output at zero costs a specific input.

That gave us a physical interpretation of zeros and zero dynamics.

Then we saw that changing where we measure can dramatically change the zeros while leaving the internal dynamics unchanged. In our examples, the visible poles stayed the same too.

Finally, the Laplace transform let us switch on a heater and calculate its whole response from rest.

So when we now write

$$X(s)=\int_{0^-}^{\infty} x(t)e^{-st}\,dt,$$

the variable $s$ is not a mysterious new symbol.

It is the same $s$ that appeared naturally when we asked:

**What exponential motions are compatible with the physics?**

---

## 21. Quick reference {#section-21}

For exponential trial functions (the derivative substitutions below apply to $e^{st}$; Laplace transforms also include initial-condition terms):

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

$$
\boxed{
G(s)=\frac{N(s)}{D(s)}
}
$$

Here $N$ and $D$ are coprime.

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

$$
\boxed{
X(s)
=
\int_{0^-}^{\infty}
x(t)e^{-st}\,dt
}
$$

**The Laplace transform works because exponentials are the natural language of linear differential equations.**

---

## Review questions and answers

Use these questions to check both the algebra and its physical meaning.

### Thermal system ([§2](#section-2))

**1. Why must the thermal pole be real in this simple one-state model?**

**Answer:** The characteristic equation $Cs+1/R=0$ is linear with real coefficients, so its single root is real: $s=-1/(RC)$. There is no second independent state to support an oscillatory conjugate pair.

**2. What physical changes move the pole closer to the origin?**

**Answer:** Increasing $R$ or $C$ increases $\tau=RC$ and moves $s=-1/\tau$ toward the origin along the negative real axis.

**3. Why does a larger thermal resistance slow the system?**

**Answer:** A larger $R$ reduces heat loss for a given temperature difference. The energy balance therefore changes the temperature more slowly, and $\tau$ increases.

**4. The transfer function $R/(\tau s+1)$ blows up at $s=-1/\tau$. What is physically happening at that value of $s$?**

**Answer:** The chosen forcing rate coincides with the natural rate, so a constant multiple of the same exponential cannot be a particular solution. For $q_{\mathrm{in}}=q_0e^{-t/\tau}$, the particular solution is $(q_0/C)t e^{-t/\tau}$. The temperature does not become infinite.

### Spring-mass-damper ([§3](#section-3)–[§5](#section-5))

**1. What determines whether the roots are real or complex?**

**Answer:** The discriminant $c^2-4mk$ determines the root type: positive gives distinct real roots; zero gives a repeated real root; negative gives a conjugate pair. At $c=0$ that pair is purely imaginary.

**2. What does the real part of $s$ do? The imaginary part?**

**Answer:** In $e^{(\sigma+j\omega)t}=e^{\sigma t}(\cos\omega t+j\sin\omega t)$, $\sigma$ sets growth or decay and $\omega$ sets the oscillation rate.

**3. If the displacement is a real number, where did the $j$ go?**

**Answer:** For real coefficients and real initial conditions, conjugate roots have conjugate amplitudes. Their imaginary parts cancel, leaving $e^{\sigma t}(B\cos\omega t+C\sin\omega t)$ with real $B,C$.

**4. What would a pole in the RHP mean physically?**

**Answer:** A right-half-plane pole has positive real part, so its natural mode grows exponentially when excited. This represents an unstable mode, even with no applied input.

**5. We found $G(s)=1/(ms^2+cs+k)$ by assuming a *particular* solution. What happened to the free modes?**

**Answer:** They belong to the homogeneous part of the complete solution. Their amplitudes enforce the initial conditions after the particular solution is included; they can be nonzero even when the system starts from rest.

**6. Why is the denominator of $G(s)$ the same polynomial as the characteristic equation? (Answer it with the "no input" argument, not by inspection.)**

**Answer:** With $F=0$, the amplitude equation $(ms^2+cs+k)X=F$ permits nonzero $X$ exactly when the polynomial vanishes. Solving the same equation for $X/F$ puts that polynomial in the denominator. In this model there is no numerator factor to cancel a root.

### Pendulum and the $s$-plane ([§6](#section-6)–[§7](#section-7))

**1. Why does the same pendulum have different linear models around downward and upright equilibria?**

**Answer:** The local slope of gravity torque depends on the equilibrium. Near downward, $\sin\theta\approx\theta$; near upright, writing $\theta=\pi+\phi$ gives $\sin(\pi+\phi)\approx-\phi$.

**2. What changed sign, and why does that sign change cause instability?**

**Answer:** The effective stiffness changes from $+m_pgl$ to $-m_pgl$. The upright characteristic equation has root product $-m_pgl/J<0$, giving one positive real root and one negative real root. The positive root produces exponential growth.

**3. Locate both pendulum models' poles on the $s$-plane. What physically happened between the two pictures?**

**Answer:** With positive damping, both downward poles lie in the LHP; with zero damping they are $\pm j\sqrt{m_pgl/J}$. Upright has one negative and one positive real pole for any nonnegative damping. Changing the equilibrium changes gravity from restoring to destabilizing.

**4. What kind of motion corresponds to a pole exactly at the origin?**

**Answer:** A simple zero rate gives a constant mode, $e^{0t}=1$. Repeated scalar roots can add polynomial factors: a free mass has $x=x_0+v_0t$. In a state model, repeated eigenvalues produce such factors only when nontrivial Jordan blocks are present.

### Two-mass system ([§8](#section-8)–[§13](#section-13))

**1. If $x_1=0$, must $x_2=0$?**

**Answer:** No. Holding $x_1\equiv0$ leaves $m_2\ddot x_2+c_2\dot x_2+k_2x_2=0$, which allows nonzero motion of $m_2$.

**2. Can internal energy exist when the measured output is zero?**

**Answer:** Yes. With $x_1=0$, the second mass and coupling spring can store $E=\tfrac12m_2\dot x_2^2+\tfrac12k_2x_2^2$. If $c_2>0$, this energy decays through damping.

**3. Holding $x_1\equiv 0$ requires an input. What is that input doing, physically?**

**Answer:** The input $u=-(c_2\dot x_2+k_2x_2)$ cancels the coupling force that would otherwise move $m_1$. It can be nonzero even though the measured displacement is identically zero.

**4. Why did moving the sensor change the zeros but not the poles?**

**Answer:** The dynamic-stiffness matrix and its determinant $D(s)$ are unchanged. Reading a different coordinate changes the numerator. With no cancellation, the transfer poles remain the same; a changed sensor can also hide a mode through cancellation in a more general case.

**5. The collocated numerator is the characteristic polynomial of the $m_2$ subsystem when $x_1$ is pinned. Would you expect that pattern to generalize?**

**Answer:** For the ideal collocated mechanical model, yes: constraining the measured coordinate gives the zero dynamics of the remaining structure. Here it is $m_1$ that is pinned, leaving the $m_2$ subsystem. Passive-model and cancellation assumptions matter; Lecture 2 develops the flexible-structure version.

### Laplace transform ([§15](#section-15)–[§18](#section-18))

**1. Why do exponentials make differential equations easy?**

**Answer:** Every derivative of $e^{st}$ is the same exponential multiplied by a power of $s$. A linear constant-coefficient differential equation therefore reduces to a polynomial or matrix equation in $s$.

**2. What is the precise difference between $\dot x\leftrightarrow sx$ and $\mathcal L\{\dot x\}=sX-x(0^-)$?**

**Answer:** The substitution $\dot x=sx$ is exact for a single exponential trial function. The transform identity applies to broader signals and includes the boundary contribution $-x(0^-)$ from integration by parts.

**3. When do characteristic roots appear as transfer-function poles, and what can a cancellation hide?**

**Answer:** A characteristic rate appears as a transfer pole when the input excites its mode and the output observes it. A common numerator-denominator factor can cancel, hiding internal dynamics from that channel without removing them from the system.

**4. What does the region of convergence have to do with $\sigma$?**

**Answer:** The real part $\sigma$ controls the exponential weight $e^{-\sigma t}$. If $|x(t)|\le Ke^{at}$ for sufficiently large $t$, then $\sigma>a$ is sufficient for convergence. The inversion line must lie inside the region of convergence.

**5. Looking at the inversion integral, in what sense is the Laplace transform "the same idea" as substituting $e^{st}$?**

**Answer:** The inversion integral reconstructs $x(t)$ from a continuous superposition of $e^{st}$ along a vertical line. Each exponential retains the derivative-to-multiplication property; the unilateral derivative rule also accounts for initial state.

**6. The heater starts from zero temperature deviation. Why does its step response still contain $e^{-t/\tau}$?**

**Answer:** The complete zero-state response is $Rq_0(1-e^{-t/\tau})$. Its decaying term makes $x(0)=0$ while allowing $x(\infty)=Rq_0$. A zero-state response can contain natural-mode transients; it is different from a particular response alone.

---

## Optional computational examples

The accompanying Python examples recompute the numerical results and generate figures. From the directory containing these notes:

```sh
cd demos
uv run python demo1_splane_modes.py
```

Use `--show` for an interactive plot or `--no-save` for terminal output only. `uv run python run_all.py` regenerates all eight examples. Numerical residuals depend on the solver and environment.

| Script | Topic |
|---|---|
| [demo1_splane_modes.py](demos/demo1_splane_modes.py) | Pole locations and time responses |
| [demo2_damping_pole_locus.py](demos/demo2_damping_pole_locus.py) | Damping and the pole locus |
| [demo3_real_from_complex.py](demos/demo3_real_from_complex.py) | Real motion from conjugate modes |
| [demo4_sensor_moves_zeros.py](demos/demo4_sensor_moves_zeros.py) | Changing the measured coordinate |
| [demo5_zero_dynamics.py](demos/demo5_zero_dynamics.py) | Motion with zero measured output |
| [demo6_antiresonance.py](demos/demo6_antiresonance.py) | Exact undamped antiresonance |

`twomass.py` supplies the shared physical model for examples 4–6. Example 4 has a damped, finite notch; example 6 sets the coupling damping to zero for an exact null. Example 5 checks both the frequency and decay rate of the zero dynamics.
