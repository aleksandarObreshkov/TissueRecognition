from imio import load, save
import os

dirs = ["ADI", "BACK", "DEB", "LYM", "MUC", "MUS", "NORM", "STR", "TUM"]
#The following directories should be updated to the directories where the nii and tiff images are stored
tiff_dir = f"f{os.curdir}/Tumor samples/tiff"
nii_dir = f"{os.curdir}/Tumor samples/nii"

def convert_all_images():
    for dir in dirs:
        images = os.listdir(f'{tiff_dir}/{dir}')
        for image in images:
            orig_dir = f'{tiff_dir}/{dir}/{image}'
            tiff_image = load.load_any(orig_dir)
            image.replace(".tif", "")
            save.to_nii(tiff_image, f'{nii_dir}/{dir}/{image}.nii')
