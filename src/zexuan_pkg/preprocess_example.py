import sys
sys.dont_write_bytecode = True

import os
import pandas as pd
import numpy as np
import scipy 
from scipy import stats
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

import preprocess as pp


def main():
    datadir = "."
    lmsites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(lmsites_csv_path)

    scenarios = ["historical", "rcp45"]
    variables = ["tasmax"]
    pp.calculate_Nth_percentile(sites, scenarios, variables, datadir, N=99)

    df_pr_csv_path = os.path.join(datadir, "LMsites_99th_percentile.csv")
    pp.calculate_pr_count_amount(sites, scenarios, variables, datadir, df_pr_csv_path)

    start_date = "2020-01-05"
    end_date = "2059-12-09"
    pp.calculate_temporal_mean(sites, scenarios, variables, datadir, start_date, end_date)


if __name__ == "__main__":
    main()
