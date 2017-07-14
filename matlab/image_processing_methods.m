% Jackie Loven
% 14 July 2017

function image_processing_methods()
end

% functions
function s = getSigma(kernel)
s = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8;
end