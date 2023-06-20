import os
import shutil
import datetime

#ROOT_DIR = os.getenv('ROOTDIR')
ROOT_DIR = "C:\\Users\\aleks\\Projects\\IDC_Finder\\past_scans"

def make_new_dir():
    curtime = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    new_dir = f'{ROOT_DIR}\\{curtime}'
    os.mkdir(new_dir)
    return new_dir

def copy_original_in_scan_dir(original_img_path, scan_dir):
    shutil.copy(original_img_path, scan_dir)


