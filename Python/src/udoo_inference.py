# Author : Yi-Chun Hung
# Email : nick831111@gmail.com
# Date : 05/29/2018
# Usage : Run the trained model on udoo.

import cv2
import argparse
from scipy.misc import imresize

label = {0: 'neg', 1: 'pos'}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Load the trained model and run.')
    parser.add_argument("--model_path", required=True, help="The path to the model file.", type=str)
    parser.add_argument("--target_img_size", required=True, nargs='*', help="The image size to inference", type=int)
    args = parser.parse_args()

    if len(args.target_img_size) > 2:
        raise Exception('length of traget_img_size should be 2')


    net = cv2.dnn.readNetFromTensorflow(args.model_path)
    cap = cv2.VideoCapture(0)

    while 1:
        ret, frame = cap.read()
        frame = imresize(frame, tuple(args.target_img_size))
        frame = cv2.dnn.blobFromImage(frame)
        net.setInput(frame)
        pred = net.forward()

        ans = pred[0, :, 0, 0].argmax(axis=-1)
        print(label[ans])
