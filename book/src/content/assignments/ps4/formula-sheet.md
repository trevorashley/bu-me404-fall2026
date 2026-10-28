# ME404 Midterm Formula Sheet (FPE Chapters 1–4)

This sheet is handed out with the midterm. It contains formulas only. Notation: $D_c(s)$ controller, $G(s)$ plant, $H(s)$ sensor, $L=D_cG$ loop gain, $\mathcal T=Y/R$, $E=R-Y$ the system error, $W$ a disturbance, $1(t)$ the unit step.

## 1. Laplace transform

$$
F(s)=\int_{0^-}^{\infty}f(t)e^{-st}\,dt
$$

| $f(t)$, $t\ge0$ | $F(s)$ | $f(t)$, $t\ge0$ | $F(s)$ |
|---|---|---|---|
| $\delta(t)$ | $1$ | $e^{-at}$ | $\dfrac{1}{s+a}$ |
| $1(t)$ | $\dfrac1s$ | $te^{-at}$ | $\dfrac{1}{(s+a)^2}$ |
| $t$ | $\dfrac1{s^2}$ | $\sin\omega t$ | $\dfrac{\omega}{s^2+\omega^2}$ |
| $\dfrac{t^n}{n!}$ | $\dfrac{1}{s^{n+1}}$ | $\cos\omega t$ | $\dfrac{s}{s^2+\omega^2}$ |
| $e^{-\sigma t}\sin\omega t$ | $\dfrac{\omega}{(s+\sigma)^2+\omega^2}$ | $e^{-\sigma t}\cos\omega t$ | $\dfrac{s+\sigma}{(s+\sigma)^2+\omega^2}$ |

| Property | Time domain | Transform |
|---|---|---|
| Linearity | $\alpha f+\beta g$ | $\alpha F+\beta G$ |
| Derivative | $\dot f$ | $sF(s)-f(0^-)$ |
| Second derivative | $\ddot f$ | $s^2F(s)-sf(0^-)-\dot f(0^-)$ |
| Integral | $\int_{0}^{t}f(\tau)\,d\tau$ | $F(s)/s$ |
| Time delay | $f(t-\tau)1(t-\tau)$ | $e^{-s\tau}F(s)$ |
| Convolution | $\int_0^t h(t-\tau)u(\tau)\,d\tau$ | $H(s)U(s)$ |
| Exponential weight | $e^{-at}f(t)$ | $F(s+a)$ |
| Final Value Theorem | if **every pole of $sF(s)$ is strictly in the LHP**: $\lim_{t\to\infty}f(t)=\lim_{s\to0}sF(s)$ | |
| Initial Value Theorem | $f(0^+)=\lim_{s\to\infty}sF(s)$ ($F$ strictly proper) | |

**Partial fractions.** For a simple pole $p_i$ of $F(s)$, the residue is $C_i=\left[(s-p_i)F(s)\right]_{s=p_i}$ (cover-up). Repeated poles and complex pairs: match coefficients or complete the square.

## 2. Frequency response and Fourier series

For a **stable** $G(s)$ driven by $u=A\cos\omega t$, the steady-state output is

$$
y_{ss}(t)=A\,|G(j\omega)|\cos\bigl(\omega t+\angle G(j\omega)\bigr).
$$

Periodic $u(t)$ with period $T$, $\omega_0=2\pi/T$:

$$
u(t)=\sum_{k=-\infty}^{\infty}c_ke^{jk\omega_0t},
\qquad
c_k=\frac1T\int_{t_0}^{t_0+T}u(t)e^{-jk\omega_0t}\,dt,
\qquad
c_{-k}=\overline{c_k}\ \text{(real }u\text{)}.
$$

Pairing $\pm k$: $c_ke^{jk\omega_0t}+c_{-k}e^{-jk\omega_0t}=2|c_k|\cos(k\omega_0t+\angle c_k)$. Periodic steady-state output of a stable $G$: $d_k=G(jk\omega_0)\,c_k$.

## 3. Block diagrams

Series $G_1G_2$; parallel $G_1+G_2$; negative feedback with forward $G$ and return $H$:

$$
\frac{Y}{R}=\frac{G}{1+GH}.
$$

Pickoff point moved from the input of $G$ to its output: $1/G$ on the moved branch. Summing junction moved from the input of $G$ to its output: $G$ on the moved input. Reverse moves use the reciprocal. Or write the signal equation at each junction and eliminate the internal signals.

## 4. Second-order response

$$
\frac{\omega_n^2}{s^2+2\zeta\omega_ns+\omega_n^2},
\qquad
s=-\sigma\pm j\omega_d,
\qquad
\sigma=\zeta\omega_n,\quad
\omega_d=\omega_n\sqrt{1-\zeta^2},\quad
\zeta=\sin\theta
$$

where $\theta$ is the angle of the pole from the imaginary axis. Unit-step response for $0<\zeta<1$:

$$
y(t)=1-e^{-\sigma t}\left(\cos\omega_dt+\frac{\sigma}{\omega_d}\sin\omega_dt\right)
=1-\frac{e^{-\sigma t}}{\sqrt{1-\zeta^2}}\cos\bigl(\omega_dt-\sin^{-1}\zeta\bigr).
$$

| Specification | Formula | Notes |
|---|---|---|
| Rise time (10–90%) | $t_r\simeq\dfrac{1.8}{\omega_n}$ | fit near $\zeta\approx0.6$; $\omega_nt_r\approx1.1,\,1.6,\,2.1,\,3.4$ at $\zeta=0.1,\,0.5,\,0.7,\,1$ |
| Peak time | $t_p=\dfrac{\pi}{\omega_d}$ | exact, no zeros |
| Overshoot | $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ | exact, no zeros; $M_p=0$ for $\zeta\ge1$ |
| Settling time (1%) | $t_s\simeq\dfrac{4.6}{\sigma}$ | from the envelope; critically damped: $t_s\approx6.6/\omega_n$ |

| $\zeta$ | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 |
|---|---|---|---|---|---|
| $M_p$ | 25% | 16% | 9.5% | 4.6% | 1.5% |

**First order** $\dfrac{\sigma}{s+\sigma}$: $y=1-e^{-\sigma t}$, $M_p=0$, $t_r=\dfrac{\ln9}{\sigma}\approx\dfrac{2.2}{\sigma}$, $t_s=\dfrac{\ln100}{\sigma}\approx\dfrac{4.6}{\sigma}$.

**Zeros** ($z>0$, $y_0$ the step response of the zero-free second-order $H_0$ above). An LHP zero at $s=-z$: $H=\left(1+\dfrac sz\right)H_0$, $y=y_0+\dfrac1z\dot y_0$, which for an underdamped pair adds overshoot and shortens the rise, more so the closer the zero is to the dominant poles. An RHP zero at $s=+z$: $H=\left(1-\dfrac sz\right)H_0$, $y=y_0-\dfrac1z\dot y_0$, which causes initial undershoot. **Extra poles** slow the rise. Poles or zeros more than about four times farther from the imaginary axis than the dominant pair have a small effect; closer ones must be checked.

## 5. Routh's criterion

$a(s)=a_ns^n+\dots+a_0$ with $a_n>0$. All roots in the LHP **only if** every $a_i>0$, and **if and only if** every entry of the first column of the array is positive. The number of sign changes equals the number of RHP roots.

$$
\begin{array}{c|ccc}
s^n & a_n & a_{n-2} & a_{n-4}\\
s^{n-1} & a_{n-1} & a_{n-3} & a_{n-5}\\
s^{n-2} & b_1 & b_2 & \cdots\\
s^{n-3} & c_1 & c_2 & \cdots\\
\vdots
\end{array}
\qquad
b_1=\frac{a_{n-1}a_{n-2}-a_na_{n-3}}{a_{n-1}},\quad
b_2=\frac{a_{n-1}a_{n-4}-a_na_{n-5}}{a_{n-1}},\quad
c_1=\frac{b_1a_{n-3}-a_{n-1}b_2}{b_1}.
$$

Cubic $s^3+a_2s^2+a_1s+a_0$: stable iff $a_2,a_1,a_0>0$ and $a_2a_1>a_0$. If a whole row is zero, form the **auxiliary polynomial** from the row above; its roots (symmetric about the origin, often $\pm j\omega$) are roots of $a(s)$, and the row is replaced by the derivative of the auxiliary polynomial.

## 6. Feedback properties

$$
S=\frac{1}{1+L},\qquad
\mathcal T=\frac{L}{1+L},\qquad
S+\mathcal T=1,\qquad
L=D_cG\ (\text{unity feedback}).
$$

Unity feedback with $W$ at the plant input and sensor noise $V$:

$$
Y=\mathcal T R+GS\,W-\mathcal T V,
\qquad
E=R-Y=S\,R-GS\,W+\mathcal T V.
$$

Sensitivity of a gain $\mathcal T$ to a parameter $K$: $S^{\mathcal T}_K=\dfrac{d\mathcal T/\mathcal T}{dK/K}=\dfrac{K}{\mathcal T}\dfrac{d\mathcal T}{dK}$. Open loop: $S^{\mathcal T}_G=1$. Feedback: $S^{\mathcal T}_G=\dfrac{1}{1+L}$.

## 7. System type and steady-state error

Unity feedback, reference $r=t^k/k!$, loop stable. Write $L(s)=\dfrac{L_o(s)}{s^n}$ with $L_o(0)\ne0$; the loop is **Type $n$**.

| Type | step error | ramp error | parabola error | constant |
|---|---|---|---|---|
| 0 | $\dfrac{1}{1+K_p}$ | $\infty$ | $\infty$ | $K_p=\lim_{s\to0}L$ |
| 1 | $0$ | $\dfrac{1}{K_v}$ | $\infty$ | $K_v=\lim_{s\to0}sL$ |
| 2 | $0$ | $0$ | $\dfrac{1}{K_a}$ | $K_a=\lim_{s\to0}s^2L$ |

General structure (sensor $H$, prefilter, or anything else): with $\mathcal T=Y/R$,

$$
e_{ss}=\lim_{s\to0}\frac{1-\mathcal T(s)}{s^k},
$$

and the loop is Type $k$ when this limit is a nonzero constant. For a disturbance, with $R=0$, $T_w=\dfrac{E}{W}=-\dfrac{Y}{W}$; write $T_w=s^nT_{o,w}$ with $T_{o,w}(0)=1/K_{n,w}\ne0$: the loop is Type $n$ with respect to $W$, and for $w=t^k/k!$ the error is $0$ if $n>k$, $T_{o,w}(0)$ if $n=k$, unbounded if $n<k$.

## 8. PID control and Ziegler–Nichols tuning

$$
D_c(s)=k_P+\frac{k_I}{s}+k_Ds
=k_P\left(1+\frac{1}{T_Is}+T_Ds\right),
\qquad
k_I=\frac{k_P}{T_I},\quad k_D=k_PT_D.
$$

Step-response (process reaction curve) rules, with $R$ the reaction rate (slope) and $L$ the lag of the open-loop step response (Table 4.2; here $R$ and $L$ are not the reference and loop gain):

| Controller | $k_P$ | $T_I$ | $T_D$ |
|---|---|---|---|
| P | $1/(RL)$ | — | — |
| PI | $0.9/(RL)$ | $L/0.3$ | — |
| PID | $1.2/(RL)$ | $2L$ | $0.5L$ |

Ultimate-sensitivity rules, with $K_u$ the proportional gain at which the loop just oscillates and $P_u=2\pi/\omega_u$ the period of that oscillation (Table 4.3):

| Controller | $k_P$ | $T_I$ | $T_D$ |
|---|---|---|---|
| P | $0.5K_u$ | — | — |
| PI | $0.45K_u$ | $P_u/1.2$ | — |
| PID | $0.6K_u$ | $P_u/2$ | $P_u/8$ |

## 9. Constants

$\ln2=0.693$, $\ln9=2.197$, $\ln100=4.605$, $\pi=3.142$, $e^{-\pi}=0.0432$, $1/\sqrt2=0.707$, $\sqrt3=1.732$, $1\ \mathrm{rad/s}=9.549\ \mathrm{rpm}$.
