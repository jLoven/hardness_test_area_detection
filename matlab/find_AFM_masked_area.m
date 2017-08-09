% Jackie Loven
% 9 August 2017
% AFM Masked Area Identified. All Rights Reserved.
% Mask indent area in an AFM image in red, and click several points on the 
% scale bar to identify pixels per area.

original = imread('/Users/platypus/Desktop/mse_4920/images/afm/redone_masks_2/2942_4_edit.png');
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
[~,ind] = max([s.Area]);
pix = sub2ind(size(im), s(ind).PixelList(:,2), s(ind).PixelList(:,1));
pixelArea = s(ind).Area;

% Color the indent green on the image.
for i = 1:pixelArea
    x = s(ind).PixelList(i, 2);
    y = s(ind).PixelList(i, 1);
    originalCopy(x, y, 1) = 0;
    originalCopy(x, y, 2) = 255;
    originalCopy(x, y, 3) = 0;
end

imshow(originalCopy);
areaOfRed = pixelArea * micronsPerPixel * micronsPerPixel;
totalString = strcat(num2str(areaOfRed), ' sq. µm');
disp(totalString);
