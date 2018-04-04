# Here is an example of some basic features that rasterpy provides. Three bands are read from an image. Then we do some
# raster calculation on it. This new bands are then written to a new multi band TIFF.

# At first import rasterpy.
import rasterpy as rpy
import numpy as np

# After that we define a path where our test tif file is located.
path = "C:\Users\ibari\Dropbox\GitHub\\rasterpy\\tests\data"

# Then we open the grid and read it to an multidimensional array:
grid = rpy.Raster('RGB.BRF.tif', path)

# The quantification factor is a factor which scales reflectance value between 0 and 1. For sentinel 2 the factor is
# 10000
grid.to_array(flatten=False, quantification_factor=10000)

# By default the loaded grid is flatten. The reason is as following: With a flatten 2 dimensional array the calculations
# based on the array are much easier. But in our case this is not necessary:
print(grid.array)

# Now we convert the whole file from a Bidirectional Reflectance Factor (BRF) into a Bidirectional Reflectance
# Distribution Function (BRDF):
grid.convert(system='BRF', to='BRDF', output_unit='dB')
print(grid.array)

# After that we can write the converted data as a multi band tiff:
grid.write(data=grid.array, filename='RGB.BRDF.tif', path=path)

# We can also convert the arrays from a BRF or BRDF into Backscatter coefficients (BSC). For this we need the
# inclination and viewing angles:
angle = rpy.Raster('RGB.BRF.Angle.tif', path)
angle.to_array(band=(1, 2), flatten=False)

# Note, that the arrays were converted from a BRF into a BRDF (dB) in the previous step:
grid.convert(system='BRDF', to='BSC', system_unit='dB', output_unit='dB', iza=angle.array[0], vza=angle.array[1])
print(grid.array)

# After the conversion we can wrtie the array to a raster file:
grid.write(data=grid.array, filename='RGB.BSC.tif', path=path)
