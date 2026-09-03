%=======================================================================
% blackBox.m
%
%   out = blackBox(t,u,model,figNum)
%   
%   A matlab file to take in an input and produce an output according to 
%   one of several different models. The idea is to try different inputs 
%   and classify the systems as LTI, LTV, nonlinear, etc. All models are 
%   single input, single output. Returns the system output and plots the 
%   input and the response.
%
%   Note that you need to clear your figure manually if you want a fresh
%   one. This way you can put multiple things on the same one easily.
%
%   INPUTS
%       t: Nx1 vector of times
%       u: Nx1 vector of inputs
%       model: index into model number
%       figNum: what figure number to use
%
%   OUTPUTS
%       out: output of the system at timepoints in t
%
%   When you are done reading this, stand up and wait until everyone 
%   else is done.
%=======================================================================
function out = blackBox(t,u,model,figNum)

NUMMODELS = 5;  % number of different models I've coded up
if( model > NUMMODELS )
    disp(['There are only ',num2str(NUMMODELS), ...
        ' possible model choices.']);
    out = [];
    return
end

%=========================================================================
% Generate the output based on the model selection
%=========================================================================
switch model
    case 1
        % Second order LTI system
        wn = 10;
        zeta = 0.1;
        gain = 0.1;
        sys = 0.1*tf(wn^2,[1 zeta*wn wn^2]);
        out = lsim(sys,u,t);
        
    case 2
        % eigth order LTI system because why not
        z = [1 2+i 2-i -3];
        p = [-2 -10 -4-2*i -4+2*i -8-9*i -8+9*i -10+2*i -10-2*i];
        k = 2e5;
        sys = zpk(z,p,k);
        out = lsim(sys,u,t);
        
    case 3
        % how about a nice Van der Pol equation
        ut = t;
        [t,y] = ode45(@(t,y)vdp(t,y,u,ut),t,[0;0]);
        out = y(:,1);
        
    case 4
        % how about a time varying system
        omega = pi;
        a = 1+0.5*sin(omega*t);
        ut = t; at = t;
        [t,out] = ode23s(@(t,y)ltv(t,y,u,ut,a,at),t,0);
        
    case 5
        % for kicks a hybrid model
        y = zeros(size(t));
        for cnt=1:length(t)-1
            if( (y(cnt) < -1) && (y(cnt) > -1.1) )
                y(cnt+1) = 2;
            else
                y(cnt+1) = y(cnt) - 0.005*u(cnt);
            end
            out = y;
        end
end


%=========================================================================
% Plot the response
%=========================================================================
figure(figNum)
hold on
plot(t,u,'linewidth',2);
plot(t,out,'r','linewidth',2);
legend('in','out','Location','NorthEast');
xlabel('time','fontsize',14);
ylabel('signal','fontsize',14);
set(gca,'fontsize',14);

%=========================================================================
% Van der Pol oscillator
%=========================================================================
function dy = vdp(t,y,u,ut);
    % interpolate u
    uval = interp(u,t,ut);
    dy = zeros(2,1);
    dy(1) = y(2);
    dy(2) = -y(1) + uval + 2*(1-y(1)^2)*y(2);
    
%=========================================================================
% Linear time varying system
%=========================================================================
function dy = ltv(t,y,u,ut,a,at);
    % interpolate u
    uval = interp(u,t,ut);
    aval = interp(a,t,at);
    dy = -aval*y + uval;

%=========================================================================
% Hybrid system
%=========================================================================
function dy = hybrid(t,y,u,ut);
    uval = interp(u,t,ut);
    if( y(1) < 0 )
        a = -1;
    elseif( y(1) < 0.2 )
        a = 20;
    elseif( y(1) < 1 )
        a = -5;
    else
        a = -8;
    end
    dy = zeros(2,1);
    dy(1) = y(2);
    dy(2) = a*y(1) + uval;
    
    
%=========================================================================
% Linear interpolation of a function define at time points ut
%=========================================================================
function val = interp(u,t,ut);
    % Get index of closest value
    tmp = abs(ut-t);
    [idt,idt] = min(tmp);
    if( ut(idt) >= t )
        idt = max(idt-1,1);    % take closest without going over
    end
    tInt = (t-ut(idt))/(ut(2)-ut(1));
    val = tInt*u(idt+1) + (1-tInt)*u(idt);
    
    
    