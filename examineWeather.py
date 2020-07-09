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
#prcpFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
#snwDepthFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
#metFile = "m:\\Documents\\thesis\\data\\weather\\View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"

# Home
prcpFile = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
snwDepthFile = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
tempFile = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/qeqertarsuaq-heliport-daily-20192020.csv"
#metFile = "/Volumes/ElementsSE/thesisData/weather/View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"


prcp = pd.read_csv(prcpFile, delimiter="\t", encoding="unicode_escape")
snowDepth = pd.read_csv(snwDepthFile, delimiter="\t", encoding="unicode_escape")
temp = pd.read_csv(tempFile, delimiter=";")#, encoding="unicode_escape")

temp['Date'] = temp.DateTime.apply(lambda x: x.split()[0])
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

prcpDaily1920 = prcpDaily.loc[prcpDaily.index >= '2019-04-12']
snowDepthDaily1920 = snowDepthDaily.loc[snowDepthDaily.index >= '2019-04-12']
temp = temp.loc[temp.Date >= '2019-04-12']

def plotSnwPrcp():
    # subplot with shared x-axis
    fig=plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    
    ax1.plot(prcpDaily1920.index, prcpDaily1920.prcp)
    ax2.plot(snowDepthDaily1920.index, snowDepthDaily1920.SnwDepth_avg)
        
    ax1.set_title('Precipitation')
    ax2.set_title('Snow Depth')
    
    ax1.set_ylabel('Precipitation [mm]')
    ax2.set_ylabel('Snow depth [m]')
        
    #fig.suptitle('Histogram for polarisation on '+splitDate, fontsize=14)
    
    ax1.get_shared_x_axes().join(ax1, ax2)
    ax2.set_xticklabels(list(prcpDaily1920.index))
    ax2.autoscale() ## call autoscale if needed
        
    plt.show()


def subplotsSnwPrcp():
    dates = snowDepthDaily1920.index
    fig2, axs2 = plt.subplots(2, sharex=True)
    axs2[0].plot(dates, snowDepthDaily1920.SnwDepth_avg)
    axs2[1].plot(dates, prcpDaily1920.prcp)
    axs2[2].plot()
    
    axs2[0].set_ylabel('Avarage daily snow depth [m]', fontsize=8)
    axs2[1].set_ylabel('Daily precipitation [mm]', fontsize=8)
    axs2[1].set_xlabel('Date', fontsize=8)
#plt.plot(list(snowDepthDaily.index), list(snowDepthDaily['SnwDepth_avg']))
#plt.savefig('/Volumes/Transcend1/IIKT/thesis/report/plots/snowDepth.png')


def plotTemp():
#=============================================================================
# =============================================================================
#     d = temp.Date
#     plt.plot(d,temp.Middel)
#     plt.plot(d,temp.Laveste, '--')
#     plt.plot(d, temp.Højeste, '--')
#     # Customize the tickes on the graph
#     plt.xticks(d,rotation=45, fontsize=10)   
#     plt.xlabel('Date')
#     plt.ylabel('Temperature [°C]')
#     plt.title('Temperatures on Disko Island April 2019 - April 2020')
#     plt.rcParams["figure.figsize"] = (40,5)
# =============================================================================
#=============================================================================

# =============================================================================
     fig, ax = plt.subplots()
     d = temp.Date
     ax.plot(d,temp.Middel, linewidth=1)
     ax.plot(d,temp.Laveste, '--', linewidth=0.5)
     ax.plot(d, temp.Højeste, '--', linewidth=0.5)
     #ax.set_xticks(ax.get_xticks()[::10])
      #ax.xticks.set_tick_params()
     ax.set_title('Temperatures at Qeqertarsuaq Heliport')
     ax.set_xlabel('Date')
     ax.set_ylabel('Temperature [°C]')
     fig.autofmt_xdate(bottom=0.2)
     fig.set_dpi(200)
     plt.show()
     fig.show()
# =============================================================================
     #plt.show()
# =============================================================================
#plt.plot(list(prcpDaily.index), list(prcpDaily['prcp']))
#plt.savefig('/Volumes/Transcend1/IIKT/thesis/report/plots/prcp.png')