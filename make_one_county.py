# This script generates the histograms for a single county

import os
import rasterio
import numpy as np
import glob
from counties import get_counties_dict
import math
from multiprocessing import Pool
import pickle
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
import numpy.ma as ma
from numba import jit

np.set_printoptions(linewidth=100, edgeitems=12)

# use calhoun 2015
'''
# of bins
# dims
'''

start_year = 2015
end_year = 2015
start_date = '04-01' # MM-DD
end_date = '11-01' # MM-DD
counties = {19025 : 'Calhoun'} # get_counties_dict()

collections = [
    # "T1_SR"
    "NASA/ORNL/DAYMET_V4" 
    # "ECMWF/ERA5/DAILY"
    # 'NASA/GLDAS/V021/NOAH/G025/T3H'
]

paths = []


for year in range(start_year, end_year+1):
    _start_date = f"{year}-{start_date}"
    _end_date = f"{year}-{end_date}"
    l = []
    for collection in collections:
        col_name = collection.split('/')[-1]
        for county in counties.values():
            count_name = county.replace(' ', '_')
            l.append(os.path.join(os.getcwd(), 'data', count_name, str(year), col_name))
    paths.append(l)

NBINS = 100

def make_hists(flat_tiffs):
    s = flat_tiffs.shape
    res = np.zeros((NBINS, s[1], s[2], s[3]))
    for i in range(s[1]):
        for j in range(s[2]):
            for k in range(s[3]):
                res[:, i, j, k] = np.histogram(flat_tiffs[:, i, j, k].flatten(), bins=NBINS)
    return res
   
def opener(_paths):
    # print(_paths)
    hists = []
    for _path in _paths:
        print(_path)
        if 'DAILY' in _path:
            num_chan = 9
        elif 'T1_SR' in _path:
            num_chan = 12
        elif 'DAYMET' in _path:
            num_chan = 7
        file_list = sorted(glob.glob(f'{_path}/*.tif'))
        tiffs = []
        for geotiff_file in file_list:
            print(geotiff_file)
            cdl_name = '/'.join(geotiff_file.split("/")[:-3]) + "/cdl.tif"
            cdl = rasterio.open(cdl_name)
            # cdl_data = np.transpose(cdl.read(out_shape=(cdl.count, int(cdl.height/2), int(cdl.width/2)), resampling=Resampling.bilinear), axes=(1, 2, 0)).astype('bool')
            # plt.imshow(cdl_data[:, :, 0], cmap='binary_r')
            with rasterio.open(geotiff_file) as src:
                print(int(cdl.height/2), int(cdl.width/2))
                ds = src.read( out_shape=(src.count, int(cdl.height/4), int(cdl.width/4)), resampling=Resampling.bilinear )
                img = np.transpose(ds, axes=(1, 2, 0)).astype('float32')
                print(img.shape, num_chan)
                if img.shape[-1] == num_chan:
                    tiffs.append(img)
            cdl.close()
        if len(tiffs) == 0:
            print('Tiff empty!', _path, len(file_list))
        stacked_tiffs = np.stack(tiffs)
        print(stacked_tiffs.shape)
        flat_tiffs = stacked_tiffs
        print('prehist')
        # x = make_hists(flat_tiffs)
        x = np.apply_along_axis(lambda el: np.histogram(el, bins=NBINS, range=(np.min(el), np.max(el)))[0], axis=0, arr=flat_tiffs)
        print('posthist', x.shape)
    fname = f"{'_'.join(_paths[0].split('/')[-2:])}_calhoun.pkl"
    pickle.dump(x, open(fname, 'w+b'), protocol=4)

for p in paths:
   opener(p)
