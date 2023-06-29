import numpy as np
import tifffile as tiffio
import glob
import os
from tqdm import tqdm
from PIL import Image
import shutil
import math


def correct(subsetVolume, correctIntensityVariationFlag, gamma):
    
    '''---------------------------------------
    Summary: Bleach and gamma correction

    This script takes a folder name that was created from the previous scripts.
    Example: sample_name\\Red channel
    Verify that the first image in the stack looks reasonable if doing bleach correction or gamma correction.
    If not, delete those slices.
    ------------------------------------------'''

    '''---------------------------------------
    Inputs
    ------------------------------------------'''
    sample_name = 'mid-cervical-sr001-r'
    sub_folder  = 'r0_g1_b0'

    sample_folder = r'C:\\Users\\cxk340\\Desktop\\' + sample_name + '\\'
    save_folder = r'Individual image slices\\'

    # If you want to do bleach correction
    bleach_correction = True

    # If you want to do gamma correction
    gamma_correction = True
    gamma_value = 0.54

    gamma_bleach_correction_folder = r'Gamma bleach corrected slices\\'

    '''---------------------------------------
    Inputs
    ------------------------------------------'''


    '''---------------------------------------
    Algorithm
    ------------------------------------------'''
    stacks_folder = sample_folder + sub_folder + '\\'

    # Remove save folder if it exists
    if os.path.exists(stacks_folder + gamma_bleach_correction_folder):
        shutil.rmtree(stacks_folder + gamma_bleach_correction_folder)

    os.makedirs(stacks_folder + gamma_bleach_correction_folder)

    # Bytes per image
    bytes_per_image = 12009644

    # Example image size
    example_width = 4000
    example_height = 3000

    # List of image files
    image_filelist = glob.glob(stacks_folder + save_folder + '*.png')

    for k in tqdm(np.arange(len(image_filelist))):

        image = Image.open(image_filelist[k])
        image = np.array(image)

        # Bleach correction, simple ratio method, background assumed to be 0.
        if bleach_correction:
            if k == 0:
                mean_first_slice = np.mean(image)
            else:
                mean_current_slice = np.mean(image)
                image = mean_first_slice * image / (mean_current_slice)
                image = np.floor(np.clip(image, 0, 255)) 
                image = image.astype(np.uint8)

        if gamma_correction:
            # do gamma correction
            image = (np.power(image/255, gamma_value)*255).clip(0,255).astype(np.uint8)

        if k != 0:
            pil_image = Image.fromarray(image)
            pil_image.save(stacks_folder + gamma_bleach_correction_folder + 'Image_' + str(k).zfill(5) + '.png')

    '''---------------------------------------
    Algorithm
    ------------------------------------------'''
