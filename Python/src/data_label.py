# Author : Yi-Chun Hung
# Email : nick831111@gmail.com
# Date : 05/26/2018
# Usage : For label

import os
import pickle
import matplotlib.image as mpimg
import argparse
import cv2
from matplotlib import pyplot as plt
from subprocess import call

class Data_label():
    # it only supports 2 labels {0, 1} for now.

    def __init__(self, data_base, label_path):
        # Parameters :
        #   data_base (str) : The data base directory.
        #   label_path (str) : The label file, if not exist, it will create one.
        #

        self.data_base = data_base
        self.label_path = label_path
        self.data = [data for data in os.listdir(data_base) if data.endswith(".jpg")]
            # Only take the file name ending with ".jpg" in data_base.

        if os.path.isfile(label_path):
            self.label = pickle.load(open(label_path,"rb"))
            assert (type(self.label)==dict), "label file must be dict type."
            # Check for the type of label file. It only supports dict format.

        else:   # If path not exists, just create one.
            self.label = {}

    def show_info(self):
        # To show the label quality.
        #
        # Parameters :
        #    None
        #

        print("There are {} images in total.".format(len(self.data)))
        print("There are {} label.".format(len(self.label)))
        self.missing_data = list(set(self.data) - set(self.label.keys()))
        self.valid_data = list(set(self.data) & set(self.label.keys()))
        print("There are {} valid label and {} missing label.\n".format(len(self.valid_data), len(self.missing_data)))
        all_label = [self.label[idx] for idx in self.valid_data]

        if len(all_label) <= 0:
            print("Start from blank label file")
        else:
            print("label   count  %")
            print("=======================")
            print("positive {}  {}%".format(all_label.count("1"),all_label.count("1")*100/len(all_label)))
            print("negative {}  {}%".format(all_label.count("0"),all_label.count("0")*100/len(all_label)))
            print("=======================")

    def clean_label_file(self, save_path):
        # Clean the label file by delete the labeled images which is not in data base.
        #
        # Parameters :
        #    save_path (str) : The saving path for cleaned label, which take out the labels not in data.
        #

        self.label = {k:self.label[k] for k in self.valid_data}
        pickle.dump(self.label,open(save_path, "wb"))

    def start_label(self, duplicate_base):
        # Ummm, start label, of course...
        #
        # Parameters :
        #    duplicate_base (str) : The saving base for the data which is labeled as duplicate.
        #
        # For labeling :
        #    "1" : for positive, which means the object is in the image.
        #    "0" : for negative, which means the object is NOT in the image.
        #    "e" : Ending label, it will save the current label to the label file.
        #    Other keys : Move the duplicated data into duplicate_base.
        #

        print("'1' : for positive, which means the object is in the image.")
        print("'0' : for negative, which means the object is NOT in the image.")
        print("'e' : Ending label, it will save the current label to the label file.")
        print("Other keys : Move the duplicated data into duplicate_base.")
        plt.ion()
        plt.show()
        for img_name in self.missing_data:
            img = mpimg.imread(os.path.join(self.data_base, img_name))
            plt.imshow(img)
            print(img_name+" : ", end="")
            key = input()
            if key == "1" or key == "0":
                self.label[img_name] = key
            elif key == "e":
                break
            else:
                call(["mv", os.path.join(self.data_base, img_name), duplicate_base])

        pickle.dump(self.label, open(self.label_path,"wb")) # Save the label file as pickle format.


if __name__ == "__main__":
    # add the argument to parse
    parser = argparse.ArgumentParser(description = 'label the data in the fast way.')
    parser.add_argument("--data_base", required = True, help = "The directory path to the data.", type = str)
    parser.add_argument("--label_path", required = True,  help = "The path to the label file.", type = str)
    parser.add_argument("--dup_base", required = True, help = "The duplicate directory.", type = str)

    # parse args
    args = parser.parse_args()
    Data = Data_label(args.data_base, args.label_path) # construct the data_label class
    Data.show_info() # show the data quality of label
    Data.clean_label_file(args.label_path)
    Data.start_label(args.dup_base) # start label
