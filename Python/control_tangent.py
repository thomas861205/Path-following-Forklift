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

def control( line_yellows, line_whites ):
	angle_diffs = []
	if not line_yellows == []:
		slope_yellows =  [line[0] for line in line_yellows]
		slope_yellow = np.average( slope_yellows, axis=0 )
		if slope_yellow > 0:
			angle_diff_yellow = np.arctan(slope_yellow) - np.pi/2
		else:
			angle_diff_yellow = np.arctan(slope_yellow) + np.pi/2 
		print("slope yellow = ", slope_yellow)
		angle_diffs.append(angle_diff_yellow)

	if not line_whites == []:
		slope_whites =  [line[0] for line in line_whites]
		slope_white = np.average( slope_whites, axis=0 )
		if slope_white > 0:
			angle_diff_white = np.arctan(slope_white) - np.pi/2
		else:
			angle_diff_white = np.arctan(slope_white) + np.pi/2
		print("slope white = ", slope_white)
		angle_diffs.append(angle_diff_white)

	angle_diff = np.average(angle_diffs)
	print("angle diff = ", angle_diff)
	print( "controller = ", _control_center( (np.sin(angle_diff), np.cos(angle_diff) ))) 

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		img = cv2.imread( filename )
		line_yellows = get_yellow( img )
		line_whites  = get_range( img, np.array([0,100,0], np.uint8), np.array([255,255,255], np.uint8), cv2.COLOR_BGR2HLS )
		control( line_yellows, line_whites )
