import cv2
import sys
import matplotlib.pyplot as plt

img = cv2.imread(sys.argv[1])
if sys.argv[2] == "BGR2HLS":
    print("Config: BGR2HLS")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
elif sys.argv[2] == "BGR2HSV":
    print("Config: BGR2HSV")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
else:
    print("Config: BGR2RGB")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()
