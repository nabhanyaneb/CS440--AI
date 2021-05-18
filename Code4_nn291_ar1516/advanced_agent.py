from PIL import Image
import pprint
import random
import math
import sys
import numpy as np

#width and height
w = 300 
h = 200

#returns the nine-component vector for a given x,y
def get_nine(image,x,y):
	values = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

	if (x-1) >= 0 and (x+1) < w and (y-1) >= 0 and (y+1) < h:
		values[0] = image.getpixel((x-1,y-1))[0] / 255.0
		values[1] = image.getpixel((x,y-1))[0] / 255.0
		values[2] = image.getpixel((x+1,y-1))[0] / 255.0
		values[3] = image.getpixel((x-1,y))[0] / 255.0
		values[4] = image.getpixel((x,y))[0] / 255.0
		values[5] = image.getpixel((x+1,y))[0] / 255.0
		values[6] = image.getpixel((x-1,y+1))[0] / 255.0
		values[7] = image.getpixel((x,y+1))[0] / 255.0
		values[8] = image.getpixel((x+1,y+1))[0] / 255.0

	return values

#sigmoid function
def sigmoid(z):
	ret = (1.0/(1.0 + np.exp(-z)))
	return ret

#calculate predicted y value
def pred_y(wVect, xVect):
	ret = (sigmoid(np.dot(wVect,xVect)))
	return ret

#calculate new w vector
def calculations(xVect, y, wVect, a):
	F = pred_y(wVect,xVect)
	loss = (2 * (F - y) * F * (1 - (F / 255.0))) * xVect
	wReturn = wVect - (a*loss)
	return wReturn

#start the training algorithm
def logistic(image, bw_dict, n):
	a = 0.5

	#initialize weights based on whether we are using the r, g, or b model
	if n == 0:
		wVect = np.array([0.2 for x in range(10)])
	elif n == 1:
		wVect = np.array([0.4 for x in range(10)])
	elif n == 2:
		wVect = np.array([0.3 for x in range(10)])

	#run training algorithm
	t = 0
	while t < 10000:
		xCord = random.randint(1,145)
		yCord = random.randint(1,195)

		xVect = np.array(bw_dict[(xCord,yCord)])
		xVect = np.insert(xVect,0,1)

		y = image.getpixel((xCord,yCord))[n]/255.0	

		wVect = calculations(xVect, y, wVect, a)

		t = t + 1

	return wVect

#predict value based on the corresponding w vector
def predictions(wVect, x, y):
	xVect = np.array(bw_dict[(x,y)])
	xVect = np.insert(xVect,0,1)

	z = np.dot(wVect,xVect)
	ret = sigmoid(z)
	return ret

#formula for finding the distance between two colors	
def find_distance(p1, p2):
	r1 = p1[0]
	g1 = p1[1]
	b1 = p1[2]

	r2 = p2[0]
	g2 = p2[1]
	b2 = p2[2]

	dist = math.sqrt(2*((r1-r2)**2) + 4*((g1-g2)**2) + 3*((b1-b2)**2))	

	return dist

#numerical calculation for image
def calculate_numerical(img1, img2):
	sum = 0
	for x in range(int(w/2),w):
		for y in range(h):
			p1=img1.getpixel((x,y))
			p2=img2.getpixel((x,y))
			sum = sum + find_distance(p1,p2)

	return (sum/(w/2 * h))

#the images
str = 'fall-leaves.jpeg'
img = Image.open(str);
img_gray = Image.open(str) 
img_test = Image.open(str)

#dictionary of vectors for each (x,y)
bw_dict = {}

#setting the black and white image
for x in range(w):
	for y in range(h):
		pixel=img.getpixel((x,y))
		r = int(0.21 * pixel[0])
		g = int(0.72 * pixel[1])
		b = int(0.07 * pixel[2])

		gray = r + g + b

		img_gray.putpixel((x,y),(gray,gray,gray))

#fill the dictionary with the surrounding nine colors for each (x,y)
for x in range(w):
	for y in range(h):
		bw_dict[(x,y)] = get_nine(img_gray,x,y)

#train to find the w vector for r, g and b
wR = logistic(img, bw_dict, 0)
wG = logistic(img, bw_dict, 1)
wB = logistic(img, bw_dict, 2)

#using the w vector, predict the r, g, and b values
for x in range(int(w/2),w):
	for y in range(h):
		r = int(255*predictions(wR,x,y))
		g = int(255*predictions(wG,x,y))
		b = int(255*predictions(wB,x,y))

		img_test.putpixel((x,y),(r,g,b))

#display recolored image
img_test.show()

#numerical calculation of image
print(calculate_numerical(img,img_test))
