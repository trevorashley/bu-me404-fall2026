%=======================================================================
% testSystems.m
%
%   Template file for creating inputs and using blackBox.m
%=======================================================================

%%
close all;clear all;clc
% Let's make a time vector
dt = 0.001;
T = 10;
t = 0:dt:T;

%%
% Let's make a unit step
startLoc = 0.7;        % Should be in [0,1] and is fraction 
u_1 = zeros(size(t));
u_1(floor(startLoc*length(u_1)):end) = 1;

% Throw that input into the blackBox function for model 1
y_1 = blackBox(t,u_1,2,1);

%%
% Now a sinusoidal input
f = 1;                 % Frequency in Hz
u_2 = zeros(size(t));
u_2 = sin(2*pi*f*t);

% Throw that input into the blackBox function for model 1
y_2 = blackBox(t,u_2,2,2);

%% 
u_3 = 2*u_1
y_2 = blackBox(t,u_3,2,3);

err = y_2 - 2*y_1;
figure();
plot(t,err);