import os
import alexnet
from tensorflow import keras
import image_preprocessing


if __name__ == '__main__':
    alexnet_model: keras.models.Model

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = alexnet.train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)

    image_path = "C:\\Users\\aleks\\Desktop\\image\\testing\\sample2.tif"
    validated_image_path = "C:\\Users\\aleks\\Desktop\\image\\testing\\merged1.jpg"
    image_preprocessing.validate_large_image(alexnet_model,image_path, validated_image_path)

    