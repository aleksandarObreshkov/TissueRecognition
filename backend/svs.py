import os
import re
OPENSLIDE_PATH = f'{os.curdir}\\openslide\\openslide-win64-20230414\\bin'
os.add_dll_directory(OPENSLIDE_PATH)

import py_wsi
from PIL import Image
import numpy as np
import utils
from datetime import datetime


FILE_DIR = f'{os.curdir}\\py_wsi\\original'
DB_LOCATION = f'{os.curdir}\\py_wsi\\db'
DB_NAME = "db"
PATCH_SIZE = 50

def __apply_color(arr, severity):
    if severity=='low':
        arr[:,:,0] = 175
        arr[:,:,1] = 242
        arr[:,:,2] = 131
    if severity=='high':
        arr[:,:,0] = 240
        arr[:,:,1] = 148
        arr[:,:,2] = 62

    return arr


def __get_level_to_scan(dims_arr):
    counter = 0
    for dim in dims_arr:
        if dim[0]>4000 and dim[1]>4000:
            return counter, dim
        counter+=1


def __split_svs(filepath):
    if utils.get_file_extension(filepath) != '.svs':
        raise RuntimeError("Loaded image is not in SVS format.")

    new_filepath = utils.copy_original_to_scan_dir_for_svs(filepath, FILE_DIR)
    filename = utils.extract_last_element_from_path(new_filepath)
    turtle = py_wsi.Turtle(FILE_DIR, DB_LOCATION, DB_NAME, label_map={}, storage_type='disk')

    _level_count, _level_tiles, level_dims = turtle.retrieve_tile_dimensions(filename, patch_size=PATCH_SIZE)
    level, dims = __get_level_to_scan(level_dims)
    turtle.sample_and_store_patches(PATCH_SIZE, level, 0)
    return level, dims, utils.remove_file_extension(filename)


def __run_patch_batches_in_nn(patches_arr, cnn):
    batch_size = 32
    patches_results = []
    for index in range(0, len(patches_arr), batch_size):
         sub_arr = patches_arr[index:index+batch_size]
         results = cnn(np.array(sub_arr))
         patches_results.extend(results)
    return patches_results


def __read_patches_from_db(filename):
    print(f"Filename is: {filename}")
    files = os.listdir(DB_LOCATION)
    files = [file for file in files if filename in file] #filter out the patches not belonging to the current image
    all_images = []
    for file in files:
        image = np.array(Image.open(f"{DB_LOCATION}\\{file}"))
        all_images.append(image)
    
    return all_images, files


def __delete_patch_and_svs_files(filename):
    for file in os.listdir(f"{DB_LOCATION}"):
        os.remove(f"{DB_LOCATION}\\{file}")
    
    for file in os.listdir(FILE_DIR):
        if filename in file:
            os.remove(f"{FILE_DIR}\\{file}")


def split_svs(filepath):
    print(f"Splitting patches {datetime.now()}")
    _level, dims, test_image_name = __split_svs(filepath)
    print(f"Done splitting patches {datetime.now()}")
    return dims, test_image_name


def read_svs_patches(image_name):
    print(f"Fetching patches {datetime.now()}")
    patches_arr, filenames = __read_patches_from_db(image_name)
    print(f"Fetched patches {datetime.now()}")
    return patches_arr, filenames


def run_patches_in_nn(patches_arr, nn):
    print(f"Starting scanning of patches {datetime.now()}")
    results_arr = __run_patch_batches_in_nn(patches_arr, nn)
    print(f"Stopping scanning of patches {datetime.now()}")
    return results_arr


def merge_scan_arr(dims, filenames, scan_results, test_image_name):
    print(f"Started forming result image {datetime.now()}")
    results_numpy = np.zeros((dims[0], dims[1], 3), dtype=np.uint8)
    for file, result in zip(filenames, scan_results):
        match = re.search(f"{test_image_name}_(\d+)_(\d+)_", file)
        row = int(match.group(1))*PATCH_SIZE
        col = int(match.group(2))*PATCH_SIZE
        if result >= 0.80:
            __apply_color(results_numpy[col:col+PATCH_SIZE,row:row+PATCH_SIZE], 'high')
        if result > 0.3 and result < 0.80:
            __apply_color(results_numpy[col:col+PATCH_SIZE,row:row+PATCH_SIZE], 'low')
    print(f"Formed result image {datetime.now()}")

    print(f"Deleting patches and svs {datetime.now()}")
    __delete_patch_and_svs_files(test_image_name)
    print(f"Deleted patches and svs {datetime.now()}")

    return results_numpy


def cleanup(filename):
    for file in  os.listdir(FILE_DIR):
        if filename in file:
            os.remove(f'{FILE_DIR}{file}')
    
    print(f"Deleted original. Proof: {os.listdir(FILE_DIR)}")
    
    for patch in os.listdir(DB_LOCATION):
        if filename in patch:
            os.remove(f'{DB_LOCATION}{patch}')
    print("Deleted patches")