import os
import numpy as np
import alexnet
import tensorflow as tf
from tensorflow import keras
from datasets import dirs


def get_single_image_prediction(alexnet_model, image_path):
    training_data_gen = tf.keras.preprocessing.image.ImageDataGenerator().flow_from_directory(directory=image_path,
                                                            batch_size=1)
    
    res_from_single_image = alexnet_model(training_data_gen.next()[0])
    print(res_from_single_image)
    index = np.array(res_from_single_image).argmax()
    return dirs[index]


if __name__ == '__main__':
    alexnet_model: keras.models.Model

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = alexnet.train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)

    print(get_single_image_prediction(alexnet_model, "C:\\Users\\aleks\\Desktop\\image"))
    