function results = verify_frequency_response_stability_margins()
%VERIFY_FREQUENCY_RESPONSE_STABILITY_MARGINS Compare independent margin and pole calculations.
r = frequency_response_stability_margins(false);
s = tf('s');
G = 1/(s*(1+s)^2);
for k = 1:height(r.cubic)
    row = r.cubic(k,:); L = row.Gain*G;
    checkMargins(L,row.Wc,row.PM,1,row.GM);
    p = roots([1 2 1 row.Gain]);
    assert(sum(real(p)>1e-8)==2*(row.Gain>2));
    assert(sum(abs(real(p))<1e-8)==2*(row.Gain==2));
end
assert(abs(r.designK-.181809199)<1e-8);
checkMargins(r.designK*G,r.designWc,70,1,2/r.designK);
assert(abs(r.cubicWv-sqrt((3+sqrt(41))/16))<1e-7);
assert(abs(r.cubicDv-abs(1+evalfr(G,1i*r.cubicWv)))<1e-12);

% The exact no-zero formulas can be checked with wn = 1 by frequency scaling.
for z = [.2 .5 1/sqrt(2) .9 1 1.15]
    L = 1/(s*(s+2*z)); T = feedback(L,1);
    x = sqrt(sqrt(1+4*z^4)-2*z^2);
    [gm,pm,~,wcp] = margin(L);
    assert(isinf(gm) && abs(wcp-x)/x<1e-3 && abs(pm-atand(2*z/x))<.01);
    assert(abs(abs(evalfr(L,1i*x))-1)<1e-12);
    if z<1
        tp = pi/sqrt(1-z^2);
        y = step(T,linspace(0,tp,401));
        assert(abs(y(end)-1-exp(-pi*z/sqrt(1-z^2)))<1e-9);
    end
    if z<1/sqrt(2)
        wr = sqrt(1-2*z^2);
        assert(abs(abs(evalfr(T,1i*wr))-1/(2*z*sqrt(1-z^2)))<1e-10);
    else
        assert(abs(dcgain(T)-1)<1e-12 && abs(evalfr(T,1i*.1))<1);
    end
end

A = r.ex612; B = r.ex613;
checkMargins(A.model,A.wc,A.pm,A.wp,A.gm);
assert(abs(A.wc-11.923603)<1e-6 && abs(A.pm-10.0287)<1e-4);
assert(abs(A.gm-5/7)<1e-12 && abs(1+A.gm*evalfr(A.model,10i))<1e-12);
for K = [4 5 7]
    p = roots([1 K 20*K 100*K]); T = feedback((K/7)*A.model,1);
    checkPoles(p,pole(T));
    assert(sum(real(p)>1e-8)==2*(K<5) && sum(abs(real(p))<1e-8)==2*(K==5));
end
checkMargins(B.model,B.wc,B.pm,B.wp,B.gm);
assert(max(abs(B.wc-[.743648175;9.451119214;9.838826013]))<1e-7);
assert(max(abs(B.pm-[36.736829;72.179462;39.110025]))<1e-5);
assert(abs(B.wp-10.343107969)<1e-7 && abs(B.gm-1.262453499)<1e-8);
p = roots([4 16 748 1804 34148 15385 14705]);
checkPoles(p,B.poles);
assert(all(real(p)<0) && all(real(A.poles)<0));
assert(max(abs([A.turns B.turns]))<1e-8);
% Independent global peak of the reciprocal distance for the stable feedback loop.
[peak,wv] = getPeakGain(feedback(1,B.model),1e-8);
assert(abs(1/peak-B.dv)<1e-7 && abs(wv-B.wv)<1e-3);
assert(abs(B.wv-10.27273378)<1e-6 && abs(B.dv-.187205714)<1e-8);
results.gainCrossings = B.wc;
results.phaseMargins = B.pm;
results.vectorMinimum = [B.wv B.dv];
results.winding = [A.turns;B.turns];
end

function checkPoles(p,other)
assert(numel(p)==numel(other) && max(min(abs(p(:)-other(:).'),[],2))<1e-7);
end

function checkMargins(L,wc,pm,wp,gm)
z = arrayfun(@(w) evalfr(L,1i*w),wc);
assert(max(abs(abs(z)-1))<1e-8);
% Rotation through the reported phase margin must land on the critical point.
assert(max(abs(z.*exp(-1i*deg2rad(pm))+1))<1e-8);
v = evalfr(L,1i*wp);
assert(real(v)<0 && abs(imag(v))<1e-8 && abs(1+gm*v)<1e-8);
all = allmargin(L);
[toolW,order] = sort(all.PMFrequency(:));
assert(numel(toolW)==numel(wc) && max(abs(toolW-wc(:))./wc(:))<1e-3);
toolPM = all.PhaseMargin(:);
% On a steep resonance, compare the toolbox phase at its own frequency.
toolZ = arrayfun(@(w) evalfr(L,1i*w),toolW);
phaseResidual = rad2deg(angle(-toolZ.*exp(-1i*deg2rad(toolPM(order)))));
assert(max(abs(phaseResidual))<.01);
for k = 1:numel(toolW)
    refined = fzero(@(w) abs(evalfr(L,1i*w))-1,toolW(k)*[.999 1.001]);
    assert(abs(refined-wc(k))<1e-8);
end
% Disregard limiting zero-frequency entries for integrators.
keep = isfinite(all.GMFrequency) & all.GMFrequency>0;
assert(nnz(keep)==1 && abs(all.GMFrequency(keep)-wp)/wp<1e-3);
assert(abs(all.GainMargin(keep)-gm)/gm<1e-3);
end
