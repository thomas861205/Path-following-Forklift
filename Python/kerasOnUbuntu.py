
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
from keras.models import load_model
from scipy.misc import imresize

label = {0: 'neg', 1: 'pos'}
# If you train multiple classes, you may change the index to your label.

def pikachu( frame = None ):

    global label

    if frame is None:
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()

    model = load_model("src/mobil_e30.h5")

    frame_resize = imresize(frame, (128, 128))
    # [possibility_neg, possibility_pos]
    ans = model.predict(np.expand_dims(frame_resize, axis=0))
    ans = ans.argmax(axis=-1)
    print(label[ans[0]])    
    # cv2.imwrite('a.jpg', frame)

if __name__ == "__main__":

    pikachu("mobil_e30.h5")

