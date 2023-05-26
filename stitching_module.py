import numpy as np
import itk
from pathlib import Path
from skimage import data as skidata
import h5py
import os

'''
After working on this problem a bit more, I discovered the issue I was experiencing was related to the order of the dimensions
in my image data. It seems that ITK Montage is expecting data dimensions to be ordered […, Z, Y, X]. 
When I rework code to preserve that format, Im able to register the images and generate a highly-accurate montage. 
Im happy to post an updated code example if interested. Otherwise, I believe this issue is resolved. Thanks
'''
# read in and reshape data
original = skidata.cells3d()[:, 1, :, :] # data.shape -> (60, 256, 256)
#original = np.moveaxis(original, 0, 2) # data.shape -> (256, 256, 60)
original = original/original.max() # normalize to 1.
dshape, tile_dshape = original.shape, (135, 135, 60)

# split into sub-arrays, Dim order is now [Y, X, Z]
tile_list = [
    original[:tile_dshape[0], :tile_dshape[1], :], # 0, 0
    original[:tile_dshape[0]:, -tile_dshape[1]:, :], # 0, 1
    original[-tile_dshape[0]:, :tile_dshape[1], :], # 1, 0
    original[-tile_dshape[0]:, -tile_dshape[1]:, :]  # 1, 1
]

tile_positions = [ # X, Y, Z
    (0., 0., 0.),
    (float(dshape[0] - tile_dshape[0]), 0., 0.),
    (0., float(dshape[1] - tile_dshape[1]), 0.),
    (float(dshape[0] - tile_dshape[0]), float(dshape[1] - tile_dshape[1]), 0.),
    ]

# create tile config text string
tile_config_str = f"""
# defined in index-space, not lab-space
dim = {len(tile_list[0].shape)}

img_0.h5;;{tile_positions[0]}
img_1.h5;;{tile_positions[1]} 
img_2.h5;;{tile_positions[2]}
img_3.h5;;{tile_positions[3]}
"""

# create output dir and save tile config
parent_dir = Path("/tmp/")
tile_config_path = parent_dir / 'TileConfigurationTest.txt'
with open(tile_config_path, 'w') as fp:
    fp.write(tile_config_str)

# define number of dims to stitch on
dimension = len(tile_list[0].shape)
stage_tiles = itk.TileConfiguration[dimension]()
stage_tiles.Parse(str(tile_config_path))

# get ITK image objects and origins
grayscale_images = []
for t in range(stage_tiles.LinearSize()):
    origin = stage_tiles.GetTile(t).GetPosition()
    image = itk.image_from_array(tile_list[t])    
    image.SetOrigin(origin)
    grayscale_images.append(image)

# only float is wrapped as coordinate representation type in TileMontage
montage = itk.TileMontage[type(grayscale_images[0]), itk.F].New()
montage.SetMontageSize(stage_tiles.GetAxisSizes())
for t in range(stage_tiles.LinearSize()):
    montage.SetInputTile(t, grayscale_images[t])

print("Computing tile registration transforms")
montage.Update()

print("Writing tile transforms")
actual_tiles = stage_tiles # we will update it later
reg_positions = []
for t in range(stage_tiles.LinearSize()):
    index = stage_tiles.LinearIndexToNDIndex(t)
    regTr = montage.GetOutputTransform(index)
    tile = stage_tiles.GetTile(t)
    itk.transformwrite([regTr], str(parent_dir / (tile.GetFileName() + ".tfm")))

    # calculate updated positions - transform physical into index shift
    pos = tile.GetPosition()
    for d in range(dimension):
        pos[d] -= regTr.GetOffset()[d]
    reg_positions.append(tuple(pos))
    tile.SetPosition(pos)
    actual_tiles.SetTile(t, tile)


out_file = parent_dir / 'mosaic_test.h5'
print("Producing the mosaic")
resampleF = itk.TileMergeImageFilter[type(grayscale_images[0])].New()
resampleF.SetMontageSize(stage_tiles.GetAxisSizes())
for t in range(stage_tiles.LinearSize()):
    resampleF.SetInputTile(t, grayscale_images[t])
    index = stage_tiles.LinearIndexToNDIndex(t)
    resampleF.SetTileTransform(index, montage.GetOutputTransform(index))
resampleF.Update()
if out_file.is_file():
    os.remove(out_file)
itk.imwrite(resampleF.GetOutput(), str(out_file))
print("Resampling complete")    


# read mosaic
f = h5py.File(out_file, 'r')
mosaic_test = np.array(f['ITKImage']['0']['VoxelData'])
    
print(f'True Positions:\n{tile_positions}\n')
# [(0.0, 0.0, 0.0), (121.0, 0.0, 0.0), (0.0, 121.0, 0.0), (121.0, 121.0, 0.0)]

print(f'Registered Positions:\n{reg_positions}\n') 
# ~[(0, 0, 0), (191, -2, -4), (4, 116, 3), (195, 115, 16)] ?!?!?

print(f'Mosaic shape: {mosaic_test.shape}') # (155, 253, 255) ?!?!?