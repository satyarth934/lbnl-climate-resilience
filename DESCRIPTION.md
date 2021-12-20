# lbnl-climate-resilience

[pip package](https://pypi.org/project/climate-resilience/)

---
## [Download Examples](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/examples/climate-resilience/download_example.py)
This file requires a [`download_params.yml`](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/examples/climate-resilience/download_params.yml) file to specify the download configurations.

We cannot directly download the data from the Google Earth Engine directly onto the local machine. So the best option is to download to the drive and then download that data to the local drive.

---
## [Preprocess Examples](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/examples/climate-resilience/preprocess_example.py)
The preprocessing functions will expect that the local data drive contains the downloaded data.

If the data is on drive, the drive needs to be mounted. 
This is easier to do in a google colab session. Once the drive is mounted, the path of the mounted drive can be used with the functions as normal.

#### Expected file and directory structure:
The input file and directory structure for functions `calculate_Nth_percentile()`, `calculate_pr_count_amount()`, and `calculate_temporal_mean()` in the [preprocessing code](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/src/climate_resilience/preprocess.py) should be as follows:
```
datadir
├── scenario1_variable1_ensemble
│   ├── name1_state1_scenario1_variable1.csv
│   └── name2_state2_scenario1_variable1.csv
├── scenario1_variable2_ensemble
│   ├── name1_state1_scenario1_variable2.csv
│   └── name2_state2_scenario1_variable2.csv
├── scenario2_variable1_ensemble
│   ├── name1_state1_scenario2_variable1.csv
│   └── name2_state2_scenario2_variable1.csv
└── scenario2_variable2_ensemble
    ├── name1_state1_scenario2_variable2.csv
    └── name2_state2_scenario2_variable2.csv
```

---
## [Visualization Examples](https://github.com/satyarth934/lbnl-climate-resilience/tree/main/notebooks/climate-resilience)
The visualization code will be easier to be used in a notebook as inline visualizations can be used.



#### [Map visualization notebook](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/notebooks/climate-resilience/visualize_example_1.ipynb)

Below is a screenshot of the interactive map with the sites marked.

![Map](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/notebooks/climate-resilience/sample_map_screenshot.png?raw=true)

![Map Colorbar](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/notebooks/climate-resilience/sample_map_colorbar.png?raw=true)



#### [Box plot visualization notebook](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/notebooks/climate-resilience/visualize_example_3.ipynb)

Below is a screenshot of boxplot of annual precipitation in different regions of the United States.

![Boxplot](https://github.com/satyarth934/lbnl-climate-resilience/blob/main/notebooks/climate-resilience/sample_boxplot.png?raw=true)
