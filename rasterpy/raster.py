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
        Filename as string or a tuple with filename of the raster data.
    path : str, optional
        Path to raster data. If path is None the path will set to current
        directory with os.getwd().
    extension : str, optional
        If you want to import all files in a directory with a
        specific extension, set filename to None and define an extension like '.tiff' or '.bin'.
    check_dim : bool
        If True the imported files must have the same dimensions.

    Returns
    -------
    All returns are attributes!
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
                print ("Loading file {0}".format(str(self.filename[i])))
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



        else:
            inds = gdal.Open(self.filename, GA_ReadOnly)
            self.raster = inds

            print ("Loading file {0}".format(str(self.filename)))
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

    def to_array(self, band=1, subset_x=None, subset_y=None, ndim=1):
        """
        Converts a binary file of ENVI or PolSARpro or a tif to a numpy
        array. Lack of an ENVI .hdr file will cause this to crash.

        Parameters
        ----------
        band : int
            Define a band which you want to export.
        subset_x : tuple with int
            If you want to load a subset of the raster file define here the
            x pixel coordinates like (500, 800).
        subset_y : tuple with int
            If you want to load a subset of the raster file define here the
            y pixel coordinates like (500, 800).
        ndim : {1, 2}
            if ndim is 1 the output array is one dimensional. You can convert it to an 2 dimensional array with
            Raster.reshape

        Returns
        -------
        array : array_like or tuple with array_likes
            Raster files as arrays.

        """
        if isinstance(self.raster, tuple):
            band_ = tuple(map(lambda item: item.GetRasterBand(band), self.raster))

            self.array = tuple(map(lambda tband, tcols, trows: tband.ReadAsArray(0, 0, tcols, trows),
                                   band_, self.cols, self.rows))

            if subset_x is not None and subset_y is not None:
                self.array = self.__subset(x=subset_x, y=subset_y)
                self.cols = tuple(map(lambda item: item.shape[1], self.array))
                self.rows = tuple(map(lambda item: item.shape[0], self.array))

            for i in srange(len(self.array)):
                self.array[i][np.isnan(self.array[i])] = self.nodata[i]

            if ndim == 1:
                array = []
                for i in srange(len(self.array)):
                    temp = self.array[i].flatten()
                    array.append(temp)

                self.array = tuple(array)

            for item in self.filename:
                print ("File {0} opened successfully".format(str(item)))

        else:
            band_ = self.raster.GetRasterBand(band)
            self.array = band_.ReadAsArray(0, 0, self.cols, self.rows)

            if subset_x is not None and subset_y is not None:
                self.array = self.__subset(x=subset_x, y=subset_y)
                self.cols = self.array.shape[1]
                self.rows = self.array.shape[0]

            self.array[np.isnan(self.array)] = self.nodata

            if ndim == 1:
                self.array = self.array.flatten()

            print ("File {0} opened successfully".format(str(self.filename)))

    def reshape(self):
        """
        Reshape loaded arrays to their original dimension.

        Returns
        -------
        None

        """
        try:
            self.array
        except AttributeError:
            raise AssertionError(
                "Before you can reshape a file you must convert it to an array with Raster.to_array().")

        if isinstance(self.raster, tuple):
            array = []
            for i in srange(len(self.array)):
                temp = self.array[i].reshape((self.rows[i], self.cols[i]))
                array.append(temp)

            self.array = tuple(array)

        else:
            self.array = self.array.reshape((self.rows, self.cols))

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
            array = []
            for i in srange(len(self.array)):
                temp = self.array[i].flatten()
                array.append(temp)

            self.array = tuple(array)

        else:
            self.array = self.array.flatten()

    def set_nodata(self, nodata):
        """
        Set and assign new no data value.

        Parameters
        ----------
        nodata : int, float or np.nan
            New no data value

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
            for i in range(len(self.array)):
                nodata_list.append(nodata)

            self.nodata = tuple(nodata_list)

            for i in srange(len(self.array)):
                self.array[i][np.isnan(self.array[i])] = self.nodata[i]

        else:
            self.nodata = nodata
            self.array[np.isnan(self.array)] = self.nodata

    def to_grid(self, data, filename, path=None, export='all', band=1, reference=0):
        """
        Convert an array into a binary (.bin) file with header (.hdr) or a Tif file.

        Parameters
        ----------
        data : array_like or tuple with array_like
            Arrays you want to export.
        filename : str or tuple with str
            File names of the exported arrays. Supported file extension are '.tif' or '.bin'
        path : str, optional
            Export path. If path is None the path will set to current
            directory with os.getwd().
        export : int or 'all', optional
            If data is tuple instance you can specify which tuple item you want to export. If 'all' (default) all items
            will be exported. In this case filename must have the same len as data.
        band : int
            Write the data in a specific band.
        reference :
            If the Raster import contains several grids, you can specify which of these grids you want to use as
            reference for geospatial information (default=0).

        Returns
        -------
        Grid as .tif or .bin
        """
        if path is not None:
            os.chdir(path)
        else:
            pass

        if isinstance(data, tuple):
            if export == 'all':
                if not isinstance(filename, tuple) or len(filename) != len(data):
                    raise AssertionError(
                        "If you want to export all arrays you need as much as filnames in a tuple as arrays.")

                for i in srange(len(data)):
                    data_ = data[i]
                    if data_.ndim <= 1:
                        raise AssertionError("Only 2 dimensional array can be converted into a .tiff file.")
                    rows, cols = data_.shape
                    bands = band
                    gdal_dtype = self.__TYPEMAP[data_.dtype.name]
                    origin_x = self.xmin[reference] if isinstance(self.xmin, tuple) else self.xmin
                    origin_y = self.ymin[reference] if isinstance(self.ymin, tuple) else self.ymin

                    filename_temp = filename[i].split('.')

                    if filename_temp[-1] == 'tif':
                        outdriver = gdal.GetDriverByName("GTiff")
                    elif filename_temp[-1] == 'bin':
                        outdriver = gdal.GetDriverByName('ENVI')
                    else:
                        raise AssertionError("File extension must be `tif` or `bin`. The actual extension is {0}".format(str(filename_temp[-1])))

                    outds = outdriver.Create(filename[i], cols, rows, bands, gdal_dtype)

                    post_1 = self.xres[reference] if isinstance(self.xres, tuple) else self.xres
                    post_2 = self.yres[reference] if isinstance(self.yres, tuple) else self.yres
                    outds.SetGeoTransform([origin_x, post_1, 0.0, origin_y, 0.0, post_2])

                    outds.SetProjection(self.projection[reference] if isinstance(self.projection, tuple) else self.projection)

                    out_band = outds.GetRasterBand(band)
                    out_band.WriteArray(data_)
                    out_band.SetNoDataValue(
                        self.nodata[reference] if isinstance(self.nodata, tuple) else self.nodata)

                    print ("File {0} converted successfully".format(str(filename[i])))

            else:
                filename_temp = filename.split('.')

                if filename_temp[-1] == 'tif':
                    outdriver = gdal.GetDriverByName("GTiff")
                elif filename_temp[-1] == 'bin':
                    outdriver = gdal.GetDriverByName('ENVI')
                else:
                    raise AssertionError(
                        "File extension must be `tif` or `bin`. The actual extension is {0}".format(
                            str(filename_temp[-1])))

                data = data[export]

                if data.ndim <= 1:
                    raise AssertionError("Only 2 dimensional array can be converted into a .tiff file.")

                rows, cols = data.shape
                bands = band
                gdal_dtype = self.__TYPEMAP[data.dtype.name]
                origin_x = self.xmin[reference] if isinstance(self.xmin, tuple) else self.xmin
                origin_y = self.ymin[reference] if isinstance(self.ymin, tuple) else self.ymin

                outds = outdriver.Create(filename, cols, rows, bands, gdal_dtype)

                post_1 = self.xres[reference] if isinstance(self.xres, tuple) else self.xres
                post_2 = self.yres[reference] if isinstance(self.yres, tuple) else self.yres
                outds.SetGeoTransform([origin_x, post_1, 0.0, origin_y, 0.0, post_2])

                outds.SetProjection(
                    self.projection[reference] if isinstance(self.projection, tuple) else self.projection)

                out_band = outds.GetRasterBand(band)
                out_band.WriteArray(data)
                out_band.SetNoDataValue(self.nodata[reference] if isinstance(self.nodata, tuple) else self.nodata)

                print ("File {0} converted successfully".format(str(filename)))

        else:
            filename_temp = filename.split('.')

            if filename_temp[-1] == 'tif':
                outdriver = gdal.GetDriverByName("GTiff")
            elif filename_temp[-1] == 'bin':
                outdriver = gdal.GetDriverByName('ENVI')
            else:
                raise AssertionError("File extension must be `tif` or `bin`. The actual extension is {0}".format(str(filename_temp[-1])))

            if data.ndim <= 1:
                raise AssertionError("Only 2 dimensional array can be converted into a .tiff file.")

            rows, cols = data.shape
            bands = band
            gdal_dtype = self.__TYPEMAP[data.dtype.name]
            origin_x = self.xmin[reference] if isinstance(self.xmin, tuple) else self.xmin
            origin_y = self.ymin[reference] if isinstance(self.ymin, tuple) else self.ymin

            outds = outdriver.Create(filename, cols, rows, bands, gdal_dtype)

            post_1 = self.xres[reference] if isinstance(self.xres, tuple) else self.xres
            post_2 = self.yres[reference] if isinstance(self.yres, tuple) else self.yres
            outds.SetGeoTransform([origin_x, post_1, 0.0, origin_y, 0.0, post_2])

            outds.SetProjection(self.projection[reference] if isinstance(self.projection, tuple) else self.projection)

            out_band = outds.GetRasterBand(band)
            out_band.WriteArray(data)
            out_band.SetNoDataValue(self.nodata[reference] if isinstance(self.nodata, tuple) else self.nodata)

            print ("File {0} converted successfully".format(str(filename)))
