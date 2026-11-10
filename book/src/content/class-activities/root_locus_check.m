function result = root_locus_check(roundNumber, K, tFinal)
%ROOT_LOCUS_CHECK Check the ME404 pair activity after working by hand.
%   ROOT_LOCUS_CHECK(N,K) checks Round N at the gain K you calculated.
%   Rounds 2, 3, and 4 can also be called without a gain.
%   ROOT_LOCUS_CHECK(N,K,TFINAL) extends the response horizon (default 30 s).
%   Requires Control System Toolbox. Times are seconds; settling band is 1%.
arguments
    roundNumber (1,1) double {mustBeInteger,mustBeGreaterThanOrEqual(roundNumber,1),mustBeLessThanOrEqual(roundNumber,6)}
    K (1,1) double {mustBeReal,mustBePositive,mustBeFinite} = 1
    tFinal (1,1) double {mustBeReal,mustBeFinite,mustBeGreaterThanOrEqual(tFinal,1)} = 30
end
if ismember(roundNumber,[1 5 6]) && nargin < 2
    error('ME404:GainRequired','Enter the gain you calculated: root_locus_check(%d,K).',roundNumber);
end
s = tf('s');
result = struct;
switch roundNumber
    case 1
        result.L0 = (s+1)/s^2;
        figure; tiledlayout(1,2)
        nexttile; rlocus(1/s^2); grid on; axis equal
        title('Proportional control: double integrator')
        nexttile; rlocus(result.L0); grid on; axis equal
        title('PD control: double integrator')
        result.T = feedback(K*result.L0,1);
        pair = tf(K,[1 K K]);
        result.comparison = compareResponses( ...
            {result.T,pair},{'Complete PD','Same poles; no zero'},tFinal);
        result.poles = pole(result.T);
        disp('PD closed-loop poles:'); disp(result.poles)
    case 2
        pValues = [12 9 4];
        figure; tiledlayout(1,3)
        result.L0 = cell(1,3);
        for idx = 1:3
            p = pValues(idx);
            result.L0{idx} = (s+1)/(s^2*(s+p));
            nexttile; rlocus(result.L0{idx}); grid on; axis equal
            xlim([-14 1]); ylim([-8 8]); title(sprintf('p = %g',p))
        end
        % Use the same K to compare all three controllers if a gain is given.
        if nargin >= 2
            result.poles = cell(1,3);
            for idx = 1:3
                result.poles{idx} = pole(feedback(K*result.L0{idx},1));
                fprintf('p = %g, K = %.8g\n',pValues(idx),K);
                disp(result.poles{idx})
            end
        end
    case 3
        flex = (s+0.1)^2+6.6^2;
        result.L0 = {(s+1)*((s+0.1)^2+6^2)/(s^2*(s+12)*flex), ...
            (s+1)/(s^2*(s+12)*flex)};
        labels = {'Collocated','Noncollocated'};
        figure; tiledlayout(2,2)
        for idx = 1:2
            nexttile; rlocus(result.L0{idx}); grid on; axis equal
            title(labels{idx})
        end
        for idx = 1:2
            nexttile; rlocus(result.L0{idx}); grid on; axis equal
            xlim([-0.4 0.2]); ylim([6 6.9]); title([labels{idx} ' flexible mode'])
        end
        result.poles = cell(2,2);
        gains = [100 200];
        for idx = 1:2
            for jdx = 1:2
                T = feedback(gains(jdx)*result.L0{idx},1);
                result.poles{idx,jdx} = pole(T);
                fprintf('%s, K = %g, stable = %d\n',labels{idx},gains(jdx),isstable(T));
                disp(result.poles{idx,jdx})
            end
        end
    case 4
        result.L0 = 1/(s*(s+2)*((s+1)^2+4));
        figure; rlocus(result.L0); grid on; axis equal
        title('Complex multiple-root example')
        if nargin >= 2
            result.poles = pole(feedback(K*result.L0,1));
            hold on
            plot(real(result.poles),imag(result.poles),'rs','MarkerSize',9)
            disp('Closed-loop poles (repeated roots may split numerically):'); disp(result.poles)
        end
    case 5
        result.L0 = 1/(s*(s+1));
        figure; rlocus(result.L0); grid on; axis equal
        result.T = feedback(K*result.L0,1);
        result.poles = pole(result.T);
        disp('Selected-gain poles:'); disp(result.poles)
        disp('K = 5 poles:'); disp(pole(feedback(5*result.L0,1)))
        result.comparison = compareResponses( ...
            {result.T,feedback(5*result.L0,1)}, ...
            {sprintf('Selected K = %.6g',K),'K = 5'},tFinal);
    case 6
        result.L0 = 1/(s*(s+2)*(s+4));
        result.T = feedback(K*result.L0,1);
        result.poles = pole(result.T);
        figure; rlocus(result.L0); grid on; axis equal
        disp('All closed-loop poles:'); disp(result.poles)
        % Extract the conjugate pair from the submitted gain, not a stored answer.
        upperPole = result.poles(imag(result.poles) > 1e-7);
        if isscalar(upperPole) && isstable(result.T)
            sigma = -real(upperPole);
            wn = abs(upperPole);
            pair = tf(wn^2,[1 2*sigma wn^2]);
            result.comparison = compareResponses( ...
                {result.T,pair},{'Complete cubic','Unit-DC-gain pair approximation'},tFinal);
        else
            warning('ME404:PairRequired','A stable complex pair is needed for this comparison.');
        end
        result.Kv = K/8;
        fprintf('Kv = %.8g; unit-ramp error = %.8g (if stable)\n',result.Kv,1/result.Kv);
end
end

function summary = compareResponses(models,labels,tFinal)
% Use a common explicit grid, the known final value, and the course definitions.
t = linspace(0,tFinal,ceil(tFinal/0.001)+1)';
metrics = nan(numel(models),3);
figure; hold on
for idx = 1:numel(models)
    if ~isstable(models{idx})
        error('ME404:Unstable','Settling metrics require an asymptotically stable system.');
    end
    finalValue = dcgain(models{idx});
    y = step(models{idx},t);
    % Require an observed in-band tail; never label a truncated response verified.
    % This finite-window check does not prove that no later excursion can occur.
    tailStart = tFinal-min(5,tFinal/6);
    if any(abs(y(t >= tailStart)-finalValue) > 0.01*abs(finalValue))
        warning('ME404:LongTail', ...
            'Metrics withheld for %s. Increase the third argument (currently %g s) and inspect the response.', ...
            labels{idx},tFinal);
    else
        info = stepinfo(y,t,finalValue,'RiseTimeLimits',[0.1 0.9], ...
            'SettlingTimeThreshold',0.01);
        metrics(idx,:) = [info.Overshoot info.RiseTime info.SettlingTime];
    end
    plot(t,y,'LineWidth',1.4)
end
yline(0.99,'k:','HandleVisibility','off');
yline(1.01,'k:','HandleVisibility','off');
grid on; xlabel('Time (s)'); ylabel('Output for a unit step')
legend(labels,'Location','best'); xlim([0 tFinal])
summary = array2table(metrics,'RowNames',labels, ...
    'VariableNames',{'Overshoot_percent','RiseTime_s','SettlingTime_1percent_s'});
disp(summary)
end
