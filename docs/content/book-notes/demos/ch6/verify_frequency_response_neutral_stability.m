function results = verify_frequency_response_neutral_stability()
%VERIFY_FREQUENCY_RESPONSE_NEUTRAL_STABILITY Check the FPE cubic independently.
cases = frequency_response_neutral_stability(false);
assert(isequal([cases.gain],[0.1 2 10]));
expected = {[-1.27955689;-.58739443;-.13304868], [-2;1i;-1i], ...
    [-2.86746002;.43373001+1.81639347i;.43373001-1.81639347i]};
tol = 1e-9;
for k = 1:numel(cases)
    c = cases(k);
    q = [1 2 1 c.gain];
    p = roots(q);
    % Compare unordered distinct sets and also check the polynomial residual.
    dist = abs(p-c.poles.');
    assert(max(min(dist,[],2)) < tol && max(abs(polyval(q,c.poles))) < tol);
    assert(max(min(abs(p-expected{k}.'),[],2)) < 1e-7);
    results.rhpCount(k) = sum(real(p)>tol);
    results.axisCount(k) = sum(abs(real(p))<tol);
    assert(abs(c.loopAtOne+c.gain/2) < tol);
    margins = allmargin(tf(c.gain,[1 2 1 0]));
    phaseCrossover = margins.GMFrequency;
    gainMargin = margins.GainMargin;
    assert(abs(phaseCrossover-1)<1e-3 && abs(gainMargin*c.gain/2-1)<1e-3);
    results.magnitudeDB(k) = 20*log10(abs(c.loopAtOne));
end
assert(isequal(results.rhpCount,[0 0 2]) && isequal(results.axisCount,[0 2 0]));
assert(sum(real(roots([1 2 1 -1]))>tol)==1 && any(roots([1 2 1 0])==0));
assert(abs(cases(2).loopAtOne+1)<tol);
t = cases(2).time;
exact = 1-exp(-2*t)/5-(4*cos(t)+2*sin(t))/5;
results.neutralStepMaxError = max(abs(cases(2).step-exact));
assert(results.neutralStepMaxError < tol);
end
