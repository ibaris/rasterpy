# Here is an example of some basic stack features that rasterpy provides. Four bands of angle information are read from
# an image. Then we stack these bands together in an new array.

# At first import rasterpy.
import rasterpy as rpy
import numpy as np

# After that we define a path where our test tif file is located.
path = "C:\Users\ibari\Dropbox\GitHub\\rasterpy\\tests\data"

# Then we open the grid and read it to an multidimensional array:
angle = rpy.Raster('RGB.BRF.Angle.tif', path)
angle.to_array()

# Now we can store the angle information in a 2D array:
angle.dstack(unfold=True)

# With `angle.stack` we can access to the stacked arrays:
print(angle.stack)

# The advantage of this stack is we can access to the angle information for each pixel wit `angle.stack[pixel]`:
print(angle.stack[0])

# As one can see the sensing geometry of the first pixel is:
print("The inclination zenith angle is: {0} [DEG]".format(angle.stack[0][0]))
print("The viewing zenith angle is: {0} [DEG]".format(angle.stack[0][1]))
print("The relative azimuth angle is: {0} [DEG]".format(angle.stack[0][2]))