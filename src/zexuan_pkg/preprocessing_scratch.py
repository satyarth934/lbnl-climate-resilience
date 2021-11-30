import sys
sys.dont_write_bytecode = True

import os
import pandas as pd
import numpy as np
import glob
import geopandas as gpd
import datetime
from pprint import pprint
from tqdm import tqdm

from typing import List
import utils


def get_climate_ensemble(
    sites: pd.DataFrame, 
    scenarios: List[str], 
    variables: List[str], 
    datadir: str, 
) -> None:
    """Calculates the mean and std of data for each site.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        scenarios (List[str]):  Scenarios of interest.
        variables (List[str]):  Variables of interest.
        datadir (str): Parent directory containing all the data files.
            The generated output file is also stored here.
    """
    # Create the output directory where the generated CSVs will be stored
    output_dir = os.path.join(datadir, "climate_ensemble")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    # Iterating over all sites
    name_state_list = list(zip(sites.NameMnemonic, sites.StateCode))
    with tqdm(name_state_list) as tqdm_name_state_list:
        tqdm_name_state_list.set_description("Sites")
        
        for name, state in tqdm_name_state_list:

            # Iterating over all combinations of scenarios and variables
            for scenario in scenarios:
                for variable in variables:

                    filepath_format = os.path.join(datadir, f"{scenario}_{variable}", f"{name}_{state}*.csv")
                    all_files = glob.glob(filepath_format)

                    # Iterating over all_files to create a single data frame of mean values of all the models
                    for i, filename in enumerate(all_files):
                        if i == 0:
                            df = pd.read_csv(filename, index_col=None, header=0)
                        else:
                            df[str(i)] = pd.read_csv(filename, index_col=None, header=0).iloc[:, 1]

                    # Creating a new data frame that contains the ensemble mean and std values
                    df2 = pd.DataFrame()

                    start_date = datetime.date(1950, 1, 1)    # TODO: Ideally this should be read from the CSV file but the date in the CSV file seems incorrect.
                    end_date = start_date + datetime.timedelta(days=len(df)-1)    # TODO: Ideally this should be read from the CSV file but the date in the CSV file seems incorrect.
                    df2["date"] = pd.date_range(start_date, end_date)

                    df2["mean"] = df.mean(axis=1, numeric_only=True)    # avoids the date column
                    df2["std"] = df.std(axis=1, numeric_only=True)    # avoids the date column

                    output_csv_path = os.path.join(output_dir, f"{name}_{state}_{scenario}_{variable}.csv")
                    df2.to_csv(output_csv_path)
                    # print(f"STATUS UPDATE: The output file is stored as {output_csv_path}.")

        
if __name__ == "__main__":
    datadir = "/global/scratch/satyarth/Projects/lbnl-zexuan-code/data"
    sites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(sites_csv_path)
    
    scenarios = ["historical"]
    variables = ["pr"]
    
    get_climate_ensemble(sites, scenarios, variables, datadir)