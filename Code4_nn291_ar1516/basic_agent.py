from PIL import Image
import pprint
import random
import math
import sys

#width and height
w = 300 
h = 200

#returns the nine-component vector for a given x,y
def get_nine(image,x,y):
	values = [0,0,0,0,0,0,0,0,0]

	if (x-1) >= 0 and (x+1) < w and (y-1) >= 0 and (y+1) < h:
		values[0] = image.getpixel((x-1,y-1))[0]
		values[1] = image.getpixel((x,y-1))[0]
		values[2] = image.getpixel((x+1,y-1))[0]
		values[3] = image.getpixel((x-1,y))[0]
		values[4] = image.getpixel((x,y))[0]
		values[5] = image.getpixel((x+1,y))[0]
		values[6] = image.getpixel((x-1,y+1))[0]
		values[7] = image.getpixel((x,y+1))[0]
		values[8] = image.getpixel((x+1,y+1))[0]

	return values

#k-means clustering algorithm
def k_clusters(image, k):
	C = [[] for i in range(k)] 
	pixels = []
	c = []
	
	for x in range(int(w/2)):
		for y in range(h):
			pixels.append(image.getpixel((x,y)))
	
	#randomly pick six centers
	while len(c) < k:
		point = random.choice(pixels)
		if point not in c:
			c.append(point)

	#cluster the points to the closest center
	for x in range(int(w/2)):
		for y in range(h):	

			index = -1
			min_dist = w * h + 1

			for i in range(len(c)):
				if find_distance(c[i], image.getpixel((x,y))) < min_dist:
					min_dist = find_distance(c[i], image.getpixel((x,y)))
					index = i

			C[index].append((x,y))

	print("C:")
	for i in range(k):
		print(c[i], len(C[i]))
	print()

	#repeat t times
	t = 0
	while t < 100:
		for i in range(k):
			sums_x = 0
			sums_y = 0

			if len(C[i])>0:
				for z in range(len(C[i])):
					sums_x = sums_x + (C[i])[z][0]
					sums_y = sums_y + (C[i])[z][1]

				avg_x = int(sums_x / len(C[i]))
				avg_y = int(sums_y / len(C[i]))
				c[i] = image.getpixel((avg_x , avg_y))


		for i in range(k):
			C[i] = []

		for x in range(int(w/2)):
			for y in range(h):	
				index = -1
				min_dist = w * h + 1
				for i in range(len(c)):
					if find_distance(c[i], image.getpixel((x,y))) < min_dist:
						min_dist = find_distance(c[i], image.getpixel((x,y)))
						index = i

				C[index].append((x,y))

		t = t+1

	print("C:")
	for i in range(k):
		print(c[i], len(C[i]))
	print()
	return (C, c, k)

#set the left half of the image with colors from clustering
def set_image_k_color(C, c, k):
	for i in range(k): 
		for z in range (len(C[i])):
			img_train.putpixel(C[i][z], c[i])

	return

#find the six most similar clusters and pick a color for the (x,y) point
def find_six(dicts, x, y):
	v1 = dicts[(x,y)]

	maximum = float("inf")
	distances = [(maximum,(0,0)), (maximum,(0,0)), (maximum,(0,0)), (maximum,(0,0)), (maximum,(0,0)), (maximum,(0,0))]

	#find the six most similar vectors
	for xx in range(int(w/2)):
		for yy in range(h):	
			v2 = dicts[(xx,yy)]
			sim = find_similar(v1,v2)
			if (sim < max(distances)[0]):
				index_max = distances.index(max(distances))
				distances[index_max] = (sim,(xx,yy))

	distances.sort()
	
	colors = []
	counts = []

	#store how many times each color shows up
	for i in range(6):
		(xx,yy) = distances[i][1]
		pixel = img_train.getpixel((xx,yy))

		if pixel not in colors:
			colors.append(pixel)
			counts.append(1)
		else:
			index = colors.index(pixel)
			counts[index] = counts[index] + 1

	max_count = max(counts)

	index = counts.index(max_count)
	ret = colors[index]

	#pick what to color the pixel
	for i in range(len(counts)):
		if i != index:
			if counts[i] == max_count:
				(xx,yy) = distances[0][1]
				ret = img_train.getpixel((xx,yy))

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

#check similarity between two nine-component vectors
def find_similar(v1, v2):

	dist = math.sqrt(((v1[0]-v2[0])**2) + ((v1[1]-v2[1])**2) + ((v1[2]-v2[2])**2) + ((v1[3]-v2[3])**2) + ((v1[4]-v2[4])**2) + ((v1[5]-v2[5])**2) + ((v1[6]-v2[6])**2) + ((v1[7]-v2[7])**2) + ((v1[8]-v2[8])**2))
	
	return dist

#the three images
str = 'fall-leaves.jpeg'
img = Image.open(str);
img_gray = Image.open(str) 
img_5 = Image.open(str)
img_train = Image.open('training.png') #the saved image from running the k-clusters algorithm for k=5

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

#calling the clustering algorithm
(C, c, k) = k_clusters(img,5)
set_image_k_color(C, c, k)

#update right half
for x in range(int(w/2),w):
	for y in range(h):
		pixel = find_six(bw_dict, x, y)
		img_5.putpixel((x,y),pixel)

img_5.show()
	