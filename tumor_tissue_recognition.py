import tensorflow as tf
from tensorflow import keras
import dataset_service as datasets
import os
import metrics
import alexnet
import numpy as np

def train_model():
    alexnet_model = alexnet.create_model()
    alexnet_model.fit(train_ds,
                epochs=100,
                validation_data=validation_ds,
                validation_freq=1,
                callbacks=[tensorboard_cb])
    alexnet_model.evaluate(test_ds)
    alexnet_model.save(alexnet.model_name)
    return alexnet_model

if __name__ == '__main__':
    run_logdir = metrics.get_run_logdir()
    tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)
    alexnet_model: keras.models.Model
    (train_ds, test_ds, validation_ds) = datasets.get_datasets()

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)
    
    path = f"{os.curdir}/Tumor samples/tiff/TUM/TUM-TCGA-QEKTGGKG.tif"
    image = keras.preprocessing.image.load_img(path)

    image_numpy = np.array(tf.keras.preprocessing.image.img_to_array(image))
    image_numpy = np.resize(image_numpy, (1, 227, 227, 3))
    alexnet_model.evaluate(test_ds)
    prediction = alexnet_model(image_numpy, training=False)
    print(prediction)
