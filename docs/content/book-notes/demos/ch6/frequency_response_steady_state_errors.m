function report = frequency_response_steady_state_errors(makeFigures)
%FREQUENCY_RESPONSE_STEADY_STATE_ERRORS FPE Section 6.1.2, Example 6.7.
% Requires MATLAB and Control System Toolbox. FALSE computes without figures.
if nargin < 1, makeFigures = true; end
s = tf('s');
L = 10/(s*(s+1)); T = feedback(L,1); S = feedback(1,L);
report.poles = pole(T);
assert(all(real(report.poles)<0),'Closed loop must be stable.');
report.Kv = dcgain(minreal(s*L)); % Algebraic evaluation of lim(s*L), not hardware cancellation.
report.stepError = dcgain(S);
report.rampError = 1/report.Kv;
report.readingFrequency = [.01 1];
report.asymptoteReadings = 10./report.readingFrequency;
report.exactReadings = abs(squeeze(freqresp(L,report.readingFrequency))).';
report.time = (0:.002:30)';
report.reference = report.time;
report.error = lsim(S,report.reference,report.time);
wd = sqrt(39)/2; t = report.time;
report.exactError = .1+exp(-t/2).*(-.1*cos(wd*t)+.95/wd*sin(wd*t));
report.maxTransientDifference = max(abs(report.error-report.exactError));
report.finalError = report.error(end);
report.finalTransientBound = exp(-t(end)/2)*hypot(.1,.95/wd);
if ~makeFigures, return; end
out = fullfile(fileparts(mfilename('fullpath')),'figures');
if ~isfolder(out), mkdir(out); end
% Feedback diagram: unity return enters the lower minus port.
f = figure('Color','w','Position',[100 100 1000 350]);
axes('Position',[0 0 1 1]); axis([0 10 0 3.5]); axis off; hold on
rectangle('Position',[4.3 1.65 2 1.1],'LineWidth',1.5);
text(5.3,2.2,'L(s) = D_c(s)G(s)','HorizontalAlignment','center','FontSize',15);
th = linspace(0,2*pi,160);plot(2.6+.24*cos(th),2.2+.24*sin(th),'k','LineWidth',1.4);
arrow([.7 2.2],[2.34 2.2]); arrow([2.85 2.2],[4.3 2.2]); arrow([6.3 2.2],[9.2 2.2]);
plot([8 8 2.6],[2.2 .65 .65],'k','LineWidth',1.5);arrow([2.6 .65],[2.6 1.94]);
plot(8,2.2,'k.','MarkerSize',18);
text(.8,2.55,'R(s)','FontSize',15);text(3.35,2.55,'E(s)','FontSize',15);text(8.6,2.55,'Y(s)','FontSize',15);
text(2.05,2.45,'+','FontSize',18);text(2.95,1.8,'-','FontSize',22);
text(4.5,.3,'Unity sensor: H(s) = 1','FontSize',14);
saveplot(f,out,'n03_error_feedback');
% Symbolic sketch, with arbitrary plot coordinates and no invented gain.
f = figure('Color','w','Position',[100 100 960 400]);
axes('Position',[.1 .2 .52 .65]);semilogx([.01 1],[1 1],'LineWidth',2);hold on;grid on
xlim([.01 10]);ylim([0 1.8]);yticks(1);yticklabels({'K_p'});xticks([.01 .1 1 10]);xticklabels({});
xlabel('Frequency (log scale)');ylabel('Linear magnitude');title('Type 0: low-frequency asymptote');
text(.025,1.2,'Horizontal: 0 dB/decade','FontSize',13);
annotation(f,'textbox',[.68 .38 .3 .22],'String',{'Unit-step error:','e_{ss} = 1/(1+K_p)'},'EdgeColor','none','FontSize',15);
saveplot(f,out,'n03_type0_asymptote');
w = logspace(-2,1,1400);
f = figure('Color','w','Position',[100 100 1000 580]);
loglog(w,10./(w.*sqrt(1+w.^2)),'LineWidth',1.8);hold on
loglog(w,10./w,'--','LineWidth',1.8);
loglog([.01 1],[1000 10],'ko','MarkerFaceColor','w','MarkerSize',8);
loglog(1,10/sqrt(2),'s','MarkerFaceColor',[0 .45 .74],'MarkerSize',8);
grid on;xlim([.008 12]);ylim([.05 2000]);xlabel('Frequency (rad/s)');ylabel('Linear loop magnitude');
title('Example 6.7: model from FPE Fig. 6.13');
legend('Exact 10/[omega sqrt(1+omega^2)]','Extended low-frequency line 10/omega','Asymptote readings','Exact at 1 rad/s','Location','southwest');
text(.014,1100,'A(0.01) = 1000','FontSize',12);
text(1.3,15,'A(1) = 10','FontSize',12);
text(.18,3.5,'M(1) = 7.07107','FontSize',12);
saveplot(f,out,'n03_ex607_asymptote');
f = figure('Color','w','Position',[100 100 1000 460]);
plot(t,report.exactError,'LineWidth',1.8);hold on
plot(t(1:250:end),report.error(1:250:end),'o','MarkerSize',4);
yline(.1,'--','LineWidth',1.3);grid on;xlabel('Time (s)');ylabel('Tracking error (output units)');xlim([0 30]);
title('Example 6.7: unit-ramp error');legend('Exact transient','MATLAB lsim samples','Steady-state error 0.1','Location','northeast');
saveplot(f,out,'n03_ex607_ramp_error');
end
function arrow(a,b)
quiver(a(1),a(2),b(1)-a(1),b(2)-a(2),0,'k','LineWidth',1.5,'MaxHeadSize',.15);
end
function saveplot(fig,out,name)
exportgraphics(fig,fullfile(out,[name '.svg']),'ContentType','vector');
exportgraphics(fig,fullfile(out,[name '.png']),'Resolution',160);
close(fig);
end
