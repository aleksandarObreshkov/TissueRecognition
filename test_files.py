import os
from PIL import Image
import SimpleITK as sitk
import numpy as np


folder_path = 'E:/Bioinformatics/Tumor samples/samples_tiff'
extensions = []


def test_files_are_valid():
    for fldr in os.listdir(folder_path):
        sub_folder_path = f'{folder_path}/{fldr}'
        for filee in os.listdir(sub_folder_path):
            file_path =f'{sub_folder_path}/{filee}'
            print('** Path: {}  **'.format(file_path), end="\r", flush=True)
            im = Image.open(file_path)
            rgb_im = im.convert('RGB')
            if filee.split('.')[1] not in extensions:
                extensions.append(filee.split('.')[1])


def test_open_nii_file():
    for fldr in os.listdir(folder_path):
        sub_folder_path = f'{folder_path}/{fldr}'
        for filee in os.listdir(sub_folder_path):
            file_path =f'{sub_folder_path}/{filee}'
            print('** Path: {}  **'.format(file_path), end="\r", flush=True)
            im = sitk.ReadImage(file_path)
            array = sitk.GetArrayFromImage(im)
            print(array)

