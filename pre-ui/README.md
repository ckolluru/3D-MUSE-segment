# SBFpreprocess
Software to preprocess serial block-face microscopy images for segmentation, visualization and tractography.

The software provides the following functions:
1. Demosaicing
2. Mean intensity correction across the Z stack
3. Window/level adjustment, gamma correction
4. 2D image stitching between tiles 
5. Automatically find slices containing sectioning artifact/debris and remove them
6. Slice to slice registration (translation only)
7. Padding images so that the stack is of the same size

Steps 1-4 contain user defined parameters, and are thus run on intermediate slices within the stack.
User can modify parameters as desired.
When suitable, all images in the stack can be processed. 

Features include 
1. Parallel processing across nodes using Dask
2. Image datasets are written in Zarr format with multiscale options.
3. GUI allows user to select best parameters prior to processing.

# Installation
1. Clone this repository
```git clone https://github.com/ckolluru/SBFpreprocess.git```

2. Navigate to the repository folder

3. Create a conda environment
```conda create --name preprocess --file requirements.txt```

4. Activate the environment
```conda activate preprocess```
