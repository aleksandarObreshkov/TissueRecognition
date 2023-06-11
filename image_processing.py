import slideio
from patchify import patchify, unpatchify
from PIL import Image, ImageFilter
import numpy as np
import tensorflow as tf
import cv2
import imutils

IMAGE_SIZE = 10

# Results in a pixelated image with black squares for places without tumours
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
            result = cnn(np.reshape(patch, (1, IMAGE_SIZE, IMAGE_SIZE, 3))) #i believe this can be optimised
            result = np.array(result)[0]
            if result > 0.7: patch[...] = 0
    
    merged = unpatchify(patches, (tiles_y*IMAGE_SIZE, tiles_x*IMAGE_SIZE, 3))
    tf.keras.preprocessing.image.save_img(validated_image_path, merged)
    return merged

# Results in a smoothed-out binary image of the pixelated one with white for tumors and black for non-tumorous cells
def get_tumor_mask(analyzed_image_path):
    
    image = Image.open(analyzed_image_path)
    
    image_greyscale = image.convert("L")
    threshold = 0 # white, 0 - black
    img_mask = image_greyscale.point(
     lambda x: 0 if x == threshold else 255
    )

    for _ in range(20):
        img_mask = img_mask.filter(ImageFilter.MaxFilter(3))

    for _ in range(20):
        img_mask = img_mask.filter(ImageFilter.MinFilter(3))

    img_mask = img_mask.convert("L")
    #img_mask = 255 - np.array(img_mask)
    img_mask = img_mask.filter(ImageFilter.BoxBlur(20))
    return img_mask


def outline_tumors(filtered_img_path, original_img_path):
    image = cv2.imread(filtered_img_path)
    original = cv2.imread(original_img_path)
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)

    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.drawContours(original, cnts, -1, (0, 0, 255), 8, lineType=cv2.LINE_8)

    Image.fromarray(original).save("C:\\Users\\aleks\\Desktop\\image\\testing\\result.png")


def apply_tumor_mask(image_path, mask):
    image = Image.open(image_path)
    w, h = np.array(mask).shape
    image = image.resize([h, w])
    blank = image.point(lambda _:0)
    tumor_image = Image.composite(image, blank, mask)
    return tumor_image


def apply_peaks(binary_arr, peaks):
	for peak in peaks:
		x = peak[0]
		y = peak[1]
		binary_arr[x][y] = True
	return binary_arr