# lbnl-climate-resilience

[pip package](https://pypi.org/project/climate-resilience/)

---
## Download [Examples](./examples/climate-resilience/download_example.py)
We cannot directly download the data from the Google Earth Engine directly onto 
the local machine. So the best option is to download to the drive and then 
download that data to the local drive.

---
## Preprocess [Examples](./examples/climate-resilience/preprocess_example.py)
The preprocessing functions will expect that the local data drive contains the 
downloaded data.

If the data is on drive, the drive needs to be mounted. This is easier to do in 
a google colab session. Then the path of the mounted drive can be used with the 
functions as normal.

#### Expected file and directory structure:
The input file and directory structure for functions `calculate_Nth_percentile()`, `calculate_pr_count_amount()`, and `calculate_temporal_mean()` in the [preprocessing code](./src/climate_resilience/preprocess.py) should be as follows:
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
## Visualize Examples [1](./notebooks/climate-resilience/visualize_example_1.ipynb), [2](./notebooks/climate-resilience/visualize_example_2.ipynb), and [3](./notebooks/climate-resilience/visualize_example_3.ipynb)
The visualization code will be easier to be used in a notebook as inline 
visualizations can be used.

The sample map that is generated from the visualization code can be viewed [here](./link/to/be/updated).