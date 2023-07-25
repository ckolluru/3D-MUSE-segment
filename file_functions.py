import glob
import matplotlib.pyplot as plt
import numpy as np

def read_images(zarr_file):

    # find all png images with the filename structure 'Image_#####.png'
    filelist = glob.glob(zarr_file + '\\Image_*.png') 

    # Read the images and store them in a single array
    img_stack = []
    for file_name in filelist:
        image = plt.imread(file_name)
        img_stack.append(image)

    # Convert the list to a Numpy Array
    img_stack = np.array(img_stack)

    return img_stack