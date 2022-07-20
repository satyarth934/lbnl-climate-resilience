# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import datetime
import probscale
import sys
import os
from pandas.core.arrays.numeric import T

#from google.colab import drive
#drive.mount('/content/drive')

#curdir = '/content/drive/MyDrive/EM_Climate_Resilience/Bias_Correction/'
#datadir = '/content/drive/MyDrive/EM_Climate_Resilience/ClimateData/'
#obsdir = '/content/drive/MyDrive/EM_Climate_Resilience/Observational_Data/Processed/'
#sys.path.append(datadir)
#sys.path.append(curdir+'/ec20_hamman_etal')

from skdownscale.pointwise_models import BcsdTemperature, BcsdPrecipitation
models_temp = {'BCSD: BcsdTemperature': BcsdTemperature(return_anoms=False)}
models_prec = {'BCSD: BcsdPrecipitation': BcsdPrecipitation(return_anoms=False)}

#variable_short = "Pr" for Precipitation
#variable_short = "Tmax" for Temperature_Max
#variable_short = "Tmax" for Temperature_Max

"""## Read CMIP5 climate model data (this is what we downloaded and processed)"""

# TO READ FROM THE ENSEMBLE AVERAGE
def read_ensemble_average(sitename, state, variable_short, modeldir):
  hist = pd.read_csv(modeldir+variable_short+'/historical_' + variable_short + '_ensemble/'+ sitename +'_'+ state +'_historical_' + variable_short + '.csv')
  rcp45 = pd.read_csv(modeldir+variable_short+ '/rcp45_' + variable_short + '_ensemble/'+ sitename +'_'+ state +'_rcp45_' + variable_short + '.csv')
  rcp85 = pd.read_csv(modeldir+ variable_short + '/rcp85_' + variable_short + '_ensemble/'+ sitename +'_'+ state +'_rcp85_' + variable_short + '.csv')
  cmip_hist_rcp85 = pd.concat([hist, rcp45, rcp85])
  cmip_hist_rcp85 = cmip_hist_rcp85.set_index("date")
  cmip_hist_rcp85.index = pd.to_datetime(cmip_hist_rcp85.index)
  return cmip_hist_rcp85

def read_individual_model(sitename, state, modelname, var,modeldir):
  hist = pd.read_csv(modeldir+ var + '/historical_' + var + '/'+ sitename +'_'+ state + '/'+ sitename +'_'+ state +'_historical_' + var + '_'  + modelname +'.csv')
  rcp45 = pd.read_csv(modeldir+ var + '/rcp45_' + var + '/'+ sitename +'_'+ state + '/'+ sitename +'_'+ state +'_rcp45_'+ var + '_'  + modelname +'.csv')
  rcp85 = pd.read_csv(modeldir+ var + '/rcp85_' + var + '/'+ sitename +'_'+ state + '/'+ sitename +'_'+ state +'_rcp85_' + var + '_' + modelname +'.csv')
  cmip_hist_rcp85 = pd.concat([hist, rcp45, rcp85])

  if "Date" in cmip_hist_rcp85.columns:
      cmip_hist_rcp85.index = pd.date_range(start=cmip_hist_rcp85["Date"][0], periods = len(cmip_hist_rcp85), freq='D')
  if "date" in cmip_hist_rcp85.columns:
      cmip_hist_rcp85.index = pd.date_range(start=cmip_hist_rcp85["date"][0], periods = len(cmip_hist_rcp85), freq='D')


  return cmip_hist_rcp85

"""## Read observation data provided by the sites
Note that the format of this dataset varies 
"""

def read_observation_data(site, var,obsdir):
  for filename in os.listdir(obsdir  + "Site_" + var +"/"):
    if site in filename: 
      data = pd.read_csv(obsdir + "Site_" + var + "/" +filename)
      data = pd.read_csv(obsdir + "Site_" + var + "/" +filename)
      if "Date" in data.columns:
        data = data.set_index('Date')
      if "date" in data.columns:
        data = data.set_index('date')

      return data

"""## Call BCSD function to fit the data"""

# will need to have the files in https://github.com/earthcube2020/ec20_hamman_etal
# in the same directory or link to the directory to be able to call these two BCSD functions
# For temperature (tasmax), use BcsdTemperature
# For precipitation, use BcsdPrecipitation

def run_model(data,cmip_hist_rcp85, variable_short):
  if variable_short == "Pr":
    models = models_prec
  else:
    models = models_temp

  data.index = data.index.astype('datetime64[ns]')
  cmip_hist_rcp85.index = cmip_hist_rcp85.index.astype('datetime64[ns]')
  merged = pd.merge(data, cmip_hist_rcp85, left_index=True, right_index=True,how="inner")

  data = data.loc[merged.index].dropna()
  cmip_hist_rcp85 = cmip_hist_rcp85.loc[data.index].dropna()

  if variable_short == "Tmax":
    if variable_short not in data.columns:
      variable_short = "Tmean"

  
  print(data.columns)

  train_data = data[(data.index<np.percentile(data.index, 80))]
  val_data = data[(data.index>np.percentile(data.index, 80))]
  train_slice = slice(train_data.index[0], train_data.index[-1])
  validate_slice = slice(val_data.index[0], val_data.index[-1])

  X_train = pd.DataFrame(cmip_hist_rcp85['mean'][train_slice])
  X_train.columns = [variable_short]

  y_train = pd.DataFrame(data[variable_short][train_slice])
  y_train.columns = [variable_short]
  y_train.index.name='date'

  X_validate = pd.DataFrame(cmip_hist_rcp85['mean'][validate_slice])
  X_validate.columns = [variable_short]

  y_validate = pd.DataFrame(data[variable_short][validate_slice])
  y_validate.columns = [variable_short]

  for key, model in models.items():
    model.fit(X_train, y_train)

  for key, model in models.items():
    y_predict = model.predict(X_validate)

  return X_train, y_train , X_validate, y_validate, y_predict,variable_short

def plot_1(X_validate,y_validate , y_predict, variable_short, site =""):
  if variable_short == "Pr":
    unit = "(mm)"
  else:
    unit = "(C)"
  fig = plt.figure(figsize=(12,6))

  ax1 = fig.add_subplot(111)
  ax1.set_xlabel('Dates')
  ax1.set_ylabel(variable_short + " " + unit, color='k')
  ax1.set_title(site + variable_short )
  ax1.plot(X_validate.index, X_validate[variable_short], y_validate.index, y_validate[variable_short], y_predict.index, y_predict[variable_short])
  ax1.tick_params(axis='y', labelcolor='k')
  ax1.legend(['original (cmip5)','target (observation)','corrected (BSCD)'])
  
# ax1.set_xlim((datetime.date(1950, 1, 1), datetime.date(2000, 1, 1)))

def plot_2(X_validate,y_validate , y_predict, variable_short, site="", outdir):

  if variable_short == "Pr":
    unit = "(mm)"
  else:
    unit = "(C)"
  fig, axs = plt.subplots(2, 3, figsize=(20, 15))

  for i in range(6):
      ax1 = axs[i//3, i%3]
      ax1.set_xlabel('Dates')
      ax1.set_ylabel(variable_short + " " + unit, color='k')
      ax1.plot(X_validate.index, X_validate[variable_short], y_validate.index, y_validate[variable_short], y_predict.index, y_predict[variable_short])

      ax1.legend(['original (cmip5)','target (observation)','corrected (BSCD)'])
      year = 2000+i
      ax1.set_xlim((datetime.date(year, 1, 1), datetime.date(year+1, 1, 1)))    
      ax1.set_title(str(year) + site + variable_short)
  fig.tight_layout()
  # fig.savefig(curdir+'annual_tmax_CESM1.png')
  fig.savefig(outdir+'annual_' + variable_short +'.png')

def prob_plots(x, y, y_hat, variable, shape=(2, 2), figsize=(8, 8)):

    fig, axes = plt.subplots(*shape, sharex=True, sharey=True, figsize=figsize)

    scatter_kws = dict(label="", marker=None, linestyle="-")
    common_opts = dict(plottype="qq", problabel="", datalabel="")

    for ax, (label, series) in zip(axes.flat, y_hat.items()):

        scatter_kws["label"] = "original"
        fig = probscale.probplot(x, ax=ax, scatter_kws=scatter_kws, **common_opts)

        scatter_kws["label"] = "target"
        fig = probscale.probplot(y, ax=ax, scatter_kws=scatter_kws, **common_opts)

        scatter_kws["label"] = "corrected"
        fig = probscale.probplot(series, ax=ax, scatter_kws=scatter_kws, **common_opts)
        ax.set_title(label)
        ax.legend()

    [ax.set_xlabel("Standard Normal Quantiles") for ax in axes[-1]]
    [ax.set_ylabel(variable) for ax in axes[:, 0]]
    [fig.delaxes(ax) for ax in axes.flat[len(y_hat.keys()) :]]
    fig.tight_layout()

    return fig


def plot_3(X_validate,y_validate , y_predict,variable_short, site=""):
  fig = prob_plots(X_validate, y_validate[variable_short], y_predict, variable_short, shape=(2, 2), figsize=(12, 12))
  fig.suptitle(site + variable_short )

def data_time_series(y_predict, directory, outdir):
  print(curdir+ "Processed" + directory)
  y_predict.to_csv(outdir+ "Processed/" + directory)







