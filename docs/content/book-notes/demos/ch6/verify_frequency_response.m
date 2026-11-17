function results = verify_frequency_response()
%VERIFY_FREQUENCY_RESPONSE Independent numerical checks for the owned demo.
% Run this function from this folder, or add this folder to the MATLAB path.
% No figures, Symbolic Math Toolbox, external helpers, or Python are required.
report = frequency_response(false);
s = tf('s');
G1 = 1/(s+1);
t = (0:0.00025:10)';
exact = (10*exp(-t)+sin(10*t)-10*cos(10*t))/101;
ysim = lsim(G1,sin(10*t),t);
firstError = max(abs(ysim-exact));
assert(firstError < 3e-7,'First-order lsim disagreement exceeds discretization tolerance.');
tCoarse = (0:0.0005:10)';
yCoarse = (10*exp(-tCoarse)+sin(10*tCoarse)-10*cos(10*tCoarse))/101;
coarseError = max(abs(lsim(G1,sin(10*tCoarse),tCoarse)-yCoarse));
assert(firstError < coarseError/3,'lsim error did not improve under time refinement.');
% Independent ODE and initial-condition residuals, using the analytic derivative.
dy = (-10*exp(-t)+10*cos(10*t)+100*sin(10*t))/101;
odeResidual = max(abs(dy+exact-sin(10*t)));
assert(odeResidual < 2e-14 && exact(1)==0,'Exact response fails ODE or initial condition.');
checkRounded(report.firstOrder.magnitude,0.0995037);
assert(abs(report.firstOrder.phaseDegrees+84.2894)<.01);
% Capacitor analytical identity; arbitrary-input simulation is inappropriate.
theta = linspace(0,4*pi,1001);
capacitorResidual = max(abs(cos(theta)-sin(theta+pi/2)));
assert(capacitorResidual < 2e-14);
assert(abs(sin(pi/2)-1)<eps && abs(cos(0)-1)<eps);
% Example 6.2: direct complex evaluation, BODE, limits, and source locations.
Dc = (s+1)/(s/10+1);
w = logspace(-1,2,801);
h = (1+1j*w)./(1+.1j*w);
[m,p] = bode(Dc,w);
leadMagnitudeResidual = max(abs(squeeze(m)-abs(h(:))));
leadPhaseResidual = max(abs(squeeze(p)-rad2deg(angle(h(:)))));
assert(leadMagnitudeResidual < 2e-13 && leadPhaseResidual < 2e-12);
assert(abs(dcgain(Dc)-1)<1e-14);
assert(abs(abs(evalfr(Dc,1j*1e8))-10)<1e-10);
assert(abs(angle(evalfr(Dc,1j*1e-10)))<1e-8);
assert(abs(angle(evalfr(Dc,1j*1e10)))<1e-8);
assert(abs(zero(Dc)+1)<1e-13 && abs(pole(Dc)+10)<1e-13);
assert(all(angle(h)>0));
assert(abs(abs(evalfr(Dc,1j*sqrt(10)))-sqrt(10))<1e-13);
checkRounded(rad2deg(angle(evalfr(Dc,1j*sqrt(10)))),54.9032,.01);
% Second-order checks use direct rational evaluation, scalar optimization,
% bracketed roots, and MATLAB bandwidth with the exact half-power dB drop.
zeta = [0.05 .1 .2 .3 .5 .7 .9 1/sqrt(2)];
maxPeakRelativeError = 0; maxBandwidthRelativeError = 0;
maxMatlabBandwidthRelativeError = 0;
for z = zeta
    Tclosed = 1/(s^2+2*z*s+1);
    hf = @(r) 1./(1-r.^2+2j*z*r);
    assert(abs(abs(hf(1))-1/(2*z)) < 1e-13);
    assert(abs(rad2deg(angle(hf(1)))+90) < 1e-12);
    if z < 1/sqrt(2)
        rr = sqrt(1-2*z^2);
        peak = 1/(2*z*sqrt(1-z^2));
        [rNumerical,negativePeak] = fminbnd(@(r) -abs(hf(r)),0,2, ...
            optimset('TolX',1e-12));
        assert(abs(rNumerical-rr) < 2e-6);
        peakError = abs(-negativePeak/peak-1);
        assert(abs(abs(hf(rr))-peak)<2e-13);
        assert(abs(4*rr*(rr^2+2*z^2-1))<1e-13);
    else
        assert(all(diff(abs(hf(linspace(0,3,10001))))<=1e-13));
        peakError = abs(abs(hf(0))-1);
    end
    maxPeakRelativeError = max(maxPeakRelativeError,peakError);
    rb = sqrt(1-2*z^2+sqrt(4*z^4-4*z^2+2));
    rbDirect = fzero(@(r) abs(hf(r))-1/sqrt(2),[0 3]);
    assert(abs(abs(hf(rb))-1/sqrt(2))<2e-13);
    assert(abs(rb^4+(4*z^2-2)*rb^2-1)<2e-13);
    assert(abs(hf(rb+.0001))<1/sqrt(2)); % descending crossing
    maxBandwidthRelativeError = max(maxBandwidthRelativeError,abs(rbDirect/rb-1));
    rbMatlab = bandwidth(Tclosed,-10*log10(2));
    maxMatlabBandwidthRelativeError = max(maxMatlabBandwidthRelativeError,abs(rbMatlab/rb-1));
    % Step comparison independently checks the closed-form expression vs STEP.
    ts = linspace(0,25,5001)'; b = sqrt(1-z^2);
    stepExact = 1-exp(-z*ts).*(cos(b*ts)+z/b*sin(b*ts));
    assert(max(abs(step(Tclosed,ts)-stepExact))<5e-12);
    tp = pi/b;
    atPeak = 1-exp(-z*tp)*(cos(b*tp)+z/b*sin(b*tp));
    assert(abs((atPeak-1)-exp(-pi*z/b))<1e-14);
end
assert(maxPeakRelativeError<1e-10);
assert(maxBandwidthRelativeError<1e-12);
assert(maxMatlabBandwidthRelativeError<.001);
assert(abs(report.secondOrder.halfPowerRatio(end)-1)<1e-14);
checkRounded(report.secondOrder.halfPowerRatio(6),1.010049494);
% A nonunit DC gain must not change a DC-relative bandwidth.
assert(abs(bandwidth(3/(s^2+.6*s+1),-10*log10(2))/ ...
    report.secondOrder.halfPowerRatio(4)-1)<.001);
results = struct('passed',true,'firstOrderLsimError',firstError, ...
    'firstOrderCoarseError',coarseError,'odeResidual',odeResidual, ...
    'capacitorResidual',capacitorResidual,'leadMagnitudeResidual',leadMagnitudeResidual, ...
    'leadPhaseResidualDegrees',leadPhaseResidual, ...
    'peakRelativeError',maxPeakRelativeError, ...
    'halfPowerRelativeError',maxBandwidthRelativeError, ...
    'matlabHalfPowerRelativeError',maxMatlabBandwidthRelativeError);
fprintf('Frequency-response verification passed.\n');
disp(results);
end

function checkRounded(actual,expected,absoluteTolerance)
if nargin < 3
    absoluteTolerance = 0.001*abs(expected); % 0.1% rounded benchmark tolerance
end
assert(abs(actual-expected)<=absoluteTolerance,'Rounded benchmark mismatch.');
end
