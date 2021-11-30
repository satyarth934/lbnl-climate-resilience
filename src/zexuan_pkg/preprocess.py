import sys
sys.dont_write_bytecode = True

import os
import glob
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm

from typing import List


def calculate_Nth_percentile(
    sites: pd.DataFrame, 
    scenarios: List[str], 
    variables: List[str], 
    datadir: str, 
    N: int=99,
) -> None:
    """Calculates the Nth percentile.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        scenarios (List[str]):  Scenarios of interest.
        variables (List[str]):  Variables of interest.
        datadir (str): Parent directory containing all the data files.
            The generated output file is also stored here.
        N (int): Nth percentile will be calculated.
    
    Returns:
        pd.DataFrame: The output DataFrame that is written to a csv file is also returned.
        
    Raises:
        ValueError: If the integer value of N is outside the range [0, 100].
    """
    
    # Verify the value of N
    if N < 0 or N > 100:
        raise ValueError("Incorrect value for N. N must be between 0 and 100.")
    
    # Declare variables that will be used to convert the processed data to a DataFrame
    df_array = []
    df_colnames = []
    
    # Loop over all the sites. 
    # ID and Object ID are stored only to inspect the final result with the corresponding site
    for _oid, _id, name, state in zip(sites.OBJECTID, sites.ID, sites.NameMnemonic, sites.StateCode):
        array_ind = [_oid, _id, name, state]
        df_colnames = ["OBJECTID", "ID", "Name", "State"]
        
        # Iterate over all combinations of variables and scenarios
        for sce in scenarios:
            for var in variables:
                # TODO: Should these filenames be something else? 
                # These do not match the download script filenaming format.
                csv_path = os.path.join(datadir, 
                                        f"{sce}_{var}_ensemble", 
                                        f"{name}_{state}_{sce}_{var}.csv")
                
                if not os.path.exists(csv_path):
                    print(f"WARNING: {csv_path} does not exist. Continuing to the next file.")
                    continue
                
                # Preprocessing step
                df = pd.read_csv(csv_path)
                df1 = df.set_index('date')
                
                mean_val = np.percentile(df1['mean'], N)  
                
                # Update the column names
                colname = f"{sce}_{var}_percentile"
                if colname not in df_colnames:
                    df_colnames.append(colname)
                
                # Store the row information
                array_ind.append(mean_val)
        
        # Store the row for conversion to DataFrame
        df_array.append(array_ind)
    
    # Convert the generated data to a DataFrame
    df_pr = pd.DataFrame(df_array)
    df_pr.columns = df_colnames
    
    # Merge the generated data with the original Data Frame
    df_pr = pd.merge(sites, df_pr, 
                     how="inner", 
                     left_on=["OBJECTID", "ID"], 
                     right_on=["OBJECTID", "ID"],
                    )
    
    # Write to CSV
    output_csv_path = os.path.join(datadir, f"LMsites_{N}th_percentile.csv")
    df_pr.to_csv(output_csv_path)
    print(f"STATUS UPDATE: The output file generated from calculate_Nth_percentile() function is stored as {output_csv_path}.")
    
    return df_pr
    

def calculate_pr_count_amount(
    sites: pd.DataFrame, 
    scenarios: List[str], 
    variables: List[str], 
    datadir: str, 
    df_pr_csv_path: str
) -> None:
    """Calculates precipitation count and amount.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        scenarios (List[str]): Scenarios of interest.
        variables (List[str]): Variables of interest.
        datadir (str): Parent directory containing all the data files.
            The generated output file is also stored here.
        df_pr_csv_path (str): This data frame can be generated using the calculate_Nth_percentile() function.
            The csv file generated from this function is passed here as argument.
    
    Returns:
        pd.DataFrame: The output DataFrame that is written to a csv file is also returned.
    
    Raises:
        KeyError: This error is raised if the correct historical column does not 
            exist in the df_pr data frame that is mentioned in df_pr_csv_path.
    """
    
    nyr_hist = 56    # QUESTION: fixed values or random values for experiment?
    nyr_proj = 93    # QUESTION: fixed values or random values for experiment?
    
    # df_pr is required to calculate counts and amounts greater than 'historical' values
    df_pr = pd.read_csv(df_pr_csv_path)
    
    # Declare variables that will be used to convert the processed data to a DataFrame
    df_array = []
    df_colnames = []
    
    # Loop over all the sites. 
    # ID and Object ID are stored only to inspect the final result with the corresponding site
    i=0
    for _oid, _id, name, state in zip(sites.OBJECTID, sites.ID, sites.NameMnemonic, sites.StateCode):
        array_ind = [_oid, _id, name, state]
        df_colnames = ["OBJECTID", "ID", "Name", "State"]
        
        # Iterate over all combinations of variables and scenarios
        for sce in scenarios:
            for var in variables:
                # Verify if the column required for counts and amounts calculation is present in the df_pr DataFrame.
                historical_col_name = f"historical_{var}_percentile"
                if historical_col_name not in df_pr:
                    raise KeyError(f"{historical_col_name} column does not exist in the percentile data frame. Check the df_pr_csv_path argument.")
                
                # TODO: Should these filenames be something else? 
                # These do not match the download script filenaming format.
                csv_path = os.path.join(datadir, 
                                        f"{sce}_{var}_ensemble", 
                                        f"{name}_{state}_{sce}_{var}.csv")
                
                if not os.path.exists(csv_path):
                    print(f"WARNING: {csv_path} does not exist. Continuing to the next file.")
                    continue
                
                # Preprocessing step
                df = pd.read_csv(csv_path)
                df1 = df.set_index('date')

                div_const = nyr_hist if sce == "historical" else nyr_proj
                count = np.count_nonzero(df1['mean'] > df_pr[historical_col_name].iloc[i]) / div_const
                amount = np.mean(df1[df1['mean'] > df_pr[historical_col_name].iloc[i]]['mean']) / div_const

                # Update the column names and store the row information
                colname = f"{sce}_{var}_counts"
                if colname not in df_colnames:
                    df_colnames.append(colname)
                array_ind.append(count)
                
                colname = f"{sce}_{var}_amount"
                if colname not in df_colnames:
                    df_colnames.append(colname)
                array_ind.append(amount)
        
        # Store the row for conversion to DataFrame
        df_array.append(array_ind)
        i+=1

    # Convert the generated data to a DataFrame
    df_pr_counts_amounts = pd.DataFrame(df_array)
    df_pr_counts_amounts.columns = df_colnames
    
    # Merge the generated data with the original Data Frame
    df_pr = pd.merge(sites, df_pr_counts_amounts, 
                     how="inner", 
                     left_on=["OBJECTID", "ID"], 
                     right_on=["OBJECTID", "ID"],
                    )
    
    # Write to CSV
    output_csv_path = os.path.join(datadir, "LMsites_counts_amounts.csv")
    df_pr_counts_amounts.to_csv(output_csv_path)
    print(f"STATUS UPDATE: The output file generated from calculate_pr_count_amount() function is stored as {output_csv_path}.")    
    
    return df_pr_counts_amounts
    

def calculate_temporal_mean(
    sites: pd.DataFrame, 
    scenarios: List[str], 
    variables: List[str], 
    datadir: str, 
    start_date: str, 
    end_date: str
) -> None:
        
    """Calculates mean precipitation for the 'historical' scenario or 
    between the start_date and the end_date.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        scenarios (List[str]): Scenarios of interest.
        variables (List[str]): Variables of interest.
        datadir (str): Parent directory containing all the data files.
            The generated output file is also stored here.
        start_date (str): Must be in the format 'YYYY-MM' or 'YYYY-MM-DD'.
        end_date (str): Must be in the format 'YYYY-MM' or 'YYYY-MM-DD'.
    
    Returns:
        pd.DataFrame: The output DataFrame that is written to a csv file is also returned.
        
    """

    # Declare variables that will be used to convert the processed data to a DataFrame
    df_array = []
    df_colnames = []

    # Loop over all the sites. 
    # ID and Object ID are stored only to inspect the final result with the corresponding site
    for _oid, _id, name, state in zip(sites.OBJECTID, sites.ID, sites.NameMnemonic, sites.StateCode):
        array_ind = [_oid, _id, name, state]
        df_colnames = ["OBJECTID", "ID", "Name", "State"]

        # Iterate over all combinations of variables and scenarios
        for sce in scenarios:
            for var in variables:
                # TODO: Should these filenames be something else? 
                # These do not match the download script filenaming format.
                csv_path = os.path.join(datadir, 
                                        f"{sce}_{var}_ensemble", 
                                        f"{name}_{state}_{sce}_{var}.csv")
                
                if not os.path.exists(csv_path):
                    print(f"WARNING: {csv_path} does not exist. Continuing to the next file.")
                    continue
                
                # Preprocessing step
                df = pd.read_csv(csv_path)
                df1 = df.set_index('date')
                
                # 'historial' scenario dates from 1950 to 2006.
                if sce != 'historical':
                    c0 = df1.index.to_series().between(start_date, end_date)
                    df2 = df1[c0]
                    mean_val = np.mean(df2['mean'])  
                    
                    # Generate column names
                    colname = f"{start_date}_{end_date}_{var}_mean"

                else:
                    mean_val = np.mean(df1['mean'])
                    
                    # Generate column names
                    colname = f"{sce}_{var}_mean"
                
                # Update the column names
                if colname not in df_colnames:
                    df_colnames.append(colname)
                
                # Store the row information
                array_ind.append(mean_val)

        # Store the row for conversion to DataFrame
        df_array.append(array_ind)

    # Convert the generated data to a DataFrame
    df_pr = pd.DataFrame(df_array)
    df_pr.columns = df_colnames
    
    # Merge the generated data with the original Data Frame
    df_pr = pd.merge(sites, df_pr, 
                     how="inner", 
                     left_on=["OBJECTID", "ID"], 
                     right_on=["OBJECTID", "ID"],
                    )

    # Write to CSV
    output_csv_path = os.path.join(datadir, "LMsites_seg.csv")
    df_pr.to_csv(output_csv_path)
    print(f"STATUS UPDATE: The output file generated from calculate_temporal_mean() function is stored as {output_csv_path}.")    
    
    return df_pr


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
        tqdm_name_state_list.set_description("LM Sites")
        
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
    
    print(f"STATUS UPDATE: The CSVs generated from get_climate_ensemble() function are stored in the '{output_dir}' directory.")


############################
# NOTES
############################
"""
Questions:
1. Is the sites csv file expected to be on local drive?
2. Are the downloaded csv files expected to by on the local drive as well?
3. Is it assumed that the data will be downloaded locally from drive? - [My guess: YES]
4. Where is the "*_ensemble*" file downloaded from?
5. The variable nyr_hist and nyr_proj, are the supposed to have a fixed value or are they experimental?
6. Confirm if ObjectID and ID are good unique identifiers for each row.

Tasks:
1. Do not worry about drive or local file downloads.
    It is for the user to worry about. 
    Just the function would be from the library that can be used either in colab for drive files or on local machine.
    The directory path would work the same for both the cases.
"""