# ECE471 Final Project: Crop Yield Prediction
Presentation: [ppt](https://github.com/rlee360/PLaTYPI/blob/master/SPACY_%20Satellite%20Prediction%20of%20Aggregate%20Corn%20Yield.pptx)

Final Report: [report]()

The goal of our work was to predict locations that, should corn be planted there, increase aggregate yield without being biased by current crop locations. 

The main benefit of such a project is to predict locations for new corn farms in order to maximize yield. Our tool can also be used to analyze current corn farm locations and predict how much yield the farm generates (in bushels/acre). This is important in order to identify under/over-performing farms for investments of any future analysis using yield. 

**Two main concerns addressed:**
* Remaining unbiased by current crops and landscape
* Generating pixel-wise maps from coarse county-wise yield data

## Proposed Model:
![model](/model.png)

## Resulting Pixel-wise map of Calhoun, Iowa for current crop locations
![yield prediction for Calhoun, Iowa](/crop_valid_2.png)
