% Jackie Loven
% 16 August 2017
% Indent Identifier. All Rights Reserved.
% Need a relatively high-contrast image of an indent.
% Also need to image a reticule using Reticle Measurer to find microns per
% pixel.

close all;
clear all;
original = imread('/Users/platypus/Desktop/mse_4920/images/final_metallized_images/after/490.3_4_after.png');
originalCopy = original;
originalCopy2 = original;

% 1. Convert to grayscale
grayscaleImage = rgb2gray(originalCopy);

% 2. Dilate
 kernel2 = strel('square', 4);
 dilateImage1 = imdilate(grayscaleImage, kernel2);

% 3. Binarize image
binaryImage = imbinarize(dilateImage1,'adaptive','ForegroundPolarity','dark','Sensitivity',0.55);
figure;
imshow(binaryImage);

% 4. Canny edge detect
cannyImage = edge(binaryImage, 'canny');
cannyImageCast = +cannyImage;

% 5. Binarize image again
binaryImage2 = imbinarize(cannyImageCast,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

% 6. https://stackoverflow.com/questions/28614074/how-to-select-the-largest-contour-in-matlab
% Select the largest contour in the selected area.
im = binaryImage2;
im_fill = imfill(im, 'holes');
s = regionprops(im_fill, 'Area', 'PixelList');
[~,ind] = max([s.Area]);
pix = sub2ind(size(im), s(ind).PixelList(:,2), s(ind).PixelList(:,1));
pixelArea = s(ind).Area;

% 7. Color the indent green on the image.
for i = 1:pixelArea
    x = s(ind).PixelList(i, 2);
    y = s(ind).PixelList(i, 1);
    originalCopy2(x, y, 1) = 0;
    originalCopy2(x, y, 2) = 255;
    originalCopy2(x, y, 3) = 0;
end

imshow(originalCopy2);
% Save this image in same resolution.
%imwrite(originalCopy2, '/Users/platypus/Desktop/mse_4920/images/final_metallized_images/after_analyzed/490.3_4.png');

% 8. Calculate indent area based on previous measurements of a reticle.
micronsPerPixel = 0.18694;
indentArea = pixelArea * micronsPerPixel * micronsPerPixel;
totalString = strcat(num2str(indentArea), ' sq. µm');
disp(totalString);
