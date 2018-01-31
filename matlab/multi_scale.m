for i = 1:10
  img = imread(strcat('../images/', int2str(i),'.jpg'));
  [height, width] = size(img);
  unit_height = int32(height/3);
  originImage = zeros(unit_height, width, 3);
  originImage(:,:,3) = img(1:unit_height, :);
  originImage(:,:,2) = img(unit_height+1:unit_height*2, :);
  originImage(:,:,1) = img(unit_height*2+1:unit_height*3, :);
  [w,h,d] = size(originImage);
  depth = floor(log((w+h)/20));
  [newImage, offset] = multi_align(originImage, depth);
  i
  offset
  imwrite(newImage/255, strcat('out',int2str(i),'.jpg'));
endfor