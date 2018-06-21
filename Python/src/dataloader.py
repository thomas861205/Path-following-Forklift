# Author : Yi-Chun Hung
# Email : nick831111@gmail.com
# Date : 05/28/2018
# Usage : For loading data

import scipy.misc
import os
import pickle as pkl
import numpy as np
import argparse
from tqdm import tqdm
from scipy.misc import imresize

class Dataloader():

    def __init__(self,data_base,label_path):
        # Constructor
        #   Parameters :
        #       data_base (str) : The path to data base.
        #       label_path (str) : The path to the label file.
        #
        self.data_base = data_base
        self.label_path = label_path
        if os.path.isfile(label_path):
             self.label = pkl.load(open(label_path,"rb"))
             assert (type(self.label)==dict), "label file must be dict type."
             # Check for the type of label file. It only supports dict format.
        else:   # Check if the path is right.
            raise Exception("label file url is wrong.")

    def read_data(self, pos_neg_num, target_size):
        # Read the data
        #   Parameters :
        #       pos_neg_num (tuple) : Number of postive and negtive data (pos, neg).
        #       target_size (tuple) : The size for resizing image (width, height).
        #
        #   Return :
        #       data (np-array) : (num, width, heigh, channel), umm, data of course.
        #       label (np-array) : (num,), label.

        pos_num = pos_neg_num[0]
        neg_num = pos_neg_num[1]
        pos_data = []
        neg_data = []
        img_files = [img_file for img_file in os.listdir(self.data_base) if img_file.endswith(".jpg")]
        valid_img_files = list(set(img_files) & set(self.label.keys()))
        data_pos_num = list(self.label.values()).count("1")
        data_neg_num = list(self.label.values()).count("0")
        if pos_num > data_pos_num or neg_num > data_neg_num :
            print("There are only {} pos, and {} neg".format(data_pos_num, data_neg_num))
            raise Exception('No enough pos_num or neg_num')
        pbar = tqdm(total = pos_num + neg_num)
        for img_name in valid_img_files:
            img = scipy.misc.imread(os.path.join(self.data_base,img_name))
            img = imresize(img,target_size)
            if len(pos_data) >= pos_num and len(neg_data) >= neg_num:
                break
            if self.label[img_name] == '1':
                if len(pos_data) < pos_num :
                    pos_data.append(img)
                    pbar.update(1)
            else :
                if len(neg_data) < neg_num :
                    neg_data.append(img)
                    pbar.update(1)
        pbar.close()
        data = pos_data + neg_data
        data = np.stack(data,axis=0)
        label = np.concatenate((np.ones(pos_num),np.zeros(neg_num)))

        return data, label


if __name__ == "__main__":
    # add the argument to parse
    parser = argparse.ArgumentParser(description = 'Generate the data and label in the format for training.')
    parser.add_argument("--data_base", required = True, help = "The directory path to the data.", type = str)
    parser.add_argument("--label_path", required = True,  help = "The path to the label file.", type = str)
    parser.add_argument("--pos_neg_num", required = False, nargs='*', help = "The number of pos and neg images <pos neg>", type = int, default = [200, 200])
    parser.add_argument("--target_size", required = False, nargs='*', help = "The resize images size <width height>", type = int, default = [128, 128])

    # parse args
    args = parser.parse_args()
    if len(args.pos_neg_num)!=2 or len(args.target_size)!=2:
       raise Exception('--pos_neg_num and --target_size should be put 2 args in the following.')
    dataloader = Dataloader(args.data_base,args.label_path)
    data, label = dataloader.read_data(args.pos_neg_num,tuple(args.target_size))
    # print(data.shape, data[0].shape)
    print(label.shape)
