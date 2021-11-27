import sys
sys.dont_write_bytecode = True

import pandas as pd
import numpy as np
import scipy 
from scipy import stats
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def calculate_Nth_percentile(sites, scenarios, variables, N=99):
    """ Calculates the Nth percentile and stores it as a new CSV file.
    Default value for N is 99.
    """
    var = 'tasmax'
    
    array = []
    for name, state in zip(sites.NameMnemonic,sites.StateCode):
        array_ind = [name, state]
        
        for sce in scenarios:
            csv_path = os.path.join(datadir, f"{sce}_{var}_ensemble", f"{name}_{state}_{sce}_{var}.csv")
            df = pd.read_csv(csv_path)
            
            df1 = df.set_index('date')
            
            mean_val = np.percentile(df1['mean'], N)  
            array_ind.append(mean_val)   
        
        array.append(array_ind)
    
    df_pr = pd.DataFrame(array)
    df_pr.columns = ['Name','State','historical', 'rcp45', 'rcp85']
    
    df_pr = pd.concat((sites, df_pr), axis=1)
    
    # Write to CSV
    output_csv_path = os.path.join(datadir, f"LMsites_tasmax_{N}th.csv")
    df_pr.to_csv(output_csv_path)


def calculate_pr_count_amount(sites, scenarios, variables):
    """Calculates pr count and amount.
    """
    var = 'tasmax'
    
    nyr_hist = 56    # QUESTION: fixed values or random values for experiment?
    nyr_proj = 93    # QUESTION: fixed values or random values for experiment?
    
    array = []
    i=0
    for name, state in zip(sites.NameMnemonic,sites.StateCode):
        array_ind = [name, state]
        for sce in scenarios:
            csv_path = os.path.join(datadir, f"{sce}_{var}_ensemble", f"{name}_{state}_{sce}_{var}.csv")
            df = pd.read_csv(csv_path)
            df1 = df.set_index('date')

            div_const = nyr_hist if sce == "historical" else nyr_proj
            count = np.count_nonzero(df1['mean'] > df_pr['historical'].iloc[i]) / div_const
            amount = np.mean(df1[df1['mean'] > df_pr['historical'].iloc[i]]['mean']) / div_const
            
            array_ind.append(count)
            array_ind.append(amount)
            
        array.append(array_ind)
        i+=1

    # Convert to DataFrame
    df_pr_counts_amounts = pd.DataFrame(array)
    df_pr_counts_amounts.columns = ['Name','State','historical_counts','historical_amount', 'rcp45_counts', 'rcp45_amount', 'rcp85_counts', 'rcp85_amount']
    df_pr_counts_amounts = pd.concat((sites, df_pr_counts_amounts), axis = 1)
    
    # Write to CSV
    output_csv_path = os.path.join(datadir, "LMsites_tasmax_counts_amounts.csv")
    df_pr_counts_amounts.to_csv(os.path.join(datadir, "LMsites_tasmax_counts_amounts.csv"))

    
def calculate_temporal_mean(sites, scenarios, variables):
    """Calculates mean between temporal ranges.
    """
    var = 'tasmax'
    
    array = []

    for name, state in zip(sites.NameMnemonic,sites.StateCode):
        array_ind = [name, state]

        for sce in scenarios:
            df = pd.read_csv(datadir + sce + '_' + var  + '_ensemble/' + name + '_' + state + '_' + sce + '_' + var + '.csv')

            df1 = df.set_index('date')

            if sce != 'historical':
                c0 = df1.index.to_series().between('2020-01', '2059-12')
                df2 = df1[c0]
                c1 = df1.index.to_series().between('2060-01', '2099-12')
                df3 = df1[c1]

                mean_val1 = np.mean(df2['mean'])  
                array_ind.append(mean_val1)   
                mean_val2 = np.mean(df3['mean'])
                array_ind.append(mean_val2)

            else:
                mean_val = np.mean(df1['mean'])  
                array_ind.append(mean_val)

        array.append(array_ind)

    df_pr = pd.DataFrame(array)
    df_pr.columns = ["Name", "State", "historical", "rcp45_near", "rcp45_far", "rcp85_near", "rcp85_far"]

    df_pr = pd.concat((sites, df_pr), axis=1)
    df_pr.to_csv(datadir+'LMsites_tasmax_99th_seg.csv')


def main():
    datadir = "."
    lmsites_path = os.path.join(datadir, "LMsites.csv")
    sites  = pd.read_csv(lmsites_path)
    
    variables  = ['tasmax']
    scenarios = ['historical', 'rcp45', 'rcp85']
    
    # Calculate 99th percentile
    calculate_Nth_percentile()
    
    # Calculate pr count and amount
    calculate_pr_count_amount()
    
    # Calculate temporal mean
    calculate_temporal_mean()


if __name__ == "__main__":
    main()