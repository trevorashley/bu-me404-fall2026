function report = frequency_response_stability_margins(makeFigures)
%FREQUENCY_RESPONSE_STABILITY_MARGINS  FPE 6.4, including Examples 6.12–6.13.
if nargin == 0
    makeFigures = true;
end
K = [.1 .5 1 2 5 10]';
wc = arrayfun(@(k) fzero(@(w) w^3+w-k,[0 k]),K);
report.cubic = table(K,wc,90-2*atand(wc),2./K,20*log10(2./K), ...
    'VariableNames',{'Gain','Wc','PM','GM','GMdB'});
report.designWc = tand(10);
report.designK = report.designWc*(1+report.designWc^2);
s = tf('s');
cubic = 1/(s*(1+s)^2);
[report.cubicDv,report.cubicWv] = vectorMargin(cubic);

A.model = 7*(s+10)^2/s^3;
A.wc = fzero(@(w) w^3-7*w^2-700,[10 15]);
A.pm = 180+(-270+2*atand(A.wc/10));
A.wp = 10;
A.gm = 1/abs(evalfr(A.model,1i*A.wp));
A.poles = pole(feedback(A.model,1));
B.model = 85*(s+1)*(s^2+2*s+43.25)/(s^2*(s^2+2*s+82)*(s^2+2*s+101));
% In x = w^2 the squared magnitude of (s^2+2*s+c) is x^2+(4-2*c)*x+c^2.
factor = @(c) [1 4-2*c c^2];
denSq = conv([1 0 0],conv(factor(82),factor(101)));
numSq = 85^2*conv([1 1],factor(43.25));
B.wc = sqrt(positiveRoots(denSq-[zeros(1,3) numSq]));
z = arrayfun(@(w) evalfr(B.model,1i*w),B.wc);
B.pm = 180+rad2deg(angle(z)); % All three phases are on the (-180,0) branch.
wp = sqrt(positiveRoots([4 -881 61891 -1435724]));
z = arrayfun(@(w) evalfr(B.model,1i*w),wp);
B.wp = wp(real(z)<0);
B.gm = 1./abs(z(real(z)<0));
[B.dv,B.wv] = vectorMargin(B.model);
B.poles = pole(feedback(B.model,1));
for level = 1:3
    radius = 100*2^(level-1);
    epsilon = .1/2^(level-1);
    n = 512*2^(level-1);
    A.turns(level) = winding(A.model,radius,epsilon,n);
    B.turns(level) = winding(B.model,radius,epsilon,n);
end
report.ex612 = A;
report.ex613 = B;
if ~makeFigures
    return
end
out = fullfile(fileparts(mfilename('fullpath')),'figures');
if ~isfolder(out)
    mkdir(out)
end
geometry(out,cubic,report,false);
gainSelection(out,report);
dampingFigures(out);
geometry(out,cubic,report,true);
conditionalFigure(out,A);
multipleFigures(out,B);
end

function r = positiveRoots(coeff)
r = roots(coeff);
r = sort(real(r(abs(imag(r))<1e-9 & real(r)>0)));
end

function [dv,wv] = vectorMargin(L)
% Bracket each sampled local minimum, then minimize in log frequency.
[num,den] = tfdata(L,'v');
distance = @(v) abs(1+polyval(num,1i*exp(v))./polyval(den,1i*exp(v)));
v = unique([linspace(-12,12,4001) log(linspace(8,12,2001))]);
d = distance(v);
minima = find(d(2:end-1)<d(1:end-2) & d(2:end-1)<=d(3:end))+1;
% Both loops here have integrators at DC and decay to zero at infinity.
dv = 1; wv = Inf;
for k = minima
    [u,candidate] = fminbnd(distance,v(k-1),v(k+1),optimset('TolX',1e-13));
    if candidate<dv
        dv = candidate; wv = exp(u);
    end
end
end

function pieces = contourImage(L,R,e,n)
w = logspace(log10(e),log10(R),n);
s = {-1i*fliplr(w),e*exp(1i*linspace(-pi/2,pi/2,n)), ...
    1i*w,R*exp(1i*linspace(pi/2,-pi/2,n))};
[num,den] = tfdata(L,'v');
pieces = cellfun(@(v) polyval(num,v)./polyval(den,v),s,'UniformOutput',false);
end

function N = winding(L,R,e,n)
pieces = contourImage(L,R,e,n);
F = 1+[pieces{:}];
a = unwrap(angle(F));
assert(max(abs(diff(a)))<pi/4 && min(abs(F))>.01 && abs(F(end)-F(1))<1e-10);
N = -(a(end)-a(1))/(2*pi);
end

function f = sheet(w,h)
f = figure('Color','white','Position',[80 80 w h]);
end

function saveFigure(f,out,name)
base = fullfile(out,['n06_' name]);
exportgraphics(f,[base '.svg'],'ContentType','vector');
exportgraphics(f,[base '.png'],'Resolution',150);
close(f)
end

function circlePlane()
hold on; axis equal; grid on
a = linspace(0,2*pi,801);
plot(cos(a),sin(a),':','Color',[.42 .44 .46],'LineWidth',1.3);
xline(0,':'); yline(0,':'); plot(-1,0,'kx','LineWidth',2,'MarkerSize',10);
xlabel('Re L'); ylabel('Im L');
end

function geometry(out,L,r,vector)
wc = r.cubic.Wc(r.cubic.Gain==1);
phase = -90-2*atand(wc);
w = logspace(-1.2,1.1,1500);
z = squeeze(freqresp(L,w));
if vector
    f = sheet(750,470);
else
    f = sheet(1000,550); tiledlayout(2,2,'TileSpacing','compact'); nexttile([2 1])
end
circlePlane()
trace = plot(real(z),imag(z),'LineWidth',1.8,'Color',[0 .35 .58]);
radial = plot([-1 -.5],[0 0],'Color',[.79 .32 .04],'LineWidth',3);
arc = linspace(-180,phase,100);
angular = plot(cosd(arc),sind(arc),'Color',[.48 .24 .58],'LineWidth',3);
plot([-.5 cosd(phase)],[0 sind(phase)],'ko','MarkerSize',5)
xlim([-1.45 .15]); ylim([-.85 .52]);
if vector
    closest = evalfr(L,1i*r.cubicWv);
    seg = plot([-1 real(closest)],[0 imag(closest)],'Color',[.02 .52 .38],'LineWidth',3);
    plot(real(closest),imag(closest),'ko','MarkerFaceColor','w')
    legend([trace radial angular seg],{'Loop, positive frequency','Gain change','Phase change','Shortest distance'},'Location','eastoutside')
    title('Three ways to reach the critical point')
    saveFigure(f,out,'vector_margin'); return
end
legend([trace radial angular],{'Loop, positive frequency','GM at phase crossover','PM at gain crossover'},'Location','southoutside')
title('Nyquist geometry, K = 1')
nexttile(2); semilogx(w,20*log10(abs(z)),'LineWidth',1.6); hold on; grid on
yline(0,':'); plot([1 1],[-20*log10(2) 0],'-o','Color',radial.Color,'LineWidth',2);
plot(wc,0,'ks'); ylabel('Magnitude (dB)'); title('GM = 6.02 dB at 1 rad/s'); ylim([-25 18]); xlim([.08 3])
nexttile(4); semilogx(w,-90-2*atand(w),'LineWidth',1.6); hold on; grid on
yline(-180,':'); plot([wc wc],[-180 phase],'-o','Color',angular.Color,'LineWidth',2);
plot(1,-180,'ks'); ylabel('Phase (deg)'); xlabel('Frequency (rad/s)');
title('PM = 21.39° at 0.682 rad/s'); xlim([.08 3])
saveFigure(f,out,'margin_geometry')
end

function gainSelection(out,r)
f = sheet(820,550); tiledlayout(2,1,'TileSpacing','compact')
w = logspace(-1.2,.6,801);
gains = [r.designK .5 5];
crossings = [r.designWc r.cubic.Wc(r.cubic.Gain==.5) r.cubic.Wc(r.cubic.Gain==5)];
nexttile; loglog(w,1./(w.*(1+w.^2)),'LineWidth',1.8); hold on; grid on
for k = 1:3
    yline(1/gains(k),':',sprintf('1/K, K = %.3g',gains(k)));
    plot(crossings(k),1/gains(k),'ko','MarkerFaceColor','w')
end
ylabel('|G|'); title('Read the plant magnitude at the level 1/K'); xlim(w([1 end]))
nexttile; semilogx(w,-90-2*atand(w),'LineWidth',1.8); hold on; grid on; yline(-180,':')
for k = 1:3
    phi = -90-2*atand(crossings(k));
    plot([crossings(k) crossings(k)],[-180 phi],'-o','LineWidth',1.4);
    text(crossings(k)*1.05,phi,sprintf('%.1f°',180+phi));
end
xlabel('Frequency (rad/s)'); ylabel('Phase (deg)'); title('Read the signed phase margin at the same frequency'); xlim(w([1 end]))
saveFigure(f,out,'gain_selection')
end

function dampingFigures(out)
z = linspace(.03,1.2,1601);
x = sqrt(sqrt(1+4*z.^4)-2*z.^2); pm = atand(2*z./x);
f = sheet(720,420); plot(pm,z,'LineWidth',2); hold on; grid on
plot([0 70],[0 .7],'--','LineWidth',1.6); xlabel('Phase margin (deg)'); ylabel('Damping ratio')
title('No-zero second-order model'); legend('Exact','PM / 100','Location','northwest');
saveFigure(f,out,'pm_damping')
f = sheet(820,410); tiledlayout(1,2,'TileSpacing','compact')
mp = zeros(size(z)); under = z<1;
mp(under) = exp(-pi*z(under)./sqrt(1-z(under).^2));
mr = ones(size(z)); peak = z<1/sqrt(2);
mr(peak) = 1./(2*z(peak).*sqrt(1-z(peak).^2));
nexttile; plot(pm,100*mp,'LineWidth',2); grid on; xlabel('PM (deg)'); ylabel('Step overshoot (%)');
nexttile; semilogy(pm,mr,'LineWidth',2); grid on; xlabel('PM (deg)'); ylabel('Peak magnitude M_r (ratio)');
sgtitle('Step and frequency peaks for the no-zero second-order model')
saveFigure(f,out,'pm_peaks')
end

function conditionalFigure(out,A)
f = sheet(1130,390); tiledlayout(1,3,'TileSpacing','compact')
nexttile; hold on; grid on; axis equal; xline(0,':'); yline(0,':');
p = rlocus(tf([1 20 100],[1 0 0 0]),linspace(0,90,1600));
plot(real(p.'),imag(p.'),'Color',[.22 .36 .43]); p5 = [-5;10i;-10i];
h5 = plot(real(p5),imag(p5),'s','MarkerSize',8); h7 = plot(real(A.poles),imag(A.poles),'o','MarkerSize',8);
xlim([-42 5]); ylim([-26 26]); xlabel('Re s'); ylabel('Im s'); title('Closed-loop poles');
legend([h5 h7],{'K = 5','K = 7'},'Location','southwest')
nexttile; hold on; axis equal; grid on
pieces = contourImage(A.model,150,2,1801); styles = {'--','-','-',':'};
for k = 1:4
    plot(real(pieces{k}),imag(pieces{k}),styles{k},'LineWidth',1.6);
end
plot(-1,0,'kx'); xlabel('Re L'); ylabel('Im L'); title('Full finite contour, K = 7')
legend('Negative frequency','Origin detour','Positive frequency','Outer arc','Location','southoutside')
nexttile; circlePlane(); w = logspace(-1,3,2001); v = squeeze(freqresp(A.model,w));
plot(real(v),imag(v),'LineWidth',1.6); plot(real(v),-imag(v),'--');
plot([-1.4 -1],[0 0],'-o','Color',[.75 .28 .05],'LineWidth',2);
xlim([-1.8 .15]); ylim([-.8 .8]); title('Gain reduction: −1.4 to −1');
saveFigure(f,out,'ex612')
end

function multipleFigures(out,B)
f = sheet(970,580); tiledlayout(2,2,'TileSpacing','compact');
ranges = {[.25 50],[9 10.6]};
for k = 1:2
    w = logspace(log10(ranges{k}(1)),log10(ranges{k}(2)),2600);
    v = squeeze(freqresp(B.model,w));
    phase = -180+atand(w)+atan2d(2*w,43.25-w.^2)-atan2d(2*w,82-w.^2)-atan2d(2*w,101-w.^2);
    nexttile(k); semilogx(w,20*log10(abs(v)),'LineWidth',1.6); hold on; grid on
    yline(0,':'); plot(B.wc,zeros(3,1),'o','MarkerSize',7); plot(B.wp,-20*log10(B.gm),'ks');
    ylabel('Magnitude (dB)'); xlim(ranges{k});
    if k==1, title('All gain crossovers'); else, title('Resonance detail'); end
    nexttile(k+2); semilogx(w,phase,'LineWidth',1.6); hold on; grid on; yline(-180,':');
    plot(B.wc,B.pm-180,'o','MarkerSize',7); plot(B.wp,-180,'ks'); xlim(ranges{k});
    xlabel('Frequency (rad/s)'); ylabel('Phase (deg)');
end
saveFigure(f,out,'ex613_bode')
f = sheet(940,430); tiledlayout(1,2,'TileSpacing','compact')
w = logspace(-2,3,9000); v = squeeze(freqresp(B.model,w));
for k = 1:2
    nexttile; circlePlane(); plot(real(v),imag(v),'LineWidth',1.7);
    plot(real(v),-imag(v),'--','LineWidth',1.2);
    p = evalfr(B.model,1i*B.wv);
    plot([-1 real(p)],[0 imag(p)],'-o','Color',[.07 .52 .33],'LineWidth',2);
    plot(-1/B.gm,0,'ks');
    c = arrayfun(@(w) evalfr(B.model,1i*w),B.wc);
    plot(real(c),imag(c),'o');
    if k==1
        axis([-2 1.1 -1.25 1.25]); title('Unit circle and frequency branches');
    else
        axis([-1.07 -.69 -.24 .24]); title('Closest point (segment) and phase crossover (square)');
    end
end
saveFigure(f,out,'ex613_nyquist')
end
