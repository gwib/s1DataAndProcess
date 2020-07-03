# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:26:33 2020

@author: galinavj
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### HELPER FUNCTIONS
def nanForNeg(x):
    if x < 0:
        return np.nan
    else: return x

# Windows
prcpFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
snwDepthFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
metFile = "m:\\Documents\\thesis\\data\\weather\\View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"

# Home
prcpFile = "/Volumes/ElementsSE/thesisData/weather/View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
snwDepthFile = "/Volumes/ElementsSE/thesisData/weather/View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
metFile = "/Volumes/ElementsSE/thesisData/weather/View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"


prcp = pd.read_csv(prcpFile, delimiter="\t", encoding="unicode_escape")
snowDepth = pd.read_csv(snwDepthFile, delimiter="\t", encoding="unicode_escape")
met = pd.read_csv(metFile, delimiter="\t", encoding="unicode_escape")

# snow depth
snowDepth['Date'] = snowDepth[snowDepth.columns[0]]
snowDepth_new = snowDepth[['Date', 'SD (m)']].copy()
aggregation_functions_snowDepth = {'SD (m)': 'mean'} # snow depth

snowDepthDaily = snowDepth_new.groupby(snowDepth_new['Date']).aggregate(aggregation_functions_snowDepth)

snowDepthDaily['SnwDepth_avg'] = snowDepthDaily['SD (m)'].apply(lambda x: nanForNeg(x))

# Precipitation
prcp['Date'] = prcp[prcp.columns[0]]
prcp_new = prcp[['Date', 'PRE (mm)']].copy()
aggr_func_prcp = {'PRE (mm)': 'sum'}
# total precipitation per day
prcpDaily = prcp_new.groupby(prcp_new['Date']).aggregate(aggr_func_prcp)
# remove precipitation < 0
prcpDaily['prcp'] = prcpDaily['PRE (mm)'].apply(lambda x: nanForNeg(x))


plt.plot(list(snowDepthDaily.index), list(snowDepthDaily['SnwDepth_avg']))
plt.savefig('/Volumes/Transcend1/IIKT/thesis/report/plots/snowDepth.png')

plt.plot(list(prcpDaily.index), list(prcpDaily['prcp']))
plt.savefig('/Volumes/Transcend1/IIKT/thesis/report/plots/prcp.png')