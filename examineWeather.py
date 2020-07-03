# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:26:33 2020

@author: galinavj
"""

import pandas as pd
import matplotlib.pyplot as plt

prcpFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
snwDepthFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
metFile = "m:\\Documents\\thesis\\data\\weather\\View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"

prcp = pd.read_csv(prcpFile, delimiter="\t", encoding="unicode_escape")
snowDepth = pd.read_csv(snwDepthFile, delimiter="\t", encoding="unicode_escape")
met = pd.read_csv(metFile, delimiter="\t", encoding="unicode_escape")

snowDepth['Date'] = snowDepth[snowDepth.columns[0]]
snowDepth_new = snowDepth[['Date', 'SD (m)']].copy()
aggregation_functions_snowDepth = {'SD (m)': 'mean'} # snow depth

snowDepthDaily = snowDepth_new.groupby(snowDepth_new['Date']).aggregate(aggregation_functions_snowDepth)

# Precipitation
prcp['Date'] = prcp[prcp.columns[0]]
prcp_new = prcp[['Date', 'PRE (mm)']].copy()
aggr_func_prcp = {'PRE (mm)': 'sum'}
prcpDaily = prcp_new.groupby(prcp_new['Date']).aggregate(aggr_func_prcp)

plt.plot(snowDepthDaily.index, snowDepthDaily['SD (m)'])
plt.show()

plt.plot(prcpDaily.index, prcpDaily['PRE (mm)'])
plt.show()