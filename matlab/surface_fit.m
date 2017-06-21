load franke
%sf = fit([x, y],z,'poly23')
%plot(sf,[x,y],z)

sample_indent = [ 0 0 0 0 0;
  0 -1 -1 -1 0;
  0 -1 -2 -1 0;
  0 -1 -1 -1 0;
  0 0 0 0 0
];


T = table(x,y,z);
f = fit([T.x, T.y],T.z,'linearinterp')
plot( f, [T.x, T.y], T.z )
