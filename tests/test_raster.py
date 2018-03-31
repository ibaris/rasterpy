import pytest
import rasterpy as rpy

path = "./data/"
file1 = 'test_file_1.tif'
file2 = 'test_file_2.tif'
files = (file1, file2)

class TestImport:
    def import_one(self):
        ras = rpy.Raster(file1, path)
