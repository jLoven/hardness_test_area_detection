% Jackie Loven
% 14 July 2017

original = imread('/Users/platypus/Desktop/mse_4920/hardness_test_area_detection/images/1.png');
originalCopy = original;
%  TODO: REMOVE CROPPING STEP ONCE REASONABLE IMAGES OBTAINED
originalCropped = imcrop(originalCopy);
%imshow(originalCropped);

% 1. Convert to grayscale
grayscaleImage = rgb2gray(originalCropped);

% 2. Gaussian blur
% OpenCV uses standard dev of 0.3*((ksize-1)*0.5 - 1) + 0.8
% see http://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#getgaussiankernel
kernel = 7;
sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8;
gaussianBlurImage1 = imgaussfilt(grayscaleImage, sigma);
%imshow(gaussianBlurImage);

% 3. Erode and dilate
kernel = strel('square', 7);
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
%imshow(binaryImage);

% 7. Canny edge detect
cannyImage = edge(binaryImage, 'canny');
%imshow(cannyImage);
cannyImageCast = +cannyImage;

% 8. Gaussian blur
gaussianBlurImage2 = imgaussfilt(cannyImageCast, sigma);
complementImage = imcomplement(gaussianBlurImage2);
%imshow(gaussianBlurImage2);

% 9. Binarize image again
binaryImage2 = imbinarize(gaussianBlurImage2,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

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

% Return the pixel area of this image.
disp(ind)

