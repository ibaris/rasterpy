import rasterpy as rpy

path = "./tests/data/"
file1 = 'test_file_1.tif'
file2 = 'test_file_2.tif'

files = (file1, file2)
r = rpy.Raster(files, path)
r.to_array(subset_x=(500, 600), subset_y=(500, 600))