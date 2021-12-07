import os
import glob
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List, Tuple, Callable

from climate_resilience import utils

import warnings
warnings.formatwarning = utils.warning_format


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
        df_colnames = ["OBJECTID", "ID", "NameMnemonic", "StateCode"]
        
        # Iterate over all combinations of variables and scenarios
        for sce in scenarios:
            for var in variables:
                
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
                     suffixes=(None, "_copy"),
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
        df_colnames = ["OBJECTID", "ID", "NameMnemonic", "StateCode"]
        
        # Iterate over all combinations of variables and scenarios
        for sce in scenarios:
            for var in variables:
                # Verify if the column required for counts and amounts calculation is present in the df_pr DataFrame.
                historical_col_name = f"historical_{var}_percentile"
                if historical_col_name not in df_pr:
                    raise KeyError(f"{historical_col_name} column does not exist in the percentile data frame. Check the df_pr_csv_path argument.")
                
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
                     suffixes=(None, "_copy"),
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
        df_colnames = ["OBJECTID", "ID", "NameMnemonic", "StateCode"]

        # Iterate over all combinations of variables and scenarios
        for sce in scenarios:
            for var in variables:
                
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
                     suffixes=(None, "_copy"),
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


def get_per_year_stats(
    sites: pd.DataFrame, 
    scenarios: List[str], 
    variables: List[str], 
    datadir: str, 
) -> None:
    """Calculates the year-wise max, mean, and std of data for each site.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        scenarios (List[str]):  Scenarios of interest.
        variables (List[str]):  Variables of interest.
        datadir (str): Parent directory containing all the data files.
            The generated output file is also stored here.
    """
    # Create the output directory where the generated CSVs will be stored
    output_dir = os.path.join(datadir, "per_year_stats")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    else:
        warnings.warn(f"{output_dir} already exists! The generated CSVs will be added or overwritten in this directory.")
    
    # Iterating over all sites
    name_state_list = list(zip(sites.NameMnemonic, sites.StateCode))
    with tqdm(name_state_list) as tqdm_name_state_list:
        tqdm_name_state_list.set_description("LM Sites")

        for name, state in tqdm_name_state_list:
            df_array = []

            # Iterating over all combinations of scenarios and variables and 
            # concating data for all combinations in a single data frame
            df = pd.DataFrame()
            for sce in scenarios:
                for var in variables:
                    csv_path = os.path.join(datadir, f"{sce}_{var}_ensemble", f"{name}_{state}_{sce}_{var}.csv")
                    df_i = pd.read_csv(csv_path)
                    df_i = df_i.set_index("date")

                    if df.empty:
                        df = df_i
                    else:
                        df = pd.concat([df, df_i])

                    df.index = pd.to_datetime(df.index)

            # Calculating the year-wise max, mean, and std for the data
            max_val = df['mean'].groupby(pd.Grouper(freq='1Y')).max()
            mean_val = df['mean'].groupby(pd.Grouper(freq='1Y')).mean()
            std_val = df['mean'].groupby(pd.Grouper(freq='1Y')).std()

            # Adding data to the data frame array
            df_array.append(max_val)
            df_array.append(mean_val)
            df_array.append(std_val)

            # Converting data frame array to data frame
            df_pr = pd.DataFrame(np.array(df_array).T)
            df_pr.columns = ["maximum", "mean", "std"]
            df_pr.index = range(1950,2100)

            # Write to CSV file
            output_csv_path = os.path.join(output_dir, f"{name}_{state}_PMP.csv")
            df_pr.to_csv(output_csv_path)
    
    print(f"STATUS UPDATE: The CSVs generated from get_per_year_stats() function are stored in the '{output_dir}' directory.")
    

def get_sub_period_stats(
    sites: pd.DataFrame, 
    scenarios: List[str], 
    variables: List[str], 
    datadir: str, 
    date_ranges: List[Tuple[str]], 
    comp_function: str="gt", 
    get_stats: bool=True, 
    agg_function: Callable=None, 
    **kwargs: object
) -> None:
    """Calculates some stats within a specified date range.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        scenarios (List[str]):  Scenarios of interest.
        variables (List[str]):  Variables of interest.
        datadir (str): Parent directory containing all the data files.
            The generated output file is also stored here.
        date_ranges (List[Tuple[str]]): Each tuple contains a start date and 
            an end date as string in the format 'YYYY-MM' or 'YYYY-MM-DD'.
        comp_function (str, optional): Comparision function between the 
            aggregation function output and the date range values. 
            This is used to get stats. Defaults to 'gt' (greater).
            Options: 'eq' (equal) | 'gt' (greater) | 'lt' (lesser)
            Can be a callable as well but that can be implemented if needed.
        get_stats (bool, optional): Count and Amount values are calculated only 
            if this flag is set to True. Otherwise only the aggregation of 
            values between the dates is performed. 
            Defaults to True.
        agg_function (Callable, optional): This is the function that is used to 
            aggregate the data between the given time ranges. 
            Defaults to None, in which case 99th percentile is calculated. 
            All argument other than an input array can be passed as kwargs.
        kwargs (object, optional): All the parameters that are needed as input 
            for the agg_function can be passed in sequence at the end.
            Example: agg_function(data, **kwargs)
    
    Raises:
        ValueError: Raises this exception if the value of comp_function() is 
            anything other than the specified options.
        ValueError: Raises this exception if the input format or type of dates 
            in date_ranges is incorrect.
    """
    
    # If a default aggregation function is not provided, the 99th percentile is 
    # calculated for the data within the date range.
    if agg_function is None:
        agg_function = np.percentile
        kwargs["q"] = 99    # qth percentile for the percentile function
    
    # Checking the type and format of input date_ranges
    try:
        for start_date, end_date in date_ranges:
            pd.to_datetime(start_date)
            pd.to_datetime(end_date)
    except Exception as e:
        raise ValueError("The input format or type of the dates is incorrect. \
            Input is expected to be in the following format: \
            [('YYYY-MM-DD', 'YYYY-MM-DD'), ('YYYY-MM-DD', 'YYYY-MM-DD'), ...]\
            OR\
            [('YYYY-MM', 'YYYY-MM'), ('YYYY-MM', 'YYYY-MM'), ...]")
    
    # Declare variables that will be used to convert the processed data to a DataFrame
    df_array = []
    df_colnames = []
    
    # Generates a different CSV for each variables
    for var in variables:
        oid_id_name_state_list = list(zip(sites.OBJECTID, sites.ID, sites.NameMnemonic, sites.StateCode))
        with tqdm(oid_id_name_state_list) as tqdm_oid_id_name_state_list:
            tqdm_oid_id_name_state_list.set_description(f"Iterating LM Sites for '{var}' variable.")

            for _oid, _id, name, state in tqdm_oid_id_name_state_list:
                array_ind = [_oid, _id, name, state]
                df_colnames = ["OBJECTID", "ID", "NameMnemonic", "StateCode"]

                # Iterating over all combinations of scenarios and variables and 
                # concating data for all combinations in a single data frame
                df = pd.DataFrame()
                for sce in scenarios:
                    csv_path = os.path.join(datadir, f"{sce}_{var}_ensemble", f"{name}_{state}_{sce}_{var}.csv")
                    df_i = pd.read_csv(csv_path)
                    df_i = df_i.set_index("date")

                    if df.empty:
                        df = df_i
                    else:
                        df = pd.concat([df, df_i])

                    df.index = pd.to_datetime(df.index)

                # Extracting data for each date range
                for start_date, end_date in date_ranges:
                    date_range_idxs = df.index.to_series().between(start_date, end_date)
                    df_date_range = df[date_range_idxs]

                    # Aggregating the values for the date range and storing as a row in formation
                    agg_val = agg_function(df_date_range['mean'], **kwargs)
                    array_ind.append(agg_val)

                    # Update the column names
                    start_yr = pd.to_datetime(start_date).year
                    end_yr = pd.to_datetime(end_date).year
                    colname = f"{start_yr}_{end_yr}_{agg_function.__name__}"
                    if colname not in df_colnames:
                        df_colnames.append(colname)

                    # Calculate stats only if flagged
                    if get_stats:
                        # Define the query based on the comparison function 
                        if comp_function == "gt":
                            query = df_date_range['mean'] > agg_val
                        elif comp_function == "lt":
                            query = df_date_range['mean'] < agg_val
                        elif comp_function == "eq":
                            query = df_date_range['mean'] == agg_val
                        else:
                            raise ValueError("Incorrect value passed for the 'comp_function'. Expecting one of these three: 'eq' | 'gt' | 'lt'.")

                        delta_yrs = (end_yr - start_yr + 1)

                        # -----
                        # Count the number of values in comparison with the aggregated value
                        count = np.count_nonzero(query) / delta_yrs    # count per year - TODO: Ensure that this is fine because it generates the same counts for all the sites.
                        array_ind.append(count)

                        # Update the column names
                        colname = f"{start_yr}_{end_yr}_count_{comp_function}_{agg_function.__name__}"
                        if colname not in df_colnames:
                            df_colnames.append(colname)

                        # -----
                        # Get the mean of the values in comparison with the aggregated value
                        amount = np.sum(df_date_range["mean"][query]) / delta_yrs     # mean amount per year
                        array_ind.append(amount)

                        # Update the column names
                        colname = f"{start_yr}_{end_yr}_amount_{comp_function}_{agg_function.__name__}"
                        if colname not in df_colnames:
                            df_colnames.append(colname)

                # Store the row for conversion to DataFrame
                df_array.append(array_ind)

        # Converting data frame array to data frame
        df_sub_periods = pd.DataFrame(df_array)
        df_sub_periods.columns = df_colnames

        # Merge the generated data with the original Data Frame
        # if any duplicate column names are found, the first one will be left 
        # untouched and '_copy' will be appended to the other occurance.
        df_final = pd.merge(sites, df_sub_periods, 
                            how="inner", 
                            left_on=["OBJECTID", "ID"], 
                            right_on=["OBJECTID", "ID"],
                            suffixes=(None, "_copy"),
                           )

        # Write to CSV
        output_csv_path = os.path.join(datadir, f"{var}_sub_period_stats.csv")
        df_final.to_csv(output_csv_path)
        print(f"STATUS UPDATE: The output file generated from get_sub_period_stats() function is stored as {output_csv_path}.")
