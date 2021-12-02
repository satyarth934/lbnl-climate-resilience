import sys
sys.dont_write_bytecode = True

import os
import pandas as pd
import numpy as np
import scipy 
from scipy import stats
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

import utils
import preprocess as pp


def main():
    datadir = "/global/scratch/satyarth/Projects/lbnl-zexuan-code/data"
    lmsites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(lmsites_csv_path)

    scenarios = ["historical", "rcp45"]
    variables = ["tasmax"]
    with utils.ExecTimeCM("calculate_Nth_percentile()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.calculate_Nth_percentile(sites, scenarios, variables, datadir, N=99)

    df_pr_csv_path = os.path.join(datadir, "LMsites_99th_percentile.csv")
    with utils.ExecTimeCM("calculate_pr_count_amount()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.calculate_pr_count_amount(sites, scenarios, variables, datadir, df_pr_csv_path)

    start_date = "2020-01-05"
    end_date = "2059-12-09"
    with utils.ExecTimeCM("calculate_temporal_mean()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.calculate_temporal_mean(sites, scenarios, variables, datadir, start_date, end_date)

    scenarios = ["historical"]
    variables = ["pr"]    
    with utils.ExecTimeCM("get_climate_ensemble()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.get_climate_ensemble(sites, scenarios, variables, datadir)
    
    scenarios = ["historical", "rcp45", "rcp85"]
    variables = ["pr"]
    with utils.ExecTimeCM("get_per_year_stats()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.get_per_year_stats(sites, scenarios, variables, datadir)
        
    scenarios = ["historical", "rcp45", "rcp85"]
    variables = ["pr"]
    date_ranges = [
        ('1950-01', '1989-12'),
        ('1990-01', '2019-12'),
        ('2020-01', '2059-12'),
        ('2060-01', '2099-12'),
    ]
    with utils.ExecTimeCM("get_sub_period_stats()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.get_sub_period_stats(sites, scenarios, variables, datadir, date_ranges, comp_function="gt", agg_function=None, get_stats=True)
    

if __name__ == "__main__":
    main()
