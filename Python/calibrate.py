import sys
import cv2
import numpy as np

def calibrate( img, dump=False, filename="" ):
	global img_size
	img_size = (160,120)
	img_width = img_size[0]
	img_height = img_size[1]
	transform_ratio = 0.9
	transform_dst = np.float32([ [0,0], [img_width,0], [img_width,img_height], [0,img_height]])
	transform_src = np.float32([ [int((1-transform_ratio)*img_width),0], [int(transform_ratio*img_width),0], [img_width,img_height], [0,img_height]])

	M = cv2.getPerspectiveTransform(transform_src, transform_dst)
	img_resized = cv2.resize( img, img_size, interpolation=cv2.INTER_CUBIC )
	img_warp_resized = cv2.warpPerspective(img_resized, M, img_size, flags=cv2.INTER_NEAREST)
	if dump: cv2.imwrite( filename, img_warp_resized )
	return img_warp_resized

if __name__ == "__main__":
	# img = cv2.imread( sys.argv[1] )
	camera = cv2.VideoCapture(1)
	ret, img = camera.read()
	img_calibrated = calibrate( img, dump=True, filename="result/calibrated_test.jpg" )
