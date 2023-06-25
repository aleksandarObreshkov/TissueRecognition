import utils
import image_processing


def scan(image_path, model):
    curr_scan_dir = utils.make_new_dir()
    original_image_path = copy_original_to_scan_dir(image_path, curr_scan_dir)

    validated_image_path = f"{curr_scan_dir}\\merged.png"
    filter_path = f"{curr_scan_dir}\\filtered.png"
    result_path = f'{curr_scan_dir}\\result.png'

    image_processing.analyze_image(model, original_image_path, validated_image_path)
    
    tumor_mask = image_processing.get_tumor_mask(validated_image_path)
    tumor_mask.save(filter_path)

    filtered = image_processing.apply_tumor_mask(original_image_path, tumor_mask)
    filtered.save(filter_path)

    image_processing.outline_tumors(filter_path, original_image_path, result_path)
    utils.change_file_extension(original_image_path)
    return curr_scan_dir


def copy_original_to_scan_dir(image_path, scan_dir):
    utils.copy_original_in_scan_dir(image_path, scan_dir)
    original_image_path = f"{scan_dir}\\{utils.extract_last_element_from_path(image_path)}"
    return original_image_path