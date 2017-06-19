sample_indent = [ 0 0 0 0 0;
  0 -1 -1 -1 0;
  0 -1 -2 -1 0;
  0 -1 -1 -1 0;
  0 0 0 0 0
];
disp(sample_indent)
%contour(sample_indent)
surf(sample_indent)
%mesh(sample_indent)

mask = sample_indent;
mask(mask < 0) = NaN;
disp(mask)

% area of indent = number of NaN's in center
% given approx. size of indent, cut out that size and count NaN's


