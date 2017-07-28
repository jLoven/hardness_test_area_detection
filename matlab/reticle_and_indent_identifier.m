% Jackie Loven
% 27 July 2017

reticle = imread('/Users/platypus/Desktop/reticle.png');
reticleCopy = reticle;
inputNumber = 10;
figure('name','Please click ten consecutive points on the horizontal reticle.');
imshow(reticleCopy);
[x, y] = ginput(inputNumber);

prompt = {'Scale bar size in mm:'};
dlg_title = 'Input';
num_lines = 1;
defaultans = {'0.05'};
answer = inputdlg(prompt, dlg_title, num_lines, defaultans);
scaleBarSize = str2double(answer);

close all;

total = 0;
for i = 2 : inputNumber
    x1 = x(i);
    x2 = x(i - 1);
    distance = x2 - x1;
    disp(distance);
    total = total + distance;
end

average = total / inputNumber;
mmPerPixel = scaleBarSize / average;
micronsPerPixel = mmPerPixel * 1000;

% do image analysis, pick out contour
original = imread('/Users/platypus/Desktop/sample_indent.png');
originalCopy = original;

% 1. Convert to grayscale
grayscaleImage = rgb2gray(originalCopy);

% 6. Binarize image
binaryImage = imbinarize(grayscaleImage,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);
imshow(binaryImage);

% 7. Canny edge detect
cannyImage = edge(binaryImage, 'canny');
cannyImageCast = +cannyImage;

% 8. Gaussian blur
kernel = 7;
sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8;
gaussianBlurImage = imgaussfilt(cannyImageCast, sigma);

% 9. Binarize image again
binaryImage2 = imbinarize(gaussianBlurImage,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

% 10. https://stackoverflow.com/questions/28614074/how-to-select-the-largest-contour-in-matlab
% Select the largest contour in the selected area.
im = binaryImage2;
im_fill = imfill(im, 'holes');
s = regionprops(im_fill, 'Area', 'PixelList');
[~,ind] = max([s.Area]);
pix = sub2ind(size(im), s(ind).PixelList(:,2), s(ind).PixelList(:,1));
out = zeros(size(im));
out(pix) = im(pix);
imshow(out);

pixelArea = ind;
indentArea = pixelArea * micronsPerPixel * micronsPerPixel;
totalString = strcat(num2str(indentArea), ' sq. µm');
disp(totalString);
