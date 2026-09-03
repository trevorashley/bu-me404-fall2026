%=======================================================================
% [e,y,t] = secondOrder_good(yss,T,seed).m
%
%   matlab file to show the response of a second order system with a PI
%   controller 
%
%   INPUTS
%       yss: steady state desired
%       T: end time of simulation
%       seed: seed value for RNG or 0 for no particular seed
%
%   OUTPUTS
%       e: final error
%       y: output (a vector of length T)
%       t: vector of times at which output y is given
%=======================================================================
function [e,y,t] = secondOrder(yss,T,seed);

%=======================================================================
% Set the random number generator seed
%=======================================================================
if( seed > 0 )
    rng(seed);
end

%=======================================================================
% Define the system
%=======================================================================
wn = 10 + rand(1);
xi = 0.4 + 0.2*rand(1);
k = 1 + 2*rand(1);
P = k*tf(wn^2,[1 2*xi*wn wn^2]);

%=======================================================================
% Define the controller
%=======================================================================
kp = 3;
ki = 5;
C = tf([kp ki],[1 0]);

Gcl = feedback(C*P,1);

%=======================================================================
% Get the step response
%=======================================================================
[y,t] = step(Gcl,T);
y = yss*y;
e = y(end) - yss;

%=======================================================================
% Plot the response
%=======================================================================
figure(1)
clf
plot(t,y,'linewidth',2);
hold on
plot(t,yss*ones(length(t)),'r','linewidth',2);
legend('y','y_{ss}');
xlabel('time','fontsize',14);
ylabel('in/out','fontsize',14);
set(gca,'fontsize',14);