% We are using the BlackScholes function from github and please run this
% code section by section. Thank you, sir.
%% Question 1
clear
load DerivativeAssignment.mat
%a)
r=0.00071;
S0=1376.92;
T=21/252;
%b)
CallPricewithNodiv=zeros(1,80);
PutPricewithNodiv=zeros(1,82);
for i=1:80
    [CallPricewithNodiv(i), ~, ~, ~, ~, ~, ~, ~, ~, ~]=BlackScholes(S0, StrikeCall(i), r, 0, T, ImpliedVolCall(i));
end
for i=1:82
    [~, PutPricewithNodiv(i), ~, ~, ~, ~, ~, ~, ~, ~]=BlackScholes(S0, StrikePut(i), r, 0, T, ImpliedVolPut(i));
end
CallPrice=CallPricewithNodiv(63)
%c)
%Mid Point
MidPointCall=(CloseBidPriceCall+CloseAskPriceCall)/2;
MidPointPut=(CloseBidPricePut+CloseAskPricePut)/2;
%g for call I did't notice that we are choosing only one option at first,0 so I wrote
%a loop. It may take a little time to run it. Please wait.
gcall=[];
for i=1:80
syms g;
g=vpasolve(BlackScholes(S0, StrikeCall(i), r, g, T, ImpliedVolCall(i))==MidPointCall(i),g);
g=double(g);
gcall=[gcall;g];
end
%g for put
gput=[];
for i=1:82
syms g;
[~, eq, ~, ~, ~, ~, ~, ~, ~, ~]=BlackScholes(S0, StrikePut(i), r, g, T, ImpliedVolPut(i));
g=vpasolve(eq==MidPointPut(i),g);
g=double(g);
gput=[gput;g];
end
%
DividendYieldCall=gcall(63)
DividendYieldPut=gput(41);
%% Question 2
clear
S0=1376.92;
K=1375;
SigmaCall=0.16476;
DividendYieldCall=0.0381;
T=21/252;
r=0.00071;
CallSigma=zeros(1,20);
CallTime=zeros(1,6);
CallRate=zeros(1,57);
%a)
sigma=0.05:0.05:1;
for i=1:20
    [CallSigma(i), ~, ~, ~, ~, ~, ~, ~, ~, ~]=BlackScholes(S0,K,r,DividendYieldCall,T,sigma(i));
end
plot(sigma,CallSigma,"bo-","LineWidth",2)
xlabel('Sigma')
ylabel('CallPrice')
title('CallPrice-Sigma');
%b)
figure;
T=[1/52 1/12 1/4 1/2 1 5];
for i=1:6
    [CallTime(i), ~, ~, ~, ~, ~, ~, ~, ~, ~]=BlackScholes(S0,K,r,DividendYieldCall,T(i),SigmaCall);
end
plot(T,CallTime,"bo-",LineWidth=2)
xlabel('T')
ylabel('CallPrice')
title('CallPrice-T');
%c)
figure;
T=21/252;
r=0:0.0025:0.14;
for i=1:57
    [CallRate(i), ~, ~, ~, ~, ~, ~, ~, ~, ~]=BlackScholes(S0,K,r(i),DividendYieldCall,T,SigmaCall);
end
plot(r,CallRate,"bo-","LineWidth",2)
xlabel('r')
ylabel('CallPrice')
title('CallPrice-Interest Rate');
%% Question 3
clear
K=1375;
r=0.00071;
T=21/252;
%Call Option
g=0.0381;
Sigmacall=0.16476;
x=0.4:0.05:1.6;
S=zeros(1,25);
BlackScholesCallprice=zeros(1,25);
IntrinsicvalueCall=zeros(1,25);
for i=1:25
    S(i)=1376.92*x(i);
    [BlackScholesCallprice(i), ~, ~, ~, ~, ~, ~, ~, ~, ~] = BlackScholes(S(i), K, r, g, T, Sigmacall);
    IntrinsicvalueCall(i)=max(S(i)-K,0);
end
hold on
plot(S,IntrinsicvalueCall,"ro-","LineWidth",2);
plot(S,BlackScholesCallprice,"bo-","LineWidth",2);
legend('IntrinsicvalueCall','BlackScholesCallprice');
xlabel("S");
ylabel("Value");
title("CALL OPTION");
hold off
%Put Option
BlackScholesPutprice=zeros(1,25);
IntrinsicvaluePut=zeros(1,25);
g=0.0005;
Sigmaput=0.16479;
for i=1:25
    [~, BlackScholesPutprice(i), ~, ~, ~, ~, ~, ~, ~, ~] = BlackScholes(S(i), K, r, g, T, Sigmaput);
    IntrinsicvaluePut(i)=max(K-S(i),0);
end
figure
hold on
plot(S,IntrinsicvaluePut,"ro-","LineWidth",2);
plot(S,BlackScholesPutprice,"bo-","LineWidth",2);
legend('IntrinsicvaluePut','BlackScholesPutprice');
xlabel("S");
ylabel("Value");
title("PUT OPTION");
hold off
%% Question 4
clear
ImpliedVol=0.16476;
%
% Sample script to load daily returns; GARCH(1,1) model volatility
% and compare to the VIX and future realised vol.
%
% Richard J. McGee (richard.mcgee@ucd.ie)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%*******************!Set Dates Here!***************************************
tradeDate = datenum('19042012','ddmmyyyy');
%                   ~~~~~~~~~~
expiryDate = datenum('19052012','ddmmyyyy');
%                   ~~~~~~~~~~

%*************!Set Sample Size for GARCH Fitting Here!*********************
S = 1000; % the number of previous returns used to fit the GARCH model
%   ~~~~

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Load S&P500 data
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sp500 = csvread('SPXDaily1950.csv',1);
indexdates = x2mdate(sp500(:,1));
index = sp500(:,6);
rm =log(index(2:end)./index(1:end-1));
sp500Dates = indexdates(2:end);
%
fprintf('************************************************************* \n');
fprintf('Loaded Daily S&P500 data from %s to %s \n', ...
    datestr(min(sp500Dates)),datestr(max(sp500Dates)));

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Load VIX data
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
VIX = csvread('VIX.csv',1);
vixDates = x2mdate(VIX(:,1));
VIX = VIX(:,6);

fprintf('************************************************************* \n');
fprintf('Loaded VIX data from %s to %s \n', ...
    datestr(min(vixDates)),datestr(max(vixDates)));
fprintf('************************************************************* \n');

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Select Garch(1,1)
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ToEstMdl = garch(1,1); % tells Matlab what model to estimate

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% index using provided dates and create correct return samples
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
d1 = find(sp500Dates == tradeDate);
d2 = find(sp500Dates <= expiryDate,1,'last');
d3 = find(vixDates == tradeDate);
% historical returns up to the forecast date to estimate the GARCH model
ret_h  = rm(d1-(S-1):d1);
% realised returns over the following month (being forecast)
ret_r  = rm(d1+1:d2);nRets = numel(ret_r);
% calculate the 'future' realised vol the model is trying to forecast
timeFactor = 252/nRets; %(to annualise the variance)
realisedVol = sqrt(sum(ret_r.^2)*timeFactor); 
% Estimate a GARCH(1,1)
fprintf('Fitting GARCH Model:\n');
EstMdl = estimate(ToEstMdl,ret_h);

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Variance sums over time - sum variance forecasts, convert to annualised
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
forecastVariance = sum(forecast(EstMdl,nRets,'Y0',ret_h)); % monthly variance
forecastVol = (timeFactor*forecastVariance).^0.5; % annualised vol
vixVol = VIX(d3);

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Print the results
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fprintf('************************************************************* \n');
fprintf('GARCH(1,1) forecast Vol: %.2f \n', 100*forecastVol);
fprintf('************************************************************* \n');
fprintf('VIX: %.2f \n', vixVol);
fprintf('************************************************************* \n');
fprintf('Realised Vol: %.2f \n', 100*realisedVol);
fprintf('************************************************************* \n');
fprintf('Implied Vol: %.2f \n',100*ImpliedVol);
%In question 4, we use the close ask price for the options to calculate the net cost and maximum return.
%% Straddle
clear
x=1250:1500;
c=zeros(1,251);
p=zeros(1,251);
S=1375;
CallPriceStraddle=39.1;
PutPriceStraddle=19.5;
for  i=1:251
c(i)=max((x(i)-CallPriceStraddle-S),0-CallPriceStraddle);
end
hold on
plot(x,c,"r--")
for i=1:251
    p(i)=max((S-PutPriceStraddle-x(i)),0-PutPriceStraddle);
end
plot(x,p,"b--")
plot(x,c+p,"k-")
plot(1295,c(46)+p(46),'o',LineWidth=2)
title("Straddle")
xlabel("Stock Price")
ylabel("Profit & Loss")
legend("Call","Put")
axis([1250 1500 -80 60])
grid on;
hold off
NetCostofStraddle=min(c+p)
ResultingPL=c(46)+p(46)
%% Strangle
clear
c=zeros(1,251);
p=zeros(1,251);
x=1250:1500;
Sput=1350;
Scall=1400;
CallPriceStrangle=13.1;
PutPriceStrangle=42.9;
for  i=1:251
c(i)=max((x(i)-CallPriceStrangle-Scall),0-CallPriceStrangle);
end
figure
hold on
plot(x,c,"r--")
for i=1:251
    p(i)=max((Sput-PutPriceStrangle-x(i)),0-PutPriceStrangle);
end
plot(x,p,"b--")
plot(x,c+p,"k-")
plot(1295,c(46)+p(46),'o',LineWidth=2)
title("Strangle")
xlabel("Stock Price")
ylabel("Profit & Loss")
legend("Call","Put")
axis([1250 1500 -80 60])
grid on;
hold off
NetCostofStrangle=min(c+p)
ResultingPL=c(46)+p(46)
%% Butterfly Spread
clear
figure
a=zeros(1,251);
b=zeros(1,251);
c=zeros(1,251);
x=1250:1500;
Sa=1350;
Sb=1375;
Sc=1400;
Volcall=0.16476;
CallAskPriceA=39.1;
CallAskPriceB=26.1;
CallAskPriceC=15.4;
for  i=1:251
a(i)=max((x(i)-CallAskPriceA-Sa),0-CallAskPriceA);
end
for  i=1:251
b(i)=max((x(i)-CallAskPriceB-Sb),0-CallAskPriceB);
end
for  i=1:251
c(i)=max((x(i)-CallAskPriceC-Sc),0-CallAskPriceC);
end
hold on
plot(x,a-2*b+c,"k-")
plot(1295,a(46)+c(46)-2*b(46),'o',LineWidth=2)
title("Butterfly Spread")
xlabel("Stock Price")
ylabel("Profit & Loss")
axis([1250 1500 -5 25])
grid on;
hold off
MaxReturnofButterfly=max(a-2*b+c)
NetCostofButterfly=min(a-2*b+c)
ResultingPL=a(46)+c(46)-2*b(46)
%% Question 5
clear;
K =1375;
TC = 1e-4;
dt = 1/365;
% Time to expiry on each date to expiry
timeToExp =[30;29;26;25;24;23;22;19;18;17;16;15;12;11;10;9;8;5;4;3;2;1;0]/365;
%Index on each date to expiry

St = [1376.920044;1378.530029;1366.939941;1371.969971;1390.689941;1399.97998;
1403.359985;1397.910034;1405.819946;1402.310059;1391.569946;1369.099976;1369.579956;
1363.719971;1354.579956;1357.98999;1353.390015;1338.349976;1330.660034;1324.800049;
1304.859985;1295.219971;1295.219971];
  
subplot(2,1,1),plot(St); hold all; plot(0*St+K);title('Index Level');
axis([-inf,inf,-inf,inf]); grid on;
r = 0.00071;
y=0.0381;
Ca = 26.1;
IV = 0.16476;
N = numel(St)-1;
deltah = zeros(N-1,1);
fprintf('------------------------------------------------------------------\n');
fprintf('Delta Hedging (Using Implied Volatility)\n');
fprintf('------------------------------------------------------------------\n');

% Call premium

CallPremium = Ca * (1-TC);

BankBalance = CallPremium;
stockCosts=0;
% Get the vector of delta positions
for t =1:N-1
    S0 = St(t);
    t2e = timeToExp(t);
    [ ~, deltah(t), ~ ] = blackScholesCallPrice( K, t2e, S0, r, y, IV ); 
    if t>1
        oldStockPosition = deltah(t-1);
    else
        oldStockPosition = 0;
    end
    amtBuy = (deltah(t)-oldStockPosition)*St(t);
    stockCosts = amtBuy +abs(amtBuy)*TC;
    BankBalance = BankBalance*exp(r*dt) - stockCosts;

    fprintf(' t= %i; delta = %.2f; bought $ %.2f of the index; Bank $ %.2f \n', t,deltah(t),amtBuy,BankBalance);
   
end

subplot(2,1,2),plot(deltah(1:end));
axis([-inf,inf,-inf,inf]); grid on;
title('Delta Position');
fprintf('------------------------------------------------------------------\n');

CallPayoff = max(0,St(end)-K);
profit = deltah(end)*St(end) +BankBalance - CallPayoff;

fprintf('Total Hedge Profit: $ %.2f \n', profit);
fprintf('------------------------------------------------------------------\n');
clear;
figure;
K =1375;
TC = 1e-4;
dt = 1/365;
% Time to expiry on each date to expiry
timeToExp =[30;29;26;25;24;23;22;19;18;17;16;15;12;11;10;9;8;5;4;3;2;1;0]/365;
%Index on each date to expiry

St = [1376.920044;1378.530029;1366.939941;1371.969971;1390.689941;1399.97998;
1403.359985;1397.910034;1405.819946;1402.310059;1391.569946;1369.099976;1369.579956;
1363.719971;1354.579956;1357.98999;1353.390015;1338.349976;1330.660034;1324.800049;
1304.859985;1295.219971;1295.219971];
  
subplot(2,1,1),plot(St); hold all; plot(0*St+K);title('Index Level');
axis([-inf,inf,-inf,inf]); grid on;
r = 0.00071;
y=0.0381;
Ca = 26.1;
IV = 0.1745;
N = numel(St)-1;
deltah = zeros(N-1,1);
fprintf('------------------------------------------------------------------\n');
fprintf('Delta Hedging (Using Forecast Volatility)\n');
fprintf('------------------------------------------------------------------\n');

% Call premium

CallPremium = Ca * (1-TC);

BankBalance = CallPremium;
stockCosts=0;
% Get the vector of delta positions
for t =1:N-1
    S0 = St(t);
    t2e = timeToExp(t);
    [ ~, deltah(t), ~ ] = blackScholesCallPrice( K, t2e, S0, r, y, IV ); 
    if t>1
        oldStockPosition = deltah(t-1);
    else
        oldStockPosition = 0;
    end
    amtBuy = (deltah(t)-oldStockPosition)*St(t);
    stockCosts = amtBuy +abs(amtBuy)*TC;
    BankBalance = BankBalance*exp(r*dt) - stockCosts;

    fprintf(' t= %i; delta = %.2f; bought $ %.2f of the index; Bank $ %.2f \n', t,deltah(t),amtBuy,BankBalance);
   
end

subplot(2,1,2),plot(deltah(1:end));
axis([-inf,inf,-inf,inf]); grid on;
title('Delta Position');
fprintf('------------------------------------------------------------------\n');

CallPayoff = max(0,St(end)-K);
profit = deltah(end)*St(end) +BankBalance - CallPayoff;

fprintf('Total Hedge Profit: $ %.2f \n', profit);
fprintf('------------------------------------------------------------------\n');