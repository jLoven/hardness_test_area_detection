% Jackie Loven
% 14 July 2017



original = imread('/Users/platypus/Desktop/mse_4920/hardness_test_area_detection/images/1.png');
originalCopy = original;
imshow(originalCopy);

% 1. Convert to grayscale
grayscaleImage = rgb2gray(originalCopy);

% 2. Gaussian blur
% OpenCV uses standard dev of 0.3*((ksize-1)*0.5 - 1) + 0.8
% see http://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#getgaussiankernel
kernel = 7;
sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8;
gaussianBlurImage = imgaussfilt(grayscaleImage, sigma);
imshow(gaussianBlurImage);







