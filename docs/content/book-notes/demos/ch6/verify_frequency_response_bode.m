function results = verify_frequency_response_bode()
%VERIFY_FREQUENCY_RESPONSE_BODE Independent rational and factor checks.
% This verifier does not call the demonstration or reuse its helpers.
w=sort(unique([logspace(-3,4,3001),linspace(.95,1.05,8001),linspace(1.9,2.1,8001)]));
z=1i*w;
direct=[2000*(z+.5)./(z.*(z+10).*(z+50)); ...
    10./(z.*(z.^2+.4*z+4)); ...
    .01*(z.^2+.01*z+1)./(z.^2.*(z.^2/4+.01*z+1))];
normalized=[2*(1+z/.5)./(z.*(1+z/10).*(1+z/50)); ...
    2.5./(z.*((z/2).^2+.2*z/2+1)); ...
    .01./z.^2.*(1+.01*z+z.^2)./(1+.01*z+z.^2/4)];
results.normalization=max(abs(direct-normalized)./abs(direct),[],'all');
assert(results.normalization<3e-14);
factorM=[2./w.*sqrt(1+(2*w).^2)./sqrt(1+(w/10).^2)./sqrt(1+(w/50).^2); ...
    2.5./w./sqrt((1-w.^2/4).^2+(.1*w).^2); ...
    .01./w.^2.*sqrt(((1-w.^2).^2+(.01*w).^2)./((1-w.^2/4).^2+(.01*w).^2))];
phase=[-90+atand(2*w)-atand(w/10)-atand(w/50); ...
    -90-atan2d(.1*w,1-w.^2/4); ...
    -180+atan2d(.01*w,1-w.^2)-atan2d(.01*w,1-w.^2/4)];
results.factorMagnitude=max(abs(factorM-abs(direct))./abs(direct),[],'all');
results.factorPhasor=max(abs(exp(1i*deg2rad(phase))-direct./abs(direct)),[],'all');
assert(results.factorMagnitude<3e-14 && results.factorPhasor<3e-14);
assert(max(abs(diff(phase,1,2)),[],'all')<10,'Displayed branch is discontinuous.');
s=tf('s'); models={2000*(s+.5)/(s*(s+10)*(s+50)),10/(s*(s^2+.4*s+4)),.01*(s^2+.01*s+1)/(s^2*(s^2/4+.01*s+1))};
results.bodeMagnitude=zeros(1,3);results.bodePhase=zeros(1,3);
for k=1:3
    [m,p]=bode(models{k},w);m=reshape(m,1,[]);p=reshape(p,1,[]);
    results.bodeMagnitude(k)=max(abs(m-abs(direct(k,:)))./abs(direct(k,:)));
    results.bodePhase(k)=max(abs(mod(p-phase(k,:)+180,360)-180));
end
assert(max(results.bodeMagnitude)<1e-11 && max(results.bodePhase)<1e-8);
results.ex604Corner=abs(10/(2i*((2i)^2+.4*2i+4)));
assert(abs(results.ex604Corner-6.25)<1e-13);
assert(abs(phase(2,w==2)+180)<1e-10);
f=@(v) abs(.01*((1i*v).^2+.01i*v+1)./((1i*v).^2.*((1i*v).^2/4+.01i*v+1)));
results.ex605Corners=[f(1),f(2)];
bench=[.0001333215,.3750083];
assert(max(abs(results.ex605Corners-bench)./bench)<.001);
% Squared magnitude as a rational function of x=w^2. Its log derivative
% vanishes at extrema; bracketed roots are independent of sampled plots.
N=@(x) (1-x).^2+.0001*x;
D=@(x) (1-x/4).^2+.0001*x;
dlog=@(x) -2./x+(2*x-1.9999)./N(x)-(.125*x-.4999)./D(x);
xn=fzero(dlog,[.999,1.001]);xp=fzero(dlog,[3.99,4.01]);
results.extrema=[sqrt(xn),f(sqrt(xn));sqrt(xp),f(sqrt(xp))];
results.extremaResidual=max(abs(dlog([xn xp])));
assert(results.extremaResidual<1e-7);
assert(f(sqrt(xn))<min(f(sqrt(xn)+[-1e-4 1e-4])));
assert(f(sqrt(xp))>max(f(sqrt(xp)+[-1e-4 1e-4])));
for k=1:2
    ranges=[.95 1.05;1.9 2.1];
    coarse=linspace(ranges(k,1),ranges(k,2),4001);
    fine=linspace(ranges(k,1),ranges(k,2),8001);
    if k==1, a=min(f(coarse));b=min(f(fine));else,a=max(f(coarse));b=max(f(fine));end
    results.refinement(k)=abs(a-b)/b;
    results.sampleToRoot(k)=abs(b-results.extrema(k,2))/results.extrema(k,2);
end
assert(max(results.refinement)<1e-5 && max(results.sampleToRoot)<1e-5);
g1=10*(z+1)./(z+10);g2=10*(z-1)./(z+10);
p1=atand(w)-atand(w/10);p2=180-atand(w)-atand(w/10);
results.equalMagnitude=max(abs(abs(g1)-abs(g2))./abs(g1));
results.allpass=max(abs(abs(g2./g1)-1));
results.nmpPhase=max([abs(exp(1i*deg2rad(p1))-g1./abs(g1)),abs(exp(1i*deg2rad(p2))-g2./abs(g2))]);
assert(results.equalMagnitude<1e-14 && results.allpass<1e-14 && results.nmpPhase<1e-14);
assert(p2(1)>179 && p2(end)<.1 && p1(1)>0);
% Independent factor-rule checkpoints and resonance condition.
r=[.01 1 100];q=1-r.^2+.2i*r;
assert(abs(abs(1+1i)-sqrt(2))<1e-14 && abs(abs(q(2))-.2)<1e-14);
zeta=.1;rr=sqrt(1-2*zeta^2);
assert(abs(abs(1/(1-rr^2+2i*zeta*rr))-1/(2*zeta*sqrt(1-zeta^2)))<1e-12);
results.passed=true;
disp(results);
end
