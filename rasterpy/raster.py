from __future__ import division

import os
import sys

import numpy as np
from osgeo import (gdal, gdal_array, osr)
from osgeo.gdalconst import GA_ReadOnly

# python 3.6 comparability
if sys.version_info < (3, 0):
    srange = xrange
else:
    srange = range


class Raster:
    """
    Import a binary file of ENVI or PolSARpro or a tif to a raster object.

    Parameters
    ----------
    filename : str or tuple, optional
        Filename as a string or a tuple with filenames of the raster data.
    path : str, optional
        Path to raster data. If path is None the path will set to current
        directory with os.getwd().
    extension : str, optional
        If you want to import all files in a directory with a
        specific extension, set filename to None and define an extension like '.tiff' or '.bin'.
    check_dim : bool
        If True the imported files must have the same dimensions.

    Attributes
    ----------
    raster : osgeo.gdal.Dataset
        Contains the gdal data set for the raster files.
    cols, rows : int or tuple
        Columns and row size of the imported raster files.
    band : int or tuple
        Number of bands in each raster file.
    dim : list or tuple
        Information about the dimension. It contains [rows, cols, bands].
    dtype : str or tuple
        Gdal data types.
    projection : str or tuple
        Information about the projection of each raster file.
    xmin, ymin : int or tuple
        Origen of x and y pixel.
    xres, yres : int or tuple
        Resulution information in x and y axis.
    nodata :
        No data values.
    info : dict
        All information in a dictionary.
    """

    def __init__(self, filename=None, path=None, extension=None, check_dim=True):

        self.filename = filename

        self.__TYPEMAP = {}
        for name in dir(np):
            obj = getattr(np, name)
            if hasattr(obj, 'dtype'):

                try:
                    npn = obj(0)
                    nat = np.asscalar(npn)
                    if gdal_array.NumericTypeCodeToGDALTypeCode(npn.dtype.type):
                        self.__TYPEMAP[npn.dtype.name] = gdal_array.NumericTypeCodeToGDALTypeCode(npn.dtype.type)
                except:
                    pass

        driver = gdal.GetDriverByName('ENVI')
        driver.Register()

        if path is not None:
            os.chdir(path)
            gwd = os.getcwd()
        else:
            gwd = os.getcwd()

        if ((self.filename is None and extension is None) or
                (self.filename is not None and extension is not None)):
            raise AssertionError("You must define a filename OR a extension")

        elif self.filename is None and isinstance(extension, str) is False:
            raise AssertionError("Extension must be a str. For example '.bin'")

        else:
            if self.filename is None and extension is not None:
                for root, dirs, files in os.walk(gwd):
                    filename_list = []
                    for file in files:
                        if file.endswith(extension):
                            filename_list.append(file)

                    self.filename = tuple(filename_list)

            else:
                pass

        if not isinstance(self.filename, (str, tuple)):
            raise AttributeError("filename must be tuple or str instance.")

        if isinstance(self.filename, tuple):
            tuple_str_check = tuple([type(item) == str for item in self.filename])
            tuple_str_check = np.all(np.all(tuple_str_check) == True)

            if not tuple_str_check:
                raise AttributeError("If filename is a tuple, the tuple items must be str instance")

        if isinstance(self.filename, tuple):

            inds = tuple(map(lambda x: gdal.Open(x, GA_ReadOnly), self.filename))
            self.raster = inds

            for i in srange(len(inds)):
                if inds[i] is None:
                    raise IOError(
                        "Couldn't open file {0}. Perhaps you need an .hdr file?".format(str(self.filename[i])))
                else:
                    pass

            self.cols = tuple(map(lambda items: items.RasterXSize, inds))
            self.rows = tuple(map(lambda items: items.RasterYSize, inds))

            if check_dim:
                _col = self.cols[1:] == self.cols[:-1]
                _row = self.rows[1:] == self.rows[:-1]

                if _col is not True or _row is not True:
                    raise AssertionError("Status: Input dimensions must agree",
                                         "shapes: cols = {0}, rows = {1}".format(self.cols, self.rows))

            self.bands = tuple(map(lambda items: items.RasterCount, inds))
            self.dim = [self.rows, self.cols, self.bands]

            self.driver = tuple(map(lambda items: items.GetDriver(), inds))
            self.dtype = tuple(map(lambda items: gdal.GetDataTypeName(items.GetRasterBand(1).DataType), inds))

            self.projection = tuple(map(lambda items: items.GetProjection(), inds))
            self.srs = tuple(map(lambda items: osr.SpatialReference(wkt=items), self.projection))

            self.geotransform = tuple(map(lambda items: items.GetGeoTransform(), inds))

            self.xmin = tuple(map(lambda items: items[0], self.geotransform))
            self.ymin = tuple(map(lambda items: items[3], self.geotransform))
            self.xres = tuple(map(lambda items: items[1], self.geotransform))
            self.yres = tuple(map(lambda items: items[5], self.geotransform))

            self.nodata = tuple(map(lambda items: items.GetRasterBand(1).GetNoDataValue(), inds))

            self.nodata = list(self.nodata)
            for i in srange(len(self.nodata)):
                if self.nodata[i] is None:
                    self.nodata[i] = -99999

            self.nodata = tuple(self.nodata)

            self.info = {'bands': self.bands,
                         'dim': self.bands,
                         'dtype': self.dtype,
                         'projection': self.projection,
                         'geotrandform': self.geotransform,
                         'xmin': self.xmin,
                         'ymin': self.ymin,
                         'xres': self.xres,
                         'yres': self.yres,
                         'nodata': self.nodata}



        else:
            inds = gdal.Open(self.filename, GA_ReadOnly)
            self.raster = inds

            if inds is None:
                raise IOError(
                    "Couldn't open file {0}. Perhaps you need an .hdr file?".format(str(self.filename)))
            else:
                pass

            self.cols = inds.RasterXSize
            self.rows = inds.RasterYSize
            self.bands = inds.RasterCount
            self.dim = [self.rows, self.cols, self.bands]

            self.driver = inds.GetDriver()
            self.dtype = gdal.GetDataTypeName(inds.GetRasterBand(1).DataType)

            self.projection = inds.GetProjection()
            # self.srs = osr.SpatialReference(wkt=inds)

            self.geotransform = inds.GetGeoTransform()

            self.xmin = self.geotransform[0]
            self.ymin = self.geotransform[3]
            self.xres = self.geotransform[1]
            self.yres = self.geotransform[5]

            self.nodata = inds.GetRasterBand(1).GetNoDataValue()

            if self.nodata is None:
                self.nodata = -99999

            self.info = {'bands': self.bands,
                         'dim': self.bands,
                         'dtype': self.dtype,
                         'projection': self.projection,
                         'geotrandform': self.geotransform,
                         'xmin': self.xmin,
                         'ymin': self.ymin,
                         'xres': self.xres,
                         'yres': self.yres,
                         'nodata': self.nodata}

    def __subset(self, x, y):
        """
        Note
        ----------
        Subsetting an Image with coordinates.

        Parameters
        ----------
        data:            array
                         Data to subset.

        area:            tuple with lists
                         Subset coordinates like ([450,477], [0,10]).
        Returns
        -------
        array_like

        """
        try:
            self.array
        except AttributeError:
            raise AssertionError("Before you can subset a file you must convert it to an array with Raster.to_array().")

        if x[0] >= x[1] or y[0] >= y[1]:
            raise AssertionError("The second element of subset_x or subset_y must greater than the first element")

        # Subsetting an Image with a
        if isinstance(self.array, tuple):
            arrays = []
            for i in srange(len(self.array)):
                arrays_subset = self.array[i][y[0]:y[1], x[0]:x[1]]
                arrays.append(arrays_subset)

            data = tuple(arrays)

        else:
            data = self.array[y[0]:y[1], x[0]:x[1]]

        return data

    def copy(self):
        """
        Copy the imported array.

        Returns
        -------
        copy : array_like or tuple
            A copy of Raster.array attribute.

        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can copy a array you must convert the raster files to an array with Raster.to_array().")

        return self.array

    def to_array(self, band=None, flatten=True, quantification_factor=1):
        """
        Converts a binary file of ENVI or PolSARpro or a tif to a numpy
        array.

        Parameters
        ----------
        band : int, tuple or None, optional:
            Define bands which you want to import. If None (default) import all bands in a multidimensional array. You
            can also specify bands in a tuple. E.g. band=(1, 3) will load the first and third band of the image.
        flatten : bool
            if flatten is True the output array is one dimensional. You can convert it to an 2 dimensional array with
            Raster.reshape
        quantification_factor : int, optional
            A quantification factor that scales the reflectance values from 0 to 1. It is only required if the imported
            raster files are reflectance values. For sentinel 2 the factor is 10000. Default is 1, which have no effect.

        Attributes
        ----------
        array : array_like or tuple with array_likes
            Raster files as arrays.

        """
        if isinstance(self.raster, tuple):
            images = []
            for i in srange(len(self.raster)):

                if band is not None:
                    if isinstance(band, list):
                        band = tuple(band)
                        nband = len(band)

                    elif isinstance(band, int):
                        nband = 1

                    else:
                        nband = len(band)

                else:
                    nband = self.bands[i]
                    band = range(self.bands[i])
                    band = [x + 1 for x in band]

                image = np.zeros((nband, self.rows[i], self.cols[i]),
                                 dtype=gdal_array.GDALTypeCodeToNumericTypeCode(self.dtype[i]))

                if isinstance(band, int):
                    band_ = self.raster[i].GetRasterBand(band)
                    image[0] = band_.ReadAsArray()

                else:
                    band_select_list = []
                    for b in band:
                        # Remember, GDAL index is on 1, but Python is on 0 -- so we add 1 for our GDAL calls
                        band_ = self.raster[i].GetRasterBand(b)
                        band_select_list.append(band_)

                    for j in srange(nband):
                        # Read in the band's data into the third dimension of our array
                        image[j] = band_select_list[j].ReadAsArray()

                if quantification_factor > 1:
                    image = image.astype(np.float32) / quantification_factor
                else:
                    pass

                if flatten:
                    array = image

                    image = np.zeros((nband, array[0].size,),
                                     dtype=gdal_array.GDALTypeCodeToNumericTypeCode(self.dtype))

                    if isinstance(band, int):
                        image[0] = array.flatten()
                        image = image.flatten() if nband == 1 else image

                    else:
                        for b in srange(nband):
                            image[b] = array[b].flatten()

                        image = image.flatten() if nband == 1 else image

                image[np.isnan(image)] = self.nodata[i]

                images.append(image)

            self.array = tuple(images)

        else:
            if band is not None:
                if isinstance(band, list):
                    band = tuple(band)
                    nband = len(band)

                elif isinstance(band, int):
                    band = band
                    nband = 1

                else:
                    nband = len(band)

            else:
                nband = self.bands
                band = range(self.bands)
                band = [x + 1 for x in band]

            image = np.zeros((nband, self.rows, self.cols),
                             dtype=gdal_array.GDALTypeCodeToNumericTypeCode(self.dtype))

            if isinstance(band, int):
                band_ = self.raster.GetRasterBand(band)
                image[0] = band_.ReadAsArray()

            else:
                band_select_list = []
                for b in band:
                    # Remember, GDAL index is on 1, but Python is on 0 -- so we add 1 for our GDAL calls
                    band_ = self.raster.GetRasterBand(b)

                    band_select_list.append(band_)

                for j in srange(nband):
                    # Read in the band's data into the third dimension of our array
                    image[j] = band_select_list[j].ReadAsArray()

            if quantification_factor > 1:
                self.array = image.astype(np.float32) / quantification_factor
            else:
                self.array = image

            if flatten:
                image = np.zeros((nband, self.array[0].size,),
                                 dtype=gdal_array.GDALTypeCodeToNumericTypeCode(self.dtype))

                if isinstance(band, int):
                    image[0] = self.array.flatten()
                else:
                    for b in srange(nband):
                        image[b] = self.array[b].flatten()

                self.array = image.flatten() if nband == 1 else image

    def reshape(self):
        """
        Reshape loaded arrays to their original dimension.
        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can reshape a file you must convert it to an array with Raster.to_array().")

        if isinstance(self.raster, tuple):
            if self.array[0].ndim == 1:
                array = []
                for i in srange(len(self.array)):
                    temp = self.array[i].reshape((self.rows[i], self.cols[i]))
                    array.append(temp)

                self.array = tuple(array)

            else:
                array = []
                for i in srange(len(self.array)):
                    temp = self.array[i].reshape((self.array[i].shape[0], self.rows[i], self.cols[i]))
                    array.append(temp)

                self.array = tuple(array)
        else:
            if self.array.ndim == 1:
                self.array = self.array.reshape((self.rows, self.cols))

            else:
                self.array = self.array.reshape((self.array.shape[0], self.rows, self.cols))

    def flatten(self):
        """
        Collapse the loaded arrays into one dimension.

        Returns
        -------
        None

        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can flatten a file you must convert it to an array with Raster.to_array().")

        if isinstance(self.raster, tuple):
            if self.array[0].ndim == 1:
                array = []
                for i in srange(len(self.array)):
                    temp = self.array[i].flatten()
                    array.append(temp)

                self.array = tuple(array)

            else:
                images = []
                for i in srange(len(self.array)):
                    image = np.zeros((self.bands[i], self.array[i][0].size,),
                                     dtype=gdal_array.GDALTypeCodeToNumericTypeCode(self.dtype[i]))

                    for b in srange(self.bands[i]):
                        image[b] = self.array[i][b].flatten()

                    images.append(image)

                self.array = tuple(images)

        else:
            if self.array.ndim == 1:
                self.array = self.array.flatten()

            else:
                image = np.zeros((self.bands, self.array[0].size,),
                                 dtype=gdal_array.GDALTypeCodeToNumericTypeCode(self.dtype))

                for b in srange(self.bands):
                    image[b] = self.array[b].flatten()

                self.array = image

    def set_nodata(self, nodata):
        """
        Set and assign a new no data value.

        Parameters
        ----------
        nodata : int, float or np.nan
            New no data value. A tuple with in, float or np.nan is also possible if you imported more than one file.

        Returns
        -------
        None

        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can assign a new no data value must convert the data to an array with Raster.to_array().")

        if isinstance(self.raster, tuple):
            nodata_list = []
            for i in srange(len(self.array)):
                nodata_list.append(nodata)

            self.nodata = tuple(nodata_list)

            for i in srange(len(self.array)):
                self.array[i][np.isnan(self.array[i])] = self.nodata[i]
                self.array[i][np.where(self.array[0] == 0)] = self.nodata[i]
        else:
            self.nodata = nodata
            self.array[np.isnan(self.array)] = self.nodata
            self.array[np.where(self.array[0] == 0)] = self.nodata

    def write(self, data, filename, path=None, reference=0):
        """
        Convert an array into a binary (.bin) file with header (.hdr) or a Tif file.

        Parameters
        ----------
        data : array_like or tuple
            Arrays you want to export.
        filename : str or tuple
            File names of the exported arrays. Supported file extension are '.tif' or '.bin'
        path : str, optional
            Export path. If path is None the path will set to current
            directory with os.getwd().
        reference :
            If the Raster import contains several grids, you can specify which of these grids you want to use as
            reference for geo-spatial information (default=0).

        Returns
        -------
        Grid as .tif or .bin
        """
        if path is not None:
            os.chdir(path)
        else:
            pass

        if isinstance(data, tuple):
            if not isinstance(filename, tuple) or len(filename) != len(data):
                raise AssertionError(
                    "If you want to export all arrays you need as much as filnames in a tuple as arrays.")

            for i in srange(len(data)):
                data_ = data[i]
                if data_.ndim <= 1:
                    raise AssertionError("Only 2 dimensional array can be converted into a .tiff file.")

                if data_.ndim == 2:
                    rows, cols = data_.shape
                    ndim = 1

                else:
                    ndim, rows, cols = data_.shape

                gdal_dtype = self.__TYPEMAP[data_.dtype.name]
                origin_x = self.xmin[reference] if isinstance(self.xmin, tuple) else self.xmin
                origin_y = self.ymin[reference] if isinstance(self.ymin, tuple) else self.ymin

                filename_temp = filename[i].split('.')

                if filename_temp[-1] == 'tif' or filename_temp[-1] == 'tiff':
                    outdriver = gdal.GetDriverByName("GTiff")
                elif filename_temp[-1] == 'bin':
                    outdriver = gdal.GetDriverByName('ENVI')
                else:
                    raise AssertionError(
                        "File extension must be `tif`, `tiff` or `bin`. The actual extension is {0}".format(
                            str(filename_temp[-1])))

                outds = outdriver.Create(filename[i], cols, rows, ndim, gdal_dtype)

                for j in srange(ndim):
                    post_1 = self.xres[reference] if isinstance(self.xres, tuple) else self.xres
                    post_2 = self.yres[reference] if isinstance(self.yres, tuple) else self.yres
                    outds.SetGeoTransform([origin_x, post_1, 0.0, origin_y, 0.0, post_2])

                    outds.SetProjection(
                        self.projection[reference] if isinstance(self.projection, tuple) else self.projection)

                    out_band = outds.GetRasterBand(j + 1)
                    if data_.ndim > 2:
                        out_band.WriteArray(data_[j])
                    else:
                        out_band.WriteArray(data_)
                    out_band.SetNoDataValue(self.nodata[reference] if isinstance(self.nodata, tuple) else self.nodata)

        else:
            filename_temp = filename.split('.')

            if filename_temp[-1] == 'tif' or filename_temp[-1] == 'tiff':
                outdriver = gdal.GetDriverByName("GTiff")
            elif filename_temp[-1] == 'bin':
                outdriver = gdal.GetDriverByName('ENVI')
            else:
                raise AssertionError(
                    "File extension must be `tif` or `bin`. The actual extension is {0}".format(str(filename_temp[-1])))

            if data.ndim <= 1:
                raise AssertionError("Only 2 dimensional array can be converted into a .tiff file.")

            # if export != 'all':
            if data.ndim == 2:
                rows, cols = data.shape
                ndim = 1
            else:
                ndim, rows, cols = data.shape

            gdal_dtype = self.__TYPEMAP[data.dtype.name]
            origin_x = self.xmin[reference] if isinstance(self.xmin, tuple) else self.xmin
            origin_y = self.ymin[reference] if isinstance(self.ymin, tuple) else self.ymin

            outds = outdriver.Create(filename, cols, rows, ndim, gdal_dtype)

            for i in srange(ndim):
                post_1 = self.xres[reference] if isinstance(self.xres, tuple) else self.xres
                post_2 = self.yres[reference] if isinstance(self.yres, tuple) else self.yres
                outds.SetGeoTransform([origin_x, post_1, 0.0, origin_y, 0.0, post_2])

                outds.SetProjection(
                    self.projection[reference] if isinstance(self.projection, tuple) else self.projection)

                out_band = outds.GetRasterBand(i + 1)
                if data.ndim > 2:
                    out_band.WriteArray(data[i])
                else:
                    out_band.WriteArray(data)
                out_band.SetNoDataValue(self.nodata[reference] if isinstance(self.nodata, tuple) else self.nodata)

    @staticmethod
    def dB(x):
        """
        Convert a linear value to dB.
        """
        with np.errstate(invalid='ignore'):
            return 10 * np.log10(x)

    @staticmethod
    def linear(x):
        """
        Convert a dB value in linear.
        """
        return 10 ** (x / 10)

    @staticmethod
    def BRDF(BSC, iza, vza, angle_unit='RAD'):
        """
        Convert a Radar Backscatter Coefficient (BSC) into a BRDF.

        Parameters
        ----------
        BSC : int, float or array_like
            Radar Backscatter Coefficient (sigma 0).

        iza : int, float or array_like
            Sun or incidence zenith angle.

        vza : int, float or array_like
            View or scattering zenith angle.

        angle_unit : {'DEG', 'RAD'} (default = 'RAD'), optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG].
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].

        Returns
        -------
        BRDF value : int, float or array_like

        """
        if angle_unit == 'RAD':
            return BSC / (np.cos(iza) * np.cos(vza) * (4 * np.pi))

        elif angle_unit == 'DEG':
            return BSC / (np.cos(np.radians(iza)) * np.cos(np.radians(vza)) * (4 * np.pi))
        else:
            raise ValueError("angle_unit must be 'RAD' or 'DEG'")

    @staticmethod
    def BRF(BRDF):
        """
        Convert a BRDF into a BRF.

        Parameters
        ----------
        BRDF : int, float or array_like
            BRDF value.

        Returns
        -------
        BRF value : int, float or array_like

        """
        return np.pi * BRDF

    @staticmethod
    def BSC(BRDF, iza, vza, angle_unit='RAD'):
        """
        Convert a BRDF in to a Radar Backscatter Coefficient (BSC).

        Parameters
        ----------
        BSC : int, float or array_like
            Radar Backscatter Coefficient (sigma 0).

        iza : int, float or array_like
            Sun or incidence zenith angle.

        vza : int, float or array_like
            View or scattering zenith angle.

        angle_unit : {'DEG', 'RAD'} (default = 'RAD'), optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG].
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].

        Returns
        -------
        BRDF value : int, float or array_like

        """
        if angle_unit == 'RAD':
            return BRDF * np.cos(iza) * np.cos(vza) * 4 * np.pi

        elif angle_unit == 'DEG':
            return BRDF * np.cos(np.radians(iza)) * np.cos(np.radians(vza)) * (4 * np.pi)
        else:
            raise ValueError("angle_unit must be 'RAD' or 'DEG'")

    def convert(self, system='BSC', to='BRDF', system_unit='linear', output_unit='linear', iza=None, vza=None,
                angle_unit='RAD'):
        """
        Convert the data from BSC, BRDF, BRF to BRDF, BSC or BRF.

        Parameters
        ----------
        system : {'BSC', 'BRDF', 'BRF'}
            The actual unit of the data. Default is 'BSC'.
        to : {'BSC', 'BRDF', 'BRF'}
            The desired unit after conversion. Default is 'BRDF'
        system_unit : {'linear', 'dB'}, optional
            Are the measurements in a linear scale or in decibel? Default is 'linear'.
        output_unit :  {'linear', 'dB'}, optional
            The desired output format. Default is 'linear'.
        iza : int, float, array_like or None, , optional
            Sun or incidence zenith angle. Default is None.
        vza : int, float, array_like or None, optional
            View or scattering zenith angle.
        angle_unit : {'DEG', 'RAD'}, optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG] (default).
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].

        Returns
        -------
        None
        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can convert you must convert the data to an array with Raster.to_array().")

        if isinstance(self.raster, tuple):
            if system is 'BSC':
                if to is 'BRDF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BRDF(self.array[i], iza, vza, angle_unit)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BRDF(self.array[i], iza, vza, angle_unit)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BRDF(temp, iza, vza, angle_unit)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BRDF(temp, iza, vza, angle_unit)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

                elif to is 'BRF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BRDF(self.array[i], iza, vza, angle_unit)
                                temp = Raster.BRF(temp)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BRDF(self.array[i], iza, vza, angle_unit)
                                temp = Raster.BRF(temp)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BRDF(temp, iza, vza, angle_unit)
                                temp = Raster.BRF(temp)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BRDF(temp, iza, vza, angle_unit)
                                temp = Raster.BRF(temp)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

            if system is 'BRDF':
                if to is 'BSC':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BSC(self.array[i], iza, vza, angle_unit)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BSC(self.array[i], iza, vza, angle_unit)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BSC(temp, iza, vza, angle_unit)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BSC(temp, iza, vza, angle_unit)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)
                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

                elif to is 'BRF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BRF(self.array[i])
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.BRF(self.array[i])
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BRF(temp)
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        elif output_unit is 'dB':
                            array_list = []
                            for i in srange(len(self.array)):
                                temp = Raster.linear(self.array[i])
                                temp = Raster.BRF(temp)
                                temp = Raster.dB(temp)
                                temp[np.isnan(temp)] = self.nodata
                                array_list.append(temp)

                            self.array = tuple(array_list)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

        else:
            if system is 'BSC':
                if to is 'BRDF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)

                        elif output_unit is 'dB':
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)
                            self.array = Raster.dB(self.array)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)

                        elif output_unit is 'dB':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

                elif to is 'BRF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)
                            self.array = Raster.BRF(self.array)

                        elif output_unit is 'dB':
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)
                            self.array = Raster.BRF(self.array)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)
                            self.array = Raster.BRF(self.array)

                        elif output_unit is 'dB':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BRDF(self.array, iza, vza, angle_unit)
                            self.array = Raster.BRF(self.array)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

            if system is 'BRDF':
                if to is 'BSC':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)

                        elif output_unit is 'dB':
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)

                        elif output_unit is 'dB':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

                elif to is 'BRF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            self.array = Raster.BRF(self.array)

                        elif output_unit is 'dB':
                            self.array = Raster.BRF(self.array)
                            self.array = Raster.dB(self.array)

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BRF(self.array)

                        elif output_unit is 'dB':
                            self.array = Raster.linear(self.array)
                            self.array = Raster.BRF(self.array)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

            if system is 'BRF':
                if to is 'BSC':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            self.array = self.array / np.pi
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)

                        elif output_unit is 'dB':
                            self.array = self.array / np.pi
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            self.array = Raster.linear(self.array)
                            self.array = self.array / np.pi
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)

                        elif output_unit is 'dB':
                            self.array = Raster.linear(self.array)
                            self.array = self.array / np.pi
                            self.array = Raster.BSC(self.array, iza, vza, angle_unit)
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

                elif to is 'BRDF':
                    if system_unit is 'linear':

                        if output_unit is 'linear':
                            self.array = self.array / np.pi

                        elif output_unit is 'dB':
                            self.array = self.array / np.pi
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    elif system_unit is 'dB':

                        if output_unit is 'linear':
                            self.array = Raster.linear(self.array)
                            self.array = self.array / np.pi

                        elif output_unit is 'dB':
                            self.array = Raster.linear(self.array)
                            self.array = self.array / np.pi
                            self.array = Raster.dB(self.array)
                            self.array[np.isnan(self.array)] = self.nodata

                        else:
                            raise AssertionError("Output unit must be 'linear' or 'dB'")

                    else:
                        raise AssertionError("System unit must be 'linear' or 'dB'")

    def dstack(self, unfold=False):
        """
        Stack 1-D arrays as columns into a 2-D array.
        Take a sequence of 1-D arrays and stack them as columns to make a single 2-D array.
        2-D arrays are stacked as-is, just like with numpy.hstack. 1-D arrays are turned into 2-D columns first.

        Parameters
        ----------
         unfold : bool, optional
            If the arrays are multi dimensional this option extracts the individual dimension and stack it to an array.
            Default is False.

        Attributes
        ----------
        stack : array_like
            Stacked array.

        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can convert you must convert the data to an array with Raster.to_array().")

        if unfold is False:
            if not isinstance(self.raster, tuple):
                raise AssertionError("You need more than one array to build a stack.")

            self.stack = np.column_stack(self.array)

        else:
            if not isinstance(self.raster, tuple):
                if self.bands < 2:
                    raise AssertionError("You need more than one dimension to build a folded stack.")

                elif self.array.ndim >= 3:
                    self.flatten()

                else:
                    array_list = []
                    for i in srange(self.bands):
                        array_list.append(self.array[i])

                    array = tuple(array_list)

                    self.stack = np.column_stack(array)

            else:
                band_list = []
                for i in srange(len(self.bands)):

                    if self.bands[i] < 2:
                        raise AssertionError("You need more than one dimension to build a folded stack.")

                    elif self.array[i].ndim >= 3:
                        self.flatten()

                    else:
                        array_list = []
                        for j in srange(self.bands[i]):
                            array_list.append(self.array[i][j])

                        array_stack = np.column_stack(tuple(array_list))

                        band_list.append(array_stack)

                self.stack = tuple(band_list)

    def reset(self):
        """
        Delete the attributes Raster.array and Raster.stack
        """
        try:
            del self.array
        except AttributeError:
            pass

        try:
            del self.stack
        except AttributeError:
            pass
