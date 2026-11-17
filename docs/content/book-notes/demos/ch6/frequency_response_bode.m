function report = frequency_response_bode(makeFigures)
%FREQUENCY_RESPONSE_BODE FPE Examples 6.3-6.6 and Bode factor rules.
% Requires MATLAB and Control System Toolbox. No figures when false.
if nargin < 1, makeFigures = true; end
s = tf('s');
models = {2000*(s+.5)/(s*(s+10)*(s+50)), ...
    10/(s*(s^2+.4*s+4)), ...
    .01*(s^2+.01*s+1)/(s^2*(s^2/4+.01*s+1))};
w = sort(unique([logspace(-2,3,2000),linspace(.95,1.05,4001),linspace(1.9,2.1,4001)]));
z = 1i*w;
M = zeros(3,numel(w)); P = M;
A = M;
A(1,:) = 2./w.*max(1,w/.5)./max(1,w/10)./max(1,w/50);
A(2,:) = 2.5./w./max(1,(w/2).^2);
A(3,:) = .01./w.^2.*max(1,w.^2)./max(1,(w/2).^2);
P(1,:) = -90+atand(2*w)-atand(w/10)-atand(w/50);
P(2,:) = -90-atan2d(.1*w,1-w.^2/4);
P(3,:) = -180+atan2d(.01*w,1-w.^2)-atan2d(.01*w,1-w.^2/4);
for k=1:3
    [bmag,bphase] = bode(models{k},w);
    M(k,:) = reshape(bmag,1,[]);
    report.bodeMagnitude{k} = squeeze(bmag);
    report.bodePhase{k} = squeeze(bphase);
end
report.frequency = w;
report.magnitude = M;
report.phase = P;
report.asymptote = A;
report.ex604Corner = [abs(evalfr(models{2},2i)),-180];
report.ex605Corners = [abs(evalfr(models{3},1i)),abs(evalfr(models{3},2i))];
f = @(v) abs(.01*((1i*v).^2+.01i*v+1)./((1i*v).^2.*((1i*v).^2/4+.01i*v+1)));
opts = optimset('TolX',1e-12);
wn = fminbnd(f,.95,1.05,opts);
wp = fminbnd(@(v)-f(v),1.9,2.1,opts);
report.flexibleExtrema = [wn,f(wn);wp,f(wp)];
refined = sort(unique([w,linspace(.95,1.05,8001),linspace(1.9,2.1,8001)]));
for k=1:2
    interval = [.95,1.05;1.9,2.1];
    wc = w(w>=interval(k,1)&w<=interval(k,2));
    wr = refined(refined>=interval(k,1)&refined<=interval(k,2));
    if k==1, report.sampledExtrema(k,:)=[min(f(wc)),min(f(wr))];
    else, report.sampledExtrema(k,:)=[max(f(wc)),max(f(wr))]; end
end
report.nmpMagnitude = 10*sqrt((w.^2+1)./(w.^2+100));
report.nmpPhase = [atand(w)-atand(w/10);180-atand(w)-atand(w/10)];
report.complexFrequency = z;
if ~makeFigures, return; end
out = fullfile(fileparts(mfilename('fullpath')),'figures');
if ~isfolder(out), mkdir(out); end
% Related normalized factors: exact curves and corresponding asymptotes.
r = logspace(-2,2,1600);
q = 1-r.^2+.2i*r;
F = [1i*r;1./(1i*r);1+1i*r;1./(1+1i*r);q;1./q];
FA = [r;1./r;max(1,r);1./max(1,r);max(1,r.^2);1./max(1,r.^2)];
FP = [90+0*r;-90+0*r;atand(r);-atand(r);atan2d(.2*r,1-r.^2);-atan2d(.2*r,1-r.^2)];
names = {'s','1/s','1+s','1/(1+s)','pair, zeta=0.1','inverse pair'};
fig = figure('Color','w','Position',[100 100 1200 760]);
tiledlayout(2,3,'TileSpacing','compact');
for k=1:3
    nexttile; semilogx(r,db(abs(F(2*k-1,:))),'LineWidth',1.6); hold on
    semilogx(r,db(abs(F(2*k,:))),'LineWidth',1.6);
    semilogx(r,db(FA(2*k-1,:)),'k:',r,db(FA(2*k,:)),'k:');
    grid on; ylabel('Magnitude (dB)'); xlabel('Normalized frequency');
    legend(names(2*k-1:2*k),'Location','best');
end
for k=1:3
    nexttile; semilogx(r,FP(2*k-1:2*k,:),'LineWidth',1.6);grid on
    xlabel('Normalized frequency');ylabel('Phase (deg)');
    if k==2
        hold on; ramp=min(90,max(0,45*(1+log10(r))));
        semilogx(r,ramp,'k--',r,-ramp,'k--','LineWidth',1);
        legend('zero exact','pole exact','zero ramp','pole ramp','Location','best');
    end
end
saveplot(fig,out,'n02_factor_rules');
% Example 6.3 component addition and composite construction.
fig = figure('Color','w','Position',[100 100 1100 800]); tiledlayout(2,2,'TileSpacing','compact');
parts = [2./w;abs(1+2i*w);1./abs(1+1i*w/10);1./abs(1+1i*w/50)];
nexttile; semilogx(w,db(parts),'LineWidth',1.3); grid on; ylabel('Component magnitude (dB)');
legend('2/s','zero at -0.5','pole at -10','pole at -50','Location','best');
nexttile; semilogx(w,db(M(1,:)),w,db(A(1,:)),'--','LineWidth',1.6);grid on;ylabel('Composite magnitude (dB)');legend('exact','asymptote','Location','southwest');corners([.5 10 50]);
nexttile;semilogx(w,[-90+0*w;atand(2*w);-atand(w/10);-atand(w/50)],'LineWidth',1.3);grid on;ylabel('Component phase (deg)');xlabel('Frequency (rad/s)');
nexttile; guide=-90+90*(w>=.5)-90*(w>=10)-90*(w>=50);
semilogx(w,P(1,:),w,guide,':','LineWidth',1.6);grid on;ylabel('Composite phase (deg)');xlabel('Frequency (rad/s)');legend('exact sum','step guide','Location','southwest');corners([.5 10 50]);
saveplot(fig,out,'n02_ex603');
fig = pairplot(w,M(2,:),P(2,:),A(2,:),'Example 6.4: complex poles');
nexttile(1);xlim([.1 10]);ylim([-45 30]);hold on;corners(2);semilogx(2,db(6.25),'ko','HandleVisibility','off');
nexttile(2);xlim([.1 10]);corners(2);ylim([-280 -80]);saveplot(fig,out,'n02_ex604');
fig = figure('Color','w','Position',[100 100 1000 750]);tiledlayout(2,1,'TileSpacing','compact');
nexttile;semilogx(w,db(A(3,:)),'--','LineWidth',1.7);hold on
semilogx([1 2],db([.0001 .5]),'rx','MarkerSize',10,'LineWidth',1.8);
semilogx([1 2],db(report.ex605Corners),'ko','MarkerSize',7,'LineWidth',1.5);grid on
xlabel('Frequency (rad/s)');ylabel('Magnitude (dB)');xlim([.01 100]);legend('asymptote','isolated correction estimates','full-model corner values','Location','southwest');corners([1 2]);
nexttile;guide=-180+180*(w>=1)-180*(w>=2);
semilogx(w,guide,':','LineWidth',1.7);grid on;xlim([.01 100]);ylim([-200 20]);xlabel('Frequency (rad/s)');ylabel('Step phase guide (deg)');corners([1 2]);
saveplot(fig,out,'n02_ex605_hand_sketch');
fig=figure('Color','w','Position',[100 100 1200 760]);tiledlayout(2,3,'TileSpacing','compact');
for k=1:3
    nexttile;semilogx(w,db(M(3,:)),w,db(A(3,:)),'--','LineWidth',1.6);grid on;ylabel('Magnitude (dB)');
    if k==1,xlim([.01 100]);legend('exact','asymptote','Location','southwest');title('Full response');elseif k==2,xlim([.95 1.05]);ylim([-80 -35]);title('Antiresonance close-up');else,xlim([1.9 2.1]);ylim([-45 -5]);title('Resonance close-up');end
end
for k=1:3
    nexttile;semilogx(w,P(3,:),w,guide,':','LineWidth',1.6);grid on;ylabel('Phase (deg)');xlabel('Frequency (rad/s)');
    if k==1,xlim([.01 100]);legend('exact','step guide','Location','northwest');elseif k==2,xlim([.95 1.05]);else,xlim([1.9 2.1]);end
end
saveplot(fig,out,'n02_ex606_exact_comparison');
fig=figure('Color','w','Position',[100 100 1000 750]);tiledlayout(2,1,'TileSpacing','compact');
nexttile;semilogx(w,db(report.nmpMagnitude),'LineWidth',1.8);grid on;ylabel('Magnitude (dB)');title('G1(0)=+1 and G2(0)=-1: identical magnitudes');
nexttile;semilogx(w,report.nmpPhase,'LineWidth',1.8);grid on;xlabel('Frequency (rad/s)');ylabel('Phase (deg)');legend('G1: LHP zero, DC +1','G2: RHP zero, DC -1','Location','best');ylim([-5 190]);
saveplot(fig,out,'n02_nonminimum_phase');
end
function y=db(x)
y=20*log10(x);
end
function corners(v)
for k=1:numel(v),xline(v(k),':',sprintf('%g rad/s',v(k)),'HandleVisibility','off');end
end
function fig=pairplot(w,m,p,a,caption)
fig=figure('Color','w','Position',[100 100 1000 750]);tiledlayout(2,1,'TileSpacing','compact');
nexttile;semilogx(w,db(m),w,db(a),'--','LineWidth',1.7);grid on;ylabel('Magnitude (dB)');title(caption);legend('exact','asymptote');
nexttile;semilogx(w,p,'LineWidth',1.7);grid on;xlabel('Frequency (rad/s)');ylabel('Phase (deg)');
end
function saveplot(fig,out,stem)
exportgraphics(fig,fullfile(out,[stem '.svg']),'ContentType','vector');
exportgraphics(fig,fullfile(out,[stem '.png']),'Resolution',160);
close(fig);
end
