function [loc] = get_image_point (I)
figure('name','Doubleclick to set location');
imshow(I);
[c, r] = getpts(1);
loc = int64([c r]);
if size(loc)>1
    loc = [loc(1,1) loc(1,2)];
end
disp("hello")
close all;
end 