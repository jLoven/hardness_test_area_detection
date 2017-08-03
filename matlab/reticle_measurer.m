%  Jackie Loven


reticle = imread('/Users/platypus/Desktop/final_metallized_images/reticle.png');
reticleCopy = reticle;
inputNumber = 5;
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

average = total / (inputNumber - 1);
mmPerPixel = scaleBarSize / average;
micronsPerPixel = mmPerPixel * 1000;

disp(strcat(num2str(micronsPerPixel), ' µm per pixel'));
