from scipy import misc
from scipy import signal
import numpy as np
import os
import math


for j in range(23):
	offset = [0,0,0,0]

	img = misc.imread('ans'+ str(j+1) +'.jpg').astype('f')
	h,w,d = img.shape


	fractor = 4.5
	threshold = np.var(img[:,:,:], axis = (0,1))/fractor#[np.var(img[:,:,0])/fractor, np.var(img[:,:,1])/fractor,np.var(img[:,:,2])/fractor]
	print(threshold)

	for i in range(int(h*0.05)):
		v = np.var(img[i:i+1, :, :], axis = (0,1))
		if (v>threshold).all():
			offset[0] = i
			break
		offset[0]=i
	for i in range(int(h*0.95), h-1)[::-1]:
		v = np.var(img[i:i+1, :, :], axis = (0,1))
		if (v>threshold).all():
			offset[1] = i
			break
		offset[1] = i
	for i in range(int(w*0.05)):
		v = np.var(img[:, i:i+1, :], axis = (0,1))
		if (v>threshold).all():
			offset[2] = i
			break
		offset[2] = i
	for i in range(int(w*0.95), w-1)[::-1]:
		v = np.var(img[:, i:i+1, :], axis = (0,1))
		if (v>threshold).all():
			offset[3] = i
			break
		offset[3] = i

	img = img[offset[0]:offset[1], offset[2]:offset[3]]
	misc.imsave('ans'+str(j+1)+'_crop.jpg', img)

# img = misc.imread('ans1.jpg').astype('f')
# h,w,d = img.shape
# v = np.var(img[0:2, :, :], axis = (0,1))
# print(v)