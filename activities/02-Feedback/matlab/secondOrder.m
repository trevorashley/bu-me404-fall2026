%=======================================================================
% secondOrder.m
%
%   [e,y,t] = secondOrder(yss,kp,FB,T,seed) shows the response of a second 
%   order system to a given (constant) input in either open or closed loop 
%   mode.
%
%   INPUTS
%       yss: steady state desired and constant input
%       kp: input level (open loop) or P gain (closed loop)
%       FB: determines if in feedback (1) or not (0)
%       T: end time of simulation
%       seed: seed value for RNG or 0 for no particular seed
%
%   OUTPUTS
%       e: final error (a scalar)
%       y: output (a vector of length T)
%       t: vector of times at which output y is given
%=======================================================================
function [e,y,t] = secondOrder(yss,kp,FB,T,seed);

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

if( FB == 1 )
    P = feedback(kp*P,1);
end

%=======================================================================
% Get the step response
%=======================================================================
[y,t] = step(P,T);
if( FB == 1 )   
    y = yss*y;
else
    y = kp*y;
end
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
ylabel('output','fontsize',14);
set(gca,'fontsize',14);