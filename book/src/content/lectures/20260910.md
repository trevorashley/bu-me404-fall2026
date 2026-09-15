# Lecture 2: Zeros, Geometry, and Noncollocation

**Student lecture notes — internal motion and control limitations**

This lecture builds on [Lecture 1: From Physical Models to the Laplace Transform](lecture_0.0.8_student_lecture_1.md). The central idea is that moving a sensor leaves the internal dynamics fixed while changing the zeros. Cancellations can also change which internal modes appear as transfer-function poles.

**Prerequisites:** Exponential modes, transfer functions, poles, and the two-mass zero-dynamics example from Lecture 1. The state-space section is an optional extension.

## Learning objectives

After studying this lecture, you should be able to:

1. Determine, for a given input-output geometry, whether a mechanical system has a right-half-plane zero.
2. Explain why right-half-plane zeros are associated with nonminimum-phase behavior and with bandwidth limits.
3. Distinguish an unstable pole from a right-half-plane zero, and give an example of a stable, nonminimum-phase plant.
4. Distinguish underactuation from nonminimum-phase behavior.
5. Derive zero dynamics by imposing zero measured output and finding the required input.
6. Explain when damping can move zeros between half planes and when it cannot.

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
| $A$ | complex amplitude in $x = Ae^{st}$; local coefficient/matrix uses in [§4](#section-4)/[§9](#section-9) are defined there |
| $\mathcal A(s)$ | Laplace transform of a beam angle $\alpha(t)$ |

Physical masses, inertias, capacitances, resistances, and restoring stiffnesses are positive unless stated otherwise; damping coefficients are nonnegative. Amplitudes such as $X$ and $U$ are numbers. Transforms such as $X(s)$ and $U(s)$ are introduced in [Lecture 1, §15](lecture_0.0.8_student_lecture_1.md#section-15).

**Terminology:** LHP and RHP mean the left and right half planes of the complex $s$-plane. CM means center of mass. A configuration degree of freedom is an independent position or angle; a second-order coordinate contributes two states. We call a proper real-rational continuous-time SISO transfer function minimum phase when its poles and finite zeros are all strictly in the LHP. SISO means single input, single output; LTI means linear and time invariant.

---

## 1. Ball-and-beam: underactuation and internal coordinates {#section-1}

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

### 1.1 Ball dynamics {#section-1-1}

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

### 1.2 What is the input, really? {#section-1-2}

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

The neglected gravitational torque from the ball is proportional to $mgx$ near the centered equilibrium and is first order. Omitting it is an additional modeling assumption, not a consequence of small-angle linearization. This simplified cascade gives

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

**This second version is the underactuated one.** Count configuration coordinates rather than states — a single mass pushed by a single force has two states and one input, and it is fully actuated. Underactuation compares actuators to **configuration degrees of freedom**:

$$
\boxed{
2\ \text{configuration DOFs }(x,\alpha),
\quad
1\ \text{independent actuator }(M)
\ \Rightarrow\
\text{underactuated}
}
$$

The four states arise merely because both coordinates obey second-order equations. The actuator reaches the ball coordinate $x$ only through the beam angle $\alpha$.

The angle-input and torque-input models are distinct. The underactuated label applies to the torque-input model with two configuration degrees of freedom.

### What the example establishes

The simplified ball-and-beam models used here do **not** produce a finite RHP zero. Its numerator is a constant.

The models illustrate that:

- the actuator acts through an intermediate coordinate,
- the system is underactuated (in the torque-input version),
- multiple state variables are needed,
- one instantaneous position measurement does not specify all the state variables.

These models connect transfer behavior to internal states and disprove the claim that underactuation requires a RHP zero. The quadrotor in [§5](#section-5) provides another example. The integrators still prevent asymptotic stability.

---

## 2. Flexible structures and noncollocation {#section-2}

The two-mass system of [Lecture 1, §8](lecture_0.0.8_student_lecture_1.md#section-8) is a lumped model of a flexible structure. For a genuine flexible beam, the displacement field expands in modes:

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

For distinct participating undamped frequencies with positive modal coefficients, the poles and zeros **interlace along the $j\omega$ axis**: between adjacent positive-frequency resonances sits exactly one antiresonance. These are the natural frequencies of the structure constrained at the measured coordinate — the [Lecture 1, §11](lecture_0.0.8_student_lecture_1.md#section-11) result again.

For this ideal passive mechanical model, collocation excludes finite RHP zeros. Undamped zeros lie on the axis; they do not satisfy [Lecture 1, §14](lecture_0.0.8_student_lecture_1.md#section-14)'s strict minimum-phase convention. If damping makes the constrained zero dynamics asymptotically stable, its zeros move strictly into the LHP. A stable plant with those LHP zeros is minimum phase. Under light damping, the resonance/notch ordering remains a useful picture, but exact interlacing is the undamped result.

With the usual positive force/displacement sign convention, the frequency-response phase lies between $-180^\circ$ and $0^\circ$ wherever the response is nonzero and finite.

### Two collocation results, not one

The two results concern different measured outputs:

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

Collocation provides these structural guarantees under the stated passive-model assumptions.

### The noncollocated case

For $x_a\neq x_s$, the product

$$
\phi_i(x_s)\phi_i(x_a)
$$

may change sign from one mode to another, because the sensor may sit on the opposite side of a mode's node line from the actuator. Different modes then subtract at the measured output rather than adding.

The interlacing guarantee is lost. Zeros are free to move off the $j\omega$ axis, and for some actuator/sensor geometries they land in the right half plane.

Noncollocation removes the interlacing guarantee; it does not by itself require a RHP zero.

---

## 3. Hard-disk read head: a real engineering interpretation {#section-3}

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

which is precisely [Lecture 1, §6](lecture_0.0.8_student_lecture_1.md#section-6) $\rightarrow$ [Lecture 1, §8](lecture_0.0.8_student_lecture_1.md#section-8) $\rightarrow$ [§2](#section-2).

The location of zeros depends on the actuator and sensor geometry; a RHP zero is possible but is not required:

$$
\boxed{
\text{remote sensing + flexible modes}
\Rightarrow
\text{zeros become strongly geometry dependent}
}
$$

This example connects resonances, antiresonances, collocation, noncollocation, and bandwidth limitations. Flexible modes and the resulting servo-bandwidth limits are one of the important constraints on achievable track-following accuracy, and hence on track density — alongside disturbances, spindle runout, sensing noise, and media mechanics.

---

## 4. A stable, nonminimum-phase rigid body {#section-4}

A right-half-plane zero can arise without any structural flexibility at all. The example demonstrates the distinction in [§10](#section-10): **stable poles do not imply minimum phase.**

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

Over the common denominator:

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

This is a sufficient condition for a RHP zero, not a necessary one: outside this interval there can be a RHP conjugate pair or even two positive real zeros. The full classification appears below. Because the plant poles are in the LHP, a positive numerator root cannot cancel.

**1. Damping cannot remove the RHP zero when $AC<0$, but it moves both zeros.** Damping enters $B$, and hence the root sum $-B/A$, while the negative product $C/A$ stays fixed. For every finite choice of damping there is still one positive and one negative root. This conclusion applies to the opposite-sign-root case; it is not a rule for every sensor geometry.

$$
\boxed{AC<0\ \Rightarrow\ \text{one RHP zero for every damping distribution}}
$$

Consider the $AC<0$ case with $ab=0.15$ and the numbers below. The left family has $c_\theta=0.1c_x$; the right family has $c_\theta=0.25c_x$ and includes the worked case:

| $c_x$ | $c_\theta$ | zeros | $c_x$ | $c_\theta$ | zeros |
|---:|---:|---|---:|---:|---|
| $0$ | $0$ | $\pm10.00$ | $0$ | $0$ | $\pm10.00$ |
| $2$ | $0.2$ | $+9.05,\ -11.05$ | $2$ | $0.5$ | $+12.20,\ -8.20$ |
| $6$ | $0.6$ | $+7.44,\ -13.44$ | $6$ | $1.5$ | $+17.66,\ -5.66$ |
| $20$ | $2.0$ | $+4.14,\ -24.14$ | $20$ | $5.0$ | $+42.36,\ -2.36$ |

The RHP zero moves a long way — and which direction it moves depends on the sign of $B$, i.e. on how the damping is distributed between the two channels. In the left-hand family it drifts *toward the origin*, which makes the plant harder to control (see [§11](#section-11)). For this geometry, damping does not remove the RHP zero and can move it closer to the origin.

**Numerical check.** For this $AC<0$ geometry, $C/A=-100$ throughout the damping sweep, so the zeros retain opposite signs. Extending to $c_x=60$ gives RHP zeros near $+1.6$ and $+121$ for the two families. For positive damping in these families, initial acceleration and final displacement have opposite signs, as derived below.

**2. If $ab<0$** — sensor and actuator on the *same* side of the center of mass — then $A>0$, $B>0$ and $C>0$, so both zeros lie in the open **left** half plane. (For the worked numbers below with $ab=-0.15$: $-1.60\pm j11.72$.) Only in the *undamped* case $B=0$ do those zeros sit exactly on the $j\omega$ axis.

Note that "same side" is weaker than collocated: the two can sit at different points and still share a sign. True collocation is the special case $b=-a$, meaning the sensor is *at* the actuator, which gives $ab=-a^2<0$. So collocation lives inside this family, and the favorable sign structure of [§2](#section-2) turns out to extend to a strictly larger set of geometries than collocation alone. Collocation is sufficient for this favorable sign structure, but other geometries can have it too.

**3. If $ab=J/m$ exactly**, then $A=0$. When $B\ne0$, the numerator is linear, with a root at $-C/B$, and the relative degree is **3**. If also $B=0$ but $C\ne0$, the relative degree is **4**. Here $B=0$ means $c_\theta=(J/m)c_x$, the mass-proportional damping condition for these coordinates; the undamped limit satisfies it too. If $A=B=C=0$, the entire output transfer function is zero and no finite relative degree is assigned. As usual, common factors must be canceled when identifying finite transfer zeros.

### A worked numerical case

Take $m=1$, $J=0.1$, $k_x=100$, $k_\theta=20$, $c_x=2$, $c_\theta=0.5$, with $a=0.3$ and $b=0.5$, so $ab=0.15$.

Check the condition: $J/m=0.1$ and $k_\theta/k_x=0.2$, and indeed $0.1<0.15<0.2$.

- **Poles:** $s^2+2s+100=0 \Rightarrow s=-1\pm j9.95$, and $0.1s^2+0.5s+20=0 \Rightarrow s=-2.5\pm j13.92$. All four are stable.
- **Numerator:** $A=-0.05$, $B=0.2$, $C=5$, so $-0.05s^2+0.2s+5=0$, i.e. $s^2-4s-100=0$, giving $s=-8.20$ and $\boxed{s=+12.20}$.

This is a stable plant with a right-half-plane zero, illustrating [§10](#section-10).

(These values are not mass-proportionally damped: $c_\theta/c_x=0.25\ne J/m=0.1$. Thus, if we move the sensor to $ab=J/m$, item 3 gives relative degree 3.)

### Physical interpretation

The actuator causes both translation and rotation. At the measured point, those two effects **subtract**.

Both translation and rotation have relative degree **two**. For a force step $u_0>0$ from rest, compare their acceleration contributions and their static displacements:

$$
\ddot y(0^+)=u_0\left(\frac1m-\frac{ab}{J}\right)=\frac{u_0A}{mJ},
\qquad
y(\infty)=u_0\left(\frac1{k_x}-\frac{ab}{k_\theta}\right)=\frac{u_0C}{k_xk_\theta}.
$$

When $AC<0$, initial acceleration and final displacement have opposite signs. In the worked case, $J/m<ab<k_\theta/k_x$: rotation wins initially ($A=-0.05$), translation wins at DC ($C=5$). The reverse ordering, $k_\theta/k_x<ab<J/m$, also gives inverse response, with translation winning initially and rotation at DC. The distinction is acceleration gain versus static gain, not relative degree.

This wrong-way motion is called an **inverse response**.

Important caution:

Wrong-way initial motion is a common physical manifestation of a RHP zero, but it should not be used as the formal definition of one. The definition is in [Lecture 1, §14](lecture_0.0.8_student_lecture_1.md#section-14) and [§8](#section-8).

### Full quadratic classification

For $A,C\ne0$, the full classification is:

| Condition | Roots of $As^2+Bs+C$ |
|---|---|
| $C/A<0$ | One positive and one negative real root, for every $B$ |
| $C/A>0$, $B/A>0$ | Both strictly in the LHP |
| $C/A>0$, $B/A<0$ | Both strictly in the RHP; real if $B^2-4AC\ge0$, otherwise conjugate |
| $C/A>0$, $B=0$ | A purely imaginary conjugate pair |

When $AC>0$, changing the damping distribution can change the half plane of the zeros. For the same $m,J,k_x,k_\theta$ as the worked example, but $ab=0.05$ and $c_x=2$:

$$
\begin{array}{c|c|c}
c_\theta & N(s) & \text{zeros}\\ \hline
0.05 & 0.05s^2-0.05s+15 & 0.5\pm j17.3133\\
0.20 & 0.05s^2+0.10s+15 & -1\pm j17.2916
\end{array}
$$

The plant poles remain in the LHP in both cases. Damping alone removes the RHP pair. Two **real** positive zeros are also possible outside the interval: with $ab=0.05$, $c_x=100$, $c_\theta=0.05$, the numerator is $0.05s^2-4.95s+15$, with roots approximately $3.12921$ and $95.87079$.

For positive $c_x$ and nonzero $A,B,C$, all three coefficients share a sign exactly when $ab$ lies strictly below all three ratios $J/m$, $k_\theta/k_x$, $c_\theta/c_x$, or strictly above all three. This is the generic LHP-zero condition. Handle boundaries separately: $A=0$ is item 3 above; $C=0$ gives a numerator factor $s$ and requires the usual cancellation check. Thus the “same side of three ratios” rule is not a substitute for checking degree reductions.

---

## 5. Quadrotor: underactuation does not require a RHP zero {#section-5}

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

$$
\boxed{
\text{underactuated}
\not\Rightarrow
\text{a RHP zero}
}
$$

**Stability:** Four poles at the origin and relative degree 4 make this a demanding control problem. The free response can grow polynomially; the plant is neither asymptotically stable nor BIBO stable. “No finite zeros” describes the zeros only, and does not make this plant minimum phase under [Lecture 1, §14](lecture_0.0.8_student_lecture_1.md#section-14)'s convention.

---

## 6. Quadrotor with an offset measurement point {#section-6}

Now measure the horizontal position of a point offset vertically from the center of mass — a downward-facing camera used for visual servoing, a landing skid, or a sensor mast.

Note that these are all **rigidly attached** points. The relation $y=x-h\theta$ describes a point bolted to the airframe. A cable-suspended payload is a genuinely different problem: the swing angle is an extra generalized coordinate with its own dynamics, and this model does not describe it.

### Which way does the offset point move?

With the convention of [§5](#section-5) — positive $\theta$ tilts the thrust axis toward $+x$ — a body-fixed point at height $+h$ **above** the center of mass has horizontal position $x+h\theta$. It swings the same way the vehicle accelerates.

A point a distance $h$ **below** the center of mass has horizontal position

$$
\boxed{
y=x-h\theta
}
$$

It swings *opposite* to the direction the vehicle is about to accelerate. That is the case that produces the RHP zero.

### The transfer function

From [§5](#section-5),

$$
\frac{X}{M}
=
\frac{g}{Js^4},
\qquad
\frac{\Theta}{M}
=
\frac{1}{Js^2},
$$

so

$$
\frac{Y}{M}
=
\frac{g}{Js^4}
-
\frac{h}{Js^2}
$$

and therefore

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

This is a nonminimum-phase zero. Summarizing the geometry:

| Measurement point | Output | Zeros | Character |
|---|---|---|---|
| At the center of mass | $y=x$ | none (finite) | no finite zeros; four integrators |
| A distance $h$ **above** the CM | $y=x+h\theta$ | $\pm j\sqrt{g/h}$ | on the $j\omega$ axis |
| A distance $h$ **below** the CM | $y=x-h\theta$ | $\pm\sqrt{g/h}$ | **RHP zero** |

### Where that zero comes from: derive the zero dynamics directly

The zero can also be found directly from the equations of motion.

This is the exact same trick we did with the second mass. Set the measured output to zero, and ask what the rest of the machine is still free to do.

In [Lecture 1, §11](lecture_0.0.8_student_lecture_1.md#section-11), holding $x_1=0$ left $m_2$ free to oscillate. Here, holding the camera fixed leaves the airframe free to pitch.

**Numerical example and model scope.** For $h=0.2\ \mathrm{m}$, the growing zero-dynamics rate is $\sqrt{g/h}=7.00357\ \mathrm{s}^{-1}$. With $\dot\theta(0)=0$, the matched zero-output motion is $\theta(t)=\theta(0)\cosh(\sqrt{g/h}\,t)$. A torque-step response changes sign at $t=\sqrt{12h/g}\approx0.4946\ \mathrm{s}$; [§7](#section-7) derives this result.

These predictions describe the linearized model. At that crossing time, a unit torque with $J=0.02$ would produce $\theta\approx6.12\ \mathrm{rad}$, outside the small-angle approximation. Reducing the torque scales down the motion without changing the linear model's crossing time. Growing zero-dynamics trajectories are likewise physically valid only while angles remain small.

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

It is an **inverted**-pendulum equation, not a hanging one. A hanging pendulum of length $h$ oscillates at $\sqrt{g/h}$; this one *diverges* at rate $\sqrt{g/h}$. The positive zero is a divergence rate: its magnitude matches the hanging-pendulum frequency, but its motion grows rather than oscillating.

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
z=\sqrt{\frac{9.81}{0.2}}\approx 7.0\ \mathrm{s}^{-1}.
$$

The design heuristic of [§11](#section-11) — keep crossover comfortably below the RHP zero, with $z/2$ a common illustrative target — then suggests a practical closed-loop bandwidth for that output somewhere around $3.5\ \text{rad/s}$, about $0.56\ \text{Hz}$. Treat that as an order-of-magnitude expectation, not a computed limit.

Mounting the camera *lower* makes it worse: $h$ up, $z$ down, achievable bandwidth down. Shortening the mount or choosing a different measured point changes this geometric constraint; the precise bandwidth still depends on the rest of the design.

Moving the sensor did not change the vehicle's open-loop dynamics; the four integrators were already there.

We changed the output.

The center of mass and the offset point combine translation and rotation differently.

That changes the zeros.

In these three channels, the same four poles remain. The zeros change with the chosen output.

**Connection to [§4](#section-4):** translation and rotation subtract at the sensor in both examples. The actuation paths differ. Platform force drives translation and rotation in parallel, each with relative degree two; quadrotor torque drives translation through attitude, giving relative degrees four and two. Both worked examples have real zeros, but their initial-motion arguments are different.

---

## 7. Why the offset-point quadrotor moves the wrong way first {#section-7}

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

### Worked torque-step response

For a constant torque $M_0$ switched on at $t=0$ and zero initial state, integrate $J\ddot\theta=M_0$ twice:

$$
\theta(t)=\frac{M_0}{2J}t^2.
$$

Substitute into $\ddot x=g\theta$ and integrate twice again:

$$
x(t)=\frac{gM_0}{24J}t^4.
$$

The point below the center of mass therefore follows

$$
\boxed{y(t)=\frac{M_0}{24J}t^2(gt^2-12h),\qquad t\ge0.}
$$

For $M_0>0$ and small positive $t$, $y<0$. The nonzero crossing time is $t=\sqrt{12h/g}$, after which translation dominates. The center-of-mass output is positive for $t>0$, and the above-center output adds $hM_0t^2/(2J)$ rather than subtracting it. None of these open-loop step responses approaches a finite steady state. The small-angle qualification in [§6](#section-6) applies throughout.

---

## 8. Zero dynamics in general {#section-8}

The transfer-function definition of [Lecture 1, §14](lecture_0.0.8_student_lecture_1.md#section-14) is algebraically convenient, but the physical interpretation is more revealing and generalizes to nonlinear systems.

Suppose the output is $y(t)$. Impose

$$
\boxed{
y(t)\equiv0
}
$$

**using whatever input is required to maintain it**, and ask:

What internal motions can still occur?

Those internal motions are the **zero dynamics**. Recall [Lecture 1, §11](lecture_0.0.8_student_lecture_1.md#section-11), where the required input was $u=-(c_2\dot x_2+k_2x_2)$ and the internal motion was the free vibration of the pinned second mass.

- If all compatible internal motions decay toward equilibrium, the zero dynamics are asymptotically stable.
- A growing compatible mode makes them unstable.

For a minimal SISO continuous-time **LTI** system, an exponentially growing zero-dynamics mode corresponds to a RHP transmission zero. Simple imaginary-axis zeros give nondecaying modes; generalized modes on the axis can grow polynomially. The nonlinear definition still uses $y\equiv0$, but its stability requires analysis of the resulting nonlinear dynamics.

---

## 9. Optional: the state-space statement {#section-9}

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

So: the internal state evolves as $e^{zt}$, the input $u_0e^{zt}$ sustains that motion, and the output is identically zero. That is precisely [Lecture 1, §11](lecture_0.0.8_student_lecture_1.md#section-11) and [§8](#section-8), written in matrix form — and note that $u_0$ is generally nonzero, which is why [Lecture 1, §11](lecture_0.0.8_student_lecture_1.md#section-11)'s derivation of the required input mattered.

The minimality hypothesis matters: for a nonminimal realization the system-matrix condition describes invariant zeros, which need not coincide with the reduced transfer-function zeros. The exponential trajectory above gives the physical interpretation of the matrix condition.

---

## 10. Nonminimum phase does not mean unstable plant {#section-10}

An unstable **pole** means:

The system has a natural internal mode that grows when left alone.

A RHP **zero** means:

The chosen input-output channel has unstable zero dynamics.

A system can therefore have stable poles *and* a RHP zero — and [§4](#section-4) is a fully worked example: four poles at $-1\pm j9.95$ and $-2.5\pm j13.92$, all comfortably stable, alongside a zero at $s=+12.20$.

For each underdamped platform mode, increasing its damping coefficient moves the pole pair leftward toward critical damping; beyond critical damping one real pole returns toward the origin ([Lecture 1, §4.4](lecture_0.0.8_student_lecture_1.md#section-4-4)). Damping also moves the zeros.

In the worked platform, $AC<0$: the numerator's leading and constant coefficients have opposite signs. Their negative root product forces one positive and one negative real root for every finite damping distribution. Thus **for this geometry**, damping cannot remove the RHP zero.

$$
\boxed{AC<0:\ \text{damping moves the zeros but preserves one RHP root}}
$$

To remove that zero in this case, change $ab$, $J/m$, or $k_\theta/k_x$ — for example by moving the sensor or actuator, redistributing mass, or retuning mount stiffnesses. Outside the $AC<0$ case, damping distribution can create or remove a RHP pair, as [§4](#section-4)'s reference table shows. There is no general rule that damping affects only location while geometry alone decides existence.

$$
\boxed{
\text{stable plant poles}
\not\Rightarrow
\text{minimum-phase input-output behavior}
}
$$

The upright pendulum of [Lecture 1, §6.2](lecture_0.0.8_student_lecture_1.md#section-6-2) supplies the other distinction: it has an unstable pole and no finite zeros. Thus unstable poles do not require RHP zeros. Under [Lecture 1, §14](lecture_0.0.8_student_lecture_1.md#section-14)'s convention, we do not call that unstable plant minimum phase.

---

## 11. Why RHP zeros matter in control {#section-11}

A RHP zero places **fundamental** limitations on achievable closed-loop behavior — limitations no controller can design around, because they follow from the plant structure rather than from any particular design.

Conceptually:

1. The output may initially move in the wrong direction ([§4](#section-4), [§7](#section-7)).
2. Aggressive tracking becomes difficult: reacting hard to the initial wrong-way motion drives the system the wrong way.
3. **Bandwidth is limited.** Crossover is normally kept comfortably below the RHP zero, with $\omega_c\lesssim z/2$ widely used as an illustrative design target. This factor is a heuristic. The interpolation constraint below is fundamental; a numerical bandwidth target also depends on phase margin, loop slope, robustness requirements, and the remaining plant dynamics. Different texts quote different factors for exactly this reason. What is *not* negotiable is the direction of the effect — a slow RHP zero is a severe constraint, and [§6](#section-6)'s camera example makes it concrete.
4. Exact pole-zero cancellation is dangerous. Specifically: cancelling a plant RHP zero with a controller RHP pole (or a plant RHP pole with a controller RHP zero) produces a closed loop whose input-output transfer function looks fine but which is **internally unstable** — a hidden mode grows without bound and eventually saturates or breaks something. The cancelled factor does not go away; it just stops being visible from that one input-output pair. This is why [Lecture 1, §14](lecture_0.0.8_student_lecture_1.md#section-14) insisted $N$ and $D$ be coprime.
5. Fast plant inversion is fundamentally problematic: inverting a RHP zero produces a RHP pole.

### The underlying reason, in one line

For the standard negative-feedback loop with plant $G(s)$ and controller $K(s)$, define the sensitivity $S(s)=1/[1+G(s)K(s)]$. A well-posed, **internally stabilizing** loop satisfies the interpolation constraint

$$
S(z)=1
$$

at every RHP zero $z$ of the plant. Internal stability excludes canceling that zero with a controller RHP pole.

Read that carefully: for a real RHP zero, $z>0$ is a point on the **positive real axis of the $s$-plane**, not a sinusoidal frequency. Frequency response lives on $s=j\omega$, so it is wrong to say the sensitivity is stuck at 1 "at that frequency." $S(z)=1$ is an *analytic* constraint pinning the value of $S$ at one point of the complex plane — and because $S$ is analytic, pinning it there restricts how small it can be made along the $j\omega$ axis, which is where performance is actually measured. Together with stability and the remaining plant dynamics, this constraint underlies the tracking and robustness tradeoffs measured on the imaginary axis.

In physical terms:

A RHP zero means that making the output do exactly what we want may require the internal system to do something unstable.

---

## Review questions and answers

Use these questions to connect sensor geometry, internal motion, and control behavior.

### Zeros and geometry

**1. Why is the ball-and-beam underactuated — and under which of the two models in [§1.2](#section-1-2)?**

**Answer:** The torque-input model has two configuration degrees of freedom, $x$ and $\alpha$, but one independent actuator, $M$. The angle-input model treats $\alpha$ as an imposed input and retains only the ball coordinate; the two models have different orders.

**2. Does underactuation automatically imply a RHP zero?**

**Answer:** No. Both simplified ball-and-beam transfer functions have constant numerators, as does the quadrotor center-of-mass channel $g/(Js^4)$. Their integrator poles still prevent asymptotic and BIBO stability.

**3. Why does moving the quadrotor's output point create a zero, and why does *below* the center of mass differ from *above*?**

**Answer:** The output combines translation and rotation. Below the center of mass, $y=x-h\theta$ gives numerator $g-hs^2$ and zeros $\pm\sqrt{g/h}$. Above it, $y=x+h\theta$ gives $g+hs^2$ and zeros $\pm j\sqrt{g/h}$. At the center of mass there are no finite zeros.

**4. Why does adding damping to the rigid platform in [§4](#section-4) not remove the RHP zero?**

**Answer:** For the worked geometry, $A=J-abm$ and $C=k_\theta-abk_x$ have opposite signs. Damping changes $B=c_\theta-abc_x$ but leaves the negative root product $C/A$ unchanged. One positive real root remains for every finite damping distribution. This conclusion is specific to $AC<0$; when $AC>0$, damping can change the half plane of the roots.

**5. What do [§4](#section-4) and [§6](#section-6) have in common mechanically?**

**Answer:** Both outputs subtract a rotational contribution from a translational contribution. On the platform the input drives both paths in parallel, each with relative degree two; initial and static gains determine the opposite signs. On the quadrotor translation follows attitude, so the rotational term appears after two integrations and translation after four.

**6. Can a stable plant have a RHP zero? Can an unstable plant have no finite zeros?**

**Answer:** Yes to both. The worked rigid platform has all poles in the LHP and a zero at about $+12.20$. The upright pendulum has one unstable pole and a constant numerator, so it has no finite zeros.

---

## Optional computational examples

The accompanying Python examples recompute the numerical results and generate figures. From the directory containing these notes:

```sh
cd demos
uv run python demo7_damping_moves_zeros.py
```

Use `--show` for an interactive plot or `--no-save` for terminal output only. `uv run python run_all.py` regenerates all eight examples. Numerical residuals depend on the solver and environment.

| Script | Topic |
|---|---|
| [demo7_damping_moves_zeros.py](demos/demo7_damping_moves_zeros.py) | Zero locations under changing damping |
| [demo8_quadrotor_rhp.py](demos/demo8_quadrotor_rhp.py) | Sensor offsets and unstable zero dynamics |

Example 7 verifies the root-product result for the selected $AC<0$ geometry. Its statements about damping preserving the half planes of the zeros apply to that case; the full classification in these notes explains why they do not extend to every geometry. Example 8 checks the divergence rate through the transfer zeros, analytic zero dynamics, and numerical simulation. Its center-of-mass plot label “minimum phase” should be read as “no finite zeros” under the convention used here. Its unit-torque and growing-angle traces illustrate the linear equations; they exceed the physical small-angle range at sufficiently large amplitudes. The worked derivation in these notes states the applicable model limits.
