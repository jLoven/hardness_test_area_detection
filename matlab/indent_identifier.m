% Jackie Loven
% 27 July 2017

original = imread('/Users/platypus/Desktop/final_metallized_images/after/2942_2_after.png');
originalCopy = original;
originalCopy2 = original;

% 1. Convert to grayscale
grayscaleImage = rgb2gray(originalCopy);

% 2. Erode image
kernel = strel('square', 8);
erodeImage = imerode(grayscaleImage, kernel);
kernel2 = strel('square', 8);
dilateImage1 = imdilate(erodeImage, kernel2);
%kernel2 = strel('square', 2);
%dilateImage2 = imdilate(dilateImage1, kernel2);

% 6. Binarize image
binaryImage = imbinarize(dilateImage1,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);
imshow(binaryImage);

% 7. Canny edge detect
cannyImage = edge(binaryImage, 'canny');
cannyImageCast = +cannyImage;

% 8. Gaussian blur
%kernel = 7;
%sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8;
%gaussianBlurImage = imgaussfilt(cannyImageCast, sigma);

% 9. Binarize image again
binaryImage2 = imbinarize(cannyImageCast,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

% 10. https://stackoverflow.com/questions/28614074/how-to-select-the-largest-contour-in-matlab
% Select the largest contour in the selected area.
im = binaryImage2;
im_fill = imfill(im, 'holes');
s = regionprops(im_fill, 'Area', 'PixelList');
[~,ind] = max([s.Area]);
pix = sub2ind(size(im), s(ind).PixelList(:,2), s(ind).PixelList(:,1));
pixelArea = s(ind).Area;

for i = 1:pixelArea
    x = s(ind).PixelList(i, 2);
    y = s(ind).PixelList(i, 1);
    originalCopy2(x, y, 1) = 0;
    originalCopy2(x, y, 2) = 255;
    originalCopy2(x, y, 3) = 0;
end

%contourColor = zeros(size(im));
%out = originalCopy2;
%originalCopy2(pix) = out(pix);
imshow(originalCopy2);
imwrite(originalCopy2, '/Users/platypus/Desktop/hello.png');

micronsPerPixel = 0.18694;
indentArea = pixelArea * micronsPerPixel * micronsPerPixel;
totalString = strcat(num2str(indentArea), ' sq. �m');
disp(totalString);