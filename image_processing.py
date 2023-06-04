import slideio
from patchify import patchify, unpatchify
from PIL import Image, ImageFilter
import numpy as np
import tensorflow as tf

IMAGE_SIZE = 10


def analyze_image(cnn, large_image_path, validated_image_path):
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
            if result > 0.7: patch[...] = 255
    
    merged = unpatchify(patches, (tiles_y*IMAGE_SIZE, tiles_x*IMAGE_SIZE, 3))
    tf.keras.preprocessing.image.save_img(validated_image_path, merged)
    return merged


def get_tumor_mask(analyzed_image_path):
    
    with Image.open(analyzed_image_path) as image:
        image.load()

    image_greyscale = image.convert("L")
    threshold = 255 # white, 0 - black
    img_mask = image_greyscale.point(
     lambda x: 255 if x == threshold else 0
    )

    for _ in range(20):
        img_mask = img_mask.filter(ImageFilter.MinFilter(3))

    for _ in range(20):
        img_mask = img_mask.filter(ImageFilter.MaxFilter(3))


    img_mask = img_mask.convert("L")
    img_mask = 255 - np.array(img_mask)
    img_mask = Image.fromarray(img_mask).filter(ImageFilter.BoxBlur(20))
    img_mask.show()
    return img_mask


def apply_tumor_mask(image_path, mask):
    with Image.open(image_path) as image:
        image.load()
    w, h = np.array(mask).shape
    image = image.resize([h, w])
    blank = image.point(lambda _:0)
    tumor_image = Image.composite(image, blank, mask)
    return tumor_image
