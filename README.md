<h1 align="center">
  <br>
  <a href="http://elib.dlr.de/115785/"><img src="https://i.imgur.com/uspi5KE.png" alt="RadOptics" width="300"></a>
</h1>

<h3 align="center">Basic Routines to Read and Write Raster Files with Python</h3>

<p align="center">
  <a href="http://forthebadge.com">
    <img src="http://forthebadge.com/images/badges/made-with-python.svg"
         alt="Gitter">
  </a>
  <a href="http://forthebadge.com"><img src="http://forthebadge.com/images/badges/built-with-love.svg"></a>
  <a href="http://forthebadge.com">
      <img src="http://forthebadge.com/images/badges/built-with-science.svg">
  </a>
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#installation">Installation</a> •
  <a href="#example">Example</a> •
    <a href="#documentation">Doumentation</a> •
  <a href="#authors">Author</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>

<p align="center">
  <a href="https://www.travis-ci.org/ibaris/rasterpy"><img src="https://www.travis-ci.org/ibaris/rasterpy.svg?branch=master"></a>
</p>

# Description
Rasterpy contains basic routines to read and write raster files with python. With Rasterpy one can read the following raster formats:
* **'tif'**: All `.tiff` formats like GEOtiff etc.
* **'.hdr'**: All ENVI formats like `.bin` and `.hdr` formats. This is usefull if you want to read data from third-party software like Polsarpro. 

# Installation
There are currently different methods to install `rasterpy`.
### Using pip
The ` rasterpy ` package is provided on pip. You can install it with::

    pip install rasterpy
    
### Standard Python
You can also download the source code package from this repository or from pip. Unpack the file you obtained into some directory (it can be a temporary directory) and then run::

    python setup.py install
  
### Test installation success
Independent how you installed ` pyrism `, you should test that it was sucessfull by the following tests::

    python -c "from rasterpy import Raster"

If you don't get an error message, the module import was sucessfull.

# Example
Here is an example of some basic features that rasterpy provides. Three bands are read from an image and averaged to produce something like a panchromatic band. This new band is then written to a new single band TIFF.

At first import rasterpy:
```python
import rasterpy as rpy
import numpy as np
```
After that we define a path where our test tif file is located:
```python
path = "C:\Users\ibari\Dropbox\GitHub\\rasterpy\\tests\data"
```

Then we open the grid and read it to an multidimensional array:
```python
grid = rpy.Raster('RGB.byte.tif', path)
grid.to_array()
```

By default the loaded grid is flatten. The reason is as following: With a flatten 2 dimensional array the calculations based on the array are much easier:
```python
>>> print(grid.array)
[[0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]]
```

We can reshape the array to their original shapes with:
```python
>>> grid.reshape()
>>> print(grid.array)
[[[0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  ...
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]]
 [[0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  ...
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]]
 [[0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  ...
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]
  [0. 0. 0. ... 0. 0. 0.]]]
```
And we can also flatten it again with:
```python
>>> grid.flatten()
>>> print(grid.array)
[[0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]]
```

Now average each pixels of the RGB bands:
```python
pan = np.mean(grid.array, axis=0)
```

After that we can write the reshaped pan array as a tiff:
```python
grid.write(data=pan.reshape(grid.rows, grid.cols), filename='RGB_total.tif', path=path)
```

The result is as following:
<br>
<a href="https://i.imgur.com/oCfHTNj.png"><img src="https://i.imgur.com/oCfHTNj.png" alt="RGB_total.tif" width="500"></a>

# Documentation

# Built With
* Python 2.7 (But it works with Python 3.5 as well)
* Requirements: numpy, gdal

# Authors
* **Ismail Baris** - *Initial work* - (i.baris@outlook.de)

## Acknowledgments
*  <a href="https://github.com/johntruckenbrodt/pyroSAR">John Truckenbrodt and Felix Cremer </a>

---

> ResearchGate [@Ismail_Baris](https://www.researchgate.net/profile/Ismail_Baris) &nbsp;&middot;&nbsp;
> GitHub [@ibaris](https://github.com/ibaris) &nbsp;&middot;&nbsp;
> Instagram [@ism.baris](https://www.instagram.com/ism.baris/)

