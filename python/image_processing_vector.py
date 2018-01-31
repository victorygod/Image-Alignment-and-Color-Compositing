from scipy import misc
from scipy import signal
import numpy as np

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

def GaussianBlur(layer):
	Gaussian_kernel = np.array([[0.075, 0.124, 0.075], [0.124, 0.204, 0.124], [0.075, 0.124, 0.075]])
	return signal.convolve2d(layer, Gaussian_kernel, 'same')

def align(originImage):
	padding=15
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
	for i in range(3):
		layers[i] = originImage[:,:,i]#GaussianBlur(originImage[:,:,i])
		layerX[i] = signal.convolve2d(layers[i], sobel_kernel_x, 'same')#>50
		layerY[i] = signal.convolve2d(layers[i], sobel_kernel_y, 'same')#>50
		layers[i] = np.sqrt(layerX[i]**2+layerY[i]**2)#>threshold
		h, w = layers[i].shape
		# misc.imsave("test"+str(i)+".jpg", layers[i][2*padding:h-2*padding, 2*padding:w-2*padding])

	layer0 = layers[0]
	layer1 = layers[1]
	layer2 = layers[2]

	bestOffset = [[0, 0], [0, 0]]
	bestLoss0 = loss(layerX[0], layerX[2])+loss(layerY[0], layerY[2])
	bestLoss1 = loss(layerX[1], layerX[2])+loss(layerY[1], layerY[2])

	lm1 = np.zeros([31,31])
	lm2 = np.zeros([31,31])
	for offsetX in range(-padding, padding+1):
		for offsetY in range(-padding, padding+1):
			new_layerX = move(layerX[0], [offsetX, offsetY])
			new_layerY = move(layerY[0], [offsetX, offsetY])
			current_loss = loss(new_layerX, layerX[2]) + loss(new_layerY, layerY[2])

			lm1[offsetX+padding, offsetY+padding] = current_loss
			if current_loss<bestLoss0:
				bestLoss0 = current_loss
				bestOffset[0] = [offsetX, offsetY]
			new_layerX = move(layerX[1], [offsetX, offsetY])
			new_layerY = move(layerY[1], [offsetX, offsetY])
			current_loss = loss(new_layerX, layerX[2]) + loss(new_layerY, layerY[2])

			lm2[offsetX+padding, offsetY+padding] = current_loss
			if current_loss<bestLoss1:
				bestLoss1 = current_loss
				bestOffset[1] = [offsetX, offsetY]

	print(bestLoss0)
	print(bestLoss1)
	print(bestOffset)
	originImage[:,:,0] = move(originImage[:,:,0], bestOffset[0])
	originImage[:,:,1] = move(originImage[:,:,1], bestOffset[1])


	misc.imsave("loss1.jpg", lm1)
	misc.imsave("loss2.jpg", lm2)
	return originImage	

for i in range(1):
	img = misc.imread("../images/"+str(i+1)+".jpg")

	height, width = img.shape

	unit_height = int(height/3)

	originImage = [[[img[y+2*unit_height][x], img[y + unit_height][x], img[y][x]] for x in range(width)] for y in range(unit_height)]
	originImage = np.array(originImage, dtype = 'f')

	sobel_kernel_x = np.array([[1, 0, -1],
	[2, 0 , -2],
	[1, 0, -1]])
	l0 = signal.convolve2d(originImage[:,:,0], sobel_kernel_x, 'same')
	l2 = signal.convolve2d(originImage[:,:,2], sobel_kernel_x, 'same')
	print(loss(l0, l2))
	# originImage = align(originImage)

	# misc.imsave("ans"+str(i+1)+".jpg", originImage)