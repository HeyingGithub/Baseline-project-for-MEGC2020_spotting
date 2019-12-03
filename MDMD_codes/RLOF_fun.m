function [u, v] = RLOF_fun(image1, image2, method)
% demo estimates and displays motion vectors for a given grid of samples 
%%
gridSize = 1;
noRows = size(image1,1);
noCols = size(image1,2);
% initialize pointlist with features to track
[Y,X] = meshgrid(0:gridSize:noRows-1, 0:gridSize:noCols-1);
pointlist1 = [reshape(X, size(X,1) * size(X,2), 1)'; reshape(Y, size(Y,1) * size(Y,2), 1)' ];
%track features
parameter = struct('method',method, 'options', 'PrintParameter');
pointlist2 = mex_RLOF(image1, image2, pointlist1, parameter);
uv = pointlist2-pointlist1;
u = uv(1,:);
v = uv(2,:);
u = reshape(u,[noCols, noRows]);
u = u';
v = reshape(v,[noCols, noRows]);
v = v';
