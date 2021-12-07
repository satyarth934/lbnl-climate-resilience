import os
import itertools
import numpy as np
import pandas as pd
from tqdm import tqdm
import geopandas as gpd
from typing import List
from pprint import pprint
from datetime import datetime, timedelta

import ee
from eecmip5 import eecmip5 as cmip5
# from google.auth import compute_engine

from joblib import Parallel, delayed
parallel_function = Parallel(n_jobs=-1, verbose=5)

from climate_resilience import utils
from climate_resilience import constants as C
# import utils
# import constants as c


class SitesDownloader:
    def __init__(self, folder: str, site_json_file_path: str) -> None:
        """Initializes the SitesDownloader object.
        
        Args:
            folder (str): Prefix of the output folder on google drive.
            site_json_file_path (str): Path to the json file containing the 
                site information for downloading data.
        """
        
        self.folder = folder
        
        self.site_json_file_path = site_json_file_path
        self.sites = gpd.read_file(self.site_json_file_path)


    def download_model_average_daily(self, start_date: datetime, end_date: datetime, variable: str, scenario: str, geom: ee.Geometry.Point, name: str, state: str) -> ee.batch.Task:
        """Download average daily data.
        
        Args:
            start_date (datetime): Starting date of the dataset to download. 
                Format: YYYY-MM-DD
            end_date (datetime): Ending date of the dataset to download.
                Format: YYYY-MM-DD
            variable (str): Variable of interest.
            scenario (str): Scenario of interest.
            geom (ee.Geometry.Point): Site location in latitude and longitude.
            name (str): Name Mnemonic of the site.
            state (str): Site location state code.
        
        Returns:
            ee.batch.Task: Returns the google earth engine task that performs the download process.
                Not necessaily useful for basic download commands.
        """
        
        if variable not in C.CONST:
            raise ValueError("Incorrect variable.")
            
        # Get CMIP5 image collection
        CMIP5 = ee.ImageCollection('NASA/NEX-GDDP') \
                    .filterDate(start_date, end_date) \
                    .select(variable) \
                    .filter(ee.Filter.eq('scenario', scenario)) \

        timeseries = ee.FeatureCollection(CMIP5.map(lambda img: img.multiply(C.CONST[variable]["multiply"]) \
                                                                    .add(C.CONST[variable]["add"]) \
                                                                    .reduceRegions(geom, ee.Reducer.mean(), 500) \
                                                                    .first() \
                                                   )
                                         )
        
        # Possible destinations for the downloaded files: 
        # toDrive; toCloud; toAsset. We can add support for other destinations later as and when needed.
        desc_name = f"{name}_{state}_{scenario}_{variable}_daily"
        my_task = ee.batch.Export.table.toDrive(
                            collection = timeseries,
                            fileFormat='csv',
                            folder = os.path.join(self.folder, scenario, variable),
                            description = desc_name
                            #selectors=['date','mean']
                            )
        
        my_task.start()
        print(f"Downloading... {desc_name}")
        return my_task

    
    def download_historical_daily(self, start_date: datetime, end_date: datetime, variable: str, scenario: str, model: str, geom: ee.Geometry.Point, name: str, state: str) -> ee.batch.Task:
        """Download daily data.
        
        Args:
            start_date (datetime): Starting date of the dataset to download. 
                Format: YYYY-MM-DD
            end_date (datetime): Ending date of the dataset to download.
                Format: YYYY-MM-DD
            variable (str): Variable of interest.
            scenario (str): Scenario of interest.
            model (str): Model of interest.
            geom (ee.Geometry.Point): Site location in latitude and longitude.
            name (str): Name Mnemonic of the site.
            state (str): Site location state code.
        
        Returns:
            ee.batch.Task: Returns the google earth engine task that performs the download process.
                Not necessaily useful for basic download commands.
        """
        
        if variable not in C.CONST:
            raise ValueError("Incorrect variable.")
        
        # Get CMIP5 image collection
        CMIP5 = ee.ImageCollection('NASA/NEX-GDDP') \
                  .filterDate(start_date, end_date) \
                  .select(variable) \
                  .filter(ee.Filter.eq('scenario', scenario)) \
                  .filter(ee.Filter.eq('model', model))

        timeseries = ee.FeatureCollection(CMIP5.map(lambda img: img.multiply(C.CONST[variable]["multiply"]) \
                                                                    .add(C.CONST[variable]["add"]) \
                                                                    .reduceRegions(geom,ee.Reducer.mean(),500) \
                                                                    .first() \
                                                                    .set('date', ee.Date(img.date()).format('YYYY-MM-DD')) \
                                                   )
                                         )
        
        # Possible destinations for the downloaded files: 
        # toDrive; toCloud; toAsset. We can add support for other destinations later as and when needed.
        desc_name = f"{name}_{state}_{scenario}_{variable}_{model}"
        my_task = ee.batch.Export.table.toDrive(
                            collection = timeseries,
                            fileFormat='csv',
                            folder = os.path.join(self.folder, scenario, variable),
                            description = desc_name,
                            selectors=['date','mean'])
        my_task.start()
        print(f"Downloading... {self.folder} {desc_name}")
        return my_task


    def download_historical_monthly(self, start_date: datetime, end_date: datetime, variable: str, scenario: str, model: str, geom: ee.Geometry.Point, name: str, state: str) -> ee.batch.Task:
        """Download monthly data.
        
        Args:
            start_date (datetime): Starting date of the dataset to download. 
                Format: YYYY-MM-DD
            end_date (datetime): Ending date of the dataset to download.
                Format: YYYY-MM-DD
            variable (str): Variable of interest.
            scenario (str): Scenario of interest.
            model (str): Model of interest.
            geom (ee.Geometry.Point): Site location in latitude and longitude.
            name (str): Name Mnemonic of the site.
            state (str): Site location state code.
        
        Returns:
            ee.batch.Task: Returns the google earth engine task that performs the download process.
                Not necessaily useful for basic download commands.
        """
        
        if variable not in C.CONST:
            raise ValueError("Incorrect variable.")
        
        # Get CMIP5 image collection
        CMIP5 = ee.ImageCollection('NASA/NEX-DCP30_ENSEMBLE_STATS') \
                  .filterDate(start_date, end_date) \
                  .select(variable) \
                  .filter(ee.Filter.eq('scenario', scenario)) \

        timeseries = ee.FeatureCollection(CMIP5.map(lambda img: img.multiply(C.CONST[variable]["multiply"]) \
                                                                    .add(C.CONST[variable]["add"]) \
                                                                    .reduceRegions(geom,ee.Reducer.mean(),500) \
                                                                    .first() \
                                                                    .set('date', ee.Date(img.date()).format('YYYY-MM'))
                                                   )
                                         )

        # Possible destinations for the downloaded files: 
        # toDrive; toCloud; toAsset. We can add support for other destinations later as and when needed.
        desc_name = f"{name}_{state}_{scenario}_{variable}_monthly"
        my_task = ee.batch.Export.table.toDrive(
                            collection = timeseries,
                            fileFormat='csv',
                            folder = os.path.join(self.folder, scenario, variable),
                            description = desc_name,
                            selectors=['date','mean'])
        my_task.start()
        print(f"Downloading... {desc_name}")
        return my_task

    
    
    def _download_samples_util(self, download_config: List[object], params: dict, mode: str) -> None:
        """Private utility function to download all the data samples from Google Earth Engine.
        
        Args:
            download_config (List[object]): List of parameters containing a single download configuration.
                item 0: Tuple of site Latitude, Longitude, NameMnemonic, and StateCode
                item 1: Variable
                item 2: Model
                item 3: Scenario
            params (dict): Dictionary of YAML file parameters.
            mode (str): Type of dataset to download from the Google Earth Engine.
                Possible values: 'average_daily' | 'daily' | 'monthly'
        
        Raises:
            ee.ee_exception.EEException: Raises this expection if there is some issue with Google Earth Engine authentication.
            ValueError: Raises this exception in following conditions:
                1. if the number of items in download_config List is not 4.
                2. if the value for mode is anything other than the 3 options mentioned above.
        """
        
        # Initialize Google Earth Engine
        try:
            ee.Initialize()
        except ee.ee_exception.EEException as ee_exp:
            raise Exception(f"{ee_exp}\n\n\n \
                   Encountered issue with the Google Earth Engine Authentication. \
                   Try again after proper authentication.\n \
                   Try the following commands to authenticate using commandline: \
                       'https://developers.google.com/earth-engine/guides/command_line'.\n \
                   OR, Use the following link to authenticate using python: \
                       'https://developers.google.com/earth-engine/guides/service_account'.\n")
        
        # Making sure that there are expected number of values in the configuration vector
        if len(download_config) != 4:
            raise ValueError(f"Incorrect number of parameters in the download_config vector. 4 expected, found {len(download_config)}")
        
        # Extracting individual values from the configuration vector
        llns_i, variable_i, model_i, scenario_i = download_config
        
        lat, long, name, state = llns_i
        geoPoint = ee.Geometry.Point(long, lat)
        
        start_date = datetime.strptime(params["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(params["end_date"], "%Y-%m-%d")
        
        # Downloading data based on the mode selected
        if mode == "average_daily":
            self.download_model_average_daily(
                start_date=start_date, 
                end_date=end_date, 
                variable=variable_i, 
                scenario=scenario_i, 
                geom=geoPoint, 
                name=name, 
                state=state,
            )
            
        elif mode == "daily":
            self.download_historical_daily(
                start_date=start_date, 
                end_date=end_date, 
                variable=variable_i, 
                scenario=scenario_i, 
                model=model_i, 
                geom=geoPoint, 
                name=name, 
                state=state,
            )
            
        elif mode == "monthly":
            self.download_historical_monthly(
                start_date=start_date, 
                end_date=end_date, 
                variable=variable_i, 
                scenario=scenario_i, 
                model=model_i, 
                geom=geoPoint, 
                name=name, 
                state=state,
            )
            
        else:
            raise ValueError("Incorrect value for mode.")
    
    
    def download_samples(self, params_yaml_file: str, mode: str) -> None:
        """Download all the data samples from the Google Earth Engine based on
        YAML file download configuration parameters.
        
        Args:
            params_yaml_files (str): Path to the YAML file containing all the download configuration parameters.
            mode (str): Type of dataset to download from Google Earth Engine.
        """
        
        params = utils.parse_input_yaml(params_yaml_file)
        print("STATUS UPDATE: Parsed YAML Params.")
        
        # latitude (l), longitude (l), name mnemonic (n), state code (s)
        llns = list(zip(self.sites.Latitude, self.sites.Longitude, self.sites.NameMnemonic, self.sites.StateCode))
        
        # All download configuration permutations
        download_configs = list(itertools.product(
            llns, 
            params["variables"], 
            params["models"], 
            params["scenario_future"],
        ))
        print(f"STATUS UPDATE: Generated {len(download_configs)} download configurations.")
        
        # # Single node download process
        # for config_i in download_configs:
        #     self._download_samples_util(download_config=config_i, params=params, mode=mode)
        
        # Parallel download process
        parallel_function(
            delayed(self._download_samples_util)(
                download_config=config_i, 
                params=params, 
                mode=mode
            )
            for config_i in download_configs
        )
