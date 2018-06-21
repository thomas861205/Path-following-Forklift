import sys
import time
import cv2
import numpy as np
#from cv2.dnn import readNetFromTensorflow
#from cv2.dnn import blobFromImage
from sklearn.cluster import KMeans, DBSCAN
import serial
from draw_line import get_yellow, get_range
from get_contours import get_gray_countour, contour_dump, remove_contour, contour_leftest

def control_arc( accept_pts ):
	avg_ang = np.average(accept_pts)
	turn = 1-abs(avg_ang)
	if turn < 0.1: turn = 0.1
	if avg_ang < 0: turn = -turn
	speed = int(20*abs(turn)+10)
	return speed, turn

def uphalf_circle( center, r ):
	ret = []
	for ang in range(180,360):
		rad = ang/180*3.14
		ret.append(tuple([int(center[0]+r*np.cos(rad)), int(center[1]+r*np.sin(rad)) ]))
	# print("ret = ", ret)
	return ret

def draw_line_in_contours( img, contour ):
	accept_pts = []
	for detect_radius in range(int(np.shape(img)[0]*0.85),1,-100):
	# while len(accept_pts) == 0:
		detect_circle = uphalf_circle((np.shape(img)[1]/2,np.shape(img)[0]), detect_radius)
		for detect_pt in detect_circle:
			if cv2.pointPolygonTest( contour, detect_pt, 0 ) > 0:
				cv2.line( img, tuple(detect_pt), tuple(detect_pt), (0,255,0), 3)
				ang = np.arctan2( np.shape(img)[1]/2-detect_pt[0], np.shape(img)[0]-detect_pt[1] )
				accept_pts.append(ang)
		if len(accept_pts): return accept_pts
if __name__ == "__main__":
	global filename, f, start_time
	filename = "test"

	img = cv2.imread( sys.argv[1] )
	print("img size = ", np.shape(img))
	line_yellows = get_yellow( img )
	line_whites  = get_range( img, np.array([0,100,0], np.uint8), np.array([255,255,255], np.uint8), cv2.COLOR_BGR2HLS)
	line_reds    = get_range( img, np.array([150,0,0], np.uint8), np.array([255,255,255], np.uint8), cv2.COLOR_BGR2HLS)
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert the color image to gray image
	contours = get_gray_countour(img_gray)
	_, contours = remove_contour( line_yellows, contours, 1 )
	_, contours = remove_contour( line_whites, contours, -1 )
	contour_left = contour_leftest(contours)
	accept_pts = draw_line_in_contours( img, contour_left )
	speed, turn = control_arc( accept_pts )
	print("speed, turn = ", speed, turn)
