class RasterResult(dict):
    """ Represents the reflectance result.

    Returns
    -------
    All returns are attributes!
    cols, rows : int or tuple
        Columns and row size of the imported raster files.
    files : str
        Filenames of each raster file.
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

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume

    The attribute 'ms' is the multi scattering contribution. This is only available if it is calculated. For detailed
    parametrisation one can use BSC.ms.sms or BSC.ms.smv for the multiple scattering contribution of surface or volume,
    respectively.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())