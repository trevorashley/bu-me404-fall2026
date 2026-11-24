function results = verify_frequency_response_nyquist()
%VERIFY_FREQUENCY_RESPONSE_NYQUIST Compare sampled windings with analytic models.
r = frequency_response_nyquist(false);
expectedN = {[0 0 1],[0 2 1],[1 -1 0],[0 0]};
expectedP = [0 0 1 0];
expectedK = {[1 -.5 -2],[.5 4 -1],[.5 2 -1],[.5 2]};
w = logspace(-2,2,45);
results = table();
for i = 1:4
    c = r.examples{i};
    assert(isequal(c.gains,expectedK{i}));
    P = sum(real(pole(c.model))>1e-9);
    assert(P==expectedP(i));
    finite = isfinite(c.frequency);
    testW = [w c.frequency(finite)];
    x = testW.^2;
    switch i
        case 1
            g = (1-x-2i*testW)./(1+x).^2;
        case 2
            g = (-2+1i*(x-1)./testW)./(1+x).^2;
        case 3
            g = (-110+10i*(10-x)./testW)./(x+100);
        case 4
            g = (x-3).*(x-1+2i*testW)./(1+x).^2;
    end
    direct = arrayfun(@(v) evalfr(c.model,1i*v),testW);
    assert(max(abs(g-direct)./(1+abs(g)))<1e-12);
    assert(max(abs(c.samples(finite)-direct(numel(w)+1:end)))<1e-12);
    % Reconstruct using the exact magnitude and phase data shown on the plots.
    magnitude = c.markerMagnitude;
    phase = c.markerPhase;
    valid = isfinite(phase);
    polar = zeros(size(phase));
    polar(valid) = magnitude(valid).*exp(1i*deg2rad(phase(valid)));
    assert(all(magnitude(~valid)==0) && max(abs(c.samples(finite)-polar))<1e-12);
    if i==4
        assert(isequal(find(~valid),3) && c.samples(end)==1);
        assert(abs(evalfr(c.model,1i*1e9)-1)<3e-9);
    elseif i==1
        assert(c.samples(end)==0);
    end
    for j = 1:numel(c.gains)
        K = c.gains(j);
        switch i
            case 1
                q = [1 2 1+K];
            case 2
                q = [1 2 1 K];
            case 3
                q = [1 10*K-10 10*K];
            case 4
                q = [1+K 2 1+3*K];
        end
        poles = roots(q);
        assert(all(abs(real(poles))>1e-9));
        Z = sum(real(poles)>0);
        checks = c.checks(j,:);
        counts = [checks.N]; clearance = min([checks.clearance]);
        assert(max(abs(counts-expectedN{i}(j)))<1e-8 && Z==P+round(counts(end)));
        assert(clearance>.01 && max([checks.closure])<1e-10 && max([checks.maxAngleStep])<pi/4);
        row = table(7+i,K,P,counts(1),counts(2),counts(3),Z,clearance, ...
            'VariableNames',{'ExampleSuffix','Gain','P','N1','N2','N3','Z','MinClearance'});
        results = [results; row]; %#ok<AGROW>
    end
end
% Direct checks at boundaries, where ordinary winding is undefined.
assert(all(roots([1 2 1])==-1) && any(roots([1 2 0])==0));
assert(abs(evalfr(r.examples{1}.model,0)-1)<1e-12);
for i = [2 3]
    wc = [1 sqrt(10)]; criticalK = [2 1]; k = i-1;
    G = r.examples{i}.model;
    assert(abs(1+criticalK(k)*evalfr(G,1i*wc(k)))<1e-12);
    margins = allmargin(G);
    [distance,j] = min(abs(margins.GMFrequency-wc(k)));
    assert(distance<1e-3 && abs(margins.GainMargin(j)-criticalK(k))<1e-3);
end
end
