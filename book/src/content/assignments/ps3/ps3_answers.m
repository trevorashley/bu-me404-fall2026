% ME404 Problem Set 3: answer-key calculations and step-response plots.
% Requires MATLAB with Control System Toolbox.
% Run ps3_answers from MATLAB; local functions appear at the end.

s = tf('s');
gains = [0.5 1 2];
t1 = (0:0.002:200)';
motorResults = zeros(numel(gains),3);
figure('Name','Problem 1: motor position servo');
for i = 1:numel(gains)
    k = gains(i);
    T = 0.2*k/(s^2 + 0.104*s + 0.2*k);
    y = step(T,t1);
    info = stepinfo(y,t1,1,'RiseTimeLimits',[0.1 0.9], ...
        'SettlingTimeThreshold',0.01);
    motorResults(i,:) = [info.RiseTime info.Overshoot info.SettlingTime];
    for panel = 1:2
        subplot(1,2,panel); hold on
        plot(t1,y,'DisplayName',sprintf('K = %g',k));
    end
end
for panel = 1:2
    subplot(1,2,panel);
    yline(1,'--','HandleVisibility','off'); grid on
    xlabel('Time (s)'); ylabel('Motor angle (rad)');
    ylim([0 1.85]); legend('show');
end
subplot(1,2,1); xlim([0 16]); title('First rise and overshoot');
yline(0.1,':','HandleVisibility','off');
yline(0.9,':','HandleVisibility','off');
subplot(1,2,2); xlim([0 100]); title('Slow transient decay');
disp(table(gains',motorResults(:,1),motorResults(:,2),motorResults(:,3), ...
    'VariableNames',{'K','RiseTime_s','Overshoot_percent','SettlingTime1pct_s'}));

zetaMin = log(5)/sqrt(pi^2 + log(5)^2);
K20 = 0.052^2/(0.2*zetaMin^2);
KriseEstimate = (1.8/4)^2/0.2;
Krise = fzero(@(k) motorRise(k)-4,[0.02 2]);
fprintf('Overshoot < 20%%: 0 < K < %.9f V/rad\n',K20);
fprintf('Rise < 4 s, numerical boundary: K > %.9f V/rad\n',Krise);
fprintf('Rise < 4 s, moderate-damping estimate: K > %.4f V/rad\n', ...
    KriseEstimate);

Q = s^2 + 4*s + 40;
systems = {40/Q, 40/((s+1)*Q), 120/((s+3)*Q), ...
    20*(s+2)/((s+1)*Q), ...
    (36040/401)*(s^2+s+401)/(Q*(s^2+s+901))};
t2 = (0:0.0005:30)';
results = zeros(5,3);
figure('Name','Problem 2: complete transfer-function responses');
for i = 1:5
    y = step(systems{i},t2);
    info = stepinfo(y,t2,1,'RiseTimeLimits',[0.1 0.9], ...
        'SettlingTimeThreshold',0.01);
    results(i,:) = [info.Overshoot info.RiseTime info.SettlingTime];
    subplot(5,2,2*i-1);
    plot(t2,y); hold on
    yline(1,'--'); yline(0.1,':'); yline(0.9,':');
    xlim([0 3]); ylim([0 1.45]); grid on
    ylabel(sprintf('y_%d(t)',i));
    if i == 1, title('Unit-step responses'); end
    subplot(5,2,2*i);
    plot(t2,y); hold on
    yline(1,'--'); yline(0.99,':'); yline(1.01,':');
    xline(info.SettlingTime,':');
    xlim([0 8]); ylim([0.965 1.035]); grid on
    if i == 1, title('1% settling detail'); end
end
subplot(5,2,9); xlabel('Time (s)');
subplot(5,2,10); xlabel('Time (s)');
disp(table((1:5)',results(:,1),results(:,2),results(:,3), ...
    results(:,1)<=5,results(:,2)<=0.5,results(:,3)<=2.5, ...
    'VariableNames',{'System','Overshoot_percent','RiseTime_s', ...
    'SettlingTime1pct_s','PassOvershoot','PassRise','PassSettling'}));

% Problem 3: one strictly stable point satisfying p > z > 0 and K*K0 > p*a^2/z.
a = 1; K0 = 1; z = 1; p = 2; K = 3;
disp('Problem 3 example: roots of the full characteristic polynomial');
disp(roots([1 p K*K0-a^2 K*K0*z-p*a^2]));

% Problem 4: all three stage gains vary together; beta values stay fixed.
K = 10;
c = 10^(1/3);
beta1 = 0.01;
beta2 = 1/c - 0.1;
beta3 = 0.099;
overallGains = [-beta1*K^3; -(K/(1+K*beta2))^3; -K^3/(1+beta3*K^3)];
sensitivityK = [3; 3/(1+K*beta2); 3/(1+beta3*K^3)];
% beta1 is an input scaling gain; its sensitivity is included for comparison.
sensitivityBeta = [1; -3*K*beta2/(1+K*beta2); -beta3*K^3/(1+beta3*K^3)];
disp(table({'a';'b';'c'},[beta1;beta2;beta3],overallGains, ...
    sensitivityK,sensitivityBeta,'VariableNames', ...
    {'Topology','Beta','OverallGain','SensitivityK','SensitivityBeta'}));

function tr = motorRise(k)
    % This root calculation is for the underdamped branch, k > 0.01352.
    wd = sqrt(0.2*k - 0.052^2);
    y = @(t) 1-exp(-0.052*t).*(cos(wd*t)+0.052/wd*sin(wd*t));
    tp = pi/wd;
    t10 = fzero(@(t) y(t)-0.1,[0 tp]);
    t90 = fzero(@(t) y(t)-0.9,[0 tp]);
    tr = t90-t10;
end
