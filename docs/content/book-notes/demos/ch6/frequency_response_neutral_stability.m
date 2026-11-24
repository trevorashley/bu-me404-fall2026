function report = frequency_response_neutral_stability(makeFigures)
%FREQUENCY_RESPONSE_NEUTRAL_STABILITY Compare three gains in FPE 6.2.
% Pass false for numerical results only. Times are in s, frequencies in rad/s.
if nargin == 0
    makeFigures = true;
end
s = tf('s');
G = 1/(s*(s+1)^2);
gains = [0.1 2 10];
horizons = [50 20 10];
report = repmat(struct('gain',0,'loopAtOne',0,'poles',[], ...
    'time',[],'step',[]),size(gains));
for k = 1:numel(gains)
    L = gains(k)*G;
    T = feedback(L,1);
    t = (0:0.01:horizons(k))';
    report(k).gain = gains(k);
    report(k).loopAtOne = evalfr(L,1i);
    report(k).poles = pole(T);
    report(k).time = t;
    report(k).step = step(T,t);
end
if ~makeFigures
    return
end
out = fullfile(fileparts(mfilename('fullpath')),'figures');
if ~isfolder(out)
    mkdir(out);
end
colors = [0.05 0.36 0.60; 0.08 0.48 0.33; 0.72 0.27 0.09];
labels = "K = " + string(gains);

f = figure('Color','w','Position',[80 80 900 350]);
tiledlayout(1,2);
nexttile; axis equal; axis([0 10 0 5]); axis off; hold on
title('Unity negative feedback');
rectangle('Position',[1.8 2.6 .6 .6],'Curvature',[1 1]);
rectangle('Position',[4 2.35 2.2 1.1]);
text(5.1,2.9,'KG(s)','HorizontalAlignment','center');
arrow([.6 2.9],[1.8 2.9]); arrow([2.4 2.9],[4 2.9]);
arrow([6.2 2.9],[9.4 2.9]);
plot([7.8 7.8 2.1],[2.9 1 1],'k-'); arrow([2.1 1],[2.1 2.6]);
plot(7.8,2.9,'k.','MarkerSize',15);
text(.55,3.35,'R'); text(3,3.35,'E'); text(9,3.35,'Y');
text(1.4,3.2,'+'); text(2.5,2.35,'−');
nexttile; hold on; axis([-2 2 -2 2]); axis square
xline(0); yline(0); plot([0 0],[-1 1],'kx','MarkerSize',10,'LineWidth',2);
yticks([-1 0 1]); yticklabels({'−ω_0','0','+ω_0'}); xticks(0)
xlabel('Real part (1/s)'); ylabel('Imaginary part (rad/s)');
title('A conjugate pair at the boundary');
saveplot(f,out,'feedback_boundary');

w = logspace(-1.5,1.5,601);
Gj = squeeze(freqresp(G,w));
f = figure('Color','w','Position',[80 80 820 600]);
tiledlayout(2,1,'TileSpacing','compact');
nexttile;
for k = 1:numel(gains)
    semilogx(w,20*log10(abs(gains(k)*Gj)),'Color',colors(k,:), ...
        'LineWidth',1.8,'DisplayName',labels(k)); hold on
    semilogx(1,20*log10(abs(report(k).loopAtOne)),'o', ...
        'Color',colors(k,:),'HandleVisibility','off');
end
xline(1,':','HandleVisibility','off'); yline(0,':','HandleVisibility','off');
ylabel('Loop magnitude (dB)'); title('Changing gain shifts the magnitude');
legend('Location','southwest'); grid on; xlim(w([1 end]));
nexttile;
semilogx(w,rad2deg(unwrap(angle(Gj))),'k','LineWidth',1.8); hold on
semilogx(1,-180,'ko'); xline(1,':'); yline(-180,':'); grid on
yticks([-270 -225 -180 -135 -90]); ylim([-275 -85]); xlim(w([1 end]));
xlabel('Frequency (rad/s)'); ylabel('Loop phase (deg)'); title('Shared phase for all three gains');
saveplot(f,out,'bode_gains');

f = figure('Color','w','Position',[80 80 820 540]);
% Include the breakaway gain so the two real branches meet on the plot.
gainGrid = unique([0 logspace(-6,log10(18),1000) 4/27 gains]);
p = rlocus(G,gainGrid);
plot(real(p.'),imag(p.'),'Color',[.40 .44 .48],'HandleVisibility','off'); hold on
xline(0,'k:','HandleVisibility','off'); yline(0,'k:','HandleVisibility','off');
markers = {'o','s','d'};
for k = 1:numel(gains)
    poles = report(k).poles;
    plot(real(poles),imag(poles),markers{k},'LineWidth',1.8, ...
        'Color',colors(k,:),'MarkerSize',8,'DisplayName',labels(k));
end
a = rlocus(G,4); b = rlocus(G,6);
% At these gains the branches are distinct; match each pole to its neighbor.
for i = 1:numel(a)
    [~,j] = min(abs(b-a(i)));
    arrow([real(a(i)) imag(a(i))],[real(b(j)) imag(b(j))]);
end
axis equal; grid on; xlabel('Real part (1/s)'); ylabel('Imaginary part (rad/s)');
title('Closed-loop poles as K increases'); legend('Location','northwest');
saveplot(f,out,'root_locus');

f = figure('Color','w','Position',[80 80 820 690]);
tiledlayout(3,1,'TileSpacing','compact');
regime = ["settling to the command" "sustained oscillation" "growing oscillation"];
for k = 1:numel(gains)
    nexttile;
    plot(report(k).time,report(k).step,'Color',colors(k,:),'LineWidth',1.6);
    yline(1,':'); grid on; ylabel('Output y');
    xlim([0 horizons(k)]); xlabel('Time (s)');
    title(sprintf('K = %g   |   %s',gains(k),regime(k)));
end
saveplot(f,out,'step_responses');
end

function arrow(a,b)
quiver(a(1),a(2),b(1)-a(1),b(2)-a(2),0,'k','MaxHeadSize',.65, ...
    'LineWidth',1.4,'HandleVisibility','off');
end

function saveplot(f,out,stem)
name = fullfile(out,['n04_' stem]);
exportgraphics(f,[name '.svg'],'ContentType','vector');
exportgraphics(f,[name '.png'],'Resolution',160);
close(f)
end
