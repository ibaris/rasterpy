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


info_dict1 = {'bands': 1,
              'dim': 1,
              'dtype': 'Int32',
              'geotrandform': (12.203257905736805,
                               0.00011352085570948134,
                               0.0,
                               50.90488135389295,
                               0.0,
                               -0.00010517297066314768),
              'nodata': -99999,
              'projection': 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]',
              'xmin': 12.203257905736805,
              'xres': 0.00011352085570948134,
              'ymin': 50.90488135389295,
              'yres': -0.00010517297066314768}

info_dict2 = {'bands': (1, 1),
              'dim': (1, 1),
              'dtype': ('Int32', 'Int32'),
              'geotrandform': ((12.203257905736805,
                                0.00011352085570948134,
                                0.0,
                                50.90488135389295,
                                0.0,
                                -0.00010517297066314768),
                               (12.203257905736805,
                                0.00011352085570948134,
                                0.0,
                                50.90488135389295,
                                0.0,
                                -0.00010517297066314768)),
              'nodata': (-99999, -99999),
              'projection': (
                  'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]',
                  'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'),
              'xmin': (12.203257905736805, 12.203257905736805),
              'xres': (0.00011352085570948134, 0.00011352085570948134),
              'ymin': (50.90488135389295, 50.90488135389295),
              'yres': (-0.00010517297066314768, -0.00010517297066314768)}


class TestImport:
    def test_import_one(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)

        assert ras.info == info_dict1

    def test_import_tuple(self, datadir):
        file1 = datadir('test_file_1.tif')
        file2 = datadir('test_file_2.tif')
        files = (file1, file2)
        ras = rpy.Raster(files, path=None)

        assert ras.info == info_dict2

    def test_no_data(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        ras.to_array()
        ras.set_nodata(0)

        assert ras.nodata == 0

class TestArray:
    def test_array_one(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        ras.to_array(band=1)
        assert ras.array[0] == 117
        assert ras.array[-1] == 112
        assert ras.array.ndim == 1
        assert ras.array.size == 1500

class TestRaise:
    def test_reshape(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.reshape()

    def test_flatten(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.flatten()

    def test_set_nodata(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.set_nodata(-99999)

    # def test_write(self, datadir):
    #     file1 = datadir('test_file_1.tif')
    #     ras = rpy.Raster(file1, path=None)
    #     ras.to_array()
    #     with pytest.raises(AssertionError):
    #         ras.write(ras.array, 'test')

    def test_convert(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.convert()

    def test_dstack2(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.dstack2()

    def test_dstack3(self, datadir):
        file1 = datadir('test_file_1.tif')
        ras = rpy.Raster(file1, path=None)
        with pytest.raises(AssertionError):
            ras.dstack3()