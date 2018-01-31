from scipy import misc
from scipy import signal
import numpy as np
import os
import math


for j in range(23):

	img = misc.imread('ans'+ str(j+1) +'_crop.jpg').astype('f')
	h,w,d = img.shape

	# gray_img = np.matmul(img, np.array([0.299, 0.587, 0.114]).T)

	# x_max = int(h*0.05)
	# y_max = int(w*0.05)
	# x_min = x_max
	# y_min = y_max
	# for x in range(int(h*0.05), int(h*0.95)):
	# 	for y in range(int(w*0.05), int(w*0.95)):
	# 		if gray_img[x,y]>gray_img[x_max, y_max]:
	# 			x_max = x
	# 			y_max = y
	# 		if gray_img[x,y]<gray_img[x_min, y_min]:
	# 			x_min = x
	# 			y_min = y

	# upper_bound = max(img[x_max, y_max, :])

	# lower_bound = min(img[x_min, y_min, :])

	# new_img = np.minimum(np.maximum((img-lower_bound)/(upper_bound-lower_bound),0),1)
	

	# misc.imsave('contrast'+str(j+1)+'.jpg', new_img)
	n = h*w
	hist = np.zeros((3, 256))
	for x in range(h):
		for y in range(w):
			for d in range(3):
				hist[d, int(img[x,y,d])]+=1
	
	lower_bound = np.array([0,0,0])
	upper_bound = np.array([0,0,0])
	
	for d in range(3):
		s = 0
		for i in range(256):
			s+=hist[d,i]
			if s<n*0.05:
				lower_bound[d] = i
			if s>n*0.95:
				upper_bound[d] = i
				break
	
	new_img = np.zeros(img.shape)
	for d in range(3):
		new_img[:,:,d] = np.minimum(np.maximum((img[:,:,d] - lower_bound[d])/(upper_bound[d] - lower_bound[d]),0),1)

	misc.imsave('contrast'+str(j+1)+'.jpg', new_img)
	print(j)