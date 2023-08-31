import numpy as np
from PIL import Image
import os, shutil, re, math
from rbg_transform import RGBTransform

ROOT_DIR = "C:\\Users\\aleks\\Projects\\Tissues\\IDC 50x50 Original\\9022"
TEMP_DIR = "C:\\Users\\aleks\\Desktop\\9022"
PATTERN = '\d+_idx5_x(\d+)_y(\d+)_class(\d)'

def move_files_to_single_dir():

    os.mkdir(TEMP_DIR)

    for dir in os.listdir(ROOT_DIR):
        for image in os.listdir(f'{ROOT_DIR}\\{dir}'):
            shutil.copy(f'{ROOT_DIR}\\{dir}\\{image}', TEMP_DIR)


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


def make_result_image():
    max_x, max_y = get_original_image_size()
    result = np.zeros((max_y+50, max_x+50, 3), dtype=np.uint8)
    result_tint = np.zeros((max_y+50, max_x+50, 3), dtype=np.uint8)

    for image in os.listdir(TEMP_DIR):
        match = re.match(PATTERN, image)
        x = int(match[1])
        y = int(match[2])
        group = int(match[3])
        patch = Image.open(f'{TEMP_DIR}\\{image}')
        result[y:y+50, x:x+50] = np.array(patch)
        if group == 1:
            patch = RGBTransform().mix_with((240, 148, 62),factor=.30).applied_to(patch)
        result_tint[y:y+50, x:x+50] = np.array(patch)
    
    Image.fromarray(result).save("C:\\Users\\aleks\\Desktop\\original-9022.png")
    Image.fromarray(result_tint).save("C:\\Users\\aleks\\Desktop\\annotated-9022.png")

move_files_to_single_dir()
make_result_image()