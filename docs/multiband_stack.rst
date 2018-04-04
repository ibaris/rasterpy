Raster Stack
------------
Here is an example of some basic stack features that rasterpy provides. Three bands of angle information are read from an image.
The first band is the inclination(iza), the second band the viewing (vza) and the last band is the relative azimuth (raa) angle.
Then we stack these bands together in an new array.

At first import rasterpy.
.. ::
    import rasterpy as rpy
    import numpy as np

After that we define a path where our test tif file is located.
.. ::
    path = "C:\Users\ibari\Dropbox\GitHub\\rasterpy\\tests\data"

Then we open the grid and read it to an multidimensional array
.. ::
    angle = rpy.Raster('RGB.BRF.Angle.tif')
    angle.to_array()

Now we can store the angle information in a 2D array
.. ::
    angle.dstack(unfold=True)

With `angle.stack` we can access to the stacked arrays
.. ::
    print(angle.stack)
        # IZA       # VZA       # RAA
    [[  8.7763834   59.99580002 113.65518188]
     [  8.7763834   59.99580002 113.65518188]
     [  8.7763834   59.99580002 113.65518188]
     ...
     [  9.26036167  59.9394989  114.21447754]
     [  9.26036167  59.9394989  114.21447754]
     [  9.26036167  59.9394989  114.21447754]]

The advantage of this stack is we can access to the angle information for each pixel wit `angle.stack[pixel]`:
.. code::
    print(angle.stack[0])
    [  8.7763834   59.99580002 113.65518188]

As one can see the sensing geometry of the first pixel is
.. code::
    print("The inclination zenith angle is: {0} [DEG]".format(angle.stack[0][0]))
    print("The viewing zenith angle is: {0} [DEG]".format(angle.stack[0][1]))
    print("The relative azimuth angle is: {0} [DEG]".format(angle.stack[0][2]))

    The inclination zenith angle is: 8.77638339996 [DEG]
    The viewing zenith angle is: 59.9958000183 [DEG]
    The relative azimuth angle is: 113.655181885 [DEG]