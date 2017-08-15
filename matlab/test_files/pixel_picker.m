

rgbImage = imread('/Users/platypus/Desktop/mse_4920/hardness_test_area_detection/images/1.png');
% Display the original color image.
imshow(rgbImage);
% Enlarge figure to full screen.
set(gcf, 'units','normalized','outerposition',[0 0 1 1]);

[x,y] = ginput(1);
% Put a cross where they clicked.
hold on;
plot(x, y, 'w+', 'MarkerSize', 50);
% Get the location they click on.
row = int32(y);
column = int32(x);
disp(row)
disp(column)
close all;


