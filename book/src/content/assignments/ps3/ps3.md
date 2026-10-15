# ME404: Dynamics and Control of Mechanical Systems, Fall 2026
## Problem Set \#3: Dynamic Response, Stability, and Feedback

**Due Date**: 27 October, 2026 (3:30 PM in-person or 11:59 PM electronically)

**AI Policy**: AI may be used for MATLAB coding and plotting. You may also ask AI for hints on how to get started on a problem, but you cannot ask the AI to solve the problem for you.

For Problems 1 and 2, assume zero initial conditions and use a unit-step reference or input when evaluating response specifications. Measure rise time from 10% to 90% of the final output, overshoot relative to the final output, and settling time using a 1% band about the final output, consistent with the [Time-Domain Specifications notes](../../book-notes/time-domain-specs_student.md).

### Problem \#1: DC Motor Position Control

*Source: adapted from Franklin, Powell, and Emami-Naeini, Feedback Control of Dynamic Systems, 8th ed., Problem 3.34 (7th ed., Problem 3.35).*

The equation of motion for a DC motor is
$$
J_m\ddot{\theta}_m
+\left(b+\frac{K_tK_e}{R_a}\right)\dot{\theta}_m
=\frac{K_t}{R_a}v_a,
$$
where $v_a$ is the applied armature voltage and $\theta_m$ is the motor shaft angle. Armature inductance is neglected. Assume
$$
\begin{aligned}
J_m &= 0.01\ \mathrm{kg\cdot m^2},\\
b &= 0.001\ \mathrm{N\cdot m\cdot s},\\
K_e &= 0.02\ \mathrm{V\cdot s},\\
K_t &= 0.02\ \mathrm{N\cdot m/A},\\
R_a &= 10\ \Omega.
\end{aligned}
$$
Angles are measured in radians.

**(a)** Find the transfer function between the applied voltage $v_a$ and the motor speed $\dot{\theta}_m$.

**(b)** What is the steady-state speed of the motor after a voltage $v_a=10\ \mathrm{V}$ has been applied?

**(c)** Find the transfer function between the applied voltage $v_a$ and the shaft angle $\theta_m$.

**(d)** Suppose feedback is added to the system in part (c) so it becomes a position servo device such that the applied voltage is given by
$$
v_a=K(\theta_r-\theta_m),
$$
where $\theta_r$ is the reference angle and $K>0$ is the feedback gain. Find the transfer function between $\theta_r$ and $\theta_m$.

**(e)** Find the upper bound on $K$ required for an overshoot $M_p<20\%$.

**(f)** What values of $K$ will provide a rise time of less than $4\ \mathrm{s}$? Ignore the $M_p$ constraint. If you use a rise-time approximation, identify it and treat the resulting gain range as an estimate.

**(g)** Use MATLAB to plot the step response of the position servo system for values of the gain $K=0.5$, $1$, and $2$. Find the overshoot and rise time for each of the three step responses by examining your plots. Are the plots consistent with your calculations in parts (e) and (f)?

### Problem \#2: Comparing Time-Response Specifications

*Source: adapted from Franklin, Powell, and Emami-Naeini, Feedback Control of Dynamic Systems, 8th ed., Problem 3.45 (7th ed., Problem 3.46).*

Five transfer functions are given as follows:
$$
\begin{aligned}
G_1(s)&=\frac{40}{s^2+4s+40},\\[6pt]
G_2(s)&=\frac{40}{(s+1)(s^2+4s+40)},\\[6pt]
G_3(s)&=\frac{120}{(s+3)(s^2+4s+40)},\\[6pt]
G_4(s)&=\frac{20(s+2)}{(s+1)(s^2+4s+40)},\\[6pt]
G_5(s)&=\frac{\left(\dfrac{36040}{401}\right)(s^2+s+401)}{(s^2+4s+40)(s^2+s+901)}.
\end{aligned}
$$

**(a)** Which transfer function(s) will meet an overshoot specification of $M_p\le5\%$?

**(b)** Which transfer function(s) will meet a rise-time specification of $t_r\le0.5\ \mathrm{s}$?

**(c)** Which transfer function(s) will meet a settling-time specification of $t_s\le2.5\ \mathrm{s}$?

### Problem \#3: Magnetic Levitation Stability

*Source: adapted from Franklin, Powell, and Emami-Naeini, Feedback Control of Dynamic Systems, 8th ed., Problem 3.56 (7th ed., Problem 3.57).*

Consider the closed-loop magnetic levitation system shown below. Determine the conditions on the system parameters $(a,K,z,p,K_0)$ to guarantee closed-loop system stability.

![Magnetic levitation system with unity negative feedback. The reference R enters the positive input of a summing junction, and the output Y enters its negative input. The error e passes through the controller K(s+z)/(s+p), producing u, which drives the plant K_0/(s^2-a^2).](magnetic-levitation.svg)

### Problem \#4: Feedback and Sensitivity

*Source: adapted from Franklin, Powell, and Emami-Naeini, Feedback Control of Dynamic Systems, 8th ed., Problem 4.2 (7th ed., Problem 4.2).*

We define the sensitivity of a transfer function $G$ to one of its parameters $K$ as the ratio of the infinitesimal percent change in $G$ to the infinitesimal percent change in $K$:
$$
S_K^G
=\frac{dG/G}{dK/K}
=\frac{d\ln|G|}{d\ln K}
=\frac{K}{G}\frac{dG}{dK}.
$$
Here $K>0$; the absolute value in $\ln|G|$ allows us to use the logarithmic form for a negative real gain.

The purpose of this problem is to examine the effect of feedback on sensitivity. In particular, we would like to compare the three topologies shown below for connecting three amplifier stages, each with a gain of $-K$, into a single amplifier with a gain of $-10$.

![Three amplifier topologies: (a) an input gain beta_1 followed by three stages of gain -K; (b) three cascaded stages of gain -K, each with a local feedback path through beta_2 entering a positive summing input; (c) three stages of gain -K within a single feedback loop through beta_3 entering a positive summing input.](amplifier-topologies.svg)

**(a)** For each topology, compute $\beta_i$ so that if $K=10$, then $Y=-10R$.

**(b)** For each topology, compute $S_K^G$ when $G=Y/R$. Use the respective $\beta_i$ values found in part (a), holding them fixed as $K$ varies, and evaluate the sensitivities at $K=10$. The common parameter $K$ varies in all three amplifier stages together. Which case is the least sensitive?

**(c)** Compute the sensitivities of the systems in diagrams (b) and (c) to $\beta_2$ and $\beta_3$, respectively, at the nominal values from part (a), with $K=10$. In diagram (b), the common parameter $\beta_2$ varies in all three feedback paths together. Using your results, comment on the relative need for precision in sensors and actuators.
