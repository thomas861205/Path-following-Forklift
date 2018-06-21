import sys
import time
import cv2
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import serial
from draw_line import get_yellow, get_range
from get_contours import get_gray_countour, contour_dump

def remove_contour( lines, contours, left_direction, dump=False, filename=None, img=None ):
	# left is 1, other -1
	if len(lines) == 0:
		print("No target lines")
		return 0, contours
	to_be_removed = []
	ret_contour = []
	print("type(contours) = ", type(contours))
	print("lines = ", lines)
	for contour in contours:
		print("type(contour) = ", type(contour))
		moment_contour = cv2.moments(contour)
		# print("moment_contour['m00'] = ", moment_contour['m00'])
		# print("moment_contour['m10'] = ", moment_contour['m10'])
		# print("moment_contour['m01'] = ", moment_contour['m01'])
		if moment_contour['m00']:
			moment_contour_x = int(moment_contour['m10']/moment_contour['m00'])
			moment_contour_y = int(moment_contour['m01']/moment_contour['m00'])

			# print("Center at (", moment_contour_x, ", ", moment_contour_y, ")")
			fit_value = moment_contour_x * lines[0][0] + lines[0][1] - moment_contour_y
			print("(", "{0:.2f}".format(lines[0][0]), "x+", "{0:.2f}".format(lines[0][1]), "), at (", moment_contour_x, ", ", moment_contour_y, "), Value = ", fit_value)

			if left_direction == 1:
				if fit_value * lines[0][0] > 0:
					ret_contour.append(contour)
			else:
				if fit_value * lines[0][0] < 0:
					ret_contour.append(contour)
		else:
			ret_contour.append(contour)
	if dump:
		if img is None:
			raise ValueError('You should input img when you want to dump')
		contour_dump( filename, ret_contour, img)
	return len(contours)-len(ret_contour), np.asarray(ret_contour)

def contour_leftest( contours, dump=False, filename="" ):
	contour_leftest = contours[0]
	x_leftest = sys.maxsize
	for contour in contours:
		moment_contour = cv2.moments(contour)
		if moment_contour['m00']:
			moment_contour_x = int(moment_contour['m10']/moment_contour['m00'])
			if moment_contour_x < x_leftest:
				contour_leftest = contour
				x_leftest = moment_contour_x
	if dump:
		contour_dump( filename, contour_leftest, img)
	return contour_leftest

def contour_largest( contours, dump=False, filename="" ):
	contour_largest = contours[0]
	x_largest = 0
	for contour in contours:
		area = cv2.contourArea(contour)
		# print("area = ", area)
		if area > x_largest:
			contour_largest = contour
			x_largest = area
	if dump:
		contour_dump( filename, contour_largest, img)
	return contour_largest

if __name__ == "__main__":
	global filename, f, start_time

	# img = cv2.imread( sys.argv[1] )


	vc = cv2.VideoCapture(1)
	ret, img = vc.read()

	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert the color image to gray image
	contours = get_gray_countour(img_gray)

	if sys.argv[1] == "leftest":
		contour_left = contour_leftest(contours, dump=True, filename="result/contours_leftest.jpg")
	if sys.argv[1] == "largest":
		contour_largest = contour_largest(contours, dump=True, filename="result/contours_largest.jpg")
	if sys.argv[1] == "line_separate":
		_, contours = remove_contour( line_yellows, contours, 1 )
		_, contours = remove_contour( line_whites, contours, -1, dump=True, filename = "result/contours_extracted.jpg", img=img )
