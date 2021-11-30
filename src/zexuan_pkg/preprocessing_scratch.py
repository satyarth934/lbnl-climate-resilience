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





        
if __name__ == "__main__":
    datadir = "/global/scratch/satyarth/Projects/lbnl-zexuan-code/data"
    sites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(sites_csv_path)
    
    scenarios = ["historical"]
    variables = ["pr"]
    
    get_climate_ensemble(sites, scenarios, variables, datadir)