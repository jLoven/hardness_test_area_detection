original = imread('/Users/platypus/Desktop/mse_4920/hardness_test_area_detection/images/1.png');
originalCopy = original;

grayscaleImage = rgb2gray(originalCopy);

binaryImage2 = imbinarize(grayscaleImage,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

% 10. https://stackoverflow.com/questions/28614074/how-to-select-the-largest-contour-in-matlab
% Select the largest contour in the selected area.
im = binaryImage2;
im_fill = imfill(im);
