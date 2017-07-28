% Jackie Loven
% 14 July 2017

clear all;
original = imread('/Users/platypus/Desktop/sample_indent_2 2.jpg');
originalCopy = original;
%croppedImage = imcrop(originalCopy);

% 1. Convert to grayscale
grayscaleImage = rgb2gray(originalCopy);

% 2. Gaussian blur
% OpenCV uses standard dev of 0.3*((ksize-1)*0.5 - 1) + 0.8
% see http://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#getgaussiankernel
kernel = 7;
sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8;
gaussianBlurImage1 = imgaussfilt(grayscaleImage, sigma);
%imshow(gaussianBlurImage);

% 3. Erode and dilate
kernel = strel('square', 8);
erodeImage1 = imerode(gaussianBlurImage1, kernel);
dilateImage1 = imdilate(erodeImage1, kernel);
%imshow(erodeImage1);
%imshow(dilateImage1);

% 4. CLAHE
%claheImage = adapthisteq(dilateImage1, 'clipLimit', 0.055, 'Distribution', 'uniform', 'NumTiles', [8,8]);
%imshow(claheImage);

% 5. Erode, dilate, and erode
erodeImage2 = imerode(dilateImage1, kernel);
dilateImage2 = imdilate(erodeImage2, kernel);
erodeImage3 = imerode(dilateImage2, kernel);
dilateImage3 = imdilate(erodeImage3, kernel);
%imshow(dilateImage3);

% 6. Binarize image
binaryImage = imbinarize(dilateImage3,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);
imshow(binaryImage);

erodeImage4 = imerode(binaryImage, kernel);
dilateImage4 = imdilate(erodeImage4, kernel);
erodeImage5 = imerode(dilateImage4, kernel);
dilateImage5 = imdilate(erodeImage5, kernel);

erodeImage6 = imerode(dilateImage5, kernel);
dilateImage6 = imdilate(erodeImage6, kernel);

% 7. Canny edge detect
cannyImage = edge(dilateImage6, 'canny');
%imshow(cannyImage);
cannyImageCast = +cannyImage;

% 8. Gaussian blur
gaussianBlurImage3 = imgaussfilt(cannyImageCast, sigma);

complementImage = imcomplement(gaussianBlurImage3);
%imshow(gaussianBlurImage2);

% 9. Binarize image again
binaryImage2 = imbinarize(gaussianBlurImage3,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);
%imshow(binaryImage2);

% 10. https://stackoverflow.com/questions/28614074/how-to-select-the-largest-contour-in-matlab
% Select the largest contour in the selected area.
im = binaryImage2;
im_fill = imfill(im, 'holes');
s = regionprops(im_fill, 'Area', 'PixelList');
[~,ind] = max([s.Area])
pix = sub2ind(size(im), s(ind).PixelList(:,2), s(ind).PixelList(:,1));
out = zeros(size(im));
out(pix) = im(pix);
imshow(out);

% Return the pixel area of this image.
disp(ind)

