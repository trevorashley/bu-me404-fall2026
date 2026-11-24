function report = frequency_response_nyquist(makeFigures)
%FREQUENCY_RESPONSE_NYQUIST Directed contours for FPE Examples 6.8–6.11.
% With false, compute the three contour refinements without opening figures.
if nargin == 0
    makeFigures = true;
end
models = {tf(1,[1 2 1]), tf(1,[1 2 1 0]), ...
          tf([10 10],[1 -10 0]), tf([1 0 3],[1 2 1])};
gains = {[1 -.5 -2],[.5 4 -1],[.5 2 -1],[.5 2]};
markers = {[0 .5 1 2 Inf],[.1 .5 1 2 10],[.1 1 sqrt(10) 10 100],[0 1 sqrt(3) 3 Inf]};
% Columns give outer radius, indentation radius and samples per segment.
report.settings = [40 .04 256; 80 .02 512; 160 .01 1024];
report.examples = cell(1,4);
for i = 1:4
    c.model = models{i};
    [num,den] = tfdata(c.model,'v');
    g = @(s) polyval(num,s)./polyval(den,s);
    c.gains = gains{i};
    c.frequency = markers{i};
    [c.markerMagnitude,c.markerPhase] = polarData(i,c.frequency(isfinite(c.frequency)));
    c.samples = g(1i*c.frequency(isfinite(c.frequency)));
    if isinf(c.frequency(end))
        padded = [zeros(1,numel(den)-numel(num)) num];
        c.samples(end+1) = padded(1)/den(1);
    end
    indented = ismember(i,[2 3]);
    emptyCheck = struct('N',NaN,'clearance',NaN,'closure',NaN,'maxAngleStep',NaN);
    checks = repmat(emptyCheck,numel(c.gains),size(report.settings,1));
    for level = 1:size(report.settings,1)
        setting = report.settings(level,:);
        segments = contourParts(setting(1),setting(2),setting(3),indented);
        s = [segments{:}];
        for k = 1:numel(c.gains)
            F = 1+c.gains(k)*g(s);
            phi = unwrap(angle(F));
            checks(k,level) = struct('N',-(phi(end)-phi(1))/(2*pi), ...
                'clearance',min(abs(F)),'closure',abs(F(end)-F(1)), ...
                'maxAngleStep',max(abs(diff(phi))));
        end
    end
    c.checks = checks;
    report.examples{i} = c;
end
if ~makeFigures
    return
end
out = fullfile(fileparts(mfilename('fullpath')),'figures');
if ~isfolder(out)
    mkdir(out)
end
argumentFigure(out)
feedbackFigure(out)
for i = 1:4
    responseFigure(out,report.examples{i},i)
    if ismember(i,[2 3])
        detourFigure(out,models{i},i)
    end
    if ismember(i,[1 3])
        locusFigure(out,i)
    end
end
end

function parts = contourParts(R,e,n,indented)
% The axis runs upward. The right-hand indent excludes the origin.
w = logspace(log10(e),log10(R),n);
if indented
    middle = e*exp(1i*linspace(-pi/2,pi/2,n));
else
    middle = 1i*linspace(-e,e,n);
end
outer = R*exp(1i*linspace(pi/2,-pi/2,n));
parts = {-1i*fliplr(w),middle,1i*w,outer};
end

function plane(x,y)
hold on; grid on; axis equal
xline(0,':','HandleVisibility','off'); yline(0,':','HandleVisibility','off');
xlabel(x); ylabel(y);
end

function directed(v,style,color,portion)
plot(real(v),imag(v),style,'Color',color,'LineWidth',1.6);
idx = round(1+portion*(numel(v)-1));
delta = v(min(end,idx+max(1,round(.035*numel(v)))))-v(idx);
quiver(real(v(idx)),imag(v(idx)),real(delta),imag(delta),0, ...
    'Color',color,'LineWidth',1.7,'MaxHeadSize',2);
end

function finish(f,out,name)
stem = fullfile(out,['n05_' name]);
exportgraphics(f,[stem '.svg'],'ContentType','vector');
exportgraphics(f,[stem '.png'],'Resolution',150);
close(f)
end

function argumentFigure(out)
f = figure('Color','w','Position',[60 60 900 640]);
tiledlayout(2,2,'TileSpacing','compact'); blue = [0 .34 .62];
s = exp(-1i*linspace(0,2*pi,601));
for p = [-1.45 -.25]
    z = -2; at = s(90);
    nexttile; plane('Re s','Im s'); directed(s,'-',blue,.52)
    for point = [z p]
        quiver(point,0,real(at)-point,imag(at),0,'Color',[.32 .36 .40],'MaxHeadSize',.22);
    end
    plot(z,0,'ko',p,0,'kx',real(at),imag(at),'k.','MarkerSize',9);
    xlim([-2.35 1.35]); ylim([-1.15 1.15])
    if p < -1
        title('Both vectors start outside')
    else
        title('Pole vector starts inside')
    end
    nexttile; plane('Re F','Im F'); v = (s-z)./(s-p);
    directed(v,'-',blue,.6); plot(0,0,'k+','MarkerSize',10)
    if p < -1
        title('No turn around zero')
    else
        title('One counterclockwise turn around zero')
    end
end
finish(f,out,'argument_principle')
end

function feedbackFigure(out)
f = figure('Color','w','Position',[60 60 900 620]);
tiledlayout(2,2,'TileSpacing','compact'); blue = [0 .34 .62];
nexttile; axis([0 10 0 5]); axis off; hold on
title('Unity negative feedback')
rectangle('Position',[2 3 .48 .48],'Curvature',[1 1]);
rectangle('Position',[4.1 2.85 1.9 .8]); text(5.05,3.25,'L(s)','HorizontalAlignment','center');
quiver([.5 2.48 6 2.24],[3.24 3.24 3.24 1.75],[1.5 1.62 3 0],[0 0 0 1.25],0,'k');
plot([7.6 7.6 2.24],[3.24 1.75 1.75],'k-');
text(.5,3.68,'R'); text(8.7,3.68,'Y'); text(1.55,3.57,'+'); text(2.5,2.85,'−')
text(5,.65,'Characteristic equation:   1 + L(s) = 0','HorizontalAlignment','center');
nexttile; plane('Re s','Im s');
axispath = 1i*linspace(-3,3,420);
arc = 3*exp(1i*linspace(pi/2,-pi/2,420));
directed(axispath,'-',blue,.42); directed(arc,'--',[.58 .27 .08],.42);
title('Clockwise boundary of a right half-disk')
for shift = [0 1]
    nexttile; plane('Real part','Imaginary part');
    % The same rational map and radius in both panels.
    directed(shift-2./(axispath+1),'-',blue,.43);
    directed(shift-2./(arc+1),'--',[.58 .27 .08],.45)
    plot(shift-1,0,'kx','MarkerSize',10,'LineWidth',1.8);
    xlim([-2.4 1.4]); ylim([-1.15 1.15]);
    if shift == 0
        title('L = −2/(s+1), centered on −1')
    else
        title('1 + L, centered on 0')
    end
end
finish(f,out,'feedback_mapping')
end

function [mag,phase] = polarData(i,w)
switch i
    case 1
        mag = 1./(1+w.^2); phase = -2*atand(w);
    case 2
        mag = 1./(w.*(1+w.^2)); phase = -90-2*atand(w);
    case 3
        mag = 10*hypot(1,w)./(w.*hypot(10,w)); phase = 90+atand(w)+atand(w/10);
    case 4
        mag = abs(3-w.^2)./(1+w.^2);
        phase = -2*atand(w)+180*(w>sqrt(3));
        atZero = (w==sqrt(3)); mag(atZero) = 0; phase(atZero) = NaN;
end
end

function responseFigure(out,c,i)
% Match the symbols in the Bode and complex planes; log axes omit endpoints.
f = figure('Color','w','Position',[60 60 1100 550]);
tiles = tiledlayout(2,2,'TileSpacing','compact','Padding','compact');
w = logspace(-2,2.4,3000);
if i==4
    w = sort([w sqrt(3)*[1-1e-6 1 1+1e-6]]);
end
[mag,phase] = polarData(i,w);
m = c.frequency;
mMag = c.markerMagnitude; mPhase = c.markerPhase;
blue = [0 .34 .62]; orange = [.74 .32 .08];
symbols = {'o','s','d','^','v'};
axMag = nexttile(1); semilogx(w,mag,'Color',blue,'LineWidth',1.5); hold on
if i~=4
    set(gca,'YScale','log');
end
grid on; ylabel('|G|'); title('Magnitude (linear ratio)')
axPhase = nexttile(3); semilogx(w,phase,'Color',blue,'LineWidth',1.5); hold on; grid on
ylabel('Phase (deg)'); xlabel('Frequency (rad/s)'); title('Continuous phase on each branch')
axG = nexttile(2,[2 1]); plane('Re G','Im G');
v = squeeze(freqresp(c.model,w)).';
if m(1)==0
    v = [c.samples(1) v c.samples(end)];
end
directed(v,'-',blue,.48); directed(conj(fliplr(v)),'--',orange,.53)
gains = { [1 -.5 -2], [.5 4], [.5 2], 1 };
for K = gains{i}
    cp = -1/K; plot(cp,0,'kx','MarkerSize',10,'LineWidth',1.7);
    text(cp,-.08,sprintf('K=%g',K),'HorizontalAlignment','center', ...
        'VerticalAlignment','top','FontSize',10);
end
for j = 1:numel(m)
    if isfinite(m(j)) && m(j)>0
        plot(axMag,m(j),mMag(j),symbols{j},'Color',blue,'MarkerSize',7);
        if isfinite(mPhase(j))
            plot(axPhase,m(j),mPhase(j),symbols{j},'Color',blue,'MarkerSize',7);
        end
    end
    plot(axG,real(c.samples(j)),imag(c.samples(j)),symbols{j},'Color',blue,'MarkerSize',7);
end
bounds = {[-1.4 2.55 -.95 .95],[-2.35 .35 -1.2 1.2], ...
    [-2.35 .35 -1.2 1.2],[-1.35 3.45 -2 2]};
axis(axG,bounds{i}); title(axG,'G plane: solid +ω, dashed −ω');
labels = {'0, 0.5, 1, 2, ∞','0.1, 0.5, 1, 2, 10', ...
          '0.1, 1, √10, 10, 100','0, 1, √3, 3, ∞'};
title(tiles,sprintf('Example 6.%d    |    ○  □  ◇  △  ▽   in order:  %s  rad/s',i+7,labels{i}));
finish(f,out,sprintf('ex6%02d',i+7))
end

function detourFigure(out,model,i)
% Moderate radii make each part visible. Counts use the finer report settings.
f = figure('Color','w','Position',[60 60 1050 360]);
tiledlayout(1,3,'TileSpacing','compact','Padding','compact');
p = contourParts(16,.08,600,true);
[num,den] = tfdata(model,'v');
g = @(s) polyval(num,s)./polyval(den,s);
colors = [.74 .32 .08; .49 .16 .55; 0 .34 .62; .35 .38 .40];
styles = {'--','-','-',':'};
for panel = 1:3
    nexttile;
    if panel<3
        plane('Re s','Im s')
    else
        plane('Re G','Im G')
    end
    for j = 1:4
        v = p{j};
        if panel == 3
            v = g(v);
        end
        directed(v,styles{j},colors(j,:),.42);
    end
    if panel == 1
        title('Full contour, R = 16'); plot(0,0,'kx');
        if i==3
            plot(10,0,'kx','MarkerSize',10); text(10,.9,'+10');
        end
    elseif panel == 2
        xlim([-.13 .16]); ylim([-.15 .15]); plot(0,0,'kx'); title('Rightward indent, ε = 0.08');
    else
        low = g(.1i);
        plot(real(low),imag(low),'o','Color',colors(3,:),'MarkerSize',7);
        text(real(low)+.4,imag(low),'0.1 rad/s','FontSize',10);
        title('Mapped indent in purple');
        plot(0,0,'k+')
    end
end
finish(f,out,sprintf('ex6%02d_detour',i+7))
end

function locusFigure(out,i)
f = figure('Color','w','Position',[80 80 760 390]);
plane('Re s (1/s)','Im s (rad/s)')
if i==1
    K = linspace(0,5,501);
    plot(-ones(size(K)),sqrt(K),'b',-ones(size(K)),-sqrt(K),'b','LineWidth',1.6);
    plot(-1+sqrt(K),0*K,'--r',-1-sqrt(K),0*K,'--r','LineWidth',1.6);
    plot(-1,0,'kx',[-2 0],[0 0],'ks','MarkerSize',9);
    title('From the double pole at −1: positive K (solid), negative K (dashed)')
else
    model = tf([10 10],[1 -10 0]); K = sort([linspace(0,2.4,1000) (6+[-1 1]*sqrt(11))/5]);
    p = rlocus(model,K); plot(real(p.'),imag(p.'),'Color',[0 .34 .62],'LineWidth',1.6);
    plot([0 10],[0 0],'kx','MarkerSize',10);
    plot([0 0],[-1 1]*sqrt(10),'ks','MarkerSize',9);
    plot(-1,0,'ko'); title('Increasing positive gain from poles at 0 and +10')
end
grid on; finish(f,out,sprintf('ex6%02d_locus',i+7))
end
