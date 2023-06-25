import os
import alexnet
import utils
from tensorflow import keras
import image_processing


def scan(image_path):
    curr_scan_dir = utils.make_new_dir()
    utils.copy_original_in_scan_dir(image_path, curr_scan_dir)
    original_image_path = f"{curr_scan_dir}\\{utils.extract_last_element_from_path(image_path)}"
    
    alexnet_model: keras.models.Model

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = alexnet.train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)

    validated_image_path = f"{curr_scan_dir}\\merged.png"
    filter_path = f"{curr_scan_dir}\\filtered.png"
    result_path = f'{curr_scan_dir}\\result.png'

    image_processing.analyze_image(alexnet_model, original_image_path, validated_image_path)
    
    tumor_mask = image_processing.get_tumor_mask(validated_image_path)
    tumor_mask.save(filter_path)

    filtered = image_processing.apply_tumor_mask(original_image_path, tumor_mask)
    filtered.save(filter_path)

    image_processing.outline_tumors(filter_path, original_image_path, result_path)
    utils.change_file_extension(original_image_path)
    return curr_scan_dir