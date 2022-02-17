import sys
sys.dont_write_bytecode = True

import os
import scipy 
import argparse
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from climate_resilience import utils
from climate_resilience import preprocess as pp


def parse_arguments() -> argparse.Namespace:
    """Reads commandline arguments and returns the parsed object.
    
    Returns:
        argparse.Namespace: parsed object containing all the input arguments.
    """
    parser = argparse.ArgumentParser(
        description="Sample usage of preprocessing functions.",
        fromfile_prefix_chars="@",  # helps read the arguments from a file.
    )
    
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument(
        "-d",
        "--data_dir",
        type=str,
        required=True,
        help="Path to the directory containing all the data files. The output files will be written here as well.",
    )
    
    args, unknown = parser.parse_known_args()

    # print("--- args ---")
    # print(args)

    return args


def main():
    
    args = parse_arguments()
    
    datadir = args.data_dir    # Path to the data directory within this git repo '../../../data'.
    lmsites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(lmsites_csv_path)

    scenarios = ["historical", "rcp45"]
    variables = ["pr"]
    models = ['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM']
    with utils.ExecTimeCM("calculate_Nth_percentile()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.calculate_Nth_percentile(sites, scenarios, variables, datadir, N=99, mean_thresh=0.1, models=models)

    df_pr_csv_path = os.path.join(datadir, "LMsites_99th_percentile.csv")
    with utils.ExecTimeCM("calculate_pr_count_amount()") as et:    # This line is not required to run the function. It is only used to check the function's execution time.
        pp.calculate_pr_count_amount(sites, scenarios, variables, datadir, df_pr_csv_path, models=models)

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
