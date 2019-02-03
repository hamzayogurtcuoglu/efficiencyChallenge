import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import *
from time import sleep
import time
from datetime import datetime


from urllib import urlopen
from bs4 import BeautifulSoup

def slope(x1,y1, x2,y2):
	return float(y1-y2) / (x1-x2)

def group_lines_and_find_max(lines, middle=600):
	lines_left = list()
	lines_right = list()
	if lines is not None:
		for i in range(len(lines)):
			x1,y1,x2,y2 = lines[i].reshape(4)
			if(x1 < middle and x2 < middle ):
				lines_left.append(i)
			elif(x1 >= middle and x2 >= middle):
				lines_right.append(i)

		max_right_line = 0
		max_left_line = 0
		if len(lines_right) == 0:
			max_right_line = -1
		if len(lines_left) == 0:
			max_left_line = -1
		if max_right_line == -1 or max_left_line == -1:
			return max_right_line, max_left_line

		#find longest line in the right side
		x1,y1,x2,y2 = lines[lines_right[0]].reshape(4)
		max_length = line_length(x1,y1, x2,y2)
		max_right_line = lines_right[0]

		for i in lines_right:
			x1,y1,x2,y2 = lines[i].reshape(4)
			this_line_length = line_length(x1,y1, x2,y2)
			if i == 0:
				max_length = this_line_length
			else:
				if(this_line_length > max_length):
					max_length = this_line_length
					max_right_line = i

		#find longest line in the left side
		x1,y1,x2,y2 = lines[lines_right[0]].reshape(4)
		max_length = line_length(x1,y1, x2,y2)
		max_left_line = lines_left[0]

		for i in lines_left:
			x1,y1,x2,y2 = lines[i].reshape(4)
			this_line_length = line_length(x1,y1, x2,y2)
			if i == 0:
				max_length = this_line_length
			else:
				if(this_line_length > max_length):
					max_length = this_line_length
					max_left_line = i

		#If no line detected in one side, turn to that side
		return max_right_line, max_left_line

def line_length(x1,y1, x2,y2):
	return sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))

def canny_image(copy):
	gray = cv2.cvtColor(copy, cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	canny = cv2.Canny(blur, 50, 150)
	return canny

def display_lines(image, lines):
	line_image = np.zeros_like(image)
	if lines is not None:
		print ("there are " + str(len(lines)) + " lines")
		print lines[0]
		for line in lines:
		    #float rho = lines[i][0], theta = lines[i][1];
			x1,y1,x2,y2 = line.reshape(4)
			cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
			this_line_length = line_length(x1,y1, x2,y2)
#		for i in range(4):
		right,left = group_lines_and_find_max(lines)
		x1,y1,x2,y2 = lines[right].reshape(4)
		cv2.line(line_image, (x1,y1), (x2,y2), (0,0,255), 10)
		x1,y1,x2,y2 = lines[left].reshape(4)
		cv2.line(line_image, (x1,y1), (x2,y2), (0,0,255), 10)
	return line_image

def region_of_interest(image):
	height = image.shape[0]
	width = image.shape[1]
	polygons = np.array([[(0, height), (0, height/2), (width,height/2), (width,height)]])
	mask = np.zeros_like(image)
	cv2.fillConvexPoly(mask, polygons, 255)
	masked_image = cv2.bitwise_and(image,mask)
	return masked_image

#MAIN
"""
while True:
	html = urlopen('http://192.168.137.212/html/')
	bsObj = BeautifulSoup(html.read())
	print bsObj.body.find('img', attrs={'id':'mjpeg_dest'})
	print str(time.time())
	sleep(0.3)
"""

vcap = cv2.VideoCapture('http://192.168.137.212:8000/stream.mjpg')
while True:
	try:
		#image = cv2.imread('test12.jpg')
		#cap = cv2.VideoCapture("test2.mp4")
		#while cap.isOpened():
		#	_, frame = cap.read()
		ret, image = vcap.read()
		copy = np.copy(image)
		gray = cv2.cvtColor(copy, cv2.COLOR_RGB2GRAY)
		blur = cv2.GaussianBlur(gray, (5,5), 0)
		canny = canny_image(copy)
		cropped_image = region_of_interest(canny)
		lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap=5)
		line_image = display_lines(canny, lines)

		right, left = group_lines_and_find_max(lines)
		if right == -1 or left == -1:
			if right == -1:
				print "-----"
			if left == -1:
				print "-----"
		else:
			x1,y1,x2,y2 = lines[right].reshape(4)
			right_slope = slope(x1,y1,x2,y2)
			x1,y1,x2,y2 = lines[left].reshape(4)
			left_slope = slope(x1,y1,x2,y2)
			print("left slope is " + str(left_slope))
			print("right slope is " + str(right_slope))

		#plt.imshow(canny)
		#plt.show()
		cv2.namedWindow('result',cv2.WINDOW_NORMAL)
		cv2.imshow("result",line_image)
		cv2.resizeWindow('result', 600,600)
		#sleep(1)
		#cv2.waitKey(0)
		if cv2.waitKey(22) & 0xFF == ord('q'):
			break
	except TypeError:
		pass