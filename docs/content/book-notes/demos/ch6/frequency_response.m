function report = frequency_response(makeFigures)
%FREQUENCY_RESPONSE FPE Section 6.1, Examples 6.1-6.2 and source illustrations.
% report = frequency_response() computes the report and exports SVG/PNG figures.
% report = frequency_response(false) computes the same report without figures.
% Requires MATLAB and Control System Toolbox. Paths are relative to this file.
if nargin < 1
    makeFigures = true;
end
validateattributes(makeFigures, {'logical','numeric'}, {'scalar','binary'});
s = tf('s');
G1 = 1/(s+1);
t = (0:0.00025:10)';
u = sin(10*t);
y = (10*exp(-t)+sin(10*t)-10*cos(10*t))/101;
yss = (sin(10*t)-10*cos(10*t))/101;
phiRad = angle(1/(1+10j));
report.firstOrder.magnitude = 1/sqrt(101);
report.firstOrder.phaseDegrees = rad2deg(phiRad);
report.firstOrder.lagSeconds = -phiRad/10;
report.firstOrder.lsimMaxError = max(abs(lsim(G1,u,t)-y));
Dc = (s+1)/(s/10+1);
w = logspace(-1,2,800);
[mag,phase] = bode(Dc,w);
mag = squeeze(mag);
phase = squeeze(phase); % BODE returns degrees, unlike ANGLE/ATAN2.
wcheck = sqrt(10);
dcheck = evalfr(Dc,1j*wcheck);
report.lead.dcMagnitude = dcgain(Dc);
report.lead.highFrequencyMagnitude = 10;
report.lead.checkFrequency = wcheck;
report.lead.checkMagnitude = abs(dcheck);
report.lead.checkPhaseDegrees = rad2deg(angle(dcheck));
report.lead.zero = zero(Dc);
report.lead.pole = pole(Dc);
zeta = [0.05 0.1 0.2 0.3 0.5 0.7 0.9 1/sqrt(2)]';
wr = zeros(size(zeta));
Mr = ones(size(zeta));
resonant = zeta < 1/sqrt(2);
wr(resonant) = sqrt(1-2*zeta(resonant).^2);
Mr(resonant) = 1./(2*zeta(resonant).*sqrt(1-zeta(resonant).^2));
wb = sqrt(1-2*zeta.^2+sqrt(4*zeta.^4-4*zeta.^2+2));
wbDirect = zeros(size(zeta));
wbMatlab = wbDirect;
for k = 1:numel(zeta)
    Tclosed = 1/(s^2+2*zeta(k)*s+1); % omega_n = 1 rad/s
    wbDirect(k) = fzero(@(v) abs(evalfr(Tclosed,1j*v))-1/sqrt(2),[0 3]);
    wbMatlab(k) = bandwidth(Tclosed,-10*log10(2));
end
report.secondOrder = table(zeta,wr,Mr,wb,wbDirect,wbMatlab, ...
    'VariableNames',{'zeta','resonanceRatio','peakMagnitude', ...
    'halfPowerRatio','halfPowerDirect','halfPowerMatlab'});
report.conventions = struct('frequency','rad/s','phaseReport','degrees', ...
    'analyticAngles','radians','bandwidth','first descending DC-relative half power', ...
    'riseTime','10-90%','settlingBand','1%');
report.figureFiles = strings(0,1);
if ~makeFigures
    return
end
outDir = fullfile(fileparts(mfilename('fullpath')),'figures');
if ~exist(outDir,'dir')
    mkdir(outDir);
end
blue = [0.00 0.35 0.65];
orange = [0.80 0.30 0.05];
colors = lines(7);

% FPE opening first-order illustration: separate scales and a settled cycle.
f = newFigure([1050 960]);
tl = tiledlayout(f,3,1,'TileSpacing','compact','Padding','compact');
ax = nexttile(tl);
plot(ax,t,u,'Color',blue); grid(ax,'on'); xlim(ax,[0 10]);
ylabel(ax,'Input u'); title(ax,'First-order model: G(s) = 1/(s+1), u = sin(10t)');
ax = nexttile(tl);
plot(ax,t,y,'Color',blue,'LineWidth',1.2); hold(ax,'on');
plot(ax,t,yss,'--','Color',orange,'LineWidth',1);
plot(ax,t,10*exp(-t)/101,':','Color',[.2 .2 .2],'LineWidth',1.8);
grid(ax,'on'); xlim(ax,[0 10]); ylabel(ax,'Output y'); xlabel(ax,'Time t (s)');
legend(ax,{'Complete output','Steady sinusoid','Transient: (10/101)e^{-t}'}, ...
    'Location','northeast','NumColumns',3);
ax = nexttile(tl);
plot(ax,t,u,'Color',blue,'LineWidth',1.5); hold(ax,'on');
plot(ax,t,yss/report.firstOrder.magnitude,'--','Color',orange,'LineWidth',1.5);
xlim(ax,[8.1 8.85]); ylim(ax,[-1.5 1.4]); grid(ax,'on');
tzero = 26*pi/10;
xline(ax,tzero,':','Color',blue); xline(ax,tzero-phiRad/10,':','Color',orange);
plot(ax,[tzero tzero-phiRad/10],[-1.18 -1.18],'k-o','MarkerSize',3);
text(ax,tzero+.01,-1.35,sprintf('Lag %.6f s = 84.2894 deg',-phiRad/10), ...
    'FontSize',11,'VerticalAlignment','middle');
ylabel(ax,'Normalized traces'); xlabel(ax,'Time t (s), settled-cycle close-up');
legend(ax,{'Input u','Steady output / M'},'Location','northeast');
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_sinusoidal_response')];

% Example 6.1: analytical signals; do not simulate an improper differentiator.
f = newFigure([1000 440]); ax = axes(f);
theta = linspace(0,4*pi,1001);
plot(ax,theta,sin(theta),'Color',blue,'LineWidth',1.7); hold(ax,'on');
plot(ax,theta,cos(theta),'--','Color',orange,'LineWidth',1.7);
grid(ax,'on'); xlim(ax,[0 4*pi]); ylim(ax,[-1.3 1.4]);
xticks(ax,0:pi/2:4*pi); xticklabels(ax,{'0','pi/2','pi','3pi/2','2pi','5pi/2','3pi','7pi/2','4pi'});
xlabel(ax,'Phase coordinate theta = omega t (rad)'); ylabel(ax,'Normalized signal');
title(ax,'Example 6.1: capacitor current leads voltage by 90 deg');
legend(ax,{'Voltage v/A = sin(theta)','Current i/(AC omega) = cos(theta)'}, ...
    'Location','southoutside','NumColumns',2,'AutoUpdate','off');
plot(ax,[2*pi 2*pi+pi/2],[1.12 1.12],'k-o','MarkerSize',3);
text(ax,2*pi+pi/4,1.27,'Quarter cycle','HorizontalAlignment','center');
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_capacitor')];

% Example 6.2: linear magnitude on a logarithmic magnitude axis.
f = newFigure([1000 730]); tl = tiledlayout(f,2,1,'TileSpacing','compact');
ax = nexttile(tl); loglog(ax,w,mag,'Color',blue,'LineWidth',1.7); hold(ax,'on');
xline(ax,1,':'); xline(ax,10,':');
plot(ax,wcheck,abs(dcheck),'o','Color',orange,'MarkerFaceColor',orange);
grid(ax,'on'); xlim(ax,[.1 100]); ylim(ax,[.9 11]); ylabel(ax,'|D_c(j omega)|');
title(ax,'Example 6.2: D_c(s) = (s+1)/(s/10+1)');
text(ax,4,2.5,'Checkpoint: (sqrt(10), sqrt(10))','FontSize',11);
ax = nexttile(tl); semilogx(ax,w,phase,'Color',blue,'LineWidth',1.7); hold(ax,'on');
xline(ax,1,':'); xline(ax,10,':');
plot(ax,wcheck,rad2deg(angle(dcheck)),'o','Color',orange,'MarkerFaceColor',orange);
grid(ax,'on'); xlim(ax,[.1 100]); ylim(ax,[0 65]);
ylabel(ax,'Phase (deg)'); xlabel(ax,'Frequency omega (rad/s)');
text(ax,4,58,'54.9032 deg','FontSize',11);
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_ex602_lead')];

% FPE Figure 6.3 source damping values; threshold is checked, not added here.
r = unique([logspace(-1,1,2000),1,wr(1:6)']);
f = newFigure([1050 850]); tl = tiledlayout(f,2,1,'TileSpacing','compact');
ax1 = nexttile(tl); hold(ax1,'on'); ax2 = nexttile(tl); hold(ax2,'on');
labels = cell(1,7);
for k = 1:7
    h = 1./(1-r.^2+1j*2*zeta(k)*r);
    plot(ax1,r,abs(h),'Color',colors(k,:),'LineWidth',1.5);
    plot(ax2,r,rad2deg(angle(h)),'Color',colors(k,:),'LineWidth',1.5);
    labels{k} = sprintf('zeta = %.2g',zeta(k));
end
set(ax1,'XScale','log','YScale','log'); set(ax2,'XScale','log');
xline(ax1,1,':'); xline(ax2,1,':'); yline(ax2,-90,':');
xlim(ax1,[.1 10]); ylim(ax1,[.008 12]); grid(ax1,'on'); ylabel(ax1,'Magnitude |G|');
title(ax1,'Second-order family: G = 1/[(s/omega_n)^2 + 2 zeta (s/omega_n) + 1]');
legend(ax1,labels,'Location','southwest','NumColumns',2);
xlim(ax2,[.1 10]); ylim(ax2,[-180 0]); yticks(ax2,-180:30:0); grid(ax2,'on');
ylabel(ax2,'Phase (deg)'); xlabel(ax2,'Normalized frequency r = omega / omega_n');
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_second_order_family')];

% Comparison with the earlier time-domain family (not a new numbered example).
f = newFigure([1050 500]); ax = axes(f); hold(ax,'on');
tau = linspace(0,25,5001);
for k = 1:7
    beta = sqrt(1-zeta(k)^2);
    ys = 1-exp(-zeta(k)*tau).*(cos(beta*tau)+zeta(k)/beta*sin(beta*tau));
    plot(ax,tau,ys,'Color',colors(k,:),'LineWidth',1.5);
end
yline(ax,1,':','Final value'); grid(ax,'on'); xlim(ax,[0 25]); ylim(ax,[0 2]);
xlabel(ax,'Normalized time omega_n t'); ylabel(ax,'Unit-step output y');
title(ax,'Same poles, different experiment: the unit-step response');
legend(ax,labels,'Location','eastoutside');
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_second_order_steps')];

% Redraw FPE Figure 6.4 with the negative feedback sign required by 1+KG.
f = newFigure([1000 300]); ax = axes(f); axis(ax,[0 10 0 3]); axis(ax,'off'); hold(ax,'on');
rectangle(ax,'Position',[2 1.6 .65 .65],'Curvature',[1 1],'LineWidth',1.4);
text(ax,2.325,1.925,'sum','HorizontalAlignment','center','FontSize',11);
rectangle(ax,'Position',[4 1.5 2 0.85],'LineWidth',1.4);
text(ax,5,1.925,'KG(s)','HorizontalAlignment','center','FontSize',15);
plot(ax,[.8 2],[1.925 1.925],'k-'); plot(ax,[2.65 4],[1.925 1.925],'k-');
plot(ax,[6 8.8],[1.925 1.925],'k-'); plot(ax,[7.5 7.5 2.325 2.325],[1.925 .6 .6 1.6],'k-');
plot(ax,7.5,1.925,'ko','MarkerFaceColor','k','MarkerSize',5);
text(ax,1.2,2.25,'R','FontSize',14); text(ax,3.1,2.25,'E','FontSize',14);
text(ax,8.5,2.25,'Y','FontSize',14);
text(ax,1.8,2.15,'+','FontSize',18); text(ax,2.55,1.25,'-','FontSize',22);
plot(ax,[2 4 8.8],[1.925 1.925 1.925],'k>','MarkerFaceColor','k','MarkerSize',7);
plot(ax,2.325,1.6,'k^','MarkerFaceColor','k','MarkerSize',7);
title(ax,'Unity negative feedback: E = R - Y');
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_feedback_diagram')];

% FPE Figure 6.5 definitions, on a stated member of the second-order family.
z = .3; wn = 1; wrIllustration = wn*sqrt(1-2*z^2);
MrIllustration = 1/(2*z*sqrt(1-z^2));
wbIllustration = wn*sqrt(1-2*z^2+sqrt(4*z^4-4*z^2+2));
f = newFigure([1050 580]); ax = axes(f);
v = linspace(0,3.1,2001); h = 1./(1-(v/wn).^2+1j*2*z*v/wn);
plot(ax,v,abs(h),'Color',blue,'LineWidth',2); hold(ax,'on');
yline(ax,1,':','DC gain = 1','LabelHorizontalAlignment','right');
yline(ax,1/sqrt(2),'--','Half power: 1/sqrt(2)', ...
    'LabelHorizontalAlignment','right','Color',orange);
xline(ax,wbIllustration,'--','Color',orange);
plot(ax,wrIllustration,MrIllustration,'o','Color',blue,'MarkerFaceColor',blue);
plot(ax,wbIllustration,1/sqrt(2),'o','Color',orange,'MarkerFaceColor',orange);
text(ax,.12,1.92,sprintf('M_r = %.5f at omega_r = %.6f rad/s',MrIllustration,wrIllustration),'FontSize',12);
text(ax,1.65,.55,sprintf('omega_{BW} = %.5f rad/s',wbIllustration),'FontSize',12);
grid(ax,'on'); xlim(ax,[0 3.1]); ylim(ax,[0 2.1]);
xlabel(ax,'Frequency omega (rad/s)'); ylabel(ax,'Closed-loop magnitude |T(j omega)|');
title(ax,'Bandwidth illustration: second-order T, zeta = 0.3, omega_n = 1 rad/s');
report.figureFiles = [report.figureFiles; saveFigure(f,outDir,'n01_bandwidth_definition')];
end

function f = newFigure(pixels)
f = figure('Color','white','Visible','off','Position',[100 100 pixels]);
set(f,'DefaultAxesFontSize',11,'DefaultAxesLineWidth',.8,'DefaultTextFontSize',11);
end

function files = saveFigure(f,outDir,name)
files = [string(fullfile(outDir,[name '.svg'])); string(fullfile(outDir,[name '.png']))];
exportgraphics(f,files(1),'ContentType','vector','BackgroundColor','white');
exportgraphics(f,files(2),'Resolution',170,'BackgroundColor','white');
close(f);
end
