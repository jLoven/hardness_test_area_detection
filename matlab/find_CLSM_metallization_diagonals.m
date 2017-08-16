% Jackie Loven
% 16 August 2017
% CLSM and Metallization Masked Area Identifier. All Rights Reserved.
% Just for diagonals.
% Mask indent area in a CLSM/ metallized image in green, and use a reticle
% or scale bar measurer to get micronsPerPixel.

clear all;
close all;
original = imread('/Users/platypus/Desktop/mse_4920/images/final_metallized_images/after_analyzed/2942_4.png');
originalCopy = original;

% Measure a reticle:
micronsPerPixel = 0.18694;

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
totalString = strcat(num2str(diagonalArea), ' sq. µm for diagonals');
disp(totalString);



