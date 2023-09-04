import re
import numpy as np
from  rgb_transform import RGBTransform
from PIL import Image


def merge(file_to_image_map, patch_size, image_shape, original_image_name, results_arr):
    result = np.ones(image_shape, dtype=np.uint8)
    result[:,:,:] = 255

    result_no_tint = np.ones(image_shape, dtype=np.uint8)
    result_no_tint[:,:,:] = 255

    print("Starting to merge original image")
    print(f"Result image shape is {image_shape}")

    counter = 0
    for (file_name, image) in file_to_image_map:
        match = re.search(f"{original_image_name}_(\d+)_(\d+)_.png", file_name)
        row = int(match.group(1))*patch_size
        col = int(match.group(2))*patch_size

        result_no_tint[col:col+patch_size, row:row+patch_size] = image
        image = apply_tint(image, results_arr[counter])
        
        result[col:col+patch_size, row:row+patch_size] = image
        counter += 1
    print("Made the result images")
    return result_no_tint, result


def apply_tint(patch, result):
    patch = Image.fromarray(patch)
    if(result >= 0.8):
        patch = RGBTransform().mix_with((240, 148, 62),factor=.30).applied_to(patch) 
    patch = np.array(patch)
    return patch