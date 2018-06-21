import sys
import time
import cv2
import numpy as np
#from cv2.dnn import readNetFromTensorflow
#from cv2.dnn import blobFromImage
from sklearn.cluster import KMeans, DBSCAN
import serial


def contour_dump( filename, contours, base ):
	img = base.copy()
	cv2.drawContours( img, contours, -1, (0,255,0), 5)
	cv2.imwrite( filename, img)

def get_gray_countour( img, dump=False, filename=None ):
	threshold = np.average(img)+3*np.std(img)
	ret,th = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
	im2, contours, hierarchy = cv2.findContours( th, 1, cv2.CHAIN_APPROX_NONE )
	if dump:
		contour_dump( filename, contours, img )
	return contours

if __name__ == "__main__":
	# img = cv2.imread( sys.argv[1] )
	vc = cv2.VideoCapture(1)
	ret, img = vc.read()

	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# import matplotlib.pyplot as plt
	# plt.imshow(img_gray)
	# plt.show()
	
	contours = get_gray_countour( img_gray, dump=True, filename="result/gray_contour.jpg" )
	if not len(contours) > 0: raise ValueError('contours is null')
