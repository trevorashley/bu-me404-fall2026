% ME404 Part IV: MATLAB companion to the four root-locus lectures.
% Requires Control System Toolbox. Run this script from any directory.
% All feedback() calls below use its default negative-feedback convention.
clear; close all; clc;
s = tf('s');
G = 1/(s*(s+1));
Gcubic = 1/(s*(s+2)*(s+4));

% Lecture I: sketch the endpoints, breakaway points, and asymptotes first.
figure('Name','Root-locus construction: construction');
subplot(1,2,1); rlocus(G); grid on; title('Motor');
subplot(1,2,2); rlocus(Gcubic); grid on; title('Cubic');
disp('Cubic crossing at K=48:'); disp(roots([1 6 8 48]));

% Lecture II: the damping-ray calculation sets one gain for every root.
K = 224/27;
Tcubic = feedback(K*Gcubic,1);
Tpair = (16/9)/(s^2+(4/3)*s+16/9);
disp('Root-locus gain design selected cubic poles:'); disp(pole(Tcubic));
fprintf('Kv = %.8f, unit-ramp steady error = %.8f\n',K/8,8/K);
figure('Name','Root-locus gain design: full response'); step(Tcubic,Tpair); grid on;
legend('Complete cubic','Pair only');
disp(stepinfo(Tcubic,'SettlingTimeThreshold',0.01));

% Lecture III: exact PD and lead designs plus the Franklin iteration.
Dpd = 3*s+8; Dlead = 20*(s+2)/(s+8);
Tpd = feedback(Dpd*G,1); Tlead = feedback(Dlead*G,1);
Trate = 8/(s^2+4*s+8);  % Derivative on output, not reference.
figure('Name','Lead and PD design: PD and lead'); step(Tpd,Tlead,Trate); grid on;
legend('Forward PD','Lead','Rate feedback');
disp('Lead poles:'); disp(pole(Tlead));
Dinitial = 70*(s+2)/(s+10); Dfinal = 91*(s+2)/(s+13);
figure('Name','Lead and PD design: Franklin Example 5.11');
step(feedback(Dinitial*G,1),feedback(Dfinal*G,1)); grid on;
legend('Initial','Revised');
disp('Franklin revised metrics:'); disp(stepinfo(feedback(Dfinal*G,1),'SettlingTimeThreshold',0.01));
% Do not attempt step(feedback(Dpd,G)): ideal PD requires an impulse.
figure('Name','Lead and PD design: lead actuator command'); step(feedback(Dlead,G)); grid on;

% Lecture IV: long horizons are needed for ramp and disturbance comparisons.
Dlag = (s+0.01)/(s+0.002); Dpi = (s+0.01)/s;
D = {1,Dlag,Dpi}; names = {'P','Lag','PI'};
t = (0:0.02:1000)';
figure('Name','Lag and PI design: reference, ramp error, disturbance');
for i = 1:3
    T = feedback(D{i}*G,1);
    S = feedback(1,D{i}*G);
    GS = feedback(G,D{i});
    subplot(1,3,1); hold on; plot(t,step(T,t),'DisplayName',names{i});
    subplot(1,3,2); hold on; plot(t,lsim(S,t,t),'DisplayName',names{i});
    subplot(1,3,3); hold on; plot(t,step(GS,t),'DisplayName',names{i});
end
subplot(1,3,1); xlim([0 25]); title('Reference step'); ylabel('Output');
subplot(1,3,2); xlim([0 600]); title('Unit-ramp error'); ylabel('Error');
subplot(1,3,3); xlim([0 600]); title('Plant-input step disturbance'); ylabel('Output');
for i=1:3
    subplot(1,3,i); xlabel('Time [s]'); legend('show'); grid on;
end

% Extensions: combined compensator and sinusoidal notch attenuation.
Dcombined = Dfinal*(s+0.05)/(s+0.01);
disp('Lead-lag poles:'); disp(pole(feedback(Dcombined*G,1)));
omega = linspace(5,15,2000); sj = 1j*omega;
notch = (sj.^2+0.6*sj+100)./(sj.^2+6*sj+100);
figure('Name','Extension: notch detuning'); plot(omega,abs(notch)); grid on;
xlabel('Sinusoidal frequency [rad/s]'); ylabel('Amplitude ratio');
title('Filter illustration; full plant stability still needs checking');
