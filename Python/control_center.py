import sys
import time
import cv2
import numpy as np
#from cv2.dnn import readNetFromTensorflow
#from cv2.dnn import blobFromImage
from sklearn.cluster import KMeans, DBSCAN
import serial
from draw_line import get_yellow, get_range
from get_contours import get_gray_countour, contour_dump
from select_contours import contour_leftest, remove_contour

def _control_center( center_point ):

	ang = np.arctan2( center_point[0], center_point[1] )
	print("ang = ", ang)
	turn = 1-abs(ang)
	if turn < 0.1: turn = 0.1
	if ang < 0: turn = -turn
	speed = int(20*abs(turn)+10)
	return speed, turn

def get_contour_center( contour ):
	moment_contour = cv2.moments(contour)
	if moment_contour['m00']:
		moment_contour_x = int(moment_contour['m10']/moment_contour['m00'])
		moment_contour_y = int(moment_contour['m01']/moment_contour['m00'])
		return (moment_contour_x, moment_contour_y)

def get_contour_from_image( img ):
	line_yellows = get_yellow( img )
	line_whites  = get_range( img, np.array([0,100,0], np.uint8), np.array([255,255,255], np.uint8), cv2.COLOR_BGR2HLS)
	line_reds    = get_range( img, np.array([150,0,0], np.uint8), np.array([255,255,255], np.uint8), cv2.COLOR_BGR2HLS)
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert the color image to gray image
	contours = get_gray_countour(img_gray)
	_, contours = remove_contour( line_yellows, contours, 1 )
	_, contours = remove_contour( line_whites, contours, -1 )
	contour_left = contour_leftest(contours)
	return contour_left

def control( contour ):
	contour_center = get_contour_center(contour)
	control_vec = np.subtract( (np.shape(img)[1]/2, np.shape(img)[0]), contour_center )
	speed, turn = _control_center( control_vec )
	print("speed, turn = ", speed, turn)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		img = cv2.imread( filename )
		contour = get_contour_from_image(img)
		control(contour)

