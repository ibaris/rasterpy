import os
from distutils import dir_util

from pytest import fixture
import pytest
import rasterpy as rpy
import numpy as np


@fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for locating the test data directory and copying it
    into a temporary directory.
    Taken from  http://www.camillescott.org/2016/07/15/travis-pytest-scipyconf/
    """
    filename = request.module.__file__
    test_dir = os.path.dirname(filename)
    data_dir = os.path.join(test_dir, 'data')
    dir_util.copy_tree(data_dir, str(tmpdir))

    def getter(filename, as_str=True):
        filepath = tmpdir.join(filename)
        if as_str:
            return str(filepath)
        return filepath

    return getter


info_dict1 = {'bands': 3,
              'dim': 3,
              'dtype': 'Float32',
              'geotrandform': (625680.0, 20.0, 0.0, 5693480.0, 0.0, -20.0),
              'nodata': -99999.0,
              'projection': 'PROJCS["WGS 84 / UTM zone 32N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","32632"]]',
              'xmin': 625680.0,
              'xres': 20.0,
              'ymin': 5693480.0,
              'yres': -20.0}

info_dict2 = {'bands': (3, 3),
              'dim': (3, 3),
              'dtype': ('Float32', 'Float32'),
              'geotrandform': ((625680.0, 20.0, 0.0, 5693480.0, 0.0, -20.0),
                               (625680.0, 20.0, 0.0, 5693480.0, 0.0, -20.0)),
              'nodata': (-99999.0, -99999.0),
              'projection': (
              'PROJCS["WGS 84 / UTM zone 32N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","32632"]]',
              'PROJCS["WGS 84 / UTM zone 32N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","32632"]]'),
              'xmin': (625680.0, 625680.0),
              'xres': (20.0, 20.0),
              'ymin': (5693480.0, 5693480.0),
              'yres': (-20.0, -20.0)}


class TestImport:
    # def test_import_one(self, datadir):
    #     file1 = datadir('RGB.BRDF.tif')
    #     ras = rpy.Raster(file1, path=None)
    #
    #     assert ras.info == info_dict1
    #
    # def test_import_tuple(self, datadir):
    #     file1 = datadir('RGB.BRDF.tif')
    #     file2 = datadir('RGB.BRDF.tif')
    #     files = (file1, file2)
    #     ras = rpy.Raster(files, path=None)
    #
    #     assert ras.info == info_dict2

    def test_no_data(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        ras = rpy.Raster(file1, path=None)
        ras.to_array()
        ras.set_nodata(0)

        assert ras.nodata == 0


class TestRaiseOne:
    def test_reshape(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.reshape()

    def test_flatten(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.flatten()

    def test_set_nodata(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.set_nodata(-99999)

    def test_convert(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.convert()

    def test_dstack2(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.dstack()


class TestRaiseTuple:
    def test_reshape(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)
        ras = rpy.Raster(files, path=None)
        with pytest.raises(AssertionError):
            ras.reshape()

    def test_flatten(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)
        ras = rpy.Raster(files, path=None)
        with pytest.raises(AssertionError):
            ras.flatten()

    def test_set_nodata(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)
        ras = rpy.Raster(files, path=None)
        with pytest.raises(AssertionError):
            ras.set_nodata(-99999)

    def test_convert(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)
        ras = rpy.Raster(files, path=None)
        with pytest.raises(AssertionError):
            ras.convert()

    def test_dstack2(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)
        ras = rpy.Raster(files, path=None)
        with pytest.raises(AssertionError):
            ras.dstack()
