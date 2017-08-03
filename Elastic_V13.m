function Elastic_V13
close all;
clear all;

%%%%%%%%%%%%% Beginging of Calibration %%%%%%%%%%%%%%%%%%
fileId = 1;
%  base_1, base_2, base_3 .......
startVal = [9]; % pick from figure 1
endValmid = [307]; % pick from figure 1
% endVal = [1];

rgb = imread('1.png');
figure(1);
imshow(rgb);

startVal = startVal(fileId);
endValmid = endValmid(fileId);

minFactor = 10;     % Threshold for begining and end of letters, interms of value  
maxFactor = 0.2;    % Threshold for features of importance, interms of value      
clustLen = 1;       % min gap between peaks [features of important]
gradThld = 1e3;     % Grad Threshold value for selection of valleys 
wrdGap = 10; %10     % num of pixels between words. Seeting a very low values will pick gaps between letters. too high and gaps between words will be missed-> 10
rThreshold = 0.8;   % Threshold Pearsons'Corr Coeff [r] value of matching
fwinLen = 5;        % Median filter window length

% Way to select to the best colour [r, g, or b] that would highlight features
highest = -1e-5;
for tempk = 1:3
    temp = std(reshape(double(rgb(:,:,tempk)),[],1)); % standard deviation
    if temp > highest
        highest = temp;
        colourInd = tempk;
    end
end
% select the best colour 
rawData = (rgb(:,:,colourInd));

[p q] = size(rawData);

% median filter to reduce noise
K = medfilt2(uint8(rawData),[fwinLen fwinLen]);
rawData =  double(K);
baseTemplate = rawData(:,startVal);
figure(2);
imshow(K);

% Calculate the maximum value
maxErr = 1e-5;
for k= startVal:1:endValmid 
    tempc  = rawData(:,k);
    errArr(k-startVal+1) = sum((tempc - baseTemplate).^2);
    if errArr(k-startVal+1) > maxErr
        maxErr = errArr(k-startVal+1);
    end
end

figure(3); 
plot(startVal:(startVal+length(errArr)-1),errArr,'-k');grid on;

% set of peaks, initialisation : main components
lastPos = 0;
lastMag = 1e-5;
countMax = 0;
maxArray = zeros(100,2); % (position, value)
for k = 2:length(errArr)-1
    % peaks search
    if errArr(k)> maxFactor*maxErr
        if errArr(k) > errArr(k-1) && errArr(k) > errArr(k+1) % check Maximums           
            if ((errArr(k) - errArr(k-2))*(errArr(k+2) - errArr(k))) <= 0  % eliminate local maximuma from the maximum identified
                if k - lastPos > clustLen
                    countMax = countMax+1;
                    lastPos = k;
                    lastMag = errArr(k);
                    maxArray(countMax,1) = lastPos;
                    maxArray(countMax,2) = lastMag;
                else
                    if errArr(k) >= lastMag  
                        lastMag = errArr(k);
                        lastPos = k;
                        maxArray(countMax,1) = lastPos;
                        maxArray(countMax,2) = lastMag;
                    end
                end
            end
        end
    end 
end

% set of valleys initialisation : main components
minErr = errArr(endValmid- startVal + 1);
minArray = zeros(100,2); % start and end of words in 2 columnss
flag = 0;
countMin = 1;
status = 0;
% figure(111);
% plot(startVal:(startVal+length(errArr)-1),gradient(errArr)); grid on;
% figure(112);
% plot(startVal:(startVal+length(errArr)-1),gradient(gradient(errArr))); grid on;

% % new addition
% gradVal = gradient(errArr);
% grad2Val = gradient(gradVal);
% count = 0;
% status = 0;
% for k = 3:length(errArr)-1
%    % Valleys search
%    if errArr(k) < minFactor*minErr
%        if status  == 0;
%            count = count +1;
%            status = 1;
%            tData(count,1) = k;
%        else
%            tData(count,2) = k;
%        end
%    else
%        status  = 0;
%    end 
% end
% 
% 


for k = 3:length(errArr)-1
   % Valleys search
   if errArr(k) < minFactor*minErr
       if flag == 0; % encountering a new valley or interesting area for the fist time
           flag = 1;
           gradVal =  (errArr(k  +1) - errArr(k  -1))/2; % put  gradVal(k)
           if abs(gradVal) < gradThld % thershold value for gradient
               status = 1;  % within the background region and about to enter a letter
           else
               if gradVal < 0 % put mean of gradVal(k: k-3) %mean(gradVal(k-2):gradVal(k)) < 0 % put mean of gradVal(k: k-3)
                   status = 1;
                   minArray(countMin,2) = k + 1; % -1 is added to stick to letter
                   countMin = countMin + 1;
               else
                   status = 1; % entering a letter
               end
           end
       else
           gradVal =  (errArr(k  +1) - errArr(k  -1))/2;  % put gradVal(k)
            if status == 1 % store values , haiyoo
                if abs(gradVal) < gradThld % entering a letter, so keep on changing till last index of proper range is added
                   minArray(countMin,1) = k + 1; % +1 is added to stick to letter
                end
            else
                display('some weired shit is happening');
            end
       end       
   else
       if  countMin > 1 && (minArray(countMin,1) -  minArray(countMin-1,2) < wrdGap)
           if flag == 1
               countMin = countMin - 1;
               flag = 0;
           else
               pause;
           end
       else
            if flag  == 1 
                flag = 0;
            end
       end
   end   
end
if countMin > 1
    countMin = countMin -1;
end
figure(3); hold on;
plot(maxArray(1:countMax,1)+startVal-1,maxArray(1:countMax,2),'.b','MarkerSize',15);
figure(3); hold on;
plot(startVal + floor(minArray(1:countMin,1)) -1,errArr(floor(minArray(1:countMin,1))),'.g','MarkerSize',15);
grid on;
figure(3); hold on;
plot(startVal + floor(minArray(1:countMin,2)) -1,errArr(floor(minArray(1:countMin,2))),'.r','MarkerSize',15);
grid on;

for inc = 1:countMin
    figure(1); hold on;
    line([minArray(inc,1) + startVal - 1, minArray(inc,1)+ startVal - 1], [1 p],'Color',[.0 .9 .0]);
    figure(1); hold on;
    line([minArray(inc,2) + startVal - 1, minArray(inc,2)+ startVal - 1], [1 p],'Color',[.9 .0 .0]);
end


gap = minArray(countMin,2) - minArray(1,1) + 1;

if countMax < 10
    display('Number of features < 10. Lower maxFactor value and re-run');
    % but you can continue. :) :) :) 
end
pcmp = zeros(countMax,1);
for k = 1:countMax 
    pcmp(k) = (maxArray(k,1) - minArray(1,1) + 1)/gap;
end
maxArray = maxArray(1:countMax,2)';
% 
% if countMax < 11
%     display('Number of features < 10. Lower maxFactor value and re-run');
%     countMax = 11;
%     pcmp = [0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75];
%     maxArray = errArr(minArray(1,1) + 1 + floor(gap*pcmp));
% else
%     pcmp = zeros(countMax,1);
%     for k = 1:countMax 
%         pcmp(k) = (maxArray(k,1) - minArray(1,1) + 1)/gap;
%     end
%     maxArray = maxArray(1:countMax,2)';
% end

% max Array is redefined, We better use better terms



% Important Pararameters are : maxArray,  pcmp, countMax, countMin;
%%%%%%%%%%%%% End of Calibrations %%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%% Continuously running program %%%%%%%%%%%%%
clear errArr minArray;
% baseTemplate is the same as before
rgb = imread('1.png');
figure(200);
imshow(rgb);
if length(rgb(:,1,1)) ~= p
    if length(rgb(:,1,1)) < p
        rawData = (rgb(:,:,colourInd));
        baseTemplate = baseTemplate(1:length(rgb(:,1,1)));
    else
        rawData = (rgb(1:p,:,colourInd));
    end
else
    rawData = (rgb(:,:,colourInd));
end

% rawData = uint8(0.2989*double(rgb(:,:,1)) + 0.5870*double(rgb(:,:,2)) + 0.1140*double(rgb(:,:,3)));
figure(10);
imshow(rawData);
[p q] = size(rawData);
endVal = q-5;
% median filter to reduce noise
K = medfilt2(uint8(rawData),[fwinLen fwinLen]);
figure(11);
imshow(K);
rawData =  double(K);

startVal = 1;
for k= startVal:1:endVal    % 1 D signal for entire image
    tempc  = rawData(:,k);
    errArr(k-startVal+1) = sum((tempc - baseTemplate).^2);
end

if min(errArr) > minErr
    minErr = min(errArr); %New addition
end

figure(5);
plot(errArr,'-k');
grid on;

minArray = zeros(100,2); % start and end of words in 2 columnss
flag = 0;
count = 1;
status = 0;

for k = startVal + 1:length(errArr)-1
   % Valleys search
   if errArr(k - startVal +1) < minFactor*minErr
       if flag == 0; % encountering a new valley or interesting area for the fist time
           flag = 1;
           gradVal =  (errArr(k - startVal +1 +1) - errArr(k - startVal +1 -1))/2;
           if abs(gradVal) < gradThld % thershold value for gradient
               status = 1;  % within the background region and about to enter a letter
           else
               if gradVal < 0
                   status = 1;
                   minArray(count,2) = k + 1; % -1 is added to stick to letter
                   count = count + 1;
               else
                   status = 1; % entering a letter
               end
           end
       else
           gradVal =  (errArr(k - startVal +1 +1) - errArr(k - startVal +1 -1))/2; 
            if status == 1 % store values , haiyoo
                if abs(gradVal) < gradThld % entering a letter, so keep on changing till last index of proper range is added
                   minArray(count,1) = k + 1; % +1 is added to stick to letter
                end
             else
                display('holy buckets !!!!!!!!!!!!!! ');
            end
       end       
   else 
       if  count > 1 && (minArray(count,1) -  minArray(count-1,2) < wrdGap) % -ve one are also counted here 
           if flag == 1
               count = count - 1;
               flag = 0;
           else
               pause;
           end
       else
            if flag  == 1 
                flag = 0;
            end
       end
   end   
end

if minArray(count,2) == 0
    count = count -1;
end
countStrt = 1;
if minArray(1,1) == 0
    countStrt = 2;
end

for inc = 1:count  % draw all the posibilities 
    figure(10); hold on;
    line([minArray(inc,1), minArray(inc,1)], [1 p],'Color',[.0 .9 .0]);
    figure(10); hold on;
    line([minArray(inc,2), minArray(inc,2)], [1 p],'Color',[.9 .0 .0]);
end

figure(5); hold on;
plot(floor(minArray(countStrt:count,1)) ,errArr((minArray(countStrt:count,1))),'.g','MarkerSize',15);
grid on;
figure(5); hold on;
plot(floor(minArray(countStrt:count,2)) ,errArr((minArray(countStrt:count,2))),'.r','MarkerSize',15);
grid on;

itrns = count - countStrt + 1;
r  = zeros(itrns,1);
x_bar = mean(maxArray);

% comparison using Pearsons correlation coefficient
for k = countStrt:itrns + countStrt - 1
    indBgn = k ;
    indEnd = (countMin - 1 + k) + 2;
    if indEnd > itrns + countStrt - 1
        indEnd = itrns + countStrt - 1;     
    end
    for index = indBgn:1:indEnd
        tempdata = errArr(minArray(k,1) + floor(pcmp.*(minArray(index,2) - minArray(k,1))));
        tempc_bar = mean(tempdata);
        num_sum = sum((maxArray - x_bar).*(tempdata -tempc_bar));
        den_sum = sqrt(sum((maxArray - x_bar).^2))*sqrt(sum((tempdata -tempc_bar).^2));
        r(k-countStrt+1,index - indBgn + 1) = abs(num_sum./den_sum);
        if   r(k-countStrt+1,index - indBgn + 1) > rThreshold
            figure(11); hold on;
            line([minArray(k,1), minArray(k,1)], [1 p],'Color',[.0 1 .0]);
            figure(11); hold on;
            line([minArray(index,2), minArray(index,2)], [1 p],'Color',[1 .0 .0]);
        end
    end
end

end