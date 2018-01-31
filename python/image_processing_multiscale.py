from scipy import misc
from scipy import signal
import numpy as np
import os
import math

def loss(img1, img2):
	h,w= img1.shape
	paddingh = int(h/4)
	paddingw = int(w/4)

	s=np.mean((img1[paddingh:h-paddingh, paddingw:w-paddingw] - img2[paddingh:h-paddingh, paddingw:w-paddingw])**2)
	return s

def move(img, direction):
	h, w= img.shape
	new_img = img.copy()
	if direction[0]<0:
		for y in range(h+direction[0]):
			new_img[y,:] = new_img[y-direction[0],:]
	elif direction[0]>0:
		for y in range(direction[0], h)[::-1]:
			new_img[y,:] = new_img[y-direction[0],:]

	if direction[1]<0:
		for x in range(w+direction[1]):
			new_img[:,x] = new_img[:,x-direction[1]]
	elif direction[1]>0:
		for x in range(direction[1], w)[::-1]:
			new_img[:,x] = new_img[:,x-direction[1]]
	return new_img

def GaussianBlur(img):
	Gaussian_kernel = np.array([[0.03082,0.03717,0.03957, 0.03717, 0.03082], 
		[0.03717,0.04484,0.04773,0.04484,0.03717], 
		[0.03957,0.04774,0.05081,0.04773,0.03957],
		[0.03717,0.04484,0.04773,0.04484,0.03717],
		[0.03082,0.03717,0.03957,0.03717,0.03082]])
	new_img = np.zeros(img.shape)
	for i in range(3):
		new_img[:,:,i] = signal.convolve2d(img[:,:,i], Gaussian_kernel, 'same')
	return new_img

def align(originImage, depth):
	padding=3
	threshold = 150

	sobel_kernel_x = np.array([[1, 0, -1],
		[2, 0 , -2],
		[1, 0, -1]])
	sobel_kernel_y = np.array([[1, 2, 1],
		[0, 0, 0],
		[-1, -2, -1]])

	layers = [0,0,0]
	layerX=[0,0,0]
	layerY = [0,0,0]
	# blured_img = GaussianBlur(originImage)
	for i in range(3):
		layers[i] = originImage[:,:,i].astype('float')#blured_img[:,:,i]
		layerX[i] = signal.convolve2d(layers[i], sobel_kernel_x, 'same')
		layerY[i] = signal.convolve2d(layers[i], sobel_kernel_y, 'same')
		# layers[i] = np.sqrt(layerX[i]**2+layerY[i]**2)#>threshold
		# h, w = layers[i].shape
		#misc.imsave("test"+str(i)+".jpg", layers[i][2*padding:h-2*padding, 2*padding:w-2*padding])

	layer0 = layers[0]
	layer1 = layers[1]
	layer2 = layers[2]

	bestOffset = [[0, 0], [0, 0]]
	# bestLoss0 = loss(layer0, layer2)
	# bestLoss1 = loss(layer1, layer2)
	bestLoss0 = loss(layerX[0], layerX[2])+loss(layerY[0], layerY[2])
	bestLoss1 = loss(layerX[1], layerX[2])+loss(layerY[1], layerY[2])

	lm1 = np.zeros([2*padding+1,2*padding+1])
	lm2 = np.zeros([2*padding+1,2*padding+1])

	for offsetX in range(-padding, padding+1):
		for offsetY in range(-padding, padding+1):
			# new_layer = move(layer0, [offsetX, offsetY])
			# current_loss = loss(new_layer, layer2)

			new_layerX = move(layerX[0], [offsetX, offsetY])
			new_layerY = move(layerY[0], [offsetX, offsetY])
			current_loss = loss(new_layerX, layerX[2]) + loss(new_layerY, layerY[2])

			lm1[offsetX+padding, offsetY+padding] = current_loss

			if current_loss<bestLoss0:
				bestLoss0 = current_loss
				bestOffset[0] = [offsetX, offsetY]
			# new_layer = move(layer1, [offsetX, offsetY])
			# current_loss = loss(new_layer, layer2)

			new_layerX = move(layerX[1], [offsetX, offsetY])
			new_layerY = move(layerY[1], [offsetX, offsetY])
			current_loss = loss(new_layerX, layerX[2]) + loss(new_layerY, layerY[2])

			lm2[offsetX+padding, offsetY+padding] = current_loss
			if current_loss<bestLoss1:
				bestLoss1 = current_loss
				bestOffset[1] = [offsetX, offsetY]

	# print(bestLoss0)
	# print(bestLoss1)
	# print(bestOffset)
	originImage[:,:,0] = move(originImage[:,:,0], bestOffset[0])
	originImage[:,:,1] = move(originImage[:,:,1], bestOffset[1])
	misc.imsave("loss1" + str(depth)+".jpg", lm1)
	misc.imsave("loss2"+str(depth)+".jpg", lm2)

	return originImage, bestOffset

def resize_by_2(img):
	img = GaussianBlur(img)
	h, w, d = img.shape
	new_img = misc.imresize(img, (int(h/2), int(w/2)), interp = "nearest")
	new_img = new_img.astype('float')
	# new_img = np.zeros((int(h/2), int(w/2), 3))
	# for hh in range(int(h/2)):
	# 	for ww in range(int(w/2)):
	# 		# n=1
	# 		new_img[hh, ww,:] = img[hh*2, ww*2, :]
	# 		# if hh*2+1<h:
	#		#   n+=1
	# 		# 	new_img[hh,ww,:]+=new_img[hh*2+1,ww,:]
	# 		# if ww*2+1<w:
	#		#   n+=1
	# 		# 	new_img[hh,ww,:]+=new_img[hh,ww*2+1,:]
	# 		# if hh*2+1<h and ww*2+1<w:
	#		#   n+=1
	# 		# 	new_img[hh,ww,:]+=new_img[hh*2+1,ww*2+1,:]
	#		# new_img[hh,ww,:]/=n
	return new_img.astype('f')

def multiscale_align(image, depth):
	if depth==0:
		return align(image, depth)
	new_image = resize_by_2(image)
	_, offset = multiscale_align(new_image, depth-1)

	cc = [[offset[0][0]*2, offset[0][1]*2], [offset[1][0]*2, offset[1][1]*2]]

	new_image = np.zeros(image.shape) 
	for i in range(2):
		new_image[:,:,i] = move(image[:,:,i], cc[i])
	new_image[:,:,2] = image[:,:,2]

	
	img, offset = align(new_image, depth)

	offset = [[offset[0][0]+cc[0][0], offset[0][1]+cc[0][1]],[offset[1][0]+cc[1][0], offset[1][1]+cc[1][1]]]

	return img, offset

for i in range(23):
	img = misc.imread("../images/"+str(i+1)+".jpg")

	height, width = img.shape

	unit_height = int(height/3)

	originImage = np.zeros((unit_height, width, 3))
	originImage[:,:,2] = img[0:unit_height,:]
	for y in range(unit_height):
		originImage[y,:,1] = img[y + unit_height,:]
		originImage[y,:,0] = img[y + 2*unit_height,:]

	w,h,d = originImage.shape
	depth = int(math.log((w+h)/20))
	print(depth)

	originImage, offset = multiscale_align(originImage, depth)
	print(offset)

	misc.imsave("ans"+str(i+1)+".jpg", originImage)


