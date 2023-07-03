import slideio
from scipy import ndimage
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

    patches_arr = flatten_patches(patches)
    patches_results = run_patch_batches_in_nn(patches_arr, cnn)
    binarise_patches(patches_arr, patches_results)

    merged = unpatchify(patches, (tiles_y*IMAGE_SIZE, tiles_x*IMAGE_SIZE, 3))
    tf.keras.preprocessing.image.save_img(validated_image_path, merged)
    return merged


def flatten_patches(patches):
    patches_arr = []
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patches_arr.append(patch)
    return patches_arr


def run_patch_batches_in_nn(patches_arr, cnn):
    batch_size = 32
    patches_results = []
    for index in range(0, len(patches_arr), batch_size):
         sub_arr = patches_arr[index:index+batch_size]
         results = cnn(np.array(sub_arr))
         patches_results.extend(results)
    return patches_results


def binarise_patches(patches_arr, patches_results):
    it = 0
    for patch_result in patches_results:
         if patch_result>0.7: patches_arr[it][...] = 0
         it+=1


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
    img_mask = img_mask.filter(ImageFilter.BoxBlur(20))
    return img_mask

# Thresholds the smoothed binary image and draws contours
def outline_tumors(filtered_img_path, original_img_path, result_path):
    filtered_image = cv2.imread(filtered_img_path)
    original_image = cv2.imread(original_img_path)

    shifted = cv2.pyrMeanShiftFiltering(filtered_image, 21, 51)
    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    cv2.drawContours(original_image, contours, -1, (0, 0, 255), 8, lineType=cv2.LINE_8)

    Image.fromarray(original_image).save(result_path)


def apply_tumor_mask(image_path, mask):
    with Image.open(image_path) as image:
        image.load()
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