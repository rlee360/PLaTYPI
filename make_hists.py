# This script stacks multiple images together to make a histogram that
# it exports as a pickle file.

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

np.set_printoptions(linewidth=100, edgeitems=12)

'''
# of bins
# dims
'''

start_year = 2013
end_year = 2019
start_date = '04-01' # MM-DD
end_date = '11-01' # MM-DD
counties = get_counties_dict()

collections = [
    # "T1_SR"
    # "NASA/ORNL/DAYMET_V4"
    "ECMWF/ERA5/DAILY"
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
        file_list = glob.glob(f'{_path}/*.tif')
        tiffs = []
        for geotiff_file in file_list:
            # print(geotiff_file)
            cdl_name = '/'.join(geotiff_file.split("/")[:-3]) + "/cdl.tif"
            cdl = rasterio.open(cdl_name)
            cdl_data = np.transpose(cdl.read(out_shape=(cdl.count, int(cdl.height/2), int(cdl.width/2)), resampling=Resampling.bilinear), axes=(1, 2, 0)).astype('bool')
            with rasterio.open(geotiff_file) as src:
                ds = src.read( out_shape=(src.count, int(cdl.height/2), int(cdl.width/2)), resampling=Resampling.bilinear )
                img = np.transpose(ds, axes=(1, 2, 0)).astype('float32')
                img = ma.array(img, mask=np.tile(np.expand_dims(cdl_data, axis=-1), (1,1,img.shape[-1])))
                if img.shape[-1] == num_chan:
                    img = img.reshape(-1, img.shape[-1])
                    tiffs.append(img)
        if len(tiffs) == 0:
            print('Tiff empty!', _path, len(file_list))
        stacked_tiffs = np.concatenate(tiffs, axis=0)
        flat_tiffs = stacked_tiffs
        hists.append(np.apply_along_axis(lambda el: np.histogram(el, bins=NBINS)[0], axis=0, arr=flat_tiffs))
    hist_stack = np.stack(hists)
    fname = f"{'_'.join(_paths[0].split('/')[-2:])}_masked.pkl"
    pickle.dump(hist_stack, open(fname, 'w+b'), protocol=4)

for p in paths:
   opener(p)

