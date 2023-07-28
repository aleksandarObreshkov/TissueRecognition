import re
import numpy as np
from  rbg_transform import RGBTransform
from PIL import Image


def merge(file_to_image_map, patch_size, image_shape, original_image_name, results_arr):
    result = np.ones(image_shape, dtype=np.uint8)
    result[:,:,:] = 255
    print("Starting to merge original image")
    print(f"Result image shape is {image_shape}")

    counter = 0
    for (file_name, image) in file_to_image_map:
        match = re.search(f"{original_image_name}_(\d+)_(\d+)_.png", file_name)
        row = int(match.group(1))*patch_size
        col = int(match.group(2))*patch_size
        print(f"Row {row}, Col {col}")
        image = Image.fromarray(image)
        if(results_arr[counter]>0.8):
            image = RGBTransform().mix_with((240, 148, 62),factor=.30).applied_to(image) 
        if results_arr[counter] > 0.3 and results_arr[counter] < 0.9:
            image = RGBTransform().mix_with((175, 242, 161),factor=.30).applied_to(image) 
        
        image = np.array(image)
        result[col:col+patch_size, row:row+patch_size] = image
        counter += 1
    print("Made the result image")
    return result
