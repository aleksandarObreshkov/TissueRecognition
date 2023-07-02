import os
import shutil
import datetime
from PIL import Image
import signal

#ROOT_DIR = os.getenv('ROOTDIR')
ROOT_DIR = "C:\\Users\\aleks\\Projects\\IDC_Finder\\past_scans"


def make_new_dir(image_name):
    curtime = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    new_dir = f'{ROOT_DIR}\\{curtime}-{image_name}'
    os.mkdir(new_dir)
    return new_dir


def copy_original_in_scan_dir(original_img_path, scan_dir):
    shutil.copy(original_img_path, scan_dir)


def extract_last_element_from_path(path: str):
    path = path.split("\\")
    return path[len(path)-1]


def change_file_extension(image_path: str):
    png_image_path = image_path.replace('.tif', '.png')
    print(png_image_path)
    image = Image.open(image_path)
    image.save(png_image_path)
    os.remove(image_path)


def remove_file_extension(file_name: str):
    index_of_dot = file_name.index('.')
    return file_name[:index_of_dot]


def close_app():
    process_id = os.getpid()
    os.kill(process_id, signal.SIGTERM) #find a better way to do this
