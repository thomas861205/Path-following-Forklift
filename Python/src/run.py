
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
from keras.models import load_model
from scipy.misc import imresize

label = {0: 'neg', 1: 'pos'}
# If you train multiple classes, you may change the index to your label.

def pikachu(model_path = "src/mobil_e30.h5"):

    global label

    # parser = argparse.ArgumentParser(description='Load the trained model and run.')

    # parser.add_argument("--model_path",
    #                     required=True,
    #                     help="The path to the model file.",
    #                     type=str)

    # parser.add_argument("--target_img_size",
    #                     required=True,
    #                     nargs='*',
    #                     help="The target image size to the model.",
    #                     type=int)
    # parser.set_defaults(model_path = "mobil_e30.h5", traget_img_size = [128, 128])
    # args = parser.parse_args()

    # if len(args.target_img_size) != 2:
        # raise Exception('length of traget_img_size should be 2')

    cap = cv2.VideoCapture(1)

    # model = load_model(args.model_path)

    model = load_model(model_path)

    for _ in range(10):
        ret, frame = cap.read()
        # frame_resize = imresize(frame, tuple(args.target_img_size))

        frame_resize = imresize(frame, (128, 128))
        # [possibility_neg, possibility_pos]
        ans = model.predict(np.expand_dims(frame_resize, axis=0))
        ans = ans.argmax(axis=-1)
        print(label[ans[0]])
        cv2.imwrite('a.jpg', frame)

if __name__ == "__main__":

    pikachu("mobil_e30.h5")

