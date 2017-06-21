
xLength = 5;
yLength = 5;
sampleIndent = [ 0 0 0 0 0;
  0 -1 -1 -1 0;
  0 -1 -2 -1 0;
  0 -1 -1 -1 0;
  0 0 0 0 0
];


[X,Y]=ndgrid(1:sampleIndent, 1:yLength);
f = fit([X(:),Y(:)], sampleIndent(:),'linearinterp');
plot( f, [X(:),Y(:)], sampleIndent(:))

%x = -3 + 6 * rand(50, 1);
%y = -3 + 6 * rand(50, 1);
%v = zeros(100, 1);

% [xq,yq] = meshgrid(-3:0.2:3);
% 
% z4 = griddata(x,y,v,xq,yq,'cubic');
% figure
% plot3(x,y,v,'mo')
% hold on
% mesh(xq,yq,z4)
% title('Cubic')
% legend('Sample Points','Interpolated Surface','Location','NorthWest')