import os
import shutil
import datetime
from PIL import Image
import signal

ROOT_DIR = "C:\\Users\\aleks\\Projects\\IDC_Finder\\past_scans"


def make_new_dir_from_path(image_path):
    image_name = extract_last_element_from_path(image_path)
    image_name = remove_file_extension(image_name)
    curr_scan_dir = make_new_dir_from_name(image_name)
    return (copy_original_to_scan_dir(image_path, curr_scan_dir), curr_scan_dir)


def copy_original_to_scan_dir_for_svs(image_path, scan_dir):
    copy_original_in_scan_dir(image_path, scan_dir)
    original_image_path = f"{scan_dir}\\{extract_last_element_from_path(image_path)}"
    return original_image_path


def copy_original_to_scan_dir(image_path, scan_dir):
    image_timespamp = extract_last_element_from_path(scan_dir)
    file_extension = get_file_extension(image_path)
    original_image_path = f"{scan_dir}\\{image_timespamp}{file_extension}"
    copy_original_in_scan_dir(image_path, original_image_path)
    return original_image_path


def copy_original_in_scan_dir(path1, path2):
    shutil.copy(path1, path2)


def make_new_dir_from_name(image_name):
    curtime = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    new_dir = f'{ROOT_DIR}\\{curtime}-{image_name}'
    os.mkdir(new_dir)
    return new_dir


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


def get_file_extension(file_name: str):
    index_of_dot = file_name.index('.')
    extension = file_name[index_of_dot:]
    return extension


def close_app():
    process_id = os.getpid()
    os.kill(process_id, signal.SIGTERM) #find a better way to do this


def delete(file_path):
    os.remove(file_path)


def delete_force(dir_path):
    shutil.rmtree(dir_path)