function [output_image, offset] = multi_align(image, depth)
  padding = 3;
  if depth==0
    [output_image, offset] = align(image, padding);
    return;
   endif
  new_image = imresize(image, 0.5, 'bilinear');
  [_, upper_offset] = multi_align(new_image, depth-1);
  upper_offset = upper_offset * 2.0;
  
  image(:,:,1) = circshift(image(:,:,1), upper_offset(1,:));
  image(:,:,2) = circshift(image(:,:,2), upper_offset(2,:));
  image(:,:,3) = image(:,:,3);
  
  [output_image, offset] = align(image, padding);
  offset = offset+upper_offset;
  