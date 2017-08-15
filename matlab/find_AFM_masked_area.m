% Jackie Loven
% 9 August 2017
% AFM Masked Area Identified. All Rights Reserved.
% Mask indent area in an AFM image in red, and click several points on the 
% scale bar to identify pixels per area.

original = imread('/Users/platypus/Desktop/mse_4920/images/afm/redone_masks_2/245.2_4.png');
originalCopy = original;
secondCopy = original;
[width, height, z1] = size(originalCopy);
blankImage = ones(width, height);

figure('name','Please click five consecutive points on the vertical scale bar.');
imshow(originalCopy);
[x, y] = ginput(5);

prompt = {'Scale bar size in µm:'};
dlg_title = 'Input';
num_lines = 1;
defaultans = {'10'};
answer = inputdlg(prompt, dlg_title, num_lines, defaultans);
scaleBarSize = str2double(answer);

close all;

difference1 = abs(y(3) - y(2));
difference2 = abs(y(2) - y(1));
difference3 = abs(y(4) - y(3));
difference4 = abs(y(5) - y(4));
average = (difference1 + difference2 + difference3 + difference4) / 4;

micronsPerPixel = scaleBarSize / average;

for i = 1:width
    for j = 1:height
        first = originalCopy(i, j, 1) <= 255 && originalCopy(i, j, 1) >= 205;
        second = originalCopy(i, j, 2) <= 30 && originalCopy(i, j, 2) >= 0;
        third = originalCopy(i, j, 3) <= 30 && originalCopy(i, j, 3) >= 0;
        if not(first && second && third)
            % turn everything not red into black, then find largest contour
            blankImage(i, j, 1) = 0;
            blankImage(i, j, 2) = 0;
            blankImage(i, j, 3) = 0;
        end
    end
end

%  Find largest contour. Adaptive binarization on grayscale image.
grayscaleImage = rgb2gray(blankImage);
cannyImage = edge(grayscaleImage, 'Canny', 0);
cannyImageCast = +cannyImage;
binaryImage = imbinarize(cannyImageCast,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

% https://stackoverflow.com/questions/28614074/how-to-select-the-largest-contour-in-matlab
% Select the largest contour in the selected area.
im = binaryImage;
im_fill = imfill(im, 'holes');
s = regionprops(im_fill, 'Area', 'PixelList');
[~,index] = max([s.Area]);
pixelArea = s(index).Area;
relevantPixelList = s(index).PixelList;

% Color the indent green on the image.
for i = 1:pixelArea
    x = relevantPixelList(i, 2);
    y = relevantPixelList(i, 1);
    originalCopy(x, y, 1) = 0;
    originalCopy(x, y, 2) = 255;
    originalCopy(x, y, 3) = 0;
end

areaOfIndent = pixelArea * micronsPerPixel * micronsPerPixel;
totalString = strcat(num2str(areaOfIndent), ' sq. µm');
disp(totalString);

figure('name','Please click the four indent vertices in clockwise order.');
imshow(originalCopy);

%  Following taken from https://www.mathworks.com/matlabcentral/answers/95813-how-can-i-use-the-ginput-function-to-select-a-point-on-an-image-in-matlab-along-with-the-zoom-functi
zoom on;
pause() % you can zoom with your mouse and when your image is okay, you press any key
zoom off; % to escape the zoom mode
point1 = ginput(1);
zoom out; % go to the original size of your image
zoom on;
pause() % you can zoom with your mouse and when your image is okay, you press any key
zoom off; % to escape the zoom mode
point2 = ginput(1);
zoom out; % go to the original size of your image
zoom on;
pause() % you can zoom with your mouse and when your image is okay, you press any key
zoom off; % to escape the zoom mode
point3 = ginput(1);
zoom out; % go to the original size of your image
zoom on;
pause() % you can zoom with your mouse and when your image is okay, you press any key
zoom off; % to escape the zoom mode
point4 = ginput(1);
zoom out; % go to the original size of your image

% sqrt((x2-x1)^2+(y2-y1)^2)
diagonal1 = sqrt((point1(1) - point3(1))^2 + ((point1(2) - point3(2))^2));
diagonal2 = sqrt((point2(1) - point4(1))^2 + ((point2(2) - point4(2))^2));
% draw diagonals in blue
hold on;
plot([point1(1),point3(1)],[point1(2),point3(2)],'Color','blue','LineWidth',2)
plot([point2(1),point4(1)],[point2(2),point4(2)],'Color','blue','LineWidth',2)

avgDiag = (diagonal1 + diagonal2) / 2;
avgDiagInMicrons = avgDiag * micronsPerPixel;
diagonalArea = avgDiagInMicrons^2 * 0.5;
totalString2 = strcat(num2str(diagonalArea), ' sq. µm for diagonals');
disp(totalString2);



% Calculate diagonals 




