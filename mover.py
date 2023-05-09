import os
import shutil


dirs = ["ADI", "BACK", "DEB", "LYM", "MUC", "MUS", "NORM", "STR", "TUM"]
#The following directories should be updated to the directories where the nii and tiff images are stored
tiff_dir = f"f{os.curdir}/Tumor samples/tiff"
nii_dir = f"{os.curdir}/Tumor samples/nii"


def reorder():
    for dir in dirs:
        counter = 0
        images = os.listdir(f'{os.curdir}/{nii_dir}/{dir}')
        size = len(images)
        for image in images:
            counter+=1
            orig_dir = f'{nii_dir}/{dir}/{image}'
            if(counter <= (size/100)*60):
                new_dir = f'records/train/{dir}/{image}'
                shutil.copy(orig_dir, new_dir)
            if(counter > (size/100)*60 and counter <= (size/100)*80):
                new_dir = f'records/validate/{dir}/{image}'
                shutil.copy(orig_dir, new_dir)
            if(counter > (size/100)*80):
                new_dir = f'records/test/{dir}/{image}'
                shutil.copy(orig_dir, new_dir)
                
