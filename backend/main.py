import utils
import image_processing
import requests


def make_new_dir(image_path):
    image_name = utils.extract_last_element_from_path(image_path)
    image_name = utils.remove_file_extension(image_name)
    curr_scan_dir = utils.make_new_dir(image_name)
    return (copy_original_to_scan_dir(image_path, curr_scan_dir), curr_scan_dir)


def scan(original_image_path, curr_scan_dir, model):
    validated_image_path = f"{curr_scan_dir}\\merged.png"
    filter_path = f"{curr_scan_dir}\\filtered.png"
    result_path = f'{curr_scan_dir}\\result.png'

    image_processing.analyze_image(model, original_image_path, validated_image_path)
    
    print("Debugging: getting tumor mask")
    tumor_mask = image_processing.get_tumor_mask(validated_image_path)
    tumor_mask.save(filter_path)

    print("Debugging: Applying tumor mask")
    filtered = image_processing.apply_tumor_mask(original_image_path, tumor_mask)
    filtered.save(filter_path)

    print("Debugging: Outlining tumors in main image")
    image_processing.outline_tumors(filter_path, original_image_path, result_path)
    utils.change_file_extension(original_image_path)
    requests.post('http://127.0.0.1:5001/update')


def copy_original_to_scan_dir(image_path, scan_dir):
    utils.copy_original_in_scan_dir(image_path, scan_dir)
    original_image_path = f"{scan_dir}\\{utils.extract_last_element_from_path(image_path)}"
    return original_image_path
