# Here is an example of some basic features that rasterpy provides. Three bands are read from an image and averaged to
# produce something like a panchromatic band. This new band is then written to a new single band TIFF.

# At first import rasterpy.
import rasterpy as rpy
import numpy as np

# After that we define a path where our test tif file is located.
path = "C:\Users\ibari\Dropbox\GitHub\\rasterpy\\tests\data"

# Then we open the grid and read it to an multidimensional array:
grid = rpy.Raster('RGB.byte.tif', path)
print(grid.to_array())

# By default the loaded grid is flatten. The reason is as following: With a flatten 2 dimensional array the calculations
# based on the array are much easier:
print(grid.array)

# We can reshape the array to their original shapes with:
grid.reshape()
print(grid.array)

# And we can also flatten it again with:
grid.flatten()
print(grid.array)

# Now average each pixels of the RGB bands:
pan = np.mean(grid.array, axis=0)

# After that we can write the reshaped pan array as a tiff:
grid.write(data=pan.reshape(grid.rows, grid.cols), filename='RGB_total.tif', path=path)
