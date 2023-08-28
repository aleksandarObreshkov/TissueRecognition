import neural_network
import numpy as np
from PIL import Image
import os, re
from rbg_transform import RGBTransform
TEMP_DIR = "C:\\Users\\aleks\\Desktop\\9346"
PATTERN = '\d+_idx5_x(\d+)_y(\d+)_class(\d)'


def get_original_image_size():
    max_x = 0
    max_y = 0
    for image in os.listdir(TEMP_DIR):
        match = re.match(PATTERN, image)
        x = int(match[1])
        y = int(match[2])
        max_x = max([x, max_x])
        max_y = max([y, max_y])
    return (max_x, max_y)

def make_result_image(patches_arr):
    max_x, max_y = get_original_image_size()
    result = np.zeros((max_y+50, max_x+50, 3), dtype=np.uint8)

    for image_name, patch in zip(os.listdir(TEMP_DIR), patches_arr):
        match = re.match(PATTERN, image_name)
        x = int(match[1])
        y = int(match[2])
        result[y:y+50, x:x+50] = np.array(patch)
    
    Image.fromarray(result).save("C:\\Users\\aleks\\Desktop\\result1.png")



cnn = neural_network.get_model('idc_smaller')
images_arr = []

for image in os.listdir(TEMP_DIR):
    images_arr.append(np.array(Image.open(f'{TEMP_DIR}\\{image}')))

batch_size = 32
patches_results = []
for index in range(0, len(images_arr), batch_size):
        sub_arr = images_arr[index:index+batch_size]
        results = cnn(np.array(sub_arr))
        patches_results.extend(results)
colored_arr = []
for patch, result in zip(images_arr, patches_results, strict=True):
    if(result > 0.80):
        patch = RGBTransform().mix_with((240, 148, 62),factor=.30).applied_to(Image.fromarray(patch))
    colored_arr.append(patch)
make_result_image(colored_arr)



