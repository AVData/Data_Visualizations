
# Sleep Quality App Analysis

The primary aim of this project was to obtain answers focused on a specific question regarding sleeping habits over time.  Hence, the repo was created to perform analysis and generate visualizations from data collected by the [sleep cycle app](https://www.sleepcycle.com).

The Sleep Cycle app collects information based on your sleeping habits; my analysis attempts to extract more tailored insight from the available data.  If you would like a brief view of the results and hypothesis questions posed, take a look at my [medium blog post](https://medium.com/@mydata/my-sleeping-habits-over-the-past-year-90d08aa36a46).

## Table of Contents
- [Data exploration notebooks](https://github.com/AVData/SleepQuality_app_analysis/tree/master/exploratory)
- [Wrangle function created to process data](https://github.com/AVData/SleepQuality_app_analysis/tree/master/wrangle)
- [Visualization function provides visualizations given a split date](https://github.com/AVData/SleepQuality_app_analysis/tree/master/visualizations)
- [Raw data from app](https://github.com/AVData/SleepQuality_app_analysis/tree/master/raw_data)

## Usage

Open the Sleep Cycle app (v6.9), to go the profile tab:
- `settings > (Statistics) Database`

When in the Database, press the `Export database` link.

Your data will be emailed to the associated email address as a .CSV file.  That .CSV file is what will be used in this analysis.

Git clone this repo, and in a new jupyter notebook (within the same directory) import the [wrangle_function](https://github.com/AVData/SleepQuality_app_analysis/tree/master/wrangle).  Use the wrangle function to process your data.  To do this, use the name of the CSV file as argument in the function.  (Note: if the CSV file is named filename.CSV, the argument in the function should only be the string 'filename')

The wrangle function will process your data and generate:
- `t-test value`
- `p-value`
- `DataFrame`

Use the following example as template to execute and generate statistics and a cleaned DataFrame:

CSV File: `sleepdata.csv`

```python
from wrangle import wrangle_function

t_stat, p_value, sleepdata_df = wrangle_function('sleepdata')
```

Notes on visualizations to come.

![](https://github.com/AVData/SleepQuality_app_analysis/blob/master/visualizations/all_time_in_bed_dist.png?raw=true)

Keep in mind that I will continue to grow this analysis, as more things become available, namely step tracker, and heart rate monitoring device.
