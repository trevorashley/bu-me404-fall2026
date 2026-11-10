function result = ps5_servo(lambda,p)
%PS5_SERVO Simulate the supplied ME404 PS5 servo with measurement noise.
%   RESULT = PS5_SERVO(LAMBDA,P) returns responses and metrics. Use P = Inf
%   for the unfiltered controller. Requires MATLAB and Control System Toolbox.
%   With no output argument, PS5_SERVO also draws a diagnostic figure.
%
%   The physical output is y; the sensor reads y + measurementNoise.
%   outputError = 1 - y, NOT 1 - (y + measurementNoise).
%   stepInfo uses the NOISE-FREE response and the course's 1% settling band.
%   keep selects 20 <= t < 60 s. Every call uses the same measurement noise.
%
%   Useful fields: t, yStep, y, outputError, poles, stepInfo, keep,
%   errorStd, errorMean, tailMaxError, T, measurementNoise.
%   Time is in seconds; signals are normalized. All initial states are zero.

validateattributes(lambda,{'numeric'},{'real','scalar','finite','positive'}, ...
    mfilename,'lambda',1);
validateattributes(p,{'numeric'},{'real','scalar','positive','nonnan'}, ...
    mfilename,'p',2);
lambda = double(lambda);
p = double(p);

% G = 1/[s(s+1)], Dc = lambda*(5s^2+8s+4)/s.
% For finite p, multiply the WHOLE controller by p/(s+p).
% Form the full characteristic polynomial without pole-zero cancellation.
if isinf(p)
    numerator = lambda*[5 8 4];
    denominator = [1 1+5*lambda 8*lambda 4*lambda];
    setting = sprintf('lambda = %.3g, unfiltered',lambda);
else
    numerator = lambda*p*[5 8 4];
    denominator = [1 1+p (1+5*lambda)*p 8*lambda*p 4*p*lambda];
    setting = sprintf('lambda = %.3g, p = %.3g s^{-1}',lambda,p);
end
if any(~isfinite([numerator denominator]))
    error('ps5_servo:InvalidScale','Parameters overflow the model coefficients.');
end
allPoles = roots(denominator);
if any(real(allPoles) >= -1e-10)
    error('ps5_servo:Unstable', ...
        'This setting is unstable or marginally stable. Choose stable parameters.');
end
T = tf(numerator,denominator);

% A private random stream preserves the user's global random-number state.
% This finite-bandwidth fixture is supplied; no noise-generation work is due.
persistent time noise
if isempty(time)
    time = (0:60000)'/1000;
    stream = RandStream('mt19937ar','Seed',40405);
    phase = 2*pi*rand(stream,128,1);
    omega = 2*pi*(128:4:636)'/40;
    amplitude = 0.02*sqrt(2/128);
    noise = zeros(size(time));
    for k = 1:numel(omega)
        noise = noise + amplitude*cos(omega(k)*time + phase(k));
    end
end
t = time;
keep = t >= 20 & t < 60; % Exclude the repeated periodic endpoint.
yStep = step(T,t);
% Both closed-loop output paths are proper, even for the ideal PID.
% Use linear interpolation of the sampled input for every candidate.
yNoise = -lsim(T,noise,t,[],'foh');
y = yStep + yNoise;
outputError = 1-y;
info = stepinfo(yStep,t,1,'SettlingTimeThreshold',0.01, ...
    'RiseTimeLimits',[0.1 0.9]);
tailMaxError = max(abs(1-yStep(keep)));
if tailMaxError > 1e-4
    warning('ps5_servo:TransientRemaining', ...
        ['The noise-free tail is not negligible in the fixed analysis window. ' ...
        'Do not interpret errorStd as a settled noise statistic.']);
end

result = struct('lambda',lambda,'p',p,'label',setting,'T',T, ...
    't',t,'yStep',yStep,'y',y,'outputError',outputError, ...
    'measurementNoise',noise,'poles',allPoles,'stepInfo',info, ...
    'keep',keep,'retainedWindow',[20 60], ...
    'errorStd',std(outputError(keep),0), ...
    'errorMean',mean(outputError(keep)),'tailMaxError',tailMaxError);

fprintf('\n%s\n',setting);
fprintf('All closed-loop poles (s^-1):\n');
disp(allPoles);
fprintf('Noise-free overshoot: %.3f %%\n',info.Overshoot);
fprintf('Noise-free 1%% settling time: %.3f s\n',info.SettlingTime);
fprintf('Noise-free 10-90%% rise time: %.3f s\n',info.RiseTime);
fprintf('Retained window: 20 <= t < 60 s (%d samples)\n',nnz(keep));
fprintf('True-output error standard deviation: %.7f\n',result.errorStd);
fprintf('Mean true-output error (bias diagnostic): %.3g\n',result.errorMean);
fprintf('Maximum noise-free tail error in retained window: %.3g\n',tailMaxError);

if nargout == 0
    figure('Name',setting);
    tiledlayout(2,2,'TileSpacing','compact');
    nexttile;
    plot(t,yStep,'LineWidth',1.2); hold on;
    yline(1,'k:'); yline(0.99,'k--'); yline(1.01,'k--');
    xlim([0 10]); grid on;
    xlabel('Time (s)'); ylabel('True output');
    title('Noise-free step; dashed lines: 1% band');
    nexttile;
    semilogy(t,max(abs(1-yStep),eps),'LineWidth',1.2);
    xline(20,'k--','Retain from 20 s'); grid on;
    xlabel('Time (s)'); ylabel('|1 - y_{step}|');
    title('Noise-free transient check');
    nexttile;
    plot(real(allPoles),imag(allPoles),'x','MarkerSize',9,'LineWidth',1.5);
    xline(0,'k:'); yline(0,'k:'); grid on;
    xlabel('Real part (s^{-1})'); ylabel('Imaginary part (s^{-1})');
    title('All closed-loop poles');
    nexttile;
    plot(t(keep),y(keep)); hold on; yline(1,'k:'); grid on;
    xlabel('Time (s)'); ylabel('True noisy output');
    title('Retained window: 20 <= t < 60 s');
    sgtitle(setting);
end
end
