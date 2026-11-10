# ME404: Dynamics and Control of Mechanical Systems, Fall 2026

## Problem Set \#5: Root-locus construction and servo analysis

**Assigned:** Tuesday, November 10, 2026  
**Due:** Thursday, November 19, 2026, at 3:30 PM in person or 11:59 PM electronically  
**Grading:** 100 points, based on correctness with partial credit for correct reasoning and calculations. Allow approximately six to eight hours, including MATLAB and submission preparation; this is an estimate.

**AI policy:** AI may help with MATLAB coding and plotting and provide hints on how to start. Your analytical reasoning, calculations, and explanations must be your own. Do not ask AI to solve the problems for you.

Use unity negative feedback throughout. Assume linear continuous-time models, normalized signals, no actuator saturation, and zero initial conditions for forced responses. Interpret zero-parameter endpoints using the full characteristic polynomial before transfer-function cancellations. Time is in seconds, and pole coordinates are in $\mathrm{s}^{-1}$. Use 10–90% rise time and a **1% settling band** about the known final output.

Work by hand first, then verify with MATLAB. Submit your calculations, labeled hand sketches with arrows for increasing parameter, MATLAB plots, short interpretation, and the commands used. Code alone does not earn plot-verification credit. There are **five distinct loci**: one each in Problems 1–3 and two in Problem 4. Show the filter locus in both a full view and a zoomed view. Legible panels may share a page.

For every locus, state the varied parameter and its range, what is held fixed, and the rational function passed to `rlocus`. Use the [Root Locus I checklist](../../book-notes/root-locus-construction_student.md#section-4) in order: (1) branch starts and endpoints with multiplicity, (2) real-axis portions, (3) asymptotes, (4) departure or arrival directions where needed, and (5) multiple-root events. Imaginary-axis crossings and stability are additional checks. Let $L$ denote the physical loop; $L_{0,\beta}$, $L_{0,\lambda}$, and $L_{0,p}$ exclude their respective varied parameters.

*Sources:* These are original course exercises using FPE, *Feedback Control of Dynamic Systems*, 8th edition, §§5.1–5.2, checked against the 7th edition. Nise, *Control Systems Engineering*, 7th edition, §8.5 and Example 8.3, supplements the break-point method. See also [Root Locus II](../../book-notes/root-locus-gain-design_student.md) and [Root Locus III](../../book-notes/root-locus-lead-pd_student.md).

### Problem 1: Breakaway and break-in (20 points)

The loop transfer function is

$$
L(s)=K L_0(s),\qquad L_0(s)=\frac{s+3}{s(s+2)},\qquad K\geq0.
$$

**(a) [4 points]** Write the characteristic equation in polynomial and Evans forms. Identify the branch starts, finite endpoint, branch count, symmetry, real-axis portions, and asymptote, including its centroid.

**(b) [6 points]** Form $K(s)$ and use $dK/ds=0$ to find the real-axis multiple-root candidates. Check each against the real-axis rule and $K\geq0$. Find the gain at each accepted point and identify breakaway versus break-in. Use Rule 5 to show the local incoming and outgoing directions, then complete the hand sketch. A proof of the exact curved-branch shape is not required.

**(c) [4 points]** Test $s=-2+j\sqrt2$ using both the angle and magnitude conditions. Show the individual vector angles, find the gain, and report all closed-loop poles at that gain.

**(d) [2 points]** Determine the gain interval for asymptotic stability, including the status of $K=0$.

**(e) [4 points]** Submit a MATLAB `rlocus` plot with the calculated break points and trial-point poles labeled. Use equal real and imaginary axis scales and briefly compare it with your sketch.

*Single-asymptote hint, also useful in Problem 4:* If $L_0=c\,b(s)/a(s)$ with $c>0$, monic $a,b$, and $\deg a=\deg b+1$, polynomial division gives $a/b=s-\sigma_a+O(1/s)$. Thus the escaping root satisfies $s\approx\sigma_a-cK$ at large gain. A positive centroid is an offset in this relation and does not by itself imply an unstable high-gain pole. Preserve any fixed scale factor $c$ when interpreting MATLAB's parameter.

### Problem 2: Complex departure and a stability limit (20 points)

The loop transfer function is

$$
L(s)=\frac{K}{(s+1)(s^2+4s+8)},\qquad K\geq0.
$$

**(a) [6 points]** Write the characteristic polynomial. Find the branch starts and endpoints, symmetry, real-axis portion, asymptotes, and centroid. Calculate the departure angle from the upper complex pole using the individual pole vectors, then use symmetry for the lower pole. Measure angles counterclockwise from the positive real axis.

**(b) [4 points]** Use $dK/ds=0$ to determine whether there are real-axis breakaway or break-in points. Complete the hand sketch using all five rules.

**(c) [6 points]** Find the actual imaginary-axis crossing, the gain there, and the stable gain interval. You may use Routh's criterion or substitute $s=j\omega$ and establish stability on each side. Explain why the crossing is not generally where an asymptote intersects the imaginary axis.

**(d) [4 points]** Submit a MATLAB root-locus plot with the calculated stability crossing labeled and compare it with your hand sketch.

### Problem 3: Geometry of a noncollocated servo (25 points)

Disk-head positioning motivates studying systems whose actuator and sensor are at different locations. Here the supplied model is a **rigid platform on compliant mounts**, an original numerical adaptation of the [course platform model](../../book-notes/modeling-and-dynamics-zeroes_student.md#section-4).

![A rigid platform on symmetric compliant mounts. An upward actuator force u acts at offset plus a from the center of mass. A displacement sensor at offset minus b measures y equals x minus b theta. Center-of-mass translation x is upward and positive rotation theta is counterclockwise.](platform.svg)

*Figure 1. Opposite-side actuation and sensing on the platform; small motions are assumed.*

Let $x$ be center-of-mass translation and $\theta$ be small rotation. Positive coefficients and symmetric support properties decouple translation and rotation. The actuator and sensor offsets are $+a$ and $-b$, respectively, with $a,b>0$. The equations and transfer function are supplied:

$$
m\ddot x+c_x\dot x+k_xx=u,\qquad
J\ddot\theta+c_\theta\dot\theta+k_\theta\theta=au,\qquad y=x-b\theta,
$$

$$
G(s)=\frac{(J-abm)s^2+(c_\theta-abc_x)s+k_\theta-abk_x}
{(ms^2+c_xs+k_x)(Js^2+c_\theta s+k_\theta)}.
$$

In normalized coordinates, use

$$
m=1,\quad c_x=2,\quad k_x=1,\quad c_\theta=2,\quad k_\theta=4,
\quad \beta=ab,
$$

so that

$$
G(s;\beta,J)=\frac{(J-\beta)s^2+(2-2\beta)s+4-\beta}
{(s+1)^2(Js^2+2s+4)}.
$$

Fix the proportional controller at $D_c=3$. In parts (a)–(d) and (f), hold $J=1$ and vary the sensor offset, keeping the body and actuator unchanged. Compare $\beta=0.5,1,1.2,1.5$; the physical comparison interval is $0.5\leq\beta\leq1.5$. Noncollocation permits, but does not require, a right-half-plane zero.

**(a) [4 points]** Find the plant zeros at the four specified values of $\beta$. Explain what happens at $\beta=1$ and why the plant poles remain fixed during this geometry sweep. The simultaneous disappearance of the quadratic and linear numerator terms is specific to these coefficients; do not assume it happens in every geometry sweep.

**(b) [4 points]** Derive the closed-loop characteristic polynomial and isolate $\beta$ to obtain $1+\beta L_{0,\beta}(s)=0$. Retain any negative fixed multiplier. Identify the poles and zeros of this auxiliary model and distinguish them from the physical plant's poles and zeros. The controller remains fixed at 3. For the sign convention, see [Root Locus I, §8](../../book-notes/root-locus-construction_student.md#section-8).

**(c) [5 points]** The following factorization is supplied, with $\mu=\sqrt{3\beta}$:

$$
P(s,\beta)=
\bigl[s^2+(2-\mu)s+4-\mu\bigr]
\bigl[s^2+(2+\mu)s+4+\mu\bigr].
$$

Use the quadratics to find the departure directions from the repeated starting poles, sketch the branches, and find the closed-loop stability boundary and crossing frequency. A quartic Routh calculation is not required. For completing the full mathematical sketch, you may use these later features without deriving them: at $\beta=4$, the complex branches meet the real axis at $s=-1\pm\sqrt3$; thereafter two branches approach $-1$ and the others go to opposite infinities. Concentrate your detailed interpretation on the physical comparison interval.

**(d) [6 points]** Use the quadratic formula to tabulate all four closed-loop roots for $\beta=0.5,1,1.2,1.5$. For each value, report the damping ratio $\zeta=-\Re s/|s|$ of the pair nearest the imaginary axis and classify stability. Explain why a right-half-plane plant zero, poor damping, and closed-loop instability are distinct observations. Include the behavior at $\beta=1$ in your comparison.

**(e) [3 points]** Now hold $\beta=0.5$ and reduce $J$ from 1 to 0.25. Find the new plant zeros and use MATLAB to calculate all closed-loop poles. Compare stability and slow-pair damping with the original case. Explain why a change in damping cannot be attributed to the zero alone. No additional parameter-locus construction is required.

**(f) [3 points]** Submit `rlocus(L0beta)`, labeled as a geometry-parameter locus with $D_c=3$ and $J=1$. Use equal axis scales, mark all four roots at each specified $\beta$, and identify the physical comparison interval.

### Problem 4: Shared PID gain and measurement-noise filtering (35 points)

Use the normalized motor and supplied controller proportions

$$
G(s)=\frac1{s(s+1)},\qquad
D_0(s)=5s+8+\frac4s=\frac{5s^2+8s+4}{s},\qquad
D_c(s)=\lambda D_0(s),\quad\lambda>0.
$$

Thus $(k_P,k_I,k_D)=\lambda(8,4,5)$: one shared multiplier varies all three gains together. Download [ps5_servo.m](ps5_servo.m) into your MATLAB working folder. It requires Control System Toolbox and supplies the simulation, noise record, and response metrics. You do not need to write noise-generation code.

**(a) [7 points]** Derive the characteristic polynomial and Evans form $1+\lambda L_{0,\lambda}(s)=0$. Sketch the gain locus by hand, identifying starts and endpoints, the real-axis portion, the asymptote and centroid, and the departure directions from the double origin. Determine the stable range of $\lambda$. Keep the fixed leading factor 5 in the model passed to MATLAB. Calculating complex-zero arrival angles is optional practice.

**(b) [5 points]** Compare $\lambda=0.25,0.5,1$ using `result = ps5_servo(lambda,Inf)`. Here `Inf` explicitly selects the unfiltered controller. Submit the MATLAB gain locus with all poles at these gains marked, a full step-response comparison, and a compact table of overshoot and 1% settling time. Select a gain satisfying **at most 10% overshoot and at most 4 s settling**. Freeze this gain for all remaining parts.

For the selected unfiltered setting, the supplied measurement noise gives true-output error standard deviation of approximately 0.00222, or 0.222% of the unit setpoint. The next task is to reduce this residual jitter while preserving an acceptable transient response. Add a low-pass filter to the **whole controller**:

$$
F_p(s)=\frac p{s+p},\qquad D_{c,p}(s)=\lambda D_0(s)F_p(s),\qquad p>0.
$$

The physical filter pole is at $-p$; $p$ is a positive parameter in $\mathrm{s}^{-1}$. Its numerator preserves unity DC gain. This filters the whole PID, whereas another common implementation filters only its derivative term.

**(c) [7 points]** Define $a(s)=s^2(s+1)$ and $b(s)=5s^2+8s+4$. Starting with $1+D_{c,p}G=0$, collect terms in $p$ and derive Evans form $1+pL_{0,p}(s)=0$ with $\lambda$ held fixed. Write the resulting characteristic polynomial for your selected gain. Determine the stable range of $p$ and the imaginary-axis crossing. Treat $p=0$ only as a limiting endpoint, not an operating choice.

**(d) [5 points]** Sketch this filter-parameter locus by hand. Identify starts with multiplicities, finite endpoints, real-axis portions, the asymptote and centroid, and departure directions from the origin. Explain what the auxiliary endpoints represent physically. For the selected gain, use the supplied breakaway at $(s,p)\approx(-0.773802,0.111628)$ and break-in at $(-9.063428,18.751541)$ to connect the branches; no hand solution of a break-point quartic is required. Submit `rlocus(L0p)` with these points and your calculated crossing marked. Include a full view and a second view spanning approximately $-1.5\leq\Re s\leq0.5$, $|\Im s|\leq2.5$.

The sensor measures $y_m=y+n_m$, so the controller acts on $e=r-y_m$. The performance error is instead **$e_y=r-y$**, using the true physical output.

![Negative unity feedback with reference r entering the positive control summing junction. The controller Dc,p drives plant G to produce true output y. Measurement noise nm is added to y before the resulting sensor signal ym returns to the negative input. The evaluation error is r minus y.](measurement-noise.svg)

*Figure 2. Measurement noise enters the feedback signal. The performance metric uses the true output.*

**(e) [11 points]** Keep your selected $\lambda$ fixed. Use the helper to compare **$p=8,12,20\ \mathrm{s}^{-1}$** with the unfiltered baseline. The filtered-response limits are **at most 15% overshoot and at most 4 s settling**, measured from each complete noise-free step response. Use the supplied retained interval **$20\leq t<60$ s** for noise statistics. Submit:

- A compact table of overshoot, 1% settling time, true-output error standard deviation, and whether each filter candidate meets the transient limits.
- The complete noise-free step-response comparison and a plot comparing the retained true noisy outputs. Label the retained interval clearly.
- A justification for discarding the first 20 s using **all closed-loop poles and the noise-free tail**. The helper displays the mean error as a bias diagnostic; no separate mean calculation or table column is required.
- A filter choice justified by low output-error standard deviation and the transient limits. A numerical optimizer is not required; justify any preference for additional transient margin.
- One sentence identifying which pole pair changes below the supplied break-in and connecting that change to the larger full-response overshoot.

*Hint:* The pair nearest the imaginary axis need not determine overshoot. Inspect all poles and then the full response. A small mean error does not establish that the transient has decayed, and the 1% transient settling band is not a steady-state noise specification.

### MATLAB plotting and simulation guide

`rlocus` varies a scalar multiplier on the fixed model supplied to it. For a geometry or filter-pole sweep, pass the **derived auxiliary model**. Plotting the physical loop with a fixed geometry or filter would vary controller gain instead. The following scaffolding leaves the model and parameter selection to your analysis.

After defining `L0`, `parameterGrid`, and `selectedValues`, you can plot its MATLAB locus on ordinary axes for easy annotation:

```matlab
R = rlocus(L0,parameterGrid);  % Each column contains all roots at one value.
figure
plot(real(R.'),imag(R.'),'Color',[0.15 0.35 0.65]); hold on
P = pole(L0); Z = zero(L0);
plot(real(P),imag(P),'kx','MarkerSize',9,'LineWidth',1.5)
plot(real(Z),imag(Z),'ko','MarkerSize',9,'LineWidth',1.5)
Q = rlocus(L0,selectedValues);
plot(real(Q(:)),imag(Q(:)),'rs','MarkerSize',7)
xline(0,'k:'); yline(0,'k:'); grid on
xlabel('Real part (s^{-1})'); ylabel('Imaginary part (s^{-1})')
% Add a title naming the parameter and labels for your special points.
% Use axis equal for Problems 1 and 3.
```

Choose a parameter grid fine enough to resolve the bends and include the requested values. You may also use MATLAB's automatic `rlocus(L0)` plot. For Problem 3, use different markers or colors for the four geometries and highlight the interval from 0.5 to 1.5. For Problem 4's second filter view, repeat the plot and set `xlim([-1.5 0.5]); ylim([-2.5 2.5])`.

The helper returns a structure. `result.stepInfo.Overshoot` is a percentage and `result.stepInfo.SettlingTime` is in seconds. `result.errorStd` uses `std(result.outputError(result.keep),0)`. `result.poles`, `result.tailMaxError`, and the noise-free response support your transient-removal explanation. Calling `ps5_servo(lambda,p)` without an output variable also draws diagnostic plots. All runs use the same noise record, a 0.001 s time step, and zero initial states; unstable settings are rejected.

For the filter comparison, first set `lambda` to your selected value, then use:

```matlab
pValues = [Inf 8 12 20];
labels = {'Unfiltered','p = 8','p = 12','p = 20'};
response = cell(size(pValues));
metrics = zeros(numel(pValues),3);
for k = 1:numel(pValues)
    response{k} = ps5_servo(lambda,pValues(k));
    z = response{k};
    metrics(k,:) = [z.stepInfo.Overshoot, z.stepInfo.SettlingTime, z.errorStd];
end
comparison = array2table(metrics,'VariableNames', ...
    {'Overshoot_percent','SettlingTime_s','OutputErrorStd'},'RowNames',labels)
figure
tiledlayout(2,1)
nexttile; hold on
for k = 1:numel(response)
    z = response{k}; plot(z.t,z.yStep,'LineWidth',1.2)
end
xlim([0 10]); yline(1,'k:'); yline(0.99,'k--'); yline(1.01,'k--')
grid on; xlabel('Time (s)'); ylabel('Noise-free true output')
legend(labels,'Location','best')
nexttile; hold on
for k = 1:numel(response)
    z = response{k}; plot(z.t(z.keep),z.y(z.keep))
end
xlim([20 60]); yline(1,'k:'); grid on
xlabel('Time (s)'); ylabel('True noisy output')
title('Retained interval: 20 <= t < 60 s'); legend(labels,'Location','best')
```

Use the same response fields to compare the three unfiltered gains in part (b). For a clearer noise comparison, separate panels with common vertical limits are also acceptable. Submit readable figures, not just the script or its printed metrics.
