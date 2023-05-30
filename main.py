import os
import alexnet
from tensorflow import keras
import image_processing


if __name__ == '__main__':
    alexnet_model: keras.models.Model

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = alexnet.train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)

    image_path = "C:\\Users\\aleks\\Desktop\\image\\testing\\sample4.png"
    validated_image_path = "C:\\Users\\aleks\\Desktop\\image\\testing\\merged6.png"
    validated_img = image_processing.analyze_image(alexnet_model, image_path, validated_image_path)
    tumor_mask = image_processing.get_tumor_mask(validated_image_path)
    result = image_processing.apply_tumor_mask(image_path, tumor_mask)
    result.show()
