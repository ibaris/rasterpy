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
  <a href="https://www.travis-ci.org/ibaris/pyrism"><img src="https://www.travis-ci.org/ibaris/pyrism.svg?branch=master"></a>
  <a href='https://coveralls.io/github/ibaris/pyrism?branch=master'><img src='https://coveralls.io/repos/github/ibaris/pyrism/badge.svg?branch=master' alt='Coverage Status' /></a>
  <a href='http://pyrism.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/pyrism/badge/?version=latest' alt='Documentation Status' /></a>
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

# Documentation
You can find the full documentation <a href="http://pyrism.readthedocs.io/en/latest/index.html">here</a>.

# Built With
* Python 2.7 (But it works with Python 3.5 as well)
* Requirements: numpy, scipy

# Authors
* **Ismail Baris** - *Initial work* - (i.baris@outlook.de)

## Acknowledgments
*  <a href="https://github.com/johntruckenbrodt/pyroSAR">John Truckenbrodt and Felix Cremer </a>

---

> ResearchGate [@Ismail_Baris](https://www.researchgate.net/profile/Ismail_Baris) &nbsp;&middot;&nbsp;
> GitHub [@ibaris](https://github.com/ibaris) &nbsp;&middot;&nbsp;
> Instagram [@ism.baris](https://www.instagram.com/ism.baris/)

