import os
import shutil


dirs = ["ADI", "BACK", "DEB", "LYM", "MUC", "MUS", "NORM", "STR", "TUM"]
#The following directories should be updated to the directories where the nii and tiff images are stored
all_pictures_dir = "C:\\Users\\aleks\\Projects\\python\Tissues\\NCT-CRC-HE-100K-NONORM-1"


def reorder():
    for dir in dirs:
        counter = 0
        images = os.listdir(f'{all_pictures_dir}/{dir}')
        size = len(images)
        for image in images:
            counter+=1
            orig_dir = f'{all_pictures_dir}/{dir}/{image}'
            if(counter <= (size/100)*60):
                new_dir = f'TumorSamples/train/{dir}/{image}'
                shutil.copy(orig_dir, new_dir)
            if(counter > (size/100)*60 and counter <= (size/100)*80):
                new_dir = f'TumorSamples/validate/{dir}/{image}'
                shutil.copy(orig_dir, new_dir)
            if(counter > (size/100)*80):
                new_dir = f'TumorSamples/test/{dir}/{image}'
                shutil.copy(orig_dir, new_dir)
                