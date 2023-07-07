import utils
import image_processing
from threading import Thread
import server_utils


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
    tumor_mask.save(filter_path) #TODO: Remove this line

    print("Debugging: Applying tumor mask")
    filtered = image_processing.apply_tumor_mask(original_image_path, tumor_mask)
    filtered.save(filter_path) #TODO: Remove this line

    print("Debugging: Outlining tumors in main image")
    image_processing.outline_tumors(filter_path, original_image_path, result_path)
    utils.change_file_extension(original_image_path)
    server_utils.inform_scan_ready(utils.extract_last_element_from_path(curr_scan_dir))
