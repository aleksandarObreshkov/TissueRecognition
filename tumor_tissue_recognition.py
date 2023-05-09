import os
import sys
import numpy as np
import alexnet
import tensorflow as tf
from tensorflow import keras


def get_single_image_prediction(alexnet_model, image_path) -> int:

    image = keras.preprocessing.image.load_img(image_path)

    image_numpy = np.array(tf.keras.preprocessing.image.img_to_array(image))
    image_numpy = np.resize(image_numpy, (1, 227, 227, 3))
    return alexnet_model(image_numpy, training=False)


if __name__ == '__main__':
    alexnet_model: keras.models.Model

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = alexnet.train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)
    
    path = sys.argv[1]
    prediction = get_single_image_prediction(alexnet_model, path)
    print(prediction)
