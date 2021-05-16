# ECE471 Final Project: Crop Yield Prediction
Presentation: [ppt](https://github.com/rlee360/PLaTYPI/blob/master/SPACY_%20Satellite%20Prediction%20of%20Aggregate%20Corn%20Yield.pptx)

Final Report: [report]()

The goal of our work was to predict locations that, should corn be planted there, increase aggregate yield without being biased by current crop locations. 

The main benefit of such a project is to predict locations for new corn farms in order to maximize yield. Our tool can also be used to analyze current corn farm locations and predict how much yield the farm generates (in bushels/acre). This is important in order to identify under/over-performing farms for investments of any future analysis using yield. 

**Two main concerns addressed:**
* Remaining unbiased by current crops and landscape
* Generating pixel-wise maps from coarse county-wise yield data

**Used Data:**
* [Yield: Historical Corn Yields by County in Iowa](https://www.extension.iastate.edu/agdm/crops/pdf/a1-12.pdf) - Reproduced as csv in [yield.csv](https://github.com/rlee360/PLaTYPI/blob/master/yield.csv)
* [Daymet V4: Daily Surface Weather and Climatological Summaries](https://developers.google.com/earth-engine/datasets/catalog/NASA_ORNL_DAYMET_V4)
* [ERA5 Daily aggregates - Latest climate reanalysis produced by ECMWF / Copernicus Climate Change Service](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_DAILY?hl=en)

## Proposed Model:
![model](/model.png)

## Resulting pixel-wise map for current crop locations in Calhoun, Iowa 2015
![yield prediction for Calhoun, Iowa](/crop_valid_2.png)
