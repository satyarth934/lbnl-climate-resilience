import sys
sys.dont_write_bytecode = True

import os
import time
import pandas as pd
import numpy as np
import glob
import geopandas as gpd
import datetime
from pprint import pprint
from tqdm import tqdm
import warnings

from typing import List, Tuple, Callable
import utils


if __name__ == "__main__":
    datadir = "/global/scratch/satyarth/Projects/lbnl-zexuan-code/data"
    sites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(sites_csv_path)
    