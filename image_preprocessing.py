import slideio
from patchify import patchify, unpatchify
from PIL import Image
import numpy as np
import tensorflow as tf

IMAGE_SIZE = 50


def validate_large_image(cnn, large_image_path, validated_image_path):
    image = Image.open(large_image_path)
    image = np.array(image, dtype='float')
    print(f"Image shape is: {image.shape}")
    patches = patchify(image, (IMAGE_SIZE, IMAGE_SIZE, 3), step=IMAGE_SIZE)
    (tiles_y, tiles_x, _, _, _, _) = patches.shape
    print(f"Patches shape is: {patches.shape}")

    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            result = cnn(np.reshape(patch, (1, IMAGE_SIZE, IMAGE_SIZE, 3)))
            result = np.array(result)[0]
            if result > 0.5: patch[...] = 255
    
    merged = unpatchify(patches, (tiles_y*IMAGE_SIZE, tiles_x*IMAGE_SIZE, 3))
    merged = tf.keras.preprocessing.image.save_img(validated_image_path, merged)
            