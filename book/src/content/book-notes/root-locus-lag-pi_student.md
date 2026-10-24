# The Root-Locus Design Method IV — Lag, PI, and Design Extensions

**Student lecture notes — FPE 8th ed., Sections 5.4.2–5.4.3; PI supplement and feedback extension**

Lead and PD mainly address transient behavior. Lag and PI address low-frequency tracking and disturbance rejection. They add dynamics, so their benefit must be checked against changes in the transient response.

**Prerequisites:** [III — PD and lead design](root-locus-lead-pd_student.md), [system type and error constants](system-type_student.md), and [PID implementation](pid-tuning_student.md).

**Sources:** FPE 8th ed., §§5.4.2–5.4.3, checked against the 7th ed.; §5.6.2 for successive loop closure. Nise 7th ed., §9.2, supplies the explicit PI versus lag comparison, with §§9.4–9.5 for combined and feedback compensation. Ogata 5th ed., §§6–7 and 6–8, supplements lag and lag–lead design. Our motor lag and PI designs are **[course examples]**; §6 uses FPE's own lead–lag values. The notch and rate-feedback calculations are **[course extensions]**, not complete flexible-robot designs.

## Learning objectives

1. Design a lag pole-zero pair for a specified error-constant improvement.
2. Design a PI controller and verify its increased system type and stability.
3. Check the slow mode in both reference and disturbance responses.
4. Explain the roles of lag–lead, notch, and feedback compensation.
5. Recognize where a pole-zero cancellation or an approximate design argument needs further validation.

## Notation and assumptions

Negative unity position feedback, normalized $G=1/[s(s+1)]$, and seconds throughout. Plant-input disturbance $W$ adds to the actuator command, so $Y=G(U+W)$. With $R=0$, $E=-Y$. Use $L=D_cG$, $S=1/(1+L)$, $\mathcal T=L/(1+L)$. In $D_c=K(s+z)/(s+p)$, $z,p>0$ are positive parameters and the actual locations are $-z,-p$. Lag has $z>p$; PI has $p=0$ and $z>0$. Settling times use the course’s 1% band.

---

## Where we are, and where this lecture goes

Lecture III fixed the transient by adding a zero that pulled the branches left. Lecture II left a second problem untouched: the tracking error to a ramp, which is set by the loop gain at low frequency and which the locus does not display. This lecture addresses that problem, and the trick is almost the opposite of lead. Instead of moving the dominant branches, we try to leave them exactly where they are.

The device is a pole and a zero placed very close together near the origin. Seen from the dominant pair, the two arrows nearly coincide, so their angles cancel and the locus near the pair hardly moves. Seen from $s=0$, their ratio $z/p$ multiplies the DC gain of the controller, and with it the velocity constant. Such a pair is a **lag compensator**; the name refers to the negative phase it contributes, which Part V will make precise. Push the pole all the way to the origin and the finite DC gain becomes an integrator: the lag becomes PI, and the system type goes up by one.

Nothing is free. The added pole and zero capture one closed-loop pole near the origin, and that pole is slow. The story of this lecture is designing the lag (§2), discovering the slow tail and understanding where it comes from and where it matters (§3), making the same improvement with PI (§4), comparing the two (§5), and then surveying three extensions that use the same "change the pattern" idea (§§6–8).

## 1. Specify the accuracy improvement {#section-1}

The baseline controller is $D_c=1$. Its poles are $-0.5\pm0.8660j$, with $16.30\%$ overshoot, and

$$
K_v=\lim_{s\to0}sD_cG=1\ \mathrm{s}^{-1}.
$$

For a ramp of slope $v$, $e_{ss}=v/K_v$. We seek a factor-five reduction for unit slope: from 1 to at most 0.2. We would like to keep the early transient reasonably close to the baseline. This is a tracking specification plus a transient preference; we will measure the change rather than assume it is zero.

Raising the proportional gain to 5 would meet $K_v=5$, but gives $\zeta=1/(2\sqrt5)=0.224$ and about 48.6% overshoot. Instead, raise the gain near $s=0$ while keeping the compensator close to unity near the original pair.

## 2. Full lag design {#section-2}

Choose

$$
D_c(s)=K\frac{s+z}{s+p},\qquad z>p>0.
$$

At zero frequency $D_c(0)=Kz/p$; for $|s|\gg z,p$, $D_c(s)\approx K$. Thus with $K=1$, choose $z/p=5$.

Why does this not wreck the transient we already have? The dominant pair sits about one unit from the origin, and the new pole and zero are a few hundredths away from it. The arrows from $-z$ and from $-p$ to the pair are almost the same arrow, so their angle contributions nearly cancel and the angle condition at the pair is nearly unchanged. Their lengths are nearly equal too, so the magnitude condition is nearly unchanged. "Nearly" is the operative word, and the first candidate below measures how nearly.

### First candidate and angle check

Take $z=0.05$, $p=0.01$. At the old pole $s_d=-0.5+0.8660j$,

$$
\arg(s_d+0.05)-\arg(s_d+0.01)\approx-2.04^\circ.
$$

This is small but not zero. The old pair is no longer exactly on the new locus. If the gain were retuned, the exact error-constant improvement would be $(K_{new}/K_{old})(z/p)$, not simply $z/p$.

For $K=1$, the characteristic equation is

$$
s(s+1)(s+0.01)+(s+0.05)=0,
$$

$$
P=s^3+1.01s^2+1.01s+0.05.
$$

Its roots are $-0.05208$ and $-0.47896\pm0.85482j$. Stability follows independently from the cubic Routh conditions: all coefficients are positive and $1.01(1.01)>0.05$.

The error constant is exactly $K_v=5$, hence the unit-ramp error is exactly 0.2. However, the reference step has about **21.56% overshoot** and **28.32 s settling time (1%)**, compared with 16.30% and about 8.8 s initially. A small angular change was not enough to preserve the transient.

What went wrong? Look at the roots. The complex pair moved only slightly, from $-0.5\pm0.866j$ to $-0.479\pm0.855j$. That small shift explains some extra overshoot, but not a tripled settling time. The culprit is the third root at $-0.052$, which did not exist before. The lag pole and zero near the origin have captured one closed-loop pole between them, and it decays with a time constant of about $19$ s. Section 3 explains why its effect on the reference step is small but not negligible, and why its effect elsewhere is larger.

### Revised lag design

Move both locations five times closer to the origin, retaining the ratio:

$$
\boxed{D_c(s)=\frac{s+0.01}{s+0.002}}.
$$

The characteristic polynomial is

$$
\boxed{P=s^3+1.002s^2+1.002s+0.01}.
$$

The poles are approximately $-0.010081$ and $-0.49596\pm0.86373j$. Routh gives $1.002^2>0.01$, so the loop is stable. $K_v$ remains exactly 5. The angle perturbation at the original pair is about $-0.40^\circ$.

Moving the pair inward makes the captured pole even slower, with a time constant near $99$ s. It also moves that pole closer to the zero at $-z$, which shrinks its share of the reference step response. The trade is a longer but much smaller tail, and for the step the smaller amplitude wins.

The reference step now overshoots **17.38%** and enters its 1% band for the last time at about **12.0 s**. This is faster than the first lag candidate’s 28.32 s, but slower than the baseline’s roughly 8.8 s. The accuracy improvement still costs some settling time, even though the early response remains close to baseline.

This design meets the specified ramp accuracy and keeps the early transient close to baseline. If there were a strict 16.3% overshoot limit, further redesign would be needed.

## 3. Why the small pole still matters {#section-3}

Here is the mechanism behind the tail, and why its size depends on which input you look at.

For a lag controller on this motor,

$$
P=s(s+1)(s+p)+K(s+z),\qquad
\frac YR=\frac{K(s+z)}P,\qquad
\frac YW=\frac{s+p}P.
$$

The slow closed-loop pole lies near $-z$, so its reference-step residue is small because $Y/R$ has a nearby zero. The disturbance path has a different zero, at $-p$. It need not suppress that mode by the same amount.

The close-up locus in §4 shows how the slow pole arises. At very small gain the two near-origin poles, at $0$ and $-p$, leave the real axis, circle around the lag zero, and land again just to its left. One of them then travels right toward the zero at $-z$ and is captured there; the other heads left to meet the motor pole from $-1$ and form the familiar dominant pair. By $K=1$ the captured pole has nearly reached the zero. That is why the reference step barely sees it: in $Y/R$ a pole almost on top of a zero has a tiny residue. The disturbance path $Y/W$ has its zero at $-p$ instead, well away from the captured pole on the scale of the pair, so the slow mode appears there at nearly full strength.

For the first candidate, the slow-pole term in the unit reference step is approximately

$$
0.04369e^{-0.05208t}.
$$

That term alone remains larger than 1% for roughly 28.3 s. The full settling time depends on its sum with the oscillatory terms. In the revised design the slow pole has an approximately 99 s time constant, even though the reference step enters its 1% band much earlier.

For a unit step disturbance at the plant input,

$$
y_{ss}=\lim_{s\to0}\frac{G}{1+D_cG}=\frac1{D_c(0)}=0.2,
\qquad e_{ss}=-0.2.
$$

The ramp-tracking error and disturbance response approach their final values slowly. Simulate long enough to see that approach; a short reference-step plot is insufficient.

![Lag and PI reference steps, ramp tracking errors, and plant-input disturbance steps](demos/ch5/figures/l4_demo1_lag_pi.svg)

## 4. Full PI design {#section-4}

A finite DC gain leaves a finite ramp error. To eliminate it, make the DC gain infinite: move the lag pole to the origin and increase the loop type from 1 to 2. Nise §9.2 makes this distinction explicit: lag improves an error constant; PI adds an integrator. Nise calls PI an “ideal integral compensator.”

Use

$$
D_c(s)=K\frac{s+z}{s}=K+\frac{Kz}s,
\qquad k_P=K,\quad k_I=Kz.
$$

Choose $K=1$, $z=0.01$ to keep the added zero near the added pole at the origin:

$$
\boxed{D_c(s)=1+\frac{0.01}s},\qquad
\boxed{P=s^3+s^2+s+0.01}.
$$

### Stability before final values

For general $K,z>0$,

$$
P=s^3+s^2+Ks+Kz,
\qquad
\begin{array}{c|cc}
s^3&1&K\\
s^2&1&Kz\\
s^1&K(1-z)&0\\
s^0&Kz&0
\end{array}.
$$

With the motor pole normalized to $-1\ \mathrm{s}^{-1}$, stability requires $K>0$ and $0<z<1\ \mathrm{s}^{-1}$. For a motor denominator $s(s+a)$, the corresponding condition is $0<z<a$, not a universal numerical bound of one.

The zero is doing more than tuning here; it is what makes the loop stable at all. Without it the loop would be $K/[s^2(s+1)]$: a double pole at the origin that departs at $\pm90^\circ$, three branches to infinity at $\pm60^\circ$ and $180^\circ$, and a Routh array with a negative entry for every $K>0$. Pure integral control of this motor is unstable at every gain. The zero at $-z$ pulls the two branches from the origin back into the left half-plane, and the condition $z<a$ says it must sit closer to the origin than the motor pole to do so.

Our selected poles are approximately $-0.010101$ and $-0.49495\pm0.86315j$, all stable. The angle perturbation at the old pair is about $-0.50^\circ$.

### Tracking and disturbance checks

There are two uncancelled loop poles at the origin:

$$
L(s)=\frac{K(s+z)}{s^2(s+1)},\qquad K_a=\lim_{s\to0}s^2L=Kz=0.01\ \mathrm{s}^{-2}.
$$

Thus steady-state errors to step and ramp references are zero. A unit parabolic reference $r=t^2/2$ gives $e_{ss}=1/K_a=100$; zero ramp error is not perfect tracking of every trajectory.

For the plant-input step disturbance,

$$
\frac YW=\frac{s}{s^3+s^2+s+0.01},\qquad y_{ss}=0.
$$

The disturbance is eventually rejected, but the slow mode still takes about 100 s per time constant. The unit reference step overshoots **17.66%** and has about **12.76 s** 1% settling time. As with lag, the reference transient can look fast while disturbance rejection is slow.

The result assumes no saturation. The integral state can wind up under actuator limits; use the antiwindup techniques developed in [PID implementation](pid-tuning_student.md).

![Root-locus closeups show the added poles and zero near the origin and the slow root selected at K=1](demos/ch5/figures/l4_demo1_lag_pi_locus.svg)

The closeups show only the branches near the origin. At $K=1$, the complex pair lies outside each window; the marked square is the slow real root.

## 5. Lag versus PI {#section-5}

| Feature | Lag $K(s+z)/(s+p)$ | PI $K(s+z)/s$ |
|---|---|---|
| Pole-zero relation | $z>p>0$ | $z>0$, pole at origin |
| Loop type | unchanged, absent cancellation | increases by one, absent cancellation |
| DC controller gain | finite, $Kz/p$ | unbounded |
| Unit-ramp error on this motor | $p/(Kz)$ | zero when stable |
| Step plant-input disturbance | finite offset $p/(Kz)$ | zero eventual offset when stable |
| Main check | slow tails and phase perturbation | stability, slow rejection, saturation |

Taking $p\to0$ at fixed $z,K$ connects lag to PI, but the long-time behavior changes: the finite DC gain becomes an integrator. Setting **both** $p=z=0$ cancels the intended factor and leaves proportional control; that does not increase the type.

## 6. Extension: lag–lead, using Franklin's design {#section-6}

The remaining sections are variations on one theme: when the locus does not go where you need it, change the pattern of poles and zeros that generates it. Three such patterns are common enough to have names.

Lead and lag act in different frequency ranges, so they can be combined. A lead section shapes the dominant branches; a lag section then raises the low-frequency gain without disturbing them much.

FPE §5.4.2 starts from the revised lead of Example 5.11:

$$
D_{lead}=91\frac{s+2}{s+13},\qquad K_v=\frac{91\cdot2}{13}=14.
$$

To obtain $K_v=70$, the book adds $(s+0.05)/(s+0.01)$:

$$
D_c=91\frac{(s+2)(s+0.05)}{(s+13)(s+0.01)}.
$$

The full characteristic polynomial is

$$
P=s^4+14.01s^3+104.14s^2+186.68s+9.1.
$$

Its roots are approximately $-0.050140$, $-2.3967$, and $-5.7816\pm6.5038j$. All are in the LHP. The computed reference step has about 17.47% overshoot and 0.190 s rise time, preserving the original 20% and 0.3 s requirements. Unit-ramp error is $1/70$.

The two sections are designed for different purposes, but they interact. Verify the combined system after adding the second section. “Lead first, lag second” is a practical sequence, not a theorem that the first design remains unchanged.

## 7. Extension: a notch for a flexible mode {#section-7}

The second pattern targets a resonance. A lightly damped mechanical mode is an open-loop pole pair close to the imaginary axis, and the departure-angle calculation of Lecture I often shows feedback pushing it toward instability. The remedy is a controller zero pair placed near the mode, so that the offending branches end almost where they begin, backed by a better-damped pole pair so that the controller is realizable.

FPE §5.4.3 treats an additional lightly damped mechanical mode: its Eq. (5.74) plant has a troublesome resonance near 50 rad/s. Our 10 rad/s filter below is a simpler illustration, not the book’s numerical design. A controller designed for a rigid model may excite that mode. One option is a notch filter with a conjugate pair of zeros near the troublesome frequency and a more heavily damped pole pair:

$$
D_N(s)=\frac{s^2+2\zeta_z\omega_f s+\omega_f^2}
{s^2+2\zeta_p\omega_f s+\omega_f^2},\qquad
0<\zeta_z<\zeta_p.
$$

For a stable filter, substituting $s=j\omega$ gives the gain applied to a sinusoid at frequency $\omega$; this is the frequency-response idea already introduced with harmonic forcing. At $\omega=\omega_f$,

$$
|D_N(j\omega_f)|=\frac{\zeta_z}{\zeta_p},\qquad
D_N(0)=1,\qquad D_N(\infty)=1.
$$

For $\omega_f=10\ \mathrm{rad/s}$, $\zeta_z=0.03$, $\zeta_p=0.30$,

$$
D_N(s)=\frac{s^2+0.6s+100}{s^2+6s+100}.
$$

It transmits 10% of a 10 rad/s sinusoid's amplitude. At 8 and 12 rad/s its amplitude ratios are approximately 0.605 and 0.528. A shifted resonance can therefore greatly reduce its effectiveness.

This calculation explains a notch; it does not establish closed-loop stability for an unspecified flexible plant. Include the flexible dynamics, inspect the complete root locus and departure directions, and check plausible frequency variation. Do not rely on exact cancellation of an uncertain lightly damped plant pole; never use cancellation of an unstable pole as a stability argument.

## 8. Extension: feedback compensation and successive loop closure {#section-8}

The third pattern changes not the controller's transfer function but where the measurement enters. Lecture III noted that a derivative acting on the measured output, rather than on the error, gives the same poles without the reference zero. Here is that arrangement, now seen as a root-locus design.

A velocity sensor can provide damping inside a position loop. Let

$$
u=K(r-y)-k_v\dot y,\qquad G=\frac1{s(s+1)}.
$$

Substituting into $Y=GU$ gives

$$
[s(s+1)+k_vs+K]Y=KR,
\qquad
\boxed{\frac YR=\frac K{s^2+(1+k_v)s+K}}.
$$

Choose $K=8$, $k_v=3$. The poles are again $-2\pm2j$, but $Y/R=8/(s^2+4s+8)$ has no PD reference zero. The step overshoot is the standard pair's 4.32%.

Equivalently, first close the velocity loop:

$$
G_{inner}=\frac{G}{1+k_vsG}
=\frac1{s(s+1+k_v)},
$$

then use $K$ in the outer position loop. This is **successive loop closure** (FPE §5.6.2). Include the actual sensor and filter dynamics before treating this ideal derivative feedback as a realizable design.

![Lead-lag response, notch detuning, and comparison of rate feedback with forward-path PD](demos/ch5/figures/l4_demo2_extensions.svg)

## 9. MATLAB and demonstrations {#section-9}

```matlab
s = tf('s');
G = 1/(s*(s+1));
Dlag = (s+0.01)/(s+0.002);
Dpi = (s+0.01)/s;
Tlag = feedback(Dlag*G,1);
Tpi = feedback(Dpi*G,1);
pole(Tlag), pole(Tpi)
step(Tlag,Tpi); grid on
% A long horizon exposes the slow disturbance response:
t = (0:0.02:1000)';
figure; step(feedback(G,Dlag),feedback(G,Dpi),t); grid on
% feedback(G,D) is G/(1+G*D), the plant-input disturbance path.
```

Run `l4_demo1_lag_pi.py` for the full designs and `l4_demo2_extensions.py` for the optional extensions. See the [demo guide](demos/ch5/guide.md).

## What to take away

- A lag compensator is a pole-zero pair close together near the origin. Seen from the dominant poles the pair nearly cancels; seen from $s=0$ its ratio $z/p$ multiplies the error constant.
- The pair captures one closed-loop pole near the lag zero. Its residue in the reference step is small, but the same mode appears in full in the disturbance response and in the approach to the final ramp error. Simulate long enough to see it.
- PI is lag with the pole at the origin. The DC gain becomes infinite and the type goes up by one, so ramp error and plant-input disturbance offset both vanish. The zero is what keeps the loop stable: $0<z<a$ on this motor.
- Lag–lead, notch, and rate feedback are the same idea in three more forms: change the pattern of poles and zeros, or where the measurement enters, and re-check the complete locus and response.

### The root-locus toolkit, in one place

Across the four lectures the method reduced to a few moves. A gain slides every closed-loop pole along fixed branches (I, II). A left-half-plane zero pulls the branches toward it, which is how PD and lead improve the transient (III). A pole pushes them away, which is why lead's extra pole and every unmodelled lag cost stability margin (I, III). A near-origin pole-zero pair raises the low-frequency gain while leaving the branches almost alone, which is how lag and PI improve accuracy (IV). Every one of these moves is checked the same way: find all the poles at the chosen gain, form the complete transfer function, and look at the response. Part V develops the same designs from the frequency response, where the cost of each move appears as phase.

## Review questions

1. Why does the ratio $z/p$ improve $K_v$ without increasing system type?
2. Why must the gain correction be included if a lag design retunes $K$?
3. Can a 99 s time constant coexist with a 12.0 s reference-step settling time at 1%?
4. For $G=1/[s(s+a)]$, derive the PI stability condition and interpret it physically.
5. Does zero steady-state ramp error imply small error throughout a finite move?
6. Why does velocity feedback have a different reference numerator from forward-path PD?
7. Why is a notch filter's attenuation at the nominal mode frequency insufficient to establish robustness?

## Optional practice

For the lag design, sweep $z$ while holding $z/p=5$, and compare reference-step overshoot, last 1% band entry, and time to approach the final ramp error. For PI, sweep $z$ toward the Routh boundary. Use Nise 7th ed. §9.2 and Ogata 5th ed. §6–7 for additional examples; Ogata §6–8 covers lag–lead.

**Previous:** [III — PD and lead](root-locus-lead-pd_student.md). **Next course topic:** frequency response, Bode plots, and design margins in Part V.
