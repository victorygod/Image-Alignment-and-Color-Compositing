function [output_image, offset] = alignWithPixels(image, padding)
  [h,w,d] = size(image);
  
  bestOffset = [0 0; 0 0];
  output_image = zeros(size(image));
  bestLoss1 = loss(image(:,:,1), image(:,:,3));
  bestLoss2 = loss(image(:,:,2), image(:,:,3));
  for offsetX = -padding:padding
    for offsetY = -padding:padding
      new_image = circshift(image(:,:,1), [offsetX, offsetY]);
      current_loss1 = loss(new_image, image(:,:,3));
      new_image = circshift(image(:,:,2), [offsetX, offsetY]);
      current_loss2 = loss(new_image, image(:,:,3));
      
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