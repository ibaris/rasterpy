import os
from distutils import dir_util

from pytest import fixture
import pytest
import rasterpy as rpy
from numpy import allclose


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


class TestDim:

    def test_ndim(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        r = rpy.Raster(file1, path=None)
        r.to_array()

        r2 = rpy.Raster(file1, path=None)
        r2.to_array(flatten=False)

        r3 = rpy.Raster(file1, path=None)
        r3.to_array(flatten=False, quantification_factor=10000)

        r4 = rpy.Raster(file1, path=None)
        r4.to_array(band=1)

        assert r.array.ndim == 2
        assert r.array.shape[0] == 3
        assert r.array.shape[1] == 62328

        assert r2.array.shape[0] == 3
        assert r2.array.shape[1] == 196
        assert r2.array.shape[2] == 318

    def test_ndim_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)

        r = rpy.Raster(files, path=None)
        r.to_array()

        r2 = rpy.Raster(files, path=None)
        r2.to_array(flatten=False)

        r3 = rpy.Raster(files, path=None)
        r3.to_array(flatten=False, quantification_factor=10000)

        r4 = rpy.Raster(files, path=None)
        r4.to_array(band=1)

        assert r.array[0].ndim == 2
        assert r.array[0].shape[0] == 3
        assert r.array[0].shape[1] == 62328

        assert r2.array[0].shape[0] == 3
        assert r2.array[0].shape[1] == 196
        assert r2.array[0].shape[2] == 318

        assert r.array[1].ndim == 2
        assert r.array[1].shape[0] == 3
        assert r.array[1].shape[1] == 62328

        assert r2.array[1].shape[0] == 3
        assert r2.array[1].shape[1] == 196
        assert r2.array[1].shape[2] == 318

        # assert allclose(r3.array.mean(), -0.0016487569)


class TestArraySelect:
    def test_select_int(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        r = rpy.Raster(file1, path=None)
        r.to_array(band=1)

        assert r.array.shape[0] == 62328

    def test_select_int_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)

        r = rpy.Raster(files, path=None)
        r.to_array(band=1)

        assert r.array[0].shape[0] == 62328
        assert r.array[1].shape[0] == 62328

    def test_select_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        r = rpy.Raster(file1, path=None)
        r.to_array(band=(1, 3))

        assert r.array.ndim == 2

    def test_select_tuple_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)

        r = rpy.Raster(files, path=None)
        r.to_array(band=(1, 3))

        assert r.array[0].ndim == 2
        assert r.array[1].ndim == 2

class TestValues:
    def test_value(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        r = rpy.Raster(file1, path=None)
        r.to_array()

        assert allclose(r.array.mean(), -16.48756920623467)

    def test_value_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)

        r = rpy.Raster(files, path=None)
        r.to_array()

        assert allclose(r.array[0].mean(), -16.48756920623467)
        assert allclose(r.array[1].mean(), -16.48756920623467)

    def test_value_select_int(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        r = rpy.Raster(file1, path=None)
        r.to_array(band=1)

        assert allclose(r.array.mean(), -16.961706109713138)

    def test_value_tuple_select_int(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)

        r = rpy.Raster(files, path=None)
        r.to_array(band=1)

        assert allclose(r.array[0].mean(), -16.961706109713138)
        assert allclose(r.array[1].mean(), -16.961706109713138)

    def test_value_select_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        r = rpy.Raster(file1, path=None)
        r.to_array(band=(1, 3))

        assert allclose(r.array.mean(), -16.39290269043384)

    def test_value_tuple_select_tuple(self, datadir):
        file1 = datadir('RGB.BRDF.tif')
        file2 = datadir('RGB.BRDF.tif')
        files = (file1, file2)

        r = rpy.Raster(files, path=None)
        r.to_array(band=(1, 3))

        assert allclose(r.array[0].mean(), -16.39290269043384)
        assert allclose(r.array[1].mean(), -16.39290269043384)