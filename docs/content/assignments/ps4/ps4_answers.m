% ME404 Problem Set 4: answer-key calculations and step-response checks.
% Requires MATLAB with Control System Toolbox. Run ps4_answers from MATLAB.

s = tf('s');

%% Problem 1, Part A: zeta = 0.5, a = 0.5, K = 2, b = 0
charA = [1 1 3 1];                      % s^3 + 2 zeta s^2 + (1+K) s + K a
disp('Problem 1A: closed-loop poles for zeta=0.5, a=0.5, K=2');
disp(roots(charA));
fprintf('Routh s^1 entry: %.4f (positive means stable); K_v = %.4f\n', ...
    (charA(2)*charA(3)-charA(4))/charA(2), 2*0.5);

%% Problem 1, Part B: satellite
G = 1/s^2; Dc = 10*(s+2)/(s+5); L = minreal(G*Dc);
charB = [1 5 10 20];
disp('Problem 1B: closed-loop poles');
disp(roots(charB));
Ka = dcgain(minreal(s^2*L));
Tw = minreal(-feedback(G,Dc));          % E/W = -G/(1+G Dc)
fprintf('K_a = %.4f; E/W at s=0: %.4f; unit-step torque error %.4f\n', ...
    Ka, dcgain(Tw), dcgain(Tw));

%% Problem 2: two feedback systems
K0 = 1; K1 = 1; K2 = 4/3; K3 = 3;
plant = @(k0) k0/(4*s+1);
Ta = feedback(K1/s*plant(K0),1);
Tb = K2*feedback(K3*plant(K0),1);
Ea = 1-Ta; Eb = 1-Tb;
fprintf('Problem 2 nominal: step errors %.4g, %.4g; ramp errors %.4f, %.4f\n', ...
    dcgain(Ea), dcgain(Eb), dcgain(minreal(Ea/s)), dcgain(minreal(Eb/s)));
dK = 0.1;
TaP = feedback(K1/s*plant(K0+dK),1);
TbP = K2*feedback(K3*plant(K0+dK),1);
fprintf('Problem 2 perturbed (K0=1.1): step errors %.4f, %.4f (expected 0 and -1/43 = %.4f)\n', ...
    1-dcgain(TaP), 1-dcgain(TbP), -1/43);
t2 = (0:0.001:60)';
ia = stepinfo(step(Ta,t2),t2,1,'SettlingTimeThreshold',0.01);
ib = stepinfo(step(Tb,t2),t2,1,'SettlingTimeThreshold',0.01);
fprintf('Problem 2 (a): poles %s; overshoot %.2f%%, 1%% settling %.2f s\n', ...
    mat2str(pole(Ta),4), ia.Overshoot, ia.SettlingTime);
fprintf('Problem 2 (b): pole %s; overshoot %.2f%%, 1%% settling %.3f s\n', ...
    mat2str(pole(Tb),4), ib.Overshoot, ib.SettlingTime);
figure('Name','Problem 2'); hold on
step(Ta,TaP,Tb,TbP,40); grid on
legend('(a) nominal','(a) K_0 = 1.1','(b) nominal','(b) K_0 = 1.1','Location','southeast');

%% Problem 3: DC motor with rate feedback and integral action
a1 = 65; b0 = 200; c0 = 10;
fprintf('Problem 3(b): open-loop speed at 100 V = %.2f rpm\n', b0*100/a1*60/(2*pi));
zetaMin = log(1/0.17)/sqrt(pi^2+log(1/0.17)^2);
fprintf('Problem 3(c): zeta_min = %.4f, sigma_min = %.1f 1/s\n', zetaMin, 4.6/0.05);
K = 200; TD = 0.003375; kI = 4000;
den2 = [1 a1+b0*K*TD b0*K];
Tr  = tf(b0*K, den2);                   % reference to angle
Tw  = tf(c0, den2);                     % torque to angle, no integral
TwI = tf([c0 0], [1 a1+b0*K*TD b0*K b0*kI]);  % torque to angle, with integral
disp('Problem 3(c): closed-loop poles');
disp(pole(Tr));
t = (0:1e-5:0.2)';
info = stepinfo(step(Tr,t),t,1,'SettlingTimeThreshold',0.01);
fprintf('Problem 3(g): overshoot %.4f%% (predicted %.4f%%), peak time %.5f s, 1%% settling %.5f s\n', ...
    info.Overshoot, 100*exp(-pi/sqrt(3)), info.PeakTime, info.SettlingTime);
fprintf('Problem 3(d): K_v = %.1f 1/s, ramp error %.4f\n', b0*K/(a1+b0*K*TD), (a1+b0*K*TD)/(b0*K));
fprintf('Problem 3(e): step-torque error = %.3e rad (predicted %.3e)\n', -dcgain(Tw), -c0/(b0*K));
fprintf('Problem 3(f): Routh s^1 entry 40000 - kI = %.0f > 0; poles with kI = %d:\n', 40000-kI, kI);
disp(pole(TwI));
tI = (0:1e-5:0.5)';
yI = step(TwI,tI);
fprintf('Problem 3(f): step-torque error with integral = %.3e rad; peak deviation %.3e rad\n', ...
    -yI(end), max(yI));
figure('Name','Problem 3: reference step'); hold on
y = step(Tr,t);
plot(t,y); yline(1,'--'); yline(0.99,':'); yline(1.01,':');
xline(info.SettlingTime,':'); xlim([0 0.08]); grid on
xlabel('Time (s)'); ylabel('Shaft angle (rad)');
figure('Name','Problem 3: load-torque step'); hold on
plot(t*1e3,step(Tw,t)*1e3,'DisplayName','P + rate feedback');
plot(tI*1e3,yI*1e3,'DisplayName','with integral action');
yline(0.25,'--','HandleVisibility','off'); xlim([0 200]); grid on
xlabel('Time (ms)'); ylabel('Shaft angle (mrad)'); legend('show');
