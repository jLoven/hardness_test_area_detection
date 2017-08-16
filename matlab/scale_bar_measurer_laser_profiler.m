

close all;
original = imread('/Users/platypus/Desktop/mse_4920/images/laser_profiler/245.2_1_masked.png');


figure('name','Please click opposite ends of the scale bar five times.');
imshow(original);

zoom on;
pause() % you can zoom with your mouse and when your image is okay, you press any key
[x, y] = ginput(5);
zoom off; % to escape the zoom mode


prompt = {'Scale bar size in µm:'};
dlg_title = 'Input';
num_lines = 1;
defaultans = {'20'};
answer = inputdlg(prompt, dlg_title, num_lines, defaultans);
scaleBarSize = str2double(answer);

close all;

difference1 = abs(x(3) - x(2));
difference2 = abs(x(2) - x(1));
difference3 = abs(x(4) - x(3));
difference4 = abs(x(5) - x(4));
average = (difference1 + difference2 + difference3 + difference4) / 4;

micronsPerPixel = scaleBarSize / average;
disp(micronsPerPixel);

