function [output_image, offset] = align(image, padding)
  sobel_kernel_x = [1 0 -1;2 0 -2;1 0 -1];
  sobel_kernel_y = [1 2 1;0 0 0;-1 -2 -1];
  [h,w,d] = size(image);
  gradientX = zeros(h,w,d);
  gradientY = zeros(h,w,d);
  for i = 1:3
    gradientX(:,:,i) = conv2(image(:,:,i), sobel_kernel_x, 'same');
    gradientY(:,:,i) = conv2(image(:,:,i), sobel_kernel_y, 'same');
  endfor
  
  bestOffset = [0 0; 0 0];
  output_image = zeros(size(image));
  bestLoss1 = loss(gradientX(:,:,1), gradientX(:,:,3)) + loss(gradientY(:,:,1), gradientY(:,:,3));
  bestLoss2 = loss(gradientX(:,:,2), gradientX(:,:,3)) + loss(gradientY(:,:,2), gradientY(:,:,3));
  for offsetX = -padding:padding
    for offsetY = -padding:padding
      new_gradientX1 = circshift(gradientX(:,:,1), [offsetX, offsetY]);
      new_gradientY1 = circshift(gradientY(:,:,1), [offsetX, offsetY]);
      current_loss1 = loss(new_gradientX1, gradientX(:,:,3)) + loss(new_gradientY1, gradientY(:,:,3));
      new_gradientX2 = circshift(gradientX(:,:,2), [offsetX, offsetY]);
      new_gradientY2 = circshift(gradientY(:,:,2), [offsetX, offsetY]);
      current_loss2 = loss(new_gradientX2, gradientX(:,:,3)) + loss(new_gradientY2, gradientY(:,:,3));
      
      if current_loss1<bestLoss1
        bestLoss1 = current_loss1;
        bestOffset(1,:) = [offsetX, offsetY];
      endif
      if current_loss2<bestLoss2
        bestLoss2 = current_loss2;
        bestOffset(2,:) = [offsetX, offsetY];
      endif
    endfor
  endfor
  offset = bestOffset;
  output_image(:,:,1) = circshift(image(:,:,1), bestOffset(1,:));
  output_image(:,:,2) = circshift(image(:,:,2), bestOffset(2,:));
  output_image(:,:,3) = image(:,:,3);