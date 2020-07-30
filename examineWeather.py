# -*- coding: utf-8 -*-

"""
Created on Fri Jul  3 10:26:33 2020

@author: galinavj
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from colours import colorDict
import datetime as dt

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
tempFile1920 = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/temp19-20/qeqertarsuaq-heliport-daily-20192020.csv"
metFile = "/Volumes/ElementsSE/thesisData/weather/View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"


def readTempFromFile(tempFp):
    temp_df = pd.read_csv(tempFp, delimiter=";")
    temp_df['Date'] = temp_df.DateTime.apply(lambda x: dt.datetime.strptime(x.split()[0], '%Y-%m-%d'))
    return temp_df

def readPrcpFile(prcpFile):
    prcp = pd.read_csv(prcpFile, delimiter="\t", encoding="unicode_escape")
    # Precipitation
    prcp['Date'] = prcp[prcp.columns[0]]
    prcp['Datetime'] = prcp['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
    prcp_new = prcp[['Datetime', 'PRE (mm)']].copy()
    aggr_func_prcp = {'PRE (mm)': 'sum'}
    # total precipitation per day
    prcpDaily = prcp_new.groupby(prcp_new['Datetime']).aggregate(aggr_func_prcp)
    # remove precipitation < 0
    prcpDaily['prcp'] = prcpDaily['PRE (mm)'].apply(lambda x: nanForNeg(x))
    return prcpDaily

def readSnwDepth(snwDepthFile):
    snowDepth = pd.read_csv(snwDepthFile, delimiter="\t", encoding="unicode_escape")
    snowDepth['Date'] = snowDepth[snowDepth.columns[0]]
    snowDepth['Datetime'] = snowDepth['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
    snowDepth_new = snowDepth[['Datetime', 'SD (m)']].copy()
    aggregation_functions_snowDepth = {'SD (m)': 'mean'} # snow depth
    
    snowDepthDaily = snowDepth_new.groupby(snowDepth_new['Datetime']).aggregate(aggregation_functions_snowDepth)
    snowDepthDaily['SnwDepth_avg'] = snowDepthDaily['SD (m)'].apply(lambda x: nanForNeg(x))
    
    return snowDepthDaily

# =============================================================================
# 
# # Precipitation
# prcp1920 = pd.read_csv(prcpFile1920, delimiter="\t", encoding="unicode_escape")
# prcp1920['Date'] = prcp1920[prcp1920.columns[0]]
# prcp1920['Datetime'] = prcp1920['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
# prcp_new1920 = prcp1920[['Datetime', 'PRE (mm)']].copy()
# aggr_func_prcp = {'PRE (mm)': 'sum'}
# # total precipitation per day
# prcpDaily1920 = prcp_new1920.groupby(prcp_new1920['Datetime']).aggregate(aggr_func_prcp)
# # remove precipitation < 0
# prcpDaily1920['prcp'] = prcpDaily1920['PRE (mm)'].apply(lambda x: nanForNeg(x))# Precipitation
# prcp1920['Date'] = prcp1920[prcp1920.columns[0]]
# prcp1920['Datetime'] = prcp1920['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
# prcp_new1920 = prcp1920[['Datetime', 'PRE (mm)']].copy()
# aggr_func_prcp = {'PRE (mm)': 'sum'}
# # total precipitation per day
# prcpDaily1920 = prcp_new1920.groupby(prcp_new1920['Datetime']).aggregate(aggr_func_prcp)
# # remove precipitation < 0
# prcpDaily1920['prcp'] = prcpDaily1920['PRE (mm)'].apply(lambda x: nanForNeg(x))
#
# Snow Depth
# snowDepth1920 = pd.read_csv(snwDepthFile1920, delimiter="\t", encoding="unicode_escape")
# snowDepth1920['Date'] = snowDepth1920[snowDepth1920.columns[0]]
# snowDepth1920['Datetime'] = snowDepth1920['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
# snowDepth1920_new = snowDepth1920[['Datetime', 'SD (m)']].copy()
# aggregation_functions_snowDepth = {'SD (m)': 'mean'} # snow depth

# snowDepth1920Daily = snowDepth1920_new.groupby(snowDepth1920_new['Datetime']).aggregate(aggregation_functions_snowDepth)

# snowDepth1920Daily['SnwDepth_avg'] = snowDepth1920Daily['SD (m)'].apply(lambda x: nanForNeg(x))
# =============================================================================




temp1920 = readTempFromFile(tempFile1920)
prcpDaily= readPrcpFile(prcpFile)
snowDepthDaily = readSnwDepth(snwDepthFile)



prcpDaily1920 = prcpDaily.loc[prcpDaily.index >= dt.datetime(2019, 4, 12)]
snowDepthDaily1920 = snowDepthDaily.loc[snowDepthDaily.index >= dt.datetime(2019, 4, 12)]
temp1920 = temp1920.loc[temp1920.Date >= dt.datetime(2019, 4, 12)]

snowDepthDaily1619 = snowDepthDaily.loc[snowDepthDaily.index >= dt.datetime(2016, 4, 1)]
snowDepthDaily1619 = snowDepthDaily1619.loc[snowDepthDaily1619.index <= dt.datetime(2019, 12, 30)]
prcpDaily1619 = prcpDaily.loc[prcpDaily.index >= dt.datetime(2016, 4, 1)]
prcpDaily1619 = prcpDaily1619.loc[prcpDaily1619.index <= dt.datetime(2019, 12, 30)]

def subplotsSnwPrcp():
    dates = snowDepthDaily1920.index
    fig2, axs2 = plt.subplots(2, sharex=True)
    axs2[0].plot(dates, snowDepthDaily1920.SnwDepth_avg)
    axs2[1].plot(dates, prcpDaily1920.prcp)
    axs2[2].plot()
    
    axs2[0].set_ylabel('Average daily snow depth [m]', fontsize=8)
    axs2[1].set_ylabel('Daily precipitation [mm]', fontsize=8)
    axs2[1].set_xlabel('Date', fontsize=8)
#plt.plot(list(snowDepthDaily.index), list(snowDepthDaily['SnwDepth_avg']))
#plt.savefig('/Volumes/Transcend1/IIKT/thesis/report/plots/snowDepth.png')

def pltSnwPrcp(snowDepthDaily,prcpDaily):
    fig, ax1 = plt.subplots(dpi=200)
    
    color=colorDict['blue']
    ax1.set_xlabel('Date')
    ax1.set_ylabel(r'Snow depth in $m$', color=color)
    ax1.plot(snowDepthDaily.index, snowDepthDaily.SnwDepth_avg, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    #ax1.grid(color=colorDict['black15'], linestyle='-')
    ax1.set_facecolor('w')
    color='#000000'
    ax2 = ax1.twinx()
    ax2.set_ylabel(r'Precipitation in $mm$', color=color)
    ax2.bar(prcpDaily.index, prcpDaily.prcp, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    #ax2.grid(color=colorDict['black45'])
    #plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    #plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    for ax in fig.get_axes():
        if ax.is_last_row():
            for label in ax.get_xticklabels():
                label.set_ha('right')
                label.set_rotation(30.)
        else:
            for label in ax.get_xticklabels():
                label.set_visible(False)
            ax.set_xlabel('')
    fig.subplots_adjust(bottom=0.15)
    fig.tight_layout()
    align_yaxis_np(ax1,ax2)
    #fig.set_dpi(200)
    plt.show()
    

def plotTemp(temp):
     #fig, ax = plt.subplots()
     fig = plt.figure(dpi=200)
     ax = fig.subplots(1)
     d = temp.Date
     ax.plot(d,temp.Middel, linewidth=1)
     ax.plot(d,temp.Laveste, '--', linewidth=0.3)
     ax.plot(d, temp.Højeste, '--', linewidth=0.3)
     #ax.set_xticks(ax.get_xticks()[::10])
      #ax.xticks.set_tick_params()
     #ax.set_title('Temperatures at Qeqertarsuaq Heliport')
     ax.set_xlabel('Date')
     ax.set_ylabel(r'Temperature in $°C$')
     
     for ax in fig.get_axes():
        if ax.is_last_row():
            for label in ax.get_xticklabels():
                label.set_ha('right')
                label.set_rotation(30.)
        else:
            for label in ax.get_xticklabels():
                label.set_visible(False)
            ax.set_xlabel('')
     #fig.subplots_adjust(bottom=0.15)
     
     fig.subplots_adjust(bottom=0.24)
     fig.show()

def plotPrcp():
     #fig, ax = plt.subplots()
     fig = plt.figure(dpi=200)
     ax = fig.subplots(1)
     d = temp1920.Date
     ax.plot(d,temp1920.Middel, linewidth=1)
     ax.plot(d,temp1920.Laveste, '--', linewidth=0.3)
     ax.plot(d, temp1920.Højeste, '--', linewidth=0.3)
     #ax.set_xticks(ax.get_xticks()[::10])
      #ax.xticks.set_tick_params()
     #ax.set_title('Temperatures at Qeqertarsuaq Heliport')
     ax.set_xlabel('Date')
     ax.set_ylabel(r'Temperature in $°C$')
     fig.autofmt_xdate(bottom=0.2)
     fig.subplots_adjust(bottom=0.24)
     fig.show()
     
def align_yaxis_np(ax1, ax2):
    """Align zeros of the two axes, zooming them out by same ratio"""
    axes = np.array([ax1, ax2])
    extrema = np.array([ax.get_ylim() for ax in axes])
    tops = extrema[:,1] / (extrema[:,1] - extrema[:,0])
    # Ensure that plots (intervals) are ordered bottom to top:
    if tops[0] > tops[1]:
        axes, extrema, tops = [a[::-1] for a in (axes, extrema, tops)]

    # How much would the plot overflow if we kept current zoom levels?
    tot_span = tops[1] + 1 - tops[0]

    extrema[0,1] = extrema[0,0] + tot_span * (extrema[0,1] - extrema[0,0])
    extrema[1,0] = extrema[1,1] + tot_span * (extrema[1,0] - extrema[1,1])
    [axes[i].set_ylim(*extrema[i]) for i in range(2)]