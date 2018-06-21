import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import sys
def photo():
    img_saving_base = "/home/ell/ee2405/emlab5/img"
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    filename = "img.jpg"
    cv2.imwrite(os.path.join(img_saving_base,filename), frame)
    camera.release()

photo()
img_saving_base = "/home/ell/ee2405/emlab5/img"
filename = "img.jpg"
img = cv2.imread(os.path.join(img_saving_base,filename))
if sys.argv[1] == "BGR2HLS":
    print("Config: BGR2HLS")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
elif sys.argv[1] == "BGR2HSV":
    print("Config: BGR2HSV")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
else:
    print("Config: BGR2RGB")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()
