function [ans] = loss(layer1, layer2)
  [h,w] = size(layer1);
  crop1 = double(layer1(int16(h/4.0):h - int16(h/4.0), int16(w/4.0):w-int16(w/4.0)));
  crop2 = double(layer2(int16(h/4.0):h - int16(h/4.0), int16(w/4.0):w-int16(w/4.0)));

  ans = mean(((crop1 - crop2).^2)(:));