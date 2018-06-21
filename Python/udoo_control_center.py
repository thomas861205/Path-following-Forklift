import sys
import time
import cv2
import numpy as np
#from cv2.dnn import readNetFromTensorflow
#from cv2.dnn import blobFromImage
from sklearn.cluster import KMeans, DBSCAN
import serial
from calibrate import *
from draw_line import get_yellow, get_white, get_red, get_range
from get_contours import get_gray_countour, contour_dump
from select_contours import contour_leftest, remove_contour, contour_largest
from kerasOnUbuntu import pikachu

redline_cnt = 0

def _control_center( center_point ):

	ang = np.arctan2( center_point[0], center_point[1] )
	# print("ang = ", ang)
	turn = 1-abs(ang)
	if turn < 0.1: turn = 0.1
	if ang < 0: turn = -turn
	# speed = int(20*abs(turn)+10)
	speed = int(20*abs(turn) + 50)
	return speed, turn

def get_contour_center( contour ):
	moment_contour = cv2.moments(contour)
	if moment_contour['m00']:
		moment_contour_x = int(moment_contour['m10']/moment_contour['m00'])
		moment_contour_y = int(moment_contour['m01']/moment_contour['m00'])
		return (moment_contour_x, moment_contour_y)

def get_contour_from_image( img ):
	line_yellows = get_yellow( img )
	# line_whites  = get_white( img )
	line_reds    = get_red( img )

	global redline_cnt

	if not line_reds:
		
		redline_cnt = 0
		print("no red line")

	else:
		redline_cnt += 1
		# cmd = "redline \n"
		# s.write(cmd.encode())
		print("red lines:{0}".format(redline_cnt))

	if redline_cnt >= 20:

		cmd = "/ServoStop/run \n"

		s.write(cmd.encode())

		return None

	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert the color image to gray image
	contours = get_gray_countour(img_gray)

	# contour_dump( "img/contours_full" + str(int(time.time()*10)) + ".jpg", contours, img)

	_, contours = remove_contour( line_yellows, contours, 1 )
	if len(contours) == 0: return None

	# _, contours = remove_contour( line_whites, contours, -1 )
	# if len(contours) == 0: return None

	contour_large = contour_largest(contours)
	# contour_dump( "img/contours_extracted" + str(int(time.time()*10)) + ".jpg", contour_large, img)
	contour_dump( "img/contours_extracted.jpg", contour_large, img)
	return contour_large

def control( contour, s ,img):
	contour_center = get_contour_center(contour)
	if contour_center is None: return
	# print("contour center = ", contour_center)

	control_vec = np.subtract( (np.shape(img)[1]/2, np.shape(img)[0]), contour_center )
	speed, turn = _control_center( control_vec )
	cmd = "/ServoTurn/run " + str(speed) + " " + "{0:.2f}".format(turn) + " \n"
	# print("cmd = ", cmd)

	s.write(cmd.encode())
	# print("speed, turn = ", speed, turn)

def ServoStop():

	cmd = "/ServoStop/run \n"

	s.write(cmd.encode())

def ServoCtrl( speed = 50, sec = 1):
	cmd = "/ServoCtrl/run {0} \n".format(speed)

	s.write(cmd.encode())

	time.sleep(sec)

	cmd = "/ServoStop/run \n"
	
	s.write(cmd.encode())

def HangerCtrl( angle ):

	cmd = "/HangerCtrl/run {0} \n".format( angle )
	
	s.write(cmd.encode())


def HangerReset():

	# cmd = "/HangerStop/run \n"

	cmd = "/HangerCtrl/run -40 \n"
	
	s.write(cmd.encode())

def ServoTurn(speed = 80, turn = 0.3):

	cmd = "/ServoTurn/run {0} {1} \n".format(speed, turn)

	s.write(cmd.encode())

def main():

	global redline_cnt
	redline_cnt = 0

	for i in range(0,20): vc.read()

	while 1:

		start_time = time.time()
		_, img = vc.read()

		img = calibrate(img)

		contour = get_contour_from_image(img)
		if contour is None: break
		if not contour is None: control(contour,s,img)
	
	return

if __name__ == "__main__":
	s = serial.Serial("/dev/ttyACM0")
	# s = serial.Serial("/dev/ttyACM1")

	vc = cv2.VideoCapture(1)
	# vc = cv2.VideoCapture(0)

	# for i in range(0,20): vc.read()
	# # f = open("timer.txt", "w")

	ServoStop()
	HangerReset()
	main()


	
	ServoCtrl()

	time.sleep(1)


	ret, img = vc.read()

	pikachu( img )

	ServoCtrl(-50, 1)

	ServoTurn(80, 0.02)

	time.sleep(3)

	ServoStop()

	ServoCtrl(-65, 0.5)

	ServoStop()

	HangerCtrl(30)

	time.sleep(0.8)

	# HangerReset()

	# ServoCtrl(50, 1)

	# main()

