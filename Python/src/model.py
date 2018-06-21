
import keras
import argparse
from keras_squeezenet import SqueezeNet
from dataloader import Dataloader
from sklearn.model_selection import train_test_split
from keras.applications.mobilenet import MobileNet
from keras.layers import Conv2D, Reshape, Activation, Dropout, GlobalAveragePooling2D
from keras.models import Model

def add_squeezenet_top(pre_model, classes, tunable = False):
    # Add the classification layers to squeezenet
    #   parameters :
    #       pre_model : Feature extraction layers in squeezenet.
    #       classes (Int) : Number of classes in your label file.
    #       tunable (Bool) : If freeze the weight of feature extraction layers.
    #               If True, it will need more data to train, and be more time-consuming.
    #   return :
    #       model : The model including feature extraction layers and classification layers.

    for layer in pre_model.layers:
        layer.trainable = tunable
    x = pre_model.layers[-1].output
    x = Dropout(0.5,name='drop9')(x)
    x = Conv2D(classes, (1,1), padding='valid', name='conv10')(x)
    x = Activation('relu', name='relu_conv10')(x)
    x = GlobalAveragePooling2D()(x)
    x = Activation('softmax', name='loss')(x)
    model = Model(inputs=pre_model.layers[0].input,outputs=x)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def add_mobilenet_top(pre_model, classes, tunable = False):
    # Add the classification layers to mobilenet
    #   parameters :
    #       pre_model : Feature extraction layers in squeezenet.
    #       classes (Int) : Number of classes in your label file.
    #       tunable (Bool) : If freeze the weight of feature extraction layers.
    #               If True, it will need more data to train, and be more time-consuming.
    #   return :
    #       model : The model including feature extraction layers and classification layers.

    for layer in pre_model.layers:
         layer.trainable = tunable
    x = pre_model.layers[-1].output
    x = Reshape((1, 1, 1024))(x)
    x = Dropout(0.3, name='Dropout')(x)
    x = Conv2D(classes, (1, 1), padding='same')(x)
    x = Activation('softmax', name='softmax')(x)
    output = Reshape((classes,))(x)
    model = Model(inputs=pre_model.layers[0].input, outputs=output)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Train a model.')
    parser.add_argument("--data_base", required = True, help = "The directory path to the data.", type = str)
    parser.add_argument("--label_path", required = True,  help = "The path to the label file.", type = str)
    parser.add_argument("--model_path", required = True, help = "The path to save the training model", type = str)
    parser.add_argument("--pos_neg_num", required = False, nargs = '*', help = "The number of postive and negative training data <pos neg>", type = int, default = [400, 400])
    parser.add_argument("--target_img_size", required = False, nargs = '*', help = "The training image size <width height>", type = int, default = [128, 128])
    parser.add_argument("--if_feature_trainable", required = False, help = "If the feature extraction layers trainable", type = bool, default = False)
    parser.add_argument("--split_ratio", required = False, help = "The split ratio for training data and validation data", type = float, default = 0.1)
    parser.add_argument("--classes", required = False, help = "The number of classes in labeling.", type = int, default = 2)
    parser.add_argument("--batch_epoch_size", required = False, nargs = '*', help = "The number of batch size and epoch size (batch, epoch)", type = int, default = [16, 30])
    args = parser.parse_args()

    if len(args.pos_neg_num)!=2 or len(args.target_img_size)!=2 or len(args.batch_epoch_size)!=2 :
      raise Exception("--pos_neg_num, --target_img_size, and --batch_epoch_size should follow with 2 args.")

    # MobileNet still needs to check how to train it.

    # model = MobileNet(input_shape=(128, 128, 3), alpha=1.0, depth_multiplier=1, dropout=1e-3, include_top=False, weights='imagenet', input_tensor=None, pooling='avg', classes=2)
    #print(model.summary())
    # model = add_mobilenet_top(model, 2, True)

    model = SqueezeNet(include_top=False) # Construct the feature extraction layers in squeezenet.
    model = add_squeezenet_top(model, args.classes, False) # Add the classification layers to squeezenet.
    data_set = Dataloader(args.data_base,args.label_path) # Construct the Dataloader class
    data, label = data_set.read_data(args.pos_neg_num,args.target_img_size) # Read the data
    X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=args.split_ratio, random_state=42)
        # Split the data into training and validation
    y_train = keras.utils.to_categorical(y_train, args.classes)
    y_test = keras.utils.to_categorical(y_test, args.classes)
        # Convert the label to one-hot label
    batch_size = args.batch_epoch_size[0] # Set the batch size of training, normally 16 or 32
    nb_epoch = args.batch_epoch_size[1] # Set the epoch size of training

    model.fit(X_train, y_train, batch_size=batch_size, epochs=nb_epoch, verbose=1, validation_data=(X_test, y_test))
        # Start training
    model.save(args.model_path)
        # Save the model to specific path
