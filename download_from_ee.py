# This script loops over year, image collection, county and downloads the 
# data in parallel across 16 threads

import ee

# ee.Authenticate()
ee.Initialize()

from counties import get_counties_dict

import math
from multiprocessing import Pool
import os
import json
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import geemap.eefolium as geemap

def make_aoi(shape_file):
    with open (shape_file, 'r') as f:
        borders = json.load(f)

    iowa_geometry = borders['features'][0]['geometry']
    pprint(iowa_geometry)
    return ee.Geometry(iowa_geometry)

# crop stuff

fip_header = 19
STATE = "Iowa"
aoi = ee.FeatureCollection('TIGER/2018/States').filterMetadata('NAME', 'equals', STATE).geometry()
crop_collection = ee.ImageCollection('USDA/NASS/CDL').filterBounds(aoi).filterDate('2018-01-01', '2019-12-31')
counties_dict = get_counties_dict()
start_year = 2020
end_year = 2020

# Crop Season
start_date = '04-01' # MM-DD
end_date = '11-01' # MM-DD
area = 'iowa_simplified.geojson'

crop_collection = crop_collection.map(lambda image: image.clip(aoi))

# is cropland
crops = crop_collection.select(['confidence']).mean()
crop_threshold = 97
ee_crop_threshold = ee.Image.constant(crop_threshold)
is_crop_mask = crops.gte(ee_crop_threshold)

# is corn
crop_types = crop_collection.select(['cropland']).mode()
corn = 1
ee_corn = ee.Image.constant(corn)
is_corn_mask = crop_types.eq(ee_corn)

# is cultivated
cultivated = crop_collection.select(['cultivated']).mean()
cultivated_threshold = 1.5
ee_cultivated_threshold = ee.Image.constant(cultivated_threshold)
final_mask = cultivated.gte(ee_cultivated_threshold).bitwise_and(is_crop_mask)

# we want these products
collections = [
    #"LANDSAT/LC08/C01/T1_SR",
    'NASA/ORNL/DAYMET_V4'
    #'ECMWF/ERA5/DAILY',
    # 'NASA/GLDAS/V021/NOAH/G025/T3H'
]

def make_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def ee_export_image_collection(
    ee_object, out_dir, scale=None, crs=None, region=None, file_per_band=False
):
    """Exports an ImageCollection as GeoTIFFs.
    Args:
        ee_object (object): The ee.Image to download.
        out_dir (str): The output directory for the exported images.
        scale (float, optional): A default scale to use for any bands that do not specify one; ignored if crs and crs_transform is specified. Defaults to None.
        crs (str, optional): A default CRS string to use for any bands that do not explicitly specify one. Defaults to None.
        region (object, optional): A polygon specifying a region to download; ignored if crs and crs_transform is specified. Defaults to None.
        file_per_band (bool, optional): Whether to produce a different GeoTIFF per band. Defaults to False.
    """

    if not isinstance(ee_object, ee.ImageCollection):
        print("The ee_object must be an ee.ImageCollection.")
        return

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    try:

        count = int(ee_object.size().getInfo())
        print("Total number of images: {}\n".format(count))

        for i in range(0, count):
            image = ee.Image(ee_object.toList(count).get(i))
            name = image.get("system:index").getInfo() + ".tif"
            filename = os.path.join(os.path.abspath(out_dir), name)
            if os.path.exists(filename):
                continue
            print("Exporting {}/{}: {}".format(i + 1, count, name))
            geemap.ee_export_image(
                image,
                filename=filename,
                scale=scale,
                crs=crs,
                region=region,
                file_per_band=file_per_band,
            )
            print("\n")

    except Exception as e:
        print(e)

def save_col(l):
    for a in l:
        print(a[1])
        ee_export_image_collection(a[0], out_dir=a[1], region=a[2], scale=50)
        break

cur_path = os.getcwd()
make_if_not_exists(os.path.join(cur_path, 'data'))

save_list = []

for fip_code, county_name in counties_dict.items():
    cname = county_name.replace(' ', '_')
    # make_if_not_exists(os.path.join(cur_path, 'data', f"{cname}"))
    # make_if_not_exists(os.path.join(cur_path, 'data', f"{cname}", f"{year}"))
    out_dir = os.path.join(cur_path, 'data', f"{cname}", "cdl.tif")
    # make_if_not_exists(out_dir)
    county_aoi = ee.FeatureCollection('TIGER/2018/Counties').filterMetadata('STATEFP', 'equals', f'{fip_header}').filterMetadata('COUNTYFP', 'equals', f'{(fip_code-fip_header*1000):03}').geometry()
    geemap.ee_export_image(final_mask, filename=out_dir, region=county_aoi, scale=20)

for year in range(start_year, end_year+1):
    _start_date = f"{year}-{start_date}"
    _end_date = f"{year}-{end_date}"
        # date_filter = (_start_date, _end_date)
    for collection in collections:
        for fip_code, county_name in counties_dict.items():
            cname = county_name.replace(' ', '_')
            make_if_not_exists(os.path.join(cur_path, 'data', f"{cname}"))
            make_if_not_exists(os.path.join(cur_path, 'data', f"{cname}", f"{year}"))
            out_dir = os.path.join(cur_path, 'data', f"{cname}", f"{year}", f"{collection.split('/')[-1]}")
            make_if_not_exists(out_dir)
            county_aoi = ee.FeatureCollection('TIGER/2018/Counties').filterMetadata('STATEFP', 'equals', f'{fip_header}').filterMetadata('COUNTYFP', 'equals', f'{(fip_code-fip_header*1000):03}').geometry()
            clipped_ic = ee.ImageCollection(collection).filterBounds(county_aoi).filterDate(_start_date, _end_date).map(
                lambda image : image.clip(county_aoi)) # .updateMask(final_mask))
#            save_col((clipped_ic, out_dir, county_aoi))
            save_list.append((clipped_ic, out_dir, county_aoi))

num_per_thread = int(math.ceil(len(save_list)/16))
print(num_per_thread)
new_list = [save_list[i:i+num_per_thread] for i in range(0, len(save_list), num_per_thread)]

pool = Pool(16)
pool.map(save_col, new_list)

# save_col(save_list)
