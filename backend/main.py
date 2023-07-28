import utils
import math
import threading
import server_utils
import svs
import merger
from PIL import Image

def exception_hook(args:threading.ExceptHookArgs):
    server_utils.inform_scan_failed(args.exc_value.args)

threading.excepthook = exception_hook

def start_scan_in_thread(original_image_path, curr_scan_dir, model):
    executor_thread = threading.Thread(target=scan, args=(original_image_path, curr_scan_dir, model))
    executor_thread.daemon = True
    executor_thread.start()


def scan(original_image_path, curr_scan_dir, model):
    try:
        validated_image_path = f"{curr_scan_dir}\\merged.png"
        #filter_path = f"{curr_scan_dir}\\filtered.png"
        result_path = f'{curr_scan_dir}\\result.png'

        dims, image_name = svs.split_svs(original_image_path)
        patches, all_filenames = svs.read_svs_patches(image_name)
        results_arr = svs.run_patches_in_nn(patches, model)
        result_probability_map = svs.merge_scan_arr(dims, all_filenames,results_arr,image_name)

        name_to_image_map = zip(all_filenames, patches)
        print(f"Dimensions are {dims}")
        image_shape = (math.ceil(dims[1]/50)*50, math.ceil(dims[0]/50)*50, 3)
        patches_merged = merger.merge(name_to_image_map, 50, image_shape, image_name, results_arr)
        print("Merging result image")
        Image.fromarray(result_probability_map).save(result_path)
        print("Merging original image")

        Image.fromarray(patches_merged).save(validated_image_path)
        
        # image_processing.analyze_image(model, original_image_path, validated_image_path)
        
        # print("Debugging: Getting tumor mask")
        # tumor_mask = image_processing.get_tumor_mask(validated_image_path)
        # tumor_mask.save(filter_path) #TODO: Remove this line

        # print("Debugging: Applying tumor mask")
        # filtered = image_processing.apply_tumor_mask(original_image_path, tumor_mask)
        # filtered.save(filter_path) #TODO: Remove this line

        # print("Debugging: Outlining tumors in main image")
        # image_processing.outline_tumors(filter_path, original_image_path, result_path)
        # utils.change_file_extension(original_image_path)
        # 
        print("Merge successful")
        server_utils.inform_scan_ready(utils.extract_last_element_from_path(curr_scan_dir))
    except Exception as err:
        failed_scan_name = utils.extract_last_element_from_path(curr_scan_dir)
        raise RuntimeError(failed_scan_name, str(err))
