![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)

# SPACY - Satellite Prediction of Aggregate Corn Yield
****ECE471 Final Project: Crop Yield Prediction****

Presentation: [ppt](https://github.com/rlee360/PLaTYPI/blob/master/SPACY_%20Satellite%20Prediction%20of%20Aggregate%20Corn%20Yield.pptx)

Report: [report](https://github.com/rlee360/PLaTYPI/blob/master/ECE471_Final_Paper.pdf)

[SPACY](https://github.com/rlee360/PLaTYPI) is a tool to predict pixel-wise corn yield independently of current land cover usage through the use of histograms. 
It is authored by [Richard Lee](https://github.com/rlee360) and [Yuval Ofek](https://github.com/yuvalofek). 

## Introduction:

The goal of this work is to predict locations that, should corn be planted there, increase aggregate yield without being biased by current crop locations. 

The main benefit of such a project is to predict locations for new corn farms in order to maximize yield. The tool can also be used to analyze current corn farm locations and predict how much yield the farm generates (in bushels/acre). This is important in order to identify under/over-performing farms and farm locations for investments of any future yield analysis. 

**Two main concerns are addressed:**
* Remaining unbiased by current crops and landscape
* Generating pixel-wise maps from coarse county-wise yield data

**Used Data:**
* [Yield: Historical Corn Yields by County in Iowa](https://www.extension.iastate.edu/agdm/crops/pdf/a1-12.pdf) - Reproduced as csv in [yield.csv](https://github.com/rlee360/PLaTYPI/blob/master/yield.csv)
* [Daymet V4: Daily Surface Weather and Climatological Summaries](https://developers.google.com/earth-engine/datasets/catalog/NASA_ORNL_DAYMET_V4)
* [ERA5 Daily aggregates - Latest climate reanalysis produced by ECMWF / Copernicus Climate Change Service](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_DAILY?hl=en)

**Primary Tools:**
* Google Earth Engine Python API
* Numpy
* Multiprocessing 
* 

## Results

|| MAE | MSE|
| --- | --- | --- |
| Baseline| 20.637 | 734.300  |
| Ours    | 10.703 | 203.604  |

### Pixel-wise yield prediction for counties
<p align="center">
  <img src='/crop_valid_2.png' alt='pixel-wise yield prediction for Calhoun, Iowa, in 2015' width=480>
  <br>
  <sup>Pixel-wise yield prediction (in bushels/acre) for Calhoun, Iowa using 2015 data</sup>
</p>

## Code File Breakdown:
* **download_from_ee.py -**
Parallelizes file download from google earth engine - loops over year, image collection, county and downloads
* **counties.py -**
returns the FPS code for each county in Iowa in a dict (FPS code: county)
* **make_hists.py -**
For each county-year pair downloaded, generates a spatial-temporal histogram of the data
* **make_one_county.py -**
For testing, generates a temporal histogram for each pixel in a specified county-year pair
* **Masked_Yield_Prediction_PoC.ipynb -**
Takes yield data and histogram, preprocesses data, generates and trains a tf model (see proposed model), saves model, and then evaluates model on one-county's pixel-wise temporal histograms
* **proof_of_concept.ipynb -**
An attempt to create histograms directly from google earth engine API - NOT FUNCTIONING
* **proof_of_concept_2.ipynb -**
Another attempt to to create histograms directly from google earth engine API, somewhat limited and slow (and susceptible to crs of image collections). 

<p align="center">
  <img src='/model.png' alt='proposed model' width=480>
  <br>
  <sup>Proposed model plotted</sup> 
</p>




