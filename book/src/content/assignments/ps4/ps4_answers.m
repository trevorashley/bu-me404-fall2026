% ME404 Problem Set 4: MATLAB parts 3(d), 6(g), 7(f), and 10(e).
% Requires MATLAB with Control System Toolbox. Run ps4_answers from MATLAB.
% Rise time is 10% to 90%, and settling time uses a 1% band, as in the course.

s = tf('s');
opts = {'RiseTimeLimits',[0.1 0.9],'SettlingTimeThreshold',0.01};

%% Problem 3(d): specifications of the six transfer functions
H = { 25/(s^2+6*s+25), ...
      25/(s^2+2*s+25), ...
      100/((s+4)*(s^2+6*s+25)), ...
      25*(4-s)/(4*(s^2+6*s+25)), ...
      25*(s+2)/(2*(s^2+6*s+25)), ...
      5/(s+5) };
t3 = (0:0.0005:6)';
fprintf('Problem 3(d): rise time (s), overshoot (%%), 1%% settling time (s)\n');
for i = 1:6
    y = step(H{i}, t3);
    info = stepinfo(y, t3, 1, opts{:});
    fprintf('   H%d: t_r = %.3f  M_p = %5.1f  t_s = %.3f  (min y = %.3f)\n', ...
        i, info.RiseTime, info.Overshoot, info.SettlingTime, min(y));
end
% Expected: H1 0.371/9.5/1.25, H2 0.241/52.7/4.59, H3 0.575/1.9/1.41,
% H4 0.282/12.9/1.84 (undershoot to -0.37), H5 0.079/76.3/1.56, H6 0.439/0/0.92.

%% Problem 6(g): DC motor with rate feedback and integral action
a1 = 50; b0 = 100; c0 = 5;
K = 50; TD = 0.01;                        % poles at -50 +- 50j
Tref = b0*K/(s^2 + (a1 + b0*K*TD)*s + b0*K);
t6 = (0:0.00005:0.15)';
y6 = step(Tref, t6);
info6 = stepinfo(y6, t6, 1, opts{:});
fprintf('Problem 6(g): M_p = %.2f%%, t_s = %.4f s, t_r = %.4f s\n', ...
    info6.Overshoot, info6.SettlingTime, info6.RiseTime);   % 4.32%, 0.093 s
figure('Name','Problem 6: reference step');
plot(t6, y6, 'LineWidth', 1.5); hold on; grid on
yline(1,'--'); yline(0.99,':'); yline(1.01,':');
xline(info6.SettlingTime, ':');
xlabel('Time (s)'); ylabel('\theta_m (rad)');
title('Unit-step reference response, K = 50, T_D = 0.01 s');

kI = 500;                                  % one-tenth of the Routh limit 5000
Tw_noI = c0/(s^2 + (a1 + b0*K*TD)*s + b0*K);
Tw_I   = c0*s/(s^3 + (a1 + b0*K*TD)*s^2 + b0*K*s + b0*kI);
t6w = (0:0.0001:0.5)';
figure('Name','Problem 6: load-torque step');
plot(t6w, step(Tw_noI, t6w), t6w, step(Tw_I, t6w), 'LineWidth', 1.5); grid on
yline(c0/(b0*K), '--');
legend('without integral action', 'with k_I = 500', 'Location', 'east');
xlabel('Time (s)'); ylabel('\theta_m (rad)');
title('Response to a unit-step load torque');
fprintf('   steady state without integral: %.4g rad (predicted %.4g)\n', ...
    dcgain(Tw_noI), c0/(b0*K));
fprintf('   steady state with integral:    %.4g rad (predicted 0)\n', dcgain(Tw_I));
disp('   closed-loop poles with integral action:'); disp(pole(Tw_I));
% Expected poles: -12.90, -43.55 +- 44.50j.

%% Problem 7(f): Ziegler-Nichols designs for G = 1/(s(s+1)(s+4))
G7 = 1/(s*(s+1)*(s+4));
Ku = 20; Pu = pi;
designs = struct('name', {'P','PI','PID'}, ...
    'Dc', { 0.5*Ku, ...
            0.45*Ku*(1 + 1/((Pu/1.2)*s)), ...
            0.6*Ku*(1 + 1/((Pu/2)*s) + (Pu/8)*s) });
t7 = (0:0.005:40)';      % plotting window
t7long = (0:0.01:200)';   % the PI design settles to 1% only after about 157 s
figure('Name','Problem 7: Ziegler-Nichols designs'); hold on; grid on
for i = 1:3
    T7 = feedback(designs(i).Dc*G7, 1);
    y7 = step(T7, t7);
    info7 = stepinfo(step(T7, t7long), t7long, 1, opts{:});
    fprintf('Problem 7(f): %-3s overshoot = %.1f%%, settling = %.1f s\n', ...
        designs(i).name, info7.Overshoot, info7.SettlingTime);
    plot(t7, y7, 'LineWidth', 1.5, 'DisplayName', designs(i).name);
    fprintf('   closed-loop poles:'); fprintf(' %s', num2str(pole(T7).', '%.3f ')); fprintf('\n');
end
yline(1, '--', 'HandleVisibility', 'off');
xlabel('Time (s)'); ylabel('y(t)'); legend('show');
% Expected: P 62%, PI 102% (poles -0.029 +- 1.341j, barely stable), PID 61%.

%% Problem 10(e): square wave through 1/(0.1 s + 1)
G10 = 1/(0.1*s + 1);
t10 = (0:0.0001:1.5)';
u10 = double(mod(t10, pi/5) < pi/10)*2 - 1;    % +-1 square wave, omega_0 = 10 rad/s
y10 = lsim(G10, u10, t10);
w0 = 10; yss = zeros(size(t10));
for k = [1 3 5]
    ck = 2/(1j*k*pi);
    dk = ck*evalfr(G10, 1j*k*w0);
    yss = yss + 2*real(dk*exp(1j*k*w0*t10));   % pairs +k and -k
end
figure('Name','Problem 10: square wave through the filter');
plot(t10, u10, 'Color', [0.75 0.75 0.75]); hold on; grid on
plot(t10, y10, 'LineWidth', 1.5);
plot(t10, yss, '--', 'LineWidth', 1.2);
legend('square-wave input', 'simulated output', 'steady state, harmonics 1, 3, 5', ...
    'Location', 'southeast');
xlabel('Time (s)'); ylabel('u(t), y(t)');
title('Square wave through 1/(0.1s + 1)');
fprintf('Problem 10(e): output harmonic amplitudes: %s\n', ...
    num2str(4./([1 3 5]*pi).*squeeze(abs(freqresp(G10, [10 30 50]))).', '%.4f '));
% Expected: 0.900, 0.134, 0.050.
