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
There are currently one method to install `rasterpy`.
    
### Standard Python
You can also download the source code package from this repository or from pip. Unpack the file you obtained into some directory (it can be a temporary directory) and then run::

    python setup.py install
  
### Test installation success
Independent how you installed ` pyrism `, you should test that it was sucessfull by the following tests::

    python -c "from rasterpy import Raster"

If you don't get an error message, the module import was sucessfull.

# Example
## Raster Calculation
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

## Raster Conversion
Three bands are read from an image. Then we do some raster conversion on it. This new bands are then written to a new multi band TIFF.

At first import rasterpy.
```python
import rasterpy as rpy
import numpy as np
```

After that we define a path where our test tif file is located.
```python
path = "C:\Users\ibari\Dropbox\GitHub\\rasterpy\\tests\data"
```

Then we open the grid and read it to an multidimensional array:
```python
grid = rpy.Raster('RGB.BRF.tif', path)
```

The quantification factor is a factor which scales reflectance value between 0 and 1. For sentinel 2 the factor is 10000
```python
grid.to_array(flatten=False, quantification_factor=10000)
```

By default the loaded grid is flatten. The reason is as following: With a flatten 2 dimensional array the calculations based on the array are much easier. But in our case this is not necessary:
```python
>>> print(grid.array)
[[[0.1049 0.0979 0.1047 ... 0.0469 0.0551 0.0553]
  [0.1008 0.0974 0.0984 ... 0.0449 0.0497 0.0574]
  [0.1039 0.0957 0.1002 ... 0.0477 0.0546 0.0653]
  ...
  [0.1226 0.1151 0.1363 ... 0.0641 0.0599 0.0643]
  [0.1136 0.1299 0.144  ... 0.0654 0.0625 0.0651]
  [0.1069 0.1034 0.1356 ... 0.0616 0.0546 0.0629]]
 [[0.1025 0.0968 0.1027 ... 0.0435 0.0567 0.0585]
  [0.1008 0.0943 0.0996 ... 0.0466 0.0531 0.0625]
  [0.0969 0.0929 0.0987 ... 0.0523 0.0604 0.0692]
  ...
  [0.1223 0.112  0.1367 ... 0.0683 0.0587 0.0621]
  [0.112  0.1282 0.1409 ... 0.0658 0.0591 0.0635]
  [0.106  0.1018 0.1394 ... 0.0616 0.0551 0.0588]]
 [[0.1146 0.1088 0.114  ... 0.0484 0.0644 0.0703]
  [0.1112 0.1076 0.1148 ... 0.048  0.0599 0.0773]
  [0.1125 0.1064 0.1119 ... 0.0564 0.0747 0.0886]
  ...
  [0.1381 0.1259 0.1473 ... 0.0873 0.0746 0.0746]
  [0.1268 0.1404 0.1624 ... 0.0782 0.0702 0.0758]
  [0.1207 0.1194 0.1543 ... 0.0752 0.0617 0.0678]]]
```

Now we convert the whole file from a Bidirectional Reflectance Factor (BRF) into a Bidirectional Reflectance Distribution Function (BRDF):
```python
grid.convert(system='BRF', to='BRDF', output_unit='dB')
```

```python
>>> print(grid.array)
[[[-14.763744 -15.063672 -14.772033 ... -18.259771 -17.559982 -17.544247]
  [-14.936894 -15.085909 -15.041548 ... -18.449036 -18.007935 -17.38238 ]
  [-14.805344 -15.16238  -14.962821 ... -18.186316 -17.599571 -16.822367]
  ...
  [-14.086595 -14.360746 -13.626541 ... -16.90292  -17.197231 -16.889389]
  [-14.417715 -13.835407 -13.387875 ... -16.815722 -17.0127   -16.83569 ]
  [-14.681722 -14.826293 -13.648902 ... -17.075691 -17.599571 -16.984993]]
 [[-14.86426  -15.112745 -14.855795 ... -18.586605 -17.435669 -17.29994 ]
  [-14.936894 -15.226382 -14.988905 ... -18.28764  -17.720554 -17.0127  ]
  [-15.108261 -15.291342 -15.028326 ... -17.786482 -17.161129 -16.570438]
  ...
  [-14.097234 -14.479319 -13.613813 ... -16.62729  -17.285118 -17.040583]
  [-14.479319 -13.892618 -13.482389 ... -16.78924  -17.255625 -16.943762]
  [-14.718439 -14.89402  -13.528872 ... -17.075691 -17.559982 -17.277725]]
 [[-14.379653 -14.605209 -14.402451 ... -18.123045 -16.88264  -16.501945]
  [-14.510451 -14.653377 -14.372081 ... -18.159086 -17.197231 -16.089705]
  [-14.459973 -14.702083 -14.483198 ... -17.458708 -16.238293 -15.497161]
  ...
  [-13.569563 -13.971242 -13.289471 ... -15.561357 -16.24411  -16.24411 ]
  [-13.940307 -13.497828 -12.865639 ... -16.03943  -16.508127 -16.174807]
  [-14.154426 -14.201455 -13.08784  ... -16.20932  -17.068647 -16.6592  ]]]

```

After that we can write the converted data as a multi band tiff:
```python
grid.write(data=grid.array, filename='RGB.BRDF.tif', path=path)
```

We can also convert the arrays from a BRF or BRDF into Backscatter coefficients (BSC). For this we need the inclination (iza) and viewing (vza) angles:
```python
angle = rpy.Raster('RGB.BRF.Angle.tif')
angle.to_array(flatten=False)
```

Note, that the arrays were converted from a BRF into a BRDF (dB) in the previous step:
```python
grid.convert(system='BRDF', to='BSC', system_unit='dB', output_unit='dB', iza=angle.array[0], vza=angle.array[2])
```

```python
>>> print(grid.array)
[[[-4.96271712 -5.26264553 -4.97100609 ... -7.62126904 -6.92148086
   -6.9057452 ]
  [-5.13586758 -5.28488271 -5.24052164 ... -7.81053428 -7.36943237
   -6.74387795]
  [-5.00431669 -5.36135311 -5.16179448 ... -7.5478137  -6.96106918
   -6.18386485]
  ...
  [-3.90826298 -4.18241472 -3.44820966 ... -6.10610002 -6.40041111
   -6.09256871]
  [-4.23938353 -3.65707628 -3.20954311 ... -6.0189023  -6.21587891
   -6.03886975]
  [-4.50339076 -4.64796155 -3.47057097 ... -6.27887148 -6.80275109
   -6.18817325]]
 [[-5.06323355 -5.31171929 -5.05476833 ... -7.9481029  -6.79716676
   -6.66143884]
  [-5.13586758 -5.42535533 -5.18787861 ... -7.64913781 -7.08205228
   -6.374197  ]
  [-5.3072346  -5.49031489 -5.22729991 ... -7.14797961 -6.52262663
   -5.93193652]
  ...
  [-3.91890241 -4.3009875  -3.43548169 ... -5.83047042 -6.48829808
   -6.24376328]
  [-4.3009875  -3.7142869  -3.30405791 ... -5.99241989 -6.45880451
   -6.14694236]
  [-4.54010816 -4.71568912 -3.3505403  ... -6.27887148 -6.76316277
   -6.48090502]]
 [[-4.57862624 -4.80418309 -4.60142373 ... -7.4845433  -6.24413949
   -5.86344365]
  [-4.7094249  -4.8523499  -4.57105403 ... -7.52058505 -6.5587292
   -5.45120237]
  [-4.65894679 -4.90105644 -4.68217143 ... -6.82020658 -5.59979082
   -4.85865945]
  ...
  [-3.39123113 -3.79291025 -3.1111394  ... -4.76453681 -5.44729009
   -5.44729009]
  [-3.76197545 -3.31949574 -2.68730743 ... -5.24261142 -5.71130764
   -5.37798651]
  [-3.97609467 -4.02312353 -2.90950882 ... -5.41249989 -6.27182743
   -5.86238026]]]
```

After the conversion we can wrtie the array to a raster file:
```python
grid.write(data=grid.array, filename='RGB.BSC.tif', path=path)
```

The result is:
<br>
<a href="https://i.imgur.com/jAOn2dp.png"><img src="https://i.imgur.com/jAOn2dp.png" width="500"></a>

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

