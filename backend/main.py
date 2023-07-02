import utils
import image_processing
from threading import Thread
import server_utils


def make_new_dir(image_path):
    image_name = utils.extract_last_element_from_path(image_path)
    image_name = utils.remove_file_extension(image_name)
    curr_scan_dir = utils.make_new_dir(image_name)
    return (copy_original_to_scan_dir(image_path, curr_scan_dir), curr_scan_dir)


def start_scan(image_path, model):
    print(image_path)
    original_image_path, curr_scan_dir = make_new_dir(image_path)
    print(original_image_path)
    curr_scan_path = utils.extract_last_element_from_path(curr_scan_dir)
    start_scan_in_thread(original_image_path, curr_scan_dir, model)
    return curr_scan_path


def start_scan_in_thread(original_image_path, curr_scan_dir, model):
    executor_thread = Thread(target=scan, args=(original_image_path, curr_scan_dir, model))
    executor_thread.daemon = True
    executor_thread.start()


def scan(original_image_path, curr_scan_dir, model):
    validated_image_path = f"{curr_scan_dir}\\merged.png"
    filter_path = f"{curr_scan_dir}\\filtered.png"
    result_path = f'{curr_scan_dir}\\result.png'

    image_processing.analyze_image(model, original_image_path, validated_image_path)
    
    print("Debugging: Getting tumor mask")
    tumor_mask = image_processing.get_tumor_mask(validated_image_path)
    tumor_mask.save(filter_path)

    print("Debugging: Applying tumor mask")
    filtered = image_processing.apply_tumor_mask(original_image_path, tumor_mask)
    filtered.save(filter_path)

    print("Debugging: Outlining tumors in main image")
    image_processing.outline_tumors(filter_path, original_image_path, result_path)
    utils.change_file_extension(original_image_path)
    server_utils.inform_scan_ready(utils.extract_last_element_from_path(curr_scan_dir))


def copy_original_to_scan_dir(image_path, scan_dir):
    utils.copy_original_in_scan_dir(image_path, scan_dir)
    original_image_path = f"{scan_dir}\\{utils.extract_last_element_from_path(image_path)}"
    return original_image_path
