function results = verify_frequency_response_steady_state_errors()
%VERIFY_FREQUENCY_RESPONSE_STEADY_STATE_ERRORS Independent numerical checks.
% Does not call the demonstration or export figures.
s = tf('s'); L = tf(10,[1 1 0]);
T = feedback(L,1); S = feedback(1,L);
pExpected = [-.5+1i*sqrt(39)/2;-.5-1i*sqrt(39)/2];
pActual = pole(T);
results.poleResidual = max(abs(polyval([1 1 10],pActual)));
results.poleDifference = max(abs(sort(imag(pActual))-sort(imag(pExpected))));
assert(all(real(pActual)<0) && results.poleResidual<1e-12 && results.poleDifference<1e-12);
results.Kv = dcgain(minreal(s*L));
assert(abs(results.Kv-10)<1e-12 && abs(dcgain(S))<1e-12);
w = [.01 1]; z = 1i*w;
results.exactReadings = abs(10./(z.*(z+1)));
results.asymptoteReadings = 10./w;
response = reshape(freqresp(L,w),1,[]);
results.frequencyResidual = max(abs(response-10./(z.*(z+1))));
assert(results.frequencyResidual<1e-10);
assert(abs(results.exactReadings(1)-999.9500037496876)<1e-9);
assert(abs(results.exactReadings(2)-sqrt(50))<1e-12);
assert(isequal(results.asymptoteReadings,[1000 10]));
% Partial-fraction identity is checked away from its poles.
z = [.3+.7i,2+3i,-.2+2i];
results.partialFractionResidual = max(abs((z+1)./(z.*(z.^2+z+10))-(.1./z+(-.1*z+.9)./(z.^2+z+10))));
assert(results.partialFractionResidual<1e-12);
t = (0:.002:30)'; wd = sqrt(39)/2;
exact = .1+exp(-t/2).*(-.1*cos(wd*t)+.95/wd*sin(wd*t));
computed = lsim(S,t,t);
results.maxRampDifference = max(abs(computed-exact));
results.finalError = computed(end);
results.finalDifference = abs(computed(end)-.1);
results.finalTransientBound = exp(-15)*hypot(.1,.95/wd);
assert(results.maxRampDifference<1e-9);
assert(results.finalDifference<results.finalTransientBound+1e-11);
assert(abs(exact(1))<1e-14);
% Check the final second rather than accepting a lucky endpoint crossing.
results.tailDifference = max(abs(computed(t>=29)-.1));
assert(results.tailDifference<2e-7);
results.passed = true;
disp(results)
end
